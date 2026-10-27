
let projectsData = [];
let projectsCatalogPromise = null;
let projectsCatalogLoaded = false;

const SUPPORTED_LANGS = ['vi', 'en'];
function resolveInitialLang() {
  const fromUrl = new URLSearchParams(window.location.search).get('lang');
  if (fromUrl && SUPPORTED_LANGS.includes(fromUrl)) return fromUrl;
  const stored = localStorage.getItem('portfolio_lang');
  if (stored && SUPPORTED_LANGS.includes(stored)) return stored;
  return 'vi';
}
let currentLang = resolveInitialLang();

window.portfolioLang = () => currentLang;

const elements = {
  grid: document.getElementById('portfolioGrid'),
  portfolioCarousel: document.querySelector('[data-portfolio-carousel]'),
  portfolioPrevBtn: document.getElementById('portfolioPrevBtn'),
  portfolioNextBtn: document.getElementById('portfolioNextBtn'),
  portfolioCarouselStatus: document.getElementById('portfolioCarouselStatus'),
  slides: document.getElementById('showcaseSlides'),
  filterBtns: document.querySelectorAll('.filter-btn[data-filter]'),
  langBtns: document.querySelectorAll('.lang-btn'),
  
  modal: document.getElementById('caseStudyModal'),
  modalMedia: document.getElementById('modalMedia'),
  modalTitle: document.getElementById('modalTitle'),
  modalClient: document.getElementById('modalClient'),
  modalTags: document.getElementById('modalTags'),
  modalBody: document.getElementById('modalBody'),
    closeModalBtn: document.getElementById('closeModalBtn'),
  modalBackdrop: document.getElementById('modalBackdrop')
};

let portfolioCarouselBound = false;
let portfolioPage = 0;
const PORTFOLIO_PAGE_SIZE = 6;

function updatePortfolioCarousel() {
  const { grid, portfolioCarousel, portfolioPrevBtn, portfolioNextBtn, portfolioCarouselStatus } = elements;
  if (!grid || !portfolioCarousel || !portfolioPrevBtn || !portfolioNextBtn) return;

  const cards = [...grid.querySelectorAll('.portfolio-card')];
  const pages = [...grid.querySelectorAll('.portfolio-page')];
  const total = cards.length;
  const pageCount = pages.length;
  portfolioPage = Math.max(0, Math.min(portfolioPage, pageCount - 1));

  pages.forEach((page, index) => {
    const isCurrent = index === portfolioPage;
    page.setAttribute('aria-hidden', String(!isCurrent));
    page.inert = !isCurrent;
    page.hidden = !isCurrent;
    page.classList.toggle('is-active', isCurrent);
  });

  portfolioPrevBtn.disabled = portfolioPage <= 0 || total === 0;
  portfolioNextBtn.disabled = pageCount === 0 || portfolioPage >= pageCount - 1;

  if (!portfolioCarouselStatus) return;
  if (total === 0) {
    portfolioCarouselStatus.textContent = currentLang === 'en' ? 'No products' : 'Chưa có sản phẩm';
    return;
  }

  const start = Math.min(total, portfolioPage * PORTFOLIO_PAGE_SIZE + 1);
  const end = Math.min(total, start + PORTFOLIO_PAGE_SIZE - 1);
  portfolioCarouselStatus.textContent = currentLang === 'en'
    ? `${start}–${end} of ${total}`
    : `${start}–${end} / ${total} sản phẩm`;

  const isEnglish = currentLang === 'en';
  portfolioCarousel.setAttribute('aria-label', isEnglish ? 'Portfolio products' : 'Các sản phẩm portfolio');
  portfolioPrevBtn.setAttribute('aria-label', isEnglish ? 'Previous products' : 'Sản phẩm trước');
  portfolioNextBtn.setAttribute('aria-label', isEnglish ? 'Next products' : 'Sản phẩm tiếp theo');
}

function initPortfolioCarousel() {
  const { grid, portfolioCarousel, portfolioPrevBtn, portfolioNextBtn } = elements;
  if (!grid || !portfolioCarousel || !portfolioPrevBtn || !portfolioNextBtn || portfolioCarouselBound) return;

  const movePage = (direction) => {
    const pageCount = grid.querySelectorAll('.portfolio-page').length;
    portfolioPage = Math.max(0, Math.min(portfolioPage + direction, pageCount - 1));
    updatePortfolioCarousel();
  };

  portfolioPrevBtn.addEventListener('click', () => movePage(-1));
  portfolioNextBtn.addEventListener('click', () => movePage(1));
  window.addEventListener('resize', updatePortfolioCarousel, { passive: true });
  portfolioCarouselBound = true;
  updatePortfolioCarousel();
}

function detectPillarboxedThumbnail(img) {
  if (!img?.naturalWidth || !img?.naturalHeight) return false;

  const canvas = document.createElement('canvas');
  canvas.width = 64;
  canvas.height = 36;
  const context = canvas.getContext('2d', { willReadFrequently: true });
  if (!context) return false;

  try {
    context.drawImage(img, 0, 0, canvas.width, canvas.height);
    const pixels = context.getImageData(0, 0, canvas.width, canvas.height).data;
    const columns = Array.from({ length: canvas.width }, (_, x) => {
      let luminance = 0;
      for (let y = 0; y < canvas.height; y += 1) {
        const offset = (y * canvas.width + x) * 4;
        luminance += (pixels[offset] * 0.2126) + (pixels[offset + 1] * 0.7152) + (pixels[offset + 2] * 0.0722);
      }
      return luminance / canvas.height;
    });

    const edgeLuminance = (columns.slice(0, 4).reduce((sum, value) => sum + value, 0) +
      columns.slice(-4).reduce((sum, value) => sum + value, 0)) / 8;
    const centerLuminance = columns.slice(24, 40).reduce((sum, value) => sum + value, 0) / 16;
    const threshold = Math.max(18, centerLuminance * 0.34);

    let leftMargin = 0;
    while (leftMargin < 27 && columns[leftMargin] < threshold) leftMargin += 1;
    let rightMargin = 0;
    while (rightMargin < 27 && columns[63 - rightMargin] < threshold) rightMargin += 1;

    return centerLuminance - edgeLuminance >= 16 &&
      leftMargin >= 6 && rightMargin >= 6 &&
      leftMargin + rightMargin >= 18;
  } catch {
    // A future remote thumbnail may be canvas-tainted; keep the normal image
    // rather than making the card unusable.
    return false;
  }
}

