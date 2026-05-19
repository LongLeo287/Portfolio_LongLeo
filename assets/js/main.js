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
  const cardsToShow = [];
  const cardsToHide = [];

  if (filter === "all") {
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
    portfolioCards.forEach((card) => {
      const featuredIndex = featuredCards.indexOf(card);
      if (featuredIndex !== -1 && featuredIndex < limit) {
        card.style.order = featuredIndex;
        cardsToShow.push(card);
        visibleCount += 1;
      } else {
        card.style.order = "";
        cardsToHide.push(card);
      }
    });
  } else {
    // Reset order và lọc theo category bình thường
    portfolioCards.forEach((card) => {
      card.style.order = "";
      const category = card.dataset.category;
      const shouldShow = category === filter;
      if (shouldShow) {
        cardsToShow.push(card);
        visibleCount += 1;
      } else {
        cardsToHide.push(card);
      }
    });
  }

  // 1. Thực hiện ẩn các thẻ trước
  cardsToHide.forEach((card) => {
    card.classList.add("hide");
    card.classList.remove("show");
  });

  // 2. Hiển thị các thẻ cần hiển thị với animation fade-up mượt mà
  cardsToShow.forEach((card) => {
    card.classList.remove("hide");
  });

  // Sử dụng double requestAnimationFrame để đảm bảo trình duyệt nhận biết được thay đổi display trước khi add class show
  if (cardsToShow.length > 0) {
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        cardsToShow.forEach((card) => {
          card.classList.add("show");
        });
      });
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

/* ── Lightbox for Images & Videos ── */
const lightboxModal = document.getElementById("lightboxModal");
const lightboxImage = document.getElementById("lightboxImage");
const lightboxClose = document.querySelector(".lightbox-close");
const lightboxLoader = document.getElementById("lightboxLoader");

function getYouTubeEmbedUrl(url) {
  let videoId = "";
  if (url.includes("youtube.com/watch")) {
    const urlParams = new URLSearchParams(new URL(url).search);
    videoId = urlParams.get("v");
  } else if (url.includes("youtu.be/")) {
    videoId = url.split("youtu.be/")[1]?.split("?")[0];
  } else if (url.includes("youtube.com/shorts/")) {
    videoId = url.split("youtube.com/shorts/")[1]?.split("?")[0];
  } else if (url.includes("youtube.com/playlist")) {
    const urlParams = new URLSearchParams(new URL(url).search);
    const listId = urlParams.get("list");
    if (listId) {
      return `https://www.youtube.com/embed/videoseries?list=${listId}&autoplay=1`;
    }
  }
  
  if (videoId) {
    return `https://www.youtube.com/embed/${videoId}?autoplay=1`;
  }
  return null;
}

if (lightboxModal && lightboxImage && lightboxClose && lightboxLoader) {
  const lightboxVideoWrapper = document.getElementById("lightboxVideoWrapper");
  const lightboxVideo = document.getElementById("lightboxVideo");

  portfolioCards.forEach(card => {
    const category = card.dataset.category;
    
    if (category === "Design" || category === "Photography") {
      card.addEventListener("click", function(e) {
        e.preventDefault(); // Ngăn mở tab mới
        
        // Hiện loader và ẩn ảnh/video cũ đi
        lightboxLoader.style.display = "block";
        lightboxImage.style.display = "none";
        if (lightboxVideoWrapper) lightboxVideoWrapper.style.display = "none";
        if (lightboxVideo) lightboxVideo.src = "";
        lightboxImage.src = ""; // Xoá src cũ
        
        // Lấy link hình ảnh từ thẻ img bên trong
        const imgEl = this.querySelector("img");
        let imgSrc = "";
        
        if (imgEl) {
          imgSrc = imgEl.getAttribute("src");
          imgSrc = imgSrc.replace("sz=w1000", "sz=w1600");
        } else {
          imgSrc = this.getAttribute("href");
        }
        
        lightboxImage.src = imgSrc;
        lightboxModal.classList.add("show");
      });
    } else if (category === "Video") {
      card.addEventListener("click", function(e) {
        const href = this.getAttribute("href");
        const embedUrl = getYouTubeEmbedUrl(href);
        
        if (embedUrl && lightboxVideoWrapper && lightboxVideo) {
          e.preventDefault(); // Ngăn mở tab mới
          
          lightboxLoader.style.display = "none";
          lightboxImage.style.display = "none";
          lightboxImage.src = "";
          
          lightboxVideo.src = embedUrl;
          lightboxVideoWrapper.style.display = "block";
          lightboxModal.classList.add("show");
        }
      });
    }
  });

  // Khi ảnh tải xong, ẩn loader và hiện ảnh
  lightboxImage.addEventListener("load", () => {
    lightboxLoader.style.display = "none";
    lightboxImage.style.display = "block";
  });

  function closeLightbox() {
    lightboxModal.classList.remove("show");
    lightboxImage.src = ""; // Clear để giải phóng bộ nhớ
    if (lightboxVideo) lightboxVideo.src = ""; // Stop video playback
    if (lightboxVideoWrapper) lightboxVideoWrapper.style.display = "none";
  }

  // Đóng lightbox khi click vào dấu X
  lightboxClose.addEventListener("click", closeLightbox);

  // Đóng lightbox khi click ra ngoài hình ảnh/video
  lightboxModal.addEventListener("click", (e) => {
    if (e.target === lightboxModal) {
      closeLightbox();
    }
  });

  // Đóng bằng phím ESC
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && lightboxModal.classList.contains("show")) {
      closeLightbox();
    }
  });
}

