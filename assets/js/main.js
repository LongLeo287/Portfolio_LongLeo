const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
const prefersReducedMotion = () => motionPreference.matches;
const supportsScrollTimeline =
  !prefersReducedMotion() && window.CSS && CSS.supports && CSS.supports('animation-timeline', 'scroll()');

const isEnglish = () =>
  (typeof window.portfolioLang === "function"
    ? window.portfolioLang()
    : localStorage.getItem("portfolio_lang")) === "en";

function createNativeScrollAdapter() {
  return {
    stop() {},
    start() {},
    on() {},
    raf() {},
    scrollTo(target, options = {}) {
      const offset = options.offset || 0;
      const behavior = prefersReducedMotion() ? 'auto' : (options.behavior || 'smooth');
      if (typeof target === 'number') {
        window.scrollTo({ top: target + offset, behavior });
        return;
      }
      const el = typeof target === 'string' ? document.querySelector(target) : target;
      if (el) window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY + offset, behavior });
    }
  };
}

let lenis = createNativeScrollAdapter();
window.lenis = lenis;

function installDeferredMedia() {
  const canObserve = 'IntersectionObserver' in window;
  const load = (root) => {
    if (!root) return;
    const images = root.matches?.('img[data-src]') ? [root] : [...root.querySelectorAll?.('img[data-src]') || []];
    images.forEach((img) => {
      if (img.dataset.srcset) img.srcset = img.dataset.srcset;
      if (img.dataset.sizes) img.sizes = img.dataset.sizes;
      if (img.dataset.src) img.src = img.dataset.src;
      delete img.dataset.src;
      delete img.dataset.srcset;
      delete img.dataset.sizes;
    });
    const backgrounds = root.matches?.('[data-bg-src]') ? [root] : [...root.querySelectorAll?.('[data-bg-src]') || []];
    backgrounds.forEach((node) => {
      const src = node.dataset.bgSrc;
      if (src) node.style.backgroundImage = `url("${src.replace(/"/g, '%22')}")`;
      delete node.dataset.bgSrc;
    });
  };
  const observe = (root = document) => {
    const targets = root.matches?.('img[data-src], [data-bg-src]')
      ? [root]
      : [...root.querySelectorAll?.('img[data-src], [data-bg-src]') || []];
    targets.forEach((target) => {
      if (target.tagName === 'IMG' && !target.dataset.releaseMedia) {
        target.dataset.releaseMedia = 'true';
        target.dataset.releaseSrc = target.dataset.src || target.currentSrc || target.src;
        if (target.dataset.srcset) target.dataset.releaseSrcset = target.dataset.srcset;
      }
    });
    if (!canObserve) return targets.forEach(load);
    targets.forEach((target) => mediaObserver.observe(target));
  };
  const release = (root) => {
    if (!root) return;
    const nodes = root.matches?.('[data-release-media="true"]')
      ? [root]
      : [...root.querySelectorAll?.('[data-release-media="true"]') || []];
    nodes.forEach((node) => {
      if (node.tagName === 'IMG') {
        node.removeAttribute('src');
        node.removeAttribute('srcset');
        if (node.dataset.releaseSrc) node.dataset.src = node.dataset.releaseSrc;
        if (node.dataset.releaseSrcset) node.dataset.srcset = node.dataset.releaseSrcset;
        return;
      }
      node.style.removeProperty('background-image');
      if (node.dataset.releaseBg) node.dataset.bgSrc = node.dataset.releaseBg;
    });
  };
  const mediaObserver = canObserve
    ? new IntersectionObserver((entries) => entries.forEach((entry) => {
        // Keep decoded thumbnails once loaded. Removing src on every viewport
        // exit causes decode/network churn when a visitor scrolls back up.
        if (entry.isIntersecting) load(entry.target);
      }), { rootMargin: '320px 0px' })
    : null;
  window.portfolioMedia = Object.freeze({ load, observe, release });
  observe();
}

installDeferredMedia();

const themeToggle = document.getElementById("themeToggle");
const currentTheme = localStorage.getItem("portfolio_theme") || "dark";

if (currentTheme === "light") {
  document.documentElement.classList.add("light-theme");
}

if (themeToggle) {
  themeToggle.addEventListener("click", () => {
    document.documentElement.classList.toggle("light-theme");
    const isLight = document.documentElement.classList.contains("light-theme");
    localStorage.setItem("portfolio_theme", isLight ? "light" : "dark");
  
    const cvIframe = document.querySelector("#cvModal iframe");
    if (cvIframe && cvIframe.contentWindow) {
      cvIframe.contentWindow.postMessage({ type: "THEME_TOGGLE", isLight: isLight }, window.location.origin);
    }
  });
}

const loader = document.getElementById("cinematicLoader");
if (loader) {
  lenis.stop();
  let loaderClosed = false;
  const closeSoon = () => {
    if (loaderClosed) return;
    loaderClosed = true;
    closeLoaderSequence();
  };
  const domReady = () => window.setTimeout(closeSoon, 80);
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', domReady, { once: true });
  } else {
    domReady();
  }
  // Never let a slow font/third-party request hold the first interaction.
  window.setTimeout(closeSoon, 260);
}

