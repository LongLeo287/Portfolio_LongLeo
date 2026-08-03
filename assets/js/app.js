// ==========================================================================
// LongLeo Portfolio — Dynamic App Engine (Phase 1 Fixes & Phase 2 Integration)
// ==========================================================================

let projectsData = [];

// ?lang=en wins over the stored preference so an English link is shareable.
const SUPPORTED_LANGS = ['vi', 'en'];
function resolveInitialLang() {
  const fromUrl = new URLSearchParams(window.location.search).get('lang');
  if (fromUrl && SUPPORTED_LANGS.includes(fromUrl)) return fromUrl;
  const stored = localStorage.getItem('portfolio_lang');
  if (stored && SUPPORTED_LANGS.includes(stored)) return stored;
  return 'vi';
}
let currentLang = resolveInitialLang();

// main.js needs the live value, and ?lang= means localStorage is no longer
// the single source of truth.
window.portfolioLang = () => currentLang;

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
    closeModalBtn: document.getElementById('closeModalBtn'),
  modalBackdrop: document.getElementById('modalBackdrop')
};

// ==========================================
// Init & Fetch
// ==========================================
async function initApp() {
  initLangToggle();
  
  try {
    const res = await fetch('assets/data/projects.json?v=1.17');
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
function setLangButtonState() {
  elements.langBtns.forEach(b => {
    const isActive = b.dataset.lang === currentLang;
    b.classList.toggle('active', isActive);
    b.setAttribute('aria-pressed', String(isActive));
  });
}

function initLangToggle() {
  setLangButtonState();

  elements.langBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const selectedBtn = e.target.closest('.lang-btn');
      if (!selectedBtn) return;

      currentLang = selectedBtn.dataset.lang;
      setLangButtonState();
      localStorage.setItem('portfolio_lang', currentLang);

      // Keep the URL shareable without adding a history entry per toggle.
      const url = new URL(window.location.href);
      url.searchParams.set('lang', currentLang);
      window.history.replaceState({}, '', url);

      const cvIframe = document.querySelector("#cvModal iframe");
      if (cvIframe && cvIframe.contentWindow) {
        cvIframe.contentWindow.postMessage({ type: "LANG_TOGGLE", lang: currentLang }, window.location.origin);
      }

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
    hero_pill: '✦ Technical Video Editor • Motion Graphic • UI/UX',
    hero_title: 'Hà Đình <span class="gradient-text">Long</span>',
    hero_desc: 'Biến ý tưởng thành hình ảnh sống động — từ quay dựng video, motion graphic, thiết kế đồ họa đến tối ưu UI/UX.<br>Hơn 5 năm kinh nghiệm tạo ra các sản phẩm truyền thông chất lượng cao.',
    hero_btn1: 'Xem portfolio ↗',
    hero_btn_cv: 'Xem CV 📄',
    hero_btn2: 'Liên hệ hợp tác ✉',
    stat_exp: 'Năm kinh nghiệm',
    stat_proj: 'Công ty & dự án',
    stat_start: 'Bắt đầu hành trình',
    partners_title: 'ĐỐI TÁC HỢP TÁC',
    available_for: 'Sẵn sàng hợp tác',
    about_eyebrow: 'Một chút về mình',
    about_title: 'Từ Arena Multimedia đến hành trình sáng tạo hình ảnh chuyên nghiệp.',
    about_p1: 'Chào bạn, mình là <strong>Hà Đình Long</strong> — hay còn được biết đến với tên <strong>Long Leo</strong>. Tốt nghiệp ngành Multimedia tại Arena Multimedia, mình bắt đầu hành trình sáng tạo từ năm 2019.',
    about_p2: 'Với hơn 5 năm kinh nghiệm trong lĩnh vực Sản xuất video, thiết kế đồ họa và truyền thông đa phương tiện, mình đã trải qua nhiều môi trường làm việc từ agency, in-house đến freelance — mỗi chặng đường đều giúp mình tích lũy thêm những góc nhìn và kỹ năng mới.',
    about_p3_short: '<strong>Mục tiêu ngắn hạn:</strong> Tối ưu hóa kỹ năng sản xuất hình ảnh/video chuyên sâu và ứng dụng tư duy sáng tạo để tạo ra các sản phẩm truyền thông chất lượng cao, thúc đẩy hiệu suất các chiến dịch marketing.',
    about_p3_long: '<strong>Mục tiêu dài hạn:</strong> Trở thành Chuyên gia Hậu kỳ (Post-Production Specialist), không ngừng nâng cấp bộ kỹ năng chuyên môn và ứng dụng các công cụ công nghệ mới (AI, Automation) để tối ưu hóa tốc độ dựng phim và nâng cao chất lượng đầu ra.',
    about_skill1: '<strong>Tư duy Thẩm mỹ:</strong> Cân bằng giữa yếu tố nghệ thuật và mục tiêu truyền thông thực tế.',
    about_skill2: '<strong>Quy trình Tối ưu:</strong> Ứng dụng công nghệ & AI để tối ưu hóa thời gian sản xuất mà vẫn giữ chất lượng cao.',
    about_skill3: '<strong>Thích ứng Nhanh:</strong> Khả năng đảm nhiệm linh hoạt nhiều vai trò từ Quay, Dựng, đến Thiết kế và UI/UX.',
    tools_title: 'Công cụ & Trợ lý AI sáng tạo',
    tools_group1_title: 'Phần mềm sáng tạo chuyên nghiệp',
    tool_prem: 'Dựng phim & Màu sắc',
    tool_ae: 'Motion & hậu kỳ kỹ xảo',
    tool_ps: 'Chỉnh ảnh & Cắt ghép',
    tool_ai: 'Thiết kế Vector & ấn phẩm',
    tool_lr: 'Blend màu & hậu kỳ ảnh',
    tool_figma: 'Thiết kế giao diện UI/UX',
    tool_capcut: 'Dựng video nhanh & tiện lợi',
    tool_canva: 'Thiết kế đồ họa trực tuyến',
    tools_group2_title: 'Trợ lý AI & tối ưu hiệu suất',
    tool_gemini: 'Lên ý tưởng & Lịch trình',
    tool_ai_studio: 'Thử nghiệm Prompt & API',
    tool_antigravity: 'Tự động hóa & Coding',
    tool_claude: 'Phân tích & Viết nội dung',
    tool_codex: 'Hỗ trợ Kỹ thuật & Code',
    services_eyebrow: 'Dịch vụ',
    services_title: 'Giải pháp hình ảnh & truyền thông toàn diện.',
    services_desc: 'Tập trung vào chất lượng hình ảnh, nhịp kể và tính ứng dụng thực tế <br>— từ video, thiết kế đến UI/UX cho các chiến dịch truyền thông.',
    srv_vid_title: 'Quay & Dựng Video',
    srv_vid_desc: 'Sản xuất video chuyên nghiệp: TVC, quảng cáo, unboxing, review sản phẩm, video sự kiện và các định dạng social media.',
    srv_motion_title: 'Motion Graphic',
    srv_motion_desc: 'Tạo hiệu ứng chuyển động bắt mắt, title animation, infographic động và các visual effects chuyên nghiệp bằng After Effects.',
    srv_design_title: 'Thiết kế đồ họa',
    srv_design_desc: 'Thiết kế banner, poster, thumbnail, key visual và ấn phẩm truyền thông phục vụ các chiến dịch marketing trên mọi nền tảng.',
    srv_photo_title: 'Chụp ảnh sản phẩm',
    srv_photo_desc: 'Chụp ảnh sản phẩm, sự kiện, không gian thương hiệu — chỉnh sửa hậu kỳ chất lượng cao phục vụ quảng bá.',
    srv_uiux_title: 'Thiết kế UI/UX',
    srv_uiux_desc: 'Thiết kế giao diện & trải nghiệm người dùng cho landing page, website — đảm bảo tính thẩm mỹ hiện đại và thân thiện với người dùng.',
    srv_idea_title: 'Sáng tạo ý tưởng',
    srv_idea_desc: 'Đề xuất và phát triển các concept sáng tạo, lên ý tưởng hình ảnh và định hướng nội dung trước khi sản xuất.',
    exp_eyebrow: 'Kinh nghiệm',
    exp_title: 'Hành trình 5+ năm trong ngành sáng tạo.',
    exp_desc: 'Từ in ấn, đào tạo, freelance, đến thương hiệu công nghệ —<br>mỗi môi trường đều mang đến một góc nhìn mới về truyền thông và sáng tạo.',
    exp_v2h_role: 'Nhân viên Media',
    exp_v2h_time: '2025 – nay',
    exp_v2h_desc: 'Quay dựng video review thiết bị âm thanh & công nghệ (JBL, Bose, Sony, Marshall). Quản lý kênh YouTube, thiết kế thumbnail, tối ưu SEO.',
    exp_v2h_btn: 'Ghé thăm Vua2Hand ↗',
    exp_mygear_role: 'Nhân viên Media',
    exp_mygear_desc: 'Thiết kế UI/UX landing page & website. Sản xuất video, thiết kế banner/poster, Chụp ảnh sản phẩm. Đóng góp xây dựng ý tưởng hình ảnh cùng đội ngũ sáng tạo.',
    exp_mygear_btn: 'Ghé thăm MyGear ↗',
    exp_vie_role: 'Editor Tự do',
    exp_vie_desc: 'Hậu kỳ chuyên nghiệp: xử lý file thô, cắt ghép, color grading, đồng bộ âm thanh. Tư vấn giải pháp hình ảnh trực tiếp với khách hàng.',
    exp_vie_btn: 'Ghé thăm Vie Channel ↗',
    exp_topskills_role: 'Nhân viên Media',
    exp_topskills_desc: 'Sản xuất & hậu kỳ video đào tạo. Thiết kế ấn phẩm thương hiệu (banner, poster). Phối hợp phát triển các ý tưởng sáng tạo cho dự án.',
    exp_topskills_btn: 'Ghé thăm TopSkills ↗',
    exp_tgia_role: 'Nhân viên Media',
    exp_tgia_desc: 'Thiết kế và xử lý file in ấn. Hỗ trợ sản xuất nội dung truyền thông, quay dựng video cơ bản và Chụp ảnh sản phẩm cho các chiến dịch của công ty.',
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
    skip_link: 'Bỏ qua tới nội dung chính',
    form_label_name: 'Tên của bạn',
    form_label_email: 'Email liên hệ',
    form_label_message: 'Nội dung cần trao đổi',
    form_submit: 'Gửi đi',
    form_hint: 'Nhập thông tin và nhấn Gửi đi để gửi email trực tiếp cho mình.',
    form_ph_name: 'Nguyễn Văn A',
    form_ph_email: 'ban@example.com',
    form_ph_message: 'Mình đang cần dựng một video review dài 3 phút…',
    band_1: ['QUAY DỰNG', 'MOTION GRAPHIC', 'COLOR GRADING', 'KEY VISUAL', 'THUMBNAIL', 'UI/UX'],
    band_2: ['HẬU KỲ', 'TVC', 'SOCIAL VIDEO', 'CHỤP SẢN PHẨM', 'STORYBOARD', 'BRANDING'],
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
    nav_collab: 'Let\'s collaborate',
    hero_pill: '✦ Technical Video Editor • Motion Graphic • UI/UX',
    hero_title: 'Ha Dinh <span class="gradient-text">Long</span>',
    hero_desc: 'Turning ideas into vivid visuals — from video production, motion graphics, graphic design to UI/UX optimization.<br>Over 5 years of experience in creating high-quality media products.',
    hero_btn1: 'View Portfolio ↗',
    hero_btn_cv: 'View CV 📄',
    hero_btn2: 'Let\'s Talk ✉',
    stat_exp: 'years of experience',
    stat_proj: 'companies & projects',
    stat_start: 'started journey',
    partners_title: 'TRUSTED BY',
    available_for: 'Available for',
    about_eyebrow: 'A little about me',
    about_title: 'From Arena Multimedia to a professional visual creation journey.',
    about_p1: 'Hello, I\'m <strong>Ha Dinh Long</strong> — also known as <strong>Long Leo</strong>. Graduated in Multimedia from Arena Multimedia, I started my creative journey in 2019.',
    about_p2: 'With over 5 years of experience in video production, graphic design, and multimedia communications, I have worked across various environments from agencies, in-house teams to freelance — each stage helping me gain new perspectives and skills.',
    about_p3_short: '<strong>Short-term Goal:</strong> Optimize in-depth image/video production skills and apply creative thinking to create high-quality media products, driving the performance of marketing campaigns.',
    about_p3_long: '<strong>Long-term Goal:</strong> Become a Post-Production Specialist, continuously upgrading specialized skill sets and applying new technological tools (AI, Automation) to optimize editing speed and enhance output quality.',
    about_skill1: '<strong>Aesthetic Sense:</strong> Balancing artistic elements with practical communication goals.',
    about_skill2: '<strong>Optimized Workflow:</strong> Applying technology & AI to speed up production while maintaining high quality.',
    about_skill3: '<strong>Fast Adaptation:</strong> Ability to flexibly handle multiple roles from Filming, Editing, to 2D/UI Design.',
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
    exp_title: 'A 5+ year journey in the creative industry.',
    exp_desc: 'From printing, training, freelance, to technology brands —<br>each environment brings a new perspective on media and creativity.',
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
    skip_link: 'Skip to main content',
    form_label_name: 'Your name',
    form_label_email: 'Email address',
    form_label_message: 'What would you like to discuss?',
    form_submit: 'Send message',
    form_hint: 'Fill in your details and hit Send — it goes straight to my inbox.',
    form_ph_name: 'Jane Doe',
    form_ph_email: 'you@example.com',
    form_ph_message: 'I need a 3-minute product review edited…',
    band_1: ['VIDEO EDITING', 'MOTION GRAPHIC', 'COLOR GRADING', 'KEY VISUAL', 'THUMBNAIL', 'UI/UX'],
    band_2: ['POST-PRODUCTION', 'TVC', 'SOCIAL VIDEO', 'PRODUCT PHOTOGRAPHY', 'STORYBOARD', 'BRANDING'],
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
  // Cancel any running pill typing animation first to prevent text duplication
  if (window._pillTypingInterval) {
    clearInterval(window._pillTypingInterval);
    window._pillTypingInterval = null;
  }

  // Screen readers and search engines both need the real language of the page.
  document.documentElement.lang = currentLang;

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
  
  // Labels, button and hint carry data-i18n and were handled above; only the
  // placeholders need setting by hand.
  const dict = translations[currentLang] || translations.vi;
  const setPlaceholder = (selector, key) => {
    const el = document.querySelector(selector);
    if (el && dict[key]) el.placeholder = dict[key];
  };
  setPlaceholder('#cf-name', 'form_ph_name');
  setPlaceholder('#cf-email', 'form_ph_email');
  setPlaceholder('#cf-message', 'form_ph_message');

  // Kinetic band: the visible row and its duplicate must stay identical or
  // the -50% loop develops a visible seam, so both are rebuilt together.
  document.querySelectorAll('[data-i18n-band]').forEach(row => {
    const words = dict[`band_${row.dataset.i18nBand}`];
    if (!Array.isArray(words)) return;

    const track = row.querySelector('.kinetic-track');
    const dup = row.querySelector('.kinetic-dup');
    if (!track || !dup) return;

    const build = (parent) => {
      parent.textContent = '';
      words.forEach(word => {
        const span = document.createElement('span');
        span.textContent = word;
        const sep = document.createElement('i');
        sep.setAttribute('aria-hidden', 'true');
        sep.textContent = '✦';
        parent.append(span, sep);
      });
    };

    build(dup);
    // Rebuilding `track` would wipe `dup`, which lives inside it — replace
    // only the nodes before it.
    while (track.firstChild && track.firstChild !== dup) track.removeChild(track.firstChild);
    const head = document.createDocumentFragment();
    words.forEach(word => {
      const span = document.createElement('span');
      span.textContent = word;
      const sep = document.createElement('i');
      sep.setAttribute('aria-hidden', 'true');
      sep.textContent = '✦';
      head.append(span, sep);
    });
    track.insertBefore(head, dup);
  });

  // Re-split the headings the pass above just flattened, otherwise the word
  // reveal animation silently stops existing after the first translation.
  if (typeof window.refreshTextReveal === 'function') {
    window.refreshTextReveal();
  }
}

// ==========================================
// Responsive images
// scripts/generate-image-sizes.py writes a -480.webp and a -960.webp next to
// every image referenced by projects.json. Both always exist (small sources
// are re-encoded at native width rather than skipped), so every candidate in
// the srcset resolves.
// ==========================================
const IMAGE_WIDTHS = [480, 960];

function buildSrcset(src) {
  if (!src || /^https?:/i.test(src)) return null;
  const stem = src.replace(/\.(webp|jpe?g|png)$/i, '');
  if (stem === src) return null;
  return IMAGE_WIDTHS.map(w => `${stem}-${w}.webp ${w}w`).join(', ');
}

function applyResponsiveSrc(img, src, sizes) {
  const srcset = buildSrcset(src);
  if (!srcset) return;
  img.srcset = srcset;
  img.sizes = sizes;
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
  
  const fragment = document.createDocumentFragment();

  displayList.forEach(p => {
    const card = document.createElement('a');
    card.className = `portfolio-card fade-up${p.category === 'Photography' ? ' photo-only' : ''}`;
    card.dataset.category = p.category;
    card.dataset.id = p.id;
    // Keep a real href so the card is crawlable and middle-click still works,
    // but the primary action is the in-page dialog, not a new tab.
    card.href = p.href || p.imgSrc;
    card.rel = 'noopener';
    card.setAttribute('aria-haspopup', 'dialog');

    const title = typeof p.title === 'object' ? p.title[currentLang] : p.title;
    const client = typeof p.client === 'object' ? p.client[currentLang] : p.client;

    const tagText =
      p.category === 'Design' ? (currentLang === 'vi' ? 'Thiết kế' : 'Design') :
      p.category === 'Photography' ? (currentLang === 'vi' ? 'Chụp ảnh' : 'Photography') :
      p.category;

    const thumbDiv = document.createElement('div');
    thumbDiv.className = 'portfolio-thumb';

    const img = document.createElement('img');
    img.src = p.imgSrc;
    applyResponsiveSrc(img, p.imgSrc, '(max-width: 560px) 92vw, (max-width: 900px) 46vw, 300px');
    img.alt = p.alt || title || '';
    img.loading = 'lazy';
    img.decoding = 'async';

    const tag = document.createElement('span');
    tag.className = 'tag';
    tag.textContent = tagText;

    thumbDiv.append(img, tag);

    // Play affordance, but only where the card genuinely opens a video —
    // putting one on a poster or a photo would promise something the click
    // does not deliver.
    const opensVideo = p.category === 'Video' ||
      (p.category === 'Thumbnail' && typeof p.href === 'string' && p.href.includes('youtube.com'));

    if (opensVideo) {
      card.classList.add('has-video');
      const play = document.createElement('span');
      play.className = 'thumb-play';
      play.setAttribute('aria-hidden', 'true');
      play.innerHTML = '<svg viewBox="0 0 24 24" width="22" height="22"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>';
      const scrub = document.createElement('span');
      scrub.className = 'thumb-scrub';
      scrub.setAttribute('aria-hidden', 'true');
      thumbDiv.append(play, scrub);
    }

    card.appendChild(thumbDiv);

    if ((title || client) && p.category !== 'Photography') {
      const bodyDiv = document.createElement('div');
      bodyDiv.className = 'portfolio-body';

      const clientEl = document.createElement('p');
      clientEl.className = 'client';
      clientEl.textContent = client || '';

      const titleEl = document.createElement('h3');
      titleEl.textContent = title || '';

      bodyDiv.append(clientEl, titleEl);
      card.appendChild(bodyDiv);
    } else if (title) {
      // Photography cards are image-only by design — the title still has to
      // reach a screen reader somehow.
      card.setAttribute('aria-label', title);
    }

    card.addEventListener('click', (e) => handleCardClick(e, p));

    fragment.appendChild(card);
    displayedCards.push(card);
  });

  elements.grid.appendChild(fragment);
  elements.grid.setAttribute('aria-busy', 'false');
  // Section offsets shift when the grid height changes, so the scroll-spy
  // has to be told or the active nav link points at the wrong section.
  if (typeof window.recacheSectionOffsets === 'function') {
    window.recacheSectionOffsets();
  }

  const reveal = () => {
    displayedCards.forEach((card, idx) => {
      // Restraint budget: stagger tops out so the ninth card is not 400ms late.
      card.style.transitionDelay = `${Math.min(idx * 40, 280)}ms`;
      card.classList.add('show');
    });
    applyCardEffects(displayedCards);
  };

  // Cards start at opacity 0, so their visibility must never depend on a frame
  // callback alone — rAF does not fire in a background tab.
  if (document.visibilityState === 'hidden') {
    reveal();
  } else {
    requestAnimationFrame(reveal);
  }
}

// ==========================================
// Card tilt, parallax and pointer spotlight
// One rAF-scheduled write per card per frame instead of a style write on
// every mousemove event, and bound only to the cards just rendered.
// ==========================================
function applyCardEffects(cards) {
  const motion = window.portfolioMotion;
  if (!motion || !motion.finePointer()) return;

  cards.forEach((card, i) => {
    const thumb = card.querySelector('.portfolio-thumb img');
    const key = `card-${i}`;

    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const px = e.clientX - rect.left;
      const py = e.clientY - rect.top;
      const x = px / rect.width - 0.5;
      const y = py / rect.height - 0.5;

      motion.schedule(key, () => {
        card.style.setProperty('--mx', `${px}px`);
        card.style.setProperty('--my', `${py}px`);
        card.style.transform =
          `perspective(700px) rotateX(${-y * 5}deg) rotateY(${x * 5}deg) translateY(-6px)`;
        if (thumb) thumb.style.transform = `scale(1.08) translateY(${y * -8}px)`;
      });
    }, { passive: true });

    card.addEventListener('mouseleave', () => {
      motion.schedule(key, () => {
        card.style.transform = '';
        if (thumb) thumb.style.transform = '';
      });
    }, { passive: true });
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

      elements.filterBtns.forEach(b => {
        const isActive = b === clickedBtn;
        b.classList.toggle('active', isActive);
        b.setAttribute('aria-pressed', String(isActive));
      });

      const swap = () => renderPortfolio(clickedBtn.dataset.filter);

      // Cross-fade the grid instead of swapping it instantly. Falls straight
      // through to a plain re-render where View Transitions aren't supported
      // or where the visitor has asked for less motion.
      if (document.startViewTransition) {
        document.startViewTransition(swap);
      } else {
        swap();
      }
    });
  });
}

