// ==========================================================================
// LongLeo Portfolio — Dynamic App Engine (Phase 1 Fixes & Phase 2 Integration)
// ==========================================================================

let projectsData = [];
let currentLang = localStorage.getItem('portfolio_lang') || 'vi';

const elements = {
  grid: document.getElementById('portfolioGrid'),
  slides: document.getElementById('showcaseSlides'),
  filterBtns: document.querySelectorAll('.filter-btn'),
  langBtns: document.querySelectorAll('.lang-btn'),
  
  // Case Study Modal
  modal: document.getElementById('caseStudyModal'),
  modalMedia: document.getElementById('modalMedia'),
  modalTitle: document.getElementById('modalTitle'),
  modalClient: document.getElementById('modalClient'),
  modalTags: document.getElementById('modalTags'),
  modalBody: document.getElementById('modalBody'),
  modalLink: document.getElementById('modalLink'),
  closeModalBtn: document.getElementById('closeModalBtn'),
  modalBackdrop: document.getElementById('modalBackdrop')
};

// ==========================================
// Init & Fetch
// ==========================================
async function initApp() {
  // Init Lucide
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }
  
  initLangToggle();
  
  try {
    const res = await fetch('assets/data/projects.json');
    if (!res.ok) throw new Error("Failed to fetch data");
    projectsData = await res.json();
    
    renderPortfolio();
    initFilters();
    initShowcaseSlider();
    updateStaticTranslations();
    
  } catch (error) {
    console.error("Error loading projects:", error);
    if (elements.grid) {
      elements.grid.innerHTML = `<p style="text-align:center;width:100%;color:var(--text-muted);">Failed to load portfolio projects. Please refresh the page.</p>`;
    }
  }
}

// ==========================================
// Language Toggle
// ==========================================
function initLangToggle() {
  elements.langBtns.forEach(btn => {
    if (btn.dataset.lang === currentLang) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
    
    btn.addEventListener('click', (e) => {
      const selectedBtn = e.target.closest('.lang-btn');
      if (!selectedBtn) return;
      
      elements.langBtns.forEach(b => b.classList.remove('active'));
      selectedBtn.classList.add('active');
      currentLang = selectedBtn.dataset.lang;
      localStorage.setItem('portfolio_lang', currentLang);
      
      renderPortfolio(document.querySelector('.filter-btn.active')?.dataset.filter || 'all');
      updateStaticTranslations();
      
      // Update slider titles dynamically without re-creating
      const activeSlide = document.querySelector('.showcase-slide.active');
      if (activeSlide) {
        initShowcaseSlider(); // Reinitialize showcase slider with selected language
      }
    });
  });
}

// ==========================================
// Static Translations Dictionary
// ==========================================
const translations = {
  vi: {
    nav_home: 'Trang chủ',
    nav_about: 'Về mình',
    nav_services: 'Dịch vụ',
    nav_exp: 'Kinh nghiệm',
    nav_port: 'Portfolio',
    nav_contact: 'Liên hệ',
    nav_collab: 'Liên hệ hợp tác',
    hero_pill: '✦ Video Editor • Motion Graphic • Visual Storyteller',
    hero_desc: 'Biến ý tưởng thành hình ảnh sống động — từ quay dựng video, motion graphic, thiết kế đồ họa đến tối ưu UI/UX.<br>Hơn 7 năm kinh nghiệm tạo ra sản phẩm truyền thông chất lượng cao.',
    hero_btn1: 'Xem portfolio ↗',
    hero_btn2: 'Liên hệ hợp tác ✉',
    stat_exp: 'năm kinh nghiệm',
    stat_proj: 'công ty & dự án',
    stat_start: 'bắt đầu hành trình',
    filter_all: 'Nổi bật',
    filter_vid: 'Sản xuất Video',
    filter_des: 'Thiết kế',
    filter_photo: 'Chụp ảnh',
    filter_thumb: 'YouTube Thumbnail',
    modal_view_link: 'Xem dự án ↗'
  },
  en: {
    nav_home: 'Home',
    nav_about: 'About',
    nav_services: 'Services',
    nav_exp: 'Experience',
    nav_port: 'Portfolio',
    nav_contact: 'Contact',
    nav_collab: 'Let\'s Talk',
    hero_pill: '✦ Video Editor • Motion Graphic • Visual Storyteller',
    hero_desc: 'Turning ideas into vivid visuals — from video production, motion graphics, graphic design to UI/UX optimization.<br>Over 7 years of experience in creating high-quality media products.',
    hero_btn1: 'View Portfolio ↗',
    hero_btn2: 'Let\'s Talk ✉',
    stat_exp: 'years of experience',
    stat_proj: 'companies & projects',
    stat_start: 'started journey',
    filter_all: 'Featured',
    filter_vid: 'Video Production',
    filter_des: 'Design',
    filter_photo: 'Photography',
    filter_thumb: 'YouTube Thumbnail',
    modal_view_link: 'View Project ↗'
  }
};

function updateStaticTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    if (translations[currentLang] && translations[currentLang][key]) {
      el.innerHTML = translations[currentLang][key];
    }
  });
  
  // Re-translate placeholder in inputs
  const nameInput = document.querySelector('input[name="name"]');
  const emailInput = document.querySelector('input[name="email"]');
  const msgInput = document.querySelector('textarea[name="message"]');
  const formBtn = document.querySelector('.contact-form button[type="submit"]');
  const formNote = document.getElementById('formNote');
  
  if (currentLang === 'en') {
    if (nameInput) nameInput.placeholder = "Your Name";
    if (emailInput) emailInput.placeholder = "Your Email";
    if (msgInput) msgInput.placeholder = "Message details...";
    if (formBtn) formBtn.textContent = "Send Message";
    if (formNote && formNote.className === "form-note") {
      formNote.textContent = "Enter details and click Send Message to email me directly.";
    }
  } else {
    if (nameInput) nameInput.placeholder = "Tên của bạn";
    if (emailInput) emailInput.placeholder = "Email liên hệ";
    if (msgInput) msgInput.placeholder = "Nội dung cần trao đổi";
    if (formBtn) formBtn.textContent = "Gửi đi";
    if (formNote && formNote.className === "form-note") {
      formNote.textContent = "Nhập thông tin và nhấn Gửi đi để gửi email trực tiếp cho mình.";
    }
  }
}

// ==========================================
// Render Portfolio Grid & Bind Effects
// ==========================================
function renderPortfolio(filter = 'all') {
  if (!elements.grid) return;
  
  elements.grid.innerHTML = '';
  
  let displayedCards = [];
  
  // Featured works filter
  const filtered = projectsData.filter(p => {
    if (filter === 'all') return p.isFeatured;
    return p.category === filter;
  });
  
  // Fisher-Yates Shuffle if 'Featured' category to keep layout dynamic
  let displayList = [...filtered];
  if (filter === 'all') {
    for (let i = displayList.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [displayList[i], displayList[j]] = [displayList[j], displayList[i]];
    }
    // Limit featured grid to 9 cards
    displayList = displayList.slice(0, 9);
  }
  
  displayList.forEach(p => {
    const card = document.createElement('a');
    card.className = 'portfolio-card fade-up';
    card.dataset.category = p.category;
    card.dataset.id = p.id;
    card.href = p.href || p.imgSrc;
    card.target = "_blank";
    
    // Multi-lang title & client
    const title = typeof p.title === 'object' ? p.title[currentLang] : p.title;
    const client = typeof p.client === 'object' ? p.client[currentLang] : p.client;
    
    const thumbDiv = document.createElement('div');
    thumbDiv.className = 'portfolio-thumb';
    
    const tagText = p.category === 'Design' ? (currentLang === 'vi' ? 'Thiết kế' : 'Design') : 
                    p.category === 'Photography' ? (currentLang === 'vi' ? 'Chụp ảnh' : 'Photography') : p.category;
                    
    thumbDiv.innerHTML = `
      <img src="${p.imgSrc}" alt="${p.alt || title}" loading="lazy" />
      <span class="tag">${tagText}</span>
    `;
    card.appendChild(thumbDiv);
    
    if (title || client) {
      const bodyDiv = document.createElement('div');
      bodyDiv.className = 'portfolio-body';
      bodyDiv.innerHTML = `
        <p class="client">${client}</p>
        <h3>${title}</h3>
      `;
      card.appendChild(bodyDiv);
    }
    
    card.addEventListener('click', (e) => handleCardClick(e, p));
    
    elements.grid.appendChild(card);
    displayedCards.push(card);
  });
  
  // Trigger entry transitions
  setTimeout(() => {
    displayedCards.forEach((card, idx) => {
      card.style.transitionDelay = `${idx * 0.04}s`;
      card.classList.add('show');
    });
    
    // Re-bind hover card 3D tilt effects
    applyCardEffects();
  }, 50);
}

