/* ── Initialize Lenis Smooth Scroll ── */
const lenis = new Lenis({
  duration: 1.2,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  orientation: 'vertical',
  gestureOrientation: 'vertical',
  smoothWheel: true,
  smoothTouch: false,
  touchMultiplier: 1.5,
});

window.lenis = lenis;

function raf(time) {
  lenis.raf(time);
  requestAnimationFrame(raf);
}
requestAnimationFrame(raf);

const menuBtn = document.getElementById("menuBtn");
const mobileNav = document.getElementById("mobileNav");
const backToTop = document.getElementById("backToTop");
const scrollProgress = document.getElementById("scrollProgress");
const navLinks = document.querySelectorAll('.main-nav a, .mobile-nav a');
const sections = document.querySelectorAll('section[id]');

/* ── Mobile menu toggle (Interacts with Lenis scroll) ── */
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

/* ── Portfolio filter (Staggered transition) ── */
const filterButtons = document.querySelectorAll(".filter-btn");
const portfolioCards = document.querySelectorAll(".portfolio-card");

function applyFilter(filter, immediate = false) {
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

  if (immediate) {
    cardsToHide.forEach((card) => {
      card.classList.add("hide");
      card.classList.remove("show");
      card.classList.remove("hide-anim");
    });
    cardsToShow.forEach((card) => {
      card.classList.remove("hide");
      card.classList.remove("hide-anim");
      card.classList.add("show");
    });
  } else {
    // Giai đoạn 1: Co nhỏ và mờ dần các thẻ cần ẩn
    cardsToHide.forEach((card) => {
      card.classList.remove("show");
      card.classList.add("hide-anim");
    });

    // Giai đoạn 2: Đợi hiệu ứng kết thúc, chuyển layout và hiện dần các thẻ cần hiển thị
    setTimeout(() => {
      cardsToHide.forEach((card) => {
        if (card.classList.contains("hide-anim")) {
          card.classList.add("hide");
          card.classList.remove("hide-anim");
        }
      });

      cardsToShow.forEach((card) => {
        card.classList.remove("hide");
        card.classList.remove("hide-anim");
      });

      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          cardsToShow.forEach((card) => {
            card.classList.add("show");
          });
        });
      });
    }, 300);
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

// Chạy bộ lọc "Nổi bật" (all) lập tức khi tải trang lần đầu
applyFilter("all", true);

/* ── Contact form → Web3Forms AJAX ── */
const contactForm = document.getElementById("contactForm");
const formNote = document.getElementById("formNote");

