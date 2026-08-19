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

  /* ---------- formularze (demo, bez backendu) ---------- */
  document.querySelectorAll('form[data-demo]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var box = form.querySelector('[data-formmsg]');
      if (box) {
        box.textContent = 'Dziękujemy! Zapytanie zostało przygotowane do wysyłki — podłącz obsługę formularza po stronie serwera.';
        box.style.display = 'block';
      }
    });
  });
})();