// ==========================================
// Click Actions: Modal vs Lightbox
// ==========================================
function handleCardClick(e, project) {
  e.preventDefault();
  openCaseStudyModal(project);
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
// Modal Manager — focus trap, Escape, focus restore, scroll lock
// ==========================================
const ModalManager = (() => {
  const FOCUSABLE = [
    'a[href]', 'button:not([disabled])', 'input:not([disabled])',
    'textarea:not([disabled])', 'select:not([disabled])', 'iframe',
    '[tabindex]:not([tabindex="-1"])'
  ].join(',');

  let openEl = null;
  let lastFocused = null;
  let onCloseHook = null;

  const visibleFocusable = (root) =>
    Array.from(root.querySelectorAll(FOCUSABLE))
      .filter(el => el.offsetWidth > 0 || el.offsetHeight > 0 || el === document.activeElement);

  function handleKeydown(e) {
    if (e.key === 'Escape') {
      e.preventDefault();
      close();
      return;
    }
    if (e.key !== 'Tab' || !openEl) return;

    const items = visibleFocusable(openEl);
    if (!items.length) {
      e.preventDefault();
      return;
    }
    const first = items[0];
    const last = items[items.length - 1];

    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    } else if (!openEl.contains(document.activeElement)) {
      e.preventDefault();
      first.focus();
    }
  }

  function open(el, options = {}) {
    if (!el) return;
    if (openEl) close();

    lastFocused = document.activeElement;
    openEl = el;
    onCloseHook = options.onClose || null;

    el.removeAttribute('aria-hidden');
    document.body.classList.add('modal-open');
    document.addEventListener('keydown', handleKeydown, true);
    if (window.lenis) window.lenis.stop();

    // Try synchronously first — a rAF-only approach leaves focus outside the
    // dialog in a backgrounded tab. The retries cover the modals that fade in
    // from visibility:hidden, where the element is not yet focusable on the
    // very first attempt.
    const target = options.initialFocus || visibleFocusable(el)[0] || el;
    if (target === el && !el.hasAttribute('tabindex')) el.setAttribute('tabindex', '-1');

    const tryFocus = () => {
      if (openEl !== el || el.contains(document.activeElement)) return true;
      target.focus({ preventScroll: true });
      return el.contains(document.activeElement);
    };

    if (!tryFocus()) {
      requestAnimationFrame(() => { if (!tryFocus()) setTimeout(tryFocus, 80); });
      setTimeout(tryFocus, 350); // after the fade-in transition settles
    }
  }

  function close() {
    if (!openEl) return;
    const el = openEl;
    const hook = onCloseHook;

    openEl = null;
    onCloseHook = null;

    document.removeEventListener('keydown', handleKeydown, true);
    document.body.classList.remove('modal-open');
    el.setAttribute('aria-hidden', 'true');
    if (typeof hook === 'function') hook();
    if (window.lenis) window.lenis.start();

    if (lastFocused && document.contains(lastFocused)) {
      lastFocused.focus({ preventScroll: true });
    }
    lastFocused = null;
  }

  return { open, close, isOpen: () => openEl !== null, current: () => openEl };
})();