function closeLoaderSequence() {
  if (!loader || loader.classList.contains("fade-out")) return;
  
  loader.classList.add("fade-out");
  lenis.start();
  
  document.querySelectorAll('.hero .fade-up').forEach((el, idx) => {
    setTimeout(() => {
      el.classList.add('revealed');
    }, idx * 100);
  });
  
  setTimeout(() => {
    loader.style.display = "none";
  }, 320);
}

const menuBtn = document.getElementById("menuBtn");
const mobileNav = document.getElementById("mobileNav");

if (menuBtn && mobileNav) {
  const setMenuState = (isOpen) => {
    mobileNav.classList.toggle("open", isOpen);
    menuBtn.textContent = isOpen ? "×" : "☰";
    menuBtn.setAttribute("aria-expanded", String(isOpen));
    menuBtn.setAttribute(
      "aria-label",
      isOpen
        ? (isEnglish() ? "Close menu" : "Đóng menu")
        : (isEnglish() ? "Open menu" : "Mở menu")
    );
    if (isOpen) lenis.stop(); else lenis.start();
  };

  setMenuState(false);

  menuBtn.addEventListener("click", () => {
    setMenuState(!mobileNav.classList.contains("open"));
  });

  mobileNav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => setMenuState(false));
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && mobileNav.classList.contains("open")) {
      setMenuState(false);
      menuBtn.focus();
    }
  });
}

const contactForm = document.getElementById("contactForm");
const formNote = document.getElementById("formNote");

if (contactForm && formNote) {
  contactForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const submitBtn = contactForm.querySelector("button[type='submit']");
    const originalBtnText = submitBtn.textContent;
    submitBtn.textContent = isEnglish() ? "Sending..." : "Đang gửi...";
    submitBtn.disabled = true;
    contactForm.setAttribute("aria-busy", "true");

    formNote.className = "form-note";
    formNote.textContent = "";

    const formData = new FormData(contactForm);

    const controller = new AbortController();
    const timeoutId = window.setTimeout(() => controller.abort(), 15000);

    try {
      const response = await fetch("https://api.web3forms.com/submit", {
        method: "POST",
        body: formData,
        signal: controller.signal
      });

      const result = await response.json();
      const isEn = isEnglish();

      if (result.success) {
        formNote.textContent = isEn 
          ? "Your message has been sent successfully. I will get back to you soon!" 
          : "Tin nhắn của bạn đã được gửi đi thành công. Mình sẽ liên hệ lại sớm nhất!";
        formNote.classList.add("success", "show");
        contactForm.reset();
      } else {
        formNote.textContent = isEn
          ? `Error: ${result.message || "Failed to send message. Please try again later."}`
          : `Lỗi: ${result.message || "Không thể gửi tin nhắn lúc này. Vui lòng thử lại sau."}`;
        formNote.classList.add("error", "show");
      }
    } catch (error) {
      const isEn = localStorage.getItem('portfolio_lang') === 'en';
      const timedOut = error?.name === 'AbortError';
      formNote.textContent = timedOut
        ? (isEn ? "The request timed out. Please try again." : "Yêu cầu đã hết thời gian. Vui lòng thử lại.")
        : (isEn
          ? "Network connection error. Please check your connection."
          : "Không thể kết nối máy chủ. Vui lòng kiểm tra kết nối mạng của bạn.");
      formNote.classList.add("error", "show");
    } finally {
      window.clearTimeout(timeoutId);
      submitBtn.textContent = originalBtnText;
      submitBtn.disabled = false;
      contactForm.setAttribute("aria-busy", "false");

      setTimeout(() => {
        formNote.classList.remove("show");
      }, 8000);
    }
  });
}

const backToTop = document.getElementById("backToTop");
const scrollProgress = document.getElementById("scrollProgress");
const navLinks = document.querySelectorAll('.main-nav a, .mobile-nav a');
const sections = document.querySelectorAll('section[id]');


let sectionOffsets = [];
let scrollRange = 0;
let activeSectionId = null;
let backToTopVisible = null;
let lastProgress = -1;
function cacheScrollMetrics() {
  scrollRange = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
}
function cacheSectionOffsets() {
  sectionOffsets = Array.from(sections).map(section => ({
    id: section.id,
    top: section.offsetTop - 120
  }));
  cacheScrollMetrics();
}
window.addEventListener('resize', cacheSectionOffsets);
window.recacheSectionOffsets = cacheSectionOffsets;