// ==========================================
// Card Tilt & Parallax Thumbnails
// ==========================================
function applyCardEffects() {
  const cards = document.querySelectorAll('.portfolio-card');
  cards.forEach(card => {
    // 3D Card Tilt
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
    
    // Parallax Thumbnail image scaling
    const thumb = card.querySelector('.portfolio-thumb img');
    if (thumb) {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        thumb.style.transform = `scale(1.1) translateY(${y * -8}px)`;
      });

      card.addEventListener('mouseleave', () => {
        thumb.style.transform = 'scale(1.04)';
      });
    }
  });
}

// ==========================================
// Filters Event Handler
// ==========================================
function initFilters() {
  elements.filterBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const clickedBtn = e.target.closest('.filter-btn');
      if (!clickedBtn) return;
      
      elements.filterBtns.forEach(b => b.classList.remove('active'));
      clickedBtn.classList.add('active');
      renderPortfolio(clickedBtn.dataset.filter);
    });
  });
}

// ==========================================
// Click Actions: Modal vs Lightbox
// ==========================================
function handleCardClick(e, project) {
  e.preventDefault();
  
  if (project.caseStudy) {
    openCaseStudyModal(project);
  } else {
    openLightbox(project);
  }
}

// ==========================================
// Translated Case Study Helper (vi/en)
// ==========================================
function getTranslatedCaseStudy(project, lang) {
  const cs = project.caseStudy;
  if (!cs) return null;
  
  if (lang === 'vi') {
    return {
      role: cs.role || 'Dựng phim & Kỹ xảo',
      concept: cs.concept || '',
      challenge: cs.challenge || '',
      solution: cs.solution || '',
      tools: cs.tools || []
    };
  } else {
    const titleEn = typeof project.title === 'object' ? project.title.en : project.title;
    
    let conceptEn = '';
    if (cs.concept) {
      conceptEn = `Concept development and visual execution for the project: ${titleEn}.`;
    }
    
    let challengeEn = cs.challenge;
    if (cs.challenge && cs.challenge.includes('Tối ưu hóa thời gian sản xuất')) {
      challengeEn = 'Optimize production time and enhance the effectiveness of delivering the product\'s artistic message.';
    }
    
    let solutionEn = cs.solution;
    if (cs.solution && cs.solution.includes('Áp dụng kỹ thuật chuyển cảnh')) {
      solutionEn = 'Apply smooth transitions and cinematic color grading to emphasize the main subject.';
    }
    
    let roleEn = cs.role || 'Video Editor / Motion Designer';
    if (roleEn === 'Nhân viên Media' || roleEn === 'Dựng phim & Kỹ xảo') {
      roleEn = 'Video Editor / Visual Artist';
    }
    
    return {
      role: roleEn,
      concept: conceptEn,
      challenge: challengeEn,
      solution: solutionEn,
      tools: cs.tools || []
    };
  }
}