function setupPortfolioThumbnail(thumbDiv, img, isVideo) {
  const backdrop = document.createElement('span');
  backdrop.className = 'portfolio-thumb-backdrop';
  backdrop.setAttribute('aria-hidden', 'true');

  const foreground = document.createElement('span');
  foreground.className = 'portfolio-thumb-foreground';
  foreground.appendChild(img);
  thumbDiv.insertBefore(backdrop, thumbDiv.firstChild);
  thumbDiv.insertBefore(foreground, backdrop.nextSibling);

  if (!isVideo) return;

  const update = () => {
    const isPillarboxed = detectPillarboxedThumbnail(img);
    thumbDiv.classList.toggle('has-pillarbox', isPillarboxed);
    if (!isPillarboxed) {
      backdrop.style.removeProperty('background-image');
      return;
    }

    const source = img.currentSrc || img.src;
    if (source) {
      const safeSource = source.replace(/"/g, '%22');
      backdrop.style.backgroundImage = `url("${safeSource}")`;
    }
  };

  img.addEventListener('load', update);
  img.addEventListener('error', () => {
    thumbDiv.classList.remove('has-pillarbox');
    backdrop.style.removeProperty('background-image');
  });
  if (img.complete) update();
}

async function initApp() {
  initLangToggle();
  initPortfolioCarousel();
  updateStaticTranslations();
  
  try {
    const res = await fetch('assets/data/featured-projects.json?v=1.0');
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

async function ensureFullProjectCatalog() {
  if (projectsCatalogLoaded) return projectsData;
  if (!projectsCatalogPromise) {
    projectsCatalogPromise = fetch('assets/data/projects.json?v=1.20')
      .then((res) => {
        if (!res.ok) throw new Error('Failed to fetch full project catalog');
        return res.json();
      })
      .then((catalog) => {
        projectsData = catalog;
        projectsCatalogLoaded = true;
        return catalog;
      })
      .catch((error) => {
        projectsCatalogPromise = null;
        throw error;
      });
  }
  return projectsCatalogPromise;
}

function setLangButtonState() {
  const langMeta = currentLang === 'vi'
    ? { flag: 'vi', code: 'VN', next: 'en', label: 'Chuyển sang tiếng Anh' }
    : { flag: 'en', code: 'EN', next: 'vi', label: 'Switch to Vietnamese' };

  elements.langBtns.forEach(b => {
    b.dataset.lang = currentLang;
    b.dataset.nextLang = langMeta.next;
    b.classList.add('active');
    b.removeAttribute('aria-pressed');
    b.setAttribute('aria-label', langMeta.label);
    b.title = langMeta.label;

    const flag = b.querySelector('.lang-flag');
    const code = b.querySelector('.lang-code');
    if (flag) {
      flag.textContent = '';
      flag.dataset.flag = langMeta.flag;
    }
    if (code) code.textContent = langMeta.code;
  });
}

function initLangToggle() {
  setLangButtonState();

  const cvIframe = document.querySelector('#cvModal iframe');
  if (cvIframe) {
    const cvUrl = new URL(cvIframe.dataset.src || 'cv.html?modal=1&v=1.47', window.location.href);
    cvUrl.searchParams.set('lang', currentLang);
    cvIframe.dataset.src = cvUrl.href;
  }

  elements.langBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const selectedBtn = e.target.closest('.lang-btn');
      if (!selectedBtn) return;

      currentLang = currentLang === 'vi' ? 'en' : 'vi';
      setLangButtonState();
      localStorage.setItem('portfolio_lang', currentLang);

      const url = new URL(window.location.href);
      url.searchParams.set('lang', currentLang);
      window.history.replaceState({}, '', url);

      const cvIframe = document.querySelector("#cvModal iframe");
      if (cvIframe && cvIframe.contentWindow) {
        cvIframe.contentWindow.postMessage({ type: "LANG_TOGGLE", lang: currentLang }, window.location.origin);
      } else if (cvIframe) {
        const cvUrl = new URL(cvIframe.dataset.src || 'cv.html?modal=1&v=1.47', window.location.href);
        cvUrl.searchParams.set('lang', currentLang);
        cvIframe.dataset.src = cvUrl.href;
      }

      renderPortfolio(document.querySelector('.filter-btn.active')?.dataset.filter || 'all');
      updateStaticTranslations();
      
      const activeSlide = document.querySelector('.showcase-slide.active');
      if (activeSlide) {
        initShowcaseSlider(); // Reinitialize showcase slider with selected language
      }
    });
  });
}

