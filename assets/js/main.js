/* PROMYK — skrypty strony */
(function () {
  'use strict';

  /* ---------- menu mobilne ---------- */
  var nav = document.querySelector('.nav');
  var burger = document.querySelector('.nav__burger');
  if (nav && burger) {
    burger.addEventListener('click', function () { nav.classList.toggle('is-open'); });
  }

  /* ---------- slider hero ---------- */
  var hero = document.querySelector('.hero');
  if (hero) {
    var slides = hero.querySelectorAll('.hero__slide');
    var dots = hero.querySelectorAll('.hero__dots span');
    var i = 0, timer = null;

    function show(n) {
      i = (n + slides.length) % slides.length;
      slides.forEach(function (s, k) { s.classList.toggle('is-active', k === i); });
      dots.forEach(function (d, k) { d.classList.toggle('is-active', k === i); });
    }
    function play() { timer = setInterval(function () { show(i + 1); }, 6000); }
    function restart() { clearInterval(timer); play(); }

    dots.forEach(function (d, k) { d.addEventListener('click', function () { show(k); restart(); }); });
    var prev = hero.querySelector('[data-hero="prev"]');
    var next = hero.querySelector('[data-hero="next"]');
    if (prev) prev.addEventListener('click', function () { show(i - 1); restart(); });
    if (next) next.addEventListener('click', function () { show(i + 1); restart(); });
    if (slides.length > 1) play();
  }

  /* ---------- FAQ ---------- */
  document.querySelectorAll('.faq__q').forEach(function (q) {
    q.addEventListener('click', function () {
      var row = q.closest('.faq__row');
      var open = row.classList.contains('is-open');
      row.parentNode.querySelectorAll('.faq__row').forEach(function (r) {
        r.classList.remove('is-open');
        var t = r.querySelector('.faq__q span:last-child');
        if (t) t.textContent = '+';
      });
      if (!open) {
        row.classList.add('is-open');
        q.querySelector('span:last-child').textContent = '–';
      }
    });
  });

  /* ---------- filtry galerii ---------- */
  var filters = document.querySelectorAll('.filter');
  if (filters.length) {
    filters.forEach(function (b) {
      b.addEventListener('click', function () {
        filters.forEach(function (x) { x.classList.remove('is-active'); });
        b.classList.add('is-active');
        var cat = b.getAttribute('data-filter');
        document.querySelectorAll('.gallery [data-cat]').forEach(function (item) {
          var match = cat === 'all' || item.getAttribute('data-cat') === cat;
          // pozycje ukryte pod „Pokaż więcej” zostają ukryte przy filtrze „Wszystkie”
          if (item.classList.contains('is-hidden') && cat === 'all') { item.style.display = 'none'; return; }
          item.style.display = match ? '' : 'none';
        });
        // mniej niż 4 zdjęcia w kategorii — rozciągnij je na cały rząd, żeby nie zostawały „wypierdki”
        var grid = document.querySelector('.gallery');
        var n = Array.prototype.filter.call(grid.children, function (a) { return a.style.display !== 'none'; }).length;
        grid.style.gridTemplateColumns = (n > 0 && n < 4 && window.innerWidth > 900) ? 'repeat(' + n + ', 1fr)' : '';
        var moreBtn = document.querySelector('[data-more]');
        if (moreBtn) moreBtn.style.display = (cat === 'all' && document.querySelector('.gallery .is-hidden')) ? '' : 'none';
      });
    });
  }

  /* ---------- „pokaż więcej” w galerii ---------- */
  var more = document.querySelector('[data-more]');
  if (more) {
    more.addEventListener('click', function () {
      document.querySelectorAll('.gallery .is-hidden').forEach(function (el) {
        el.classList.remove('is-hidden');
        el.style.display = '';
      });
      more.style.display = 'none';
    });
  }

  /* ---------- prefill formularza z konfiguratora ---------- */
  var params = new URLSearchParams(location.search);
  var cfg = params.get('konfiguracja');
  if (cfg) {
    var msg = document.querySelector('#f-msg');
    var cat = document.querySelector('#f-cat');
    if (msg) msg.value = 'Dzień dobry, proszę o wycenę okna wg konfiguracji:\n\n' + cfg + '\n\n';
    if (cat) cat.value = 'Wycena stolarki okiennej';
    if (msg) msg.scrollIntoView({ block: 'center' });
  }

  /* ---------- formularz kontaktowy: komunikat po wysłaniu (kontakt.php) ---------- */
  var sent = params.get('wyslano'), err = params.get('blad');
  var box = document.querySelector('[data-formmsg]');
  if (box && (sent || err)) {
    box.textContent = sent ? 'Dziękujemy! Wiadomość została wysłana — odpowiemy najszybciej, jak to możliwe.'
                           : 'Nie udało się wysłać wiadomości. Sprawdź wymagane pola albo zadzwoń: 607 941 499.';
    box.style.display = 'block';
    box.style.color = sent ? '#1f7a3f' : '#b3261e';
    box.scrollIntoView({ block: 'center' });
  }
})();

