/* ==========================================================================
// LongLeo Portfolio — Main Global Layout Engine (Phase 1 Fixes & Phase 2 Integration)
// ========================================================================== */

/* ── Initialize Lenis Smooth Scroll ── */
const lenis = new Lenis({
  duration: 1.2,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  smoothWheel: true
});

window.lenis = lenis;

function raf(time) {
  lenis.raf(time);
  requestAnimationFrame(raf);
}
requestAnimationFrame(raf);

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
      cvIframe.contentWindow.postMessage({ type: "THEME_TOGGLE", isLight: isLight }, "*");
    }
  });
}

// ==========================================
// Cinematic Loader
// ==========================================
const loader = document.getElementById("cinematicLoader");
if (loader) {
  lenis.stop();
  
  // Safety timeout in case window load event fires late
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
  menuBtn.addEventListener("click", () => {
    mobileNav.classList.toggle("open");
    const isOpen = mobileNav.classList.contains("open");
    menuBtn.textContent = isOpen ? "×" : "☰";
    if (isOpen) {
      lenis.stop();
    } else {
      lenis.start();
    }
  });

  mobileNav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      mobileNav.classList.remove("open");
      menuBtn.textContent = "☰";
      lenis.start();
    });
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
    submitBtn.textContent = localStorage.getItem('portfolio_lang') === 'en' ? "Sending..." : "Đang gửi...";
    submitBtn.disabled = true;

    formNote.className = "form-note";
    formNote.textContent = "";

    const formData = new FormData(contactForm);
    
    if (!formData.has("access_key")) {
      formData.append("access_key", "a582c035-779d-4762-b9cf-c79ee898b958");
    }

    try {
      const response = await fetch("https://api.web3forms.com/submit", {
        method: "POST",
        body: formData
      });

      const result = await response.json();
      const isEn = localStorage.getItem('portfolio_lang') === 'en';

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

function updateScrollUI() {
  const scrollTop = window.scrollY || document.documentElement.scrollTop;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;

  if (scrollProgress) scrollProgress.style.width = `${progress}%`;
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

// Listen scroll events from Lenis
lenis.on('scroll', () => {
  updateScrollUI();
});

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

window.addEventListener("scroll", updateScrollUI, { passive: true });
window.addEventListener("load", updateScrollUI);
updateScrollUI();

// ==========================================
// Lightbox Closing Handlers
// ==========================================
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

  function closeLightbox() {
    lightboxModal.classList.remove("show");
    lightboxImage.src = "";
    if (lightboxVideo) lightboxVideo.src = "";
    if (lightboxVideoWrapper) lightboxVideoWrapper.style.display = "none";
    lenis.start();
  }

  lightboxClose.addEventListener("click", closeLightbox);
  
  lightboxModal.addEventListener("click", (e) => {
    if (e.target === lightboxModal) {
      closeLightbox();
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && lightboxModal.classList.contains("show")) {
      closeLightbox();
    }
  });
}
