// Shared profile hydration. Static HTML remains the first-paint fallback;
// this layer keeps homepage and CV fields synchronized after profile.json loads.
(function () {
  const PROFILE_URL = 'assets/data/profile.json?v=2';

  function language() {
    const fromUrl = new URLSearchParams(window.location.search).get('lang');
    if (fromUrl === 'en' || fromUrl === 'vi') return fromUrl;
    return localStorage.getItem('portfolio_lang') === 'en' ? 'en' : 'vi';
  }

  function findExperience(profile, company) {
    return profile.experience.find((entry) => entry.company === company);
  }

  function localized(value, lang) {
    if (value && typeof value === 'object') return value[lang] || value.vi || value.en || '';
    return value || '';
  }

  function setLocalized(node, value, lang) {
    if (node) node.textContent = localized(value, lang);
  }

  function hydrate(profile) {
    const lang = language();
    document.querySelectorAll('[data-profile-role]').forEach((node) => {
      node.textContent = profile.titles.primary;
    });

    document.querySelectorAll('[data-profile-summary]').forEach((node) => {
      setLocalized(node, profile.bio, lang);
    });

    document.querySelectorAll('[data-profile-location]').forEach((node) => {
      setLocalized(node, profile.identity?.location, lang);
    });

    const education = profile.education?.[0];
    if (education) {
      document.querySelectorAll('[data-profile-education-school]').forEach((node) => {
        setLocalized(node, education.school, lang);
      });
      document.querySelectorAll('[data-profile-education-major]').forEach((node) => {
        setLocalized(node, education.major, lang);
      });
      document.querySelectorAll('[data-profile-education-date]').forEach((node) => {
        node.textContent = `${education.start} – ${education.end}`;
      });
      document.querySelectorAll('[data-profile-education-description]').forEach((node) => {
        setLocalized(node, education.description, lang);
      });
    }

    document.querySelectorAll('[data-profile-strength-index]').forEach((node) => {
      const item = profile.strengths?.[Number(node.dataset.profileStrengthIndex)];
      if (!item) return;
      const content = node.querySelector('p') || node;
      let title = content.querySelector('[data-profile-strength-title]');
      let description = content.querySelector('[data-profile-strength-description]');
      if (!title || !description) {
        content.innerHTML = '';
        title = document.createElement('strong');
        title.dataset.profileStrengthTitle = '';
        description = document.createElement('span');
        description.dataset.profileStrengthDescription = '';
        content.append(title, description);
      }
      setLocalized(title, item.title, lang);
      setLocalized(description, item.description, lang);
    });

    document.querySelectorAll('[data-profile-specialty-index]').forEach((node) => {
      const item = profile.specialties?.[Number(node.dataset.profileSpecialtyIndex)];
      if (!item) return;
      setLocalized(node.querySelector('[data-profile-specialty-title]'), item.title, lang);
      setLocalized(node.querySelector('[data-profile-specialty-description]'), item.description, lang);
    });

    document.querySelectorAll('[data-profile-experience]').forEach((node) => {
      const entry = findExperience(profile, node.dataset.profileExperience);
      if (!entry) return;
      const title = node.querySelector('[data-profile-company]');
      const role = node.querySelector('[data-profile-role-name]');
      const date = node.querySelector('[data-profile-date]');
      const description = node.querySelector('[data-profile-description]');
      if (title) title.textContent = entry.company;
      setLocalized(role, entry.role, lang);
      if (date) date.textContent = `${entry.start} – ${entry.end}`;
      if (description) {
        if (description.tagName === 'UL' || description.tagName === 'OL') {
          description.innerHTML = '';
          entry.description[lang].forEach((line) => {
            const item = document.createElement('li');
            item.textContent = line;
            description.appendChild(item);
          });
        } else {
          description.textContent = entry.description[lang].join(' ');
        }
      }
    });

    const logo = profile.brand.seosonaLogo;
    document.querySelectorAll('[data-profile-logo="seosona"]').forEach((image) => {
      if (image.dataset.src !== undefined) {
        image.dataset.src = logo;
        window.portfolioMedia?.observe(image);
      } else {
        image.src = logo;
      }
      image.alt = 'SEOSONA';
    });
    document.documentElement.dataset.profileLoaded = 'true';
    window.dispatchEvent(new CustomEvent('portfolio:profileloaded', { detail: profile }));
  }

  window.addEventListener('portfolio:languagechange', () => {
    if (window.__portfolioProfile) hydrate(window.__portfolioProfile);
  });
  window.addEventListener('message', (event) => {
    if (event.data?.type === 'LANG_TOGGLE' && window.__portfolioProfile) hydrate(window.__portfolioProfile);
  });
  fetch(PROFILE_URL)
    .then((response) => response.ok ? response.json() : Promise.reject(new Error('profile unavailable')))
    .then((profile) => {
      window.__portfolioProfile = profile;
      hydrate(profile);
    })
    .catch(() => {
      document.documentElement.dataset.profileLoaded = 'fallback';
    });
})();