const translations = {
  vi: {
    nav_home: 'Trang chủ',
    nav_about: 'Về mình',
    nav_services: 'Dịch vụ',
    nav_exp: 'Kinh nghiệm',
    nav_port: 'Portfolio',
    nav_labs: 'Dự án',
    nav_contact: 'Liên hệ',
    nav_collab: 'Liên hệ hợp tác',
    page_title: 'Hà Đình Long | Video Editor & Motion Graphics',
    page_description: 'Portfolio của Hà Đình Long (Long Leo) — Video Editor / Motion Graphics / Post-Production tại TP.HCM. Quay dựng, hậu kỳ, thiết kế và UI/UX. Hơn 6 năm kinh nghiệm theo các mốc công việc đã liệt kê.',
    og_title: 'Hà Đình Long | Video Editor & Motion Graphics',
    og_description: 'Video Editor / Motion Graphics / Post-Production tại TP.HCM — quay dựng, hậu kỳ, thiết kế và UI/UX.',
    hero_pill: '✦ Video Editor • Motion Graphics • Post-Production',
    hero_title: '<span class="hero-line">Video Editor</span><span class="hero-line">có <span class="gradient-text">nhịp</span></span><span class="hero-line">Hậu kỳ có lực</span>',
    hero_desc: 'Tôi biến footage, âm thanh và typography thành những câu chuyện nhìn thấy được — từ concept, quay phim đến hậu kỳ hoàn chỉnh.',
    hero_btn1: 'Xem portfolio ↗',
    hero_btn_cv: 'Xem CV 📄',
    hero_btn2: 'Liên hệ hợp tác ✉',
    stat_exp_value: '6+',
    stat_proj_value: '+100',
    stat_start_value: '03',
    stat_exp: 'năm kinh nghiệm',
    stat_proj: 'sản phẩm đã thực hiện',
    stat_start: 'trục chuyên môn',
    hero_meta_aria: 'Thông tin nhanh',
    partners_title: 'ĐỐI TÁC HỢP TÁC',
    available_for: 'Sẵn sàng hợp tác',
    about_eyebrow: 'Một chút về mình',
    about_title: 'Hậu kỳ có nhịp, hình ảnh có mục tiêu',
    about_p1: 'Mình là <strong>Hà Đình Long</strong>, hay còn được biết đến với tên <strong>Long Leo</strong> — Video Editor tập trung vào hậu kỳ, motion graphics và visual storytelling — học Multimedia tại Arena Multimedia từ năm 2015 và bắt đầu làm việc chuyên nghiệp từ năm 2018',
    about_p2: 'Với hơn 6 năm kinh nghiệm theo các mốc công việc đã liệt kê qua agency, in-house và freelance, mình biến footage, âm thanh và typography thành những sản phẩm rõ ý tưởng, có nhịp và có mục tiêu truyền thông',
    about_skill1: '<strong>Tư duy thẩm mỹ</strong>Cân bằng hình ảnh và mục tiêu truyền thông',
    about_skill2: '<strong>Quy trình tối ưu</strong>Ứng dụng công nghệ và AI để sản xuất nhanh hơn',
    about_skill3: '<strong>Đa năng</strong>Quay, dựng, motion, design và UI/UX',
    tools_kicker: 'BỘ CÔNG CỤ',
    tools_title: 'Bộ công cụ làm việc',
    tools_group1_title: 'EDITING / POST',
    tools_group_visual_title: 'VISUAL SUPPORT',
    tool_prem: 'Dựng phim & Màu sắc',
    tool_ae: 'Motion & hậu kỳ kỹ xảo',
    tool_ps: 'Chỉnh ảnh & Cắt ghép',
    tool_ai: 'Thiết kế Vector & ấn phẩm',
    tool_figma: 'Thiết kế giao diện UI/UX',
    tool_capcut: 'Dựng video nhanh & tiện lợi',
    tool_canva: 'Thiết kế đồ họa trực tuyến',
    tools_group2_title: 'AI / WORKFLOW',
    tool_gemini: 'Lên ý tưởng & Lịch trình',
    tool_ai_studio: 'Thử nghiệm Prompt & API',
    tool_antigravity: 'Tự động hóa & Coding',
    tool_claude: 'Phân tích & Viết nội dung',
    tool_codex: 'Hỗ trợ Kỹ thuật & Code',
    services_eyebrow: 'Dịch vụ',
    services_title: 'Giải pháp hình ảnh & truyền thông toàn diện',
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
    exp_title: 'Hành trình hơn 6 năm trong ngành sáng tạo',
    exp_desc: 'Từ in ấn, đào tạo, freelance, đến thương hiệu công nghệ —<br>mỗi môi trường đều mang đến một góc nhìn mới về truyền thông và sáng tạo.',
    exp_seosona_role: 'Nhân viên Media',
    exp_seosona_desc: 'Quay dựng, biên tập và hậu kỳ video phục vụ truyền thông, quảng bá thương hiệu. Thiết kế hình ảnh, banner, poster cho các nền tảng truyền thông.',
    exp_seosona_btn: 'Ghé thăm SEOSONA ↗',
    exp_v2h_role: 'Nhân viên Media',
    exp_v2h_time: '03/2025 – 05/2026',
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
    labs_eyebrow: 'Dự án',
    labs_title: 'Không chỉ dùng công cụ — mình xây luôn công cụ',
    labs_desc: 'Những dự án mình tự phát triển để biến ý tưởng thành hệ thống có thể dùng được.<br>Chọn một dự án để mở trải nghiệm.',
    labs_mode_label: 'Khám phá dự án',
    labs_toolbar_aria: 'Bộ lọc dự án',
    labs_group_aria: 'Lọc dự án',
    labs_filter_all: 'Tất cả dự án',
    labs_filter_live: 'Landing live',
    labs_filter_local: 'Dự án trong portfolio',
    labs_expand: 'Xem thêm dự án',
    labs_collapse: 'Thu gọn dự án',
    labs_all: 'Xem toàn bộ trên GitHub ↗',
    port_eyebrow: 'Portfolio',
    port_title: 'Sản phẩm nổi bật',
    port_desc: 'Tổng hợp sản phẩm video editing, motion graphics, thiết kế và nội dung sáng tạo từ kênh YouTube @LongLeo287 cùng các dự án thực tế.',
    contact_eyebrow: 'Liên hệ',
    contact_title: 'Cảm ơn bạn đã dành thời gian ghé thăm',
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
    nav_labs: 'Projects',
    nav_contact: 'Contact',
    nav_collab: 'Let\'s collaborate',
    page_title: 'Ha Dinh Long | Video Editor & Motion Graphics',
    page_description: 'Portfolio of Ha Dinh Long (Long Leo) — Video Editor / Motion Graphics / Post-Production in Ho Chi Minh City. Video, editing, design and UI/UX. More than 6 verified years across the work periods listed in my profile.',
    og_title: 'Ha Dinh Long | Video Editor & Motion Graphics',
    og_description: 'Video Editor / Motion Graphics / Post-Production in Ho Chi Minh City — video production, editing, design and UI/UX.',
    hero_pill: '✦ Video Editor • Motion Graphics • Post-Production',
    hero_title: '<span class="hero-line">Video Editor</span><span class="hero-line">with <span class="gradient-text">rhythm</span></span><span class="hero-line">Post-production with force</span>',
    hero_desc: 'I turn footage, sound and typography into visible stories — from concept and filming to finished post-production.',
    hero_btn1: 'View Portfolio ↗',
    hero_btn_cv: 'View CV 📄',
    hero_btn2: 'Let\'s Talk ✉',
    stat_exp_value: '6+',
    stat_proj_value: '+100',
    stat_start_value: '03',
    stat_exp: 'years of experience',
    stat_proj: 'creative works delivered',
    stat_start: 'creative disciplines',
    hero_meta_aria: 'Quick facts',
    partners_title: 'TRUSTED BY',
    available_for: 'Available for',
    about_eyebrow: 'A little about me',
    about_title: 'Post-production with rhythm, visuals with purpose',
    about_p1: 'I\'m <strong>Ha Dinh Long</strong>, also known as <strong>Long Leo</strong> — a Video Editor focused on post-production, motion graphics and visual storytelling — studied Multimedia at Arena Multimedia from 2015 and started working professionally in 2018',
    about_p2: 'With more than 6 verified years across the work periods listed in my profile, spanning agency, in-house and freelance work, I turn footage, sound and typography into clear, rhythmic and purposeful visual content',
    about_skill1: '<strong>Aesthetic sense</strong>Balancing visuals with communication goals',
    about_skill2: '<strong>Optimized workflow</strong>Using technology and AI to work faster',
    about_skill3: '<strong>Versatile</strong>Filming, editing, motion, design and UI/UX',
    tools_kicker: 'TOOLKIT',
    tools_title: 'Working toolkit',
    tools_group1_title: 'EDITING / POST',
    tools_group_visual_title: 'VISUAL SUPPORT',
    tool_prem: 'Video Editing & Color Grading',
    tool_ae: 'Motion Graphics & Visual Effects',
    tool_ps: 'Photo Editing & Compositing',
    tool_ai: 'Vector Design & Print Publications',
    tool_figma: 'UI/UX Interface Design',
    tool_capcut: 'Fast & Convenient Video Editing',
    tool_canva: 'Online Graphic Design',
    tools_group2_title: 'AI / WORKFLOW',
    tool_gemini: 'Brainstorming & Scheduling',
    tool_ai_studio: 'Prompting & API Experimentation',
    tool_antigravity: 'Automation & Coding',
    tool_claude: 'Analysis & Content Writing',
    tool_codex: 'Technical Support & Code',
    services_eyebrow: 'Services',
    services_title: 'Comprehensive Video & Media Solutions',
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
    exp_title: 'A journey of more than 6 years in the creative industry',
    exp_desc: 'From printing, training, freelance, to technology brands —<br>each environment brings a new perspective on media and creativity.',
    exp_seosona_role: 'Media Specialist',
    exp_seosona_desc: 'Film, edit and post-produce videos for communication and brand promotion. Design visual assets, banners and posters for communication platforms.',
    exp_seosona_btn: 'Visit SEOSONA ↗',
    exp_v2h_role: 'Media Specialist',
    exp_v2h_time: '03/2025 – 05/2026',
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
    labs_eyebrow: 'Projects',
    labs_title: 'Not just using tools — I build them',
    labs_desc: 'Projects I built to turn ideas into systems people can actually use.<br>Choose a project to open the experience.',
    labs_mode_label: 'Explore projects',
    labs_toolbar_aria: 'Project filters',
    labs_group_aria: 'Filter projects',
    labs_filter_all: 'All projects',
    labs_filter_live: 'Live landings',
    labs_filter_local: 'Portfolio projects',
    labs_expand: 'Show more projects',
    labs_collapse: 'Show fewer projects',
    labs_all: 'See everything on GitHub ↗',
    port_eyebrow: 'Portfolio',
    port_title: 'Featured Work',
    port_desc: 'A selection of video editing, motion graphics, design and creative work from YouTube channel @LongLeo287 and real-world projects.',
    contact_eyebrow: 'Contact',
    contact_title: 'Thank you for taking the time to visit',
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
  if (window._pillTypingInterval) {
    clearInterval(window._pillTypingInterval);
    window._pillTypingInterval = null;
  }

  document.documentElement.lang = currentLang;

  updateSeoMetadata();

  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    if (translations[currentLang] && translations[currentLang][key]) {
      if (key === 'hero_pill') return;
      el.innerHTML = translations[currentLang][key];
    }
  });

  document.querySelectorAll('[data-i18n-aria]').forEach(el => {
    const key = el.dataset.i18nAria;
    if (translations[currentLang] && translations[currentLang][key]) {
      el.setAttribute('aria-label', translations[currentLang][key]);
    }
  });

  const pillText = translations[currentLang] && translations[currentLang]['hero_pill'];
  if (pillText && typeof window.startPillTyping === 'function') {
    window.startPillTyping(pillText);
  }

  const themeToggle = document.getElementById('themeToggle');
  if (themeToggle && translations[currentLang] && translations[currentLang].theme_aria) {
    themeToggle.setAttribute('aria-label', translations[currentLang].theme_aria);
  }
  
  const dict = translations[currentLang] || translations.vi;
  const setPlaceholder = (selector, key) => {
    const el = document.querySelector(selector);
    if (el && dict[key]) el.placeholder = dict[key];
  };
  setPlaceholder('#cf-name', 'form_ph_name');
  setPlaceholder('#cf-email', 'form_ph_email');
  setPlaceholder('#cf-message', 'form_ph_message');

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

  if (typeof window.refreshTextReveal === 'function') {
    window.refreshTextReveal();
  }

  window.dispatchEvent(new CustomEvent('portfolio:languagechange'));
}

