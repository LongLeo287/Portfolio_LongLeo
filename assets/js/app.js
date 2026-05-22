// ==========================================
// Phase 1: Dynamic Data, i18n & Case Study Modal
// ==========================================

let projectsData = [];
let currentLang = localStorage.getItem('portfolio_lang') || 'vi';

const elements = {
  grid: document.getElementById('portfolioGrid'),
  slides: document.getElementById('showcaseSlides'),
  filterBtns: document.querySelectorAll('.filter-btn'),
  langBtns: document.querySelectorAll('.lang-btn'),
  
  // Modal
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
    updateStaticTranslations();
    
  } catch (error) {
    console.error("Error loading projects:", error);
    elements.grid.innerHTML = `<p style="text-align:center;width:100%;">Failed to load projects data.</p>`;
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
      elements.langBtns.forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      currentLang = e.target.dataset.lang;
      localStorage.setItem('portfolio_lang', currentLang);
      
      // We can implement dynamic string replacement for static texts here in the future
      // For now, just re-render dynamic content
      renderPortfolio();
      updateStaticTranslations();
    });
  });
}


// ==========================================
// Static Translations
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
    hero_pill: 'Video Editor • Motion Graphic • Visual Storyteller',
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
    filter_thumb: 'YouTube Thumbnail'
  },
  en: {
    nav_home: 'Home',
    nav_about: 'About',
    nav_services: 'Services',
    nav_exp: 'Experience',
    nav_port: 'Portfolio',
    nav_contact: 'Contact',
    nav_collab: 'Let\'s Talk',
    hero_pill: 'Video Editor • Motion Graphic • Visual Storyteller',
    hero_desc: 'Turning ideas into vivid visuals — from video production, motion graphics, graphic design to UI/UX optimization.<br>Over 7 years of experience in creating high-quality media products.',
    hero_btn1: 'View portfolio ↗',
    hero_btn2: 'Let\'s Talk ✉',
    stat_exp: 'years of experience',
    stat_proj: 'companies & projects',
    stat_start: 'started journey',
    filter_all: 'Featured',
    filter_vid: 'Video Production',
    filter_des: 'Design',
    filter_photo: 'Photography',
    filter_thumb: 'YouTube Thumbnail'
  }
};

function updateStaticTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    if (translations[currentLang] && translations[currentLang][key]) {
      el.innerHTML = translations[currentLang][key];
    }
  });
}

// ==========================================
// Render Portfolio Grid & Slider
// ==========================================
function renderPortfolio(filter = 'all') {
  if (!elements.grid) return;
  
  elements.grid.innerHTML = '';
  
  let displayedCards = [];
  
  projectsData.forEach(p => {
    // Check filter
    if (filter === 'all' && !p.isFeatured) return; // 'all' means 'Featured/Nổi bật'
    if (filter !== 'all' && p.category !== filter) return;
    
    const card = document.createElement('a');
    card.className = 'portfolio-card fade-up';
    card.dataset.category = p.category;
    card.dataset.id = p.id;
    card.href = p.href || p.imgSrc;
    card.target = "_blank";
    
    // Multi-lang support for title and client
    const title = typeof p.title === 'object' ? p.title[currentLang] : p.title;
    const client = typeof p.client === 'object' ? p.client[currentLang] : p.client;
    
    // Thumbnail container
    const thumbDiv = document.createElement('div');
    thumbDiv.className = 'portfolio-thumb';
    thumbDiv.innerHTML = `
      <img src="${p.imgSrc}" alt="${p.alt || title}" loading="lazy" />
      <span class="tag">${p.category}</span>
    `;
    card.appendChild(thumbDiv);
    
    // Body container (if featured or has title)
    if (title || client) {
      const bodyDiv = document.createElement('div');
      bodyDiv.className = 'portfolio-body';
      bodyDiv.innerHTML = `
        <p class="client">${client}</p>
        <h3>${title}</h3>
      `;
      card.appendChild(bodyDiv);
    }
    
    // Bind click event for Modal or Lightbox
    card.addEventListener('click', (e) => handleCardClick(e, p));
    
    elements.grid.appendChild(card);
    displayedCards.push(card);
  });
  
  // Trigger animations
  setTimeout(() => {
    displayedCards.forEach((card, idx) => {
      card.style.transitionDelay = `${idx * 0.05}s`;
      card.classList.add('show');
    });
  }, 50);
}

// ==========================================
// Filters
// ==========================================
function initFilters() {
  elements.filterBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      elements.filterBtns.forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      renderPortfolio(e.target.dataset.filter);
    });
  });
}

// ==========================================
// Handle Click: Modal vs Lightbox
// ==========================================
function handleCardClick(e, project) {
  e.preventDefault();
  
  if (project.caseStudy) {
    // Open Case Study Modal
    openCaseStudyModal(project);
  } else {
    // Open Simple Lightbox (Fallback to opening new tab for now)
    window.open(project.href || project.imgSrc, '_blank');
  }
}

// ==========================================
// Case Study Modal
// ==========================================
function openCaseStudyModal(project) {
  const title = typeof project.title === 'object' ? project.title[currentLang] : project.title;
  const client = typeof project.client === 'object' ? project.client[currentLang] : project.client;
  const caseStudy = typeof project.caseStudy === 'object' ? project.caseStudy[currentLang] : project.caseStudy;
  
  elements.modalTitle.textContent = title;
  elements.modalClient.textContent = client;
  elements.modalLink.href = project.href || project.imgSrc;
  
  // Tags
  let tagsHtml = '';
  if (project.tags) {
    const tagsArr = Array.isArray(project.tags) ? project.tags : project.tags.split(',');
    tagsHtml = tagsArr.map(t => `<span>${t.trim()}</span>`).join('');
  } else {
    tagsHtml = `<span>${project.category}</span>`;
  }
  elements.modalTags.innerHTML = tagsHtml;
  
  // Body (Markdown/HTML mapping)
  if (caseStudy) {
    // Simple basic text formatting
    const formattedBody = caseStudy
      .split('\\n').join('<br/>') // Handle escaped newlines
      .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>'); // Handle basic markdown bold
    elements.modalBody.innerHTML = formattedBody;
  } else {
    elements.modalBody.innerHTML = '';
  }
  
  // Media (Video or Image)
  elements.modalMedia.innerHTML = '';
  if (project.href && project.href.includes('youtube.com/watch')) {
    const videoId = new URL(project.href).searchParams.get('v');
    elements.modalMedia.innerHTML = `<iframe src="https://www.youtube.com/embed/${videoId}?autoplay=1" allow="autoplay; encrypted-media" allowfullscreen></iframe>`;
  } else {
    elements.modalMedia.innerHTML = `<img src="${project.imgSrc}" alt="${title}" />`;
  }
  
  // Show Modal
  elements.modal.classList.add('active');
  if (typeof lenis !== 'undefined') lenis.stop();
}

function closeCaseStudyModal() {
  elements.modal.classList.remove('active');
  elements.modalMedia.innerHTML = ''; // Stop video playback
  if (typeof lenis !== 'undefined') lenis.start();
}

elements.closeModalBtn?.addEventListener('click', closeCaseStudyModal);
elements.modalBackdrop?.addEventListener('click', closeCaseStudyModal);

// Start
document.addEventListener('DOMContentLoaded', initApp);