function updateScrollUI() {
  const scrollTop = window.scrollY || document.documentElement.scrollTop;
  if (scrollRange === 0 && document.documentElement.scrollHeight > window.innerHeight) cacheScrollMetrics();
  const progress = scrollRange > 0 ? (scrollTop / scrollRange) * 100 : 0;

  if (scrollProgress && !supportsScrollTimeline && Math.abs(progress - lastProgress) >= 0.05) {
    scrollProgress.style.transform = `scaleX(${progress / 100})`;
    lastProgress = progress;
  }
  const shouldShowBackToTop = scrollTop > 520;
  if (backToTop && shouldShowBackToTop !== backToTopVisible) {
    backToTop.classList.toggle("show", shouldShowBackToTop);
    backToTopVisible = shouldShowBackToTop;
  }

  let currentSection = "home";
  if (sectionOffsets.length === 0) cacheSectionOffsets();
  sectionOffsets.forEach((sec) => {
    if (scrollTop >= sec.top) currentSection = sec.id;
  });

  if (currentSection !== activeSectionId) {
    navLinks.forEach((link) => {
      link.classList.toggle("active", link.getAttribute("href") === `#${currentSection}`);
    });
    activeSectionId = currentSection;
  }
}

let scrollTicking = false;
function requestScrollUI() {
  if (scrollTicking) return;
  scrollTicking = true;
  requestAnimationFrame(() => {
    scrollTicking = false;
    updateScrollUI();
  });
}

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href === '#' || href === '') return;
    
    const target = document.querySelector(href);
    if (target) {
      e.preventDefault();
      
      if (mobileNav && mobileNav.classList.contains("open")) {
        mobileNav.classList.remove("open");
        menuBtn.textContent = "☰";
        lenis.start();
      }
      
      lenis.scrollTo(target, {
        offset: -78,
        duration: 0.68
      });
    }
  });
});

if (backToTop) {
  backToTop.addEventListener("click", () => {
    lenis.scrollTo(0, { duration: 0.75 });
  });
}

window.addEventListener("scroll", requestScrollUI, { passive: true });
window.addEventListener("load", () => {
  cacheSectionOffsets();
  updateScrollUI();
});
updateScrollUI();

function initLabAtlas() {
  const grid = document.querySelector('.labs-grid');
  if (!grid) return;

  const cards = [...grid.querySelectorAll('.lab-tile')];
  const buttons = [...document.querySelectorAll('.labs-filter')];
  const status = document.querySelector('.labs-filter-status');
  const expandButton = document.querySelector('[data-labs-expand]');
  if (!cards.length || !buttons.length) return;

  let activeFilter = 'all';
  let expanded = false;

  const render = () => {
    cards.forEach(card => {
      const matches = activeFilter === 'all' || card.dataset.labKind === activeFilter;
      const isPrimary = card.dataset.labPrimary === 'true';
      card.hidden = !matches || (!expanded && !isPrimary);
    });
    grid.dataset.labsExpanded = String(expanded);
    buttons.forEach(button => {
      const selected = button.dataset.labFilter === activeFilter;
      button.classList.toggle('is-active', selected);
      button.setAttribute('aria-pressed', String(selected));
    });
    const visible = cards.filter(card => !card.hidden);
    const architectures = new Set(visible.map(card => card.dataset.labArchitecture));
    const english = window.portfolioLang?.() === 'en';
    if (status) {
      status.textContent = english
        ? `${visible.length} projects · ${architectures.size} architectures`
        : `${visible.length} dự án · ${architectures.size} kiến trúc`;
    }
    if (expandButton) {
      expandButton.setAttribute('aria-expanded', String(expanded));
      expandButton.classList.toggle('is-expanded', expanded);
      const label = expandButton.querySelector('[data-labs-expand-label]');
      if (label) label.textContent = expanded
        ? (english ? 'Show fewer projects' : 'Thu gọn dự án')
        : (english ? 'Show more projects' : 'Xem thêm dự án');
      const icon = expandButton.querySelector('.labs-expand-icon');
      if (icon) icon.textContent = expanded ? '↑' : '↓';
    }
    window.portfolioMedia?.observe(grid);
    window.recacheSectionOffsets?.();
  };

  buttons.forEach(button => {
    button.addEventListener('click', () => {
      activeFilter = button.dataset.labFilter || 'all';
      if (activeFilter !== 'all') expanded = true;
      render();
    });
  });

  if (expandButton) {
    expandButton.addEventListener('click', () => {
      expanded = !expanded;
      render();
    });
  }

  window.addEventListener('portfolio:languagechange', () => {
    render();
  });
  render();
}

initLabAtlas();

const lightboxModal = document.getElementById("lightboxModal");
const lightboxImage = document.getElementById("lightboxImage");
const lightboxClose = document.querySelector(".lightbox-close");
const lightboxVideo = document.getElementById("lightboxVideo");
const lightboxVideoWrapper = document.getElementById("lightboxVideoWrapper");

if (lightboxModal && lightboxImage && lightboxClose) {
  lightboxImage.addEventListener("load", () => {
    const lightboxLoader = document.getElementById("lightboxLoader");
    if (lightboxLoader) lightboxLoader.style.display = "none";
    lightboxImage.style.display = "block";
  });

  const closeLightbox = () => window.ModalManager && window.ModalManager.close();

  lightboxClose.addEventListener("click", closeLightbox);

  lightboxModal.addEventListener("click", (e) => {
    if (e.target === lightboxModal) closeLightbox();
  });
}