window.ModalManager = ModalManager;

// ==========================================
// Case Study Modal
// ==========================================
function openCaseStudyModal(project) {
  const title = typeof project.title === 'object' ? project.title[currentLang] : project.title;
  const client = typeof project.client === 'object' ? project.client[currentLang] : project.client;
  
  elements.modalTitle.textContent = title;
  elements.modalClient.textContent = client;
    
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
    
    let bodyHtml = '';
    const addSection = (title, content) => {
      if (content && content.trim() !== '') {
        bodyHtml += `
          <div class="cs-section" style="margin-bottom:1.25rem;">
            <h4>✦ ${title}</h4>
            <p>${content}</p>
          </div>
        `;
      }
    };
    
    addSection(h.role, cs.role);
    addSection(h.concept, cs.concept);
    addSection(h.challenge, cs.challenge);
    addSection(h.solution, cs.solution);
    
    elements.modalBody.innerHTML = bodyHtml;
  } else {
    elements.modalBody.innerHTML = '';
  }
  
  // Media — Video: embed YouTube | Thumbnail with YT link: embed | Others: image
  elements.modalMedia.innerHTML = '';
  const isYouTubeHref = project.href && project.href.includes('youtube.com');

  if (project.category === 'Video' || (project.category === 'Thumbnail' && isYouTubeHref)) {
    const embedUrl = getYouTubeEmbedUrl(project.href || project.imgSrc);
    if (embedUrl) {
      elements.modalMedia.innerHTML = `<iframe src="${embedUrl}" allow="autoplay; encrypted-media" allowfullscreen></iframe>`;
    }
  } else {
    const blurSrc = project.imgSrc.replace(/\.(webp|jpe?g|png)$/i, '-480.webp').replace(/'/g, "%27");
    const ytLabel = currentLang === 'en' ? '▶ Watch on YouTube' : '▶ Xem trên YouTube';
    const ytBtn = isYouTubeHref
      ? `<a href="${project.href}" target="_blank" rel="noopener" class="modal-yt-btn">${ytLabel}</a>`
      : '';
    elements.modalMedia.innerHTML = `
      <div class="modal-media-blur" style="background-image: url('${blurSrc}')"></div>
      <img src="${project.imgSrc}" alt="${title}" decoding="async" style="position:relative; z-index:2;" />
      ${ytBtn}
    `;
  }

  const layout = document.querySelector('.modal-layout');
  // Auto-hide info panel for image-only cards (Thumbnail/Photography) that have no case study
  if (layout) {
    const hasInfo = project.caseStudy && (project.caseStudy.role || project.caseStudy.concept);
    if (!hasInfo) {
      layout.classList.add('info-hidden');
    } else {
      layout.classList.remove('info-hidden');
    }
  }
  elements.modal.classList.add('active');
  ModalManager.open(elements.modal, {
    initialFocus: elements.closeModalBtn,
    onClose: () => {
      elements.modal.classList.remove('active');
      // Clearing the media node is what actually stops a playing YouTube embed.
      if (elements.modalMedia) elements.modalMedia.innerHTML = '';
    }
  });
}