/* ── Showcase Slider ── */
const slider = document.getElementById("showcaseSlider");
const slidesContainer = document.getElementById("showcaseSlides");

if (slider && slidesContainer) {
  // 1. Tạo danh sách các video/playlist chất lượng để chọn ngẫu nhiên
  const videoPool = [
    {
      src: "https://www.youtube.com/embed/videoseries?list=PLhc6e124Y3Jw4qQYPAkfWcuIO-C3BsuG9",
      title: "Dự án sản xuất Video & Creative Content",
      tag: "Video Playlist"
    },
    {
      src: "https://www.youtube.com/embed/lEibZKODe8M",
      title: "SETUP GÓC MÁY CỰC CHILL: Segotep Slath Mini 🖥️",
      tag: "Setup Showcase"
    },
    {
      src: "https://www.youtube.com/embed/6sSoxzakgEE",
      title: "CASE QUỐC DÂN KÈM 6 FAN: MSI MAG Forge 120A ❄️",
      tag: "Review Công Nghệ"
    },
    {
      src: "https://www.youtube.com/embed/noGA2i3-rl4",
      title: "CASE DỊ 8 MẶT: Thermaltake Tower 300 Lùa Gà Hay Đẳng Cấp? 🤔",
      tag: "Review Tech"
    },
    {
      src: "https://www.youtube.com/embed/jlcoFXEGbQQ",
      title: "QUÁI VẬT 4K: ASUS ROG Strix RTX 5080 🚀",
      tag: "Unboxing & Review"
    },
    {
      src: "https://www.youtube.com/embed/2-3nB7gtom8",
      title: "PC CHUẨN \"BACK TO SCHOOL\": Học Giỏi - Quẩy Game 🎒",
      tag: "Build PC"
    },
    {
      src: "https://www.youtube.com/embed/bF01LIaiS6s",
      title: "PROJECT BTF ASUS X MYGEAR",
      tag: "Dự Án Hợp Tác"
    },
    {
      src: "https://www.youtube.com/embed/c-dl9-LHZLU",
      title: "Dự án Golden Crown Hải Phòng - Unicons",
      tag: "Corporate Video"
    }
  ];

  // Chọn ngẫu nhiên 1 video từ pool
  const randomVideo = videoPool[Math.floor(Math.random() * videoPool.length)];

  let slidesHtml = `
    <div class="showcase-slide active" data-type="video">
      <iframe
        src="${randomVideo.src}"
        title="${randomVideo.title}"
        loading="lazy"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        allowfullscreen>
      </iframe>
      <div class="showcase-info">
        <span class="tag">${randomVideo.tag}</span>
        <h3>${randomVideo.title}</h3>
      </div>
    </div>
  `;

  // 2. Lấy danh sách tất cả các thẻ portfolio-card chứa hình ảnh (chỉ chọn Thiết kế & Chụp ảnh)
  const imageCards = Array.from(portfolioCards).filter(card => {
    const category = card.dataset.category;
    return (category === "Design" || category === "Photography") && card.querySelector("img") !== null;
  });

  // 3. Trộn ngẫu nhiên danh sách thẻ ảnh này (Fisher-Yates Shuffle)
  for (let i = imageCards.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [imageCards[i], imageCards[j]] = [imageCards[j], imageCards[i]];
  }

  // 4. Lấy ra 4 thẻ ảnh ngẫu nhiên từ toàn bộ portfolio để tạo slide sinh động
  const randomImageCards = imageCards.slice(0, 4);
  randomImageCards.forEach(card => {
    const imgEl = card.querySelector("img");
    const titleEl = card.querySelector("h3");
    const tagEl = card.querySelector(".tag");

    const rawSrc = imgEl ? imgEl.getAttribute("src") : "";
    // Tải ảnh chất lượng cao w1600 cho slide
    const hdSrc = rawSrc.replace("sz=w1000", "sz=w1600");
    const title = titleEl ? titleEl.textContent : "Sản phẩm sáng tạo";
    const tagText = tagEl ? tagEl.textContent : (card.dataset.category === "Design" ? "Thiết kế" : "Chụp ảnh");

    slidesHtml += `
      <div class="showcase-slide" data-type="image" data-src="${hdSrc}">
        <div class="showcase-img-wrap">
          <div class="showcase-bg-blur" style="background-image: url('${hdSrc}');"></div>
          <img src="${hdSrc}" alt="${title}" />
        </div>
        <div class="showcase-info">
          <span class="tag">${tagText}</span>
          <h3>${title}</h3>
        </div>
      </div>
    `;
  });

  // Ghi đè HTML động vào container
  slidesContainer.innerHTML = slidesHtml;

  // 5. Khởi tạo slider logic điều khiển
  const slides = slider.querySelectorAll(".showcase-slide");
  const prevBtn = document.getElementById("prevSlideBtn");
  const nextBtn = document.getElementById("nextSlideBtn");
  const dotsContainer = document.getElementById("sliderDots");
  let currentSlideIndex = 0;
  let slideInterval = null;
  const intervalTime = 15000; // 15 giây đổi 1 lần

  // Tạo các chấm chỉ số (dots)
  if (dotsContainer) {
    dotsContainer.innerHTML = ""; // Xoá chấm tĩnh
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
