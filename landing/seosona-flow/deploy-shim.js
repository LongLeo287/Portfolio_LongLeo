/* Lớp nối phần động — chạy sau khi trang đã vẽ.
   Nó làm hai việc, và cả hai đều cần máy chủ nên trang không còn là web tĩnh:
   1. Mọi <form> trên trang gửi thật tới /api/lead, có trạng thái đang gửi / lỗi / xong
   2. Đọc /data/site.json lúc chạy rồi dán một dòng trạng thái deployment vào chân trang */
(function () {
  'use strict';

  /* ---------- Cuộn mượt ----------
     Đo ngày 11/09/2026: scroll-behavior khong duoc khai bao o bat ky trang
     nao trong tam, computed value la 'auto'. Bam muc nav la nhay phich sang
     vi tri moi, khong co gi noi cho mat theo kip.

     Trinh duyet tu tat cuon muot khi may bat prefers-reduced-motion, nen khoi
     @media duoi day chi la viet ro y dinh chu khong phai bat buoc. Nut len dau
     trang da tu chon 'auto' hay 'smooth' theo dung thiet lap do. */
  (function () {
    /* Phai chen lai nhieu lan. Bo dong goi thay ca documentElement bang
       replaceWith sau khi giai nen, keo theo toan bo <head> — ke ca <style>
       vua chen. Do ngay 11/09/2026: ban dau toi chen mot lan, tren trang that
       #__cuon_muot khong ton tai, scroll-behavior van la 'auto'.
       __totop_css va __focus_fix song duoc chinh vi chung chen lai. */
    function chen() {
      if (document.getElementById('__cuon_muot')) return;
      var st = document.createElement('style');
      st.id = '__cuon_muot';
      st.textContent =
        'html{scroll-behavior:smooth}' +
        '@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}';
      (document.head || document.documentElement).appendChild(st);
    }
    chen();
    setTimeout(chen, 400);
    setTimeout(chen, 1200);
    setTimeout(chen, 2500);
  })();

  /* ---------- Gỡ liên kết chết "Design System ←" ----------
     Bộ soạn thảo để lại một liên kết chân trang trỏ tới
     "Design System 8 Landing Page.dc.html" — file không có trong gói phát
     hành, bấm vào là 404. Đo ngày 11/09/2026: có trên cả 8 trang, hiện rõ
     58x68 px ở chân trang chứ không phải ẩn.

     Nó đứng trong hàng ba liên kết cùng "GitHub ↗" và "Portfolio ↗"; hai cái
     kia trả 200. Gỡ hẳn thay vì giữ lại chữ — một nhãn không dẫn đi đâu nằm
     giữa hàng liên kết thì khó hiểu hơn là không có. */
  (function () {
    function go() {
      var ds = document.querySelectorAll('a[href]');
      for (var i = ds.length - 1; i >= 0; i--) {
        if ((ds[i].getAttribute('href') || '').indexOf('.dc.html') !== -1) {
          ds[i].parentNode.removeChild(ds[i]);
        }
      }
    }
    go();
    setTimeout(go, 700);
    setTimeout(go, 1800);
  })();

  /* ---------- Lưới an toàn cho reveal theo cuộn ----------
     Cả 8 trang đặt .xx-rv{opacity:0} rồi chờ JS gắn .xx-in. Nội dung vì thế
     phụ thuộc vào JS chạy trót lọt. Trang đã chặn trường hợp thiếu
     IntersectionObserver, nhưng không chặn trường hợp IO có mà không bắn, hay
     script chết trước khi gắn observer — khi đó 23-34 khối nằm lại opacity:0
     và trang trông như hỏng. Khung xem trước của tôi đúng là như vậy: có IO,
     không bắn lần nào.

     Lưới chỉ ra tay khi có bằng chứng cơ chế đã chết, chứ không ép hiện hết
     sau vài giây — làm thế là giết luôn hiệu ứng cuộn. */
  (function () {
    var CHO = 3000;

    function danhSach() {
      var ds = document.querySelectorAll('[class*="-rv"]');
      var out = [];
      for (var i = 0; i < ds.length; i++) {
        var m = (ds[i].className || '').match(/(?:^|\s)([a-z]{2,4})-rv(?:\s|$)/);
        if (m) out.push({ el: ds[i], tien: m[1] });
      }
      return out;
    }

    function trongKhungNhin(el) {
      var r = el.getBoundingClientRect();
      var cao = window.innerHeight || document.documentElement.clientHeight || 0;
      if (!cao) return false;
      return r.top < cao && r.bottom > 0 && r.width > 0 && r.height > 0;
    }

    /* chiDoan = chỉ chẩn đoán, không sửa gì. */
    function kiem(chiDoan) {
      var ds = danhSach();
      if (!ds.length) return 'khong-co';

      var daHien = false;
      for (var i = 0; i < ds.length; i++) {
        if (ds[i].el.classList.contains(ds[i].tien + '-in')) { daHien = true; break; }
      }
      if (daHien) return 'dang-chay';   /* cơ chế đang chạy, không đụng vào */

      var coTrongKhung = false;
      for (var j = 0; j < ds.length; j++) {
        if (trongKhungNhin(ds[j].el)) { coTrongKhung = true; break; }
      }
      if (!coTrongKhung) return 'chua-cuon-toi';

      if (chiDoan) return 'hong';

      /* Có phần tử nằm trong khung nhìn mà vẫn chưa được hiện -> cơ chế hỏng. */
      for (var k = 0; k < ds.length; k++) {
        ds[k].el.classList.add(ds[k].tien + '-in');
      }
      if (window.console && console.warn) {
        console.warn('[shim] reveal theo cuộn không chạy — đã hiện ' + ds.length +
                     ' khối nội dung để trang không bị trắng.');
      }
    }

    /* Xác nhận hai nhịp. Trang nặng 350-660 KB và phải hydrate React; trên
       máy yếu 3 giây có thể chưa đủ. Bắn nhầm thì mất hiệu ứng cuộn, nên
       chỉ ra tay khi lần kiểm thứ hai vẫn thấy hỏng. Trường hợp hỏng thật
       thì nội dung vốn đã vô hình, chờ thêm 2 giây không mất gì. */
    setTimeout(function () {
      if (kiem(true) !== 'hong') return;
      setTimeout(function () {
        if (kiem(true) === 'hong') kiem();
      }, 2000);
    }, CHO);
  })();

  /* ---------- Nâng tương phản cho nhãn số thứ tự ----------
     Đo ngày 10/09/2026 trên seosona-os: 5 số 01-05 cỡ 30px, rgb(36,26,61)
     trên nền rgb(22,15,41) = 1.14:1, gần như vô hình. Mục đó tên là "Năm
     năng lực, xếp theo thứ tự chúng chạy" nên con số mang thông tin thật,
     không phải hoạ tiết.
     Giữ nguyên hue va do bao hoa, chi nang do sang toi khi dat 3:1 (nguong
     AA cho chu lon). Chi dung toi nhan hai chu so dang khong dat. */
  (function () {
    function soRGB(s) {
      var m = (s || '').match(/[\d.]+/g);
      return m ? m.slice(0, 3).map(Number) : null;
    }
    function sang(c) {
      var f = c.map(function (v) {
        v /= 255;
        return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
      });
      return 0.2126 * f[0] + 0.7152 * f[1] + 0.0722 * f[2];
    }
    function tyLe(a, b) {
      var x = sang(a), y = sang(b);
      return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05);
    }
    function nenCua(el) {
      var e = el;
      while (e) {
        var cs = getComputedStyle(e);
        if (cs.backgroundImage && cs.backgroundImage !== 'none') return null;
        var p = soRGB(cs.backgroundColor);
        if (p && cs.backgroundColor.indexOf('rgba(0, 0, 0, 0)') === -1 &&
            cs.backgroundColor !== 'transparent') return p;
        e = e.parentElement;
      }
      return [255, 255, 255];
    }
    /* RGB -> HSL -> RGB, chỉ để đổi mỗi độ sáng. */
    function rgb2hsl(c) {
      var r = c[0] / 255, g = c[1] / 255, b = c[2] / 255;
      var mx = Math.max(r, g, b), mn = Math.min(r, g, b), d = mx - mn;
      var l = (mx + mn) / 2, h = 0, s = 0;
      if (d) {
        s = l > 0.5 ? d / (2 - mx - mn) : d / (mx + mn);
        h = mx === r ? (g - b) / d + (g < b ? 6 : 0)
          : mx === g ? (b - r) / d + 2 : (r - g) / d + 4;
        h /= 6;
      }
      return [h, s, l];
    }
    function hsl2rgb(h, s, l) {
      function q(p, q2, t) {
        if (t < 0) t += 1;
        if (t > 1) t -= 1;
        if (t < 1 / 6) return p + (q2 - p) * 6 * t;
        if (t < 1 / 2) return q2;
        if (t < 2 / 3) return p + (q2 - p) * (2 / 3 - t) * 6;
        return p;
      }
      if (!s) { var v = Math.round(l * 255); return [v, v, v]; }
      var b2 = l < 0.5 ? l * (1 + s) : l + s - l * s, a2 = 2 * l - b2;
      return [q(a2, b2, h + 1 / 3), q(a2, b2, h), q(a2, b2, h - 1 / 3)]
        .map(function (v) { return Math.round(v * 255); });
    }

    function sua() {
      var ds = document.querySelectorAll('body *');
      for (var i = 0; i < ds.length; i++) {
        var el = ds[i];
        if (el.children.length) continue;
        var t = (el.textContent || '').trim();
        if (!/^\d{2}$/.test(t)) continue;              /* chỉ nhãn hai chữ số */
        if (el.dataset.tuongPhanDaSua) continue;

        var cs = getComputedStyle(el);
        var fg = soRGB(cs.color), nen = nenCua(el);
        if (!fg || !nen) continue;
        var co = parseFloat(cs.fontSize) || 16;
        var dam = parseInt(cs.fontWeight, 10) || 400;
        var can = (co >= 24 || (co >= 18.66 && dam >= 700)) ? 3 : 4.5;
        if (tyLe(fg, nen) >= can) continue;

        /* Nền tối thì kéo sáng lên, nền sáng thì kéo tối xuống. */
        var hsl = rgb2hsl(fg), toi = sang(nen) < 0.18;
        var lo = hsl[2], hi = toi ? 1 : 0, moi = null;
        for (var k = 0; k < 30; k++) {
          var mid = (lo + hi) / 2;
          var thu = hsl2rgb(hsl[0], hsl[1], mid);
          if (tyLe(thu, nen) < can + 0.05) { lo = mid; } else { hi = mid; moi = thu; }
        }
        if (!moi) continue;
        el.style.setProperty('color', 'rgb(' + moi.join(',') + ')', 'important');
        el.dataset.tuongPhanDaSua = '1';
      }
    }

    sua();
    setTimeout(sua, 800);
    setTimeout(sua, 1900);
  })();

  /* ---------- Gỡ nút đổi ngôn ngữ VI/EN ----------
     Đo trên 4 trang: bấm EN không đổi một chữ. Không có [data-i18n], không hàm
     i18n, và không có nội dung tiếng Anh ở đâu — 0 khối ẩn, 0 template, 0 dấu
     vết trong window.__resources. Nút lại đặt aria-pressed nên hứa với trình
     đọc màn hình rằng nó dùng được.
     Đặt lại thành false khi đã có bản tiếng Anh thật. */
  var GO_BO_NUT_NGON_NGU = true;

  (function () {
    if (!GO_BO_NUT_NGON_NGU) return;

    function isLangBtn(el) {
      var t = (el.textContent || '').trim();
      return (t === 'VI' || t === 'EN') && el.children.length === 0;
    }

    function strip() {
      var btns = [].slice.call(document.querySelectorAll('button, a'))
        .filter(isLangBtn);
      if (btns.length < 2) return;

      /* Gỡ cả khung bọc nếu khung đó chỉ chứa đúng mấy nút này — để không
         chừa lại một ô trống trong thanh điều hướng. */
      var parent = btns[0].parentElement;
      if (parent && parent.children.length === btns.length &&
          [].every.call(parent.children, isLangBtn)) {
        parent.remove();
      } else {
        btns.forEach(function (b) { b.remove(); });
      }
    }

    strip();
    setTimeout(strip, 600);
    setTimeout(strip, 1700);
  })();

  /* ---------- Nút lên đầu trang + nới khối giảm chuyển động ----------
     HTML và CSS thật nằm trong khối đã nén nên không sửa trực tiếp được; chèn
     ở đây vì shim chạy sau khi bộ giải nén thay thẻ <html>. */
  (function () {
    var CSS =
      '#__totop{position:fixed;right:18px;bottom:18px;z-index:9999;' +
      'width:46px;height:46px;display:grid;place-items:center;cursor:pointer;' +
      'border-radius:999px;border:1px solid;' +
      '-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);' +
      'opacity:0;transform:translateY(12px) scale(.9);pointer-events:none;' +
      'transition:opacity .28s cubic-bezier(.16,1,.3,1),' +
      'transform .28s cubic-bezier(.16,1,.3,1),border-color .2s}' +
      '#__totop.on{opacity:1;transform:none;pointer-events:auto}' +
      '#__totop:hover{transform:translateY(-3px)}' +
      '#__totop:active{transform:translateY(-1px) scale(.94)}' +
      '#__totop svg{width:20px;height:20px;display:block}' +
      '@media (max-width:640px){#__totop{right:12px;bottom:12px}}' +
      /* Giữ phản hồi hover/focus khi hệ điều hành bật giảm chuyển động.
         Chuẩn chỉ đòi bỏ thứ gây chóng mặt, không đòi bỏ hết phản hồi. */
      '@media (prefers-reduced-motion:reduce){' +
      'a,button,summary,label,input,select,textarea,[role=button],[tabindex],' +
      '[class*=btn],[class*=card],[class*=chip],[class*=tile]{' +
      'transition-duration:.12s!important}' +
      '#__totop{transition-duration:.12s!important}}';

    function injectCss() {
      if (document.getElementById('__totop_css') || !document.head) return;
      var st = document.createElement('style');
      st.id = '__totop_css';
      st.textContent = CSS;
      document.head.appendChild(st);
    }

    /* Màu nút phải tính từ nền thật. KHÔNG dùng color:inherit — <body> của các
       trang này để màu chữ mặc định là đen, màu thật nằm ở phần tử con, nên
       thừa hưởng sẽ ra mũi tên đen trên nền tối. */
    function pageBg() {
      var el = document.body;
      while (el) {
        var c = getComputedStyle(el).backgroundColor;
        if (c && c.indexOf('rgba(0, 0, 0, 0)') === -1 && c !== 'transparent') return c;
        el = el.parentElement;
      }
      return 'rgb(255,255,255)';
    }

    function isDark(c) {
      var m = (c.match(/[\d.]+/g) || [255, 255, 255]).map(Number);
      var f = m.slice(0, 3).map(function (v) {
        v /= 255;
        return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
      });
      return (0.2126 * f[0] + 0.7152 * f[1] + 0.0722 * f[2]) < 0.35;
    }

    function paint(b) {
      var dark = isDark(pageBg());
      b.style.color = dark ? '#f4f7f6' : '#14181c';
      b.style.background = dark ? 'rgba(255,255,255,.10)' : 'rgba(0,0,0,.055)';
      b.style.borderColor = dark ? 'rgba(255,255,255,.30)' : 'rgba(0,0,0,.20)';
    }

    function build() {
      if (document.getElementById('__totop') || !document.body) return;
      var b = document.createElement('button');
      b.id = '__totop';
      b.type = 'button';
      b.setAttribute('aria-label', 'Lên đầu trang');
      b.setAttribute('title', 'Lên đầu trang');
      b.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" ' +
        'aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>';
      paint(b);

      b.addEventListener('click', function () {
        var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
        window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
        var h = document.querySelector('h1');
        if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
      });
      document.body.appendChild(b);

      /* Một classList.toggle quá rẻ để cần tiết lưu, mà requestAnimationFrame
         lại thêm một chỗ có thể không chạy. Đọc vị trí theo ba cách vì trình
         duyệt cũ đặt scrollTop ở nơi khác. */
      function pos() {
        return window.scrollY || document.documentElement.scrollTop ||
               document.body.scrollTop || 0;
      }
      function onScroll() { b.classList.toggle('on', pos() > 600); }
      addEventListener('scroll', onScroll, { passive: true });
      addEventListener('resize', onScroll, { passive: true });
      onScroll();

      /* SEOSONA UX-UI có công tắc sáng/tối — tính lại màu khi chủ đề đổi. */
      try {
        new MutationObserver(function () { paint(b); }).observe(
          document.documentElement, { attributes: true,
            attributeFilter: ['class', 'data-theme', 'style'] });
      } catch (e) {}
    }

    function go() { injectCss(); build(); }
    go();
    /* Bộ giải nén có thể xong sau shim — chạy lại cho chắc. */
    setTimeout(go, 500);
    setTimeout(go, 1600);
  })();

  /* ---------- Trạng thái deployment nhìn thấy được ----------
     Footer cũ chỉ ghi một dòng sau khi gọi API, không cho biết trang đang
     kiểm tra gì và cũng không có retry. Flow là một landing page động: health
     snapshot phải hiện ngay gần workflow, nhưng không giả vờ đây là trạng thái
     live của các node AI. Chỉ endpoint deployment được kiểm tra; không mở
     WebSocket/SSE và không tự ý chạy pipeline. */
  (function () {
    return;
    var ID = '__flow_health_strip';
    var CSS =
      '#' + ID + '{max-width:1180px;margin:0 auto 22px;padding:0 24px;position:relative;z-index:4}' +
      '#' + ID + ' .fh-shell{display:flex;align-items:center;gap:12px;min-height:42px;padding:9px 12px;border:1px solid #1C3149;border-radius:8px;background:rgba(6,11,20,.88);color:#9FB6CE;font:12px/1.4 Archivo,system-ui,sans-serif}' +
      '#' + ID + ' .fh-dot{width:8px;height:8px;flex:0 0 8px;border-radius:50%;background:#F59E0B;box-shadow:0 0 0 4px rgba(245,158,11,.12)}' +
      '#' + ID + '[data-state=online] .fh-dot{background:#2DD4BF;box-shadow:0 0 0 4px rgba(45,212,191,.12)}' +
      '#' + ID + '[data-state=offline] .fh-dot{background:#FB7185;box-shadow:0 0 0 4px rgba(251,113,133,.12)}' +
      '#' + ID + ' .fh-copy{min-width:0;flex:1}' +
      '#' + ID + ' .fh-title{display:block;color:#EAF4FF;font:600 10px/1.2 "JetBrains Mono",ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase}' +
      '#' + ID + ' .fh-detail{display:block;margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}' +
      '#' + ID + ' .fh-retry{border:1px solid #36516E;border-radius:999px;padding:6px 10px;background:transparent;color:#EAF4FF;font:600 11px/1.2 Archivo,system-ui,sans-serif;cursor:pointer}' +
      '#' + ID + ' .fh-retry:hover,#' + ID + ' .fh-retry:focus-visible{border-color:#22D3EE;color:#22D3EE;outline:0}' +
      '@media (max-width:640px){#' + ID + '{padding:0 16px;margin-bottom:16px}#' + ID + ' .fh-shell{align-items:flex-start}#' + ID + ' .fh-detail{white-space:normal;overflow:visible;text-overflow:clip;overflow-wrap:anywhere}#' + ID + ' .fh-retry{flex:0 0 auto}}' +
      '@media (prefers-reduced-motion:reduce){#' + ID + ' .fh-dot{box-shadow:none}#' + ID + ' .fh-retry{transition:none}}';

    function style() {
      if (!document.head || document.getElementById(ID + '_css')) return;
      var st = document.createElement('style');
      st.id = ID + '_css';
      st.textContent = CSS;
      document.head.appendChild(st);
    }

    function build() {
      if (!document.body || document.getElementById(ID)) return document.getElementById(ID);
      var root = document.createElement('aside');
      root.id = ID;
      root.dataset.state = 'loading';
      root.setAttribute('aria-label', 'Trạng thái deployment của SEOSONA Flow');
      root.innerHTML = '<div class="fh-shell"><span class="fh-dot" aria-hidden="true"></span>' +
        '<span class="fh-copy"><span class="fh-title">Deployment health</span>' +
        '<span class="fh-detail" data-health-detail>Đang kiểm tra deployment…</span></span>' +
        '<button class="fh-retry" type="button" data-health-retry>Thử lại</button></div>';
      var main = document.querySelector('main');
      if (main) main.insertBefore(root, main.firstChild);
      else document.body.insertBefore(root, document.body.firstChild);
      root.querySelector('[data-health-retry]').addEventListener('click', probe);
      return root;
    }

    function setState(state, detail) {
      var root = build();
      if (!root) return;
      root.dataset.state = state;
      var out = root.querySelector('[data-health-detail]');
      if (out) out.textContent = detail;
    }

    var timer = 0;
    var busy = false;
    function schedule() {
      clearTimeout(timer);
      timer = setTimeout(probe, 45000);
    }

    function probe() {
      if (document.hidden || (navigator.connection && navigator.connection.saveData)) {
        schedule();
        return;
      }
      if (busy) return;
      busy = true;
      setState('loading', 'Đang kiểm tra deployment…');
      var ctl = typeof AbortController === 'function' ? new AbortController() : null;
      var timeout = setTimeout(function () { if (ctl) ctl.abort(); }, 3500);
      fetch('/api/health', {
        cache: 'no-store',
        headers: { Accept: 'application/json' },
        signal: ctl ? ctl.signal : undefined
      })
        .then(function (r) {
          if (!r.ok) throw new Error('HTTP ' + r.status);
          return r.json();
        })
        .then(function (data) {
          if (!data || data.ok !== true) throw new Error('health response không hợp lệ');
          var sha = data.commit ? String(data.commit).slice(0, 7) : 'local';
          var region = data.region || 'region chưa công bố';
          setState('online', 'Online · commit ' + sha + ' · ' + region + ' · snapshot ' + (data.at || 'vừa xong'));
        })
        .catch(function (err) {
          var reason = err && err.name === 'AbortError' ? 'timeout' : 'không kết nối được';
          setState('offline', 'Chưa đọc được deployment health · ' + reason + ' · thử lại sau');
        })
        .then(function () {
          clearTimeout(timeout);
          busy = false;
          schedule();
        });
    }

    function start() {
      style();
      build();
      probe();
      // Bundled pages thay cả documentElement; head có thể xuất hiện sau lần
      // gọi đầu tiên nên thử lại giống các enhancement khác trong shim.
      setTimeout(style, 500);
      setTimeout(style, 1600);
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
    else start();
    document.addEventListener('visibilitychange', function () { if (!document.hidden) probe(); });
  })();

  /* ---------- Fallback có nghĩa cho canvas WebGL ----------
     Graph 3D là lớp hình ảnh chính của Flow, nhưng canvas tự nó không có
     nhãn đọc được và lỗi context trước đây chỉ làm mất hero. Giữ canvas là
     surface tương tác, thêm mô tả DOM và bật ordered list khi stage ẩn canvas. */
  (function () {
    var ID = '__flow_graph_fallback';
    var BUTTON_ID = '__flow_graph_pause';
    var DESC = 'Mạng workflow 3D: ba nguồn đầu vào đi qua node xử lý ở giữa rồi tỏa ra ba đích kết quả.';

    function showFallback(canvas, list) {
      if (!list) return;
      var control = document.getElementById(BUTTON_ID);
      if (control) control.hidden = true;
      list.hidden = false;
      list.removeAttribute('aria-hidden');
      if (canvas) canvas.setAttribute('aria-hidden', 'true');
    }

    function motionControl(canvas) {
      var host = canvas && canvas.parentElement;
      if (!host) return;
      canvas.id = canvas.id || 'flow-webgl-canvas';
      var button = document.getElementById(BUTTON_ID);
      if (!button) {
        button = document.createElement('button');
        button.id = BUTTON_ID;
        button.type = 'button';
        button.hidden = true;
        button.setAttribute('aria-controls', canvas.id);
        button.setAttribute('aria-pressed', 'false');
        button.setAttribute('aria-label', 'Tạm dừng chuyển động của sơ đồ');
        button.textContent = 'Tạm dừng chuyển động';
        button.style.cssText = 'position:absolute;top:12px;right:12px;z-index:6;min-height:34px;padding:7px 10px;border:1px solid #36516E;border-radius:999px;background:rgba(6,11,20,.9);color:#EAF4FF;font:600 11px/1.2 Archivo,system-ui,sans-serif;cursor:pointer';
        button.addEventListener('click', function () {
          var paused = button.getAttribute('aria-pressed') !== 'true';
          button.setAttribute('aria-pressed', paused ? 'true' : 'false');
          button.textContent = paused ? 'Tiếp tục chuyển động' : 'Tạm dừng chuyển động';
          button.setAttribute('aria-label', paused ? 'Tiếp tục chuyển động của sơ đồ' : 'Tạm dừng chuyển động của sơ đồ');
          var stage = canvas.__flowStage;
          if (stage && stage.setPaused) stage.setPaused(paused);
        });
        host.appendChild(button);
      }

      var attempts = 0;
      function sync() {
        var stage = canvas.__flowStage;
        if (!stage) {
          if (++attempts < 35) setTimeout(sync, 100);
          return;
        }
        button.hidden = false;
        if (stage.quality === 'static') {
          button.disabled = true;
          button.textContent = 'Chuyển động tĩnh';
          button.setAttribute('aria-label', 'Sơ đồ đang ở chế độ tĩnh');
          return;
        }
        stage.setPaused(button.getAttribute('aria-pressed') === 'true');
      }
      sync();
    }

    function prepare() {
      var canvas = document.querySelector('[data-gl-hero]');
      if (!canvas || !canvas.parentElement) return;
      canvas.setAttribute('role', 'img');
      canvas.setAttribute('aria-label', DESC);
      canvas.style.maxWidth = '100%';
      canvas.parentElement.style.maxWidth = '100%';
      canvas.parentElement.style.overflow = 'hidden';
      motionControl(canvas);

      var list = document.getElementById(ID);
      if (!list) {
        list = document.createElement('ol');
        list.id = ID;
        list.hidden = true;
        list.setAttribute('aria-hidden', 'true');
        list.setAttribute('aria-label', 'Fallback workflow graph');
        list.innerHTML = '<li><strong>Input · 6 node</strong> · prompt, ảnh tham chiếu và tham số</li>' +
          '<li><strong>Transform · 7 node</strong> · image-to-prompt, aspect và crop</li>' +
          '<li><strong>Generate · 8 node</strong> · ảnh, video và seed</li>' +
          '<li><strong>Export · 5 node</strong> · save, naming và library</li>' +
          '<li><strong>Store · 0 node</strong> · kho prompt hiện chưa nối vào workflow</li>';
        canvas.parentElement.appendChild(list);
        canvas.addEventListener('webglcontextlost', function () { showFallback(canvas, list); }, { passive: true });
      }

      if (getComputedStyle(canvas).display === 'none' || canvas.width === 0) showFallback(canvas, list);
      if (!canvas.dataset.flowFallbackObserved) {
        canvas.dataset.flowFallbackObserved = '1';
        try {
          new MutationObserver(function () {
            if (getComputedStyle(canvas).display === 'none' || canvas.width === 0) showFallback(canvas, list);
          }).observe(canvas, { attributes: true, attributeFilter: ['style', 'width', 'height'] });
        } catch (e) {}
      }
    }

    prepare();
    setTimeout(prepare, 700);
    setTimeout(prepare, 1800);
  })();

  /* ---------- Navigator DOM cho workflow ----------
     Canvas khong phai tap hop node de tab vao; nguoi dung van can mot thu tu
     focus co nghia de di qua cac nhom workflow. Navigator nay luon co trong DOM,
     hien ra khi focus, va tro den card HTML chinh thay vi tao mot graph gia. */
  (function () {
    var ID = '__flow_group_nav';
    var CSS_ID = ID + '_css';
    var GROUPS = [
      { key: 'Nhận đầu vào', id: 'flow-group-input', label: 'Input · 6 node' },
      { key: 'Biến đổi', id: 'flow-group-transform', label: 'Transform · 7 node' },
      { key: 'Sinh', id: 'flow-group-generate', label: 'Generate · 8 node' },
      { key: 'Xuất', id: 'flow-group-export', label: 'Export · 5 node' },
      { key: 'Kho prompt', id: 'flow-group-store', label: 'Store · 0 node' }
    ];

    function style() {
      if (!document.head || document.getElementById(CSS_ID)) return;
      var st = document.createElement('style');
      st.id = CSS_ID;
      st.textContent =
        '#' + ID + '{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;border:0}' +
        '#' + ID + ':focus-within{position:relative;width:auto;height:auto;margin:0 0 18px;padding:10px;overflow:visible;clip:auto;clip-path:none;white-space:normal;border:1px solid #1C3149;border-radius:8px;background:#0D1A2D}' +
        '#' + ID + ' .fgn-label{display:block;margin-bottom:7px;color:#9FB6CE;font:600 10px/1.2 "JetBrains Mono",ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase}' +
        '#' + ID + ' .fgn-links{display:flex;flex-wrap:wrap;gap:6px}' +
        '#' + ID + ' a{display:inline-flex;align-items:center;min-height:32px;padding:5px 9px;border:1px solid #36516E;border-radius:999px;color:#EAF4FF;font:600 11px/1.2 Archivo,system-ui,sans-serif;text-decoration:none}' +
        '#' + ID + ' a:hover,#' + ID + ' a:focus-visible{border-color:#22D3EE;color:#22D3EE;outline:2px solid #22D3EE;outline-offset:2px}' +
        '@media (prefers-reduced-motion:reduce){#' + ID + ' a{scroll-behavior:auto}}';
      document.head.appendChild(st);
    }

    function wire() {
      style();
      var section = document.getElementById('node');
      if (!section || document.getElementById(ID)) return;
      var headings = section.querySelectorAll('h3');
      var found = [];
      for (var i = 0; i < GROUPS.length; i++) {
        for (var j = 0; j < headings.length; j++) {
          var heading = (headings[j].textContent || '').replace(/\s+/g, ' ').trim();
          if (heading !== GROUPS[i].key) continue;
          var card = headings[j].closest('.fl-rv') || headings[j].parentElement.parentElement;
          if (!card) continue;
          card.id = GROUPS[i].id;
          found.push(GROUPS[i]);
          break;
        }
      }
      if (found.length !== GROUPS.length) return;

      var nav = document.createElement('nav');
      nav.id = ID;
      nav.setAttribute('aria-label', 'Đi tới nhóm workflow');
      nav.innerHTML = '<span class="fgn-label">Workflow groups · keyboard navigation</span><span class="fgn-links"></span>';
      var links = nav.querySelector('.fgn-links');
      found.forEach(function (group) {
        var link = document.createElement('a');
        link.href = '#' + group.id;
        link.textContent = group.label;
        link.setAttribute('aria-label', 'Đi tới ' + group.label);
        links.appendChild(link);
      });
      section.appendChild(nav);
    }

    wire();
    setTimeout(wire, 700);
    setTimeout(wire, 1800);
    setTimeout(style, 500);
    setTimeout(style, 1600);
  })();

  /* ---------- Interaction states cho mockup ----------
     Side panel va Image-to-Prompt la HTML/CSS fixture, khong phai extension
     dang chay. Bien cac nhan trang tri thanh control semantic khi JS san sang
     de mockup co selected/loading/error state ma van giu duong doc khong-JS. */
  (function () {
    var CSS_ID = '__flow_mockup_css';
    var WIRED = 'flowMockupWired';

    function style() {
      if (!document.head || document.getElementById(CSS_ID)) return;
      var st = document.createElement('style');
      st.id = CSS_ID;
      st.textContent =
        '[data-flow-ratio]{cursor:pointer;background:#0D1A2D!important;color:#EAF4FF!important;border-color:#36516E!important;transition:background 150ms ease,color 150ms ease,border-color 150ms ease}' +
        '[data-flow-ratio][aria-pressed="true"]{background:#22D3EE!important;border-color:#22D3EE!important;color:#060B14!important}' +
        '[data-flow-ratio]:focus-visible,[data-flow-generate]:focus-visible,[data-flow-copy]:focus-visible{outline:2px solid #22D3EE;outline-offset:3px}' +
        '[data-flow-generate][data-flow-state="loading"]{opacity:.7;cursor:wait}' +
        '[data-flow-generate][data-flow-state="ready"]{box-shadow:0 0 0 3px rgba(45,212,191,.15)}' +
        '[data-flow-copy]{display:inline-flex;align-items:center;justify-content:center;min-height:34px;margin-top:12px;padding:7px 11px;border:1px solid #36516E;border-radius:6px;background:transparent;color:#EAF4FF;font:600 11px/1.2 Archivo,system-ui,sans-serif;cursor:pointer}' +
        '[data-flow-copy]:hover{border-color:#22D3EE;color:#22D3EE}' +
        '[data-flow-status]{display:block;min-height:17px;margin:8px 0 0;color:#7591AD;font:11px/1.45 Archivo,system-ui,sans-serif;overflow-wrap:anywhere}' +
        '[data-flow-status][data-flow-state="success"]{color:#2DD4BF}' +
        '[data-flow-status][data-flow-state="error"]{color:#FB7185}' +
        '@media (prefers-reduced-motion:reduce){[data-flow-ratio],[data-flow-copy]{transition:none}}';
      document.head.appendChild(st);
    }

    function text(el) {
      return (el && el.textContent ? el.textContent : '').replace(/\s+/g, ' ').trim();
    }

    function replaceWithButton(el, label) {
      if (!el || el.tagName === 'BUTTON') return el;
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.innerHTML = el.innerHTML;
      btn.setAttribute('style', el.getAttribute('style') || '');
      btn.className = el.className || '';
      btn.setAttribute('aria-label', label);
      el.parentNode.replaceChild(btn, el);
      return btn;
    }

    function status(host, initial) {
      var out = host.querySelector('[data-flow-status]');
      if (out) return out;
      out = document.createElement('p');
      out.setAttribute('data-flow-status', '');
      out.setAttribute('role', 'status');
      out.setAttribute('aria-live', 'polite');
      out.textContent = initial || '';
      host.appendChild(out);
      return out;
    }

    function wireSidePanel() {
      var candidates = document.querySelectorAll('div');
      var generate = null;
      for (var i = 0; i < candidates.length; i++) {
        if (text(candidates[i]) === 'Sinh ảnh' && candidates[i].children.length === 0) {
          generate = replaceWithButton(candidates[i], 'Sinh ảnh — demo fixture');
          break;
        }
      }
      if (!generate) return;

      var host = generate.parentElement;
      if (!host || host.dataset[WIRED]) return;
      host.dataset[WIRED] = '1';
      generate.dataset.flowGenerate = '';
      generate.dataset.flowState = 'idle';
      generate.setAttribute('aria-describedby', '__flow_side_status');

      var ratioHost = null;
      var ratioCandidates = host.querySelectorAll('span,button');
      var ratioButtons = [];
      for (var r = 0; r < ratioCandidates.length; r++) {
        var label = text(ratioCandidates[r]);
        if (label !== '1:1' && label !== '4:5' && label !== '16:9') continue;
        var ratio = replaceWithButton(ratioCandidates[r], 'Tỷ lệ ' + label);
        ratio.dataset.flowRatio = label;
        ratio.setAttribute('aria-pressed', label === '1:1' ? 'true' : 'false');
        ratioButtons.push(ratio);
        ratioHost = ratio.parentElement;
      }
      if (ratioHost && ratioButtons.length) {
        ratioHost.setAttribute('role', 'group');
        ratioHost.setAttribute('aria-label', 'Chọn tỷ lệ khung hình');
        ratioButtons.forEach(function (ratio) {
          ratio.addEventListener('click', function () {
            ratioButtons.forEach(function (other) { other.setAttribute('aria-pressed', other === ratio ? 'true' : 'false'); });
            generate.dataset.selectedRatio = ratio.dataset.flowRatio;
            var out = status(host, 'Demo fixture · chưa chạy extension thật.');
            out.id = '__flow_side_status';
            out.dataset.flowState = 'success';
            out.textContent = 'Đã chọn tỷ lệ ' + ratio.dataset.flowRatio + ' cho demo fixture.';
          });
        });
      }

      var out = status(host, 'Demo fixture · chưa chạy extension thật.');
      out.id = '__flow_side_status';
      generate.addEventListener('click', function () {
        if (generate.disabled) return;
        var ratio = generate.dataset.selectedRatio || '1:1';
        generate.disabled = true;
        generate.dataset.flowState = 'loading';
        generate.textContent = 'Đang xếp…';
        out.dataset.flowState = 'loading';
        out.textContent = 'Đang xếp prompt vào hàng đợi demo…';
        window.setTimeout(function () {
          generate.disabled = false;
          generate.dataset.flowState = 'ready';
          generate.textContent = 'Sinh ảnh';
          out.dataset.flowState = 'success';
          out.textContent = 'Demo fixture · prompt đã xếp vào hàng đợi với tỷ lệ ' + ratio + '.';
        }, 650);
      });
    }

    function wireCopy() {
      var section = document.getElementById('i2p');
      if (!section || section.dataset.flowCopyWired) return;
      var paragraphs = section.querySelectorAll('p');
      var prompt = null;
      for (var i = paragraphs.length - 1; i >= 0; i--) {
        if (text(paragraphs[i]).length > 90) { prompt = paragraphs[i]; break; }
      }
      if (!prompt || !prompt.parentElement) return;
      section.dataset.flowCopyWired = '1';
      var host = prompt.parentElement;
      var button = document.createElement('button');
      button.type = 'button';
      button.dataset.flowCopy = '';
      button.textContent = 'Copy prompt';
      button.setAttribute('aria-label', 'Copy prompt Image-to-Prompt');
      host.appendChild(button);
      var out = status(host, 'Prompt trong fixture · có thể copy để thử flow.');
      button.addEventListener('click', function () {
        var value = text(prompt);
        if (!value) {
          out.dataset.flowState = 'error';
          out.textContent = 'Không có prompt để copy.';
          return;
        }
        var write = navigator.clipboard && navigator.clipboard.writeText
          ? navigator.clipboard.writeText(value)
          : Promise.reject(new Error('clipboard unavailable'));
        write.then(function () {
          out.dataset.flowState = 'success';
          out.textContent = 'Đã copy prompt từ demo fixture.';
        }).catch(function () {
          out.dataset.flowState = 'error';
          out.textContent = 'Không copy được trong ngữ cảnh này. Hãy chọn và copy prompt thủ công.';
        });
      });
    }

    function wire() {
      style();
      wireSidePanel();
      wireCopy();
    }

    wire();
    setTimeout(wire, 700);
    setTimeout(wire, 1800);
    setTimeout(style, 500);
    setTimeout(style, 1600);
  })();

  /* --- Gắn lại metadata sau khi bộ giải nén thay cả thẻ <html> ---
     Bộ giải nén gọi document.documentElement.replaceWith(), nên mọi thẻ trong
     <head> của lớp bọc bị xoá sạch: title thành rỗng, mất lang, mất canonical,
     mất og:*. Bộ quét của Facebook/Zalo không chạy JS nên chúng đọc lớp bọc
     tĩnh (đã vá riêng); đoạn này lo cho trình duyệt và thanh tiêu đề. */
  var META = {"title": "SEOSONA Flow — Chrome extension sinh ảnh và video AI", "description": "Chrome extension tạo ảnh và video AI hàng loạt trên Google Flow, ChatGPT, Gemini, Grok. 26 loại node workflow, không cần API key.", "url": "https://seosona-flow.vercel.app", "image": "https://seosona-flow.vercel.app/cover.jpg"};

  function setMeta(sel, attr, key, val) {
    var el = document.head.querySelector(sel);
    if (!el) {
      el = document.createElement('meta');
      el.setAttribute(attr, key);
      document.head.appendChild(el);
    }
    el.setAttribute('content', val);
  }

  function restoreHead() {
    if (!document.head) return;
    if (document.title !== META.title) document.title = META.title;
    document.documentElement.lang = 'vi';
    setMeta('meta[name="description"]', 'name', 'description', META.description);
    setMeta('meta[property="og:title"]', 'property', 'og:title', META.title);
    setMeta('meta[property="og:description"]', 'property', 'og:description', META.description);
    setMeta('meta[property="og:url"]', 'property', 'og:url', META.url);
    setMeta('meta[property="og:image"]', 'property', 'og:image', META.image);
    setMeta('meta[property="og:type"]', 'property', 'og:type', 'website');
    setMeta('meta[name="twitter:card"]', 'name', 'twitter:card', 'summary_large_image');
    setMeta('meta[name="twitter:title"]', 'name', 'twitter:title', META.title);
    setMeta('meta[name="twitter:image"]', 'name', 'twitter:image', META.image);
    var c = document.head.querySelector('link[rel="canonical"]');
    if (!c) {
      c = document.createElement('link');
      c.rel = 'canonical';
      document.head.appendChild(c);
    }
    c.href = META.url + '/';
  }

  restoreHead();
  /* Giải nén có thể xong sau shim — chạy lại cho chắc. */
  setTimeout(restoreHead, 400);
  setTimeout(restoreHead, 1500);
  var ENDPOINT = '/api/lead';

  function wireSemanticContracts() {
    var headings = document.getElementsByTagName('h3');
    var index = 0;
    for (var i = 0; i < headings.length; i++) {
      var button = headings[i].firstElementChild;
      if (!button || button.tagName !== 'BUTTON' || !button.hasAttribute('aria-expanded')) continue;
      var answer = headings[i].nextElementSibling;
      if (!answer) continue;
      index += 1;
      var buttonId = 'flow-faq-question-' + index;
      var answerId = 'flow-faq-answer-' + index;
      button.id = buttonId;
      button.setAttribute('aria-controls', answerId);
      answer.id = answerId;
      answer.setAttribute('role', 'region');
      answer.setAttribute('aria-labelledby', buttonId);
      answer.setAttribute('aria-hidden', button.getAttribute('aria-expanded') !== 'true' ? 'true' : 'false');
    }
  }

  function observeSemanticContracts() {
    if (window.__flowSemanticsObserved || !document) return;
    window.__flowSemanticsObserved = true;
    var observer = new MutationObserver(function () { wireAll(); wireSemanticContracts(); });
    observer.observe(document, { childList: true, subtree: true, attributes: true, attributeFilter: ['aria-expanded'] });
    document.addEventListener('click', function (event) {
      var node = event.target;
      while (node && node !== document) {
        if (node.tagName === 'BUTTON' && node.hasAttribute('aria-expanded')) {
          setTimeout(wireSemanticContracts, 0);
          break;
        }
        node = node.parentElement;
      }
    }, true);
    wireSemanticContracts();
  }


  function findInput(form) {
    return form.querySelector('input[type=email], input[type=tel], input[type=text]');
  }

  function statusEl(form) {
    var p = form.querySelector('[aria-live]');
    if (p) return p;
    p = document.createElement('p');
    p.setAttribute('aria-live', 'polite');
    p.style.cssText = 'font-size:12px;margin:6px 0 0;min-height:17px';
    form.appendChild(p);
    return p;
  }

  function wire(form) {
    var btn = form.querySelector('button[type=submit], button:not([type])');
    var input = findInput(form);
    if (!input) return;
    var out = statusEl(form);
    if (!out.id) out.id = 'flow-lead-status';
    input.required = true;
    input.setAttribute('required', '');
    input.setAttribute('autocomplete', input.type === 'email' ? 'email' : 'tel');
    input.setAttribute('aria-describedby', out.id);
    if (form.dataset.wired) return;
    form.dataset.wired = '1';

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      e.stopPropagation();
      var value = (input.value || '').trim();
      if (!value) { out.textContent = 'Chưa nhập ' + (input.type === 'tel' ? 'số điện thoại' : 'email'); return; }

      var label = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Đang gửi…'; }
      out.textContent = '';

      fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ value: value, note: document.title })
      })
        .then(function (r) { return r.json().then(function (j) { return { status: r.status, body: j }; }); })
        .then(function (r) {
          if (r.body && r.body.ok) {
            out.textContent = r.body.message + ' (mã ' + r.body.id + ')';
            input.value = '';
          } else {
            out.textContent = (r.body && r.body.error) || 'Gửi không thành công. Thử lại sau.';
          }
        })
        .catch(function () {
          out.textContent = 'Không nối được máy chủ. Kiểm tra mạng rồi thử lại.';
        })
        .then(function () {
          if (btn) { btn.disabled = false; btn.textContent = label; }
        });
    }, true);
  }

  function wireAll() {
    var forms = document.querySelectorAll('form');
    for (var i = 0; i < forms.length; i++) wire(forms[i]);
    observeSemanticContracts();
    wireSemanticContracts();
  }

  function stampFooter() {}

  function mountRedesign() {
    document.documentElement.classList.add('flow-redesign');
    if (!document.head || document.getElementById('__flow_redesign_css')) return;
    var link = document.createElement('link');
    link.id = '__flow_redesign_css';
    link.rel = 'stylesheet';
    link.href = 'redesign.css?v=20261017-3';
    document.head.appendChild(link);
  }

  function observeHydration() {
    if (window.__flowRedesignHydrationObserved || !window.MutationObserver) return;
    window.__flowRedesignHydrationObserved = true;
    new MutationObserver(function () {
      if (!document.documentElement ||
          !document.documentElement.classList.contains('flow-redesign') ||
          !document.getElementById('__flow_redesign_css')) {
        mountRedesign();
      }
    }).observe(document, { childList: true });
  }

  function start() {
    mountRedesign();
    observeHydration();
    wireAll();
    stampFooter();
    setTimeout(function () { mountRedesign(); wireAll(); }, 1200);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