function updateSeoMetadata() {
  const dict = translations[currentLang] || translations.vi;
  document.title = dict.page_title;

  const setMeta = (selector, content) => {
    const el = document.querySelector(selector);
    if (el && content) el.setAttribute('content', content);
  };

  setMeta('meta[name="description"]', dict.page_description);
  setMeta('meta[property="og:title"]', dict.og_title);
  setMeta('meta[property="og:description"]', dict.og_description);
  setMeta('meta[property="og:locale"]', currentLang === 'en' ? 'en_US' : 'vi_VN');
  setMeta('meta[property="og:locale:alternate"]', currentLang === 'en' ? 'vi_VN' : 'en_US');
  setMeta('meta[name="twitter:title"]', dict.og_title);
  setMeta('meta[name="twitter:description"]', dict.og_description);

  const ogUrl = document.querySelector('meta[property="og:url"]');
  if (ogUrl) {
    const shareUrl = new URL(window.location.href);
    shareUrl.hash = '';
    ogUrl.setAttribute('content', shareUrl.href);
  }

  const schema = document.querySelector('script[type="application/ld+json"]');
  if (schema) {
    try {
      const data = JSON.parse(schema.textContent);
      data.inLanguage = currentLang;
      if (data.mainEntity) data.mainEntity.description = dict.page_description;
      schema.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
      console.warn('Could not update JSON-LD metadata:', error);
    }
  }
}

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

