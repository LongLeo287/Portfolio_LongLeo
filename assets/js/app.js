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
      
      elements.langBtns.forEach(b => {
        if (b.dataset.lang === selectedBtn.dataset.lang) {
          b.classList.add('active');
        } else {
          b.classList.remove('active');
        }
      });
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
    available_for: 'Sẵn sàng hợp tác',
    about_eyebrow: 'Một chút về mình',
    about_title: 'Từ Arena Multimedia đến hành trình sáng tạo hình ảnh chuyên nghiệp.',
    about_p1: 'Chào bạn, mình là <strong>Hà Đình Long</strong> — hay còn được biết đến với tên <strong>Long Leo</strong>. Tốt nghiệp ngành Multimedia tại Arena Multimedia, mình bắt đầu hành trình sáng tạo từ năm 2015.',
    about_p2: 'Với hơn 7 năm kinh nghiệm trong lĩnh vực sản xuất video, thiết kế đồ họa và truyền thông đa phương tiện, mình đã đi qua nhiều môi trường từ agency, công ty sản phẩm đến freelance — mỗi giai đoạn giúp mình tích lũy thêm góc nhìn và kỹ năng mới.',
    about_p3: '<strong>Mục tiêu dài hạn:</strong> Trở thành Chuyên gia hoạch định Chiến lược nội dung (Content Strategist), dẫn dắt đội ngũ sáng tạo và quản lý các dự án truyền thông đa phương tiện quy mô lớn.',
    about_skill2: 'Motion Graphic, Color Grading, UI/UX Design, Photography',
    about_skill3: 'Sáng tạo Ý tưởng (Ideation), SEO Video, Thiết kế đồ họa đa phương tiện',
    tools_title: 'Công cụ & Trợ lý AI sáng tạo',
    tools_group1_title: 'Phần mềm sáng tạo chuyên nghiệp',
    tool_prem: 'Dựng phim & Màu sắc',
    tool_ae: 'Motion & Hậu kỳ kỹ xảo',
    tool_ps: 'Chỉnh ảnh & Cắt ghép',
    tool_ai: 'Thiết kế Vector & Ấn phẩm',
    tool_lr: 'Blend màu & Hậu kỳ ảnh',
    tool_figma: 'Thiết kế giao diện UI/UX',
    tool_capcut: 'Dựng video nhanh & Tiện lợi',
    tool_canva: 'Thiết kế đồ họa trực tuyến',
    tools_group2_title: 'Trợ lý AI & Tối ưu hiệu suất',
    tool_gemini: 'Lên ý tưởng & Lịch trình',
    tool_ai_studio: 'Thử nghiệm Prompt & API',
    tool_antigravity: 'Tự động hóa & Coding',
    tool_claude: 'Phân tích & Viết nội dung',
    tool_codex: 'Hỗ trợ Kỹ thuật & Code',
    services_eyebrow: 'Dịch vụ',
    services_title: 'Giải pháp hình ảnh & truyền thông toàn diện.',
    services_desc: 'Tập trung vào chất lượng hình ảnh, nhịp kể và tính ứng dụng thực tế — từ video, thiết kế đến UI/UX cho các chiến dịch truyền thông.',
    srv_vid_title: 'Quay & Dựng Video',
    srv_vid_desc: 'Sản xuất video chuyên nghiệp: TVC, quảng cáo, unboxing, review sản phẩm, video sự kiện và các định dạng social media.',
    srv_motion_title: 'Motion Graphic',
    srv_motion_desc: 'Tạo hiệu ứng chuyển động bắt mắt, title animation, infographic động và các visual effects chuyên nghiệp bằng After Effects.',
    srv_design_title: 'Thiết kế đồ họa',
    srv_design_desc: 'Thiết kế banner, poster, thumbnail, key visual và ấn phẩm truyền thông phục vụ chiến dịch marketing trên mọi nền tảng.',
    srv_photo_title: 'Chụp ảnh sản phẩm',
    srv_photo_desc: 'Chụp ảnh sản phẩm, sự kiện, không gian thương hiệu — chỉnh sửa hậu kỳ chất lượng cao phục vụ quảng bá.',
    srv_uiux_title: 'Thiết kế UI/UX',
    srv_uiux_desc: 'Thiết kế giao diện & trải nghiệm người dùng cho landing page, website — đảm bảo thẩm mỹ hiện đại và thân thiện.',
    srv_idea_title: 'Sáng tạo Ý tưởng',
    srv_idea_desc: 'Đề xuất và phát triển các concept sáng tạo, lên ý tưởng hình ảnh và định hướng nội dung trước khi sản xuất.',
    exp_eyebrow: 'Kinh nghiệm',
    exp_title: 'Hành trình 7+ năm trong ngành sáng tạo.',
    exp_desc: 'Từ in ấn, đào tạo, freelance, đến thương hiệu công nghệ — mỗi môi trường tạo thêm một góc nhìn mới về truyền thông và sáng tạo.',
    exp_v2h_role: 'Nhân viên Media',
    exp_v2h_time: '2025 – nay',
    exp_v2h_desc: 'Quay dựng video review thiết bị âm thanh & công nghệ (JBL, Bose, Sony, Marshall). Quản lý kênh YouTube, thiết kế thumbnail, tối ưu SEO.',
    exp_v2h_btn: 'Ghé thăm Vua2Hand ↗',
    exp_mygear_role: 'Nhân viên Media',
    exp_mygear_desc: 'Thiết kế UI/UX landing page & website. Sản xuất video, thiết kế banner/poster, chụp ảnh sản phẩm. Đóng góp xây dựng ý tưởng hình ảnh cùng đội ngũ sáng tạo.',
    exp_mygear_btn: 'Ghé thăm MyGear ↗',
    exp_vie_role: 'Editor Tự do',
    exp_vie_desc: 'Hậu kỳ chuyên nghiệp: xử lý file thô, cắt ghép, color grading, đồng bộ âm thanh. Tư vấn giải pháp hình ảnh trực tiếp với khách hàng.',
    exp_vie_btn: 'Ghé thăm Vie Channel ↗',
    exp_topskills_role: 'Nhân viên Media',
    exp_topskills_desc: 'Sản xuất & hậu kỳ video đào tạo. Thiết kế ấn phẩm thương hiệu (banner, poster). Phối hợp phát triển các ý tưởng sáng tạo cho dự án.',
    exp_topskills_btn: 'Ghé thăm TopSkills ↗',
    exp_tgia_role: 'Nhân viên Media',
    exp_tgia_desc: 'Thiết kế và xử lý file in ấn. Hỗ trợ sản xuất nội dung truyền thông, quay dựng video cơ bản và chụp ảnh sản phẩm cho các chiến dịch của công ty.',
    exp_tgia_btn: 'Ghé thăm Thế Giới In Ấn ↗',
    port_eyebrow: 'Portfolio',
    port_title: 'Sản phẩm nổi bật',
    port_desc: 'Tổng hợp các sản phẩm video và nội dung sáng tạo từ kênh YouTube @LongLeo287 và các dự án thực tế.',
    contact_eyebrow: 'Liên hệ',
    contact_title: 'Cảm ơn bạn đã dành thời gian ghé thăm.',
    contact_desc: 'Cần người quay dựng, thiết kế, làm motion graphic hoặc tối ưu UI/UX? Hãy liên hệ để bắt đầu trao đổi về dự án của bạn.',
    contact_email_btn: 'Gửi email ✉',
    contact_phone_btn: 'Gọi ngay ☎',
    contact_addr_label: 'Địa chỉ',
    contact_addr_val: 'Tân Phú, Hồ Chí Minh',
    footer_copy: 'Hà Đình Long © 2026 | All Rights Reserved.',
    footer_sub: 'Video Editor Portfolio',
    modal_view_link: 'Xem dự án ↗',
    lang_label: 'Ngôn ngữ',
    theme_aria: 'Chuyển chế độ sáng/tối',
    filter_all: 'Nổi bật',
    filter_vid: 'Sản xuất Video',
    filter_des: 'Thiết kế',
    filter_photo: 'Chụp ảnh',
    filter_thumb: 'YouTube Thumbnail',
    categories: {
      video: 'Sản xuất Video',
      design: 'Thiết kế',
      photography: 'Chụp ảnh'
    }
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
    available_for: 'Available for',
    about_eyebrow: 'A little about me',
    about_title: 'From Arena Multimedia to a professional visual creation journey.',
    about_p1: 'Hello, I\'m <strong>Ha Dinh Long</strong> — also known as <strong>Long Leo</strong>. Graduated in Multimedia from Arena Multimedia, I started my creative journey in 2015.',
    about_p2: 'With over 7 years of experience in video production, graphic design, and multimedia communications, I have worked across various environments from agencies and product companies to freelancing — each stage helping me gain new perspectives and skills.',
    about_p3: '<strong>Long-term Goal:</strong> Become a Content Strategist, leading creative teams and managing large-scale multimedia communication projects.',
    about_skill2: 'Motion Graphics, Color Grading, UI/UX Design, Photography',
    about_skill3: 'Ideation, Video SEO, Multimedia Graphic Design',
    tools_title: 'Tools & Creative AI Assistants',
    tools_group1_title: 'Professional Creative Software',
    tool_prem: 'Video Editing & Color Grading',
    tool_ae: 'Motion Graphics & Visual Effects',
    tool_ps: 'Photo Editing & Compositing',
    tool_ai: 'Vector Design & Print Publications',
    tool_lr: 'Color Grading & Photo Post-processing',
    tool_figma: 'UI/UX Interface Design',
    tool_capcut: 'Fast & Convenient Video Editing',
    tool_canva: 'Online Graphic Design',
    tools_group2_title: 'AI Assistants & Performance Optimization',
    tool_gemini: 'Brainstorming & Scheduling',
    tool_ai_studio: 'Prompting & API Experimentation',
    tool_antigravity: 'Automation & Coding',
    tool_claude: 'Analysis & Content Writing',
    tool_codex: 'Technical Support & Code',
    services_eyebrow: 'Services',
    services_title: 'Comprehensive Video & Media Solutions.',
    services_desc: 'Focusing on visual quality, storytelling rhythm, and practical application — from video, design to UI/UX for media campaigns.',
    srv_vid_title: 'Video Production',
    srv_vid_desc: 'Professional video production: TVCs, commercials, unboxing, product reviews, event videos, and social media formats.',
    srv_motion_title: 'Motion Graphics',
    srv_motion_desc: 'Creating eye-catching motion graphics, title animations, animated infographics, and professional visual effects with After Effects.',
    srv_design_title: 'Graphic Design',
    srv_design_desc: 'Designing banners, posters, thumbnails, key visuals, and marketing assets for all digital platforms.',
    srv_photo_title: 'Product Photography',
    srv_photo_desc: 'Capturing products, events, and brand spaces — high-quality post-processing for promotional use.',
    srv_uiux_title: 'UI/UX Design',
    srv_uiux_desc: 'Designing user interfaces & experiences for landing pages and websites — ensuring modern aesthetics and user-friendliness.',
    srv_idea_title: 'Creative Ideation',
    srv_idea_desc: 'Proposing and developing creative concepts, visual ideas, and content direction prior to production.',
    exp_eyebrow: 'Experience',
    exp_title: 'A 7+ year journey in the creative industry.',
    exp_desc: 'From printing, training, and freelancing to technology brands — each environment shapes a new perspective on media and creativity.',
    exp_v2h_role: 'Media Specialist',
    exp_v2h_time: '2025 – Present',
    exp_v2h_desc: 'Filming and editing video reviews for audio & tech gear (JBL, Bose, Sony, Marshall). Managing YouTube channels, designing thumbnails, and optimizing SEO.',
    exp_v2h_btn: 'Visit Vua2Hand ↗',
    exp_mygear_role: 'Media Specialist',
    exp_mygear_desc: 'Designing landing page & website UI/UX. Producing videos, designing banners/posters, and shooting product photography. Contributing visual ideas with the creative team.',
    exp_mygear_btn: 'Visit MyGear ↗',
    exp_vie_role: 'Freelance Video Editor',
    exp_vie_desc: 'Professional post-production: processing raw files, editing, color grading, and audio syncing. Consulting visual solutions directly with clients.',
    exp_vie_btn: 'Visit Vie Channel ↗',
    exp_topskills_role: 'Media Specialist',
    exp_topskills_desc: 'Producing & editing training videos. Designing brand identity assets (banners, posters). Collaborating to develop creative ideas for projects.',
    exp_topskills_btn: 'Visit TopSkills ↗',
    exp_tgia_role: 'Media Specialist',
    exp_tgia_desc: 'Designing and processing print files. Supporting media content creation, basic videography, and product photography for company campaigns.',
    exp_tgia_btn: 'Visit Thế Giới In Ấn ↗',
    port_eyebrow: 'Portfolio',
    port_title: 'Featured Work',
    port_desc: 'A compilation of video productions and creative content from YouTube channel @LongLeo287 and real-world projects.',
    contact_eyebrow: 'Contact',
    contact_title: 'Thank you for taking the time to visit.',
    contact_desc: 'Need someone for video editing, design, motion graphics, or UI/UX optimization? Let\'s get in touch to discuss your project.',
    contact_email_btn: 'Email Me ✉',
    contact_phone_btn: 'Call Now ☎',
    contact_addr_label: 'Address',
    contact_addr_val: 'Tan Phu, Ho Chi Minh City',
    footer_copy: 'Ha Dinh Long © 2026 | All Rights Reserved.',
    footer_sub: 'Video Editor Portfolio',
    modal_view_link: 'View Project ↗',
    lang_label: 'Language',
    theme_aria: 'Toggle Light/Dark Mode',
    filter_all: 'Featured',
    filter_vid: 'Video Production',
    filter_des: 'Design',
    filter_photo: 'Photography',
    filter_thumb: 'YouTube Thumbnail',
    categories: {
      video: 'Video Production',
      design: 'Design',
      photography: 'Photography'
    }
  }
};

function updateStaticTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    if (translations[currentLang] && translations[currentLang][key]) {
      el.innerHTML = translations[currentLang][key];
    }
  });

  const themeToggle = document.getElementById('themeToggle');
  if (themeToggle && translations[currentLang] && translations[currentLang].theme_aria) {
    themeToggle.setAttribute('aria-label', translations[currentLang].theme_aria);
  }
  
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
  
  const getVal = (field) => {
    if (!field) return '';
    if (typeof field === 'object') {
      return field[lang] || field['vi'] || '';
    }
    return field;
  };

  return {
    role: getVal(cs.role),
    concept: getVal(cs.concept),
    challenge: getVal(cs.challenge),
    solution: getVal(cs.solution),
    tools: cs.tools || []
  };
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
let selectedSliderItems = null;
let sliderInterval = null;
let currentSlideIndex = 0;

function initShowcaseSlider() {
  const slidesContainer = document.getElementById('showcaseSlides');
  const dotsContainer = document.getElementById('sliderDots');
  const prevBtn = document.getElementById('prevSlideBtn');
  const nextBtn = document.getElementById('nextSlideBtn');
  
  if (!slidesContainer || projectsData.length === 0) return;
  
  let selectedVideo;
  let selectedImages;

  if (selectedSliderItems) {
    selectedVideo = selectedSliderItems.video;
    selectedImages = selectedSliderItems.images;
  } else {
    // 1. Choose 1 random featured video
    const featuredVideos = projectsData.filter(p => p.category === 'Video' && p.isFeatured);
    selectedVideo = featuredVideos.length > 0 
      ? featuredVideos[Math.floor(Math.random() * featuredVideos.length)]
      : projectsData.find(p => p.category === 'Video');
      
    // 2. Select 4 random image projects
    const imageProjects = projectsData.filter(p => (p.category === 'Design' || p.category === 'Photography') && p.imgSrc);
    const shuffledImages = [...imageProjects].sort(() => 0.5 - Math.random());
    selectedImages = shuffledImages.slice(0, 4);
    
    selectedSliderItems = {
      video: selectedVideo,
      images: selectedImages
    };
  }
  
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
  let slideIndexCounter = 0;
  
  if (selectedVideo) {
    const isActive = slideIndexCounter === currentSlideIndex;
    const videoThumb = getYouTubeThumbnail(selectedVideo.href);
    const videoTitle = typeof selectedVideo.title === 'object' ? selectedVideo.title[currentLang] : selectedVideo.title;
    const tagText = translations[currentLang].categories.video;
    slidesHtml += `
      <div class="showcase-slide ${isActive ? 'active' : ''}" data-type="video" data-video-src="${selectedVideo.href}">
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
    slideIndexCounter++;
  }
  
  selectedImages.forEach(imgProj => {
    const isActive = slideIndexCounter === currentSlideIndex;
    const title = typeof imgProj.title === 'object' ? imgProj.title[currentLang] : imgProj.title;
    const tagText = imgProj.category === 'Design' ? translations[currentLang].categories.design : translations[currentLang].categories.photography;
    slidesHtml += `
      <div class="showcase-slide ${isActive ? 'active' : ''}" data-type="image" data-src="${imgProj.imgSrc}">
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
    slideIndexCounter++;
  });
  
  slidesContainer.innerHTML = slidesHtml;
  
  const slides = slidesContainer.querySelectorAll('.showcase-slide');
  
  // Render dots
  if (dotsContainer) {
    dotsContainer.innerHTML = '';
    slides.forEach((_, idx) => {
      const dot = document.createElement('div');
      dot.className = `slider-dot ${idx === currentSlideIndex ? 'active' : ''}`;
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
  slidesContainer.nextSlide = nextSlide;
  slidesContainer.prevSlide = prevSlide;
  slidesContainer.resetInterval = resetInterval;
  
  if (!slidesContainer.dataset.swipeBound) {
    let touchStartX = 0;
    let touchEndX = 0;
    
    slidesContainer.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    
    slidesContainer.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      const threshold = 55;
      if (touchStartX - touchEndX > threshold) {
        if (typeof slidesContainer.nextSlide === 'function') slidesContainer.nextSlide();
        if (typeof slidesContainer.resetInterval === 'function') slidesContainer.resetInterval();
      } else if (touchEndX - touchStartX > threshold) {
        if (typeof slidesContainer.prevSlide === 'function') slidesContainer.prevSlide();
        if (typeof slidesContainer.resetInterval === 'function') slidesContainer.resetInterval();
      }
    }, { passive: true });
    
    slidesContainer.dataset.swipeBound = 'true';
  }
  
  startInterval();
}

// Start Application
document.addEventListener('DOMContentLoaded', initApp);
