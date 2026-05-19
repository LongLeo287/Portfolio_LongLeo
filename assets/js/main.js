const menuBtn = document.getElementById("menuBtn");
const mobileNav = document.getElementById("mobileNav");
const backToTop = document.getElementById("backToTop");
const scrollProgress = document.getElementById("scrollProgress");
const navLinks = document.querySelectorAll('.main-nav a, .mobile-nav a');
const sections = document.querySelectorAll('section[id]');

/* ── Mobile menu toggle ── */
if (menuBtn && mobileNav) {
  menuBtn.addEventListener("click", () => {
    mobileNav.classList.toggle("open");
    menuBtn.textContent = mobileNav.classList.contains("open") ? "×" : "☰";
  });

  mobileNav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      mobileNav.classList.remove("open");
      menuBtn.textContent = "☰";
    });
  });
}

/* ── Portfolio filter ── */
const filterButtons = document.querySelectorAll(".filter-btn");
const portfolioCards = document.querySelectorAll(".portfolio-card");

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const filter = button.dataset.filter;

    filterButtons.forEach((btn) => btn.classList.remove("active"));
    button.classList.add("active");

    let visibleCount = 0;

    portfolioCards.forEach((card) => {
      const category = card.dataset.category;
      const shouldShow = filter === "all" || category === filter;
      card.classList.toggle("hide", !shouldShow);
      if (shouldShow) visibleCount += 1;
    });

    document.getElementById("emptyState").classList.toggle("show", visibleCount === 0);
  });
});

/* ── Contact form → mailto ── */
const contactForm = document.getElementById("contactForm");
const formNote = document.getElementById("formNote");

if (contactForm && formNote) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const data = new FormData(contactForm);
    const name = data.get("name") || "Khách liên hệ";
    const email = data.get("email") || "";
    const message = data.get("message") || "";
    const subject = encodeURIComponent(`Liên hệ portfolio từ ${name}`);
    const body = encodeURIComponent(`Tên: ${name}\nEmail: ${email}\n\nNội dung:\n${message}`);

    window.location.href = `mailto:Longdragon287@gmail.com?subject=${subject}&body=${body}`;
    formNote.classList.add("show");
    contactForm.reset();
  });
}

/* ── Scroll UI: progress bar, back-to-top, active nav ── */
function updateScrollUI() {
  const scrollTop = window.scrollY || document.documentElement.scrollTop;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;

  if (scrollProgress) scrollProgress.style.width = `${progress}%`;
  if (backToTop) backToTop.classList.toggle("show", scrollTop > 520);

  let currentSection = "home";
  sections.forEach((section) => {
    const sectionTop = section.offsetTop - 120;
    if (scrollTop >= sectionTop) currentSection = section.id;
  });

  navLinks.forEach((link) => {
    link.classList.toggle("active", link.getAttribute("href") === `#${currentSection}`);
  });
}

if (backToTop) {
  backToTop.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

window.addEventListener("scroll", updateScrollUI, { passive: true });
window.addEventListener("load", updateScrollUI);
updateScrollUI();

/* ── Fade-up on scroll ── */
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("show");
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll(".fade-up").forEach((el) => observer.observe(el));

/* ── Lightbox for Images ── */
const lightboxModal = document.getElementById("lightboxModal");
const lightboxImage = document.getElementById("lightboxImage");
const lightboxClose = document.querySelector(".lightbox-close");

if (lightboxModal && lightboxImage && lightboxClose) {
  portfolioCards.forEach(card => {
    const category = card.dataset.category;
    if (category === "Design" || category === "Photography") {
      card.addEventListener("click", function(e) {
        e.preventDefault(); // Ngăn mở tab mới
        
        // Lấy link hình ảnh chất lượng cao
        const imgSrc = this.getAttribute("href");
        
        // Nếu dùng Google Drive thumbnail thì thay &sz=w1000 bằng ảnh gốc hoặc giữ nguyên
        // Hiện tại href đang là dạng /uc?id=... (link gốc)
        // Mình sẽ gán href vào src của lightbox (để xem full HD)
        lightboxImage.src = imgSrc;
        lightboxModal.classList.add("show");
      });
    }
  });

  // Đóng lightbox khi click vào dấu X
  lightboxClose.addEventListener("click", () => {
    lightboxModal.classList.remove("show");
  });

  // Đóng lightbox khi click ra ngoài hình ảnh
  lightboxModal.addEventListener("click", (e) => {
    if (e.target === lightboxModal) {
      lightboxModal.classList.remove("show");
    }
  });

  // Đóng bằng phím ESC
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && lightboxModal.classList.contains("show")) {
      lightboxModal.classList.remove("show");
    }
  });
}