function renderPortfolio(filter = 'all') {
  if (!elements.grid) return;
  
  elements.grid.innerHTML = '';
  
  let displayedCards = [];
  
  const filtered = projectsData.filter(p => {
    if (filter === 'all') return p.isFeatured;
    return p.category === filter;
  });
  
  let displayList = [...filtered];
  if (filter === 'Video') {
    displayList.sort((a, b) => String(b.publishedAt || '').localeCompare(String(a.publishedAt || '')));
  }
  if (filter === 'all') {
    const shuffle = (items) => {
      const result = [...items];
      for (let i = result.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [result[i], result[j]] = [result[j], result[i]];
      }
      return result;
    };
    const videos = filtered.filter((project) => project.category === 'Video');
    const images = filtered.filter((project) => project.category !== 'Video');
    const required = [
      ...shuffle(videos).slice(0, 1),
      ...shuffle(images).slice(0, 1),
    ];
    const requiredIds = new Set(required.map((project) => project.id));
    displayList = shuffle([
      ...required,
      ...shuffle(filtered.filter((project) => !requiredIds.has(project.id))),
    ]).slice(0, 9);
  }
  
  const fragment = document.createDocumentFragment();
  let currentPage;

  displayList.forEach((p, index) => {
    if (index % PORTFOLIO_PAGE_SIZE === 0) {
      currentPage = document.createElement('div');
      currentPage.className = 'portfolio-page';
      currentPage.dataset.page = String(index / PORTFOLIO_PAGE_SIZE);
      fragment.appendChild(currentPage);
    }

    const card = document.createElement('a');
    card.className = `portfolio-card fade-up${p.category === 'Photography' ? ' photo-only' : ''}`;
    card.dataset.category = p.category;
    card.dataset.id = p.id;
    card.href = p.href || p.imgSrc;
    card.rel = 'noopener';
    card.setAttribute('aria-haspopup', 'dialog');
    card.setAttribute('aria-controls', 'caseStudyModal');
    card.setAttribute('aria-expanded', 'false');

    const title = typeof p.title === 'object' ? p.title[currentLang] : p.title;
    const client = typeof p.client === 'object' ? p.client[currentLang] : p.client;

    const tagText =
      p.category === 'Design' ? (currentLang === 'vi' ? 'Thiết kế' : 'Design') :
      p.category === 'Photography' ? (currentLang === 'vi' ? 'Chụp ảnh' : 'Photography') :
      p.category;

    const thumbDiv = document.createElement('div');
    thumbDiv.className = 'portfolio-thumb';

    const img = document.createElement('img');
    img.dataset.src = p.imgSrc;
    const srcset = buildSrcset(p.imgSrc);
    if (srcset) {
      img.dataset.srcset = srcset;
      img.dataset.sizes = '(max-width: 560px) 92vw, (max-width: 900px) 46vw, 300px';
    }
    img.alt = p.alt || title || '';
    img.loading = 'lazy';
    img.decoding = 'async';

    const opensVideo = p.category === 'Video' ||
      (p.category === 'Thumbnail' && typeof p.href === 'string' && p.href.includes('youtube.com'));
    if (opensVideo) thumbDiv.classList.add('is-video-thumb');

    const tag = document.createElement('span');
    tag.className = 'tag';
    tag.textContent = tagText;

    thumbDiv.append(tag);
    setupPortfolioThumbnail(thumbDiv, img, opensVideo);

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
      card.setAttribute('aria-label', title);
    }

    card.addEventListener('click', (e) => handleCardClick(e, p));

    currentPage.appendChild(card);
    displayedCards.push(card);
  });

  elements.grid.appendChild(fragment);
  portfolioPage = 0;
  window.portfolioMedia?.observe(elements.grid);
  elements.grid.setAttribute('aria-busy', 'false');
  updatePortfolioCarousel();
  if (typeof window.recacheSectionOffsets === 'function') {
    window.recacheSectionOffsets();
  }

  const reveal = () => {
    displayedCards.forEach((card, idx) => {
      card.style.transitionDelay = `${Math.min(idx * 40, 280)}ms`;
      card.classList.add('show');
    });
    applyCardEffects(displayedCards);
  };

  if (document.visibilityState === 'hidden') {
    reveal();
  } else {
    requestAnimationFrame(reveal);
  }
}

function applyCardEffects(cards) {
  const motion = window.portfolioMotion;
  if (!motion || !motion.finePointer() || motion.reducedMotion()) return;

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

      const swap = async () => {
        if (clickedBtn.dataset.filter !== 'all') {
          try {
            await ensureFullProjectCatalog();
          } catch (error) {
            console.error('Error loading full project catalog:', error);
          }
        }
        renderPortfolio(clickedBtn.dataset.filter);
      };

      const reducedMotion = window.portfolioMotion?.reducedMotion?.()
        ?? window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (document.startViewTransition && !reducedMotion) {
        document.startViewTransition(swap);
      } else {
        swap();
      }
    });
  });
}

async function handleCardClick(e, project) {
  e.preventDefault();
  const trigger = e.currentTarget;
  try {
    await ensureFullProjectCatalog();
  } catch (error) {
    console.error('Error loading project details:', error);
  }
  const completeProject = projectsData.find((item) => item.id === project.id) || project;
  openCaseStudyModal(completeProject, trigger);
}

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

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, (character) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  })[character]);
}

const ModalManager = (() => {
  const FOCUSABLE = [
    'a[href]', 'button:not([disabled])', 'input:not([disabled])',
    'textarea:not([disabled])', 'select:not([disabled])', 'iframe',
    '[tabindex]:not([tabindex="-1"])'
  ].join(',');

  let openEl = null;
  let lastFocused = null;
  let lastTrigger = null;
  let onCloseHook = null;
  let backgroundInertState = [];

  function setBackgroundInert(isInert) {
    const background = Array.from(document.querySelectorAll('body > header, body > main, body > footer, body > .back-to-top'));
    if (isInert) {
      backgroundInertState = background.map((node) => ({
        node,
        inert: node.inert === true,
        hadAttribute: node.hasAttribute('inert')
      }));
      background.forEach((node) => { node.inert = true; });
      return;
    }
    backgroundInertState.forEach(({ node, inert, hadAttribute }) => {
      node.inert = inert;
      if (!inert && !hadAttribute) node.removeAttribute('inert');
    });
    backgroundInertState = [];
  }

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
    lastTrigger = options.trigger || null;
    openEl = el;
    onCloseHook = options.onClose || null;

    el.setAttribute('aria-hidden', 'false');
    if (lastTrigger) lastTrigger.setAttribute('aria-expanded', 'true');
    setBackgroundInert(true);
    document.body.classList.add('modal-open');
    document.addEventListener('keydown', handleKeydown, true);
    if (window.lenis) window.lenis.stop();

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
    setBackgroundInert(false);
    const restoreTarget = [lastFocused, lastTrigger].find((node) =>
      node && document.contains(node) && !el.contains(node) && (node.offsetWidth || node.offsetHeight || node === document.body)
    );
    if (restoreTarget) restoreTarget.focus({ preventScroll: true });
    el.setAttribute('aria-hidden', 'true');
    if (lastTrigger && document.contains(lastTrigger)) lastTrigger.setAttribute('aria-expanded', 'false');
    if (typeof hook === 'function') hook();
    if (window.lenis) window.lenis.start();
    lastFocused = null;
    lastTrigger = null;
  }

  return { open, close, isOpen: () => openEl !== null, current: () => openEl };
})();

window.ModalManager = ModalManager;