function closeCaseStudyModal() {
  ModalManager.close();
}

elements.closeModalBtn?.addEventListener('click', closeCaseStudyModal);
elements.modalBackdrop?.addEventListener('click', closeCaseStudyModal);

const toggleInfoBtn = document.getElementById('toggleInfoBtn');
if (toggleInfoBtn) {
  toggleInfoBtn.addEventListener('click', () => {
    const layout = document.querySelector('.modal-layout');
    if (layout) layout.classList.toggle('info-hidden');
  });
}

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
  
  const title = typeof project.title === 'object' ? project.title[currentLang] : (project.title || "sản phẩm");
  
  if (project.category === "Video") {
    const embedUrl = getYouTubeEmbedUrl(project.href || project.imgSrc);
    if (!embedUrl || !lightboxVideoWrapper || !lightboxVideo) {
      window.open(project.href || project.imgSrc, '_blank', 'noopener');
      return;
    }
    lightboxLoader.style.display = "none";
    lightboxVideo.src = embedUrl;
    lightboxVideoWrapper.style.display = "block";
    lightboxModal.classList.add("show");
  } else {
    lightboxImage.src = project.imgSrc;
    lightboxImage.alt = title;
    lightboxModal.classList.add("show");
  }

  ModalManager.open(lightboxModal, {
    initialFocus: lightboxModal.querySelector('.lightbox-close'),
    onClose: () => {
      lightboxModal.classList.remove("show");
      lightboxImage.src = "";
      if (lightboxVideo) lightboxVideo.src = "";
      if (lightboxVideoWrapper) lightboxVideoWrapper.style.display = "none";
    }
  });
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
          <div class="yt-facade" aria-label="Phát video: ${videoTitle}">
            <img src="${videoThumb}" alt="${videoTitle}"
                 style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover; z-index:0; border-radius:inherit;" 
                 onload="if(this.naturalWidth <= 120 && this.src.includes('maxresdefault')) { this.src = this.src.replace('maxresdefault', 'hqdefault'); this.parentElement.previousElementSibling.style.backgroundImage = 'url(' + this.src + ')'; }"
                 onerror="if(this.src.includes('maxresdefault')) { this.src = this.src.replace('maxresdefault', 'hqdefault'); this.parentElement.previousElementSibling.style.backgroundImage = 'url(' + this.src + ')'; }">
            <div class="yt-play-btn" style="position:relative; z-index:2;" aria-hidden="true">
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
    const srcset = buildSrcset(imgProj.imgSrc);
    const srcsetAttr = srcset
      ? ` srcset="${srcset}" sizes="(max-width: 1240px) 100vw, 1180px"`
      : '';
    // The blurred backdrop only ever renders behind a heavy blur, so point it
    // at the 480w file instead of re-requesting the full-size artwork.
    const blurSrc = (srcset ? imgProj.imgSrc.replace(/\.(webp|jpe?g|png)$/i, '-480.webp') : imgProj.imgSrc);
    slidesHtml += `
      <div class="showcase-slide ${isActive ? 'active' : ''}" data-type="image" data-src="${imgProj.imgSrc}">
        <div class="showcase-img-wrap">
          <div class="showcase-bg-blur" style="background-image: url('${blurSrc.replace(/'/g, "%27")}');"></div>
          <img src="${imgProj.imgSrc}"${srcsetAttr} alt="${title}" decoding="async" />
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
  
  // Video facade click to load iframe on demand.
  // Bound once: initShowcaseSlider() re-runs on every language switch, but
  // slidesContainer persists, so an unguarded listener stacked up one copy
  // per switch. Same guard the swipe handlers below already use.
  if (!slidesContainer.dataset.facadeBound) {
    slidesContainer.addEventListener('click', (e) => {
      const facade = e.target.closest('.yt-facade');
      if (!facade) return;

      const slide = facade.closest('.showcase-slide');
      const videoSrc = slide && slide.dataset.videoSrc;
      if (!videoSrc) return;

      const embedUrl = getYouTubeEmbedUrl(videoSrc);
      if (!embedUrl) return;

      const iframe = document.createElement('iframe');
      iframe.src = embedUrl;
      const heading = slide.querySelector('h3');
      iframe.title = heading ? heading.textContent : 'Video';
      iframe.setAttribute('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share');
      iframe.setAttribute('allowfullscreen', '');
      facade.replaceWith(iframe);
    });
    slidesContainer.dataset.facadeBound = 'true';
  }
  
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

// --- Image protection ---
// Deliberately narrow: only images are guarded. Blocking copy/paste/select or
// devtools shortcuts document-wide stopped visitors pasting their own email
// into the contact form and printing the CV, and none of it stops anyone who
// actually wants the files. Right-click + drag on <img> is the honest ceiling.
document.addEventListener('contextmenu', (e) => {
  if (e.target.tagName === 'IMG') e.preventDefault();
});
document.addEventListener('dragstart', (e) => {
  if (e.target.tagName === 'IMG') e.preventDefault();
});


// CV Modal Logic
document.addEventListener('DOMContentLoaded', () => {
  const openCvBtn = document.getElementById('openCvBtn');
  const cvModal = document.getElementById('cvModal');
  const closeCvBtn = document.getElementById('closeCvBtn');

  if (openCvBtn && cvModal && closeCvBtn) {
    const closeCv = () => ModalManager.close();

    openCvBtn.addEventListener('click', (e) => {
      e.preventDefault();
      cvModal.classList.add('active');
      ModalManager.open(cvModal, {
        initialFocus: closeCvBtn,
        onClose: () => cvModal.classList.remove('active')
      });
    });

    closeCvBtn.addEventListener('click', closeCv);

    cvModal.addEventListener('click', (e) => {
      if (e.target === cvModal) closeCv();
    });
  }
});

// ==========================================
// Copy email to clipboard
// ==========================================
window.copyEmail = async function (btn) {
  const email = 'Longdragon287@gmail.com';
  const isEn = currentLang === 'en';
  const originalText = btn.innerHTML;

  try {
    await navigator.clipboard.writeText(email);
    btn.innerHTML = isEn ? 'Email copied!' : 'Đã chép email!';
  } catch (err) {
    // Clipboard API needs a secure context and a permission the visitor may
    // have denied — fall back to the mail client rather than failing silently.
    window.location.href = `mailto:${email}`;
    btn.innerHTML = isEn ? 'Opening mail app…' : 'Đang mở ứng dụng mail…';
  }

  setTimeout(() => { btn.innerHTML = originalText; }, 2000);
};
