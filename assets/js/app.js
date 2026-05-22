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
    nav_home: 'Trang&nbsp;chủ',
    nav_about: 'Về&nbsp;mình',
    nav_services: 'Dịch&nbsp;vụ',
    nav_exp: 'Kinh&nbsp;nghiệm',
    nav_port: 'Portfolio',
    nav_contact: 'Liên&nbsp;hệ',
    nav_collab: 'Liên&nbsp;hệ hợp&nbsp;tác',
    hero_pill: '✦ Technical Video Editor • Motion Graphic • UI/UX',
    hero_title: 'Hà Đình <span class="gradient-text">Long</span>',
    hero_desc: 'Biến ý&nbsp;tưởng thành hình&nbsp;ảnh sống&nbsp;động — từ&nbsp;quay&nbsp;dựng video, motion graphic, thiết&nbsp;kế đồ&nbsp;họa đến&nbsp;tối&nbsp;ưu UI/UX.<br>Hơn 7 năm kinh&nbsp;nghiệm tạo ra các sản&nbsp;phẩm truyền&nbsp;thông&nbsp;chất&nbsp;lượng&nbsp;cao.',
    hero_btn1: 'Xem portfolio&nbsp;↗',
    hero_btn_cv: 'Xem CV 📄',
    hero_btn2: 'Liên&nbsp;hệ hợp&nbsp;tác&nbsp;✉',
    stat_exp: 'Năm&nbsp;kinh&nbsp;nghiệm',
    stat_proj: 'Công ty &&nbsp;dự&nbsp;án',
    stat_start: 'Bắt&nbsp;đầu hành&nbsp;trình',
    partners_title: 'ĐỐI TÁC HỢP TÁC',
    available_for: 'Sẵn sàng hợp&nbsp;tác',
    about_eyebrow: 'Một chút về&nbsp;mình',
    about_title: 'Từ&nbsp;Arena Multimedia đến&nbsp;hành trình sáng&nbsp;tạo hình&nbsp;ảnh&nbsp;chuyên&nbsp;nghiệp.',
    about_p1: 'Chào bạn, mình là&nbsp;<strong>Hà Đình Long</strong> — hay còn được biết đến&nbsp;với&nbsp;tên <strong>Long Leo</strong>. Tốt nghiệp ngành Multimedia tại&nbsp;Arena Multimedia, mình bắt&nbsp;đầu hành trình sáng&nbsp;tạo từ&nbsp;năm&nbsp;2015.',
    about_p2: 'Với&nbsp;hơn 7 năm kinh&nbsp;nghiệm trong&nbsp;lĩnh vực Sản&nbsp;xuất video, thiết&nbsp;kế đồ họa và&nbsp;truyền&nbsp;thông đa phương tiện, mình đã trải&nbsp;qua nhiều môi&nbsp;trường làm&nbsp;việc từ&nbsp;agency, in-house đến&nbsp;freelance — mỗi chặng đường đều giúp mình tích&nbsp;lũy thêm những&nbsp;góc&nbsp;nhìn và&nbsp;kỹ năng&nbsp;mới.',
    about_p3: '<strong>Mục&nbsp;tiêu dài&nbsp;hạn:</strong> Trở thành Chuyên gia Hậu&nbsp;kỳ (Post-Production Specialist), không ngừng nâng cấp bộ kỹ năng chuyên&nbsp;môn và ứng dụng các công cụ công nghệ mới (AI, Automation) để tối ưu hóa tốc độ dựng&nbsp;phim và nâng cao chất lượng đầu&nbsp;ra.',
    about_skill1: '<strong>Tư duy Thẩm mỹ:</strong> Cân bằng giữa yếu tố nghệ thuật và mục tiêu truyền thông thực tế.',
    about_skill2: '<strong>Quy trình Tối ưu:</strong> Ứng dụng công nghệ & AI để tối ưu hóa thời gian sản xuất mà vẫn giữ chất lượng cao.',
    about_skill3: '<strong>Thích ứng Nhanh:</strong> Khả năng đảm nhiệm linh hoạt nhiều vai trò từ Quay, Dựng, đến Thiết kế và UI/UX.',
    tools_title: 'Công cụ & Trợ lý AI&nbsp;sáng&nbsp;tạo',
    tools_group1_title: 'Phần mềm sáng&nbsp;tạo&nbsp;chuyên&nbsp;nghiệp',
    tool_prem: 'Dựng phim & Màu&nbsp;sắc',
    tool_ae: 'Motion & hậu&nbsp;kỳ kỹ&nbsp;xảo',
    tool_ps: 'Chỉnh ảnh & Cắt&nbsp;ghép',
    tool_ai: 'Thiết&nbsp;kế Vector &&nbsp;ấn&nbsp;phẩm',
    tool_lr: 'Blend màu & hậu&nbsp;kỳ&nbsp;ảnh',
    tool_figma: 'Thiết&nbsp;kế giao&nbsp;diện&nbsp;UI/UX',
    tool_capcut: 'Dựng video nhanh &&nbsp;tiện&nbsp;lợi',
    tool_canva: 'Thiết&nbsp;kế đồ họa trực&nbsp;tuyến',
    tools_group2_title: 'Trợ lý AI & tối&nbsp;ưu hiệu&nbsp;suất',
    tool_gemini: 'Lên ý&nbsp;tưởng & Lịch&nbsp;trình',
    tool_ai_studio: 'Thử nghiệm Prompt &&nbsp;API',
    tool_antigravity: 'Tự động hóa &&nbsp;Coding',
    tool_claude: 'Phân tích & Viết&nbsp;nội&nbsp;dung',
    tool_codex: 'Hỗ trợ Kỹ thuật &&nbsp;Code',
    services_eyebrow: 'Dịch&nbsp;vụ',
    services_title: 'Giải&nbsp;pháp hình&nbsp;ảnh & truyền&nbsp;thông toàn&nbsp;diện.',
    services_desc: 'Tập trung vào chất&nbsp;lượng hình&nbsp;ảnh, nhịp kể và&nbsp;tính ứng dụng thực&nbsp;tế <br>— từ&nbsp;video, thiết&nbsp;kế đến&nbsp;UI/UX cho&nbsp;các chiến&nbsp;dịch&nbsp;truyền&nbsp;thông.',
    srv_vid_title: 'Quay & Dựng&nbsp;Video',
    srv_vid_desc: 'Sản&nbsp;xuất video chuyên&nbsp;nghiệp: TVC, quảng&nbsp;cáo, unboxing, review sản&nbsp;phẩm, video sự&nbsp;kiện và&nbsp;các định&nbsp;dạng&nbsp;social&nbsp;media.',
    srv_motion_title: 'Motion&nbsp;Graphic',
    srv_motion_desc: 'Tạo hiệu&nbsp;ứng chuyển&nbsp;động bắt&nbsp;mắt, title animation, infographic động và&nbsp;các visual effects chuyên&nbsp;nghiệp bằng&nbsp;After&nbsp;Effects.',
    srv_design_title: 'Thiết&nbsp;kế đồ&nbsp;họa',
    srv_design_desc: 'Thiết&nbsp;kế banner, poster, thumbnail, key visual và&nbsp;ấn&nbsp;phẩm truyền&nbsp;thông phục&nbsp;vụ các chiến&nbsp;dịch marketing trên&nbsp;mọi&nbsp;nền&nbsp;tảng.',
    srv_photo_title: 'Chụp&nbsp;ảnh&nbsp;sản&nbsp;phẩm',
    srv_photo_desc: 'Chụp&nbsp;ảnh sản&nbsp;phẩm, sự&nbsp;kiện, không&nbsp;gian thương&nbsp;hiệu — chỉnh&nbsp;sửa hậu&nbsp;kỳ chất&nbsp;lượng cao phục&nbsp;vụ&nbsp;quảng&nbsp;bá.',
    srv_uiux_title: 'Thiết&nbsp;kế&nbsp;UI/UX',
    srv_uiux_desc: 'Thiết&nbsp;kế giao&nbsp;diện & trải&nbsp;nghiệm người&nbsp;dùng cho&nbsp;landing page, website — đảm&nbsp;bảo tính thẩm&nbsp;mỹ hiện&nbsp;đại và&nbsp;thân&nbsp;thiện với&nbsp;người&nbsp;dùng.',
    srv_idea_title: 'Sáng&nbsp;tạo&nbsp;ý&nbsp;tưởng',
    srv_idea_desc: 'Đề&nbsp;xuất và&nbsp;phát&nbsp;triển các concept sáng&nbsp;tạo, lên ý&nbsp;tưởng hình&nbsp;ảnh và&nbsp;định&nbsp;hướng nội&nbsp;dung trước khi&nbsp;sản&nbsp;xuất.',
    exp_eyebrow: 'Kinh&nbsp;nghiệm',
    exp_title: 'Hành trình 7+ năm trong&nbsp;ngành&nbsp;sáng&nbsp;tạo.',
    exp_desc: 'Từ&nbsp;in&nbsp;ấn, đào&nbsp;tạo, freelance, đến&nbsp;thương&nbsp;hiệu công&nbsp;nghệ —<br>mỗi môi&nbsp;trường đều mang đến&nbsp;một góc&nbsp;nhìn mới về&nbsp;truyền&nbsp;thông và&nbsp;sáng&nbsp;tạo.',
    exp_v2h_role: 'Nhân&nbsp;viên&nbsp;Media',
    exp_v2h_time: '2025 –&nbsp;nay',
    exp_v2h_desc: 'Quay&nbsp;dựng video review thiết&nbsp;bị âm&nbsp;thanh & công&nbsp;nghệ (JBL, Bose, Sony, Marshall). Quản&nbsp;lý kênh YouTube, thiết&nbsp;kế thumbnail,&nbsp;tối&nbsp;ưu&nbsp;SEO.',
    exp_v2h_btn: 'Ghé&nbsp;thăm Vua2Hand&nbsp;↗',
    exp_mygear_role: 'Nhân&nbsp;viên&nbsp;Media',
    exp_mygear_desc: 'Thiết&nbsp;kế UI/UX landing page & website. Sản&nbsp;xuất video, thiết&nbsp;kế banner/poster, Chụp&nbsp;ảnh sản&nbsp;phẩm. Đóng&nbsp;góp xây dựng ý&nbsp;tưởng hình&nbsp;ảnh cùng đội ngũ&nbsp;sáng&nbsp;tạo.',
    exp_mygear_btn: 'Ghé&nbsp;thăm MyGear&nbsp;↗',
    exp_vie_role: 'Editor Tự&nbsp;do',
    exp_vie_desc: 'Hậu&nbsp;kỳ chuyên&nbsp;nghiệp: xử lý file thô, cắt ghép, color grading, đồng bộ âm&nbsp;thanh. Tư&nbsp;vấn giải&nbsp;pháp hình&nbsp;ảnh trực&nbsp;tiếp với&nbsp;khách&nbsp;hàng.',
    exp_vie_btn: 'Ghé&nbsp;thăm Vie Channel&nbsp;↗',
    exp_topskills_role: 'Nhân&nbsp;viên&nbsp;Media',
    exp_topskills_desc: 'Sản&nbsp;xuất & hậu&nbsp;kỳ video đào&nbsp;tạo. Thiết&nbsp;kế ấn&nbsp;phẩm thương&nbsp;hiệu (banner, poster). Phối&nbsp;hợp phát&nbsp;triển các ý&nbsp;tưởng sáng&nbsp;tạo cho&nbsp;dự&nbsp;án.',
    exp_topskills_btn: 'Ghé&nbsp;thăm TopSkills&nbsp;↗',
    exp_tgia_role: 'Nhân&nbsp;viên&nbsp;Media',
    exp_tgia_desc: 'Thiết&nbsp;kế và&nbsp;xử lý file in&nbsp;ấn. Hỗ trợ sản&nbsp;xuất nội&nbsp;dung truyền&nbsp;thông, quay&nbsp;dựng video cơ bản và&nbsp;Chụp&nbsp;ảnh sản&nbsp;phẩm cho&nbsp;các chiến&nbsp;dịch của&nbsp;công&nbsp;ty.',
    exp_tgia_btn: 'Ghé&nbsp;thăm Thế Giới In Ấn&nbsp;↗',
    port_eyebrow: 'Portfolio',
    port_title: 'Sản&nbsp;phẩm&nbsp;nổi&nbsp;bật',
    port_desc: 'Tổng&nbsp;hợp các sản&nbsp;phẩm video và&nbsp;nội&nbsp;dung sáng&nbsp;tạo từ&nbsp;kênh YouTube @LongLeo287 và&nbsp;các dự&nbsp;án&nbsp;thực&nbsp;tế.',
    contact_eyebrow: 'Liên&nbsp;hệ',
    contact_title: 'Cảm&nbsp;ơn bạn đã dành thời&nbsp;gian&nbsp;ghé&nbsp;thăm.',
    contact_desc: 'Cần&nbsp;người quay&nbsp;dựng, thiết&nbsp;kế, làm motion graphic hoặc&nbsp;tối&nbsp;ưu UI/UX? Hãy&nbsp;liên&nbsp;hệ để bắt&nbsp;đầu trao&nbsp;đổi về&nbsp;dự&nbsp;án&nbsp;của&nbsp;bạn.',
    contact_email_btn: 'Gửi email&nbsp;✉',
    contact_phone_btn: 'Gọi ngay&nbsp;☎',
    contact_addr_label: 'Địa&nbsp;chỉ',
    contact_addr_val: 'Tân Phú, Hồ Chí&nbsp;Minh',
    footer_copy: 'Hà Đình Long © 2026 | All Rights&nbsp;Reserved.',
    footer_sub: 'Video Editor&nbsp;Portfolio',
    modal_view_link: 'Xem dự&nbsp;án&nbsp;↗',
    lang_label: 'Ngôn&nbsp;ngữ',
    theme_aria: 'Chuyển chế độ&nbsp;sáng/tối',
    filter_all: 'Nổi&nbsp;bật',
    filter_vid: 'Sản&nbsp;xuất&nbsp;Video',
    filter_des: 'Thiết&nbsp;kế',
    filter_photo: 'Chụp&nbsp;ảnh',
    filter_thumb: 'YouTube&nbsp;Thumbnail',
    categories: {
      video: 'Sản&nbsp;xuất&nbsp;Video',
      design: 'Thiết&nbsp;kế',
      photography: 'Chụp&nbsp;ảnh'
    }
  },
  en: {
    nav_home: 'Home',
    nav_about: 'About',
    nav_services: 'Services',
    nav_exp: 'Experience',
    nav_port: 'Portfolio',
    nav_contact: 'Contact',
    nav_collab: 'Let\'s collaborate',
    hero_pill: '✦ Technical Video Editor • Motion Graphic • UI/UX',
    hero_title: 'Ha Dinh <span class="gradient-text">Long</span>',
    hero_desc: 'Turning ideas into vivid visuals — from video production, motion graphics, graphic design to UI/UX&nbsp;optimization.<br>Over 7 years of experience in creating high-quality&nbsp;media&nbsp;products.',
    hero_btn1: 'View Portfolio&nbsp;↗',
    hero_btn_cv: 'View CV 📄',
    hero_btn2: 'Let\'s Talk ✉',
    stat_exp: 'years of&nbsp;experience',
    stat_proj: 'companies &&nbsp;projects',
    stat_start: 'started&nbsp;journey',
    partners_title: 'TRUSTED BY',
    available_for: 'Available&nbsp;for',
    about_eyebrow: 'A little about&nbsp;me',
    about_title: 'From Arena Multimedia to a professional visual creation&nbsp;journey.',
    about_p1: 'Hello,&nbsp;I\'m <strong>Ha Dinh Long</strong> — also known as <strong>Long Leo</strong>. Graduated in Multimedia from Arena Multimedia, I started my creative journey in 2015.',
    about_p2: 'With over 7 years of experience in video production, graphic design, and multimedia communications, I have worked across various environments from agencies, in-house teams to freelance — each stage helping me gain new perspectives&nbsp;and&nbsp;skills.',
    about_p3: '<strong>Long-term Goal:</strong> Become a Post-Production Specialist, continuously upgrading specialized skill sets and applying new technological tools (AI, Automation) to optimize editing speed and enhance output&nbsp;quality.',
    about_skill1: '<strong>Aesthetic Sense:</strong> Balancing artistic elements with practical communication goals.',
    about_skill2: '<strong>Optimized Workflow:</strong> Applying technology & AI to speed up production while maintaining high quality.',
    about_skill3: '<strong>Fast Adaptation:</strong> Ability to flexibly handle multiple roles from Filming, Editing, to 2D/UI Design.',
    tools_title: 'Tools & Creative AI&nbsp;Assistants',
    tools_group1_title: 'Professional Creative&nbsp;Software',
    tool_prem: 'Video Editing & Color&nbsp;Grading',
    tool_ae: 'Motion Graphics & Visual&nbsp;Effects',
    tool_ps: 'Photo Editing &&nbsp;Compositing',
    tool_ai: 'Vector Design & Print&nbsp;Publications',
    tool_lr: 'Color Grading & Photo&nbsp;Post-processing',
    tool_figma: 'UI/UX Interface&nbsp;Design',
    tool_capcut: 'Fast & Convenient Video&nbsp;Editing',
    tool_canva: 'Online Graphic&nbsp;Design',
    tools_group2_title: 'AI Assistants & Performance&nbsp;Optimization',
    tool_gemini: 'Brainstorming &&nbsp;Scheduling',
    tool_ai_studio: 'Prompting & API&nbsp;Experimentation',
    tool_antigravity: 'Automation &&nbsp;Coding',
    tool_claude: 'Analysis & Content&nbsp;Writing',
    tool_codex: 'Technical Support &&nbsp;Code',
    services_eyebrow: 'Services',
    services_title: 'Comprehensive Video & Media&nbsp;Solutions.',
    services_desc: 'Focusing on visual quality, storytelling rhythm, and practical application — from video, design to UI/UX for&nbsp;media&nbsp;campaigns.',
    srv_vid_title: 'Video&nbsp;Production',
    srv_vid_desc: 'Professional video production: TVCs, commercials, unboxing, product reviews, event videos, and social media&nbsp;formats.',
    srv_motion_title: 'Motion&nbsp;Graphics',
    srv_motion_desc: 'Creating eye-catching motion graphics, title animations, animated infographics, and professional visual effects with After&nbsp;Effects.',
    srv_design_title: 'Graphic&nbsp;Design',
    srv_design_desc: 'Designing banners, posters, thumbnails, key visuals, and marketing assets for all digital&nbsp;platforms.',
    srv_photo_title: 'Product&nbsp;Photography',
    srv_photo_desc: 'Capturing products, events, and brand spaces — high-quality post-processing for promotional&nbsp;use.',
    srv_uiux_title: 'UI/UX&nbsp;Design',
    srv_uiux_desc: 'Designing user interfaces & experiences for landing pages and websites — ensuring modern aesthetics and&nbsp;user-friendliness.',
    srv_idea_title: 'Creative&nbsp;Ideation',
    srv_idea_desc: 'Proposing and developing creative concepts, visual ideas, and content direction prior to&nbsp;production.',
    exp_eyebrow: 'Experience',
    exp_title: 'A 7+ year journey in the creative&nbsp;industry.',
    exp_desc: 'From printing, training, freelance, to technology brands —<br>each environment brings a new perspective on media&nbsp;and&nbsp;creativity.',
    exp_v2h_role: 'Media&nbsp;Specialist',
    exp_v2h_time: '2025 –&nbsp;Present',
    exp_v2h_desc: 'Filming and editing video reviews for audio & tech gear (JBL, Bose, Sony, Marshall). Managing YouTube channels, designing thumbnails, and optimizing&nbsp;SEO.',
    exp_v2h_btn: 'Visit Vua2Hand&nbsp;↗',
    exp_mygear_role: 'Media&nbsp;Specialist',
    exp_mygear_desc: 'Designing landing page & website UI/UX. Producing videos, designing banners/posters, and shooting product photography. Contributing visual ideas with the creative&nbsp;team.',
    exp_mygear_btn: 'Visit MyGear&nbsp;↗',
    exp_vie_role: 'Freelance Video&nbsp;Editor',
    exp_vie_desc: 'Professional post-production: processing raw files, editing, color grading, and audio syncing. Consulting visual solutions directly with&nbsp;clients.',
    exp_vie_btn: 'Visit Vie Channel&nbsp;↗',
    exp_topskills_role: 'Media&nbsp;Specialist',
    exp_topskills_desc: 'Producing & editing training videos. Designing brand identity assets (banners, posters). Collaborating to develop creative ideas for&nbsp;projects.',
    exp_topskills_btn: 'Visit TopSkills&nbsp;↗',
    exp_tgia_role: 'Media&nbsp;Specialist',
    exp_tgia_desc: 'Designing and processing print files. Supporting media content creation, basic videography, and product photography for company&nbsp;campaigns.',
    exp_tgia_btn: 'Visit Thế Giới In Ấn&nbsp;↗',
    port_eyebrow: 'Portfolio',
    port_title: 'Featured&nbsp;Work',
    port_desc: 'A compilation of video productions and creative content from YouTube channel @LongLeo287 and&nbsp;real-world&nbsp;projects.',
    contact_eyebrow: 'Contact',
    contact_title: 'Thank you for taking the time to&nbsp;visit.',
    contact_desc: 'Need someone for video editing, design, motion graphics, or UI/UX&nbsp;optimization?&nbsp;Let\'s get in touch to discuss your&nbsp;project.',
    contact_email_btn: 'Email Me&nbsp;✉',
    contact_phone_btn: 'Call Now&nbsp;☎',
    contact_addr_label: 'Address',
    contact_addr_val: 'Tan Phu, Ho Chi Minh&nbsp;City',
    footer_copy: 'Ha Dinh Long © 2026 | All Rights&nbsp;Reserved.',
    footer_sub: 'Video Editor&nbsp;Portfolio',
    modal_view_link: 'View Project&nbsp;↗',
    lang_label: 'Language',
    theme_aria: 'Toggle Light/Dark&nbsp;Mode',
    filter_all: 'Featured',
    filter_vid: 'Video&nbsp;Production',
    filter_des: 'Design',
    filter_photo: 'Photography',
    filter_thumb: 'YouTube&nbsp;Thumbnail',
    categories: {
      video: 'Video&nbsp;Production',
      design: 'Design',
      photography: 'Photography'
    }
  }
};