function openCaseStudyModal(project, trigger = document.activeElement) {
  const title = typeof project.title === 'object' ? project.title[currentLang] : project.title;
  const client = typeof project.client === 'object' ? project.client[currentLang] : project.client;
  
  elements.modalTitle.textContent = title;
  elements.modalClient.textContent = client;
    
  if (elements.modalLink) {
    elements.modalLink.innerHTML = translations[currentLang]['modal_view_link'];
  }
  
  let tagsHtml = '';
  if (project.caseStudy && project.caseStudy.tools) {
    tagsHtml = project.caseStudy.tools.map(t => `<span>${t.trim()}</span>`).join('');
  } else {
    tagsHtml = `<span>${project.category}</span>`;
  }
  elements.modalTags.innerHTML = tagsHtml;
  
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
  
  elements.modalMedia.innerHTML = '';
  const isYouTubeHref = Boolean(getYouTubeUrlInfo(project.href));
  const modalWrapper = elements.modal?.querySelector('.modal-content-wrapper');
  const layout = document.querySelector('.modal-layout');
  const isVideoModal = project.category === 'Video' || (project.category === 'Thumbnail' && isYouTubeHref);

  elements.modalMedia.classList.toggle('image-only', !isVideoModal);
  layout?.classList.toggle('image-only', !isVideoModal);
  modalWrapper?.classList.toggle('image-only', !isVideoModal);

  if (isVideoModal) {
    const embedUrl = getYouTubeEmbedUrl(project.href || project.imgSrc);
    if (embedUrl) {
      elements.modalMedia.appendChild(createYouTubeIframe(embedUrl, title));
    } else if (project.href) {
      elements.modalMedia.innerHTML = `<a href="${project.href}" target="_blank" rel="noopener noreferrer" class="modal-yt-btn">${currentLang === 'en' ? 'Open video on YouTube' : 'Mở video trên YouTube'}</a>`;
    }
  } else {
    const ytLabel = currentLang === 'en' ? '▶ Watch on YouTube' : '▶ Xem trên YouTube';
    const ytBtn = isYouTubeHref
      ? `<a href="${project.href}" target="_blank" rel="noopener noreferrer" class="modal-yt-btn">${ytLabel}</a>`
      : '';
    elements.modalMedia.innerHTML = `
      <img src="${project.imgSrc}" alt="${title}" decoding="async" />
      ${ytBtn}
    `;

    const modalImage = elements.modalMedia.querySelector('img');
    const syncImageModalRatio = () => {
      if (!modalImage?.naturalWidth || !modalImage?.naturalHeight || !modalWrapper) return;
      modalWrapper.style.setProperty(
        '--modal-image-ratio',
        (modalImage.naturalWidth / modalImage.naturalHeight).toFixed(6)
      );
    };
    modalImage?.addEventListener('load', syncImageModalRatio, { once: true });
    if (modalImage?.complete) syncImageModalRatio();
  }

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
    trigger,
    onClose: () => {
      elements.modal.classList.remove('active');
      if (elements.modalMedia) elements.modalMedia.innerHTML = '';
      elements.modalMedia?.classList.remove('image-only');
      layout?.classList.remove('image-only');
      modalWrapper?.classList.remove('image-only');
      modalWrapper?.style.removeProperty('--modal-image-ratio');
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

function openLightbox(project, trigger = document.activeElement) {
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
    const iframe = createYouTubeIframe(embedUrl, title);
    lightboxVideo.src = iframe.src;
    lightboxVideo.title = iframe.title;
    lightboxVideo.setAttribute('allow', iframe.getAttribute('allow'));
    lightboxVideo.setAttribute('referrerpolicy', iframe.getAttribute('referrerpolicy'));
    lightboxVideoWrapper.style.display = "block";
    lightboxModal.classList.add("show");
  } else {
    lightboxImage.src = project.imgSrc;
    lightboxImage.alt = title;
    lightboxModal.classList.add("show");
  }

  ModalManager.open(lightboxModal, {
    initialFocus: lightboxModal.querySelector('.lightbox-close'),
    trigger,
    onClose: () => {
      lightboxModal.classList.remove("show");
      lightboxImage.src = "";
      if (lightboxVideo) lightboxVideo.src = "";
      if (lightboxVideoWrapper) lightboxVideoWrapper.style.display = "none";
    }
  });
}

const YOUTUBE_HOSTS = new Set(['youtube.com', 'www.youtube.com', 'm.youtube.com', 'youtu.be', 'www.youtu.be', 'youtube-nocookie.com', 'www.youtube-nocookie.com']);

function getYouTubeUrlInfo(value) {
  if (!value || typeof value !== 'string') return null;
  let parsed;
  try {
    parsed = new URL(value);
  } catch {
    return null;
  }
  if (!/^https?:$/.test(parsed.protocol) || !YOUTUBE_HOSTS.has(parsed.hostname.toLowerCase())) return null;

  const host = parsed.hostname.toLowerCase();
  const path = parsed.pathname.replace(/^\/+|\/+$/g, '');
  const parts = path.split('/').filter(Boolean);
  const videoId = host.includes('youtu.be')
    ? parts[0]
    : (parts[0] === 'watch' ? parsed.searchParams.get('v') :
      (['shorts', 'embed', 'live'].includes(parts[0]) ? parts[1] : null));
  const listId = parsed.searchParams.get('list');
  if (!videoId && !listId) return null;
  if (videoId && !/^[A-Za-z0-9_-]{6,}$/.test(videoId)) return null;
  if (listId && !/^[A-Za-z0-9_-]{6,}$/.test(listId)) return null;
  return { videoId, listId };
}

function getYouTubeEmbedUrl(url) {
  const info = getYouTubeUrlInfo(url);
  if (!info) return null;
  const params = new URLSearchParams({ autoplay: '1', playsinline: '1', rel: '0' });
  if (info.videoId) {
    return `https://www.youtube-nocookie.com/embed/${encodeURIComponent(info.videoId)}?${params}`;
  }
  return `https://www.youtube-nocookie.com/embed/videoseries?${new URLSearchParams({ list: info.listId, autoplay: '1', playsinline: '1', rel: '0' })}`;
}

function createYouTubeIframe(src, title = 'YouTube video') {
  const iframe = document.createElement('iframe');
  iframe.src = src;
  iframe.title = title;
  iframe.loading = 'lazy';
  iframe.referrerPolicy = 'strict-origin-when-cross-origin';
  iframe.setAttribute('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share');
  iframe.setAttribute('allowfullscreen', '');
  return iframe;
}

let selectedSliderItems = null;
let sliderInterval = null;
let sliderVisibilityObserver = null;
let sliderInViewport = false;
let sliderPausedByInteraction = false;
let sliderPausedByFocus = false;
let sliderPausedByUser = false;
let resumeSliderInterval = () => {};
let currentSlideIndex = 0;

function initShowcaseSlider() {
  const slidesContainer = document.getElementById('showcaseSlides');
  const dotsContainer = document.getElementById('sliderDots');
  const toggleBtn = document.getElementById('toggleSliderBtn');
  const prevBtn = document.getElementById('prevSlideBtn');
  const nextBtn = document.getElementById('nextSlideBtn');
  
  if (!slidesContainer || projectsData.length === 0) return;
  
  let selectedVideo;
  let selectedImages;

  if (selectedSliderItems) {
    selectedVideo = selectedSliderItems.video;
    selectedImages = selectedSliderItems.images;
  } else {
    const featuredVideos = projectsData.filter(p => p.category === 'Video' && p.isFeatured);
    selectedVideo = featuredVideos.length > 0 
      ? featuredVideos[Math.floor(Math.random() * featuredVideos.length)]
      : projectsData.find(p => p.category === 'Video');
      
    const imageProjects = projectsData.filter(p => (p.category === 'Design' || p.category === 'Photography') && p.imgSrc);
    const shuffledImages = [...imageProjects].sort(() => 0.5 - Math.random());
    selectedImages = shuffledImages.slice(0, 4);
    
    selectedSliderItems = {
      video: selectedVideo,
      images: selectedImages
    };
  }
  
  const getVideoPreview = (project) => {
    const candidate = project?.imgSrc || project?.previewSrc;
    const localPreview = typeof candidate === 'string' && !/^https?:\/\//i.test(candidate)
      ? candidate
      : '';
    return localPreview || 'assets/img/og-cover.jpg';
  };
  
  let slidesHtml = '';
  let slideIndexCounter = 0;
  const totalSlideCount = (selectedVideo ? 1 : 0) + selectedImages.length;
  
  if (selectedVideo) {
    const isActive = slideIndexCounter === currentSlideIndex;
    const videoThumb = getVideoPreview(selectedVideo);
    const videoTitle = typeof selectedVideo.title === 'object' ? selectedVideo.title[currentLang] : selectedVideo.title;
    const tagText = translations[currentLang].categories.video;
    slidesHtml += `
      <div class="showcase-slide ${isActive ? 'active' : ''}" role="group" aria-roledescription="slide" aria-label="${slideIndexCounter + 1} / ${totalSlideCount}" aria-hidden="${String(!isActive)}" data-type="video" data-video-src="${escapeHtml(selectedVideo.href)}" data-preview-src="${escapeHtml(videoThumb)}">
        <div class="showcase-img-wrap">
          <div class="showcase-bg-blur" data-bg-src="${escapeHtml(videoThumb)}" data-release-media="true" data-release-bg="${escapeHtml(videoThumb)}"></div>
          <button class="yt-facade" type="button" aria-label="Phát video: ${escapeHtml(videoTitle)}">
            <img data-src="${escapeHtml(videoThumb)}" data-release-media="true" data-release-src="${escapeHtml(videoThumb)}" alt="${escapeHtml(videoTitle)}"
                 style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover; z-index:0; border-radius:inherit;">
            <div class="yt-play-btn" style="position:relative; z-index:2;" aria-hidden="true">
              <svg viewBox="0 0 24 24" width="24" height="24"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>
            </div>
          </button>
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
    const blurSrc = (srcset ? imgProj.imgSrc.replace(/\.(webp|jpe?g|png)$/i, '-480.webp') : imgProj.imgSrc);
    slidesHtml += `
      <div class="showcase-slide ${isActive ? 'active' : ''}" role="group" aria-roledescription="slide" aria-label="${slideIndexCounter + 1} / ${totalSlideCount}" aria-hidden="${String(!isActive)}" data-type="image" data-src="${escapeHtml(imgProj.imgSrc)}">
        <div class="showcase-img-wrap">
          <div class="showcase-bg-blur" data-bg-src="${escapeHtml(blurSrc)}" data-release-media="true" data-release-bg="${escapeHtml(blurSrc)}"></div>
          <img data-src="${escapeHtml(imgProj.imgSrc)}" data-release-media="true" data-release-src="${escapeHtml(imgProj.imgSrc)}"${srcsetAttr.replace(' srcset=', ' data-srcset=').replace(' sizes=', ' data-sizes=')} alt="${escapeHtml(title)}" decoding="async" loading="lazy" />
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
  window.portfolioMedia?.observe(slidesContainer);
  
  const slides = slidesContainer.querySelectorAll('.showcase-slide');
  const slideFocusableSelector = [
    'a[href]',
    'area[href]',
    'button:not([disabled])',
    'input:not([disabled])',
    'select:not([disabled])',
    'textarea:not([disabled])',
    'iframe',
    'object',
    'embed',
    '[contenteditable="true"]',
    '[tabindex]'
  ].join(',');

  function setSlideAccessibility(slide, isActive) {
    slide.setAttribute('aria-hidden', String(!isActive));
    slide.inert = !isActive;

    slide.querySelectorAll(slideFocusableSelector).forEach((control) => {
      if (isActive) {
        if (!control.hasAttribute('data-slider-original-tabindex')) return;
        const originalTabindex = control.getAttribute('data-slider-original-tabindex');
        if (originalTabindex === '') control.removeAttribute('tabindex');
        else control.setAttribute('tabindex', originalTabindex);
        control.removeAttribute('data-slider-original-tabindex');
        return;
      }

      if (!control.hasAttribute('data-slider-original-tabindex')) {
        control.setAttribute(
          'data-slider-original-tabindex',
          control.getAttribute('tabindex') ?? ''
        );
      }
      control.setAttribute('tabindex', '-1');
    });
    if (isActive && sliderInViewport) window.portfolioMedia?.load(slide);
  }

  slides.forEach((slide, idx) => {
    setSlideAccessibility(slide, idx === currentSlideIndex);
  });
  
  if (dotsContainer) {
    dotsContainer.innerHTML = '';
    slides.forEach((_, idx) => {
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.className = `slider-dot ${idx === currentSlideIndex ? 'active' : ''}`;
      dot.setAttribute('aria-label', `${currentLang === 'en' ? 'Go to slide' : 'Đến slide'} ${idx + 1}`);
      dot.setAttribute('aria-current', String(idx === currentSlideIndex));
      dot.setAttribute('aria-disabled', String(idx === currentSlideIndex));
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
    setSlideAccessibility(slides[currentSlideIndex], false);
    if (dots.length > 0) dots[currentSlideIndex].classList.remove('active');
    
    const currentSlide = slides[currentSlideIndex];
    window.portfolioMedia?.release(currentSlide);
    if (currentSlide && currentSlide.dataset.type === 'video') {
      const iframe = currentSlide.querySelector('iframe');
      if (iframe) {
        const wrap = currentSlide.querySelector('.showcase-img-wrap');
        const title = currentSlide.querySelector('h3')?.textContent || 'Video';
        const videoSrc = currentSlide.dataset.videoSrc;
        iframe.remove();
        if (wrap && videoSrc) {
          const facade = document.createElement('button');
          facade.type = 'button';
          facade.className = 'yt-facade';
          facade.setAttribute('aria-label', `${currentLang === 'en' ? 'Play video' : 'Phát video'}: ${title}`);
          const thumb = getVideoPreview(currentSlide.dataset);
          facade.innerHTML = `<img data-src="${escapeHtml(thumb)}" data-release-media="true" data-release-src="${escapeHtml(thumb)}" alt="${escapeHtml(title)}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;border-radius:inherit"><div class="yt-play-btn" style="position:relative;z-index:2" aria-hidden="true"><svg viewBox="0 0 24 24" width="24" height="24"><path d="M8 5v14l11-7z" fill="currentColor"/></svg></div>`;
          wrap.appendChild(facade);
        }
      }
    }
    
    currentSlideIndex = (idx + slides.length) % slides.length;
    slides[currentSlideIndex].classList.add('active');
    setSlideAccessibility(slides[currentSlideIndex], true);
    if (dots.length > 0) {
      dots[currentSlideIndex].classList.add('active');
      dots.forEach((dot, dotIndex) => {
        const isCurrent = dotIndex === currentSlideIndex;
        dot.setAttribute('aria-current', String(isCurrent));
        dot.setAttribute('aria-disabled', String(isCurrent));
      });
    }
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
  
  if (!slidesContainer.dataset.facadeBound) {
    slidesContainer.addEventListener('click', (e) => {
      const facade = e.target.closest('.yt-facade');
      if (facade) {
        const slide = facade.closest('.showcase-slide');
        const videoSrc = slide && slide.dataset.videoSrc;
        if (!videoSrc) return;

        const embedUrl = getYouTubeEmbedUrl(videoSrc);
        if (!embedUrl) return;

        const heading = slide.querySelector('h3');
        facade.replaceWith(createYouTubeIframe(embedUrl, heading ? heading.textContent : 'Video'));
        return;
      }

      const imageWrap = e.target.closest('.showcase-slide[data-type="image"] .showcase-img-wrap');
      if (imageWrap) {
        const slide = imageWrap.closest('.showcase-slide');
        const src = slide?.dataset.src;
        const title = slide?.querySelector('h3')?.textContent;
        if (src) openLightbox({ imgSrc: src, category: 'Photography', title }, imageWrap);
      }
    });
    slidesContainer.dataset.facadeBound = 'true';
  }
  
  slides.forEach(slide => {
    if (slide.dataset.type === 'image') slide.querySelector('.showcase-img-wrap')?.style.setProperty('cursor', 'zoom-in');
  });
  
  function startInterval() {
    clearInterval(sliderInterval);
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches ||
        document.visibilityState === 'hidden' || !sliderInViewport || sliderPausedByInteraction || sliderPausedByFocus || sliderPausedByUser || slides.length < 2) return;
    sliderInterval = setInterval(nextSlide, 10000);
  }
  
  function resetInterval() {
    startInterval();
  }
  
  const sliderEl = document.getElementById('showcaseSlider');
  if (sliderEl) {
    sliderEl.onmouseenter = () => { sliderPausedByInteraction = true; clearInterval(sliderInterval); };
    sliderEl.onmouseleave = () => { sliderPausedByInteraction = false; startInterval(); };
    sliderEl.onfocusin = () => { sliderPausedByFocus = true; clearInterval(sliderInterval); };
    sliderEl.onfocusout = (event) => {
      if (!sliderEl.contains(event.relatedTarget)) {
        sliderPausedByFocus = false;
      }
    };
    if (sliderVisibilityObserver) sliderVisibilityObserver.disconnect();
    if ('IntersectionObserver' in window) {
      sliderVisibilityObserver = new IntersectionObserver(([entry]) => {
        sliderInViewport = entry.isIntersecting;
        if (sliderInViewport) {
          window.portfolioMedia?.load(slides[currentSlideIndex]);
          startInterval();
        } else {
          clearInterval(sliderInterval);
          slides.forEach((slide) => window.portfolioMedia?.release(slide));
        }
      }, { rootMargin: '320px 0px', threshold: 0.01 });
      sliderVisibilityObserver.observe(sliderEl);
    } else {
      sliderInViewport = true;
    }
  }

  if (toggleBtn) {
    const syncRotationControl = () => {
      const paused = sliderPausedByUser || window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      toggleBtn.textContent = paused ? '▶' : 'Ⅱ';
      toggleBtn.setAttribute('aria-label', paused
        ? (currentLang === 'en' ? 'Start automatic slide rotation' : 'Chạy tự động chuyển slide')
        : (currentLang === 'en' ? 'Stop automatic slide rotation' : 'Dừng tự động chuyển slide'));
    };
    syncRotationControl();
    toggleBtn.onclick = () => {
      sliderPausedByUser = !sliderPausedByUser;
      sliderPausedByFocus = false;
      if (sliderPausedByUser) clearInterval(sliderInterval);
      else startInterval();
      syncRotationControl();
    };
  }

  resumeSliderInterval = startInterval;
  if (!document.documentElement.dataset.sliderVisibilityBound) {
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'hidden') clearInterval(sliderInterval);
      else resumeSliderInterval();
    });
    document.documentElement.dataset.sliderVisibilityBound = 'true';
  }
  
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

document.addEventListener('DOMContentLoaded', initApp);

document.addEventListener('contextmenu', (e) => {
  if (e.target.tagName === 'IMG') e.preventDefault();
});
document.addEventListener('dragstart', (e) => {
  if (e.target.tagName === 'IMG') e.preventDefault();
});


document.addEventListener('DOMContentLoaded', () => {
  const openCvBtn = document.getElementById('openCvBtn');
  const cvModal = document.getElementById('cvModal');
  const closeCvBtn = document.getElementById('closeCvBtn');

  if (openCvBtn && cvModal && closeCvBtn) {
    const cvIframe = cvModal.querySelector('iframe');
    const loadCv = () => {
      if (!cvIframe || cvIframe.hasAttribute('src') || !cvIframe.dataset.src) return;
      cvIframe.src = cvIframe.dataset.src;
    };
    const releaseCv = () => {
      if (!cvIframe) return;
      cvIframe.src = 'about:blank';
      cvIframe.removeAttribute('src');
    };
    const closeCv = () => ModalManager.close();
    const bindCvFrameKeyboard = () => {
      if (!cvIframe) return;
      try {
        const frameDocument = cvIframe.contentDocument;
        if (!frameDocument || frameDocument.documentElement?.dataset.cvEscapeBound === 'true') return;
        frameDocument.documentElement.dataset.cvEscapeBound = 'true';
        frameDocument.addEventListener('keydown', (event) => {
          if (event.key !== 'Escape') return;
          event.preventDefault();
          closeCv();
        }, true);
      } catch (error) {
        // Cross-origin CV documents cannot be instrumented; the parent close
        // button remains the reliable fallback in that case.
      }
    };

    cvIframe?.addEventListener('load', bindCvFrameKeyboard);

    openCvBtn.addEventListener('click', (e) => {
      e.preventDefault();
      loadCv();
      cvModal.classList.add('active');
      ModalManager.open(cvModal, {
        initialFocus: closeCvBtn,
        trigger: openCvBtn,
        onClose: () => {
          cvModal.classList.remove('active');
          window.setTimeout(releaseCv, 240);
        }
      });
    });

    closeCvBtn.addEventListener('click', closeCv);

    cvModal.addEventListener('click', (e) => {
      if (e.target === cvModal) closeCv();
    });
  }
});

window.copyEmail = async function (btn) {
  const email = 'Longdragon287@gmail.com';
  const isEn = currentLang === 'en';
  const originalText = btn.innerHTML;

  try {
    await navigator.clipboard.writeText(email);
    btn.innerHTML = isEn ? 'Email copied!' : 'Đã chép email!';
  } catch (err) {
    window.location.href = `mailto:${email}`;
    btn.innerHTML = isEn ? 'Opening mail app…' : 'Đang mở ứng dụng mail…';
  }

  setTimeout(() => { btn.innerHTML = originalText; }, 2000);
};