// powiększenie zdjęć z galerii — strzałki, klawiatura i przesuwanie palcem (np. „Inspiracje” na podstronie Okna)
document.querySelectorAll('[data-lightbox]').forEach(function (gal) {
  var items = Array.prototype.slice.call(gal.querySelectorAll('[data-lightbox-item]'));
  if (!items.length) return;
  var box = document.createElement('div');
  box.className = 'lightbox';
  box.innerHTML = '<img class="lightbox__img" alt="">' +
    '<button class="lightbox__btn lightbox__prev" aria-label="Poprzednie zdjęcie"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg></button>' +
    '<button class="lightbox__btn lightbox__next" aria-label="Następne zdjęcie"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg></button>' +
    '<button class="lightbox__btn lightbox__close" aria-label="Zamknij">&times;</button>' +
    '<span class="lightbox__count"></span>';
  document.body.appendChild(box);
  var img = box.querySelector('.lightbox__img'), count = box.querySelector('.lightbox__count'), cur = 0, list = items;
  function show(i) {
    cur = (i + list.length) % list.length;
    img.src = list[cur].getAttribute('href');
    img.alt = (list[cur].querySelector('img') || {}).alt || '';
    var cap = list[cur].getAttribute('data-caption');
    count.textContent = (cap ? cap + '  ·  ' : '') + (cur + 1) + ' / ' + list.length;
  }
  function open(i) { show(i); box.classList.add('is-open'); document.body.style.overflow = 'hidden'; }
  function close() { box.classList.remove('is-open'); document.body.style.overflow = ''; }
  function visible() { return items.filter(function (a) { return !a.hidden && a.style.display !== 'none'; }); }
  items.forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); var v = visible(); list = v; open(v.indexOf(a)); }); });
  box.querySelector('.lightbox__prev').addEventListener('click', function (e) { e.stopPropagation(); show(cur - 1); });
  box.querySelector('.lightbox__next').addEventListener('click', function (e) { e.stopPropagation(); show(cur + 1); });
  box.querySelector('.lightbox__close').addEventListener('click', close);
  box.addEventListener('click', function (e) { if (e.target === box) close(); });
  document.addEventListener('keydown', function (e) {
    if (!box.classList.contains('is-open')) return;
    if (e.key === 'ArrowRight') show(cur + 1);
    else if (e.key === 'ArrowLeft') show(cur - 1);
    else if (e.key === 'Escape') close();
  });
  var x0 = null;
  box.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  box.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 40) show(cur + (dx < 0 ? 1 : -1));
  });
});

// zakładki filtrujące (np. kolekcje Wikęd: po kliknięciu widać tylko modele z danej kolekcji)
document.querySelectorAll('[data-filter-grid]').forEach(function (grid) {
  var block = grid.parentElement;
  var btns = block.querySelectorAll('[data-filter-btn]');
  btns.forEach(function (b) {
    b.addEventListener('click', function () {
      var f = b.getAttribute('data-filter-btn');
      btns.forEach(function (x) { x.classList.toggle('is-active', x === b); });
      grid.querySelectorAll('[data-filter]').forEach(function (a) { a.hidden = a.getAttribute('data-filter') !== f; });
    });
  });
});