function updateStaticTranslations() {
  // FIX: Cancel any running pill typing animation first to prevent text duplication
  if (window._pillTypingInterval) {
    clearInterval(window._pillTypingInterval);
    window._pillTypingInterval = null;
  }

  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    if (translations[currentLang] && translations[currentLang][key]) {
      // FIX: Skip hero_pill — handled by typing animation below
      if (key === 'hero_pill') return;
      el.innerHTML = translations[currentLang][key];
    }
  });

  // Restart pill typing animation with correct translated text
  const pillText = translations[currentLang] && translations[currentLang]['hero_pill'];
  if (pillText && typeof window.startPillTyping === 'function') {
    window.startPillTyping(pillText);
  }

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
      formNote.textContent = "Nhập thông tin và nhấn Gửi đi để gửi email trực&nbsp;tiếp cho mình.";
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
    
    const tagText = p.category === 'Design' ? (currentLang === 'vi' ? 'thiết&nbsp;kế' : 'Design') : 
                    p.category === 'Photography' ? (currentLang === 'vi' ? 'chụp&nbsp;ảnh' : 'Photography') : p.category;
                    
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
        role: 'Vai&nbsp;trò',
        concept: 'ý&nbsp;tưởng &&nbsp;Concept',
        challenge: 'Thách thức&nbsp;sản&nbsp;xuất',
        solution: 'giải&nbsp;pháp thực&nbsp;hiện'
      },
      en: {
        role: 'Role',
        concept: 'Concept &&nbsp;Idea',
        challenge: 'Production&nbsp;Challenge',
        solution: 'Implemented&nbsp;Solution'
      }
    };
    const h = headings[currentLang];
    
    elements.modalBody.innerHTML = `
      <div class="cs-section" style="margin-bottom:1.25rem;">
        <h4 style="font-family:'Space&nbsp;Grotesk',sans-serif;color:var(--text-light);font-size:1.05rem;margin-bottom:0.25rem;">✦ ${h.role}</h4>
        <p style="margin:0;font-size:0.95rem;">${cs.role}</p>
      </div>
      <div class="cs-section" style="margin-bottom:1.25rem;">
        <h4 style="font-family:'Space&nbsp;Grotesk',sans-serif;color:var(--text-light);font-size:1.05rem;margin-bottom:0.25rem;">✦ ${h.concept}</h4>
        <p style="margin:0;font-size:0.95rem;">${cs.concept}</p>
      </div>
      <div class="cs-section" style="margin-bottom:1.25rem;">
        <h4 style="font-family:'Space&nbsp;Grotesk',sans-serif;color:var(--text-light);font-size:1.05rem;margin-bottom:0.25rem;">✦ ${h.challenge}</h4>
        <p style="margin:0;font-size:0.95rem;">${cs.challenge}</p>
      </div>
      <div class="cs-section" style="margin-bottom:1.25rem;">
        <h4 style="font-family:'Space&nbsp;Grotesk',sans-serif;color:var(--text-light);font-size:1.05rem;margin-bottom:0.25rem;">✦ ${h.solution}</h4>
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
  
  const title = typeof project.title === 'object' ? project.title[currentLang] : (project.title || "sản&nbsp;phẩm");
  
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
        <div class="showcase-img-wrap">
          <div class="showcase-bg-blur" style="background-image: url('${videoThumb}');"></div>
          <div class="yt-facade" style="background-image: url('${videoThumb}');" aria-label="Phát video: ${videoTitle}">
            <div class="yt-play-btn" aria-hidden="true">
              <svg viewBox="0 0 24 24" width="24" height="24"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>
            </div>
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
          <div class="showcase-bg-blur" style="background-image: url('${imgProj.imgSrc.replace(/'/g, "%27")}');"></div>
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

// --- Anti-Theft / Portfolio Lock ---
document.addEventListener('contextmenu', e => e.preventDefault());
document.addEventListener('copy', e => e.preventDefault());
document.addEventListener('cut', e => e.preventDefault());
document.addEventListener('paste', e => e.preventDefault());
document.addEventListener('selectstart', e => e.preventDefault());
document.addEventListener('dragstart', e => e.preventDefault());

document.addEventListener('keydown', e => {
  if (e.key === 'F12') {
    e.preventDefault();
  }
  if (e.ctrlKey && e.shiftKey && ['I', 'i', 'J', 'j', 'C', 'c'].includes(e.key)) {
    e.preventDefault();
  }
  if (e.ctrlKey && ['U', 'u', 'S', 's', 'P', 'p', 'C', 'c', 'A', 'a'].includes(e.key)) {
    e.preventDefault();
  }
});
