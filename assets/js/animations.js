
(function () {
  'use strict';

  const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
  const reducedMotion = () => motionPreference.matches;
  const finePointer = () => window.matchMedia('(pointer: fine)').matches;

  const supportsScrollTimeline =
    window.CSS && CSS.supports && CSS.supports('animation-timeline', 'scroll()');
  document.documentElement.classList.toggle('has-scroll-timeline', !!supportsScrollTimeline);

  const afrSchedule = window.portfolioAFR && window.portfolioAFR.schedule;
  const frameQueue = new Map();
  let frameHandle = null;

  function schedule(key, fn) {
    if (afrSchedule) {
      afrSchedule(key, fn);
      return;
    }
    frameQueue.set(key, fn);
    if (frameHandle !== null) return;
    frameHandle = requestAnimationFrame(() => {
      frameHandle = null;
      const jobs = Array.from(frameQueue.values());
      frameQueue.clear();
      jobs.forEach((job) => job());
    });
  }

  window.portfolioMotion = { schedule, finePointer, reducedMotion };

  const ambientTargets = document.querySelectorAll(
    '[data-afr-loop], [data-afr-heavy], .hero-orb, .marquee-track, .kinetic-row, .floating-note, .pill, .eyebrow, .brand-mark'
  );
  if ('IntersectionObserver' in window && ambientTargets.length) {
    const ambientObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => entry.target.setAttribute('data-motion-inview', String(entry.isIntersecting)));
    }, { rootMargin: '120px 0px' });
    ambientTargets.forEach((target) => ambientObserver.observe(target));
  } else {
    ambientTargets.forEach((target) => target.setAttribute('data-motion-inview', 'true'));
  }

  const revealObserver = reducedMotion()
    ? null
    : new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add('revealed');
            revealObserver.unobserve(entry.target);
          });
        },
        { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
      );

  function observeReveal(el, delay) {
    el.classList.add('reveal');
    if (delay) el.style.transitionDelay = `${delay}ms`;
    if (reducedMotion()) {
      el.classList.add('revealed');
      return;
    }
    revealObserver.observe(el);
  }

  document.querySelectorAll('.fade-up').forEach((el, i) => {
    if (el.tagName === 'H1' || el.tagName === 'H2') return;
    observeReveal(el, Math.min(i * 40, 300));
  });

  document.querySelectorAll('.stagger').forEach((container) => {
    Array.from(container.children).forEach((child, i) => {
      if (child.classList.contains('experience-rail-light')) return;
      observeReveal(child, Math.min(i * 60, 480));
    });
  });

  document.querySelectorAll('.tool-item').forEach((item, i) => {
    observeReveal(item, Math.min(i * 60, 480));
  });

  document.querySelectorAll('.contact-item').forEach((item, i) => {
    observeReveal(item, i * 100);
  });

  const REVEAL_SELECTOR = '.hero h1, .section-title h2, .about-content h2';
  let textObserver = null;

  function splitHeading(target) {
    const lines = target.innerHTML.split(/<br\s*\/?>/i);
    let newHTML = '';

    lines.forEach((line, lineIdx) => {
      if (lineIdx > 0) newHTML += '<br>';

      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = line;

      const processNode = (node) => {
        if (node.nodeType === Node.TEXT_NODE) {
          const fragment = document.createDocumentFragment();
          node.textContent.split(/(\s+)/).forEach((word) => {
            if (word.trim() === '') {
              fragment.appendChild(document.createTextNode(word));
              return;
            }
            const mask = document.createElement('span');
            mask.className = 'reveal-word-mask';
            const inner = document.createElement('span');
            inner.className = 'reveal-word';
            inner.textContent = word;
            mask.appendChild(inner);
            fragment.appendChild(mask);
          });
          return fragment;
        }

        if (node.nodeType === Node.ELEMENT_NODE) {
          if (node.classList && node.classList.contains('gradient-text')) {
            const mask = document.createElement('span');
            mask.className = 'reveal-word-mask';
            const inner = document.createElement('span');
            inner.className = 'reveal-word';
            inner.innerHTML = node.outerHTML;
            mask.appendChild(inner);
            return mask;
          }
          const clone = node.cloneNode(false);
          Array.from(node.childNodes).forEach((child) => {
            clone.appendChild(processNode(child));
          });
          return clone;
        }

        return node.cloneNode(true);
      };

      const wrapper = document.createElement('div');
      Array.from(tempDiv.childNodes).forEach((child) => {
        wrapper.appendChild(processNode(child));
      });
      newHTML += wrapper.innerHTML;
    });

    target.innerHTML = newHTML;
  }

  function playWords(target) {
    target.querySelectorAll('.reveal-word').forEach((word, idx) => {
      word.style.transitionDelay = `${idx * 25}ms`;
      word.style.transform = 'translateY(0)';
    });
  }

  function initTextReveal() {
    const targets = document.querySelectorAll(REVEAL_SELECTOR);
    if (!targets.length) return;

    if (textObserver) textObserver.disconnect();
    textObserver = reducedMotion()
      ? null
      : new IntersectionObserver(
          (entries) => {
            entries.forEach((entry) => {
              if (!entry.isIntersecting) return;
              playWords(entry.target);
              textObserver.unobserve(entry.target);
            });
          },
          { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
        );

    targets.forEach((target) => {
      splitHeading(target);
      if (reducedMotion()) {
        playWords(target);
        return;
      }
      const rect = target.getBoundingClientRect();
      if (rect.top < window.innerHeight && rect.bottom > 0) {
        requestAnimationFrame(() => playWords(target));
      } else {
        textObserver.observe(target);
      }
    });
  }

  window.refreshTextReveal = initTextReveal;
  initTextReveal();

  const spotlight = document.getElementById('cursorSpotlight');
  if (spotlight && finePointer() && !reducedMotion()) {
    let mouseX = 0, mouseY = 0, currentX = 0, currentY = 0;
    let running = false;

    function animateSpotlight() {
      if (document.documentElement.dataset.afrScroll === 'fast') {
        running = false;
        spotlight.style.opacity = '0';
        return;
      }
      currentX += (mouseX - currentX) * 0.1;
      currentY += (mouseY - currentY) * 0.1;
      spotlight.style.transform = `translate3d(${currentX}px, ${currentY}px, 0)`;
      if (Math.abs(mouseX - currentX) < 0.5 && Math.abs(mouseY - currentY) < 0.5) {
        running = false;
        return;
      }
      requestAnimationFrame(animateSpotlight);
    }

    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      if (!running) {
        running = true;
        requestAnimationFrame(animateSpotlight);
      }
    }, { passive: true });

    document.addEventListener('touchstart', () => {
      spotlight.style.opacity = '0';
      running = true; // stops the loop from being restarted
    }, { passive: true, once: true });
  }

  const counterObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        counterObserver.unobserve(el);

        const raw = el.textContent.trim();
        const numMatch = raw.match(/[\d,.]+/);
        if (!numMatch) return;

        const target = parseFloat(numMatch[0].replace(',', '.'));
        const suffix = raw.replace(numMatch[0], '');

        if (target > 999) {
          el.style.animation = 'statCount var(--dur-deliberate) var(--ease-out) both';
          return;
        }

        const isDecimal = numMatch[0].includes('.');
        const duration = 1400;
        const start = performance.now();

        function tick(now) {
          const progress = Math.min((now - start) / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 3);
          const current = target * eased;
          el.textContent = isDecimal
            ? current.toFixed(1) + suffix
            : Math.round(current) + suffix;
          if (progress < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
      });
    },
    { threshold: 0.5 }
  );

  if (!reducedMotion()) {
    document.querySelectorAll('.stat-number').forEach((el) => counterObserver.observe(el));
  }