// menu: „pigułka” podążająca za kursorem + cień po przewinięciu
(function () {
  var links = document.querySelector('.nav__links');
  var navEl = document.querySelector('.nav');
  if (navEl) {
    var onScroll = function () { navEl.classList.toggle('is-scrolled', window.scrollY > 10); };
    window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  }
  if (!links) return;
  var glider = document.createElement('span');
  glider.className = 'nav__glider';
  links.insertBefore(glider, links.firstChild);
  var top = Array.prototype.slice.call(links.querySelectorAll(':scope > a, :scope > .has-drop > a'));
  function moveTo(a) {
    if (!a || !a.offsetWidth) { glider.style.opacity = 0; return; }
    var r = a.getBoundingClientRect(), base = links.getBoundingClientRect();
    glider.style.width = r.width + 'px';
    glider.style.transform = 'translateX(' + (r.left - base.left - links.clientLeft) + 'px)';
    glider.style.opacity = 1;
  }
  var active = links.querySelector('a.is-active');
  function rest() { links.classList.remove('has-hover'); top.forEach(function (x) { x.classList.remove('is-hovered'); }); moveTo(active); }
  top.forEach(function (a) {
    var host = a.parentElement.classList.contains('has-drop') ? a.parentElement : a;
    host.addEventListener('mouseenter', function () {
      links.classList.add('has-hover');
      top.forEach(function (x) { x.classList.toggle('is-hovered', x === a); });
      moveTo(a);
    });
  });
  links.addEventListener('mouseleave', rest);
  window.addEventListener('resize', rest);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(rest);
  rest(); setTimeout(rest, 400);
})();

// pojawianie się elementów przy przewijaniu („jesteśmy sroki”)
(function () {
  if (!('IntersectionObserver' in window)) return;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var sel = ['.section-header', '.card', '.tile', '.subrow__text', '.adv', '.faq__row', '.step',
    '.gallery > a', '.sill-card', '.tech-card', '.catalog', '.split__text', '.split__media', '.swatches-grid', '.cta__inner',
    '.inv-card', '.contact-quick__item', '.info-block', '.panel', '.step-block', '.stat'];
  var obs = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); obs.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  document.querySelectorAll(sel.join(',')).forEach(function (el) {
    if (el.closest('.config, .nav, .footer, .lightbox, [data-configurator]')) return;
    if (el.getBoundingClientRect().top < window.innerHeight * 0.9) return; // to, co widać od razu, nie miga
    var sib = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
    el.style.setProperty('--d', Math.min(sib % 6, 5) * 0.08 + 's');
    if (el.matches('.subrow__text, .split__text')) el.classList.add(el.closest('.subrow--flip') ? 'reveal--right' : 'reveal--left');
    if (el.matches('.split__media')) el.classList.add('reveal--right');
    if (el.matches('.gallery > a, .tile, .swatches-grid')) el.classList.add('reveal--zoom');
    el.classList.add('reveal');
    obs.observe(el);
  });
})();

// Dla Inwestora: dom składa się element po elemencie, lista podświetla element na wizualizacji
(function () {
  var house = document.querySelector('.inv-house');
  if (!house) return;
  var split = house.closest('.split');
  var go = function () { house.classList.add('is-in'); if (split) split.classList.add('is-play'); };
  if ('IntersectionObserver' in window) {
    var o = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { go(); o.disconnect(); } }, { threshold: 0.3 });
    o.observe(house);
  } else go();
  document.querySelectorAll('.inv-list li[data-k]').forEach(function (li) {
    var k = li.getAttribute('data-k');
    li.addEventListener('mouseenter', function () {
      house.classList.add('has-hl');
      house.querySelectorAll('.ih-el').forEach(function (g) { g.classList.toggle('is-hl', g.getAttribute('data-k') === k); });
    });
    li.addEventListener('mouseleave', function () {
      house.classList.remove('has-hl');
      house.querySelectorAll('.ih-el').forEach(function (g) { g.classList.remove('is-hl'); });
    });
  });
})();