// ==========================================
// Case Study Modal
// ==========================================
function openCaseStudyModal(project) {
  const title = typeof project.title === 'object' ? project.title[currentLang] : project.title;
  const client = typeof project.client === 'object' ? project.client[currentLang] : project.client;
  
  elements.modalTitle.textContent = title;
  elements.modalClient.textContent = client;
  elements.modalLink.href = project.href || project.imgSrc;
  
  // Update view project translation
  if (elements.modalLink) {
    elements.modalLink.innerHTML = translations[currentLang]['modal_view_link'];
  }
  
  // Tags
  let tagsHtml = '';
  if (project.caseStudy && project.caseStudy.tools) {
    tagsHtml = project.caseStudy.tools.map(t => `<span>${t.trim()}</span>`).join('');
  } else {
    tagsHtml = `<span>${project.category}</span>`;
  }
  elements.modalTags.innerHTML = tagsHtml;
  
  // Format body details
  const cs = getTranslatedCaseStudy(project, currentLang);
  if (cs) {
    const headings = {
      vi: {
        role: 'Vai trò',
        concept: 'Ý tưởng & Concept',
        challenge: 'Thách thức sản xuất',
        solution: 'Giải pháp thực hiện'
      },
      en: {
        role: 'Role',
        concept: 'Concept & Idea',
        challenge: 'Production Challenge',
        solution: 'Implemented Solution'
      }
    };
    const h = headings[currentLang];
    
    elements.modalBody.innerHTML = `
      <div class="cs-section" style="margin-bottom:1.25rem;">
        <h4 style="font-family:'Space Grotesk',sans-serif;color:var(--text-light);font-size:1.05rem;margin-bottom:0.25rem;">✦ ${h.role}</h4>
        <p style="margin:0;font-size:0.95rem;">${cs.role}</p>
      </div>
      <div class="cs-section" style="margin-bottom:1.25rem;">
        <h4 style="font-family:'Space Grotesk',sans-serif;color:var(--text-light);font-size:1.05rem;margin-bottom:0.25rem;">✦ ${h.concept}</h4>
        <p style="margin:0;font-size:0.95rem;">${cs.concept}</p>
      </div>
      <div class="cs-section" style="margin-bottom:1.25rem;">
        <h4 style="font-family:'Space Grotesk',sans-serif;color:var(--text-light);font-size:1.05rem;margin-bottom:0.25rem;">✦ ${h.challenge}</h4>
        <p style="margin:0;font-size:0.95rem;">${cs.challenge}</p>
      </div>
      <div class="cs-section" style="margin-bottom:1.25rem;">
        <h4 style="font-family:'Space Grotesk',sans-serif;color:var(--text-light);font-size:1.05rem;margin-bottom:0.25rem;">✦ ${h.solution}</h4>
        <p style="margin:0;font-size:0.95rem;">${cs.solution}</p>
      </div>
    `;
  } else {
    elements.modalBody.innerHTML = '';
  }
  
  // Media (Autoplay YouTube Video vs Image)
  elements.modalMedia.innerHTML = '';
  if (project.category === "Video") {
    const embedUrl = getYouTubeEmbedUrl(project.href || project.imgSrc);
    if (embedUrl) {
      elements.modalMedia.innerHTML = `<iframe src="${embedUrl}" allow="autoplay; encrypted-media" allowfullscreen></iframe>`;
    }
  } else {
    elements.modalMedia.innerHTML = `<img src="${project.imgSrc}" alt="${title}" />`;
  }
  
  elements.modal.classList.add('active');
  if (window.lenis) window.lenis.stop();
}

function closeCaseStudyModal() {
  if (elements.modal) elements.modal.classList.remove('active');
  if (elements.modalMedia) elements.modalMedia.innerHTML = '';
  if (window.lenis) window.lenis.start();
}

elements.closeModalBtn?.addEventListener('click', closeCaseStudyModal);
elements.modalBackdrop?.addEventListener('click', closeCaseStudyModal);

// ==========================================
// Lightbox Implementation
// ==========================================
function openLightbox(project) {
  const lightboxModal = document.getElementById("lightboxModal");
  const lightboxImage = document.getElementById("lightboxImage");
  const lightboxLoader = document.getElementById("lightboxLoader");
  const lightboxVideoWrapper = document.getElementById("lightboxVideoWrapper");
  const lightboxVideo = document.getElementById("lightboxVideo");
  
  if (!lightboxModal) return;
  
  lightboxLoader.style.display = "block";
  lightboxImage.style.display = "none";
  if (lightboxVideoWrapper) lightboxVideoWrapper.style.display = "none";
  if (lightboxVideo) lightboxVideo.src = "";
  lightboxImage.src = "";
  
  const title = typeof project.title === 'object' ? project.title[currentLang] : (project.title || "Sản phẩm");
  
  if (project.category === "Video") {
    const embedUrl = getYouTubeEmbedUrl(project.href || project.imgSrc);
    if (embedUrl && lightboxVideoWrapper && lightboxVideo) {
      lightboxLoader.style.display = "none";
      lightboxVideo.src = embedUrl;
      lightboxVideoWrapper.style.display = "block";
      lightboxModal.classList.add("show");
    } else {
      window.open(project.href || project.imgSrc, '_blank');
    }
  } else {
    lightboxImage.src = project.imgSrc;
    lightboxImage.alt = title;
    lightboxModal.classList.add("show");
  }
  
  if (window.lenis) window.lenis.stop();
}

