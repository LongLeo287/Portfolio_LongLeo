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

function applyFilter(filter) {
  let visibleCount = 0;

  if (filter === "all") {
    // Ẩn tất cả thẻ trước
    portfolioCards.forEach((card) => card.classList.add("hide"));

    // Lọc ra các thẻ tiêu biểu (data-featured="true")
    const featuredCards = Array.from(portfolioCards).filter(
      (card) => card.dataset.featured === "true"
    );

    // Trộn ngẫu nhiên (Fisher-Yates Shuffle)
    for (let i = featuredCards.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [featuredCards[i], featuredCards[j]] = [featuredCards[j], featuredCards[i]];
    }

    // Hiển thị tối đa 6 sản phẩm và sắp xếp theo thứ tự ngẫu nhiên
    const limit = 6;
    featuredCards.forEach((card, index) => {
      if (index < limit) {
        card.classList.remove("hide");
        visibleCount += 1;
      } else {
        card.classList.add("hide");
      }
      card.style.order = index;
    });
  } else {
    // Reset order và lọc theo category bình thường
    portfolioCards.forEach((card) => {
      card.style.order = "";
      const category = card.dataset.category;
      const shouldShow = category === filter;
      card.classList.toggle("hide", !shouldShow);
      if (shouldShow) visibleCount += 1;
    });
  }

  const emptyState = document.getElementById("emptyState");
  if (emptyState) {
    emptyState.classList.toggle("show", visibleCount === 0);
  }
}

// Bắt sự kiện click bộ lọc
filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const filter = button.dataset.filter;

    filterButtons.forEach((btn) => btn.classList.remove("active"));
    button.classList.add("active");

    applyFilter(filter);
  });
});

// Chạy bộ lọc "Nổi bật" (all) lần đầu tiên khi tải trang
applyFilter("all");

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
const lightboxLoader = document.getElementById("lightboxLoader");

if (lightboxModal && lightboxImage && lightboxClose && lightboxLoader) {
  portfolioCards.forEach(card => {
    const category = card.dataset.category;
    if (category === "Design" || category === "Photography") {
      card.addEventListener("click", function(e) {
        e.preventDefault(); // Ngăn mở tab mới
        
        // Hiện loader và ẩn ảnh cũ đi để chuẩn bị load ảnh mới
        lightboxLoader.style.display = "block";
        lightboxImage.style.display = "none";
        lightboxImage.src = ""; // Xoá src cũ
        
        // Lấy link hình ảnh từ thẻ img bên trong
        const imgEl = this.querySelector("img");
        let imgSrc = "";
        
        if (imgEl) {
          imgSrc = imgEl.getAttribute("src");
          // Tăng độ phân giải lên w1600 (vừa đủ nét, vừa load nhanh hơn w2500)
          imgSrc = imgSrc.replace("sz=w1000", "sz=w1600");
        } else {
          imgSrc = this.getAttribute("href");
        }
        
        lightboxImage.src = imgSrc;
        lightboxModal.classList.add("show");
      });
    }
  });

  // Khi ảnh tải xong, ẩn loader và hiện ảnh
  lightboxImage.addEventListener("load", () => {
    lightboxLoader.style.display = "none";
    lightboxImage.style.display = "block";
  });

  // Đóng lightbox khi click vào dấu X
  lightboxClose.addEventListener("click", () => {
    lightboxModal.classList.remove("show");
    lightboxImage.src = ""; // Clear để giải phóng bộ nhớ
  });

  // Đóng lightbox khi click ra ngoài hình ảnh
  lightboxModal.addEventListener("click", (e) => {
    if (e.target === lightboxModal) {
      lightboxModal.classList.remove("show");
      lightboxImage.src = "";
    }
  });

  // Đóng bằng phím ESC
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && lightboxModal.classList.contains("show")) {
      lightboxModal.classList.remove("show");
      lightboxImage.src = "";
    }
  });
}

/* ── Showcase Slider ── */
const slider = document.getElementById("showcaseSlider");
if (slider) {
  const slides = slider.querySelectorAll(".showcase-slide");
  const prevBtn = document.getElementById("prevSlideBtn");
  const nextBtn = document.getElementById("nextSlideBtn");
  const dotsContainer = document.getElementById("sliderDots");
  let currentSlideIndex = 0;
  let slideInterval = null;
  const intervalTime = 15000; // 15 giây đổi 1 lần

  // Tạo các chấm chỉ số (dots)
  if (dotsContainer) {
    slides.forEach((_, index) => {
      const dot = document.createElement("div");
      dot.classList.add("slider-dot");
      if (index === 0) dot.classList.add("active");
      dot.addEventListener("click", () => {
        goToSlide(index);
        resetInterval();
      });
      dotsContainer.appendChild(dot);
    });
  }

  const dots = dotsContainer ? dotsContainer.querySelectorAll(".slider-dot") : [];

  function goToSlide(index) {
    // Ẩn slide và chấm cũ
    slides[currentSlideIndex].classList.remove("active");
    if (dots.length > 0) dots[currentSlideIndex].classList.remove("active");

    // Dừng video nếu slide hiện tại là video phát dở
    const currentSlide = slides[currentSlideIndex];
    if (currentSlide.dataset.type === "video") {
      const iframe = currentSlide.querySelector("iframe");
      if (iframe) {
        const src = iframe.src;
        iframe.src = src; // Reload src để dừng phát video
      }
    }

    // Tính chỉ số mới
    currentSlideIndex = (index + slides.length) % slides.length;

    // Hiện slide và chấm mới
    slides[currentSlideIndex].classList.add("active");
    if (dots.length > 0) dots[currentSlideIndex].classList.add("active");
  }

  function nextSlide() {
    goToSlide(currentSlideIndex + 1);
  }

  function prevSlide() {
    goToSlide(currentSlideIndex - 1);
  }

  if (prevBtn) prevBtn.addEventListener("click", () => {
    prevSlide();
    resetInterval();
  });
  if (nextBtn) nextBtn.addEventListener("click", () => {
    nextSlide();
    resetInterval();
  });

  function startInterval() {
    slideInterval = setInterval(nextSlide, intervalTime);
  }

  function resetInterval() {
    clearInterval(slideInterval);
    startInterval();
  }

  // Tạm dừng auto-play khi rê chuột vào slider
  slider.addEventListener("mouseenter", () => {
    clearInterval(slideInterval);
  });

  slider.addEventListener("mouseleave", () => {
    startInterval();
  });

  // Nhấp vào slide ảnh để mở xem ngay trong Lightbox
  slides.forEach((slide) => {
    if (slide.dataset.type === "image") {
      const imgWrap = slide.querySelector(".showcase-img-wrap");
      if (imgWrap) {
        imgWrap.addEventListener("click", () => {
          const imgSrc = slide.dataset.src;
          if (lightboxModal && lightboxImage && lightboxLoader) {
            lightboxLoader.style.display = "block";
            lightboxImage.style.display = "none";
            lightboxImage.src = "";
            lightboxImage.src = imgSrc;
            lightboxModal.classList.add("show");
          }
        });
      }
    }
  });

  startInterval();
}
