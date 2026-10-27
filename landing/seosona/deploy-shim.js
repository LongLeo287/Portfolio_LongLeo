(() => {
  'use strict';

  const root = document.documentElement;
  root.classList.add('js');

  const header = document.querySelector('[data-header]');
  const progress = document.querySelector('[data-progress]');
  const menuButton = document.querySelector('[data-menu-toggle]');
  const mobileNav = document.getElementById('mobile-nav');
  const menuLabel = menuButton?.querySelector('.sr-only');
  const reducedMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
  const finePointer = window.matchMedia?.('(pointer: fine)').matches;
  const afr = window.portfolioAFR;
  let motionMode = 'full';
  const applyAfrProfile = (nextProfile) => {
    const mode = nextProfile?.mode || 'full';
    motionMode = mode === 'static' ? 'off' : mode === 'lite' ? 'soft' : 'full';
    root.dataset.motion = motionMode;
  };
  applyAfrProfile(afr?.getProfile());
  window.addEventListener('portfolio:afrprofilechange', (event) => applyAfrProfile(event.detail), { passive: true });

  const setMenuState = (isOpen) => {
    if (!menuButton || !mobileNav) return;
    menuButton.setAttribute('aria-expanded', String(isOpen));
    mobileNav.hidden = !isOpen;
    if (menuLabel) menuLabel.textContent = isOpen ? 'Đóng menu' : 'Mở menu';
  };

  menuButton?.addEventListener('click', () => setMenuState(menuButton.getAttribute('aria-expanded') !== 'true'));
  mobileNav?.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => setMenuState(false)));
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') setMenuState(false);
  });

  let frame = 0;
  const updateScrollState = () => {
    frame = 0;
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    const value = maxScroll > 0 ? Math.min(100, Math.max(0, (window.scrollY / maxScroll) * 100)) : 0;
    header?.classList.toggle('is-scrolled', window.scrollY > 10);
    if (progress) progress.style.width = `${value}%`;
  };
  const scheduleScrollState = () => {
    if (!frame) frame = window.requestAnimationFrame(updateScrollState);
  };
  window.addEventListener('scroll', scheduleScrollState, { passive: true });
  window.addEventListener('resize', scheduleScrollState, { passive: true });
  updateScrollState();

  const revealItems = document.querySelectorAll('[data-reveal]');
  if (reducedMotion || motionMode === 'off' || !('IntersectionObserver' in window)) {
    revealItems.forEach((item) => item.classList.add('is-visible'));
  } else {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        if (entry.target.dataset.revealDelay) entry.target.style.setProperty('--reveal-delay', `${entry.target.dataset.revealDelay}ms`);
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    revealItems.forEach((item) => revealObserver.observe(item));
  }

  if (finePointer) {
    document.querySelectorAll('[data-tilt]').forEach((item) => {
      item.addEventListener('pointermove', (event) => {
        if (motionMode !== 'full') return;
        const bounds = item.getBoundingClientRect();
        const x = (event.clientX - bounds.left) / bounds.width - .5;
        const y = (event.clientY - bounds.top) / bounds.height - .5;
        item.style.setProperty('--tilt-x', `${(y * -2).toFixed(2)}deg`);
        item.style.setProperty('--tilt-y', `${(x * 2).toFixed(2)}deg`);
        item.style.transform = `perspective(1400px) rotateX(var(--tilt-x)) rotateY(var(--tilt-y)) translateY(-4px)`;
      });
      item.addEventListener('pointerleave', () => { item.style.transform = ''; });
    });
  }

  const featureData = {
    growth: {
      index: '01 / FEATURED ROUTE', title: 'Where the system starts.',
      copy: 'Bento system gom các năng lực chính thành những route rõ ràng theo intent — để người dùng không phải đoán nên bắt đầu ở đâu.',
      tags: ['CORE SOLUTIONS', 'IA / ENTRY POINT'], image: 'assets/screen-feature-bento.png',
      alt: 'Bento grid trên homepage SEOSONA với các module SEO, Ads, AI và Data & Automation',
      caption: 'CORE SOLUTIONS / BENTO NAVIGATION', link: 'https://seosona.vercel.app/', linkLabel: 'Mở surface này'
    },
    signal: {
      index: '02 / FEATURED ROUTE', title: 'Make the technical story legible.',
      copy: 'SGE, AI content, Technical SEO và Data Automation được trình bày như một hệ sinh thái có quan hệ — không phải một danh sách jargon.',
      tags: ['DATA LAYER', 'SIGNAL → ACTION'], image: 'assets/screen-ecosystem.png',
      alt: 'Hệ sinh thái công nghệ và dữ liệu của SEOSONA với SGE, tự động hóa content, technical SEO và data automation',
      caption: 'POWERED BY SONATOOLS / DATA LAYER', link: 'https://seosona.vercel.app/giai-phap/', linkLabel: 'Mở data layer'
    },
    proof: {
      index: '03 / FEATURED ROUTE', title: 'Show the result before the ask.',
      copy: 'Case study không còn là phần phụ sau cùng. Metrics, ngành và câu chuyện tăng trưởng tạo trust layer trước khi liên hệ.',
      tags: ['PROOF LAYER', 'METRIC-FIRST'], image: 'assets/screen-case-results.png',
      alt: 'Premium case studies của SEOSONA với các kết quả tăng trưởng doanh thu, lead và traffic',
      caption: 'PREMIUM CASE STUDIES / PROOF LAYER', link: 'https://seosona.vercel.app/case-study/', linkLabel: 'Xem proof layer'
    },
    return: {
      index: '04 / FEATURED ROUTE', title: 'Give people a reason to return.',
      copy: 'Ebook, webinar, workbook và bài viết được xếp thành một discovery layer có thể mở rộng — từ một lần đọc tới next step.',
      tags: ['RESOURCE HUB', 'LEARNING LOOP'], image: 'assets/screen-resource-grid.png',
      alt: 'Resource hub SEOSONA với ebook SEO, webinar AI SEO và workbook Technical SEO',
      caption: 'RESOURCE HUB / CONTENT DISCOVERY', link: 'https://seosona.vercel.app/tai-nguyen/', linkLabel: 'Mở resource hub'
    },
    process: {
      index: '05 / FEATURED ROUTE', title: 'Make the work visible.',
      copy: 'Research → strategy → execution → optimization. Process timeline biến cách làm thành một phần của product story.',
      tags: ['SHIP LOG', 'PARTNERSHIP JOURNEY'], image: 'assets/screen-process.png',
      alt: 'Timeline hành trình hợp tác minh bạch trên homepage SEOSONA với bốn bước từ nghiên cứu đến tối ưu',
      caption: 'PARTNERSHIP JOURNEY / RESEARCH → OPTIMIZATION', link: 'https://seosona.vercel.app/', linkLabel: 'Xem process layer'
    }
  };

  const featureStage = document.querySelector('[data-feature-stage]');
  const featureCards = [...document.querySelectorAll('[data-feature-key]')];
  const featureIndex = document.querySelector('[data-feature-index]');
  const featureTitle = document.querySelector('[data-feature-title]');
  const featureCopy = document.querySelector('[data-feature-copy]');
  const featureTags = document.querySelector('[data-feature-tags]');
  const featureLink = document.querySelector('[data-feature-link]');
  const featureImage = document.querySelector('[data-feature-image]');
  const featureMediaLink = document.querySelector('[data-feature-media-link]');
  const featureCaption = document.querySelector('[data-feature-caption]');
  const shelfPosition = document.querySelector('[data-shelf-position]');
  const routePreview = document.querySelector('#route-preview');
  let featureIndexValue = 0;

  const updateFeature = (key, shouldFocus = false) => {
    const data = featureData[key];
    const selected = featureCards.findIndex((card) => card.dataset.featureKey === key);
    if (!data || !featureStage || selected < 0) return;
    featureIndexValue = selected;
    const render = () => {
      featureIndex.textContent = data.index;
      featureTitle.textContent = data.title;
      featureCopy.textContent = data.copy;
      featureTags.innerHTML = data.tags.map((tag) => `<span>${tag}</span>`).join('');
      featureLink.href = data.link;
      featureLink.childNodes[0].nodeValue = `${data.linkLabel} `;
      featureMediaLink.href = data.link;
      featureImage.src = data.image;
      featureImage.alt = data.alt;
      featureCaption.textContent = data.caption;
      shelfPosition.textContent = `${String(selected + 1).padStart(2, '0')} / ${String(featureCards.length).padStart(2, '0')}`;
      featureCards.forEach((card, index) => {
        const active = index === selected;
        card.classList.toggle('is-active', active);
        card.setAttribute('aria-selected', String(active));
        card.tabIndex = active ? 0 : -1;
      });
      routePreview?.setAttribute('aria-labelledby', featureCards[selected].id);
    };
    featureStage.classList.add('is-changing');
    if (document.startViewTransition && motionMode === 'full') document.startViewTransition(render);
    else render();
    window.setTimeout(() => featureStage.classList.remove('is-changing'), motionMode === 'off' ? 0 : 220);
    if (shouldFocus) featureCards[selected].focus({ preventScroll: true });
  };

  featureCards.forEach((card) => card.addEventListener('click', () => updateFeature(card.dataset.featureKey)));
  const shelfTrack = document.querySelector('[data-shelf-track]');
  shelfTrack?.addEventListener('keydown', (event) => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    let next = featureIndexValue;
    if (event.key === 'ArrowLeft') next = Math.max(0, next - 1);
    if (event.key === 'ArrowRight') next = Math.min(featureCards.length - 1, next + 1);
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = featureCards.length - 1;
    updateFeature(featureCards[next].dataset.featureKey, true);
    featureCards[next].scrollIntoView({ behavior: motionMode === 'off' ? 'auto' : 'smooth', block: 'nearest', inline: 'nearest' });
  });
  document.querySelector('[data-shelf-prev]')?.addEventListener('click', () => updateFeature(featureCards[Math.max(0, featureIndexValue - 1)].dataset.featureKey, true));
  document.querySelector('[data-shelf-next]')?.addEventListener('click', () => updateFeature(featureCards[Math.min(featureCards.length - 1, featureIndexValue + 1)].dataset.featureKey, true));

  document.querySelectorAll('[data-year]').forEach((item) => { item.textContent = String(new Date().getFullYear()); });

  const leadForm = document.querySelector('[data-lead-form]');
  const formStatus = leadForm?.querySelector('[data-form-status]');
  const formButton = leadForm?.querySelector('button[type="submit"]');
  leadForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!leadForm.checkValidity()) { leadForm.reportValidity(); return; }
    const input = leadForm.querySelector('input[type="email"]');
    const value = input?.value.trim();
    if (!value) return;
    const originalLabel = formButton?.textContent || 'Theo dõi';
    if (formButton) { formButton.disabled = true; formButton.textContent = 'Đang gửi…'; }
    try {
      const response = await fetch(leadForm.action || 'api/lead', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ value, note: document.title }) });
      if (!response.ok) throw new Error(`lead request failed: ${response.status}`);
      leadForm.reset();
      if (formStatus) formStatus.textContent = 'Đã nhận. Mình sẽ gửi update khi có episode mới.';
    } catch (error) {
      if (formStatus) formStatus.textContent = 'Chưa gửi được lúc này. Bạn có thể theo dõi bản rebuild qua GitHub.';
    } finally {
      if (formButton) { formButton.disabled = false; formButton.textContent = originalLabel; }
    }
  });
})();