// ==========================================
// YouTube Embed URL Parser
// ==========================================
function getYouTubeEmbedUrl(url) {
  if (!url) return null;
  let videoId = "";
  if (url.includes("youtube.com/watch")) {
    const urlParams = new URLSearchParams(new URL(url).search);
    videoId = urlParams.get("v");
  } else if (url.includes("youtu.be/")) {
    videoId = url.split("youtu.be/")[1]?.split("?")[0];
  } else if (url.includes("youtube.com/shorts/")) {
    videoId = url.split("youtube.com/shorts/")[1]?.split("?")[0];
  } else if (url.includes("youtube.com/embed/")) {
    videoId = url.split("youtube.com/embed/")[1]?.split("?")[0];
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

// ==========================================
// Dynamic Showcase Slider
// ==========================================
let sliderInterval = null;
let currentSlideIndex = 0;

function initShowcaseSlider() {
  const slidesContainer = document.getElementById('showcaseSlides');
  const dotsContainer = document.getElementById('sliderDots');
  const prevBtn = document.getElementById('prevSlideBtn');
  const nextBtn = document.getElementById('nextSlideBtn');
  
  if (!slidesContainer || projectsData.length === 0) return;
  
  // 1. Choose 1 random featured video
  const featuredVideos = projectsData.filter(p => p.category === 'Video' && p.isFeatured);
  const selectedVideo = featuredVideos.length > 0 
    ? featuredVideos[Math.floor(Math.random() * featuredVideos.length)]
    : projectsData.find(p => p.category === 'Video');
    
  const getYouTubeThumbnail = (url) => {
    if (!url) return '';
    let videoId = "";
    if (url.includes("youtube.com/watch")) {
      const urlParams = new URLSearchParams(new URL(url).search);
      videoId = urlParams.get("v");
    } else if (url.includes("youtu.be/")) {
      videoId = url.split("youtu.be/")[1]?.split("?")[0];
    } else if (url.includes("youtube.com/shorts/")) {
      videoId = url.split("youtube.com/shorts/")[1]?.split("?")[0];
    }
    
    if (videoId) {
      return `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`;
    }
    return 'assets/img/thumbnails/thumbnail_default.jpg';
  };
  
  let slidesHtml = '';
  
  if (selectedVideo) {
    const videoThumb = getYouTubeThumbnail(selectedVideo.href);
    const videoTitle = typeof selectedVideo.title === 'object' ? selectedVideo.title[currentLang] : selectedVideo.title;
    const tagText = currentLang === 'vi' ? 'Sản xuất Video' : 'Video Production';
    slidesHtml += `
      <div class="showcase-slide active" data-type="video" data-video-src="${selectedVideo.href}">
        <div class="yt-facade" style="background-image: url('${videoThumb}');" aria-label="Phát video: ${videoTitle}">
          <div class="yt-play-btn" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="24" height="24"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>
          </div>
        </div>
        <div class="showcase-info">
          <span class="tag">${tagText}</span>
          <h3>${videoTitle}</h3>
        </div>
      </div>
    `;
  }
  
  // 2. Select 4 random image projects
  const imageProjects = projectsData.filter(p => (p.category === 'Design' || p.category === 'Photography') && p.imgSrc);
  const shuffledImages = [...imageProjects].sort(() => 0.5 - Math.random());
  const selectedImages = shuffledImages.slice(0, 4);
  
  selectedImages.forEach(imgProj => {
    const title = typeof imgProj.title === 'object' ? imgProj.title[currentLang] : imgProj.title;
    const tagText = imgProj.category === 'Design' ? (currentLang === 'vi' ? 'Thiết kế' : 'Design') : (currentLang === 'vi' ? 'Chụp ảnh' : 'Photography');
    slidesHtml += `
      <div class="showcase-slide" data-type="image" data-src="${imgProj.imgSrc}">
        <div class="showcase-img-wrap">
          <div class="showcase-bg-blur" style="background-image: url('${imgProj.imgSrc}');"></div>
          <img src="${imgProj.imgSrc}" alt="${title}" />
        </div>
        <div class="showcase-info">
          <span class="tag">${tagText}</span>
          <h3>${title}</h3>
        </div>
      </div>
    `;
  });
  
  slidesContainer.innerHTML = slidesHtml;
  
  const slides = slidesContainer.querySelectorAll('.showcase-slide');
  currentSlideIndex = 0;
  
  // Render dots
  if (dotsContainer) {
    dotsContainer.innerHTML = '';
    slides.forEach((_, idx) => {
      const dot = document.createElement('div');
      dot.className = `slider-dot ${idx === 0 ? 'active' : ''}`;
      dot.addEventListener('click', () => {
        goToSlide(idx);
        resetInterval();
      });
      dotsContainer.appendChild(dot);
    });
  }
  
  const dots = dotsContainer ? dotsContainer.querySelectorAll('.slider-dot') : [];
  
  function goToSlide(idx) {
    if (slides.length === 0) return;
    slides[currentSlideIndex].classList.remove('active');
    if (dots.length > 0) dots[currentSlideIndex].classList.remove('active');
    
    // Reset video slide if we leave it
    const currentSlide = slides[currentSlideIndex];
    if (currentSlide && currentSlide.dataset.type === 'video') {
      const iframe = currentSlide.querySelector('iframe');
      if (iframe) {
        iframe.src = iframe.src;
      }
    }
    
    currentSlideIndex = (idx + slides.length) % slides.length;
    slides[currentSlideIndex].classList.add('active');
    if (dots.length > 0) dots[currentSlideIndex].classList.add('active');
  }
  
  function nextSlide() {
    goToSlide(currentSlideIndex + 1);
  }
  
  function prevSlide() {
    goToSlide(currentSlideIndex - 1);
  }
  
  if (prevBtn) {
    prevBtn.onclick = () => { prevSlide(); resetInterval(); };
  }
  if (nextBtn) {
    nextBtn.onclick = () => { nextSlide(); resetInterval(); };
  }
  
  // Video facade click to load iframe on demand
  slidesContainer.addEventListener('click', (e) => {
    const facade = e.target.closest('.yt-facade');
    if (facade) {
      const slide = facade.closest('.showcase-slide');
      const videoSrc = slide.dataset.videoSrc;
      if (videoSrc) {
        const embedUrl = getYouTubeEmbedUrl(videoSrc);
        if (embedUrl) {
          const iframe = document.createElement('iframe');
          iframe.src = embedUrl;
          iframe.title = slide.querySelector('h3').textContent;
          iframe.setAttribute('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share');
          iframe.setAttribute('allowfullscreen', '');
          facade.replaceWith(iframe);
        }
      }
    }
  });
  
  // Image slide lightbox click
  slides.forEach(slide => {
    if (slide.dataset.type === 'image') {
      const imgWrap = slide.querySelector('.showcase-img-wrap');
      if (imgWrap) {
        imgWrap.style.cursor = 'zoom-in';
        imgWrap.addEventListener('click', () => {
          const src = slide.dataset.src;
          const title = slide.querySelector('h3').textContent;
          openLightbox({ imgSrc: src, category: 'Photography', title: title });
        });
      }
    }
  });
  
  // Autoplay
  function startInterval() {
    clearInterval(sliderInterval);
    sliderInterval = setInterval(nextSlide, 10000);
  }
  
  function resetInterval() {
    startInterval();
  }
  
  const sliderEl = document.getElementById('showcaseSlider');
  if (sliderEl) {
    sliderEl.onmouseenter = () => clearInterval(sliderInterval);
    sliderEl.onmouseleave = () => startInterval();
  }
  
  // Swipe support
  let touchStartX = 0;
  let touchEndX = 0;
  
  slidesContainer.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });
  
  slidesContainer.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    const threshold = 55;
    if (touchStartX - touchEndX > threshold) {
      nextSlide();
      resetInterval();
    } else if (touchEndX - touchStartX > threshold) {
      prevSlide();
      resetInterval();
    }
  }, { passive: true });
  
  startInterval();
}

// Start Application
document.addEventListener('DOMContentLoaded', initApp);
