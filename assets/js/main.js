/* ==========================================================================
// LongLeo Portfolio — Main Global Layout Engine (Phase 1 Fixes & Phase 2 Integration)
// ========================================================================== */

/* ── Smooth scroll ──────────────────────────────────────────────────
   Everything else calls lenis.stop()/start()/scrollTo(), so the no-op
   stand-in below keeps those call sites working when the library is
   unavailable, without a null check at each one. */
// animations.css drives the scroll-progress bar with a native scroll timeline
// where one exists; this stops the JS writing the same property every frame.
const supportsScrollTimeline =
  window.CSS && CSS.supports && CSS.supports('animation-timeline', 'scroll()');

// app.js owns the language state (?lang= beats localStorage); fall back to
// storage in case main.js somehow runs first.
const isEnglish = () =>
  (typeof window.portfolioLang === "function"
    ? window.portfolioLang()
    : localStorage.getItem("portfolio_lang")) === "en";

const lenis = (typeof Lenis !== 'undefined')
  ? new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true
    })
  : {
      stop() {},
      start() {},
      on() {},
      raf() {},
      scrollTo(target, options = {}) {
        const offset = options.offset || 0;
        if (typeof target === 'number') {
          window.scrollTo({ top: target + offset, behavior: 'auto' });
          return;
        }
        const el = typeof target === 'string' ? document.querySelector(target) : target;
        if (el) window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY + offset, behavior: 'auto' });
      }
    };

window.lenis = lenis;

if (typeof Lenis !== 'undefined') {
  const raf = (time) => {
    lenis.raf(time);
    requestAnimationFrame(raf);
  };
  requestAnimationFrame(raf);
}

// ==========================================
// Theme Switcher (Light/Dark Mode)
// ==========================================
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

// ==========================================
// Cinematic Loader
// ==========================================
const loader = document.getElementById("cinematicLoader");
if (loader) {
  lenis.stop();
  // Safety timeout in case the load event fires late
  const forceCloseLoader = setTimeout(closeLoaderSequence, 400);

  window.addEventListener("load", () => {
    clearTimeout(forceCloseLoader);
    setTimeout(closeLoaderSequence, 400);
  });
}

function closeLoaderSequence() {
  if (!loader || loader.classList.contains("fade-out")) return;
  
  loader.classList.add("fade-out");
  lenis.start();
  
  // Reveal Hero elements with premium delay
  document.querySelectorAll('.hero .fade-up').forEach((el, idx) => {
    setTimeout(() => {
      el.classList.add('revealed');
    }, idx * 100);
  });
  
  setTimeout(() => {
    loader.style.display = "none";
  }, 600);
}

// ==========================================
// Mobile Menu Navigation Toggle
// ==========================================
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

// ==========================================
// Contact Form Web3Forms AJAX Handler
// ==========================================
const contactForm = document.getElementById("contactForm");
const formNote = document.getElementById("formNote");

if (contactForm && formNote) {
  contactForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const submitBtn = contactForm.querySelector("button[type='submit']");
    const originalBtnText = submitBtn.textContent;
    submitBtn.textContent = isEnglish() ? "Sending..." : "Đang gửi...";
    submitBtn.disabled = true;

    formNote.className = "form-note";
    formNote.textContent = "";

    const formData = new FormData(contactForm);

    try {
      const response = await fetch("https://api.web3forms.com/submit", {
        method: "POST",
        body: formData
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
      formNote.textContent = isEn 
        ? "Network connection error. Please check your connection."
        : "Không thể kết nối máy chủ. Vui lòng kiểm tra kết nối mạng của bạn.";
      formNote.classList.add("error", "show");
    } finally {
      submitBtn.textContent = originalBtnText;
      submitBtn.disabled = false;

      setTimeout(() => {
        formNote.classList.remove("show");
      }, 8000);
    }
  });
}

// ==========================================
// Scroll UI Highlights (Progress bar, Back to top, Active nav)
// ==========================================
const backToTop = document.getElementById("backToTop");
const scrollProgress = document.getElementById("scrollProgress");
const navLinks = document.querySelectorAll('.main-nav a, .mobile-nav a');
const sections = document.querySelectorAll('section[id]');


let sectionOffsets = [];
function cacheSectionOffsets() {
  sectionOffsets = Array.from(sections).map(section => ({
    id: section.id,
    top: section.offsetTop - 120
  }));
}
window.addEventListener('resize', cacheSectionOffsets);
// app.js calls this after re-rendering the grid, which changes page height.
window.recacheSectionOffsets = cacheSectionOffsets;

function updateScrollUI() {
  const scrollTop = window.scrollY || document.documentElement.scrollTop;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;

  // scaleX, not width: this runs on every scroll frame and width would
  // relayout + repaint each time. Skipped entirely where a CSS scroll
  // timeline already drives the bar off the main thread.
  if (scrollProgress && !supportsScrollTimeline) {
    scrollProgress.style.transform = `scaleX(${progress / 100})`;
  }
  if (backToTop) backToTop.classList.toggle("show", scrollTop > 520);

  let currentSection = "home";
  if (sectionOffsets.length === 0) cacheSectionOffsets();
  sectionOffsets.forEach((sec) => {
    if (scrollTop >= sec.top) currentSection = sec.id;
  });

  navLinks.forEach((link) => {
    link.classList.toggle("active", link.getAttribute("href") === `#${currentSection}`);
  });
}

// Lenis emits its own scroll events; the native listener below covers the
// reduced-motion path. Guarded so the two never both fire per frame.
let scrollTicking = false;
function requestScrollUI() {
  if (scrollTicking) return;
  scrollTicking = true;
  requestAnimationFrame(() => {
    scrollTicking = false;
    updateScrollUI();
  });
}

lenis.on('scroll', requestScrollUI);

// Smooth anchor scrolling
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
        duration: 1.2
      });
    }
  });
});

if (backToTop) {
  backToTop.addEventListener("click", () => {
    lenis.scrollTo(0, { duration: 1.5 });
  });
}

window.addEventListener("scroll", requestScrollUI, { passive: true });
window.addEventListener("load", () => {
  // The portfolio grid renders after fetch, which changes every section's
  // offsetTop — recache or the active nav link lags a whole section.
  cacheSectionOffsets();
  updateScrollUI();
});
updateScrollUI();

// ==========================================
// Lightbox Closing Handlers
// ==========================================
const lightboxModal = document.getElementById("lightboxModal");
const lightboxImage = document.getElementById("lightboxImage");
const lightboxClose = document.querySelector(".lightbox-close");
const lightboxVideo = document.getElementById("lightboxVideo");
const lightboxVideoWrapper = document.getElementById("lightboxVideoWrapper");

// Opening, closing, Escape and focus restore all live in app.js's ModalManager.
// This only handles the image-loaded swap from spinner to picture.
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