if (contactForm && formNote) {
  contactForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    // Disable button to prevent double submit
    const submitBtn = contactForm.querySelector("button[type='submit']");
    const originalBtnText = submitBtn.textContent;
    submitBtn.textContent = "Đang gửi...";
    submitBtn.disabled = true;

    // Reset alert styles
    formNote.className = "form-note";
    formNote.textContent = "";

    const formData = new FormData(contactForm);
    
    // Ensure access key is present, default is set here but can be overridden in HTML
    if (!formData.has("access_key")) {
      formData.append("access_key", "a582c035-779d-4762-b9cf-c79ee898b958");
    }

    try {
      const response = await fetch("https://api.web3forms.com/submit", {
        method: "POST",
        body: formData
      });

      const result = await response.json();

      if (result.success) {
        formNote.textContent = "Tin nhắn của bạn đã được gửi đi thành công. Mình sẽ liên hệ lại sớm nhất!";
        formNote.classList.add("success", "show");
        contactForm.reset();
      } else {
        formNote.textContent = `Lỗi: ${result.message || "Không thể gửi tin nhắn lúc này. Vui lòng thử lại sau."}`;
        formNote.classList.add("error", "show");
      }
    } catch (error) {
      formNote.textContent = "Không thể kết nối máy chủ. Vui lòng kiểm tra kết nối mạng của bạn.";
      formNote.classList.add("error", "show");
    } finally {
      submitBtn.textContent = originalBtnText;
      submitBtn.disabled = false;

      // Automatically hide the status notification after 8 seconds
      setTimeout(() => {
        formNote.classList.remove("show");
      }, 8000);
    }
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

// Lắng nghe sự kiện cuộn từ Lenis
lenis.on('scroll', () => {
  updateScrollUI();
});

// Intercept click liên kết nội bộ để cuộn mượt bằng Lenis
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href === '#' || href === '') return;
    
    const target = document.querySelector(href);
    if (target) {
      e.preventDefault();
      
      // Đóng menu mobile nếu đang mở
      if (mobileNav && mobileNav.classList.contains("open")) {
        mobileNav.classList.remove("open");
        menuBtn.textContent = "☰";
        lenis.start();
      }
      
      lenis.scrollTo(target, {
        offset: -78, // header height is 78px
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

// Fallback listeners
window.addEventListener("scroll", updateScrollUI, { passive: true });
window.addEventListener("load", updateScrollUI);
updateScrollUI();

/* ── Fade-up on scroll ── */
/* NOTE: Handled by animations.js via .reveal / .revealed system (Fix #2) */
/* Keeping this observer removed to prevent double-observation conflicts */

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
    
    if (category === "Design" || category === "Photography" || category === "Thumbnail") {
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
  // Helper to extract YouTube video ID and get thumbnail
  function getYouTubeThumbnail(src) {
    if (src.includes("videoseries?list=")) {
      // Playlist: Fallback to Golden Crown video thumbnail
      return "https://img.youtube.com/vi/c-dl9-LHZLU/maxresdefault.jpg";
    }
    const match = src.match(/embed\/([^?]+)/);
    if (match && match[1]) {
      return `https://img.youtube.com/vi/${match[1]}/maxresdefault.jpg`;
    }
    return "";
  }

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
  const videoThumb = getYouTubeThumbnail(randomVideo.src);

  let slidesHtml = `
    <div class="showcase-slide active" data-type="video" data-video-src="${randomVideo.src}">
      <div class="yt-facade" style="background-image: url('${videoThumb}');" aria-label="Phát video: ${randomVideo.title}">
        <div class="yt-play-btn" aria-hidden="true">
          <svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
        </div>
      </div>
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

  // Setup click event for YouTube Facade to load iframe on demand
  slider.addEventListener("click", (e) => {
    const facade = e.target.closest(".yt-facade");
    if (facade) {
      const slide = facade.closest(".showcase-slide");
      const videoSrc = slide.dataset.videoSrc;
      if (videoSrc) {
        // Build autoplay iframe
        const iframe = document.createElement("iframe");
        const autoplaySrc = videoSrc.includes("?") ? `${videoSrc}&autoplay=1` : `${videoSrc}?autoplay=1`;
        iframe.src = autoplaySrc;
        iframe.title = slide.querySelector("h3").textContent;
        iframe.setAttribute("allow", "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share");
        iframe.setAttribute("allowfullscreen", "");
        
        // Replace facade with iframe
        facade.replaceWith(iframe);
      }
    }
  });

  function goToSlide(index) {
    // Ẩn slide và chấm cũ
    slides[currentSlideIndex].classList.remove("active");
    if (dots.length > 0) dots[currentSlideIndex].classList.remove("active");

    // Dừng video nếu slide hiện tại là video phát dở (chỉ hoạt động nếu iframe đã được inject)
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

  // Bổ sung sự kiện vuốt chạm (Touch Swipe) cho slider trên thiết bị di động
  let touchStartX = 0;
  let touchEndX = 0;

  slider.addEventListener("touchstart", (e) => {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });

  slider.addEventListener("touchend", (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipeGesture();
  }, { passive: true });

  function handleSwipeGesture() {
    const threshold = 60; // minimum distance in px
    if (touchStartX - touchEndX > threshold) {
      // Swiped left -> next
      nextSlide();
      resetInterval();
    } else if (touchEndX - touchStartX > threshold) {
      // Swiped right -> prev
      prevSlide();
      resetInterval();
    }
  }

  startInterval();
}
