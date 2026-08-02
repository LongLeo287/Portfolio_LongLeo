/**
 * LongLeo Portfolio — Animation Engine
 * Scroll reveals, headline word reveal, cursor spotlight, pointer effects,
 * counters, typing. Every effect is gated behind prefers-reduced-motion and
 * every pointer effect is rAF-throttled.
 */

(function () {
  'use strict';

  // Single source of truth for motion: the data-motion attribute, which the
  // head script seeds from the OS preference and the header toggle rewrites.
  // Read live, never cached, so flipping the toggle takes effect immediately
  // instead of on the next page load.
  const prefersReduced = () => document.documentElement.dataset.motion === 'reduced';
  const finePointer = () => window.matchMedia('(pointer: fine)').matches;

  // Where scroll-driven animations exist, CSS links motion to scroll position
  // directly — off the main thread, no listener, no rAF. The JS equivalents
  // below stand down so the two never fight over the same property.
  const supportsScrollTimeline =
    window.CSS && CSS.supports && CSS.supports('animation-timeline', 'scroll()');
  document.documentElement.classList.toggle('has-scroll-timeline', !!supportsScrollTimeline);

  /* Shared rAF scheduler — one frame loop for every pointer-driven effect
     instead of one style write per mousemove event. */
  const frameQueue = new Map();
  let frameHandle = null;

  function schedule(key, fn) {
    frameQueue.set(key, fn);
    if (frameHandle !== null) return;
    frameHandle = requestAnimationFrame(() => {
      frameHandle = null;
      const jobs = Array.from(frameQueue.values());
      frameQueue.clear();
      jobs.forEach((job) => job());
    });
  }

  window.portfolioMotion = { schedule, prefersReduced, finePointer };

  /* ── 1. SCROLL REVEALS ──────────────────────────────────────────── */
  const revealObserver = new IntersectionObserver(
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
    revealObserver.observe(el);
  }

  // Restraint budget: stagger caps at 300ms so a long list never trickles in.
  document.querySelectorAll('.fade-up').forEach((el, i) => {
    if (el.tagName === 'H1' || el.tagName === 'H2') return;
    observeReveal(el, Math.min(i * 40, 300));
  });

  document.querySelectorAll('.stagger').forEach((container) => {
    Array.from(container.children).forEach((child, i) => {
      observeReveal(child, Math.min(i * 60, 480));
    });
  });

  document.querySelectorAll('.tool-item').forEach((item, i) => {
    observeReveal(item, Math.min(i * 60, 480));
  });

  document.querySelectorAll('.contact-item').forEach((item, i) => {
    observeReveal(item, i * 100);
  });

  /* ── 2. HEADLINE WORD REVEAL ────────────────────────────────────────
     Splits a heading into per-word masks. Must be re-runnable: the i18n
     pass rewrites innerHTML on every language switch, which destroys the
     spans, so app.js calls refreshTextReveal() after translating. */
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
          // background-clip:text breaks when the span is split, so keep
          // .gradient-text whole and animate it as a single word.
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

      // Process tempDiv's children, not tempDiv itself — cloning the wrapper
      // would inject a block-level <div> inside the heading and break the
      // inline flow around <br>.
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

    if (prefersReduced()) return; // leave the markup untouched

    if (textObserver) textObserver.disconnect();
    textObserver = new IntersectionObserver(
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
      // Already on screen (hero, or a heading the visitor scrolled past while
      // the language was switching) — play immediately rather than waiting.
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

  /* ── 3. CURSOR SPOTLIGHT ────────────────────────────────────────── */
  const spotlight = document.getElementById('cursorSpotlight');
  if (spotlight && finePointer()) {
    let mouseX = 0, mouseY = 0, currentX = 0, currentY = 0;
    let running = false;

    function animateSpotlight() {
      currentX += (mouseX - currentX) * 0.1;
      currentY += (mouseY - currentY) * 0.1;
      spotlight.style.transform = `translate3d(${currentX}px, ${currentY}px, 0)`;
      // Park the loop once it has caught up — no idle rAF burning battery.
      if (Math.abs(mouseX - currentX) < 0.5 && Math.abs(mouseY - currentY) < 0.5) {
        running = false;
        return;
      }
      requestAnimationFrame(animateSpotlight);
    }

    document.addEventListener('mousemove', (e) => {
      if (prefersReduced()) { spotlight.style.opacity = '0'; return; }
      spotlight.style.opacity = '';
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

  /* ── 4. COUNTERS ────────────────────────────────────────────────── */
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

        // Years (2019) are read as a date, not a quantity — never count them up.
        if (target > 999 || prefersReduced()) {
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

  document.querySelectorAll('.stat-number').forEach((el) => counterObserver.observe(el));

  /* ── 5. MAGNETIC CTA ──────────────────────────────────────────────
     Writes --mag-x/--mag-y rather than `transform`. An inline transform
     would win the cascade over :hover and :active, so the button would
     stop showing lift and press feedback the moment the pointer touched
     it. The CSS composes all three.

     Bound regardless of the current motion setting and gated inside the
     handler — binding on load would mean the toggle only took effect after
     a reload. */
  if (finePointer()) {
    document.querySelectorAll('.btn-primary, .btn-dark, .header-cta').forEach((btn, i) => {
      const key = `magnet-${i}`;
      btn.addEventListener('mousemove', (e) => {
        if (prefersReduced()) return;
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

  /* ── 6. TILT + SPOTLIGHT on static cards ────────────────────────────
     Portfolio cards are rendered later by app.js and bind themselves —
     this only covers cards that exist in the markup at parse time. */
  if (finePointer()) {
    document.querySelectorAll('.service-card').forEach((card, i) => {
      const key = `tilt-${i}`;
      card.addEventListener('mousemove', (e) => {
        if (prefersReduced()) return;
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

  /* ── 7. HERO PILL TYPING ────────────────────────────────────────── */
  const pill = document.querySelector('.pill');
  if (pill) {
    const startPillTyping = (text) => {
      if (window._pillTypingInterval) {
        clearInterval(window._pillTypingInterval);
        window._pillTypingInterval = null;
      }
      pill.style.opacity = '1';
      pill.style.animation = 'none';

      if (prefersReduced()) {
        pill.textContent = text;
        pill.classList.add('pill-float');
        return;
      }

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
        pill.classList.add('pill-float');
      }, 45);
    };

    window.startPillTyping = startPillTyping;
    startPillTyping(pill.textContent.trim());
  }

  /* ── 8. EXPERIENCE RAIL ─────────────────────────────────────────────
     Fills the timeline rail in step with how far the section has scrolled.
     Where the browser has scroll-driven animations it is pure CSS and this
     does nothing; the JS path exists for everyone else. */
  const expGrid = document.querySelector('.experience-grid');
  if (expGrid && !prefersReduced() && !supportsScrollTimeline) {
    let railTicking = false;

    const updateRail = () => {
      railTicking = false;
      const rect = expGrid.getBoundingClientRect();
      // 0 when the section's top reaches the bottom third of the viewport,
      // 1 once its bottom has passed the same line.
      const line = window.innerHeight * 0.72;
      const progress = (line - rect.top) / Math.max(rect.height, 1);
      expGrid.style.setProperty('--rail-progress', Math.min(1, Math.max(0, progress)).toFixed(3));
    };

    const requestRail = () => {
      if (railTicking) return;
      railTicking = true;
      requestAnimationFrame(updateRail);
    };

    // Only listen while the section is anywhere near the viewport.
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
    updateRail();
  }

  /* ── 9. PAGE READY ──────────────────────────────────────────────── */
  document.documentElement.classList.add('js-loaded');
})();
