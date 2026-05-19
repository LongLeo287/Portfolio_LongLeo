/**
 * LongLeo Portfolio — Animation Engine
 * Scroll reveals, cursor spotlight, tilt cards, counter animation
 */

(function () {
  'use strict';

  /* ── 1. INTERSECTION OBSERVER: scroll-triggered reveals ── */
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          // Once revealed, stop observing to save resources
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
  );

  // Upgrade existing fade-up elements to use reveal system
  document.querySelectorAll('.fade-up').forEach((el, i) => {
    el.classList.add('reveal');
    el.style.transitionDelay = `${Math.min(i * 0.04, 0.3)}s`;
    revealObserver.observe(el);
  });

  // Stagger children of .stagger containers
  document.querySelectorAll('.stagger').forEach((container) => {
    const children = container.children;
    Array.from(children).forEach((child, i) => {
      child.classList.add('reveal');
      child.style.transitionDelay = `${i * 0.09}s`;
      revealObserver.observe(child);
    });
  });

  /* ── 2. CURSOR SPOTLIGHT ── */
  const spotlight = document.getElementById('cursorSpotlight');
  if (spotlight && window.matchMedia('(pointer: fine)').matches) {
    let mouseX = 0, mouseY = 0;
    let currentX = 0, currentY = 0;
    let animFrame;

    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    });

    function animateSpotlight() {
      currentX += (mouseX - currentX) * 0.1;
      currentY += (mouseY - currentY) * 0.1;
      spotlight.style.left = currentX + 'px';
      spotlight.style.top  = currentY + 'px';
      animFrame = requestAnimationFrame(animateSpotlight);
    }
    animateSpotlight();

    // Hide on mobile / touch
    document.addEventListener('touchstart', () => {
      spotlight.style.opacity = '0';
      cancelAnimationFrame(animFrame);
    }, { passive: true });
  }

  /* ── 3. COUNTER ANIMATION for stat numbers ── */
  const statNumbers = document.querySelectorAll('.stat-number');
  const counterObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const raw = el.textContent.trim();
        const numMatch = raw.match(/[\d,.]+/);
        if (!numMatch) return;

        const target = parseFloat(numMatch[0].replace(',', '.'));
        const suffix = raw.replace(numMatch[0], '');
        const isDecimal = numMatch[0].includes('.');
        const duration = 1600;
        const start = performance.now();

        function tick(now) {
          const elapsed = now - start;
          const progress = Math.min(elapsed / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
          const current = target * eased;
          el.textContent = isDecimal
            ? current.toFixed(1) + suffix
            : Math.round(current) + suffix;

          if (progress < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
        counterObserver.unobserve(el);
      });
    },
    { threshold: 0.5 }
  );

  statNumbers.forEach((el) => counterObserver.observe(el));

  /* ── 4. MAGNETIC HOVER on CTA buttons ── */
  document.querySelectorAll('.btn-primary, .btn-dark, .header-cta').forEach((btn) => {
    btn.addEventListener('mousemove', (e) => {
      const rect = btn.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top  - rect.height / 2;
      btn.style.transform = `translate(${x * 0.18}px, ${y * 0.18}px) translateY(-2px)`;
    });

    btn.addEventListener('mouseleave', () => {
      btn.style.transform = '';
    });
  });

  /* ── 5. 3D CARD TILT on service & experience cards ── */
  const tiltCards = document.querySelectorAll('.service-card, .portfolio-card');
  tiltCards.forEach((card) => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width  - 0.5;
      const y = (e.clientY - rect.top)  / rect.height - 0.5;
      card.style.transform = `
        perspective(600px)
        rotateX(${-y * 6}deg)
        rotateY(${x * 6}deg)
        translateY(-5px)
        scale(1.01)
      `;
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });
  });

  /* ── 6. TYPING EFFECT on hero pill ── */
  const pill = document.querySelector('.pill');
  if (pill) {
    const originalText = pill.textContent.trim();
    pill.textContent = '';
    pill.style.opacity = '1';
    let charIndex = 0;
    const typeInterval = setInterval(() => {
      pill.textContent += originalText[charIndex];
      charIndex++;
      if (charIndex >= originalText.length) clearInterval(typeInterval);
    }, 45);
  }

  /* ── 7. SECTION NAV HIGHLIGHT on scroll ── */
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.main-nav a, .mobile-nav a');

  const sectionObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute('id');
          navLinks.forEach((link) => {
            link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
          });
        }
      });
    },
    { threshold: 0.35, rootMargin: '-80px 0px 0px 0px' }
  );

  sections.forEach((s) => sectionObserver.observe(s));

  /* ── 8. SMOOTH REVEAL for tool items with stagger ── */
  const toolItemObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          toolItemObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -20px 0px' }
  );

  document.querySelectorAll('.tool-item').forEach((item, i) => {
    item.classList.add('reveal');
    item.style.transitionDelay = `${i * 0.06}s`;
    toolItemObserver.observe(item);
  });

  /* ── 9. PORTFOLIO CARD PARALLAX THUMBNAIL ── */
  document.querySelectorAll('.portfolio-card').forEach((card) => {
    const thumb = card.querySelector('.portfolio-thumb img');
    if (!thumb) return;

    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      thumb.style.transform = `scale(1.1) translateY(${y * -8}px)`;
    });

    card.addEventListener('mouseleave', () => {
      thumb.style.transform = 'scale(1.04)';
    });
  });

  /* ── 10. CONTACT ITEMS reveal stagger ── */
  document.querySelectorAll('.contact-item').forEach((item, i) => {
    item.classList.add('reveal');
    item.style.transitionDelay = `${i * 0.1}s`;
    revealObserver.observe(item);
  });

  /* ── 11. PAGE LOADING — remove initial flicker ── */
  document.documentElement.classList.add('js-loaded');

})();