// baner cookies (zgoda zapisywana w przeglądarce) + mapa Google dopiero po zgodzie
(function () {
  var KEY = 'promykCookies';
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function loadMaps() {
    document.querySelectorAll('iframe[data-src]').forEach(function (f) {
      if (!f.src) f.src = f.getAttribute('data-src');
      f.hidden = false;
      var ph = f.parentElement.querySelector('[data-map-consent]');
      if (ph) ph.hidden = true;
    });
  }
  var bar = document.createElement('div');
  bar.className = 'cookie-bar';
  bar.setAttribute('role', 'dialog');
  bar.setAttribute('aria-label', 'Zgoda na pliki cookies');
  bar.innerHTML = '<div class="cookie-bar__text"><strong>Szanujemy Twoją prywatność</strong>' +
    '<p>Strona korzysta z pamięci przeglądarki, aby działała poprawnie (np. konfigurator). Za Twoją zgodą wczytamy też treści zewnętrzne — mapę Google, która może zapisywać własne pliki cookies. ' +
    'Szczegóły w <a href="polityka-prywatnosci.html">polityce prywatności</a>.</p></div>' +
    '<div class="cookie-bar__btns"><button type="button" class="btn btn--outline" data-c="necessary">Tylko niezbędne</button>' +
    '<button type="button" class="btn btn--primary" data-c="all">Akceptuję wszystkie</button></div>';
  var fab = document.createElement('button');
  fab.type = 'button';
  fab.className = 'cookie-fab';
  fab.setAttribute('aria-label', 'Ustawienia plików cookies');
  fab.title = 'Ustawienia cookies';
  fab.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<path d="M12 2a10 10 0 1 0 10 10 4 4 0 0 1-5-5 4 4 0 0 1-5-5"/><circle cx="8.5" cy="8.5" r="1" fill="currentColor"/>' +
    '<circle cx="16" cy="15.5" r="1" fill="currentColor"/><circle cx="11" cy="17" r="1" fill="currentColor"/><circle cx="7" cy="13" r="1" fill="currentColor"/></svg>';
  fab.addEventListener('click', function () { if (!bar.parentNode) show(); });
  document.body.appendChild(fab);
  function show() { fab.classList.remove('is-on'); document.body.appendChild(bar); requestAnimationFrame(function () { bar.classList.add('is-on'); }); }
  function hide() { bar.classList.remove('is-on'); fab.classList.add('is-on'); setTimeout(function () { if (bar.parentNode) bar.parentNode.removeChild(bar); }, 300); }
  bar.addEventListener('click', function (e) {
    var b = e.target.closest('[data-c]'); if (!b) return;
    set(b.getAttribute('data-c'));
    if (b.getAttribute('data-c') === 'all') loadMaps();
    hide();
  });
  var c = get();
  if (!c) show(); else { fab.classList.add('is-on'); if (c === 'all') loadMaps(); }
  document.querySelectorAll('[data-map-load]').forEach(function (b) { b.addEventListener('click', loadMaps); });
  document.querySelectorAll('[data-cookie-settings]').forEach(function (a) {
    a.addEventListener('click', function (e) { e.preventDefault(); if (!bar.parentNode) show(); });
  });
})();

// formularz: czas wypełnienia (antyspam) + token reCAPTCHA v3, jeśli włączona
(function () {
  var form = document.querySelector('form[data-contact]');
  if (!form) return;
  var ts = form.querySelector('[data-ts]');
  if (ts) ts.value = String(Date.now());
  form.addEventListener('submit', function (e) {
    var key = window.PROMYK_RECAPTCHA;
    if (!key || !window.grecaptcha || form.dataset.ok) return;
    e.preventDefault();
    window.grecaptcha.ready(function () {
      window.grecaptcha.execute(key, { action: 'kontakt' }).then(function (token) {
        form.querySelector('[data-recaptcha]').value = token;
        form.dataset.ok = '1';
        form.submit();
      });
    });
  });
})();