/*     Writes --mag-x/--mag-y rather than `transform`. An inline transform
     would win the cascade over :hover and :active, so the button would
     stop showing lift and press feedback the moment the pointer touched
     it. The CSS composes all three.

     Bound regardless of the current motion setting and gated inside the
     handler — binding on load would mean the toggle only took effect after
     a reload. */
  if (finePointer() && !reducedMotion()) {
    document.querySelectorAll('.btn-primary, .btn-dark, .header-cta').forEach((btn, i) => {
      const key = `magnet-${i}`;
      btn.addEventListener('mousemove', (e) => {
        const rect = btn.getBoundingClientRect();
        const x = (e.clientX - rect.left - rect.width / 2) * 0.18;
        const y = (e.clientY - rect.top - rect.height / 2) * 0.18;
        schedule(key, () => {
          btn.style.setProperty('--mag-x', `${x.toFixed(1)}px`);
          btn.style.setProperty('--mag-y', `${y.toFixed(1)}px`);
        });
      }, { passive: true });

      btn.addEventListener('mouseleave', () => {
        schedule(key, () => {
          btn.style.removeProperty('--mag-x');
          btn.style.removeProperty('--mag-y');
        });
      }, { passive: true });
    });
  }

  if (finePointer()) {
    document.querySelectorAll('.service-card').forEach((card, i) => {
      const key = `tilt-${i}`;
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const px = e.clientX - rect.left;
        const py = e.clientY - rect.top;
        const x = px / rect.width - 0.5;
        const y = py / rect.height - 0.5;
        schedule(key, () => {
          card.style.setProperty('--mx', `${px}px`);
          card.style.setProperty('--my', `${py}px`);
          card.style.transform =
            `perspective(600px) rotateX(${-y * 5}deg) rotateY(${x * 5}deg) translateY(-4px)`;
        });
      }, { passive: true });

      card.addEventListener('mouseleave', () => {
        schedule(key, () => { card.style.transform = ''; });
      }, { passive: true });
    });
  }

  const pill = document.querySelector('.pill');
  if (pill) {
    const startPillTyping = (text) => {
      if (window._pillTypingInterval) {
        clearInterval(window._pillTypingInterval);
        window._pillTypingInterval = null;
      }
      if (reducedMotion()) {
        pill.textContent = text;
        pill.classList.remove('pill-float');
        return;
      }
      pill.style.opacity = '1';
      pill.style.animation = 'none';

      pill.textContent = '';
      let charIndex = 0;
      window._pillTypingInterval = setInterval(() => {
        if (charIndex < text.length) {
          pill.textContent += text[charIndex];
          charIndex++;
          return;
        }
        clearInterval(window._pillTypingInterval);
        window._pillTypingInterval = null;
        pill.style.removeProperty('animation');
        pill.classList.add('pill-float');
      }, 45);
    };

    window.startPillTyping = startPillTyping;
    startPillTyping(pill.textContent.trim());
  }

  const expGrid = document.querySelector('.experience-grid');
  if (expGrid) {
    let railTicking = false;
    const experienceCards = Array.from(expGrid.querySelectorAll(':scope > .experience-card'));
    const railLight = expGrid.querySelector('.experience-rail-light');

    // Keep content reveal independent from the decorative rail. This covers
    // anchor navigation and smooth-scroll startup, where the generic reveal
    // observer can receive its first entry a frame later than the rail.
    const revealVisibleExperienceCards = () => {
      const viewportTop = -40;
      const viewportBottom = window.innerHeight + 40;
      experienceCards.forEach((card) => {
        const rect = card.getBoundingClientRect();
        if (rect.bottom > viewportTop && rect.top < viewportBottom) {
          card.classList.add('revealed');
        }
      });
    };

    const updateRail = () => {
      railTicking = false;
      const rect = expGrid.getBoundingClientRect();
      const railStyle = getComputedStyle(expGrid, '::before');
      const railCenterX = rect.left + (parseFloat(railStyle.left) || 0) + ((parseFloat(railStyle.width) || 0) / 2);
      const line = window.innerHeight * 0.72;
      const rawProgress = reducedMotion()
        ? 1
        : (line - rect.top) / Math.max(rect.height, 1);
      const progress = Math.min(1, Math.max(0, rawProgress));
      expGrid.style.setProperty('--rail-progress', progress.toFixed(3));
      if (railLight) {
        const railInset = 8;
        const railSpan = Math.max(0, rect.height - (railInset * 2));
        expGrid.style.setProperty('--rail-light-y', `${(railInset + (railSpan * progress)).toFixed(2)}px`);
      }
      revealVisibleExperienceCards();

      // The filled rail and the nodes share this same tip position. This
      // prevents a card/node from appearing before the line has reached it.
      const railTip = rect.top + 8 + Math.max(0, rect.height - 16) * progress;
      experienceCards.forEach((card) => {
        const node = getComputedStyle(card, '::before');
        const cardStyle = getComputedStyle(card);
        const cardRect = card.getBoundingClientRect();
        const cardBorderLeft = parseFloat(cardStyle.borderLeftWidth) || 0;
        const cardBorderTop = parseFloat(cardStyle.borderTopWidth) || 0;
        const nodeTop = parseFloat(node.top) || 0;
        const nodeHeight = parseFloat(node.height) || 0;
        const nodeWidth = parseFloat(node.width) || 0;
        const nodeBorderX = (parseFloat(node.borderLeftWidth) || 0) + (parseFloat(node.borderRightWidth) || 0);
        const nodeBorderY = (parseFloat(node.borderTopWidth) || 0) + (parseFloat(node.borderBottomWidth) || 0);
        const nodeOuterWidth = nodeWidth + nodeBorderX;
        const nodeOuterHeight = nodeHeight + nodeBorderY;
        const cardPaddingLeft = cardRect.left + cardBorderLeft;
        const cardPaddingTop = cardRect.top + cardBorderTop;
        card.style.setProperty('--experience-node-left', `${(railCenterX - cardPaddingLeft - (nodeOuterWidth / 2)).toFixed(2)}px`);
        const nodeCenter = cardPaddingTop + nodeTop + (nodeOuterHeight / 2);
        card.classList.toggle('timeline-reached', reducedMotion() || railTip >= nodeCenter);
      });
    };

    const requestRail = () => {
      if (railTicking) return;
      railTicking = true;
      requestAnimationFrame(updateRail);
    };

    let listening = false;
    new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && !listening) {
          listening = true;
          window.addEventListener('scroll', requestRail, { passive: true });
          requestRail();
        } else if (!entry.isIntersecting && listening) {
          listening = false;
          window.removeEventListener('scroll', requestRail);
        }
      });
    }, { rootMargin: '100% 0px' }).observe(expGrid);

    window.addEventListener('resize', requestRail, { passive: true });
    window.addEventListener('load', requestRail, { once: true, passive: true });
    window.addEventListener('hashchange', requestRail, { passive: true });
    updateRail();
  }

  document.documentElement.classList.add('js-loaded');
})();
