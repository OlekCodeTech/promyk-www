# -*- coding: utf-8 -*-
"""
Generator statycznej strony PROMYK (Wieluń) — odwzorowanie projektu Figma.
Uruchomienie:  python build.py
Wynik: pliki .html w katalogu projektu (assets/ pozostają bez zmian).
"""
import os, io, html, re

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSET_VER = "46"  # podbij przy zmianach css/js (cache-busting)

PHONE = "607 941 499"
PHONE_TEL = "+48607941499"
MAIL = "info@promyk.wielun.pl"
FB_URL = "https://www.facebook.com/PromykWielun"
IG_URL = "https://www.instagram.com/Promyk_Wielun"
ADDR1 = "ul. M. Wołodyjowskiego 15"
ADDR2 = "98-300 Wieluń"

# ---------------------------------------------------------------- ikony ----
I = {
"phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
"mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
"arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
"arrowUR": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17 17 7M8 7h9v9"/></svg>',
"chevL": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>',
"chevR": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>',
"chevD": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>',
"check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
"star": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="m12 2 3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>',
"cal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18m-9 6 2 2 4-4"/></svg>',
"fb": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 12a10 10 0 1 0-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.49-3.89 3.77-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.45 2.89h-2.33v6.99A10 10 0 0 0 22 12z"/></svg>',
"ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".6" fill="currentColor"/></svg>',
"menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>',
"win": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 12h18M12 3v18"/></svg>',
"shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>',
"thermo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 14.76V4a2 2 0 1 0-4 0v10.76a4 4 0 1 0 4 0z"/></svg>',
"sparkle": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M18.4 5.6l-2.8 2.8M8.4 15.6l-2.8 2.8"/></svg>',
"cog": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .34 1.88l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06A1.7 1.7 0 0 0 15 19.4a1.7 1.7 0 0 0-1 1.55V21a2 2 0 1 1-4 0v-.09A1.7 1.7 0 0 0 9 19.4a1.7 1.7 0 0 0-1.88.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.7 1.7 0 0 0 4.6 15a1.7 1.7 0 0 0-1.55-1H3a2 2 0 1 1 0-4h.09A1.7 1.7 0 0 0 4.6 9a1.7 1.7 0 0 0-.33-1.88l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.7 1.7 0 0 0 9 4.6a1.7 1.7 0 0 0 1-1.55V3a2 2 0 1 1 4 0v.09a1.7 1.7 0 0 0 1 1.55 1.7 1.7 0 0 0 1.88-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.7 1.7 0 0 0 19.4 9c.15.6.66 1.03 1.28 1.05H21a2 2 0 1 1 0 4h-.09a1.7 1.7 0 0 0-1.51 1z"/></svg>',
"sun": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
"leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z"/><path d="M2 21c0-3 1.85-5.36 5.08-6"/></svg>',
"lock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
"ruler": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.3 8.7 8.7 21.3a1 1 0 0 1-1.4 0l-4.6-4.6a1 1 0 0 1 0-1.4L15.3 2.7a1 1 0 0 1 1.4 0l4.6 4.6a1 1 0 0 1 0 1.4z"/><path d="m7.5 10.5 2 2M10.5 7.5l2 2M13.5 4.5l2 2M4.5 13.5l2 2"/></svg>',
"palette": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22a10 10 0 1 1 10-10c0 2-1.6 3-3.5 3H17a2 2 0 0 0-1.4 3.4A2 2 0 0 1 14 22h-2z"/><circle cx="7.5" cy="10.5" r="1"/><circle cx="12" cy="7.5" r="1"/><circle cx="16.5" cy="10.5" r="1"/></svg>',
"money": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
"clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
"pdf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M12 18v-6m-3 3 3 3 3-3"/></svg>',
"bug": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 2 9.5 4M16 2l-1.5 2"/><rect x="8" y="6" width="8" height="14" rx="4"/><path d="M3 10h5M16 10h5M3 16h5M16 16h5M12 6v14"/></svg>',
"wind": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.8 19.6A2 2 0 1 0 14 16H2M17.5 8a2.5 2.5 0 1 1 2 4H2M9.6 4.6A2 2 0 1 1 11 8H2"/></svg>',
"pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
}

# ------------------------------------------------------------- produkty ----
PRODUCTS = [
    ("okna",              "Okna",               "VEKA / Aluprof",     "al39"),
    ("parapety",          "Parapety",           "Jaro-Max",           "parapety/w-marmur"),
    ("drzwi-zewnetrzne",  "Drzwi zewnętrzne",   "Wikęd / Erkado / MK-DOOR", "wiked57"),
    ("drzwi-wewnetrzne",  "Drzwi wewnętrzne",   "DRE / Porta / Erkado", "dre_binito50"),
    ("rolety-zewnetrzne", "Rolety zewnętrzne",  "Produkcja własna",   "al30_rol"),
    ("pergole",           "Pergole",            "Selt",               "pergola1"),
    ("bramy-garazowe",    "Bramy garażowe",     "Nice / AVO / Aluprof", "brama_antracyt"),
    ("markizy",           "Markizy",            "Selt",               "katalog/markiza-palladio-dom"),
    ("oslony-wewnetrzne", "Osłony wewnętrzne",  "Produkcja własna",   "plisy"),
    ("oslony-zewnetrzne", "Osłony zewnętrzne",  "Selt / Aluprof",     "katalog/screeny-dom"),
    ("moskitiery",        "Moskitiery",         "Produkcja własna",   "al25"),
]
PROD_LABEL = {s: t for s, t, _b, _i in PRODUCTS}
PROD_IMG = {s: i for s, _t, _b, i in PRODUCTS}

REVIEWS = [
    ("M", "Mariusz Kowalski", "Pełen profesjonalizm! Montaż okien VEKA wykonany bezbłędnie. Doradztwo techniczne na najwyższym poziomie, ekipa czysta i dokładna. Z czystym sumieniem polecam firmę Promyk z Wielunia."),
    ("A", "Anna Wiśniewska", "Zakupiliśmy u nich drzwi Wikęd oraz bramę garażową Nice. Wszystko działa bez zarzutu, pomiar i montaż przebiegły niezwykle sprawnie. Świetny kontakt z biurem obsługi."),
    ("T", "Tomasz Nowak", "Zleciłem montaż rolet zewnętrznych i pergoli tarasowej. Efekt przerósł moje oczekiwania, jakość materiałów i wykonania to absolutne premium. Bardzo rzetelny montaż."),
]
PARTNERS = [
    ("veka", "VEKA", "https://www.veka.pl"),
    ("aluprof", "Aluprof", "https://aluprof.com"),
    ("somfy", "Somfy", "https://www.somfy.pl"),
    ("nice", "Nice", "https://www.niceforyou.com/pl"),
    ("selt", "Selt", "https://selt.com"),
    ("mk-door", "MK-DOOR", None),
    ("wiked", "Wikęd", "https://wiked.pl"),
    ("dre", "DRE", "https://dre.pl"),
    ("porta", "Porta", "https://www.porta.com.pl"),
    ("erkado", "Erkado", "https://erkado.pl"),
    ("avo", "AVO", "https://avogroup.eu"),
    ("jaro-max", "Jaro-Max", "https://www.jaro-max.com"),
]

HOME_REALIZACJE = [  # kolejność wg klienta: okna, drzwi, bramy, pergola/refleksole
    ("realizacje/okna", "Okna — dom jednorodzinny"),
    ("realizacje/drzwi", "Drzwi zewnętrzne"),
    ("realizacje/bramy", "Brama garażowa segmentowa"),
    ("realizacje/pergola", "Pergola z lamelami"),
]

GALLERY = [  # wyłącznie realizacje PROMYK (zdjęcia ze zgodą klientów)
    ("real/pergola", "Pergola z lamelami — strefa wypoczynku", "pergole"),
    ("real/markiza-tarasowa", "Markiza tarasowa nad strefą wypoczynku", "oslony"),
    ("real/drzwi-zew-drewno", "Drzwi zewnętrzne w okleinie drewnopodobnej", "drzwi"),
    ("real/refleksole", "Refleksole ZIP na elewacji", "oslony"),
    ("real/markiza-kasetowa", "Markiza kasetowa nad tarasem", "oslony"),
    ("real/drzwi-zew-naswietle", "Drzwi wejściowe z naświetlem bocznym", "drzwi"),
    ("real/brama-drzwi", "Brama segmentowa i drzwi — nowy dom", "bramy"),
    ("real/rolety-zew", "Rolety zewnętrzne nadstawne", "rolety"),
    ("real/zaluzje-kuchnia", "Żaluzje w kuchni", "oslony"),
    ("real/okna-szczyt", "Przeszklenie szczytowe", "okna"),
    ("real/zaluzje-fasadowe", "Żaluzje fasadowe", "oslony"),
    ("real/drzwi-wew-czarne", "Drzwi wewnętrzne w czerni", "drzwi"),
    ("real/brama-antracyt", "Brama garażowa antracyt", "bramy"),
    ("real/okna-lukowe", "Okna łukowe ze szprosami", "okna"),
    ("real/rolety-dzien-noc", "Rolety dzień-noc", "oslony"),
    ("real/rolety-rzymskie", "Rolety rzymskie w kuchni", "oslony"),
    ("real/moskitiera-plisowana", "Moskitiera plisowana do drzwi tarasowych", "oslony"),
    ("real/rolety-budowa", "Rolety zewnętrzne — dom w budowie", "rolety"),
    ("real/drzwi-wew-biale", "Drzwi wewnętrzne białe", "drzwi"),
    ("real/rolety-taras", "Rolety zewnętrzne przy tarasie", "rolety"),
]

# ---------------------------------------------------------------- szkielet ----
def head(title, desc, extra=""):
    return f"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="assets/img/logo-promyk.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v={ASSET_VER}">
{extra}</head>
<body>
"""

def nav(active=""):
    def cls(k): return ' class="is-active"' if k == active else ""
    drop = "".join(
        f'<a href="{s}.html"><img src="assets/img/{i}.jpg" alt="" loading="lazy">{t}</a>'
        for s, t, _b, i in PRODUCTS)
    offer_active = ' is-active' if active in PROD_LABEL or active == "oferta" else ''
    return f"""<div class="topbar">
  <div class="container topbar__inner">
    <div class="topbar__left">
      <a href="tel:{PHONE_TEL}">{I['phone']} {PHONE}</a>
      <a class="tb-mail" href="mailto:{MAIL}">{I['mail']} {MAIL}</a>
    </div>
    <div class="topbar__right">
      <span class="tb-hours">{I['clock']} Pn–Pt 8:00–17:00 &nbsp;•&nbsp; Sob 9:00–13:00</span>
      <span class="tb-addr">{I['pin']} {ADDR1}, {ADDR2}</span>
      <span class="tb-social"><a href="{FB_URL}" target="_blank" rel="noopener" aria-label="Facebook">{I['fb']}</a><a href="{IG_URL}" target="_blank" rel="noopener" aria-label="Instagram">{I['ig']}</a></span>
    </div>
  </div>
</div>
<header class="nav">
  <div class="container nav__inner">
    <a class="logo" href="index.html" aria-label="PROMYK — strona główna">
      <img src="assets/img/logo-promyk.png" alt="PROMYK">
    </a>
    <nav class="nav__links">
      <a href="index.html"{cls('index')}>Strona główna</a>
      <a href="o-nas.html"{cls('o-nas')}>O nas</a>
      <span class="has-drop">
        <a href="oferta.html" class="{offer_active.strip()}">Oferta</a>
        <span class="drop">{drop}</span>
      </span>
      <a href="konfigurator.html"{cls('konfigurator')}>Konfigurator</a>
      <a href="dla-inwestora.html"{cls('dla-inwestora')}>Dla Inwestora</a>
      <a href="galeria.html"{cls('galeria')}>Galeria</a>
      <a href="kontakt.html"{cls('kontakt')}>Kontakt</a>
    </nav>
    <div class="nav__right">
      <a class="nav__phone" href="tel:{PHONE_TEL}">{I['phone']}{PHONE}</a>
      <a class="btn btn--primary btn--sm" href="kontakt.html">Zapytaj o wycenę {I['arrow']}</a>
      <button class="nav__burger" aria-label="Menu">{I['menu']}</button>
    </div>
  </div>
</header>
"""

def cta(tag, h2, p):
    return f"""<section class="cta">
  <div class="container cta__inner">
    {f'<span class="tag tag--onDark">{tag}</span>' if tag else ''}
    <h2>{h2}</h2>
    <p>{p}</p>
    <div class="cta__btns">
      <a class="btn btn--primary" href="kontakt.html">Zapytaj o wycenę {I['arrow']}</a>
      <a class="btn btn--ghost" href="tel:{PHONE_TEL}">{I['phone']} Zadzwoń: {PHONE}</a>
    </div>
  </div>
</section>
"""

def footer():
    links = [("index.html", "Strona główna"), ("o-nas.html", "O Nas"), ("oferta.html", "Oferta handlowa"),
             ("konfigurator.html", "Konfigurator okien"), ("dla-inwestora.html", "Dla Inwestora"),
             ("galeria.html", "Galeria realizacji"), ("kontakt.html", "Kontakt i wycena")]
    li = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in links)
    return f"""<footer class="footer">
  <div class="container">
    <div class="footer__cols">
      <div class="footer__brand">
        <img src="assets/img/logo-promyk-white.png" alt="PROMYK">
        <p>Najwyższa jakość montażu okien, drzwi zewnętrznych i wewnętrznych, bram garażowych oraz systemów zaciemnienia. Rodzinne tradycje od 1997 roku w Wieluniu.</p>
        <div class="footer__social"><a class="fb" href="{FB_URL}" target="_blank" rel="noopener">{I['fb']} Facebook</a><a class="fb" href="{IG_URL}" target="_blank" rel="noopener">{I['ig']} Instagram</a></div>
      </div>
      <div>
        <h4>Dane kontaktowe</h4>
        <p>Biuro handlowe:</p>
        <p>{ADDR1}<br>{ADDR2}</p>
        <p><a href="tel:{PHONE_TEL}">tel. {PHONE}</a></p>
        <p><a href="mailto:{MAIL}">{MAIL}</a></p>
      </div>
      <div>
        <h4>Godziny otwarcia</h4>
        <ul>
          <li class="footer__row"><span>Poniedziałek – Piątek</span><span>8:00 – 17:00</span></li>
          <li class="footer__row"><span>Sobota</span><span>9:00 – 13:00</span></li>
          <li class="footer__row"><span>Niedziela</span><span>Zamknięte</span></li>
        </ul>
      </div>
      <div>
        <h4>Nawigacja</h4>
        <ul>{li}</ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© 1997-2026 Promyk Wieluń. Wszelkie prawa zastrzeżone.</span>
      <span>Realizacja: OlekCodeTech</span>
    </div>
  </div>
</footer>

<a class="floating" href="tel:{PHONE_TEL}">{I['phone']}<span><small>Zadzwoń teraz</small><strong>{PHONE}</strong></span></a>

<script src="assets/js/main.js?v={ASSET_VER}"></script>
</body>
</html>
"""

def pagehero(img, h1, p, crumb):
    crumbs = f'<div class="crumbs"><a href="index.html">Strona główna</a> &nbsp;/&nbsp; {crumb}</div>' if crumb else ""
    return f"""<section class="pagehero">
  <img src="assets/img/{img}.jpg" alt="">
  <div class="container pagehero__body">
    {crumbs}
    <h1>{h1}</h1>
    <p>{p}</p>
  </div>
</section>
"""

def stats():
    return """<section class="stats">
  <div class="container stats__inner">
    <div class="stat">
      <div class="stat__num">150 000+</div>
      <div class="stat__label">zrealizowanych montaży</div>
    </div>
    <div class="stats__div"></div>
    <div class="stat">
      <div class="stat__num">30 lat</div>
      <div class="stat__label">doświadczenia na rynku</div>
    </div>
  </div>
</section>
"""

GOOGLE_REVIEWS_URL = "https://share.google/DOXBCy8smZ7cjqVKx"

def gbadge():
    """Baner opinii Google (ocena 4,6)."""
    stars = '<span class="stars">' + I['star'] * 4 + '<span class="halfstar">' + I['star'] + I['star'] + '</span></span>'
    return (f'<a class="gbadge" href="{GOOGLE_REVIEWS_URL}" target="_blank" rel="noopener">'
            '<span class="gbadge__logo"><svg viewBox="0 0 48 48"><path fill="#FFC107" d="M43.6 20.1H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.9 1.2 8 3l5.7-5.7C34.2 6.1 29.3 4 24 4 13 4 4 13 4 24s9 20 20 20 20-9 20-20c0-1.3-.1-2.7-.4-3.9z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.9 1.2 8 3l5.7-5.7C34.2 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.1H42V20H24v8h11.3c-.8 2.2-2.2 4.1-4.1 5.6l6.2 5.2C41 35.4 44 30.2 44 24c0-1.3-.1-2.7-.4-3.9z"/></svg></span>'
            '<strong>4,6</strong>' + stars + '<small>Opinie klientów w Google</small></a>')

def partners():
    row = "".join(
        (f'<a href="{url}" target="_blank" rel="noopener" aria-label="{name}">' if url else f'<a aria-label="{name}">')
        + f'<img src="assets/img/partners/{slug}.svg?v={ASSET_VER}" alt="{name}" loading="lazy"></a>'
        for slug, name, url in PARTNERS)
    return f"""<section class="partners">
  <div class="container">
    <h2>Pracujemy na produktach zaufanych producentów</h2>
    <p>Jesteśmy oficjalnym partnerem i autoryzowanym dystrybutorem marek premium — montujemy wyłącznie systemy, za które możemy ręczyć własną gwarancją.</p>
    <div class="partners__row">{row}</div>
  </div>
</section>
"""

def reviews():
    cards = ""
    for ini, name, txt in REVIEWS:
        cards += f"""<article class="review">
        <div class="stars">{I['star'] * 5}</div>
        <p>„{txt}”</p>
        <div class="review__by"><span class="avatar">{ini}</span><span><strong>{name}</strong><small>Klient zweryfikowany</small></span></div>
      </article>"""
    return f"""<section class="section">
  <div class="container">
    <div class="section-header">
      <div class="section-header__left">
        <h2 class="h-sec">Zaufanie budowane przez dekady</h2>
      </div>
    </div>
    <div class="grid-3">{cards}</div>
    <a class="rating rating--below" href="{GOOGLE_REVIEWS_URL}" target="_blank" rel="noopener">
      <span class="rating__num">4,6</span>
      <span class="rating__meta"><span class="stars">{I['star'] * 4}<span class="halfstar">{I['star']}{I['star']}</span></span><small class="lead">średnia ocena Google — zobacz więcej opinii</small></span>
    </a>
  </div>
</section>
"""

def write(name, content):
    with io.open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("  ->", name)

# ================================================================ STRONA GŁÓWNA ----
def build_index():
    slides = [
        ("wiked05", ), ("wiked67", ), ("al39", ),
    ]
    sl = "".join(
        f'<div class="hero__slide{" is-active" if k == 0 else ""}"><img src="assets/img/{s[0]}.jpg" alt=""></div>'
        for k, s in enumerate(slides))
    dots = "".join(f'<span class="{"is-active" if k == 0 else ""}"></span>' for k in range(len(slides)))

    tiles = ""
    for slug, title, badge, img in PRODUCTS:
        tiles += f"""<a class="tile" href="{slug}.html">
        <img src="assets/img/{img}.jpg" alt="{title}">
        <span class="tile__badge">{badge}</span>
        <div class="tile__bottom"><h3>{title}</h3><span class="tile__arrow">{I['arrowUR']}</span></div>
      </a>"""

    gal = "".join(
        f'<a href="galeria.html"><img src="assets/img/{img}.jpg" alt="{cap}"><figcaption>{cap}</figcaption></a>'
        for img, cap in HOME_REALIZACJE)

    body = f"""<section class="hero">
  <div class="hero__slides">{sl}</div>
  <div class="container hero__body">
    <div></div>
    <div class="hero__center">
      <button class="hero__arrow" data-hero="prev" aria-label="Poprzedni">{I['chevL']}</button>
      <div class="hero__text">
        <span class="tag tag--solid">Rodzinna firma od 1997 roku</span>
        <h1>Okna, drzwi i osłony na lata</h1>
        <p>Wybierz jakość popartą 30-letnim doświadczeniem.</p>
      </div>
      <button class="hero__arrow hero__arrow--next" data-hero="next" aria-label="Następny">{I['chevR']}</button>
    </div>
    <div class="hero__dots">{dots}</div>
  </div>
</section>

{stats()}

<section class="section">
  <div class="container split">
    <div class="split__text">
      <h2 class="h-sec">Od montażu rolet do lidera stolarki okiennej</h2>
      <p class="lead">Jesteśmy rodzinnym przedsiębiorstwem działającym od 1997 roku. Nasze korzenie to montaż prostych osłon okiennych – dziś dostarczamy i instalujemy kompleksowe systemy okienne, drzwiowe oraz zaawansowane zadaszenia tarasu. Działamy w promieniu 200 km od Wielunia. Gwarantujemy fachowe doradztwo techniczne i precyzyjny montaż z użyciem profesjonalnego sprzętu.</p>
      <a class="btn btn--primary" href="o-nas.html">Poznaj nas bliżej {I['arrow']}</a>
    </div>
    <div class="split__media"><img class="about__img" src="assets/img/wiked35.jpg" alt="Drzwi zewnętrzne Wikęd"></div>
  </div>
</section>

<section class="section section--soft">
  <div class="container">
    <div class="section-header">
      <div class="section-header__left">
        <h2 class="h-sec">Wybierz systemy dopasowane do Twojego domu</h2>
      </div>
    </div>
    <div class="tiles">{tiles}</div>
  </div>
</section>

{reviews()}
{partners()}

<section class="section section--soft">
  <div class="container">
    <div class="section-header">
      <div class="section-header__left">
        <h2 class="h-sec">Poznaj efekty naszych realizacji</h2>
      </div>
    </div>
    <div class="gallery gallery--home">{gal}</div>
    <div style="text-align:center;margin-top:40px">
      <a class="btn btn--primary" href="galeria.html">Zobacz więcej realizacji {I['arrow']}</a>
    </div>
  </div>
</section>
"""
    write("index.html",
          head("PROMYK Wieluń — okna, drzwi, bramy garażowe i osłony | Montaż od 1997 r.",
               "Rodzinna firma z Wielunia od 1997 r. Okna VEKA i Aluprof, drzwi Wikęd i DRE, bramy garażowe, rolety, pergole i moskitiery. Doradztwo i ciepły montaż.")
          + nav("index") + body + footer())

# ================================================================ O NAS ----
def build_onas():
    why = [
        ("30 lat doświadczenia", "Znamy branżę od podszewki i montujemy wyłącznie sprawdzone systemy klas premium.", "shield"),
        ("Kompleksowość", "Przeprowadzimy Cię przez cały proces: od profesjonalnego pomiaru aż po precyzyjny montaż.", "cog"),
        ("Gwarancja", "Dbamy o naszych klientów również po montażu.", "lock"),
        ("Lokalność", "Działamy lokalnie, stawiając na bezpośredni kontakt, zaufanie i relacje z klientami.", "leaf"),
    ]
    cards = "".join(f"""<article class="card">
      <span class="adv__icon">{I[ic]}</span>
      <div><h3>{t}</h3><p class="lead" style="margin:8px 0 0">{d}</p></div>
    </article>""" for t, d, ic in why)

    body = pagehero("wiked03", "Rodzinna firma od 1997 roku<br>Zaufanie budujemy od pokoleń",
                    "Poznaj historię naszej firmy – od pierwszych montaży żaluzji do pozycji lidera w branży stolarki okiennej.", None)
    body += stats()

    body += f"""<section class="section">
  <div class="container split">
    <div class="split__text">
      <h2 class="h-sec">Od rodzinnego rzemiosła do pozycji eksperta</h2>
      <div class="prose">
        <p><strong>PROMYK to rodzinna firma, która powstała w 1997 roku.</strong></p>
        <p>Nasza historia rozpoczęła się od montażu żaluzji. To właśnie od tej usługi właściciel firmy zaczął budować doświadczenie oraz zaufanie klientów. Z czasem dołączyła do niego żona i wspólnie stworzyli dwuosobową firmę, rozpoczynając produkcję osłon okiennych w niewielkim pomieszczeniu.</p>
        <p>Kolejne lata przyniosły dynamiczny rozwój. Firma przeniosła się do siedziby przy domu, gdzie rozszerzyliśmy działalność o produkcję rolet zewnętrznych. Rosnące grono zadowolonych klientów oraz coraz szersza oferta sprawiły, że powstał samodzielny budynek, w którym oprócz osłon okiennych zaczęliśmy oferować również okna, drzwi, bramy garażowe oraz nowoczesne zewnętrzne systemy przeciwsłoneczne.</p>
      </div>
    </div>
    <figure class="split__media about__fig"><img class="about__img about__img--full" src="assets/img/onas/budynek-pion.jpg" alt="Siedziba PROMYK w Wieluniu"><figcaption>Nasza obecna siedziba w Wieluniu</figcaption></figure>
  </div>
</section>


<section class="section section--soft">
  <div class="container split">
    <figure class="split__media about__fig"><img class="about__img" src="assets/img/onas/showroom-wizualizacja.jpg" alt="Wizualizacja nowego showroomu PROMYK"><figcaption>Wizualizacja nowego showroomu, który właśnie wykańczamy</figcaption></figure>
    <div class="split__text">
      <h2 class="h-sec">Rodzinny charakter to nasza największa siła</h2>
      <div class="prose">
        <p>Rodzinny charakter naszej firmy pozostaje jej największą siłą. Do zespołu dołączył najpierw syn, a następnie córka, dzięki czemu kolejne pokolenie aktywnie uczestniczy w dalszym rozwoju przedsiębiorstwa. Łączymy wieloletnie doświadczenie z nowoczesnym podejściem, stale poszerzając ofertę i podnosząc jakość naszych usług.</p>
        <p>Wkrótce zaprosimy Was do naszego <strong>nowego showroomu</strong> – miejsca, w którym będzie można zobaczyć najnowsze produkty, porównać dostępne rozwiązania i skorzystać z fachowego doradztwa. To kolejny etap w historii firmy PROMYK i dowód na to, że nieustannie inwestujemy w rozwój oraz komfort naszych klientów.</p>
      </div>
    </div>
  </div>
</section>

<section class="section about__then">
  <div class="container about__then-inner">
    <div class="about__then-head">
      <h3 class="about__then-title">A tak zaczynaliśmy...</h3>
    </div>
    <div class="about__strip">
      <figure class="about__fig"><img src="assets/img/onas/stara-siedziba-kw.jpg" alt="Dawna siedziba PROMYK" loading="lazy"><figcaption>Dawna siedziba firmy — „Żaluzje, rolety”</figcaption></figure>
      <figure class="about__fig"><img src="assets/img/onas/pierwsza-maszyna-kw.jpg" alt="Jedna z pierwszych maszyn PROMYK" loading="lazy"><figcaption>Jedna z pierwszych maszyn, na których pracowaliśmy</figcaption></figure>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header">
      <div class="section-header__left">
        <h2 class="h-sec">Dlaczego klienci wybierają Promyk?</h2>
      </div>
    </div>
    <div class="grid-4">{cards}</div>
  </div>
</section>

{reviews()}
{partners()}
{cta(None, "Chcesz dołączyć do grona zadowolonych klientów?",
     "Zapytaj o wycenę i przekonaj się, jak wygląda współpraca z rodzinną firmą z niemal 30-letnim doświadczeniem.")}
"""
    write("o-nas.html",
          head("O nas — rodzinna firma PROMYK od 1997 roku | Wieluń",
               "PROMYK to rodzinna firma z Wielunia działająca od 1997 roku. Od montażu żaluzji po kompleksową stolarkę otworową i nowoczesny showroom.")
          + nav("o-nas") + body + footer())

MODELS_2026 = [
    ("veka", "VEKA — okna PVC", "okna.html", [
        "SOFTLINE 82 MD: profil kl. A (ścianka 3 mm, DIN EN 12608), Uf do 1,0, Uw do 0,74 W/m²K",
        "Uszczelnienie środkowe MD, odporność RC2 wg DIN EN 1627",
        "VEKAMOTION 82 (HST): Uw od 0,78 W/m²K, rama skrzydła stałego 86 mm",
        "Powierzchnie: folie VEKA (60+ dekorów), VEKA Spectral ultramat, panele alu"]),
    ("wiked", "Wikęd — drzwi zewnętrzne", "drzwi-zewnetrzne.html", [
        "Kolekcje 2026: Rustik (Masterline/Woodline), 3D, Softline, Future Inox, Glass, Royal, Klasyk",
        "Linie technologiczne: Prima, Optimum, Termo Prestige, Alu Hybrid",
        "Drzwi na wymiar: szerokość 70–100 cm co 1 cm",
        "Przeszklenia Glass Frame, klamki RC, naświetla i dostawki"]),
    ("erkado", "Erkado — drzwi stalowe i wewnętrzne", "drzwi-zewnetrzne.html", [
        "Stalowe: konstrukcje Thermo 64 / 78 / Thermo Hot 78 / 88 mm",
        "Serie: Horn, Langen, Trebur, Wels, Bazylea, Arendal, Lahti",
        "Okleina PVC odporna na UV z wieloletnią gwarancją",
        "Wewnętrzne Stile: Werbena, Jasmin, Laurencja, Frezja — przylgowe, bezprzylgowe i rewersyjne"]),
    ("dre", "DRE — drzwi wewnętrzne", "drzwi-wewnetrzne.html", [
        "Laminaty akrylowe: Ilis, Nella, Vetro D2, Silia (połysk / super mat)",
        "Ramowe: Vetro E Synchro, Estra, Nestor, Auri, Reva, Fosca",
        "Ościeżnica DRE WaterProof — odporna na stały kontakt z wodą",
        "Okleiny: Finish, 3D, DRE-Cell, CPL 0,15–0,7 mm"]),
    ("porta", "Porta — drzwi wewnętrzne", "drzwi-wewnetrzne.html", [
        "10 linii wzorniczych w katalogu 2026",
        "Rozwiązania: drzwi akustyczne, wilgocioodporne, ukryte (zlicowane ze ścianą)",
        "Nr 1 w Polsce i Europie Środkowo-Wschodniej — 1,7 mln produktów rocznie",
        "Badania w 21 laboratoriach w kraju i za granicą"]),
    ("avo", "AVO — bramy garażowe", "bramy-garazowe.html", [
        "Modele: Base Line, Base Trend, Base Elegant, Line, Trend, Elegant, Elegant ISO 60",
        "Powierzchnie Woodgrain i Silk; dekory Woodec, Winchester, Złoty Dąb",
        "Automatyka ADO / ADO PRO: 24 V, LED w prowadnicy, sterowanie KUBE (Bluetooth) + Wi-Fi",
        "Lakierowanie: 205 kolorów RAL, 1950 kolorów NCS"]),
    ("nice", "Nice — napędy do bram", "bramy-garazowe.html", [
        "Spider 1200N: silnik bezszczotkowy, do 150 cykli/dobę, bramy do 16,9 m² (uchylne 19,5 m²)",
        "Wbudowane Wi-Fi, oświetlenie LED i system antywłamaniowy",
        "Spido 600N: otwarcie w ok. 10 s, cyfrowe wyłączniki krańcowe",
        "Integracja: Yubii Home / CORE, Alexa, Google Assistant, Siri"]),
]

# ================================================================ OFERTA ----
def build_oferta():
    tiles = ""
    for slug, title, badge, img in PRODUCTS:
        tiles += f"""<a class="tile" href="{slug}.html">
        <img src="assets/img/{img}.jpg" alt="{title}">
        <span class="tile__badge">{badge}</span>
        <div class="tile__bottom"><h3>{title}</h3><span class="tile__arrow">{I['arrowUR']}</span></div>
      </a>"""
    catalogs = [
        ("VEKA SOFTLINE 82 MD", "Okna PVC klasy A — profil 82 mm, Uw do 0,74 W/m²K", "katalog-veka-softline82.pdf"),
        ("VEKA VEKAMOTION 82", "Drzwi podnoszono-przesuwne HST — Uw od 0,78 W/m²K", "katalog-veka-vekamotion82.pdf"),
        ("Wikęd — drzwi do domu 2026", "Kolekcje Rustik, 3D, Softline, Glass, Royal; linie Prima–Alu Hybrid", "katalog-wiked.pdf"),
        ("Erkado — drzwi stalowe 2026", "Konstrukcje Thermo 64–88 mm, serie Horn, Langen, Trebur, Arendal", "katalog-erkado-stalowe.pdf"),
        ("Erkado — drzwi wewnętrzne 2026", "Ramiakowe Stile: Werbena, Jasmin, Laurencja i inne", "katalog-erkado-wewnetrzne.pdf"),
        ("DRE — katalog 2026", "Kolekcje Estra, Nestor, Vetro, Ilis; ościeżnica WaterProof", "katalog-dre.pdf"),
        ("Porta — katalog 2026", "10 linii wzorniczych, drzwi akustyczne i wilgocioodporne", "katalog-porta.pdf"),
        ("AVO — bramy garażowe 2026", "Bramy segmentowe Base Line – Elegant ISO 60, automatyka ADO", "katalog-avo-bramy.pdf"),
        ("Nice — napędy Spider i Spido", "Siłowniki do bram segmentowych i uchylnych, Wi-Fi, Yubii", "katalog-nice-napedy.pdf"),
        ("Katalog Selt", "Pergole, markizy i żaluzje fasadowe", "katalog-selt.pdf"),
        ("Cennik orientacyjny PROMYK", "Ceny typowych rozwiązań", "cennik-promyk.pdf"),
    ]
    cat = ""
    for t, sub, fname in catalogs:
        fpath = os.path.join(ROOT, "assets", "katalogi", fname)
        if os.path.exists(fpath):
            size_mb = os.path.getsize(fpath) / 1048576
            cat += f"""<a class="catalog" href="assets/katalogi/{fname}" download>
      <span class="catalog__icon">{I['pdf']}</span>
      <span class="catalog__info"><strong>{t}</strong><span>{sub}</span></span>
      <span class="catalog__meta">PDF • {size_mb:.1f} MB</span>
    </a>"""
        else:
            cat += f"""<div class="catalog catalog--soon">
      <span class="catalog__icon">{I['pdf']}</span>
      <span class="catalog__info"><strong>{t}</strong><span>{sub}</span></span>
      <span class="catalog__meta"><span class="tag">Wkrótce</span></span>
    </div>"""

    models = "".join(
        f'''<article class="card model-card">
        <div class="model-card__head"><img src="assets/img/partners/{logo}.svg?v={ASSET_VER}" alt=""><h3>{title}</h3></div>
        <ul class="bullets">{"".join(f'<li><span class="check">{I["check"]}</span> {b}</li>' for b in bullets)}</ul>
        <a class="card__more" href="{href}">Zobacz kategorię {I['arrow']}</a>
      </article>'''
        for logo, title, href, bullets in MODELS_2026)

    body = pagehero("al31_rol", "Kompleksowa stolarka otworowa",
                    "Okna, drzwi, bramy i osłony przeciwsłoneczne — wszystko w jednym miejscu, z jednym montażem i jedną gwarancją.", "Oferta")
    body += f"""<section class="section section--soft">
  <div class="container">
    <div class="section-header">
      <div class="section-header__left">
        <span class="tag">Kompleksowa stolarka otworowa</span>
        <h2 class="h-sec">Wybierz systemy dopasowane do Twojego projektu</h2>
      </div>
      <p class="section-header__right lead">W jednym miejscu zamówisz okna, drzwi zewnętrzne i wewnętrzne, bramy garażowe, rolety, parapety oraz osłony przeciwsłoneczne.</p>
    </div>
    <div class="tiles">{tiles}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header">
      <div class="section-header__left">
        <span class="tag">Prosto z katalogów 2026</span>
        <h2 class="h-sec">Modele i parametry naszych producentów</h2>
        <p class="lead">Wyciąg techniczny z aktualnych katalogów — pełne wersje PDF do pobrania poniżej.</p>
      </div>
    </div>
    <div class="grid-2">{models}</div>
  </div>
</section>

<section class="section section--soft">
  <div class="container">
    <div class="section-header">
      <div class="section-header__left">
        <span class="tag">Materiały informacyjne</span>
        <h2 class="h-sec">Katalogi do pobrania</h2>
        <p class="lead">Pobierz oficjalne katalogi naszych partnerów oraz orientacyjne cenniki, aby zapoznać się ze szczegółowymi specyfikacjami technicznymi.</p>
      </div>
    </div>
    <div class="stack">{cat}</div>
    <p class="lead" style="margin-top:18px;font-size:13px">Katalogi producentów — wersje aktualne na rok 2026. Pliki otwierają się w przeglądarce; większe katalogi (Wikęd, Porta) mogą ładować się kilka sekund.</p>
  </div>
</section>

{cta("Darmowa wycena i doradztwo", "Chcesz poznać wycenę dla swojej inwestycji?",
     "Prześlij nam zestawienie stolarki lub rzuty budynku. Przygotujemy dla Ciebie darmową, szczegółową ofertę bez żadnych zobowiązań.")}
"""
    write("oferta.html",
          head("Oferta — okna, drzwi, bramy, rolety i osłony | PROMYK Wieluń",
               "Pełna oferta PROMYK: okna PVC i aluminiowe, drzwi zewnętrzne Wikęd, drzwi wewnętrzne DRE, bramy garażowe, rolety, pergole, markizy i moskitiery.")
          + nav("oferta") + body + footer())

# ================================================================ DLA INWESTORA ----
def build_inwestor():
    benefits = [
        ("Oszczędność", "Unikasz kosztownych przeróbek otworów okiennych na późniejszych etapach budowy. Zaplanowana wcześniej stolarka to niższe koszty.", "money"),
        ("Spójność", "Uzgadniamy jednolitą kolorystykę bramy, drzwi i ram okiennych od początku. Twój dom zyskuje harmonijny i luksusowy wygląd.", "palette"),
        ("Terminowość", "Dopasowujemy harmonogram dostawy i montażu bezpośrednio do postępów prac budowlanych. Zero niepotrzebnych przestojów ekipy.", "clock"),
    ]
    ben = "".join(f"""<article class="card">
      <span class="adv__icon">{I[ic]}</span>
      <div><h3>{t}</h3><p class="lead" style="margin:8px 0 0">{d}</p></div>
    </article>""" for t, d, ic in benefits)

    steps = [
        ("01", "Konsultacja", "Prace zaczynamy od rozmowy i analizy Twojego projektu architektonicznego."),
        ("02", "Pomiar na budowie", "Wykonujemy precyzyjne pomiary otworów przy użyciu profesjonalnego lasera."),
        ("03", "Dobór i wycena", "Konfigurujemy najlepsze profile i przygotowujemy przejrzysty kosztorys."),
        ("04", "Produkcja", "Zamawiamy spersonalizowaną stolarkę u czołowych producentów (VEKA, Wikęd, DRE)."),
        ("05", "Ciepły montaż", "Przeprowadzamy montaż warstwowy gwarantujący szczelność przez dekady."),
    ]
    st = "".join(f'<article class="step"><div class="step__no">{n}</div><h3>{t}</h3><p>{d}</p></article>' for n, t, d in steps)

    groups = [
        ("Inwestorzy indywidualni", "Prowadzimy Cię za rękę przez cały proces. Pomagamy wybrać optymalne technologie, łącząc doskonały design z energooszczędnością.",
         ["Kompleksowa opieka i doradztwo", "Precyzyjny pomiar i dopasowanie", "Lokalny serwis pogwarancyjny w Wieluniu"]),
        ("Architekci i projektanci", "Dostarczamy pełną dokumentację techniczną, modele CAD/BIM oraz wsparcie inżynieryjne przy niestandardowych, dużych przeszkleniach.",
         ["Pliki CAD i parametry techniczne", "Konsultacje projektów konstrukcyjnych", "Rozwiązania do domów pasywnych i energooszczędnych"]),
        ("Wykonawcy i deweloperzy", "Oferujemy elastyczne warunki współpracy, pewne terminy realizacji oraz montaż realizowany przez doświadczone i certyfikowane ekipy.",
         ["Atrakcyjne warunki handlowe", "Gwarancja dotrzymania ustalonych terminów", "Certyfikaty zgodności z normami budowlanymi"]),
    ]
    gr = ""
    for t, d, bl in groups:
        li = "".join(f"<li>{b}</li>" for b in bl)
        gr += f"""<article class="card group-card">
      <div><h3 style="font-size:20px">{t}</h3><p class="lead" style="margin:10px 0 0">{d}</p></div>
      <div class="hr"></div>
      <ul>{li}</ul>
    </article>"""

    faq = [
        ("Kiedy najlepiej zamówić okna i drzwi do nowego domu?",
         "Najlepszym momentem jest etap stanu surowego otwartego, tuż po ukończeniu ścian i dachu. Pozwala to na precyzyjny pomiar przed tynkami oraz odpowiednie zaplanowanie montażu ciepłego oraz osłon zewnętrznych (żaluzji, rolet). Jeszcze lepiej zgłosić się do nas już na etapie projektu domu — im wcześniej rozpoczniemy współpracę, tym większe możliwości doboru optymalnych rozwiązań."),
        ("Czy doradztwo techniczne jest bezpłatne?",
         "Tak. Podczas bezpłatnego spotkania w naszej siedzibie wspólnie przeanalizujemy projekt domu, doradzimy najlepsze rozwiązania techniczne i estetyczne oraz przygotujemy wstępną, niezobowiązującą wycenę. Po podjęciu decyzji wykonujemy dokładny pomiar na budowie."),
        ("Jak długo trwa realizacja zamówienia od pomiaru?",
         "Standardowy termin realizacji to zwykle 4–8 tygodni od zatwierdzenia zamówienia i wykonania pomiaru. Termin zależy od producenta i stopnia personalizacji stolarki — dokładną datę potwierdzamy w umowie i dopasowujemy do harmonogramu budowy."),
        ("Czy wykonujecie montaż w innych miastach niż Wieluń?",
         "Tak. Działamy w promieniu ok. 200 km od Wielunia — obsługujemy cały region łódzki oraz województwa sąsiednie."),
        ("Jakiej gwarancji udzielacie na produkty i montaż?",
         "Na produkty obowiązuje gwarancja producenta (najczęściej 5–10 lat w zależności od systemu), a na wykonany przez nas montaż udzielamy własnej gwarancji. Zapewniamy też lokalny serwis gwarancyjny i pogwarancyjny."),
    ]
    fq = ""
    for k, (q, a) in enumerate(faq):
        cls = ""
        sign = "+"
        fq += f"""<div class="faq__row{cls}">
      <button class="faq__q"><span>{q}</span><span>{sign}</span></button>
      <div class="faq__a">{a}</div>
    </div>"""

    body = pagehero("wiked07", "Dla Inwestora — planuj stolarkę od pierwszej kreski projektu",
                    "Budowa domu to wiele ważnych decyzji. Wybór okien, drzwi, bramy czy rolet wpływa nie tylko na wygląd budynku, ale również na komfort, bezpieczeństwo i koszty jego użytkowania przez wiele lat.", "Dla Inwestora")

    body += f"""<section class="section">
  <div class="container split">
    <div class="split__text">
      <span class="tag">Kompleksowa obsługa inwestora</span>
      <h2 class="h-sec">Wszystko zamówisz w jednym miejscu</h2>
      <div class="prose">
        <p>Warto zgłosić się do nas już na etapie projektu domu. Im wcześniej rozpoczniemy współpracę, tym większe możliwości doboru optymalnych rozwiązań oraz lepszego zaplanowania całej inwestycji.</p>
        <p>Oferujemy kompleksową obsługę inwestorów – od pierwszej konsultacji aż po profesjonalny montaż. W jednym miejscu mogą Państwo zamówić:</p>
        <ul>
          <li><span class="check">{I['check']}</span> okna</li>
          <li><span class="check">{I['check']}</span> drzwi zewnętrzne</li>
          <li><span class="check">{I['check']}</span> bramy garażowe</li>
          <li><span class="check">{I['check']}</span> rolety zewnętrzne</li>
          <li><span class="check">{I['check']}</span> drzwi wewnętrzne</li>
          <li><span class="check">{I['check']}</span> parapety zewnętrzne i wewnętrzne</li>
          <li><span class="check">{I['check']}</span> osłony przeciwsłoneczne</li>
        </ul>
        <p>Podczas bezpłatnego spotkania w naszej siedzibie wspólnie przeanalizujemy projekt domu, doradzimy najlepsze rozwiązania techniczne i estetyczne oraz przygotujemy wstępną, niezobowiązującą wycenę. Dzięki naszemu doświadczeniu pomożemy dobrać produkty dopasowane do budżetu, oczekiwań oraz charakteru inwestycji.</p>
        <p>Po podjęciu decyzji wykonujemy dokładny pomiar na budowie, dbając o to, aby wszystkie elementy były idealnie dopasowane. Następnie zapewniamy profesjonalny montaż, wykonywany przez doświadczonych specjalistów.</p>
        <p>Naszym celem jest, aby cały proces – od projektu po montaż – przebiegał sprawnie, bezproblemowo i z pełnym wsparciem na każdym etapie. Dzięki kompleksowej ofercie oraz fachowemu doradztwu oszczędzają Państwo czas i mają pewność, że wszystkie elementy stolarki będą tworzyć spójną i funkcjonalną całość.</p>
        <p>Zapraszamy do naszego showroomu, gdzie można obejrzeć oferowane produkty, porównać różne rozwiązania i skorzystać z bezpłatnej konsultacji z naszymi doradcami.</p>
        <p>Kiedy dom jest już gotowy, a przychodzi czas na aranżację ogrodu i tarasu, nadal jesteśmy do Państwa dyspozycji. Oferujemy nowoczesne rozwiązania zwiększające komfort wypoczynku na świeżym powietrzu, takie jak <strong>pergole tarasowe, refleksole oraz sunbreakery</strong>.</p>
      </div>
      <a class="btn btn--primary" href="kontakt.html">Umów bezpłatną konsultację {I['arrow']}</a>
    </div>
    <div class="split__media"><img class="about__img" src="assets/img/al31_rol.jpg" alt="Realizacja inwestycji"></div>
  </div>
</section>

<section class="section section--soft">
  <div class="container">
    <div class="section-header">
      <div class="section-header__left">
        <span class="tag">Strategiczne podejście</span>
        <h2 class="h-sec">Dlaczego warto planować wcześniej?</h2>
      </div>
    </div>
    <div class="grid-3">{ben}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header">
      <div class="section-header__left">
        <span class="tag">Ścieżka współpracy</span>
        <h2 class="h-sec">5 kroków do idealnej stolarki</h2>
      </div>
    </div>
    <div class="steps">{st}</div>
  </div>
</section>

<section class="section section--soft">
  <div class="container">
    <div class="section-header">
      <div class="section-header__left">
        <span class="tag">Partnerzy w budowie</span>
        <h2 class="h-sec">Dedykowane wsparcie i korzyści</h2>
      </div>
    </div>
    <div class="grid-3">{gr}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header">
      <div class="section-header__left">
        <span class="tag">Najczęstsze pytania</span>
        <h2 class="h-sec">Baza wiedzy inwestora (FAQ)</h2>
      </div>
    </div>
    <div class="faq">{fq}</div>
  </div>
</section>

{cta("Umów się na konsultację stolarki", "Rozpocznij planowanie stolarki już teraz",
     "Nie zwlekaj do ostatniej chwili. Skonsultuj swój projekt z naszymi inżynierami, aby uniknąć błędów projektowych i zaoszczędzić na budowie.")}
"""
    write("dla-inwestora.html",
          head("Dla Inwestora — kompleksowa obsługa budowy | PROMYK Wieluń",
               "Planujesz budowę domu? Okna, drzwi, bramy garażowe, rolety i parapety zamówisz w jednym miejscu. Bezpłatna konsultacja i profesjonalny montaż.")
          + nav("dla-inwestora") + body + footer())

# ================================================================ GALERIA ----
def build_galeria():
    cats = [("all", "Wszystkie"), ("okna", "Okna"), ("drzwi", "Drzwi"), ("pergole", "Pergole"),
            ("rolety", "Rolety"), ("bramy", "Bramy"), ("oslony", "Osłony")]
    fl = "".join(f'<button class="filter{" is-active" if c == "all" else ""}" data-filter="{c}">{t}</button>' for c, t in cats)
    items = ""
    for k, (img, cap, cat) in enumerate(GALLERY):
        hid = " is-hidden" if k >= 12 else ""
        style = ' style="display:none"' if k >= 12 else ""
        items += f'<a href="assets/img/{img}.jpg" target="_blank" data-cat="{cat}" class="{hid.strip()}"{style}><img src="assets/img/{img}.jpg" alt="{cap}" loading="lazy"><figcaption>{cap}</figcaption></a>'

    body = pagehero("wiked67", "Galeria realizacji",
                    "Zobacz, jak nasze systemy wyglądają w prawdziwych domach — okna, drzwi, bramy, pergole i osłony.", "Galeria")
    body += f"""<section class="section" style="padding-bottom:0">
  <div class="container"><div class="filters">{fl}</div></div>
</section>

<section class="section">
  <div class="container">
    <div class="gallery">{items}</div>
    <div style="text-align:center;margin-top:48px">
      <button class="btn btn--outline" data-more>Pokaż więcej realizacji {I['chevD']}</button>
    </div>
  </div>
</section>

{cta("Precyzja i profesjonalizm", "Chcesz podobny efekt u siebie?",
     "Zadbamy o każdy detal — od dokładnego pomiaru laserowego na Twojej budowie po czysty i bezbłędny montaż z gwarancją premium.")}
"""
    write("galeria.html",
          head("Galeria realizacji — okna, drzwi, bramy i pergole | PROMYK Wieluń",
               "Galeria realizacji firmy PROMYK: montaż okien, drzwi zewnętrznych i wewnętrznych, bram garażowych, rolet, pergoli i osłon przeciwsłonecznych.")
          + nav("galeria") + body + footer())

# ================================================================ KONTAKT ----
def build_kontakt():
    opts = "".join(f"<option>{t}</option>" for t in
                   ["Wycena stolarki okiennej", "Drzwi zewnętrzne", "Drzwi wewnętrzne", "Bramy garażowe",
                    "Rolety i osłony", "Pergole i markizy", "Moskitiery", "Serwis i reklamacja", "Inne pytanie"])
    body = f"""<section class="section" style="padding-bottom:0">
  <div class="container" style="max-width:900px;text-align:center;display:flex;flex-direction:column;gap:16px;align-items:center">
    <span class="tag">Biuro Handlowe &amp; Serwis</span>
    <h1 class="h-page" style="font-size:44px">Zapraszamy do kontaktu</h1>
    <p class="lead lead--lg">Odpowiemy na Twoje pytania i doradzimy najlepsze rozwiązania dla Twojej inwestycji.</p>
  </div>
</section>

<section class="section">
  <div class="container contact-grid">
    <div class="panel">
      <h2>Napisz do nas</h2>
      <form data-demo>
        <div class="form-grid">
          <div class="field"><label for="f-name">Imię i nazwisko *</label><input id="f-name" name="name" placeholder="np. Jan Kowalski" required></div>
          <div class="field"><label for="f-tel">Telefon komórkowy *</label><input id="f-tel" name="tel" type="tel" placeholder="np. +48 {PHONE}" required></div>
          <div class="field"><label for="f-mail">E-mail *</label><input id="f-mail" name="email" type="email" placeholder="np. jan@dom.pl" required></div>
          <div class="field"><label for="f-cat">Kategoria zapytania</label><select id="f-cat" name="kategoria">{opts}</select></div>
          <div class="field field--full"><label for="f-msg">Treść wiadomości *</label><textarea id="f-msg" name="message" placeholder="Opisz swój projekt, wymiary lub zadaj pytanie..." required></textarea></div>
          <div class="field field--full">
            <label class="consent"><input type="checkbox" required> Wyrażam zgodę na przetwarzanie danych osobowych zgodnie z polityką prywatności w celu obsługi zapytania. *</label>
          </div>
        </div>
        <button class="btn btn--primary" style="width:100%;justify-content:center;margin-top:24px" type="submit">Wyślij zapytanie {I['arrow']}</button>
        <p data-formmsg style="display:none;margin-top:16px;font-size:14px;color:var(--accent)"></p>
      </form>
    </div>
    <aside>
      <div class="info-block">
        <h3>Dane rejestrowe i adres</h3>
        <p><strong>PROMYK Okna i Drzwi</strong></p>
        <p>{ADDR1}</p>
        <p>{ADDR2}</p>
      </div>
      <div class="info-block">
        <h3>Szybki kontakt</h3>
        <a class="info-line" href="tel:{PHONE_TEL}">{I['phone']} {PHONE}</a>
        <a class="info-line" href="mailto:{MAIL}">{I['mail']} {MAIL}</a>
      </div>
      <div class="info-block">
        <h3>Godziny pracy salonu</h3>
        <p>Poniedziałek – Piątek: 8:00 – 17:00</p>
        <p>Sobota: 9:00 – 13:00</p>
        <p>Niedziela: Zamknięte</p>
      </div>
    </aside>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="container">
    <div class="map">
      <iframe title="Mapa dojazdu do PROMYK Wieluń" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
        src="https://www.google.com/maps?q={ADDR1.replace(' ', '+')},+{ADDR2.replace(' ', '+')}&amp;output=embed"></iframe>
    </div>
  </div>
</section>
"""
    write("kontakt.html",
          head("Kontakt — PROMYK Wieluń | okna, drzwi, bramy, osłony",
               f"Skontaktuj się z PROMYK: {ADDR1}, {ADDR2}, tel. {PHONE}. Wycena i doradztwo w zakresie stolarki otworowej.")
          + nav("kontakt") + body + footer())

# ================================================================ KONFIGURATOR ----
def build_konfigurator():
    colors = [("Biel", "#f5f5f2"), ("Antracyt", "#3c3f43"), ("Czerń", "#17181a"), ("Brąz", "#5b3a24"),
              ("Złoty dąb", "linear-gradient(160deg,#b97c36,#8a5420)"),
              ("Orzech", "linear-gradient(160deg,#5f3c22,#3c2413)"),
              ("Winchester", "linear-gradient(160deg,#8a6240,#5e3f27)")]
    def sw(active):
        return "".join(
            f'<button type="button" class="swatch{" is-active" if n == active else ""}" data-value="{n}"><i style="background:{c}"></i>{n}</button>'
            for n, c in colors)

    types = [
        ("jedno", "Jednoskrzydłowe",
         '<svg viewBox="0 0 44 44"><rect x="4" y="4" width="36" height="36" fill="none" stroke="currentColor" stroke-width="3"/><rect x="10" y="10" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"/></svg>'),
        ("dwa", "Dwuskrzydłowe",
         '<svg viewBox="0 0 44 44"><rect x="2" y="6" width="40" height="32" fill="none" stroke="currentColor" stroke-width="3"/><path d="M22 6v32" stroke="currentColor" stroke-width="2"/><rect x="6" y="10" width="12" height="24" fill="none" stroke="currentColor" stroke-width="1.6"/><rect x="26" y="10" width="12" height="24" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'),
        ("balkon", "Drzwi balkonowe",
         '<svg viewBox="0 0 44 44"><rect x="12" y="2" width="20" height="40" fill="none" stroke="currentColor" stroke-width="3"/><rect x="17" y="7" width="10" height="30" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>'),
        ("hst", "Przesuwne HST",
         '<svg viewBox="0 0 44 44"><rect x="2" y="8" width="40" height="28" fill="none" stroke="currentColor" stroke-width="3"/><rect x="20" y="11" width="19" height="22" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 22h7m0 0-3-3m3 3-3 3" stroke="currentColor" stroke-width="2" fill="none"/></svg>'),
    ]
    ty = "".join(
        f'<button type="button" class="optcard{" is-active" if k == "dwa" else ""}" data-value="{k}">{svg}{n}</button>'
        for k, n, svg in types)

    handles = [("Biała", "#f2f2f0"), ("Srebrna", "#b9bec4"), ("Czarna", "#1c1d1f"), ("Złota", "#c79a4b")]
    hd = "".join(
        f'<button type="button" class="optcard{" is-active" if n == "Czarna" else ""}" data-value="{n}"><span class="dot" style="background:{c}"></span>{n}</button>'
        for n, c in handles)

    bars = [
        ("Brak", '<svg viewBox="0 0 44 44"><rect x="4" y="4" width="36" height="36" fill="none" stroke="currentColor" stroke-width="2.4"/></svg>'),
        ("Krzyż", '<svg viewBox="0 0 44 44"><rect x="4" y="4" width="36" height="36" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M22 4v36M4 22h36" stroke="currentColor" stroke-width="2"/></svg>'),
        ("Poziome", '<svg viewBox="0 0 44 44"><rect x="4" y="4" width="36" height="36" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M4 22h36" stroke="currentColor" stroke-width="2"/></svg>'),
        ("Wielopolowe", '<svg viewBox="0 0 44 44"><rect x="4" y="4" width="36" height="36" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M16 4v36M28 4v36M4 16h36M4 28h36" stroke="currentColor" stroke-width="1.6"/></svg>'),
    ]
    bd = "".join(
        f'<button type="button" class="optcard{" is-active" if n == "Brak" else ""}" data-value="{n}">{svg}{n}</button>'
        for n, svg in bars)

    scenes = [("plaster", "Tynk biały", "#ece9e2"), ("grey", "Tynk szary", "#b7babd"),
              ("anthracite", "Antracyt", "#43484d"), ("brick", "Cegła", "#a75d45"), ("wood", "Deska", "#a97b4e")]
    sc = "".join(
        f'<button type="button" data-scene="{k}" title="Elewacja: {n}" aria-label="Elewacja: {n}"'
        f'{" class=is-active" if k == "plaster" else ""} style="background:{c}"></button>'
        for k, n, c in scenes)

    body = f"""<section class="section" style="padding-block:56px 0">
  <div class="container">
    <span class="tag">Narzędzie online</span>
    <h1 class="h-sec" style="margin:16px 0 10px">Konfigurator okien</h1>
    <p class="lead lead--lg" style="max-width:760px">Złóż swoje okno na żywo — wybierz konstrukcję, kolory, klamkę i szprosy, sprawdź wygląd na różnych elewacjach i wyślij gotową konfigurację do bezpłatnej wyceny.</p>
  </div>
</section>

<section class="section" style="padding-top:48px" data-config>
  <div class="container config">
    <div class="cfg-stage">
      <div class="preview scene-plaster">
        <div class="preview__toolbar">
          <div class="seg">
            <button type="button" data-mode="scene" class="is-active">Wizualizacja</button>
            <button type="button" data-mode="photo">📷 Okno VEKA</button>
          </div>
          <div class="seg seg--env">
            <button type="button" data-view="out" class="is-active">Z zewnątrz</button>
            <button type="button" data-view="in">Od wewnątrz</button>
          </div>
          <div class="seg seg--env">
            <button type="button" data-time="day" class="is-active" title="Dzień">☀️</button>
            <button type="button" data-time="dusk" title="Zmierzch">🌆</button>
            <button type="button" data-time="night" title="Noc">🌙</button>
          </div>
        </div>
        <div data-svg></div>
        <div class="preview__dims" data-dims></div>
        <div class="preview__scenes"><small>Elewacja</small>{sc}</div>
      </div>
      <div class="cfg-photos">
        <h4>Okna w kolorze <span data-photocolor>Antracyt</span> — nasze realizacje</h4>
        <div class="cfg-photos__row" data-photos></div>
        <div class="cfg-photos__empty">Ten odcień prezentujemy na próbnikach w naszym showroomie w Wieluniu — zapraszamy, doradca pokaże Ci go na gotowych oknach.</div>
      </div>
      <div class="alert">💡 <strong>Wskazówka:</strong> kolory drewnopodobne (Złoty dąb, Orzech, Winchester) doskonale pasują do nowoczesnego budownictwa i elewacji z elementami naturalnego drewna.</div>
    </div>

    <div class="cfg-panel">
      <div class="optgroup cfg-only-scene" data-group="type">
        <h3><span class="no">1</span> Typ konstrukcji <span class="picked"></span></h3>
        <div class="optcards">{ty}</div>
      </div>
      <div class="optgroup cfg-only-scene">
        <h3><span class="no">2</span> Wymiary okna</h3>
        <div class="dims">
          <div><label for="cfg-w">Szerokość (50–400)</label><div class="dim-wrap"><input id="cfg-w" data-w type="number" min="50" max="400" step="5" value="180"><span class="unit">cm</span></div></div>
          <div><label for="cfg-h">Wysokość (50–280)</label><div class="dim-wrap"><input id="cfg-h" data-h type="number" min="50" max="280" step="5" value="150"><span class="unit">cm</span></div></div>
        </div>
      </div>
      <div class="optgroup" data-group="out">
        <h3><span class="no">3</span> Kolor od zewnątrz (dekory VEKA) <span class="picked"></span></h3>
        <div class="veka-cat">Paleta kolorów</div>
        <div class="veka-row" data-vekagroup="uni"></div>
        <div class="veka-cat">Dekory drewnopodobne i metalopodobne</div>
        <div class="veka-row" data-vekagroup="dekor"></div>
        <div class="veka-cat">VEKA Spectral (ultramat)</div>
        <div class="veka-row" data-vekagroup="spectral"></div>
      </div>
      <div class="optgroup cfg-only-scene" data-group="in">
        <h3><span class="no">4</span> Kolor od wewnątrz <span class="picked"></span></h3>
        <div class="swatches">{sw('Biel')}</div>
      </div>
      <div class="optgroup cfg-only-scene" data-group="handle">
        <h3><span class="no">5</span> Klamka okienna <span class="picked"></span></h3>
        <div class="optcards">{hd}</div>
      </div>
      <div class="optgroup cfg-only-scene" data-group="bars">
        <h3><span class="no">6</span> Szprosy (szczebliny) <span class="picked"></span></h3>
        <div class="optcards">{bd}</div>
      </div>
      <div class="recap">
        <h3>Twoja konfiguracja</h3>
        <dl data-recap></dl>
        <div class="recap__price">
          <small>Orientacyjna cena brutto z montażem — dokładną wycenę przygotujemy w 24 h.</small>
          <strong data-price></strong>
        </div>
        <a class="btn" data-cta href="kontakt.html">Wyślij zapytanie o wycenę {I['arrow']}</a>
      </div>
    </div>
  </div>
</section>
<script src="assets/js/veka-data.js?v={ASSET_VER}"></script>
<script src="assets/js/configurator.js?v={ASSET_VER}" defer></script>
"""
    write("konfigurator.html",
          head("Konfigurator okien online — kolory, klamki, szprosy | PROMYK Wieluń",
               "Interaktywny konfigurator okien: typ konstrukcji, wymiary, kolory od zewnątrz i wewnątrz, klamka, szprosy i podgląd na różnych elewacjach. Wyślij konfigurację do bezpłatnej wyceny.")
          + nav("konfigurator") + body + footer())

# ================================================================ PRODUKTY ----
def logo_src(logo):
    """'@plik.png' = grafika z assets/img, w innym wypadku logo partnera (SVG)."""
    return f"assets/img/{logo[1:]}" if logo.startswith("@") else f"assets/img/partners/{logo}.svg?v={ASSET_VER}"

def product_extras_html(slug):
    """Sekcje pogłębiające podstronę: specyfikacja, producenci, Warto wiedzieć, katalogi."""
    ex = PRODUCT_EXTRAS.get(slug)
    if not ex:
        return ""
    out = ""

    spec = ex.get("specs")
    if spec:
        head = "".join(f"<th>{c}</th>" for c in spec["cols"])
        rows = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in spec["rows"])
        out += f"""<section class="section section--soft">
  <div class="container">
    <div class="section-header"><div class="section-header__left">
      <span class="tag">Specyfikacja</span><h2 class="h-sec">{spec['title']}</h2>
    </div></div>
    <div class="spec-wrap"><table class="spec-table"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>
  </div>
</section>
"""

    brands = ex.get("brands") or []
    if brands:
        cards = ""
        for logo, name, bullets in brands:
            li = "".join(f'<li><span class="check">{I["check"]}</span> {b}</li>' for b in bullets)
            cards += f"""<article class="card model-card">
        <div class="model-card__head"><img src="{logo_src(logo)}" alt="{name}"><h3>{name}</h3></div>
        <ul class="bullets">{li}</ul>
      </article>"""
        out += f"""<section class="section">
  <div class="container">
    <div class="section-header"><div class="section-header__left">
      <span class="tag">Prosto z katalogów 2026</span><h2 class="h-sec">Producenci i modele w tej kategorii</h2>
    </div></div>
    <div class="grid-{min(3, len(brands))}">{cards}</div>
  </div>
</section>
"""

    know = ex.get("know") or []
    if know:
        rows = ""
        for k, (q, a) in enumerate(know):
            cls = ""
            sign = "+"
            rows += f"""<div class="faq__row{cls}">
      <button class="faq__q"><span>{q}</span><span>{sign}</span></button>
      <div class="faq__a">{a}</div>
    </div>"""
        out += f"""<section class="section section--soft">
  <div class="container">
    <div class="section-header"><div class="section-header__left">
      <span class="tag">Baza wiedzy</span><h2 class="h-sec">Warto wiedzieć przed zakupem</h2>
    </div></div>
    <div class="faq">{rows}</div>
  </div>
</section>
"""

    cat_names = {
        "katalog-veka-softline82.pdf": ("VEKA SOFTLINE 82 MD", "Okna PVC klasy A"),
        "katalog-veka-vekamotion82.pdf": ("VEKA VEKAMOTION 82", "Drzwi HST"),
        "katalog-wiked.pdf": ("Wikęd — drzwi do domu 2026", "Kolekcje i linie technologiczne"),
        "katalog-erkado-stalowe.pdf": ("Erkado — drzwi stalowe 2026", "Serie i konstrukcje Thermo"),
        "katalog-erkado-wewnetrzne.pdf": ("Erkado — drzwi wewnętrzne 2026", "Kolekcja Stile"),
        "katalog-dre.pdf": ("DRE — katalog 2026", "Kolekcje i WaterProof"),
        "katalog-porta.pdf": ("Porta — katalog 2026", "10 linii wzorniczych"),
        "katalog-avo-bramy.pdf": ("AVO — bramy garażowe 2026", "Modele i automatyka ADO"),
        "katalog-nice-napedy.pdf": ("Nice — Spider i Spido", "Napędy do bram garażowych"),
    }
    cats = [c for c in (ex.get("cats") or []) if os.path.exists(os.path.join(ROOT, "assets", "katalogi", c))]
    if cats:
        items = ""
        for c in cats:
            t, sub = cat_names.get(c, (c, ""))
            size_mb = os.path.getsize(os.path.join(ROOT, "assets", "katalogi", c)) / 1048576
            items += f"""<a class="catalog" href="assets/katalogi/{c}" download>
      <span class="catalog__icon">{I['pdf']}</span>
      <span class="catalog__info"><strong>{t}</strong><span>{sub}</span></span>
      <span class="catalog__meta">PDF • {size_mb:.1f} MB</span>
    </a>"""
        out += f"""<section class="section">
  <div class="container">
    <div class="section-header"><div class="section-header__left">
      <span class="tag">Do pobrania</span><h2 class="h-sec">Katalogi tej kategorii</h2>
    </div></div>
    <div class="stack">{items}</div>
  </div>
</section>
"""
    return out


def product_page(slug, meta):
    adv = "".join(f"""<div class="adv"><span class="adv__icon">{I[ic]}</span>
      <div><h3>{t}</h3><p>{d}</p></div></div>""" for t, d, ic in meta["adv"])

    rows = ""
    for k, r in enumerate(meta["rows"]):
        title, intro, bullets, img = r
        li = "".join(f'<li><span class="check">{I["check"]}</span> {b}</li>' for b in bullets)
        intro_html = f'<p>{intro}</p>' if intro else ""
        media = f'<div><img src="assets/img/{img}.jpg" alt="{title}" loading="lazy"></div>'
        sub = SUB_SLUGS.get((slug, k))
        sub_link = f' <a class="btn btn--more btn--sm" href="{sub}.html">Więcej o tym rozwiązaniu {I["arrow"]}</a>' if sub else ""
        text = f"""<div class="subrow__text">
        <h2><a href="{sub}.html">{title}</a></h2>
        {intro_html}
        <ul class="bullets">{li}</ul>
        <div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn--primary btn--sm" href="kontakt.html">Zapytaj o wycenę {I['arrow']}</a>{sub_link}</div>
      </div>"""
        rows += f'<div class="subrow{" subrow--flip" if k % 2 else ""}">{media if k % 2 == 0 else text}{text if k % 2 == 0 else media}</div>'

    rel = ""
    for s in meta["related"]:
        rel += f"""<a href="{s}.html"><article class="card">
        <img src="assets/img/{PROD_IMG[s]}.jpg" alt="{PROD_LABEL[s]}" style="height:150px;object-fit:cover;border-radius:var(--r-md)">
        <div><h3>{PROD_LABEL[s]}</h3></div>
        <span class="card__more">Zobacz ofertę {I['arrow']}</span>
      </article></a>"""

    prod_logos = "".join(
        f'<img src="assets/img/partners/{p}.svg?v={ASSET_VER}" alt="{p}">'
        for p in meta.get("producers", []))
    producers_bar = (f'<div class="producer-strip"><div class="container producer-strip__inner">'
                     f'<span>Producenci w tej kategorii:</span>{prod_logos}</div></div>') if prod_logos else ""

    extras_html = product_extras_html(slug)

    body = pagehero(meta["hero"], meta["h1"], meta["intro"], PROD_LABEL[slug])
    body += producers_bar
    body += f"""<section class="advantages"><div class="container advantages__inner">{adv}</div></section>

<section class="section"><div class="container">{rows}</div></section>

{extras_html}
{cta("Doradztwo i wycena", "Planujesz inwestycję budowlaną?",
     "Skontaktuj się z nami — doradzimy technicznie i przygotujemy kalkulację cenową.")}

<section class="section related">
  <div class="container">
    <h2 class="h-sec" style="margin-bottom:32px">Sprawdź również inne systemy</h2>
    <div class="grid-3">{rel}</div>
  </div>
</section>
"""
    write(f"{slug}.html", head(meta["title"], meta["desc"]) + nav(slug) + body + footer())


PRODUCT_DATA = {
"okna": dict(
  hero="al39", h1="Okna PVC i aluminiowe — VEKA i Aluprof", title="Okna PVC VEKA i aluminiowe Aluprof | PROMYK Wieluń",
  desc="Okna PVC VEKA Softline 82 MD i 70 AD, drzwi HST VEKAMOTION 82 oraz aluminiowe Aluprof MB-86N. Parametry techniczne, ciepły montaż, Wieluń.",
  intro="Certyfikowane systemy VEKA (PVC, klasa A) i Aluprof (aluminium). Montaż warstwowy zgodny z wytycznymi ITB.",
  producers=["veka", "aluprof"],
  adv=[("Energooszczędność", "Uw od 0,67 W/m²K przy pakiecie 3-szybowym Ug = 0,5", "thermo"),
       ("Klasa A profili", "Ścianki zewnętrzne min. 2,8 mm wg PN-EN 12608", "shield"),
       ("Kolorystyka", "Ponad 50 oklein: dekory drewnopodobne, RAL, VEKA Spectral", "palette")],
  rows=[("VEKA SOFTLINE 82 MD", None,
         ["Głębokość zabudowy 82 mm, 7 komór, profil klasy A",
          "Uw od 0,67 W/m²K (pakiet 3-szybowy Ug = 0,5, ciepła ramka)",
          "3 płaszczyzny uszczelnienia z uszczelką środkową (MD)",
          "Okucia obwiedniowe z zaczepami antywyważeniowymi, opcja RC2"], "al38"),
        ("VEKA SOFTLINE 70 AD", None,
         ["Głębokość zabudowy 70 mm, 5 komór, profil klasy A",
          "Uw od 0,88 W/m²K przy pakiecie 2-szybowym Ug = 1,0",
          "2 uszczelki odbojowe (AD)",
          "Sprawdzony system do wymiany stolarki w budynkach istniejących"], "abm_okno2"),
        ("VEKAMOTION 82 (HST)", None,
         ["Drzwi podnoszono-przesuwne — konstrukcje do 6,5 m szerokości",
          "Uw od 0,83 W/m²K, próg bezbarierowy 0 mm",
          "Wózki jezdne przenoszące skrzydła do 400 kg",
          "Opcja napędu elektrycznego (VEKAMOTION 82 Max)"], "al25"),
        ("Aluprof MB-86N", None,
         ["Aluminium z przekładką termiczną 34 mm i wkładami Aero",
          "Uw od 0,72 W/m²K, konstrukcje do 2,9 m wysokości",
          "Wąskie profile — maksymalna powierzchnia szklenia",
          "Wersje ST / SI / Aero, opcja ukrytego skrzydła"], "al39")],
  related=["rolety-zewnetrzne", "moskitiery", "oslony-wewnetrzne"]),

"drzwi-zewnetrzne": dict(
  hero="wiked22", h1="Drzwi zewnętrzne — Wikęd i Aluprof", title="Drzwi zewnętrzne Wikęd (Termo Prestige, Premium) i Aluprof | PROMYK",
  desc="Drzwi stalowe Wikęd Premium 54 i Termo Prestige 72, aluminiowe Aluprof MB-86 i panele HPL. Klasa RC2/RC3, Ud od 0,71 W/m²K. Wieluń.",
  intro="Linie Wikęd Premium i Termo Prestige oraz aluminiowe Aluprof — parametry potwierdzone badaniami, klasy RC2/RC3.",
  producers=["wiked", "erkado", "mk-door", "aluprof"],
  adv=[("Bezpieczeństwo", "Klasa antywłamaniowa RC2 / RC3, zamki listwowe 3-punktowe", "lock"),
       ("Termoizolacja", "Ud od 0,71 W/m²K — spełnia wymogi programu Czyste Powietrze", "thermo"),
       ("Wzornictwo", "Ponad 100 wzorów przetłoczeń, przeszkleń i naświetli", "sparkle")],
  rows=[("Wikęd Termo Prestige 72", None,
         ["Skrzydło 72 mm z wypełnieniem pianą poliuretanową",
          "Ud od 0,71 W/m²K — domy pasywne i program Czyste Powietrze",
          "Ościeżnica z przegrodą termiczną, ciepły próg z uszczelką EPDM",
          "Aplikacje inox, pochwyty, przeszklenia z szybą bezpieczną P4"], "wiked51"),
        ("Wikęd Premium 54", None,
         ["Skrzydło 54 mm, blacha ocynkowana malowana proszkowo",
          "Zamek listwowy 3-punktowy + wkładki klasy C w standardzie",
          "Ud od 1,1 W/m²K, uszczelki obwodowe EPDM",
          "Najlepszy stosunek parametrów do ceny w ofercie"], "wiked35"),
        ("Drzwi aluminiowe Aluprof MB-86", None,
         ["Panel zlicowany obustronnie z ościeżnicą",
          "Przekładki termiczne — Ud od 0,9 W/m²K",
          "Pochwyty do 1,8 m, opcja czytnika linii papilarnych i Smart Home",
          "Konstrukcje ponadwymiarowe do 2,4 m wysokości"], "wiked92"),
        ("Drzwi z panelem HPL", None,
         ["Okładzina HPL gr. 2 mm — odporna na UV, wilgoć i zarysowania",
          "Dekory drewnopodobne i jednolite, struktury szczotkowane",
          "Powłoka bezobsługowa — czyszczenie wodą z detergentem",
          "Polecane przy ekspozycji południowej i ciemnych kolorach"], "wiked26")],
  related=["drzwi-wewnetrzne", "okna", "moskitiery"]),

"drzwi-wewnetrzne": dict(
  hero="dre_saraeco2", h1="Drzwi wewnętrzne DRE", title="Drzwi wewnętrzne DRE — Nestor, Binito, Sara Eco, Estra | PROMYK",
  desc="Drzwi wewnętrzne DRE: przylgowe i bezprzylgowe (Nestor, Berge, Binito, Sara Eco 2), przesuwne (Estra 5, Enter Solid) i techniczne (Solid RC2, Forca).",
  intro="Pełna oferta polskiego lidera DRE — od klasyki po systemy bezprzylgowe i przesuwne. Pomiar i montaż naszymi ekipami.",
  producers=["dre", "porta", "erkado"],
  adv=[("Lider rynku", "DRE — największy polski producent drzwi wewnętrznych", "shield"),
       ("Wybór wzorów", "Kolekcje: Nestor, Binito, Estra, Vetro, Nova i inne", "palette"),
       ("Montaż", "Ościeżnice regulowane, montaż w tunelu lub na opasce", "ruler")],
  rows=[("Drzwi przylgowe i bezprzylgowe", "Skrzydła ramiakowe i płytowe w wykończeniach CPL, ekoszpon i lakier.",
         ["Bezprzylgowe: ukryte zawiasy, zamek magnetyczny, skrzydło zlicowane z ościeżnicą",
          "Popularne modele: Nestor, Berge, Binito 50, Sara Eco 2, Nova",
          "Okleiny CPL 0,2–0,7 mm odporne na ścieranie, szyby matowe hartowane"], "dre_nestor11"),
        ("Kolekcje dekoracyjne", "Modele z intarsjami, ryflowaniem i przeszkleniami.",
         ["Modele: City 2 (złote intarsje), Vetro E (szkło), Estra 13, Hampton",
          "Wysokości do 2,2 m, skrzydła zmiennej wysokości (Modern 30)",
          "Struktury synchroniczne — usłojenie wyczuwalne pod palcami"], "dre_saraeco"),
        ("Drzwi przesuwne", "Systemy naścienne z maskownicą lub chowane w ścianę.",
         ["Systemy DRE: Estra 5 przesuwne, Enter Solid 23 + Galeria 50",
          "Cichy domyk soft-close w standardzie",
          "Skrzydła do 100 cm — podział przestrzeni bez utraty miejsca"], "dre_seco1"),
        ("Drzwi techniczne", "Wzmocnione skrzydła o podwyższonych parametrach.",
         ["Solid RC2 — klasa antywłamaniowa RC2, wejścia do mieszkań",
          "Forca — izolacyjność akustyczna Rw do 32 dB, gabinety i sypialnie",
          "Wersje o podwyższonej odporności na wilgoć — łazienki, kotłownie"], "dre_binito10")],
  related=["drzwi-zewnetrzne", "okna", "oslony-wewnetrzne"]),

"rolety-zewnetrzne": dict(
  hero="al30_rol", h1="Rolety zewnętrzne Aluprof", title="Rolety zewnętrzne Aluprof — nadstawne SKT, podtynkowe SP, adaptacyjne SK | PROMYK",
  desc="Rolety zewnętrzne Aluprof: nadstawne SKT Opoterm, podtynkowe SP, adaptacyjne SK/SK45. Pancerz PA39/PA45, napędy Somfy io i Nice.",
  intro="Systemy Aluprof z pancerzem aluminiowym wypełnionym pianką PU i automatyką Somfy / Nice.",
  producers=["aluprof", "somfy", "nice"],
  adv=[("Termoizolacja", "Redukcja strat ciepła przez okno do 30%", "thermo"),
       ("Bezpieczeństwo", "Blokady przeciwpodważeniowe i wieszaki sztywne", "lock"),
       ("Automatyka", "Napędy Somfy io / Nice, aplikacja i czujniki pogodowe", "cog")],
  rows=[("Nadstawne — Aluprof SKT Opoterm", None,
         ["Skrzynka z Neoporu montowana na oknie na etapie budowy",
          "Docieplona skrzynka — bez mostków termicznych nad oknem",
          "Rewizja od dołu, opcja zintegrowanej moskitiery w prowadnicy",
          "Pancerz PA39 / PA45 z pianką poliuretanową"], "al30_rol"),
        ("Podtynkowe — Aluprof SP / SP-E", None,
         ["Skrzynka kryta tynkiem — niewidoczna w elewacji",
          "Montaż w nadprożu, bez ingerencji w profil okna",
          "Dedykowane do budynków energooszczędnych i pasywnych",
          "Dostęp serwisowy przez klapę rewizyjną"], "al31_rol"),
        ("Adaptacyjne — Aluprof SK, SK45, SKO-P", None,
         ["Montaż na elewacji lub we wnęce — bez prac murarskich",
          "Skrzynki ścięte 45° (SK45), półokrągłe (SKO-P), proste (SK)",
          "Pancerz aluminiowy z pianką PU, prowadnice z uszczelką szczotkową",
          "Kolory RAL i drewnopodobne spójne ze stolarką"], "al41"),
        ("Sterowanie — Somfy io / Nice", None,
         ["Napędy radiowe Somfy io-homecontrol i Nice Era",
          "Czujniki słońca, wiatru i temperatury — praca automatyczna",
          "Centrale TaHoma / Yubii: aplikacja, harmonogramy, geolokalizacja",
          "Wyłączniki naścienne i piloty wielokanałowe"], "al35_rol")],
  related=["okna", "oslony-zewnetrzne", "moskitiery"]),

"pergole": dict(
  hero="pergola1", h1="Pergole bioklimatyczne i tarasowe Selt", title="Pergole bioklimatyczne Selt — lamele 0–135°, screeny ZIP | PROMYK Wieluń",
  desc="Pergole bioklimatyczne Selt z lamelami 0–135°, pergole tarasowe z dachem tkaninowym i wolnostojące. LED, promienniki, screeny ZIP.",
  intro="Konstrukcje z ekstrudowanego aluminium (Selt) — lamele obrotowe 0–135°, wysoka odporność na wiatr i śnieg.",
  producers=["selt", "somfy"],
  adv=[("Regulacja", "Lamele obrotowe 0–135° — dozowanie światła i wentylacji", "sun"),
       ("Wytrzymałość", "Aluminium ekstrudowane, odporność na silny wiatr", "shield"),
       ("Rozbudowa", "Screeny ZIP, przeszklenia, LED i promienniki IR", "cog")],
  rows=[("Pergole bioklimatyczne", None,
         ["Lamele aluminiowe sterowane elektrycznie w zakresie 0–135°",
          "Po zamknięciu dach w pełni wodoszczelny",
          "Odprowadzenie wody rynnami zintegrowanymi w słupach",
          "Moduły łączone — zadaszenia ponad 30 m²"], "pergola1"),
        ("Pergole tarasowe (dach tkaninowy)", None,
         ["Tkanina techniczna odporna na UV, zwijana elektrycznie",
          "Konstrukcja dostawiana do ściany lub wolnostojąca",
          "Prowadnice z odwodnieniem, kolory RAL strukturalne",
          "Baza pod screeny boczne ZIP i przeszklenia"], "al25"),
        ("Pergole wolnostojące", None,
         ["Konstrukcja samonośna — taras, ogród, strefa przy basenie",
          "Duże rozpiętości bez podpór pośrednich",
          "Kotwienie do płyty lub stóp fundamentowych",
          "Moduły łączone szeregowo"], "al26"),
        ("Wyposażenie", None,
         ["Oświetlenie LED w lamelach i słupach (ściemnialne)",
          "Promienniki podczerwieni na chłodne wieczory",
          "Screeny ZIP z tkaniny serge — osłona przed wiatrem i słońcem",
          "Sterowanie Somfy io: pilot, aplikacja, czujniki pogodowe"], "al35_rol")],
  related=["markizy", "oslony-zewnetrzne", "rolety-zewnetrzne"]),

"bramy-garazowe": dict(
  hero="brama_antracyt_lampy", h1="Bramy garażowe segmentowe i roletowe", title="Bramy garażowe segmentowe (panel 40–60 mm) i roletowe, napędy Nice i Somfy | PROMYK",
  desc="Bramy segmentowe z panelem 40–60 mm z pianką PU, bramy roletowe aluminiowe, napędy Nice/Somfy, drzwi boczne w kolorze bramy.",
  intro="Bramy segmentowe (panel 40–60 mm z pianką PU) i roletowe, z napędami Nice / Somfy.",
  producers=["avo", "nice", "aluprof", "somfy"],
  adv=[("Bezpieczeństwo", "Zabezpieczenie przed pęknięciem sprężyn i opadnięciem bramy", "lock"),
       ("Izolacja", "Panel 40–60 mm z pianką poliuretanową", "thermo"),
       ("Napędy", "Nice / Somfy: pasek kevlarowy, amperometryka, aplikacja", "cog")],
  rows=[("Bramy segmentowe", None,
         ["Panel stalowy 40 lub 60 mm wypełniony pianką poliuretanową",
          "Przetłoczenia: wysokie, kasetony, gładkie; okleiny drewnopodobne",
          "Podwójne uszczelnienie obwodowe, próg z EPDM",
          "Opcje: przeszklenia, drzwi przejściowe, kratki wentylacyjne"], "brama_avo_dom"),
        ("Bramy roletowe", None,
         ["Pancerz aluminiowy z pianką PU nawijany na wał w skrzynce",
          "Zabudowa od 205 mm — garaże z niskim nadprożem",
          "Napęd rurowy z awaryjnym otwieraniem korbą w standardzie",
          "Prowadnice z uszczelką szczotkową"], "brama_4"),
        ("Napędy i automatyka Nice / Somfy", None,
         ["Przeniesienie paskiem kevlarowym — cicha praca",
          "Amperometryczne wykrywanie przeszkód i fotokomórki",
          "Nice Yubii / Somfy TaHoma: aplikacja, sterowanie głosowe",
          "Piloty z kodem dynamicznym, klawiatury kodowe"], "brama_antracyt"),
        ("Drzwi boczne", None,
         ["Panel identyczny jak w bramie — spójne przetłoczenia i kolor",
          "Ciepła ościeżnica aluminiowa z przegrodą termiczną",
          "Zamek wielopunktowy, samozamykacz w opcji",
          "Wymiary na zamówienie"], "wiked67")],
  related=["okna", "drzwi-zewnetrzne", "rolety-zewnetrzne"]),

"markizy": dict(
  hero="katalog/markiza-palladio-taras", h1="Markizy tarasowe i balkonowe Selt", title="Markizy tarasowe Selt — kaseta pełna, wysięg do 4 m, Somfy | PROMYK Wieluń",
  desc="Markizy tarasowe Selt w pełnej kasecie (wysięg do 4 m), balkonowe i pionowe. Tkanina akrylowa 300 g/m², automatyka Somfy.",
  intro="Markizy Selt z tkaniną akrylową 300 g/m² i napędami Somfy z czujnikami pogodowymi.",
  producers=["selt", "somfy"],
  adv=[("Ochrona", "Redukcja nagrzewania tarasu i wnętrza, filtr UV", "sun"),
       ("Automatyka", "Czujnik wiatru zwija markizę automatycznie", "wind"),
       ("Tkaniny", "Akryl 300 g/m² impregnowany — odporny na płowienie", "shield")],
  rows=[("Markizy tarasowe (kaseta pełna)", "Poszycie i ramiona chowane w zamkniętej kasecie aluminiowej.",
         ["Wysięg ramion do 4 m, szerokości do 7 m (łączone do 12 m)",
          "Regulacja kąta nachylenia 5–40°",
          "Napęd Somfy w standardzie, opcja listwy LED w kasecie"], "katalog/markiza-palladio-dom"),
        ("Markizy balkonowe i półkasety", "Lżejsze systemy do balkonów i mniejszych tarasów.",
         ["Konstrukcja aluminiowa, montaż ścienny lub sufitowy",
          "Wysięg do 2,5 m, obsługa korbą lub napędem",
          "Kolekcja ponad 100 tkanin"], "katalog/markiza-australia-balkon"),
        ("Markizy pionowe (przyścienne)", "Osłona krawędzi tarasu przed niskim słońcem i wiatrem.",
         ["Prowadzenie linkowe lub w prowadnicach",
          "Tkaniny akrylowe i screen, opcja okna widokowego",
          "Ochrona prywatności bez zabudowy tarasu"], "katalog/screeny-taras"),
        ("Automatyka Somfy", "Sterowanie i ochrona konstrukcji.",
         ["Czujnik wiatru Eolis — automatyczne zwinięcie przy podmuchach",
          "Czujnik słońca Sunis — automatyczne rozwijanie",
          "Pilot Telis lub aplikacja TaHoma"], "al35_rol")],
  related=["pergole", "oslony-zewnetrzne", "rolety-zewnetrzne"]),

"oslony-wewnetrzne": dict(
  hero="plisy", h1="Osłony wewnętrzne — żaluzje, plisy, rolety", title="Żaluzje aluminiowe, plisy i rolety wewnętrzne | PROMYK Wieluń",
  desc="Żaluzje aluminiowe 25/50 mm, plisy dwukierunkowe, rolety w kasecie, dzień-noc, rzymskie, verticale i żaluzje bambusowe. Pomiar i montaż.",
  intro="Osłony szyte na wymiar — od żaluzji 25/50 mm i plis po rolety dzień-noc i verticale.",
  producers=[],
  adv=[("Na wymiar", "Produkcja pod wymiar każdej wnęki i skrzydła", "ruler"),
       ("Regulacja światła", "Od pełnego zaciemnienia (blackout) po delikatne rozproszenie", "sun"),
       ("Montaż", "Bezinwazyjny na skrzydle, we wnęce lub na ścianie", "cog")],
  rows=[("Żaluzje aluminiowe", None,
         ["Lamele 25 mm (standard) i 50 mm (styl loftowy)",
          "Odporne na wilgoć — kuchnie i łazienki",
          "Obsługa sznurkiem lub łańcuszkiem, opcja napędu elektrycznego",
          "Kolory matowe, perforowane i metaliczne"], "al27"),
        ("Plisy", None,
         ["System dwukierunkowy góra-dół — zasłonisz dowolny fragment szyby",
          "Montaż bezinwazyjny na skrzydle, także okna dachowe i trapezowe",
          "Tkaniny transparentne, przyciemniające i blackout z powłoką perłową",
          "Prowadzenie żyłkowe — plisa nie odstaje przy uchyle"], "plisy"),
        ("Rolety materiałowe (w kasecie i wolnowiszące)", None,
         ["Kaseta z prowadnicami — brak prześwitów przy krawędziach",
          "Tkaniny blackout 100% — do sypialni",
          "Tkaniny transparentne i dekoracyjne"], "al29"),
        ("Rolety dzień-noc", None,
         ["Naprzemienne pasy transparentne i zaciemniające",
          "Płynna regulacja światła bez podnoszenia rolety",
          "Kasety w kolorach stolarki"], "al28"),
        ("Rolety rzymskie", None,
         ["Miękkie fałdy tkaniny, demontaż do prania",
          "Tkaniny naturalne: len, bawełna, welur",
          "Szycie na wymiar"], "al38"),
        ("Żaluzje pionowe (verticale)", None,
         ["Pasy 89 / 127 mm z regulacją kąta obrotu",
          "Do dużych przeszkleń i biur",
          "Tkaniny trudnopalne z atestem"], "al26"),
        ("Żaluzje drewniane i bambusowe", None,
         ["Lamele drewniane 25/50 mm i lekkie bambusowe",
          "Naturalne barwienie, drabinka taśmowa w opcji",
          "Do gabinetów i wnętrz klasycznych"], "abm_okno1")],
  related=["okna", "moskitiery", "oslony-zewnetrzne"]),

"oslony-zewnetrzne": dict(
  hero="katalog/screeny-taras", h1="Osłony zewnętrzne — refleksole, żaluzje fasadowe, sunbreaker",
  title="Refleksole ZIP, żaluzje fasadowe C-80/Z-90 i sunbreaker | PROMYK Wieluń",
  desc="Refleksole screen ZIP, żaluzje fasadowe C-80/Z-90, sunbreakery i moskitiery plisowane. Automatyka Somfy. Wieluń i okolice.",
  intro="Osłony zatrzymujące ciepło przed szybą (Selt / Aluprof) — najskuteczniejsza ochrona przed przegrzewaniem.",
  producers=["selt", "aluprof", "somfy"],
  adv=[("Skuteczność", "Zatrzymanie większości energii słonecznej przed szybą", "sun"),
       ("Energooszczędność", "Mniejsze zużycie klimatyzacji latem", "thermo"),
       ("Automatyka", "Somfy io + czujniki nasłonecznienia", "cog")],
  rows=[("Refleksole (screen ZIP)", "Pionowe rolety z tkaniny technicznej w prowadnicach ZIP.",
         ["Tkanina screen (serge) — widok na zewnątrz zachowany, redukcja olśnienia",
          "Prowadnice ZIP: tkanina naprężona, wysoka odporność na wiatr",
          "Szczelne prowadzenie działa również jak moskitiera",
          "Kasety 85–150 mm, szerokości do 6 m"], "katalog/screeny-elewacja"),
        ("Żaluzje fasadowe", "Zewnętrzne lamele aluminiowe o przekroju C lub Z.",
         ["Lamele C-80 / Z-90 lakierowane proszkowo",
          "Płynna regulacja kąta — światło bez olśnienia",
          "Prowadzenie linkowe lub szynowe, zabudowa podtynkowa",
          "Standard w budynkach biurowych klasy A"], "al41"),
        ("Sunbreaker (łamacze światła)", "Stałe lub ruchome lamele wielkogabarytowe.",
         ["Lamele eliptyczne, duże rozpiętości",
          "Wersje stałe i obrotowe (do 90°)",
          "Element architektoniczny elewacji — montaż pionowy lub poziomy"], "al26"),
        ("Moskitiery plisowane (do dużych przeszkleń)", "Harmonijkowa siatka do drzwi HST i portfenetrów — pełna oferta moskitier w osobnej kategorii.",
         ["Prowadnica dolna 5 mm — przejście bez progu",
          "Zatrzymanie siatki w dowolnym punkcie (bez sprężyny)",
          "Duże szerokości przy zabudowie dwustronnej"], "al25")],
  related=["moskitiery", "rolety-zewnetrzne", "pergole"]),

"moskitiery": dict(
  hero="al26", h1="Moskitiery na wymiar", title="Moskitiery ramkowe, drzwiowe, rolowane i plisowane | PROMYK Wieluń",
  desc="Moskitiery na wymiar: ramkowe, drzwiowe z samozamykaczem, rolowane w kasecie i plisowane do HST. Siatka fiberglass i pet screen. Wieluń.",
  intro="Moskitiery z naszej własnej produkcji — na wymiar do każdego typu okna i drzwi — siatka fiberglass, aluminiowa lub wzmocniona pet screen.",
  producers=[],
  adv=[("Ochrona", "Siatka o drobnym oczku — bariera także dla małych owadów", "bug"),
       ("Wentylacja", "Swobodny przepływ powietrza i światła", "wind"),
       ("Na wymiar", "Rama dopasowana do wnęki — bez szczelin montażowych", "ruler")],
  rows=[("Moskitiery ramkowe", "Do okien rozwiernych i uchylnych.",
         ["Rama aluminiowa, montaż na uchwyty obrotowe — bez wiercenia w oknie",
          "Demontaż na zimę w kilka sekund",
          "Opcja siatki pet screen odpornej na pazury zwierząt"], "moskitiera_mrs"),
        ("Moskitiery drzwiowe", "Otwierane, na zawiasach — balkon i taras.",
         ["Ościeżnica własna z samozamykaczem",
          "Uszczelka szczotkowa na obwodzie",
          "Magnesy domykające, rygiel w opcji"], "al39"),
        ("Moskitiery rolowane", "Zwijane do kasety górnej lub bocznej.",
         ["Kaseta 42–50 mm, prowadnice ze szczotką",
          "Hamulec spowalniający zwijanie",
          "Wersja dachowa do okien połaciowych"], "al28"),
        ("Moskitiery plisowane", "Harmonijkowe — do drzwi HST i dużych przeszkleń.",
         ["Prowadnica dolna 5 mm — przejście bez potykania",
          "Siatka zatrzymuje się w dowolnym położeniu",
          "Duże szerokości przy zabudowie dwustronnej"], "al25")],
  related=["okna", "rolety-zewnetrzne", "oslony-wewnetrzne"]),
}


# Rozszerzenia podstron produktowych: specs (tabela), brands (producenci+modele),
# know (Warto wiedzieć — accordion), cats (katalogi PDF tej kategorii).
PRODUCT_EXTRAS = {
"okna": dict(
  specs=dict(title="Porównanie systemów okiennych", cols=["System", "Materiał", "Głębokość", "Komory", "Uw od", "Zastosowanie"],
    rows=[["VEKA SOFTLINE 82 MD", "PVC kl. A", "82 mm", "7", "0,67 W/m²K", "domy energooszczędne i pasywne"],
          ["VEKA SOFTLINE 70 AD", "PVC kl. A", "70 mm", "5", "0,88 W/m²K", "budownictwo standardowe, wymiana stolarki"],
          ["VEKAMOTION 82 (HST)", "PVC kl. A", "82 mm", "wielokomorowy", "0,76 W/m²K (Ud)", "przeszklenia tarasowe do 6,5 m"],
          ["Aluprof MB-86N", "aluminium", "86 mm", "przekładka 34 mm", "0,72 W/m²K", "duże przeszklenia, dom nowoczesny"]]),
  brands=[
    ("veka", "VEKA", [
      "Profile klasy A wg DIN EN 12608 — ścianka zewnętrzna 3 mm (±0,2)",
      "SOFTLINE 82 MD: Uf do 1,0 W/m²K, RC2 wg DIN EN 1627",
      "VEKAMOTION 82: rama skrzydła stałego tylko 86 mm, opcja napędu Max",
      "Powierzchnie: 60+ folii dekoracyjnych, VEKA Spectral ultramat, panele alu"]),
    ("aluprof", "Aluprof", [
      "MB-86N — system okienno-drzwiowy z wkładami Aero",
      "Konstrukcje do 2,9 m wysokości, opcja ukrytego skrzydła",
      "Kolory: pełna paleta RAL, anody, dekory drewnopodobne"])],
  know=[
    ("Co oznaczają współczynniki Uw, Uf i Ug?",
     "Uw opisuje izolacyjność całego okna, Uf — samej ramy, a Ug — pakietu szybowego. Im niższa wartość, tym cieplejsze okno. Warunki techniczne WT 2021 wymagają dla okien pionowych Uw ≤ 0,9 W/m²K — wszystkie oferowane przez nas systemy spełniają ten wymóg z zapasem."),
    ("Czym różni się profil klasy A od klasy B?",
     "Norma PN-EN 12608 dzieli profile PVC według grubości ścianek: klasa A to ścianki zewnętrzne ≥ 2,8 mm, klasa B — ≥ 2,5 mm. Grubsze ścianki oznaczają sztywniejsze konstrukcje, mocniejsze zgrzewy naroży i lepsze osadzenie okuć — dlatego montujemy wyłącznie profile klasy A."),
    ("Pakiet 2-szybowy czy 3-szybowy?",
     "Pakiet 3-szybowy (Ug 0,5–0,7) ogranicza straty ciepła o ok. 30–40% względem 2-szybowego (Ug 1,0) i poprawia komfort zimą przy dużych przeszkleniach. Do tego ciepła ramka dystansowa obniża współczynnik psi na krawędzi szyby i ryzyko wykraplania pary."),
    ("Na czym polega ciepły montaż warstwowy?",
     "To montaż z trzema warstwami uszczelnienia: taśma paroszczelna od wewnątrz, piana termoizolacyjna w środku i taśma paroprzepuszczalna od zewnątrz. Eliminuje mostki termiczne i przecieki. W ścianach ocieplonych stosujemy też wysunięcie okna w warstwę ocieplenia na konsolach."),
    ("Co daje odporność RC2?",
     "Okno w standardzie RC2 ma okucia z zaczepami antywyważeniowymi (grzybkowymi), klamkę z kluczykiem i szybę laminowaną P4. Konstrukcja wytrzymuje próbę włamania narzędziami przez min. 3 minuty — to standard rekomendowany dla parterów i domów jednorodzinnych."),
    ("Czy potrzebuję nawiewników?",
     "Przy wentylacji grawitacyjnej szczelne okna wymagają nawiewników (ciśnieniowych lub higrosterowanych), aby zapewnić dopływ świeżego powietrza. Przy rekuperacji nawiewniki są zbędne. Dobieramy je na etapie zamówienia — montaż fabryczny w ramie."),
  ],
  cats=["katalog-veka-softline82.pdf", "katalog-veka-vekamotion82.pdf"]),

"drzwi-zewnetrzne": dict(
  specs=dict(title="Linie technologiczne drzwi stalowych Wikęd", cols=["Linia", "Charakterystyka", "Dla kogo"],
    rows=[["Prima", "ekonomiczna konstrukcja stalowa, zamek listwowy", "budżetowa wymiana drzwi"],
          ["Optimum", "grubsze skrzydło, lepsze wypełnienie PU", "standard w nowym domu"],
          ["Termo Prestige", "Ud od 0,71 W/m²K, ciepła ościeżnica i próg", "domy energooszczędne, Czyste Powietrze"],
          ["Alu Hybrid", "skrzydło aluminiowe, panel zlicowany", "architektura premium"]]),
  brands=[
    ("wiked", "Wikęd", [
      "Kolekcje 2026: Rustik (Masterline/Woodline), 3D, Softline, Future Inox, Glass, Royal, Klasyk",
      "Drzwi na wymiar — szerokość 70–100 cm co 1 cm",
      "Przeszklenia Glass Frame, ramki Black/Inox, klamki RC",
      "Naświetla boczne i górne, drzwi dwuskrzydłowe"]),
    ("erkado", "Erkado — drzwi stalowe", [
      "Konstrukcje Thermo 64 / Thermo 78 / Thermo Hot 78 / Thermo Hot 88 (mm)",
      "Serie: Horn, Langen, Trebur, Wels, Bazylea, Arendal, Lahti",
      "Okleina PVC odporna na UV z wieloletnią gwarancją",
      "Panele ozdobne inox, przeszklenia reflex, lustro weneckie"]),
    ("aluprof", "Aluprof", [
      "MB-86 — drzwi aluminiowe z panelem zlicowanym",
      "Pochwyty do 1,8 m, czytnik linii papilarnych, Smart Home",
      "Konstrukcje ponadwymiarowe do 2,4 m wysokości"])],
  know=[
    ("Ud — jak ciepłe powinny być drzwi wejściowe?",
     "Warunki techniczne wymagają Ud ≤ 1,3 W/m²K. Linie premium (Wikęd Termo Prestige, Erkado Thermo Hot 88) osiągają Ud od 0,71 W/m²K — takie drzwi kwalifikują się do dofinansowania w programie Czyste Powietrze i realnie obniżają straty ciepła w wiatrołapie."),
    ("Klasa RC2 i RC3 w drzwiach — co oznacza?",
     "RC określa odporność na włamanie wg PN-EN 1627. RC2 wytrzymuje próbę wyważenia narzędziami prostymi (ok. 3 min), RC3 — łomem (ok. 5 min). Składają się na to: zamki listwowe wielopunktowe, bolce antywyważeniowe, wkładki kl. C i szyby P4."),
    ("Jak dobrać szerokość drzwi?",
     "Standard w nowych domach to „dziewięćdziesiątka” — 90 cm w świetle przejścia. Przy wymianie mierzy się światło ościeżnicy istniejącej. Wikęd wykonuje skrzydła na wymiar co 1 cm (70–100 cm), więc niestandardowy otwór nie jest problemem."),
    ("Lewe czy prawe?",
     "Patrząc na drzwi od strony zawiasów: zawiasy po lewej = drzwi lewe, po prawej = prawe. Kierunek określa się zawsze od strony, na którą drzwi się otwierają. Przy zamówieniu potwierdzamy kierunek na pomiarze — to wyklucza pomyłki."),
    ("Stal, aluminium czy panel HPL?",
     "Stal to najlepszy stosunek ceny do bezpieczeństwa i sztywności. Aluminium pozwala na skrzydła zlicowane i duże formaty przy niskiej wadze. Panel HPL (2 mm) to najwyższa odporność powłoki na słońce i zarysowania — polecany przy ekspozycji południowej i ciemnych kolorach."),
    ("Czy drzwi wejściowe wymagają zadaszenia?",
     "Producenci warunkują gwarancję powłok ochroną przed bezpośrednim działaniem opadów i słońca — wystarczy daszek lub podcień o odpowiednim wysięgu. Doradzimy minimalne wymiary zadaszenia przy pomiarze."),
  ],
  cats=["katalog-wiked.pdf", "katalog-erkado-stalowe.pdf"]),

"drzwi-wewnetrzne": dict(
  specs=dict(title="Rodzaje wykończeń skrzydeł", cols=["Wykończenie", "Odporność", "Zastosowanie"],
    rows=[["Laminat CPL (0,15–0,7 mm)", "bardzo wysoka na ścieranie i uderzenia", "intensywny ruch, rodziny z dziećmi"],
          ["Laminat akrylowy (0,7–0,8 mm)", "wysoka, głęboki mat lub połysk", "wnętrza premium"],
          ["Folie 3D / DRE-Cell", "podwyższona, struktura drewna 3D", "sypialnie, salony"],
          ["Ekoszpon / Greko", "standardowa, naturalny wygląd", "ekonomiczne aranżacje"],
          ["Lakier UV", "wysoka, kolor bez połysku", "kuchnie i łazienki (AntiFinger)"]]),
  brands=[
    ("dre", "DRE", [
      "Laminaty akrylowe: Ilis, Nella, Vetro D2, Silia",
      "Ramowe: Vetro E Synchro, Estra, Nestor, Auri, Reva, Fosca",
      "Ościeżnica DRE WaterProof — nie odkształca się w kontakcie z wodą",
      "Okleiny Finish / 3D / DRE-Cell / CPL"]),
    ("porta", "Porta", [
      "10 linii wzorniczych w katalogu 2026",
      "Specjalizacje: drzwi akustyczne, wilgocioodporne, ukryte w ścianie",
      "Nr 1 w Polsce i Europie Środkowo-Wschodniej",
      "Produkty testowane w 21 laboratoriach"]),
    ("erkado", "Erkado", [
      "Ramiakowe Stile: Werbena, Jasmin, Laurencja, Frezja, Peonia",
      "Wersje przylgowe, bezprzylgowe i rewersyjne",
      "Okleiny Greko / Premium / CPL z powłoką AntiFinger",
      "Opcja uszczelki opadającej i szkła VSG"])],
  know=[
    ("Przylgowe czy bezprzylgowe?",
     "Drzwi przylgowe mają widoczną felc (uskok) na krawędzi i klasyczne zawiasy — to rozwiązanie uniwersalne i tańsze. Bezprzylgowe licują się z ościeżnicą w jednej płaszczyźnie, mają ukryte zawiasy i zamek magnetyczny — wybierane do wnętrz minimalistycznych."),
    ("Lewe czy prawe — jak określić?",
     "Stań po stronie, na którą otwierają się drzwi: zawiasy po lewej ręce = drzwi lewe, po prawej = prawe. Ten sam standard stosują DRE, Porta i Erkado, więc raz określony kierunek działa dla każdego producenta."),
    ("Jaką ościeżnicę wybrać?",
     "Regulowana obejmuje mur w zakresie kilku centymetrów i maskuje krawędzie tynku — standard w nowych domach. Stała jest tańsza, ale wymaga idealnie równego muru. Do łazienek polecamy DRE WaterProof — testowana na długi kontakt z wodą."),
    ("Jakie wymiary skrzydeł są dostępne?",
     "Typowe szerokości to „60–100” co 10 cm, mierzone w świetle ościeżnicy (norma polska). Do salonu i kuchni rekomendujemy 80–90, do łazienki min. 70 z podcięciem lub tulejami wentylacyjnymi (wymóg WT), do garderoby wystarczy 60."),
    ("Drzwi do łazienki — co jest wymagane?",
     "Przepisy wymagają otworów wentylacyjnych o łącznym przekroju min. 220 cm² (podcięcie, tuleje) oraz skrzydła odpornego na wilgoć. Wybieramy okleiny CPL/lakier i ościeżnicę WaterProof — zestaw odporny na parę i chlapanie."),
    ("Co wyciszy wnętrze?",
     "Skrzydła pełne z wypełnieniem płytą wiórową pełną lub akustyczną (np. Porta akustyczne, Erkado z uszczelką opadającą) osiągają Rw ok. 27–32 dB. Uszczelka opadająca zamyka szczelinę progową — kluczowa przy gabinetach i sypialniach."),
  ],
  cats=["katalog-dre.pdf", "katalog-porta.pdf", "katalog-erkado-wewnetrzne.pdf"]),

"rolety-zewnetrzne": dict(
  specs=dict(title="Który system rolet wybrać?", cols=["System", "Etap montażu", "Skrzynka", "Uwagi"],
    rows=[["Nadstawne (SKT Opoterm)", "budowa / wymiana okien", "na oknie, kryta od zewnątrz", "najlepsza termika, moskitiera w standardzie prowadnic"],
          ["Podtynkowe (SP/SP-E)", "budowa (nadproże)", "niewidoczna pod tynkiem", "czysta elewacja, zero ingerencji w okno"],
          ["Adaptacyjne (SK/SK45)", "budynek istniejący", "widoczna na elewacji / we wnęce", "montaż bez prac murarskich"]]),
  brands=[
    ("aluprof", "Aluprof", [
      "SKT Opoterm — skrzynka z Neoporu, rewizja od dołu",
      "SP / SP-E — systemy podtynkowe do budynków pasywnych",
      "SK, SK45, SKO-P — pełna gama adaptacyjnych",
      "Pancerze PA39 / PA45 z pianką poliuretanową"]),
    ("somfy", "Somfy", [
      "Napędy io-homecontrol z informacją zwrotną",
      "Centrala TaHoma — aplikacja, scenariusze, geolokalizacja",
      "Czujniki Sunis (słońce) i Eolis (wiatr)"]),
    ("nice", "Nice", [
      "Napędy Era z pilotami dwukierunkowymi",
      "Centrala Yubii Home — Z-Wave i Wi-Fi w jednym"])],
  know=[
    ("Jak zbudowana jest roleta zewnętrzna?",
     "Pancerz z lameli aluminiowych wypełnionych pianką PU zwija się na wał w skrzynce; boczne prowadnice z uszczelkami szczotkowymi tłumią pracę i doszczelniają zabudowę. Napęd rurowy siedzi w wale — od zewnątrz widać tylko pancerz i prowadnice."),
    ("Ile ciepła realnie oszczędzają rolety?",
     "Zamknięty pancerz tworzy poduszkę powietrzną przy szybie, ograniczając straty ciepła przez okno do ok. 30%. Latem działa odwrotnie — zatrzymuje promieniowanie słoneczne przed szybą, obniżając temperaturę w pomieszczeniu o kilka stopni bez klimatyzacji."),
    ("Który system do jakiego domu?",
     "Na etapie budowy najlepsze są nadstawne (integracja z oknem, świetna termika) lub podtynkowe (niewidoczne). W budynku wykończonym jedyną nieinwazyjną opcją są adaptacyjne — montowane na elewacji lub we wnęce w jeden dzień, bez tynkowania."),
    ("Sterowanie: przewodowe, radiowe czy smart?",
     "Przewodowe (przełącznik) jest najtańsze, ale wymaga instalacji przed tynkami. Radiowe (Somfy io / Nice Era) można dołożyć zawsze. Smart z centralą TaHoma/Yubii daje aplikację, harmonogramy i współpracę z czujnikami — rolety same reagują na słońce i wiatr."),
    ("Czy roleta może mieć moskitierę?",
     "Tak — w systemach nadstawnych moskitiera rolowana jest zintegrowana w tej samej skrzynce i prowadnicach (osobne prowadzenie), nie zabiera światła i nie wymaga dodatkowego montażu. W adaptacyjnych stosuje się prowadnice łączone."),
  ],
  cats=[]),

"pergole": dict(
  specs=None,
  brands=[
    ("selt", "Selt", [
      "Pergole bioklimatyczne z lamelami 0–135°",
      "Konstrukcje dostawne i wolnostojące, moduły ponad 30 m²",
      "Screeny ZIP, przeszklenia, LED, promienniki"]),
    ("somfy", "Somfy", [
      "Napędy io z czujnikami deszczu i wiatru",
      "Sterowanie pilotem Telis lub aplikacją TaHoma"])],
  know=[
    ("Pergola bioklimatyczna czy tarasowa?",
     "Bioklimatyczna ma obrotowe lamele aluminiowe (0–135°): reguluje światło, wentyluje, a po zamknięciu tworzy szczelny dach. Tarasowa ma dach z tkaniny technicznej zwijany elektrycznie — jest lżejsza optycznie i tańsza, ale nie daje pełnej szczelności zimą."),
    ("Co z wodą podczas deszczu?",
     "W pergolach bioklimatycznych woda spływa z lameli do rynien zintegrowanych w obwodzie dachu i dalej pionami ukrytymi w słupach — taras zostaje suchy, a instalacji nie widać."),
    ("Jakiego fundamentu wymaga pergola?",
     "Konstrukcje dostawne kotwi się chemicznie do płyty tarasu; wolnostojące wymagają stóp fundamentowych pod słupami. Obciążenia (wiatr, śnieg na lamelach) przenoszą słupy — przygotowanie podłoża omawiamy na pomiarze."),
    ("Czy z pergoli można korzystać wiosną i jesienią?",
     "Tak — po doposażeniu w screeny ZIP (osłona przed wiatrem), promienniki podczerwieni i oświetlenie LED pergola działa jak całoroczny pokój zewnętrzny. Elementy można dokładać etapami."),
  ],
  cats=[]),

"bramy-garazowe": dict(
  specs=dict(title="Modele bram segmentowych AVO", cols=["Model", "Powierzchnia", "Charakter"],
    rows=[["AVO Base Line / Base Trend / Base Elegant", "Woodgrain", "ekonomiczne, struktura drewna"],
          ["AVO Line", "Woodgrain", "klasyczne przetłoczenia"],
          ["AVO Trend / Elegant", "Silk (gładka)", "nowoczesne elewacje"],
          ["AVO Elegant ISO 60", "Silk", "panel 60 mm — najwyższa termika"]]),
  brands=[
    ("avo", "AVO", [
      "Panele Woodgrain i Silk; dekory Woodec, Winchester, Złoty Dąb",
      "Lakierowanie: 205 kolorów RAL i 1950 NCS",
      "Automatyka ADO / ADO PRO: 24 V, LED w prowadnicy, KUBE Bluetooth",
      "Prowadzenie także przy bardzo krótkich podjazdach"]),
    ("nice", "Nice", [
      "Spider 1200N: bezszczotkowy, 150 cykli/dobę, bramy do 16,9 m²",
      "Wbudowane Wi-Fi, LED i system antywłamaniowy",
      "Spido 600N: otwarcie w ok. 10 s",
      "Yubii Home / CORE — Alexa, Google Assistant, Siri"]),
    ("somfy", "Somfy", [
      "Napędy Dexxo z paskiem — cicha praca",
      "TaHoma: aplikacja i scenariusze smart home"])],
  know=[
    ("Segmentowa czy roletowa?",
     "Segmentowa (panele chowane pod sufit) daje najlepszą termikę i wygląd, wymaga ok. 10–20 cm nadproża i wolnego sufitu. Roletowa zwija się do skrzynki nad otworem — ratuje garaże z niskim nadprożem lub sufitem zajętym przez instalacje."),
    ("Woodgrain czy Silk?",
     "Woodgrain to tłoczona struktura słojów drewna — maskuje drobne ślady eksploatacji. Silk to powierzchnia idealnie gładka, efektowna w kolorach matowych i dekorach Woodec — wybierana do nowoczesnych elewacji."),
    ("Jak dobrać napęd do bramy?",
     "Liczy się powierzchnia bramy i intensywność użytkowania: do typowej bramy do ok. 10 m² wystarczy Spido 600N lub ADO; przy większych i podwójnych — Spider 800/1200N (do 16,9 m²). Przy kilkunastu cyklach dziennie wybieramy silnik bezszczotkowy (Spider 1200 BLW)."),
    ("Co zabezpiecza bramę przed wypadkiem?",
     "Standard to zabezpieczenie przed pęknięciem sprężyny (blokada opadnięcia skrzydła), amperometryczne wykrywanie przeszkód w napędzie i opcjonalne fotokomórki. Brama zatrzyma się i cofnie po napotkaniu oporu."),
    ("Jakie wymiary podać do wyceny?",
     "Wystarczą: szerokość i wysokość otworu w murze, wysokość nadproża, szerokości przestrzeni bocznych i głębokość garażu. Resztę doprecyzuje pomiar — bramy AVO produkowane są na wymiar."),
  ],
  cats=["katalog-avo-bramy.pdf", "katalog-nice-napedy.pdf"]),

"markizy": dict(
  specs=None,
  brands=[
    ("selt", "Selt", [
      "Markizy tarasowe w pełnej kasecie — wysięg do 4 m",
      "Szerokości do 7 m (sprzęgane do 12 m)",
      "Ponad 100 tkanin akrylowych 300 g/m²"]),
    ("somfy", "Somfy", [
      "Napędy radiowe io w standardzie",
      "Czujniki Eolis (wiatr) i Sunis (słońce)"])],
  know=[
    ("Kaseta pełna, półkaseta czy markiza otwarta?",
     "Pełna kaseta chroni tkaninę i ramiona całkowicie po zwinięciu — najdłuższa żywotność poszycia. Półkaseta osłania tkaninę od góry, jest lżejsza i tańsza. Otwarta sprawdza się pod zadaszeniem, gdzie poszycie nie moknie."),
    ("Akryl czy screen?",
     "Tkanina akrylowa 300 g/m² daje głęboki kolor, pełny cień i wysoką odporność na płowienie — klasyka markiz. Screen przepuszcza część widoku i światła, mniej faluje na wietrze — częściej używany w markizach pionowych."),
    ("Jak duży taras zacieni markiza?",
     "Wysięg ramion do 4 m i szerokość do 7 m pozwalają zacienić ok. 25 m² jedną markizą; większe tarasy obsługują markizy sprzęgane na wspólnym napędzie. Kąt nachylenia reguluje się w zakresie 5–40°."),
    ("Czy markiza wytrzyma wiatr?",
     "Tkanina rozwinięta ma określoną klasę wiatrową — dlatego montujemy czujnik Eolis, który zwija markizę automatycznie po przekroczeniu progu. To warunek bezpiecznej pracy i utrzymania gwarancji przy silniejszych podmuchach."),
  ],
  cats=[]),

"oslony-wewnetrzne": dict(
  specs=dict(title="Którą osłonę wybrać do pomieszczenia?", cols=["Pomieszczenie", "Rekomendacja", "Dlaczego"],
    rows=[["Sypialnia", "roleta blackout w kasecie / plisa blackout", "pełne zaciemnienie bez prześwitów"],
          ["Salon z HST", "plisy dwukierunkowe / verticale", "obsługa dużych przeszkleń"],
          ["Kuchnia, łazienka", "żaluzja aluminiowa / plisa", "odporność na wilgoć, łatwe czyszczenie"],
          ["Gabinet", "żaluzja drewniana / dzień-noc", "praca przy świetle bez olśnienia"],
          ["Okno dachowe", "plisa w prowadnicach", "trzyma się połaci pod kątem"]]),
  brands=[
    ("@logo-promyk.png", "Produkcja własna PROMYK", [
      "Osłony szyte i składane na wymiar w naszej pracowni w Wieluniu",
      "Żaluzje 25/50 mm, plisy, rolety, verticale",
      "Tkaniny: transparentne, dzień-noc, blackout, trudnopalne"])],
  know=[
    ("Plisa czy roleta — co wybrać?",
     "Plisa zasłania dowolny fragment szyby (system góra-dół) i pasuje do nietypowych kształtów — także okien dachowych i trapezów. Roleta jest szybsza w obsłudze i tańsza przy dużych prostokątnych oknach; w wersji kasetowej z prowadnicami daje pełny blackout."),
    ("Czym różni się blackout od tkaniny przyciemniającej?",
     "Blackout ma powłokę nieprzepuszczającą światła (100% zaciemnienia w tkaninie); przyciemniająca tłumi światło, ale nie eliminuje go całkowicie. Do sypialni polecamy blackout w kasecie z prowadnicami — bez smug światła przy krawędziach."),
    ("Czy montaż niszczy okno?",
     "Nie — standardem jest montaż bezinwazyjny: uchwyty zaciskane na skrzydle lub taśma montażowa systemowa. Okno zachowuje gwarancję, a osłonę można zdemontować bez śladów."),
    ("Jak mierzyć okno pod osłony?",
     "Przy montażu we wnęce podaje się szerokość i wysokość wnęki (my odejmujemy luzy); przy montażu na skrzydle — wymiary szyby z listwami. Najbezpieczniej zostawić pomiar nam."),
  ],
  cats=[]),

"oslony-zewnetrzne": dict(
  specs=None,
  brands=[
    ("selt", "Selt", [
      "Refleksole screen z prowadnicami ZIP — do 6 m szerokości",
      "Tkaniny serge o różnym stopniu otwarcia (1–5%)",
      "Kasety 85–150 mm, kolory RAL"]),
    ("aluprof", "Aluprof", [
      "Żaluzje fasadowe C-80 / Z-90",
      "Prowadzenie linkowe lub szynowe, zabudowa podtynkowa"]),
    ("somfy", "Somfy", [
      "Automatyka io z czujnikiem nasłonecznienia",
      "Scenariusze pogodowe w TaHoma"])],
  know=[
    ("Dlaczego osłona zewnętrzna chłodzi lepiej niż wewnętrzna?",
     "Zatrzymuje promieniowanie słoneczne PRZED szybą — energia nie wnika do środka. Osłona wewnętrzna działa dopiero, gdy ciepło już przeszło przez szkło. Różnica temperatury w pomieszczeniu latem sięga kilku stopni."),
    ("Co oznacza stopień otwarcia tkaniny screen?",
     "To procent mikrootworów w splocie (najczęściej 1–5%). Niższy = mocniejsze zaciemnienie i lepsza prywatność; wyższy = więcej światła i wyraźniejszy widok na zewnątrz. Do sypialni wybiera się 1%, do salonu 3–5%."),
    ("Refleksol czy żaluzja fasadowa?",
     "Refleksol (tkanina) zaciemnia płynnie i zachowuje widok — jest lżejszy wizualnie i tańszy. Żaluzja fasadowa (lamele aluminiowe) pozwala kierować światło pod dowolnym kątem i mocniej zaznacza architekturę — standard w biurowcach, coraz częstsza w domach premium."),
    ("Jak osłony znoszą wiatr?",
     "Prowadnice ZIP trzymają tkaninę naprężoną na całym obwodzie — refleksole pracują przy silnym wietrze bez łopotania. Żaluzje fasadowe przy bardzo silnych podmuchach automatycznie się podnoszą (czujnik wiatru) — to standardowe zabezpieczenie systemowe."),
  ],
  cats=[]),

"moskitiery": dict(
  specs=dict(title="Dobór moskitiery do stolarki", cols=["Typ", "Do czego", "Cechy"],
    rows=[["Ramkowa", "okna rozwierne i uchylne", "montaż bez wiercenia, demontaż na zimę"],
          ["Drzwiowa", "balkon, taras, wejście boczne", "zawiasy, samozamykacz, magnesy"],
          ["Rolowana", "okna często otwierane, okna dachowe", "kaseta, chowana gdy niepotrzebna"],
          ["Plisowana", "HST i duże przeszklenia", "niski próg 5 mm, zatrzymuje się w dowolnym punkcie"]]),
  brands=[
    ("@logo-promyk.png", "Produkcja własna PROMYK", [
      "Moskitiery na wymiar z naszej pracowni — także kształty nietypowe",
      "Ramkowe, drzwiowe, rolowane i plisowane w kolorach stolarki",
      "Siatki: fiberglass, aluminiowa, pet screen"])],
  know=[
    ("Jaką siatkę wybrać?",
     "Standardem jest fiberglass (włókno szklane) — trwały i mało widoczny. Siatka aluminiowa jest sztywniejsza, a pet screen (wzmocniony poliester) wytrzymuje pazury psów i kotów. Oczko 1,2×1,2 mm zatrzymuje także drobne owady."),
    ("Czy moskitiera ogranicza światło i widok?",
     "Nieznacznie — dobrej klasy siatka odbiera kilka procent światła. W moskitierach rolowanych i plisowanych siatkę chowa się, gdy nie jest potrzebna, więc zimą i w dni bez owadów okno pozostaje całkowicie odsłonięte."),
    ("Jak czyścić moskitiery?",
     "Wystarczy odkurzacz z miękką końcówką lub przemycie wodą z płynem. Ramkowe zdejmuje się na zimę jednym ruchem (uchwyty obrotowe), rolowane czyści się w miejscu montażu."),
  ],
  cats=[]),
}


# Teksty techniczne podstron 3. poziomu — klucz: slug kategorii, wartość: lista
# akapitów per wiersz rows[] (kolejność zgodna z PRODUCT_DATA).
SUB_DETAILS = {
"okna": [
 ["SOFTLINE 82 MD to flagowy system PVC firmy VEKA o głębokości zabudowy 82 mm i 7 komorach w ramie. Uszczelka środkowa (MD) tworzy trzecią, ciągłą płaszczyznę uszczelnienia — komora przed okuciem pozostaje sucha, co przekłada się na lepszą termikę węzła i trwałość okuć. Profil klasy A (ścianka zewnętrzna 3 mm ±0,2 wg DIN EN 12608) zapewnia sztywne zgrzewy i mocne osadzenie wkrętów okuć.",
  "System przyjmuje pakiety szybowe 2- i 3-szybowe do dużych grubości, w tym szkło bezpieczne P4 i akustyczne. Z pakietem Ug = 0,5 W/m²K i ciepłą ramką okno osiąga Uw do 0,74 W/m²K — wynik odpowiedni dla domów pasywnych. Wzmocnienia stalowe w ramie i skrzydle pozwalają na konstrukcje balkonowe i witryny bez utraty statyki."],
 ["SOFTLINE 70 AD to sprawdzony, 5-komorowy system o głębokości 70 mm z dwiema uszczelkami odbojowymi. Konstrukcyjnie lżejszy od SOFTLINE 82, zachowuje pełną klasę A profili — to rozsądny wybór, gdy budżet jest istotny, a parametry mają pozostać solidne (Uw od 0,88 W/m²K przy pakiecie Ug = 1,0).",
  "Mniejsza głębokość zabudowy ułatwia wymianę stolarki w istniejących murach — profil dobrze współpracuje z typowymi ościeżami bez skuwania tynków. Dostępna pełna paleta oklein VEKA oraz nawiewniki montowane fabrycznie."],
 ["VEKAMOTION 82 to system drzwi podnoszono-przesuwnych (HST), w którym skrzydło po przekręceniu klamki unosi się na wózkach i przesuwa bez oporu — także przy wadze kilkuset kilogramów. Wózki przenoszą skrzydła do 400 kg, a całe konstrukcje sięgają 6,5 m szerokości przy wysokości do 2,6 m.",
  "Rama skrzydła stałego ma tylko 86 mm wysokości, więc podział przeszklenia jest minimalny. Próg 0 mm (bezbarierowy) łączy podłogę z tarasem bez uskoku. Wielostopniowy system uszczelnień daje Ud do 0,76 W/m²K; opcjonalny napęd VEKAMOTION 82 Max otwiera skrzydło przyciskiem lub z aplikacji."],
 ["MB-86N to aluminiowy system okienno-drzwiowy Aluprof z przekładką termiczną 34 mm i wkładami Aero w komorach izolacyjnych. Aluminium pozwala na smukłe kształtowniki przy dużej sztywności — konstrukcje sięgają 2,9 m wysokości bez pośrednich wzmocnień.",
  "Uw od 0,72 W/m²K plasuje system w czołówce ciepłego aluminium. Wersje ST/SI/Aero różnicują izolacyjność do potrzeb inwestycji, a wariant z ukrytym skrzydłem daje elewacji jednolity, szklany wygląd. Kolory: pełny RAL, anody i okleiny drewnopodobne — również dwustronnie różne."]],
"drzwi-zewnetrzne": [
 ["Termo Prestige 72 to najcieplejsza stalowa linia Wikęd: skrzydło 72 mm wypełnione pianą poliuretanową, ościeżnica z przegrodą termiczną i ciepły próg z uszczelką EPDM. Ud od 0,71 W/m²K spełnia wymogi programu Czyste Powietrze z zapasem (wymagane ≤ 1,3).",
  "Linia obejmuje wszystkie kolekcje wzornicze 2026 — od Rustik po Royal — z aplikacjami inox, pochwytami i przeszkleniami z szybą P4. Maksymalna szerokość skrzydła 95 cm; wykonanie na wymiar co 1 cm."],
 ["Premium 54 to podstawowa linia stalowa Wikęd: skrzydło 54 mm z blachy ocynkowanej malowanej proszkowo, zamek listwowy 3-punktowy i wkładki klasy C w standardzie. Ud od 1,1 W/m²K wystarcza w budynkach z wiatrołapem.",
  "To najczęściej wybierany kompromis ceny i bezpieczeństwa — konstrukcja odporna na odkształcenia, pełna paleta przetłoczeń i oklein drewnopodobnych, opcja doposażenia w naświetla."],
 ["Drzwi aluminiowe na bazie systemu Aluprof MB-86 mają panel zlicowany obustronnie — skrzydło tworzy z ościeżnicą jedną płaszczyznę, bez widocznych ram. Przegrody termiczne dają Ud od 0,9 W/m²K przy konstrukcjach do 2,4 m wysokości.",
  "Wyposażenie premium: pochwyty do 1,8 m, czytnik linii papilarnych, kontrola dostępu i integracja ze Smart Home. Aluminium nie pracuje pod wpływem słońca, więc ciemne kolory i duże formaty są bezpieczne konstrukcyjnie."],
 ["Panel HPL (High Pressure Laminate) to okładzina z żywic utwardzanych o grubości 2 mm naklejana na skrzydło. Powłoka jest odporna na promieniowanie UV, wilgoć i zarysowania — parametry nieosiągalne dla klasycznych oklein PVC.",
  "HPL rekomendujemy przy ekspozycji południowej i ciemnych kolorach, gdzie temperatura powierzchni sięga 70°C. Dekory drewnopodobne i jednolite, także struktury szczotkowane; czyszczenie zwykłymi detergentami."]],
"drzwi-wewnetrzne": [
 ["Drzwi przylgowe mają klasyczną felc na krawędzi skrzydła i widoczne zawiasy czopowe — to najpopularniejsza, uniwersalna konstrukcja, łatwa w regulacji i najtańsza w zakupie. Bezprzylgowe licują się z ościeżnicą w jednej płaszczyźnie: zawiasy są ukryte (chowane w skrzydle), a zamek magnetyczny domyka drzwi bezgłośnie.",
  "W obu konstrukcjach dostępne są te same kolekcje DRE, Porty i Erkado — różnica dotyczy wyłącznie krawędzi skrzydła, zawiasów i ościeżnicy. Bezprzylga wymaga dedykowanej ościeżnicy i precyzyjnego montażu — wykonujemy go we własnym zakresie."],
 ["Kolekcje dekoracyjne to skrzydła z frezowaniami, intarsjami i przeszkleniami: DRE City 2 ze złotymi intarsjami, Vetro E ze szkłem hartowanym na całej wysokości, Estra 13 z ryflowaniem czy Hampton w stylu angielskim. Struktury synchroniczne odwzorowują usłojenie wyczuwalne pod palcami.",
  "Skrzydła wykonywane są w wysokościach do 2,2 m (Modern 30 — zmienna wysokość), co pozwala prowadzić linię drzwi do sufitu. Szyby: hartowane mleczne, przezierne lub VSG matowe i czarne."],
 ["Systemy przesuwne prowadzą skrzydło na szynie górnej — naściennie (z maskownicą) albo w kasecie chowanej w ścianę, która znika całkowicie po otwarciu. DRE oferuje dedykowane zestawy Estra 5 przesuwne i Enter Solid 23 z Galerią 50.",
  "Mechanizmy mają cichy domyk soft-close w standardzie, a skrzydła do 100 cm szerokości dzielą przestrzeń bez pola otwierania — zyskuje się ok. 1 m² podłogi względem drzwi rozwiernych."],
 ["Drzwi techniczne to skrzydła o podwyższonych parametrach: Solid RC2 z certyfikatem antywłamaniowym (wejścia do mieszkań), Forca z izolacyjnością akustyczną Rw do 32 dB oraz wersje wzmocnione o podwyższonej odporności na wilgoć do kotłowni i łazienek.",
  "Wypełnienie płytą wiórową pełną, wzmocnione ramiaki i uszczelki obwodowe (opcjonalnie uszczelka opadająca) odpowiadają za akustykę i stabilność. Dobór konstrukcji zależy od pomieszczenia — doradzimy przy pomiarze."]],
"rolety-zewnetrzne": [
 ["System nadstawny SKT Opoterm montuje się bezpośrednio na oknie — skrzynka ze spienionego Neoporu staje się częścią nadproża i po ociepleniu znika w elewacji. To rozwiązanie o najlepszej termice: skrzynka nie tworzy mostka, a rewizja od dołu daje łatwy serwis.",
  "W prowadnicach można zintegrować moskitierę rolowaną — jedna zabudowa obsługuje roletę i siatkę. Pancerz PA39/PA45 z pianką PU; sterowanie ręczne lub napęd rurowy."],
 ["Rolety podtynkowe SP/SP-E montuje się w nadprożu na etapie budowy — skrzynka jest kryta tynkiem i całkowicie niewidoczna, a okno zachowuje pełny prześwit. System nie ingeruje w profil okienny, więc parametry stolarki pozostają bez zmian.",
  "To standard w domach energooszczędnych i pasywnych: brak mostka termicznego i czysta elewacja. Dostęp serwisowy przez klapę rewizyjną od zewnątrz."],
 ["Rolety adaptacyjne SK, SK45 i SKO-P projektowano do budynków istniejących: skrzynka montowana jest na elewacji lub we wnęce okiennej bez prac murarskich — montaż w jeden dzień. Kształty skrzynek (proste, ścięte 45°, półokrągłe) pozwalają dopasować zabudowę do elewacji.",
  "Pancerz aluminiowy z pianką PU i prowadnice z uszczelką szczotkową zapewniają cichą pracę. Kolory RAL i okleiny drewnopodobne spójne z istniejącą stolarką."],
 ["Napędy Somfy io i Nice Era montowane w wale rolety obsługują sterowanie ścienne, pilotem lub aplikacją. Technologia io-homecontrol daje informację zwrotną o położeniu rolety, a centrale TaHoma/Yubii łączą rolety z bramą, oświetleniem i czujnikami.",
  "Automatyka pogodowa działa bez udziału domownika: czujnik słońca opuszcza rolety latem, czujnik temperatury reaguje na mróz, a harmonogramy symulują obecność podczas wyjazdu."]],
"pergole": [
 ["Pergola bioklimatyczna ma dach z obrotowych lameli aluminiowych (0–135°): ustawione pod kątem dozują światło i wentylują taras, zamknięte tworzą szczelny dach odprowadzający wodę rynnami w słupach. Konstrukcja z ekstrudowanego aluminium przenosi obciążenia wiatru i śniegu.",
  "Moduły łączy się w zadaszenia ponad 30 m². Sterowanie elektryczne z pilota lub aplikacji; doposażenie: LED w lamelach, promienniki, screeny ZIP i przesuwne przeszklenia."],
 ["Pergola tarasowa ma dach z tkaniny technicznej rozpinanej na prowadnicach — zwijany elektrycznie, z odwodnieniem w profilach. Tkanina odporna na UV i wysoką temperaturę pozwala całkowicie odsłonić niebo w pogodne dni.",
  "Konstrukcja dostawna do ściany lub wolnostojąca, kolory RAL strukturalne. To lżejsza i tańsza alternatywa dla dachu lamelowego, chętnie wybierana przy mniejszych tarasach."],
 ["Pergole wolnostojące mają samonośną konstrukcję na czterech lub więcej słupach — stają w ogrodzie, przy basenie lub jako zadaszenie strefy lounge, niezależnie od budynku.",
  "Kotwienie chemiczne do płyty albo stopy fundamentowe pod słupami; duże rozpiętości bez podpór pośrednich i możliwość szeregowego łączenia modułów."],
 ["Wyposażenie przekształca pergolę w całoroczny pokój zewnętrzny: oświetlenie LED w lamelach i słupach (ściemnialne), promienniki podczerwieni 1,5–2 kW, boczne screeny ZIP z tkaniny serge oraz przesuwne panele szklane.",
  "Całość spina automatyka Somfy io — pilot, aplikacja TaHoma i czujniki pogodowe (deszcz zamyka lamele automatycznie). Elementy można dokładać etapami, zaczynając od samej konstrukcji."]],
"bramy-garazowe": [
 ["Brama segmentowa otwiera się pionowo — panele wjeżdżają na prowadnicach pod sufit, więc przed garażem i w środku nie potrzeba miejsca na skrzydło. Panele stalowe 40 lub 60 mm z pianką poliuretanową dają bramie izolacyjność odpowiednią do garaży ogrzewanych.",
  "Powierzchnie Woodgrain i Silk, przetłoczenia od klasycznych po gładkie, dekory drewnopodobne Woodec. Uszczelnienie obwodowe i próg EPDM ograniczają przewiewy; opcje: przeszklenia, drzwi przejściowe, kratki wentylacyjne."],
 ["Brama roletowa zwija pancerz z profili aluminiowych do skrzynki nad otworem — zabudowa od 205 mm ratuje garaże z niskim nadprożem albo sufitem zajętym przez instalacje. Pancerz wypełniony pianką PU pracuje w prowadnicach z uszczelką szczotkową.",
  "Napęd rurowy z awaryjnym otwieraniem korbą jest standardem. Brama nie ogranicza światła wjazdu na boki — prowadnice zajmują tylko kilka centymetrów."],
 ["Napędy dobiera się do powierzchni i intensywności pracy bramy: Nice Spido 600N obsługuje bramy do ok. 9,6 m² i otwiera je w ok. 10 s; Spider 800/1200N — do 16,9 m², a wersja 1200 BLW z silnikiem bezszczotkowym wytrzymuje 150 cykli dziennie.",
  "Zabezpieczenia: amperometryczne wykrywanie przeszkód, fotokomórki, system antywłamaniowy w Spiderze. Sterowanie: piloty z kodem dynamicznym, Wi-Fi w standardzie (Spider), centrale Yubii/CORE i komendy głosowe Alexa/Google/Siri."],
 ["Drzwi boczne wykonuje się z tych samych paneli co bramę — przetłoczenia, struktura i kolor są identyczne, więc elewacja garażu pozostaje spójna. Ciepła ościeżnica aluminiowa z przegrodą termiczną eliminuje przemarzanie.",
  "Zamek wielopunktowy i opcjonalny samozamykacz czynią z nich pełnoprawne wejście techniczne do garażu — wygodniejsze niż otwieranie całej bramy."]],
"markizy": [
 ["Markiza tarasowa w pełnej kasecie chowa poszycie i ramiona w zamkniętym profilu aluminiowym — tkanina nie moknie i nie kurzy się poza sezonem, co wydłuża jej żywotność o lata. Wysięg ramion do 4 m i szerokości do 7 m (sprzęgane do 12 m) zacieniają ponad 25 m² tarasu.",
  "Kąt nachylenia reguluje się w zakresie 5–40°. Napęd Somfy w standardzie; opcja listwy LED w kasecie zamienia markizę w oświetlenie tarasu."],
 ["Markizy balkonowe i półkasetowe to lżejsze konstrukcje do mniejszych przestrzeni: montaż ścienny lub sufitowy, wysięg do 2,5 m, obsługa korbą albo napędem. Półkaseta osłania zwiniętą tkaninę od góry.",
  "Kolekcja ponad 100 tkanin akrylowych pozwala dopasować markizę do elewacji także we wspólnotach z określoną kolorystyką."],
 ["Markiza pionowa (przyścienna) opuszcza tkaninę wzdłuż krawędzi tarasu — zatrzymuje nisko świecące słońce i wiatr, których markiza pozioma nie blokuje. Prowadzenie linkowe lub w prowadnicach utrzymuje naprężenie.",
  "Tkaniny akrylowe pełne albo screen z okienkiem widokowym; funkcja kurtyny prywatności bez trwałej zabudowy tarasu."],
 ["Automatyka Somfy chroni markizę i zwalnia z obsługi: czujnik wiatru Eolis zwija poszycie po przekroczeniu progu (warunek gwarancji przy silnym wietrze), a czujnik słońca Sunis rozwija markizę, gdy taras się nagrzewa.",
  "Sterowanie pilotem Telis lub aplikacją TaHoma; markizę można wpiąć w sceny wspólne z roletami i pergolą."]],
"oslony-wewnetrzne": [
 ["Żaluzje aluminiowe mają lamele 25 mm (klasyka) lub 50 mm (styl loftowy) obracane pokrętłem albo łańcuszkiem — płynnie dozują światło bez zasłaniania widoku. Aluminium nie chłonie wilgoci, więc sprawdza się w kuchni i łazience.",
  "Kolory: matowe, perforowane (przepuszczają zarys światła po zamknięciu) i metaliczne. Opcja napędu elektrycznego przy trudno dostępnych oknach."],
 ["Plisa porusza się w dwóch kierunkach (góra-dół), więc zasłania dowolny pas szyby — np. tylko dół dla prywatności, z pozostawionym światłem u góry. Prowadzenie żyłkowe trzyma tkaninę przy szybie także w oknach uchylonych i dachowych.",
  "Tkaniny: transparentne, przyciemniające i blackout z powłoką perłową odbijającą ciepło. Montaż bezinwazyjny na skrzydle — bez wiercenia w profilu."],
 ["Roleta materiałowa w kasecie z prowadnicami domyka tkaninę przy krawędziach — z tkaniną blackout daje pełne zaciemnienie sypialni. Wersja wolnowisząca jest ekonomiczną alternatywą przy mniejszych wymaganiach.",
  "Kasety w kolorach stolarki (biel, antracyt, złoty dąb) zlewają się z oknem; tkaniny od transparentnych po dekoracyjne struktury."],
 ["Roleta dzień-noc przesuwa naprzemienne pasy tkaniny transparentnej i zaciemniającej względem siebie — od pełnego prześwitu, przez miękkie rozproszenie, po zaciemnienie, bez podnoszenia całej rolety.",
  "To najczęściej wybierana osłona do salonów i pokoi dziennych: reguluje prywatność przy zachowaniu kontaktu z otoczeniem."],
 ["Roleta rzymska podnosi tkaninę w miękkich, poziomych fałdach — działa jak zasłona, ale zajmuje tyle miejsca co roleta. Tkaniny naturalne (len, bawełna, welur) szyjemy na wymiar.",
  "Tkaninę zdejmuje się z taśm do prania — praktyczne w kuchni i jadalni."],
 ["Żaluzje pionowe (verticale) obracają pasy tkaniny 89 lub 127 mm wokół osi — sterują światłem na dużych przeszkleniach i w biurach, gdzie poziome lamele byłyby zbyt ciężkie.",
  "Tkaniny trudnopalne z atestem do obiektów; prowadzenie po łuku obsługuje wykusze."],
 ["Żaluzje drewniane (lamele 25/50 mm) i bambusowe wnoszą naturalny materiał do wnętrz klasycznych i gabinetów. Bambus jest lżejszy, więc sprawdza się na większych oknach.",
  "Wykończenia: naturalne barwienia i bejce, taśmy drabinkowe w kontrastowych kolorach jako detal aranżacyjny."]],
"oslony-zewnetrzne": [
 ["Refleksol to zewnętrzna roleta z tkaniny screen prowadzonej w systemie ZIP: zgrzewany brzeg tkaniny biegnie w prowadnicy, utrzymując pełne naprężenie — osłona pracuje przy silnym wietrze bez łopotania i szczelnie domyka światło przy krawędziach.",
  "Tkanina serge o stopniu otwarcia 1–5% zatrzymuje promieniowanie przed szybą, zachowując widok na zewnątrz. Kasety 85–150 mm, szerokości do 6 m, kolory RAL; szczelne prowadzenie pełni też rolę moskitiery."],
 ["Żaluzja fasadowa to zewnętrzne lamele aluminiowe o przekroju C-80 lub Z-90 (Z domyka się szczelniej), lakierowane proszkowo. Regulacja kąta obrotu steruje światłem jak żaluzja wewnętrzna — ale zatrzymuje ciepło przed elewacją.",
  "Prowadzenie linkowe lub szynowe, zabudowa natynkowa albo kryta w elewacji. Standard biurowców klasy A, coraz częściej stosowany w domach o nowoczesnej architekturze."],
 ["Sunbreaker (łamacz światła) to stałe lub obrotowe lamele wielkogabarytowe montowane przed elewacją — pionowo lub poziomo. Przekrój eliptyczny i duże rozpiętości czynią z nich element architektoniczny budynku.",
  "Wersje ruchome obracają lamele do 90°, śledząc słońce; stałe projektuje się pod kąt padania promieni w danej orientacji elewacji."],
 ["Moskitiera plisowana do dużych przeszkleń składa siatkę w harmonijkę prowadzoną w profilach — prowadnica dolna ma tylko 5 mm, więc przejście na taras pozostaje bez progu. Siatka zatrzymuje się w dowolnym punkcie (brak sprężyny).",
  "Zabudowa jedno- lub dwustronna obsługuje otwory do ok. 4 m — naturalny wybór do drzwi HST. Pełna oferta moskitier znajduje się w osobnej kategorii."]],
"moskitiery": [
 ["Moskitiera ramkowa to aluminiowa rama z siatką dopasowana do wymiaru okna, mocowana uchwytami obrotowymi na obrzeżu skrzydła — bez wiercenia w profilu, więc gwarancja stolarki pozostaje nienaruszona.",
  "Na zimę ramę zdejmuje się jednym ruchem. Siatka fiberglass w standardzie; dla właścicieli zwierząt polecamy pet screen o wielokrotnie wyższej wytrzymałości."],
 ["Moskitiera drzwiowa pracuje na zawiasach jak drugie skrzydło: własna ościeżnica, samozamykacz i magnesy domykające utrzymują ją w pozycji zamkniętej. Uszczelka szczotkowa na obwodzie odcina drogę drobnym owadom.",
  "To rozwiązanie do wyjść balkonowych i tarasowych używanych wielokrotnie w ciągu dnia — otwiera się łokciem przy zajętych rękach."],
 ["Moskitiera rolowana chowa siatkę do kasety 42–50 mm nad oknem — rozwijana tylko wtedy, gdy jest potrzebna, zimą znika całkowicie. Prowadnice ze szczotką doszczelniają krawędzie, hamulec spowalnia zwijanie.",
  "Wersja pozioma obsługuje okna dachowe. W systemach nadstawnych Aluprof kaseta moskitiery integruje się ze skrzynką rolety."],
 ["Moskitiera plisowana składa siatkę w harmonijkę przesuwaną w prowadnicach — dolna ma zaledwie 5 mm, dzięki czemu przejście przez drzwi HST pozostaje bezprogowe. Brak sprężyny: siatka zatrzymuje się w dowolnym położeniu.",
  "Zabudowa dwustronna obsługuje otwory do ok. 4 m szerokości. To standard do dużych przeszkleń tarasowych, gdzie klasyczne rozwiązania nie sięgają."]],
}

def _subslug(parent, title):
    t = title.lower()
    for a, b in [("ą","a"),("ć","c"),("ę","e"),("ł","l"),("ń","n"),("ó","o"),("ś","s"),("ż","z"),("ź","z")]:
        t = t.replace(a, b)
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    t = re.sub(r"-(i|w|z|do|na|the)-", "-", t)
    return f"{parent}--{t[:48].rstrip('-')}"

SUB_SLUGS = {}
for _p, _meta in PRODUCT_DATA.items():
    for _k, _r in enumerate(_meta["rows"]):
        SUB_SLUGS[(_p, _k)] = _subslug(_p, _r[0])


def build_subpages():
    """Strony 3. poziomu — jedna na każde rozwiązanie z podstron produktowych."""
    for parent, meta in PRODUCT_DATA.items():
        if parent in ("okna", "drzwi-zewnetrzne", "drzwi-wewnetrzne", "rolety-zewnetrzne"):   # bez podstron 3. poziomu (uwagi klienta)
            continue
        details = SUB_DETAILS.get(parent, [])
        for k, row in enumerate(meta["rows"]):
            title, intro, bullets, img = row
            slug = SUB_SLUGS[(parent, k)]
            paras = details[k] if k < len(details) else []
            lead = intro or (paras[0].split(". ")[0] + "." if paras else "")
            li = "".join(f'<li><span class="check">{I["check"]}</span> {b}</li>' for b in bullets)
            ptxt = "".join(f"<p>{p}</p>" for p in paras)

            siblings = ""
            for j, r2 in enumerate(meta["rows"]):
                if j == k: continue
                siblings += f"""<a href="{SUB_SLUGS[(parent, j)]}.html"><article class="card">
        <img src="assets/img/{r2[3]}.jpg" alt="{r2[0]}" style="height:130px;object-fit:cover;border-radius:var(--r-md)" loading="lazy">
        <div><h3 style="font-size:16px">{r2[0]}</h3></div>
        <span class="card__more">Czytaj więcej {I['arrow']}</span>
      </article></a>"""

    # producenci kategorii
            prod_logos = "".join(
                f'<img src="assets/img/partners/{p}.svg?v={ASSET_VER}" alt="{p}">'
                for p in meta.get("producers", []))
            producers_bar = (f'<div class="producer-strip"><div class="container producer-strip__inner">'
                             f'<span>Producenci w tej kategorii:</span>{prod_logos}</div></div>') if prod_logos else ""

            crumb = f'<a href="{parent}.html">{PROD_LABEL[parent]}</a> &nbsp;/&nbsp; {title}'
            body = pagehero(img, title, lead, crumb)
            body += producers_bar
            body += f"""<section class="section">
  <div class="container split" style="align-items:start">
    <div class="prose">{ptxt}
      <a class="btn btn--primary" href="kontakt.html">Zapytaj o wycenę {I['arrow']}</a>
    </div>
    <aside class="card card--soft" style="gap:14px">
      <h3>Najważniejsze parametry</h3>
      <ul class="bullets">{li}</ul>
      <a class="card__more" href="{parent}.html">Wróć do kategorii: {PROD_LABEL[parent]} {I['arrow']}</a>
    </aside>
  </div>
</section>

<section class="section section--soft">
  <div class="container">
    <div class="section-header"><div class="section-header__left">
      <span class="tag">{PROD_LABEL[parent]}</span>
      <h2 class="h-sec">Pozostałe rozwiązania w tej kategorii</h2>
    </div></div>
    <div class="grid-3">{siblings}</div>
  </div>
</section>

{cta("Doradztwo i wycena", "Chcesz zobaczyć to rozwiązanie na żywo?",
     "Zapytaj o wycenę lub odwiedź nasz showroom w Wieluniu — pokażemy przekroje, próbniki kolorów i działające ekspozycje.")}
"""
            first_b = bullets[0].rstrip(".") if bullets else ""
            write(f"{slug}.html",
                  head(f"{title} — {PROD_LABEL[parent]} | PROMYK Wieluń",
                       f"{title}: {first_b}. Doradztwo, pomiar i montaż — PROMYK Wieluń.")
                  + nav(parent) + body + footer())

# ---------------------------------------------------------------------------
# ================================================================ OKNA (układ wg uwag klienta 15.10.2026) ----
OKNA_VEKA = [
    ("VEKA SOFTLINE 82 MD",
     ["Głębokość zabudowy 82 mm, 7 komór, profil klasy A",
      "Uw od 0,74 W/m²K (pakiet 3-szybowy, ciepła ramka)",
      "3 płaszczyzny uszczelnienia z uszczelką środkową (MD)",
      "Sprawdza się zarówno w nowym budownictwie, jak i podczas modernizacji istniejących budynków"],
     "okna/softline82"),
    ("VEKA PERFECTLINE",
     ["Głębokość zabudowy 70 mm, 5 komór, profil klasy A",
      "Uw od 0,83 W/m²K",
      "2 uszczelki odbojowe (AD)",
      "Sprawdzony system do wymiany stolarki w budynkach istniejących"],
     "okna/perfectline"),
    ("VEKAMOTION 82 (HST)",
     ["Drzwi podnoszono-przesuwne — konstrukcje do 6,5 m szerokości",
      "Głębokość zabudowy ramy 194 mm",
      "Konstrukcja pozwala na niemal całkowite zlicowanie progu z poziomem podłogi",
      "Dzięki zaawansowanym mechanizmom skrzydło przesuwa się niezwykle płynnie"],
     "okna/vekamotion82"),
]
OKNA_ALUPROF = [
    ("Aluprof MB-79N",
     ["Głębokość zabudowy ramy 70 mm",
      "Uw od 0,75 W/m²K, system ten pozwala na wykonanie skrzydeł do 1350 mm × 2700 mm",
      "Wąskie profile — maksymalna powierzchnia szklenia",
      "Wysoka trwałość, odporność na promieniowanie słoneczne"],
     "al38"),
    ("Aluprof MB-77HS",
     ["Drzwi podnoszono-przesuwne, możliwość wykonania skrzydeł o wadze do 600 kg",
      "Głębokość zabudowy ramy 174 mm",
      "Konstrukcja pozwala na niemal całkowite zlicowanie progu z poziomem podłogi",
      "Innowacyjne mechanizmy podnoszono-przesuwne redukują opory ruchu do minimum. Skrzydło unosi się oraz przesuwa po szynach jezdnych niezwykle cicho, płynnie i bez wysiłku"],
     "al31_rol"),
]
OKNA_ADV_VEKA = [
    ("Energooszczędność", "Uw od 0,74 W/m²K przy pakiecie 3-szybowym", "thermo"),
    ("Klasa A profili", "Ścianki zewnętrzne min. 2,8 mm wg PN-EN 12608", "shield"),
    ("Kolorystyka", "Ponad 50 oklein: dekory drewnopodobne, RAL, VEKA Spectral", "palette"),
]
OKNA_ADV_ALUPROF = [
    ("Energooszczędność", "Uw od 0,75 W/m²K — ciepłe profile z przekładką termiczną", "thermo"),
    ("Trwałość", "Aluminium odporne na warunki atmosferyczne i promieniowanie słoneczne", "shield"),
    ("Nowoczesny design", "Smukłe profile i duże przeszklenia w pełnej palecie kolorów RAL", "sparkle"),
]
OKNA_SPECS = (["System", "Materiał", "Głębokość zabudowy", "Uw od", "Zastosowanie"], [
    ["VEKA SOFTLINE 82 MD", "PVC kl. A", "82 mm", "0,74 W/m²K", "domy energooszczędne, nowe budownictwo i modernizacje"],
    ["VEKA PERFECTLINE", "PVC kl. A", "70 mm", "0,83 W/m²K", "wymiana stolarki w budynkach istniejących"],
    ["VEKAMOTION 82 (HST)", "PVC kl. A", "194 mm (rama)", "0,78 W/m²K", "przeszklenia tarasowe do 6,5 m"],
    ["Aluprof MB-79N", "aluminium", "70 mm (rama)", "0,75 W/m²K", "nowoczesne domy i budynki komercyjne"],
    ["Aluprof MB-77HS", "aluminium", "174 mm (rama)", "0,84 W/m²K", "duże przeszklenia przesuwne, skrzydła do 600 kg"],
])
OKNA_FAQ = [
    ("Jak dobrać okna do stylu domu?",
     "<p><strong>Domy tradycyjne i dworkowe</strong> – klasyczne proporcje, białe profile, okleiny drewnopodobne i szprosy podkreślają ponadczasowy wygląd elewacji.</p>"
     "<p><strong>Domy rustykalne</strong> – okna w kolorach naturalnego drewna doskonale komponują się z kamieniem i drewnianymi elementami.</p>"
     "<p><strong>Nowoczesna architektura</strong> – duże przeszklenia, profile w kolorze antracytu lub czerni oraz systemy przesuwne podkreślają minimalistyczny charakter budynku.</p>"),
    ("Jakie okna wybrać do programu „Czyste Powietrze”?",
     "<p>Program „Czyste Powietrze” daje możliwość uzyskania dofinansowania na wymianę okien w ramach termomodernizacji budynku. Planując wymianę okien z dofinansowaniem, warto zwrócić uwagę przede wszystkim na:</p>"
     "<ul><li><strong>Współczynnik Uw</strong> – im niższy, tym mniejsze straty ciepła przez całe okno</li>"
     "<li><strong>Profil okienny</strong> – dobrej jakości system, taki jak VEKA Softline 82, stanowi solidną podstawę energooszczędnej stolarki</li>"
     "<li><strong>Profesjonalny montaż</strong> – prawidłowe osadzenie okien ma istotne znaczenie dla ich szczelności</li></ul>"),
    ("Czy można zamówić okna na wymiar?",
     "<p>Tak! Okna są produkowane na indywidualny wymiar, dzięki czemu można idealnie dopasować je do otworów okiennych oraz projektu budynku. Oferujemy rozwiązania dostosowane do różnych potrzeb – od standardowych okien po nietypowe kształty, wymiary i przeszklenia.</p>"),
    ("Czy wycena okien jest bezpłatna?",
     "<p>Tak! Przygotowujemy bezpłatną wycenę okien na podstawie projektu lub zapytania przesłanego mailowo. Możesz również odwiedzić naszą firmę i na miejscu omówić szczegóły inwestycji oraz dobrać odpowiednie rozwiązania. Pomożemy Ci wybrać okna dopasowane do Twoich potrzeb i budżetu.</p>"),
    ("Czy wykonujecie pomiar okien na miejscu?",
     "<p>Tak, wykonujemy pomiary okien bezpośrednio u klienta, aby jak najlepiej dopasować stolarkę do budynku. Pomiar ma charakter wiążący i wiąże się z pobraniem zaliczki na poczet zamówienia. Dzięki temu możemy precyzyjnie przygotować ofertę i przejść do realizacji zamówienia.</p>"),
    ("Czy demontujecie stare okna?",
     "<p>Tak, oferujemy demontaż starych okien w ramach wymiany stolarki okiennej. Zakres prac ustalamy indywidualnie, aby dopasować usługę do potrzeb klienta i specyfiki budynku. Szczegóły demontażu warto omówić już na etapie przygotowywania wyceny.</p>"),
    ("Czy zapewniacie serwis zamontowanych okien?",
     "<p>Tak! Zapewniamy serwis zamontowanych okien, ponieważ zależy nam na długotrwałej współpracy i zadowoleniu naszych klientów. Pomagamy również w przypadku problemów z funkcjonowaniem okien i w razie potrzeby wykonujemy regulację.</p>"),
    ("Co oznacza współczynnik Uw?",
     "<p>Uw opisuje izolacyjność całego okna. Im niższa wartość, tym cieplejsze okno.</p>"),
    ("Czym różni się profil klasy A od klasy B?",
     "<p>Norma PN-EN 12608 dzieli profile PVC według grubości ścianek: klasa A to ścianki zewnętrzne ≥ 2,8 mm, klasa B — ≥ 2,5 mm. Grubsze ścianki oznaczają sztywniejsze konstrukcje, mocniejsze zgrzewy naroży i lepsze osadzenie okuć — dlatego montujemy wyłącznie profile klasy A.</p>"),
    ("Pakiet 2-szybowy czy 3-szybowy?",
     "<p>Pakiet 3-szybowy (Ug 0,5–0,7) ogranicza straty ciepła o ok. 30–40% względem 2-szybowego (Ug 1,0) i poprawia komfort zimą przy dużych przeszkleniach. Do tego ciepła ramka dystansowa obniża współczynnik psi na krawędzi szyby i ryzyko wykraplania pary.</p>"),
]
OKNA_GALERIA = [f"okna/galeria-{k}" for k in range(1, 13)]


def build_okna():
    def rows_html(items, offset, veka):
        out = ""
        for k, (title, bullets, img) in enumerate(items):
            li = "".join(f'<li><span class="check">{I["check"]}</span> {b}</li>' for b in bullets)
            btns = (f'<a class="btn btn--primary btn--sm" href="konfigurator.html">Skonfiguruj okno {I["win"]}</a>'
                    f'<a class="btn btn--outline btn--sm" href="kontakt.html">Zapytaj o wycenę {I["arrow"]}</a>') if veka else \
                   f'<a class="btn btn--primary btn--sm" href="kontakt.html">Zapytaj o wycenę {I["arrow"]}</a>'
            media = f'<div><img src="assets/img/{img}.jpg" alt="{title}" loading="lazy"></div>'
            text = f"""<div class="subrow__text">
        <h2>{title}</h2>
        <ul class="bullets">{li}</ul>
        <div style="display:flex;gap:12px;flex-wrap:wrap">{btns}</div>
      </div>"""
            flip = (k + offset) % 2
            out += f'<div class="subrow{" subrow--flip" if flip else ""}">{media if not flip else text}{text if not flip else media}</div>'
        return out

    def adv_html(items):
        return "".join(f"""<div class="adv"><span class="adv__icon">{I[ic]}</span>
      <div><h3>{t}</h3><p>{d}</p></div></div>""" for t, d, ic in items)

    def brand_intro(logo, name, text):
        return f"""<div class="brand-intro">
      <img src="assets/img/partners/{logo}.svg?v={ASSET_VER}" alt="{name}">
      <p>{text}</p>
    </div>"""

    cols, srows = OKNA_SPECS
    th = "".join(f"<th>{c}</th>" for c in cols)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in srows)

    faq = ""
    for k, (q, a) in enumerate(OKNA_FAQ):
        faq += f"""<div class="faq__row">
      <button class="faq__q"><span>{q}</span><span>+</span></button>
      <div class="faq__a">{a}</div>
    </div>"""

    gal = "".join(f'<a href="assets/img/{g}.jpg" data-lightbox-item><img src="assets/img/{g}.jpg" alt="Wizualizacja okien VEKA" loading="lazy"></a>'
                  for g in OKNA_GALERIA)

    rel = ""
    for s in ["rolety-zewnetrzne", "drzwi-zewnetrzne", "bramy-garazowe"]:
        rel += f"""<a href="{s}.html"><article class="card">
        <img src="assets/img/{PROD_IMG[s]}.jpg" alt="{PROD_LABEL[s]}" style="height:150px;object-fit:cover;border-radius:var(--r-md)">
        <div><h3>{PROD_LABEL[s]}</h3></div>
        <span class="card__more">Zobacz ofertę {I['arrow']}</span>
      </article></a>"""

    body = pagehero("al39", "Okna VEKA i systemy Aluprof",
                    "Wysoka jakość, doskonałe parametry i design dopasowany do Twoich potrzeb.", None)
    body += f"""<section class="section">
  <div class="container">
    {brand_intro("veka", "VEKA", "Odpowiednio dobrane okna mają istotny wpływ na efektywność energetyczną budynku i komfort jego użytkowania. Systemy okienne VEKA z wysokiej jakości profili PVC łączą dobre parametry techniczne z estetyką i trwałością. Wybierając okna VEKA, stawiasz na sprawdzone rozwiązania, jakość i niezawodność na lata.")}
    {rows_html(OKNA_VEKA, 0, True)}
  </div>
</section>
<section class="advantages"><div class="container advantages__inner">{adv_html(OKNA_ADV_VEKA)}</div></section>

<section class="section">
  <div class="container">
    {brand_intro("aluprof", "Aluprof", "Aluprof to ceniony polski producent systemów aluminiowych, który łączy nowoczesne technologie z funkcjonalnością i estetyką. Okna Aluprof to doskonały wybór dla osób ceniących trwałość, energooszczędność i nowoczesny design. Sprawdzają się zarówno w nowoczesnych domach, jak i budynkach komercyjnych.")}
    {rows_html(OKNA_ALUPROF, 1, False)}
  </div>
</section>
<section class="advantages"><div class="container advantages__inner">{adv_html(OKNA_ADV_ALUPROF)}</div></section>

<section class="section section--soft">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Porównanie systemów okiennych</h2></div></div>
    <div class="spec-wrap"><table class="spec-table"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Warto wiedzieć przed zakupem</h2></div></div>
    <div class="faq">{faq}</div>
  </div>
</section>

<section class="section section--soft">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Inspiracje</h2></div></div>
    <div class="gallery gallery--okna" data-lightbox>{gal}</div>
  </div>
</section>

{cta("Doradztwo i wycena", "Planujesz inwestycję budowlaną?",
     "Skontaktuj się z nami — doradzimy technicznie i przygotujemy kalkulację cenową.")}

<section class="section related">
  <div class="container">
    <h2 class="h-sec" style="margin-bottom:32px">Sprawdź również inne systemy</h2>
    <div class="grid-3">{rel}</div>
  </div>
</section>
"""
    write("okna.html", head("Okna PVC VEKA i aluminiowe Aluprof | PROMYK Wieluń",
                            "Okna PVC VEKA Softline 82 MD i Perfectline, drzwi HST VEKAMOTION 82 oraz aluminiowe Aluprof MB-79N i MB-77HS. Bezpłatna wycena, profesjonalny pomiar i montaż — PROMYK Wieluń.")
          + nav("okna") + body + footer())


# ================================================================ DRZWI ZEWNĘTRZNE (uwagi klienta 19–20.10.2026) ----
DZ_WIKED_TECH = [("Alu Hybrid", "86 mm", "alu-hybrid"), ("Termo Prestige", "86 mm", "termo-prestige"),
                 ("Optimum", "76 mm", "optimum"), ("Prima", "64 mm", "prima")]
DZ_WIKED_KOLEKCJE = ["3D", "Future", "Glass", "Klasyk", "Royal", "Rustik", "Softline"]
DZ_WIKED_MODELE = [   # (kolekcja, nazwa modelu, plik) — modele ze strony wiked.pl
    ('3D', '3D01', '3d-3d01'),
    ('3D', '3D02', '3d-3d02'),
    ('3D', '3D03', '3d-3d03'),
    ('3D', '3D04', '3d-3d04'),
    ('3D', '3D05', '3d-3d05'),
    ('3D', '3D06', '3d-3d06'),
    ('3D', '3D07', '3d-3d07'),
    ('3D', '3D08', '3d-3d08'),
    ('Glass', 'GD01a', 'glass-gd01a'),
    ('Glass', 'GD01b', 'glass-gd01b'),
    ('Glass', 'GD01c', 'glass-gd01c'),
    ('Glass', 'GD02a', 'glass-gd02a'),
    ('Glass', 'GD02b', 'glass-gd02b'),
    ('Glass', 'GD03a', 'glass-gd03a'),
    ('Glass', 'GD04', 'glass-gd04'),
    ('Glass', 'GL01', 'glass-gl01'),
    ('Glass', 'GL01a', 'glass-gl01a'),
    ('Glass', 'GL02', 'glass-gl02'),
    ('Glass', 'GL02a', 'glass-gl02a'),
    ('Glass', 'GL02b', 'glass-gl02b'),
    ('Glass', 'GL02c', 'glass-gl02c'),
    ('Glass', 'GL03', 'glass-gl03'),
    ('Glass', 'GL03a', 'glass-gl03a'),
    ('Glass', 'GL03b', 'glass-gl03b'),
    ('Glass', 'GL03c', 'glass-gl03c'),
    ('Glass', 'GF01', 'glass-gf01'),
    ('Glass', 'GF01a', 'glass-gf01a'),
    ('Glass', 'GF02', 'glass-gf02'),
    ('Glass', 'GF02a', 'glass-gf02a'),
    ('Glass', 'GF02b', 'glass-gf02b'),
    ('Glass', 'GF02c', 'glass-gf02c'),
    ('Glass', 'GF03', 'glass-gf03'),
    ('Glass', 'GF03a', 'glass-gf03a'),
    ('Glass', 'GF03b', 'glass-gf03b'),
    ('Glass', 'GF03c', 'glass-gf03c'),
    ('Glass', 'GF04', 'glass-gf04'),
    ('Glass', 'GF05', 'glass-gf05'),
    ('Glass', 'GF06', 'glass-gf06'),
    ('Glass', 'GF07', 'glass-gf07'),
    ('Klasyk', '1', 'klasyk-1'),
    ('Klasyk', '3', 'klasyk-3'),
    ('Klasyk', '4', 'klasyk-4'),
    ('Klasyk', '5', 'klasyk-5'),
    ('Klasyk', '6', 'klasyk-6'),
    ('Klasyk', '8', 'klasyk-8'),
    ('Klasyk', '9', 'klasyk-9'),
    ('Klasyk', '12', 'klasyk-12'),
    ('Klasyk', '12c', 'klasyk-12c'),
    ('Klasyk', '13', 'klasyk-13'),
    ('Klasyk', '14', 'klasyk-14'),
    ('Klasyk', '21', 'klasyk-21'),
    ('Klasyk', '21a', 'klasyk-21a'),
    ('Klasyk', '22', 'klasyk-22'),
    ('Klasyk', '23', 'klasyk-23'),
    ('Klasyk', '23a', 'klasyk-23a'),
    ('Klasyk', '24', 'klasyk-24'),
    ('Klasyk', '25', 'klasyk-25'),
    ('Klasyk', '25a', 'klasyk-25a'),
    ('Klasyk', '25b', 'klasyk-25b'),
    ('Klasyk', '25c', 'klasyk-25c'),
    ('Klasyk', '26', 'klasyk-26'),
    ('Klasyk', '26a', 'klasyk-26a'),
    ('Klasyk', '26b', 'klasyk-26b'),
    ('Klasyk', '26c', 'klasyk-26c'),
    ('Klasyk', '26d', 'klasyk-26d'),
    ('Klasyk', '26e', 'klasyk-26e'),
    ('Klasyk', '26f', 'klasyk-26f'),
    ('Klasyk', '26g', 'klasyk-26g'),
    ('Klasyk', '26h', 'klasyk-26h'),
    ('Klasyk', '26i', 'klasyk-26i'),
    ('Klasyk', '26j', 'klasyk-26j'),
    ('Klasyk', '26k', 'klasyk-26k'),
    ('Klasyk', '27', 'klasyk-27'),
    ('Klasyk', '28', 'klasyk-28'),
    ('Klasyk', '29a', 'klasyk-29a'),
    ('Klasyk', '30', 'klasyk-30'),
    ('Klasyk', '30a', 'klasyk-30a'),
    ('Klasyk', '30b', 'klasyk-30b'),
    ('Klasyk', '31', 'klasyk-31'),
    ('Klasyk', '31a', 'klasyk-31a'),
    ('Klasyk', '32', 'klasyk-32'),
    ('Klasyk', '32a', 'klasyk-32a'),
    ('Klasyk', '32b', 'klasyk-32b'),
    ('Klasyk', '34', 'klasyk-34'),
    ('Klasyk', '36', 'klasyk-36'),
    ('Klasyk', '37', 'klasyk-37'),
    ('Klasyk', '37a', 'klasyk-37a'),
    ('Klasyk', '38', 'klasyk-38'),
    ('Klasyk', '38a', 'klasyk-38a'),
    ('Klasyk', '39', 'klasyk-39'),
    ('Klasyk', '40', 'klasyk-40'),
    ('Klasyk', '40a', 'klasyk-40a'),
    ('Klasyk', '41', 'klasyk-41'),
    ('Klasyk', '41a', 'klasyk-41a'),
    ('Klasyk', '39a', 'klasyk-39a'),
    ('Klasyk', '39b', 'klasyk-39b'),
    ('Klasyk', '41b', 'klasyk-41b'),
    ('Klasyk', '42', 'klasyk-42'),
    ('Klasyk', '43', 'klasyk-43'),
    ('Klasyk', '43a', 'klasyk-43a'),
    ('Klasyk', '43b', 'klasyk-43b'),
    ('Klasyk', '43c', 'klasyk-43c'),
    ('Klasyk', '44', 'klasyk-44'),
    ('Klasyk', '44a', 'klasyk-44a'),
    ('Klasyk', '44b', 'klasyk-44b'),
    ('Klasyk', '44c', 'klasyk-44c'),
    ('Klasyk', '45', 'klasyk-45'),
    ('Klasyk', '47', 'klasyk-47'),
    ('Klasyk', '48', 'klasyk-48'),
    ('Klasyk', '49', 'klasyk-49'),
    ('Klasyk', '50', 'klasyk-50'),
    ('Royal', 'RL1', 'royal-rl1'),
    ('Royal', 'RL2a', 'royal-rl2a'),
    ('Royal', 'RL2b', 'royal-rl2b'),
    ('Royal', 'RL3', 'royal-rl3'),
    ('Royal', 'RL3a', 'royal-rl3a'),
    ('Royal', 'RL3b', 'royal-rl3b'),
    ('Royal', 'RL4', 'royal-rl4'),
    ('Royal', 'RL4a', 'royal-rl4a'),
    ('Royal', 'RL4b', 'royal-rl4b'),
    ('Royal', 'RL5', 'royal-rl5'),
    ('Royal', 'RL5a', 'royal-rl5a'),
    ('Royal', 'RL5b', 'royal-rl5b'),
    ('Royal', 'RL6', 'royal-rl6'),
    ('Royal', 'RL6a', 'royal-rl6a'),
    ('Royal', 'RL7', 'royal-rl7'),
    ('Royal', 'RL7b', 'royal-rl7b'),
    ('Royal', 'RL7a', 'royal-rl7a'),
    ('Rustik', 'ML01', 'rustik-ml01'),
    ('Rustik', 'ML02', 'rustik-ml02'),
    ('Rustik', 'ML03', 'rustik-ml03'),
    ('Rustik', 'WL01', 'rustik-wl01'),
    ('Rustik', 'WL02', 'rustik-wl02'),
    ('Rustik', 'WL03', 'rustik-wl03'),
    ('Softline', 'S1', 'softline-s1'),
    ('Softline', 'S2', 'softline-s2'),
    ('Softline', 'S3', 'softline-s3'),
    ('Softline', 'S4', 'softline-s4'),
    ('Softline', 'S5', 'softline-s5'),
    ('Softline', 'S6', 'softline-s6'),
    ('Softline', 'S7', 'softline-s7'),
    ('Future', 'FI01a', 'future-fi01a'),
    ('Future', 'FI01b', 'future-fi01b'),
    ('Future', 'FI01c', 'future-fi01c'),
    ('Future', 'FI01d', 'future-fi01d'),
    ('Future', 'FI02a', 'future-fi02a'),
    ('Future', 'FI02b', 'future-fi02b'),
    ('Future', 'FI03a', 'future-fi03a'),
    ('Future', 'FI03b', 'future-fi03b'),
    ('Future', 'FI04a', 'future-fi04a'),
    ('Future', 'FI04b', 'future-fi04b'),
    ('Future', 'FI04c', 'future-fi04c'),
    ('Future', 'FI04d', 'future-fi04d'),
    ('Future', 'FI04e', 'future-fi04e'),
    ('Future', 'FI05a', 'future-fi05a'),
    ('Future', 'FI05b', 'future-fi05b'),
    ('Future', 'FI05c', 'future-fi05c'),
    ('Future', 'FI05d', 'future-fi05d'),
    ('Future', 'FI05e', 'future-fi05e'),
    ('Future', 'FI06a', 'future-fi06a'),
    ('Future', 'FI06b', 'future-fi06b'),
    ('Future', 'FI06d', 'future-fi06d'),
    ('Future', 'FI06e', 'future-fi06e'),
    ('Future', 'FI07a', 'future-fi07a'),
    ('Future', 'FI07b', 'future-fi07b'),
    ('Future', 'FI07c', 'future-fi07c'),
    ('Future', 'FI07d', 'future-fi07d'),
    ('Future', 'FI07e', 'future-fi07e'),
    ('Future', 'FI08a', 'future-fi08a'),
    ('Future', 'FI08b', 'future-fi08b'),
    ('Future', 'FI10a', 'future-fi10a'),
    ('Future', 'FI10b', 'future-fi10b'),
    ('Future', 'FI11', 'future-fi11'),
    ('Future', 'FI12', 'future-fi12'),
    ('Future', 'FI13', 'future-fi13'),
    ('Future', 'FI14', 'future-fi14'),
    ('Future', 'FI15', 'future-fi15'),
]
DZ_WIKED_PALETY = [("nd", "Natural Decor"), ("cs", "Crystal Sky"), ("tt", "Top Trends")]
DZ_WIKED_KOLORY = [
    ('nd', 'Dąb Bagienny', 'dab-bagienny'),
    ('nd', 'Dąb Bielony', 'dab-bielony'),
    ('nd', 'Orzech', 'orzech'),
    ('nd', 'Srebrno-szary', 'srebrno-szary'),
    ('nd', 'Winchester', 'winchester'),
    ('nd', 'Woodec Dąb Toffee', 'woodec-dab-toffee'),
    ('nd', 'Woodec Dąb Turner', 'woodec-dab-turner'),
    ('nd', 'Złoty Dąb', 'zloty-dab'),
    ('nd', 'Antracyt Gładki', 'antracyt-gladki'),
    ('nd', 'Antracyt Jedwabny', 'antracyt-jedwabny'),
    ('nd', 'Antracyt Struktura', 'antracyt-struktura'),
    ('nd', 'Biały Mat', 'bialy-mat'),
    ('nd', 'Czarny Mat', 'czarny-mat'),
    ('cs', 'Azure', 'azure'),
    ('cs', 'Basalt White', 'basalt-white'),
    ('cs', 'Carbon', 'carbon'),
    ('cs', 'Cobalt Blue', 'cobalt-blue'),
    ('cs', 'Coffee&Milk', 'coffee-milk'),
    ('cs', 'Dark Bronze', 'dark-bronze'),
    ('cs', 'Dark Grey', 'dark-grey'),
    ('cs', 'Dark Mint', 'dark-mint'),
    ('cs', 'Graphite Black', 'graphite-black'),
    ('cs', 'Grey Aluminium', 'grey-aluminium'),
    ('cs', 'Lagoon', 'lagoon'),
    ('cs', 'Limestone', 'limestone'),
    ('cs', 'Lunar Glow', 'lunar-glow'),
    ('cs', 'Magnolia Blossom', 'magnolia-blossom'),
    ('cs', 'Medium Grey', 'medium-grey'),
    ('cs', 'Moss', 'moss'),
    ('cs', 'Rusty Bronze', 'rusty-bronze'),
    ('cs', 'Savana', 'savana'),
    ('cs', 'Silver Grey', 'silver-grey'),
    ('tt', 'Morning White', 'morning-white'),
    ('tt', 'Arctic White', 'arctic-white'),
    ('tt', 'Light Grey', 'light-grey'),
    ('tt', 'Grey Stone', 'grey-stone'),
    ('tt', 'Skyline Gray', 'skyline-gray'),
    ('tt', 'Silver Mist', 'silver-mist'),
    ('tt', 'Ash', 'ash'),
    ('tt', 'Concrete', 'concrete'),
    ('tt', 'Solid Gray', 'solid-gray'),
    ('tt', 'Obsidian Gray', 'obsidian-gray'),
    ('tt', 'Nightfall', 'nightfall'),
    ('tt', 'Moss Stone', 'moss-stone'),
    ('tt', 'Soft Quartz', 'soft-quartz'),
    ('tt', 'Truffle', 'truffle'),
    ('tt', 'Chocolate Brown', 'chocolate-brown'),
    ('tt', 'Red Velvet', 'red-velvet'),
    ('tt', 'Blackout', 'blackout'),
    ('tt', 'Blue Mist', 'blue-mist'),
    ('tt', 'Ink', 'ink'),
    ('tt', 'Sage', 'sage'),
    ('tt', 'Forest Green', 'forest-green'),
]   # (paleta, nazwa, plik)
DZ_WIKED_POCHWYTY = [("Alfa", "alfa"), ("Alfa Vision Inox", "alfa-vision-inox"), ("Beta", "beta"),
                     ("Beta + czytnik linii papilarnych", "beta-czytnik"), ("Queen", "queen"), ("Stripe Inox", "stripe-inox"),
                     ("Toro Inox + LED", "toro-inox-led"), ("Fusion z podświetleniem", "fusion-led")]
DZ_WIKED_KLAMKI = [("Manitoba Black", "manitoba-black"), ("Tahoma Inox", "tahoma-inox"), ("Magnus Stare Złoto", "magnus-stare-zloto"),
                   ("Prime Black", "prime-black"), ("Prestige Inox", "prestige-inox"), ("Lava Black", "lava-black"),
                   ("King Black", "king-black"), ("Quadro Inox", "quadro-inox")]
DZ_WIKED_SZYBY = [("Standard", "standard"), ("Mleczna", "mleczna"), ("Reflex grafit", "reflex-grafit"),
                  ("Lustro weneckie", "lustro-weneckie"), ("Black", "black"), ("Piaskowana + pasek", "piaskowana-pasek"),
                  ("Lacobel", "lacobel"), ("Fala", "fala")]
DZ_WIKED_INSPIRACJE = ["drzwi/insp-antracyt", "wiked62", "drzwi/insp-czarne", "wiked37",
                       "drzwi/insp-granat", "wiked92", "drzwi/insp-czarne-drewno", "wiked07",
                       "drzwi/insp-szalwia", "wiked51", "wiked12", "wiked35"]
DZ_SMART = [("Otwieranie telefonem", "Otwierasz drzwi z aplikacji — także wtedy, gdy nie ma Cię w domu."),
            ("Dostęp dla bliskich", "Dajesz dostęp wybranym osobom i decydujesz, kiedy mogą wejść."),
            ("Podgląd i historia", "Sprawdzasz w telefonie, czy drzwi są zamknięte i kiedy były otwierane."),
            ("Światło po zmroku", "Podświetlenie LED włączasz jednym kliknięciem.")]
DZ_SMART_PUNKTY = [(1, 68, 24, "Naświetle z podświetleniem"), (2, 47, 82, "Podświetlany próg"),
                   (3, 38.5, 58, "Podświetlenie pochwytu"), (4, 38.5, 36, "Przycisk w pochwycie — otwierasz bez klucza")]
DZ_ERKADO_TECH = [("Thermo 64", "64 mm", "thermo-64"), ("Thermo 78", "78 mm", "thermo-78"),
                  ("Thermo Hot 78", "78 mm", "thermo-hot-78"), ("Thermo Hot 88", "88 mm", "thermo-hot-88")]
DZ_ERKADO_MODELE = [("Arendal", "arendal"), ("Utrecht", "utrecht"), ("Helmond", "helmond"), ("Lahti", "lahti"),
                    ("Alta", "alta"), ("Rotterdam", "rotterdam"), ("Bazylea", "bazylea"), ("Linden", "linden"),
                    ("Horn", "horn"), ("Fryburg", "fryburg"), ("Wels", "wels"), ("Lutter", "lutter"),
                    ("Leimen", "leimen"), ("Amberg", "amberg"), ("Lucerna", "lucerna"), ("Singen", "singen"),
                    ("Selters", "selters"), ("Langen", "langen")]
DZ_ERKADO_KOLORY = [("Antracyt jedwabny", "antracyt-jedwabny"), ("Biały mat", "bialy-mat"), ("Dąb turner", "dab-turner"),
                    ("Dąb antracyt", "dab-antracyt"), ("Orzech", "orzech"), ("Czarny", "czarny"), ("Złoty dąb", "zloty-dab"),
                    ("Winchester", "winchester"), ("Antracyt struktura", "antracyt-struktura"), ("Antracyt gładki", "antracyt-gladki"),
                    ("Szary", "szary"), ("Dąb bagienny", "dab-bagienny"), ("Dąb surowy", "dab-surowy"),
                    ("Dąb średni brąz", "dab-sredni-braz"), ("Sosna górska", "sosna-gorska"), ("Dąb naturalny", "dab-naturalny")]
DZ_ADV_WIKED = [("Bezpieczeństwo", "Ochrona antywłamaniowa do klasy RC2", "lock"),
                ("Ciepło", "Izolacyjność cieplna Ud od 0,54 W/m²K", "thermo"),
                ("Wzornictwo", "Setki wzorów i dowolna kolorystyka", "sparkle")]
DZ_ADV_ERKADO = [("Ciepło", "Ud od 0,60 W/m²K w technologii Thermo Hot 88", "thermo"),
                 ("Bezpieczeństwo", "Zamek listwowy i bolce antywyważeniowe w standardzie", "lock"),
                 ("Na wymiar", "Dopasowanie do otworu w murze co do 1 cm", "ruler")]
DZ_FAQ = [
    ("Na co zwrócić uwagę przy wyborze drzwi zewnętrznych?",
     "<p>Ważne są parametry termoizolacyjne, bezpieczeństwo, trwałość, odporność na warunki atmosferyczne oraz wygląd dopasowany do elewacji i stylu budynku.</p>"),
    ("Czy drzwi zewnętrzne można dopasować kolorystycznie do okien i bramy garażowej?",
     "<p>Tak, dobierając drzwi, można uwzględnić kolorystykę okien, bramy garażowej i pozostałych elementów stolarki, aby uzyskać spójny wygląd całego budynku.</p>"),
    ("Czy drzwi zewnętrzne kwalifikują się do dofinansowania w programie „Czyste Powietrze”?",
     "<p>Tak, w przypadku standardowych drzwi zewnętrznych obowiązują wymagania techniczne dotyczące współczynnika Ud (współczynnik przenikania ciepła) — nie może on przekraczać 1,3 W/(m²·K).</p>"),
    ("Czy można zamówić drzwi na wymiar?",
     "<p>Tak! Drzwi są produkowane na indywidualny wymiar, dzięki czemu można idealnie dopasować je do otworu wejściowego oraz projektu budynku. Oferujemy rozwiązania dostosowane do różnych potrzeb – od standardowych drzwi po nietypowe wymiary, naświetla boczne i górne.</p>"),
    ("Jak dobrać odpowiedni rozmiar drzwi zewnętrznych?",
     "<p>Rozmiar drzwi należy dopasować do wymiarów otworu w ścianie oraz warunków technicznych budynku. Przy wyborze warto uwzględnić nie tylko szerokość i wysokość skrzydła, ale również ościeżnicę i sposób montażu. Przed zamówieniem drzwi najlepiej wykonać dokładny pomiar, aby mieć pewność, że będą odpowiednio dopasowane do wejścia.</p>"),
    ("Jak rozpoznać, czy drzwi zewnętrzne są lewe czy prawe?",
     "<p>Drzwi określamy jako lewe lub prawe, patrząc na nie od strony, z której otwierają się do nas. Jeśli zawiasy znajdują się po lewej stronie, drzwi są lewe, a jeśli po prawej — prawe.</p>"),
    ("Czy wycena drzwi jest bezpłatna?",
     "<p>Tak! Przygotowujemy bezpłatną wycenę drzwi na podstawie projektu lub zapytania przesłanego mailowo. Możesz również odwiedzić naszą firmę i na miejscu omówić szczegóły inwestycji oraz dobrać odpowiednie rozwiązania. Pomożemy Ci wybrać drzwi dopasowane do Twoich potrzeb i budżetu.</p>"),
    ("Czy wykonujecie pomiar drzwi na miejscu?",
     "<p>Tak, wykonujemy pomiary drzwi bezpośrednio u klienta, aby jak najlepiej dopasować je do budynku. Pomiar ma charakter wiążący i wiąże się z pobraniem zaliczki na poczet zamówienia. Dzięki temu możemy precyzyjnie przygotować ofertę i przejść do realizacji zamówienia.</p>"),
    ("Czy demontujecie stare drzwi?",
     "<p>Tak, oferujemy demontaż starych drzwi w ramach wymiany stolarki. Zakres prac ustalamy indywidualnie, aby dopasować usługę do potrzeb klienta i specyfiki budynku. Szczegóły demontażu warto omówić już na etapie przygotowywania wyceny.</p>"),
    ("Czy zapewniacie serwis zamontowanych drzwi?",
     "<p>Tak! Zapewniamy serwis zamontowanych drzwi, ponieważ zależy nam na długotrwałej współpracy i zadowoleniu naszych klientów. Pomagamy również w przypadku problemów z funkcjonowaniem drzwi i w razie potrzeby wykonujemy regulację.</p>"),
]


def build_drzwi_zewnetrzne():
    def adv_html(items):
        return "".join(f"""<div class="adv"><span class="adv__icon">{I[ic]}</span>
      <div><h3>{t}</h3><p>{d}</p></div></div>""" for t, d, ic in items)

    def step(no, title, inner):
        return f"""<div class="step-block">
      <div class="step-block__head"><span class="step-block__no">{no:02d}</span><h3>{title}</h3></div>
      {inner}
    </div>"""

    def tech_cards(items, prefix):
        return '<div class="tech-cards">' + "".join(
            f'<figure class="tech-card"><img src="assets/img/drzwi/{prefix}-tech-{f}.jpg" alt="{n}" loading="lazy">'
            f'<figcaption><strong>{n}</strong><span>Grubość skrzydła {mm}</span></figcaption></figure>'
            for n, mm, f in items) + "</div>"

    def tiles(items, path, cls):
        return f'<div class="pick-grid {cls}" data-lightbox>' + "".join(
            f'<a href="assets/img/{path(f)}.jpg" data-lightbox-item><img src="assets/img/{path(f)}.jpg" alt="{n}" loading="lazy"><span>{n}</span></a>'
            for n, f in items) + "</div>"

    def swatches(items, prefix):
        return '<div class="swatches-grid">' + "".join(
            f'<figure><img src="assets/img/drzwi/{prefix}-kolor-{f}.jpg" alt="{n}" loading="lazy"><figcaption>{n}</figcaption></figure>'
            for n, f in items) + "</div>"

    # 02 — kolekcje Wikęd: zakładki + modele tylko z wybranej kolekcji
    tabs = '<div class="chips chips--tabs" role="tablist">' + "".join(
        f'<button type="button" class="{"is-active" if k == 0 else ""}" data-filter-btn="{c}">{c}</button>'
        for k, c in enumerate(DZ_WIKED_KOLEKCJE)) + "</div>"
    modele = '<div class="pick-grid pick-grid--doors pick-grid--contain pick-grid--models" data-lightbox data-filter-grid>' + "".join(
        f'<a href="assets/img/drzwi/wiked-modele/{f}.jpg" data-lightbox-item data-filter="{c}"{"" if c == DZ_WIKED_KOLEKCJE[0] else " hidden"}>'
        f'<img src="assets/img/drzwi/wiked-modele/{f}.jpg" alt="Wikęd {c} {n}" loading="lazy"><span>{n}</span></a>'
        for c, n, f in DZ_WIKED_MODELE) + "</div>"

    palety = ('<div class="chips chips--tabs" role="tablist">' + "".join(
        f'<button type="button" class="{"is-active" if k == 0 else ""}" data-filter-btn="{key}">{label}</button>'
        for k, (key, label) in enumerate(DZ_WIKED_PALETY)) + "</div>"
        + '<div class="swatches-grid" data-filter-grid>' + "".join(
        f'<figure data-filter="{p}"{"" if p == DZ_WIKED_PALETY[0][0] else " hidden"}><img src="assets/img/drzwi/wiked-kolor-{f}.jpg" alt="{n}" loading="lazy"><figcaption>{n}</figcaption></figure>'
        for p, n, f in DZ_WIKED_KOLORY) + "</div>")

    uchwyty = ("""<div class="step-text step-text--top">
        <h4>Które rozwiązanie sprawdzi się lepiej?</h4>
        <p><strong>Klamka</strong> to klasyczne i uniwersalne rozwiązanie. Jest wygodna w codziennym użytkowaniu, dostępna w wielu kształtach i kolorach, dzięki czemu łatwo dopasować ją do stylu drzwi oraz pozostałych elementów stolarki.</p>
        <p><strong>Pochwyt</strong> to propozycja dla osób, które cenią nowoczesny design. Doskonale komponuje się z prostymi, minimalistycznymi drzwiami. To doskonały wybór dla osób, które szukają niestandardowych rozwiązań i chcą wyróżnić wejście do swojego domu.</p>
      </div>"""
               + '<h4 class="palette-title">Pochwyty</h4>' + tiles(DZ_WIKED_POCHWYTY, lambda f: f"drzwi/wiked-pochwyt-{f}", "pick-grid--sq")
               + '<h4 class="palette-title">Klamki</h4>' + tiles(DZ_WIKED_KLAMKI, lambda f: f"drzwi/wiked-klamka-{f}", "pick-grid--sq"))

    smart_pts = "".join(f'<span class="smart__pin" style="left:{x}%;top:{y}%" title="{t}">{n}</span>' for n, x, y, t in DZ_SMART_PUNKTY)
    smart_legend = "".join(f'<li><span>{n}</span>{t}</li>' for n, x, y, t in DZ_SMART_PUNKTY)
    smart_list = "".join(f'<li><strong>{t}</strong><p>{d}</p></li>' for t, d in DZ_SMART)

    insp = '<div class="gallery gallery--okna" data-lightbox>' + "".join(
        f'<a href="assets/img/{g}.jpg" data-lightbox-item><img src="assets/img/{g}.jpg" alt="Drzwi Wikęd — inspiracja" loading="lazy"></a>'
        for g in DZ_WIKED_INSPIRACJE) + "</div>"

    faq = "".join(f"""<div class="faq__row">
      <button class="faq__q"><span>{q}</span><span>+</span></button>
      <div class="faq__a">{a}</div>
    </div>""" for q, a in DZ_FAQ)

    rel = ""
    for s in ["okna", "bramy-garazowe", "drzwi-wewnetrzne"]:
        rel += f"""<a href="{s}.html"><article class="card">
        <img src="assets/img/{PROD_IMG[s]}.jpg" alt="{PROD_LABEL[s]}" style="height:150px;object-fit:cover;border-radius:var(--r-md)">
        <div><h3>{PROD_LABEL[s]}</h3></div>
        <span class="card__more">Zobacz ofertę {I['arrow']}</span>
      </article></a>"""

    # nagłówek jak na wiked.pl: tekst wjeżdża linijkami, obok wysoki film „wejście do domu”
    body = pagehero("wiked92", "Wikęd i Erkado – drzwi dopasowane do Twojego domu",
                    "Postaw na drzwi, które łączą estetykę z funkcjonalnością i podkreślają charakter Twojego domu już od samego wejścia.", None)
    body += f"""<section class="section section--tight-bottom" id="wiked">
  <div class="container">
    <div class="brand-split">
      <div class="brand-split__text">
        <img class="brand-split__logo" src="assets/img/drzwi/wiked-logo.png" alt="Wikęd">
        <p>Wikęd to polski producent drzwi zewnętrznych, który łączy nowoczesne wzornictwo z solidnym wykonaniem. Szeroka oferta modeli, kolorów i dodatków pozwala dopasować drzwi do stylu każdego domu, zapewniając estetykę, komfort i bezpieczeństwo na co dzień.</p>
        <div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn--primary" href="kontakt.html">Zapytaj o wycenę {I['arrow']}</a></div>
      </div>
      <div class="brand-split__media">
        <video autoplay muted loop playsinline preload="metadata" poster="assets/img/drzwi/wiked-wejscie.jpg">
          <source src="assets/img/drzwi/wiked-wejscie.webm" type="video/webm">
          <source src="assets/img/drzwi/wiked-wejscie.mp4" type="video/mp4">
        </video>
      </div>
    </div>

    <h2 class="h-sec steps-title">Wybierz drzwi Wikęd krok po kroku</h2>
    {step(1, "Technologia", tech_cards(DZ_WIKED_TECH, "wiked"))}
    {step(2, "Kolekcja i wzór", tabs + modele)}
    {step(3, "Kolor", palety + '<p class="step-note">Oraz pełny wzornik RAL K7 Classic.</p>')}
    {step(4, "Pochwyty i klamki", uchwyty)}
    {step(5, "Przeszklenie", '<div class="step-text step-text--top"><p>Przeszklenie w drzwiach zewnętrznych to sposób na doświetlenie wnętrza naturalnym światłem i nadanie wejściu wyjątkowego charakteru. Wybór szyby zależy od tego, ile światła chcesz wpuścić do wnętrza i jaką prywatność chcesz zachować. Do wyboru są różne rodzaje szkła, dzięki którym można dopasować drzwi zarówno do nowoczesnej, jak i klasycznej architektury domu.</p></div>' + tiles(DZ_WIKED_SZYBY, lambda f: f"drzwi/wiked-szyba-{f}", "pick-grid--sq"))}
  </div>
</section>

<section class="section section--soft">
  <div class="container smart">
    <div class="smart__text">
      <h2 class="h-sec">Drzwi SMART — otwierasz telefonem</h2>
      <ul class="smart__list">{smart_list}</ul>
      <a class="btn btn--primary" href="kontakt.html">Zapytaj o drzwi SMART {I['arrow']}</a>
    </div>
    <div class="smart__media">
      <div class="smart__img"><img src="assets/img/drzwi/wiked-smart.jpg" alt="Drzwi Wikęd SMART z podświetleniem LED" loading="lazy">{smart_pts}</div>
      <ol class="smart__legend">{smart_legend}</ol>
    </div>
  </div>
</section>

<section class="advantages"><div class="container advantages__inner">{adv_html(DZ_ADV_WIKED)}</div></section>

<section class="section section--tight-bottom" id="erkado">
  <div class="container">
    <div class="brand-split">
      <div class="brand-split__text">
        <img class="brand-split__logo" src="assets/img/drzwi/erkado-logo.png" alt="Erkado">
        <p>Erkado to polski producent drzwi z ponad 50-letnim doświadczeniem, oferujący szeroki wybór modeli łączących nowoczesny design z funkcjonalnością. Bogata oferta pozwoli Ci wybrać drzwi odpowiadające Twoim oczekiwaniom.</p>
        <div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn--primary" href="kontakt.html">Zapytaj o wycenę {I['arrow']}</a></div>
      </div>
      <div class="brand-split__media"><img src="assets/img/drzwi/erkado-glowne.jpg" alt="Drzwi stalowe Erkado — detal pochwytu"></div>
    </div>

    <h2 class="h-sec steps-title">Wybierz drzwi Erkado krok po kroku</h2>
    {step(1, "Technologia", tech_cards(DZ_ERKADO_TECH, "erkado"))}
    {step(2, "Model", tiles(DZ_ERKADO_MODELE, lambda f: f"drzwi/erkado-model-{f}", "pick-grid--doors pick-grid--contain"))}
    {step(3, "Kolor", swatches(DZ_ERKADO_KOLORY, "erkado"))}
  </div>
</section>
<section class="advantages"><div class="container advantages__inner">{adv_html(DZ_ADV_ERKADO)}</div></section>

<section class="section section--soft">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Warto wiedzieć przed zakupem</h2></div></div>
    <div class="faq">{faq}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Inspiracje</h2></div></div>
    {insp}
  </div>
</section>

{cta("Doradztwo i wycena", "Planujesz inwestycję budowlaną?",
     "Skontaktuj się z nami — doradzimy technicznie i przygotujemy kalkulację cenową.")}

<section class="section related">
  <div class="container">
    <h2 class="h-sec" style="margin-bottom:32px">Sprawdź również inne systemy</h2>
    <div class="grid-3">{rel}</div>
  </div>
</section>
"""
    write("drzwi-zewnetrzne.html", head("Drzwi zewnętrzne Wikęd i Erkado | PROMYK Wieluń",
                                        "Drzwi zewnętrzne Wikęd (Alu Hybrid, Termo Prestige, Optimum, Prima) i Erkado (Thermo 64–88). Kolekcje, kolory, pochwyty, klamki, drzwi SMART — doradztwo i montaż PROMYK Wieluń.")
          + nav("drzwi-zewnetrzne") + body + footer())


# ================================================================ DRZWI WEWNĘTRZNE (uwagi klienta 20.10.2026) ----
DW_ROWS = [
    ("Drzwi przylgowe",
     ["Klasyczne rozwiązanie z widoczną przylgą na krawędzi skrzydła.",
      "Uniwersalny wygląd pasujący do wielu aranżacji.",
      "Sprawdzony wybór do tradycyjnych i nowoczesnych pomieszczeń."],
     "dw/przylgowe", "katalog-dre.pdf"),
    ("Drzwi bezprzylgowe",
     ["Minimalistyczny design z gładką krawędzią skrzydła.",
      "Po zamknięciu tworzą jedną płaszczyznę z ościeżnicą.",
      "Idealne do nowoczesnych i eleganckich wnętrz."],
     "dre_nestor11", "katalog-dre.pdf"),
    ("Drzwi ukryte",
     ["Ościeżnica zlicowana ze ścianą, bez widocznych opasek.",
      "Minimalistyczny design, który nie zaburza aranżacji pomieszczenia.",
      "Możliwość dopasowania wykończenia skrzydła do koloru ściany.",
      "Doskonały wybór do nowoczesnych i eleganckich wnętrz."],
     "dre_saraeco", "katalog-porta.pdf"),
    ("Drzwi przesuwne",
     ["Praktyczne rozwiązanie, które pozwala zaoszczędzić miejsce w pomieszczeniu.",
      "Szeroki wybór wzorów, kolorów i przeszkleń.",
      "Idealne do nowoczesnych mieszkań, garderób i pomieszczeń, w których liczy się funkcjonalność."],
     "dw/przesuwne-belka", "katalog-erkado-wewnetrzne.pdf"),
    ("Drzwi szklane i loftowe",
     ["Nowoczesne wzornictwo, które przyciąga uwagę i podkreśla charakter wnętrza.",
      "Szklane skrzydła, także z czarnymi ramami i szprosami w stylu loftowym.",
      "Doskonałe do nowoczesnych aranżacji, w których liczy się dostęp do naturalnego światła."],
     "dw/szklane-loftowe", "katalog-erkado-wewnetrzne.pdf"),
]
DW_ADV = [("Wzory i kolory", "Kolekcje DRE, Porta i Erkado — od klasyki po loft", "palette"),
          ("Dopasowanie do wnętrza", "Drzwi przylgowe, bezprzylgowe, ukryte, przesuwne i szklane", "sparkle"),
          ("Pomiar i montaż", "Pomagamy na każdym etapie — od wyboru po montaż", "ruler")]
DW_INSPIRACJE = ["dw/insp-drewno-1", "dre_binito50", "dw/przesuwne-belka", "dre_nestor11",
                 "dw/przesuwne-dab", "dre_saraeco", "dw/insp-drewno-2", "dre_nella6",
                 "dw/insp-drewno-3", "dw/szklane-loftowe", "dw/insp-erkado-20", "dw/insp-drewno-4"]
DW_FAQ_NOWE = [
    ("Jak dobrać kolor drzwi do podłogi i ścian?",
     "<p>Kolor drzwi warto dopasować do podłogi, ścian i stylu całego wnętrza. Nie musi być identyczny – ważne, aby poszczególne elementy dobrze ze sobą współgrały.</p>"
     "<ul><li><strong>Drzwi w kolorze podłogi</strong> – tworzą spójną aranżację i sprawdzają się szczególnie w klasycznych wnętrzach.</li>"
     "<li><strong>Drzwi kontrastujące z podłogą</strong> – np. czarne lub ciemne przy jasnych panelach, nadają wnętrzu wyrazisty charakter.</li>"
     "<li><strong>Drzwi dopasowane do ścian</strong> – białe lub w podobnym odcieniu optycznie wtapiają się w tło i nie dominują w pomieszczeniu.</li>"
     "<li><strong>Drzwi w kolorze drewna</strong> – ocieplają wnętrze i dobrze komponują się z naturalnymi materiałami.</li></ul>"),
    ("Czy można zamówić drzwi w niestandardowym kolorze?",
     "<p>Tak, w zależności od producenta i wybranego modelu istnieje możliwość zamówienia drzwi w niestandardowym kolorze lub wykończeniu. Dostępne opcje obejmują różne odcienie, dekory drewnopodobne oraz wybrane kolory z palety RAL. Zakres personalizacji zależy od konkretnej kolekcji, dlatego warto sprawdzić dostępne możliwości przed złożeniem zamówienia.</p>"),
    ("Czy oferujecie pomiar i montaż drzwi?",
     "<p>Tak, oferujemy możliwość pomiaru i montażu drzwi. Pomagamy na każdym etapie – od wyboru odpowiedniego modelu i dopasowania ościeżnicy, po ustalenie szczegółów montażu. Dzięki temu masz pewność, że drzwi będą dobrze dopasowane do otworu i przygotowane do prawidłowego użytkowania.</p>"),
]


def build_drzwi_wewnetrzne():
    rows = ""
    for k, (title, bullets, img, cat) in enumerate(DW_ROWS):
        li = "".join(f'<li><span class="check">{I["check"]}</span> {b}</li>' for b in bullets)
        media = f'<div><img src="assets/img/{img}.jpg" alt="{title}" loading="lazy"></div>'
        text = f"""<div class="subrow__text">
        <h2>{title}</h2>
        <ul class="bullets">{li}</ul>
        <div style="display:flex;gap:12px;flex-wrap:wrap">
          <a class="btn btn--primary btn--sm" href="assets/katalogi/{cat}" target="_blank" rel="noopener">Odkryj dostępne modele {I['arrow']}</a>
          <a class="btn btn--outline btn--sm" href="kontakt.html">Zapytaj o wycenę {I['arrow']}</a>
        </div>
      </div>"""
        flip = k % 2
        rows += f'<div class="subrow{" subrow--flip" if flip else ""}">{media if not flip else text}{text if not flip else media}</div>'

    adv = "".join(f"""<div class="adv"><span class="adv__icon">{I[ic]}</span>
      <div><h3>{t}</h3><p>{d}</p></div></div>""" for t, d, ic in DW_ADV)

    stare = PRODUCT_EXTRAS["drzwi-wewnetrzne"]["know"][:4]
    stare = [(q, a.replace(" Do łazienek polecamy DRE WaterProof — testowana na długi kontakt z wodą.", "")) for q, a in stare]
    faq = "".join(f"""<div class="faq__row">
      <button class="faq__q"><span>{q}</span><span>+</span></button>
      <div class="faq__a">{a}</div>
    </div>""" for q, a in stare + DW_FAQ_NOWE)

    insp = '<div class="gallery gallery--okna" data-lightbox>' + "".join(
        f'<a href="assets/img/{g}.jpg" data-lightbox-item><img src="assets/img/{g}.jpg" alt="Drzwi wewnętrzne — inspiracja" loading="lazy"></a>'
        for g in DW_INSPIRACJE) + "</div>"

    rel = ""
    for s in ["drzwi-zewnetrzne", "okna", "oslony-wewnetrzne"]:
        rel += f"""<a href="{s}.html"><article class="card">
        <img src="assets/img/{PROD_IMG[s]}.jpg" alt="{PROD_LABEL[s]}" style="height:150px;object-fit:cover;border-radius:var(--r-md)">
        <div><h3>{PROD_LABEL[s]}</h3></div>
        <span class="card__more">Zobacz ofertę {I['arrow']}</span>
      </article></a>"""

    body = pagehero("dw/hero-loft", "Drzwi wewnętrzne DRE, Porta i Erkado – styl i funkcjonalność na co dzień",
                    "Szeroki wybór wzorów, kolorów i przeszkleń, dzięki którym dopasujesz drzwi do swojego domu.", None)
    body += f"""<section class="section section--tight-bottom"><div class="container">{rows}</div></section>
<section class="advantages"><div class="container advantages__inner">{adv}</div></section>

<section class="section section--soft">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Warto wiedzieć przed zakupem</h2></div></div>
    <div class="faq">{faq}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Inspiracje</h2></div></div>
    {insp}
  </div>
</section>

{cta("Doradztwo i wycena", "Planujesz inwestycję budowlaną?",
     "Skontaktuj się z nami — doradzimy technicznie i przygotujemy kalkulację cenową.")}

<section class="section related">
  <div class="container">
    <h2 class="h-sec" style="margin-bottom:32px">Sprawdź również inne systemy</h2>
    <div class="grid-3">{rel}</div>
  </div>
</section>
"""
    write("drzwi-wewnetrzne.html", head("Drzwi wewnętrzne DRE, Porta i Erkado | PROMYK Wieluń",
                                        "Drzwi wewnętrzne DRE, Porta i Erkado: przylgowe, bezprzylgowe, ukryte, przesuwne, szklane i loftowe. Pomiar i montaż — PROMYK Wieluń.")
          + nav("drzwi-wewnetrzne") + body + footer())


# ================================================================ ROLETY ZEWNĘTRZNE (uwagi klienta 20.10.2026) ----
ROL_ROWS = [
    ("Adaptacyjne",
     ["Montaż na elewacji lub we wnęce — bez prac murarskich",
      "Sterowanie ręczne lub elektryczne – wygodna obsługa dopasowana do indywidualnych potrzeb",
      "Pancerz aluminiowy z pianką PU, prowadnice z uszczelką szczotkową",
      "Kolory RAL i drewnopodobne spójne ze stolarką"], "al30_rol"),
    ("Podtynkowe",
     ["Skrzynka kryta tynkiem — niewidoczna w elewacji",
      "Montaż warto uwzględnić już na etapie projektowania budynku.",
      "Dedykowane do budynków energooszczędnych i pasywnych",
      "Dostęp serwisowy przez klapę rewizyjną"], "rol/podtynkowe"),
    ("Sterowanie",
     ["Możliwość wyboru obsługi ręcznej (linka) lub elektrycznej",
      "Wyłączniki naścienne i piloty wielokanałowe",
      "Możliwość ustawienia godzin podnoszenia i opuszczania rolet",
      "Sterowanie grupowe - jednoczesna obsługa kilku rolet za pomocą jednego urządzenia.",
      "Centrala TaHoma (Somfy) – inteligentne zarządzanie roletami za pomocą aplikacji"], "rol/sterowanie"),
]
ROL_ADV = [("Komfort latem i zimą", "Mniej nagrzewania w upały i mniejsze straty ciepła zimą", "thermo"),
           ("Bezpieczeństwo i prywatność", "Dodatkowa osłona okien przed wzrokiem i włamaniem", "lock"),
           ("Wygodna obsługa", "Ręcznie, przyciskiem, pilotem lub z aplikacji", "cog")]
ROL_KOLORY_STD = [("bialy", "Biały"), ("szary", "Szary"), ("antracyt", "Szary antracyt"), ("bezowy", "Beżowy"),
                  ("brazowy", "Brązowy"), ("ciemnobrazowy", "Ciemnobrązowy"), ("srebrny", "Srebrny")]
ROL_KOLORY_DREWNO = [("jasny-dab", "Jasny dąb"), ("dab-slodowy", "Dąb słodowy"), ("zloty-dab", "Złoty dąb"),
                     ("orzech", "Orzech"), ("winchester", "Winchester"), ("wenge", "Wenge"), ("mahon", "Mahoń")]
ROL_FAQ = [
    ("Czy rolety zewnętrzne można zamontować w istniejącym budynku?",
     "Tak, rolety zewnętrzne można zamontować również w istniejących budynkach. W takim przypadku najczęściej wybierane są rolety adaptacyjne, które nie wymagają ingerencji w konstrukcję ścian i można je dopasować do elewacji."),
    ("Który system do jakiego domu?",
     "Na etapie budowy najlepsze są rolety podtynkowe (niewidoczne skrzynki). W budynku wykończonym jedyną nieinwazyjną opcją są adaptacyjne — montowane na elewacji lub we wnęce."),
    ("Kiedy najlepiej zaplanować montaż rolet podtynkowych?",
     "Montaż rolet podtynkowych najlepiej uwzględnić już na etapie projektowania budynku. Pozwala to odpowiednio przygotować otwory okienne i zaplanować ocieplenie elewacji, aby estetycznie ukryć skrzynki rolet."),
    ("Czy rolety zewnętrzne wymagają podłączenia do prądu?",
     "Nie zawsze. Rolety zewnętrzne mogą być obsługiwane ręcznie (za pomocą linki) lub elektrycznie. Tylko w przypadku sterowania elektrycznego konieczne jest zasilanie."),
    ("Czy rolety zewnętrzne chronią przed nagrzewaniem pomieszczeń latem?",
     "Tak, rolety zewnętrzne skutecznie ograniczają nagrzewanie pomieszczeń latem, ponieważ zatrzymują część promieni słonecznych przed szybą. Dzięki temu we wnętrzach można utrzymać przyjemniejszą temperaturę nawet podczas upałów."),
    ("Czy rolety zewnętrzne pomagają utrzymać ciepło zimą?",
     "Tak, rolety zewnętrzne tworzą dodatkową warstwę izolacyjną, która pomaga ograniczyć straty ciepła zimą. Dzięki temu mogą poprawić komfort termiczny pomieszczeń i wspierać oszczędność energii."),
    ("Czy roleta może mieć moskitierę?",
     "Tak — moskitierę rolowaną można prowadzić w tych samych, łączonych prowadnicach co roletę. Nie zabiera światła, a gdy nie jest potrzebna, po prostu się ją zwija."),
]


def build_rolety_zewnetrzne():
    rows = ""
    for k, (title, bullets, img) in enumerate(ROL_ROWS):
        li = "".join(f'<li><span class="check">{I["check"]}</span> {b}</li>' for b in bullets)
        media = f'<div><img src="assets/img/{img}.jpg" alt="Rolety zewnętrzne — {title.lower()}" loading="lazy"></div>'
        text = f"""<div class="subrow__text">
        <h2>{title}</h2>
        <ul class="bullets">{li}</ul>
        <a class="btn btn--primary btn--sm" href="kontakt.html">Zapytaj o wycenę {I['arrow']}</a>
      </div>"""
        flip = k % 2
        rows += f'<div class="subrow{" subrow--flip" if flip else ""}">{media if not flip else text}{text if not flip else media}</div>'

    adv = "".join(f"""<div class="adv"><span class="adv__icon">{I[ic]}</span>
      <div><h3>{t}</h3><p>{d}</p></div></div>""" for t, d, ic in ROL_ADV)

    def swatches(items):
        return '<div class="swatches-grid">' + "".join(
            f'<figure><img src="assets/img/rol/kolor-{f}.jpg" alt="{n}" loading="lazy"><figcaption>{n}</figcaption></figure>'
            for f, n in items) + "</div>"

    faq = "".join(f"""<div class="faq__row">
      <button class="faq__q"><span>{q}</span><span>+</span></button>
      <div class="faq__a"><p>{a}</p></div>
    </div>""" for q, a in ROL_FAQ)

    rel = ""
    for s in ["okna", "oslony-zewnetrzne", "moskitiery"]:
        rel += f"""<a href="{s}.html"><article class="card">
        <img src="assets/img/{PROD_IMG[s]}.jpg" alt="{PROD_LABEL[s]}" style="height:150px;object-fit:cover;border-radius:var(--r-md)">
        <div><h3>{PROD_LABEL[s]}</h3></div>
        <span class="card__more">Zobacz ofertę {I['arrow']}</span>
      </article></a>"""

    tahoma_li = "".join(f'<li><span class="check">{I["check"]}</span> {b}</li>' for b in [
        "Sterowanie roletami z telefonu — w domu i poza nim",
        "Scenariusze uruchamiane jednym dotknięciem, np. „Wyjście z domu” lub „Dobranoc”",
        "Harmonogramy podnoszenia i opuszczania rolet o wybranych godzinach",
        "Rolety, brama, markiza i oświetlenie w jednej aplikacji",
        "Obsługa głosowa przez Asystenta Google i Amazon Alexa"])

    body = pagehero("rol/hero", "Rolety zewnętrzne Aluprof – nowoczesne rozwiązania dla Twojego domu",
                    "Aluminiowe profile wypełnione pianką pomagają ograniczyć straty ciepła, chronią przed nadmiernym nasłonecznieniem i zapewniają mieszkańcom większy komfort na co dzień.", None)
    body += f"""<section class="section section--tight-bottom"><div class="container">{rows}</div></section>
<section class="advantages"><div class="container advantages__inner">{adv}</div></section>

<section class="section section--soft">
  <div class="container">
    <div class="tahoma">
      <div class="tahoma__media"><img src="assets/img/rol/tahoma-switch.png" alt="Centrala Somfy TaHoma switch i aplikacja w telefonie" loading="lazy"></div>
      <div class="tahoma__text">
        <h2 class="h-sec">Inteligentny dom z TaHoma® (Somfy)</h2>
        <p>TaHoma® switch to centrala Somfy, która łączy rolety z innymi urządzeniami w domu. Sterujesz nimi z aplikacji w telefonie, a zaprogramowane scenariusze same podnoszą i opuszczają rolety o odpowiedniej porze — także wtedy, gdy nie ma Cię w domu.</p>
        <ul class="bullets">{tahoma_li}</ul>
        <a class="btn btn--primary btn--sm" href="kontakt.html">Zapytaj o wycenę {I['arrow']}</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Kolory rolet</h2></div></div>
    <h4 class="palette-title">Kolory standardowe</h4>
    {swatches(ROL_KOLORY_STD)}
    <h4 class="palette-title">Kolory drewnopodobne</h4>
    {swatches(ROL_KOLORY_DREWNO)}
    <p class="colors-note">Dostępne są również inne, niestandardowe kolory — zapytaj nas o szczegóły.</p>
  </div>
</section>

<section class="section section--soft">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Warto wiedzieć przed zakupem</h2></div></div>
    <div class="faq">{faq}</div>
  </div>
</section>

{cta("Doradztwo i wycena", "Planujesz inwestycję budowlaną?",
     "Skontaktuj się z nami — doradzimy technicznie i przygotujemy kalkulację cenową.")}

<section class="section related">
  <div class="container">
    <h2 class="h-sec" style="margin-bottom:32px">Sprawdź również inne systemy</h2>
    <div class="grid-3">{rel}</div>
  </div>
</section>
"""
    write("rolety-zewnetrzne.html", head("Rolety zewnętrzne Aluprof — adaptacyjne i podtynkowe, sterowanie Somfy TaHoma | PROMYK Wieluń",
                                         "Rolety zewnętrzne Aluprof: adaptacyjne i podtynkowe, sterowanie ręczne, elektryczne i z aplikacji Somfy TaHoma. Kolory standardowe i drewnopodobne — PROMYK Wieluń.")
          + nav("rolety-zewnetrzne") + body + footer())


# ================================================================ PARAPETY (Jaro-Max, dopisane 20.10.2026) ----
PARAPETY_KOLORY = {
    'w-granit': [('Vanga', 'w-granit-01'), ('Blue Night', 'w-granit-02'), ('Colonial White', 'w-granit-03'), ('Royal Black', 'w-granit-04'), ('Nero Impala', 'w-granit-05'), ('Tan Brown', 'w-granit-06'), ('China Cristal', 'w-granit-07'), ('Steel Grey', 'w-granit-08'), ('Yellow Pink', 'w-granit-09'), ('Rosa Beta', 'w-granit-10'), ('Steel Grey Lapatura', 'w-granit-11'), ('Nero Assoluto (polerowany)', 'w-granit-12'), ('Nero Assoluto (płomień i szczotka)', 'w-granit-13')],
    'w-kwarcyt': [('Bianchissimo', 'w-kwarcyt-01'), ('Vittoria White', 'w-kwarcyt-02'), ('Navona', 'w-kwarcyt-03'), ('Blanco Paloma', 'w-kwarcyt-04'), ('Gris Ceniza', 'w-kwarcyt-06'), ('Black Nimbus', 'w-kwarcyt-07'), ('City Dark', 'w-kwarcyt-08'), ('Gris Antracita', 'w-kwarcyt-09'), ('Black Mamba', 'w-kwarcyt-10')],
    'w-marmur': [('Polare', 'w-marmur-01'), ('Monte Bianco', 'w-marmur-02'), ('Bianco Carrara', 'w-marmur-03'), ('Perla Arte', 'w-marmur-04'), ('Beige Marfil', 'w-marmur-05'), ('Marmo White', 'w-marmur-06'), ('Baltic Grey', 'w-marmur-07'), ('Crystal White', 'w-marmur-08'), ('Botticino', 'w-marmur-09'), ('Breccia Aurora', 'w-marmur-10'), ('Calacatta Gold', 'w-marmur-11'), ('Perlato Appia', 'w-marmur-12'), ('Rosso Asiago', 'w-marmur-13'), ('Beige Luna', 'w-marmur-14'), ('Giorgione', 'w-marmur-15'), ('White Iceberg', 'w-marmur-16'), ('Cotone', 'w-marmur-18')],
    'w-fornir': [('Dąb naturalny', 'w-fornir-01'), ('Winchester', 'w-fornir-02'), ('Złoty dąb', 'w-fornir-03'), ('Dąb orzech', 'w-fornir-04'), ('Stary złoty dąb', 'w-fornir-05'), ('Dąb orzech ciemny', 'w-fornir-06'), ('Dąb mahoń', 'w-fornir-07'), ('Dąb bielony', 'w-fornir-08'), ('Dąb grafit', 'w-fornir-09')],
    'w-laminat': [('Cream Beige', 'w-laminat-01'), ('Subtle Nude', 'w-laminat-02'), ('Subtle Taupe', 'w-laminat-03'), ('Biały mat', 'w-laminat-04'), ('Biały połysk', 'w-laminat-05'), ('Marmur jasny', 'w-laminat-06'), ('Beton ciemny', 'w-laminat-07'), ('Granit szary', 'w-laminat-08'), ('Dąb Ribbeck', 'w-laminat-09'), ('Jasny dąb', 'w-laminat-10'), ('Dąb Sonoma', 'w-laminat-11'), ('Dąb naturalny', 'w-laminat-12'), ('Orzech Lanzado', 'w-laminat-13'), ('Winchester', 'w-laminat-14'), ('Beton', 'w-laminat-15'), ('Dąb vintage', 'w-laminat-16'), ('Białe drewno', 'w-laminat-17'), ('Dąb Watan', 'w-laminat-18'), ('Dąb London', 'w-laminat-19'), ('Dąb Argos', 'w-laminat-20'), ('Jabłoń', 'w-laminat-21'), ('Złoty dąb', 'w-laminat-22'), ('Antracyt', 'w-laminat-23')],
    'w-lakier': [('Perła łuska', 'w-lakier-01'), ('Biały mat', 'w-lakier-02'), ('Biały połysk', 'w-lakier-03'), ('Biały wysoki połysk', 'w-lakier-04'), ('Czarny mat', 'w-lakier-05'), ('Marmurek czarny', 'w-lakier-06'), ('Marmurek biały', 'w-lakier-07'), ('Antracyt RAL 7016 półmat', 'w-lakier-08')],
    'w-pcv': [('Biały', 'w-pcv-01'), ('Marmur', 'w-pcv-02'), ('Orzech', 'w-pcv-03'), ('Złoty dąb', 'w-pcv-04'), ('Dąb skandynawski', 'w-pcv-05'), ('Winchester', 'w-pcv-06'), ('Grafit', 'w-pcv-07')],
    'z-granit': [('Vanga', 'z-granit-01'), ('Blue Night', 'z-granit-02'), ('Colonial White', 'z-granit-03'), ('Royal Black', 'z-granit-04'), ('Nero Impala', 'z-granit-05'), ('Tan Brown', 'z-granit-06'), ('China Cristal', 'z-granit-07'), ('Steel Grey', 'z-granit-08'), ('Yellow Pink', 'z-granit-09'), ('Rosa Beta', 'z-granit-10'), ('Imperial White', 'z-granit-11'), ('Steel Grey Lapatura', 'z-granit-12'), ('Nero Assoluto (polerowany)', 'z-granit-13'), ('Nero Assoluto (płomień i szczotka)', 'z-granit-14')],
    'z-contour': [('RAL 1011', 'z-contour-01'), ('RAL 7016', 'z-contour-02'), ('RAL 7024', 'z-contour-03'), ('RAL 8003', 'z-contour-04'), ('RAL 8017', 'z-contour-05'), ('RAL 8019', 'z-contour-06'), ('RAL 8028', 'z-contour-07'), ('RAL 9016', 'z-contour-08'), ('RAL 9005', 'z-contour-09')],
    'z-alu': [('Ciemny brąz RAL 8019', 'z-alu-01'), ('Gładki antracyt RAL 7016', 'z-alu-02'), ('Biały RAL 9016', 'z-alu-03')],
    'z-aluplytka': [('Biały RAL 9016', 'z-aluplytka-01'), ('Gładki antracyt RAL 7016', 'z-aluplytka-02'), ('Miedź antyczna', 'z-aluplytka-03'), ('Antracyt antyczny', 'z-aluplytka-04'), ('Złoto antyczne', 'z-aluplytka-05'), ('Dąb antyczny', 'z-aluplytka-06'), ('Jasny brąz RAL 8017', 'z-aluplytka-07'), ('JM 8230 drobna struktura', 'z-aluplytka-08'), ('RAL 7016 drobna struktura', 'z-aluplytka-09'), ('RAL 9006 drobna struktura', 'z-aluplytka-10'), ('RAL 9005 drobna struktura', 'z-aluplytka-11'), ('Ciemny brąz RAL 8019', 'z-aluplytka-12')],
    'z-stal': [('Ciemny brąz RAL 8019', 'z-stal-01'), ('Jasny brąz RAL 8017', 'z-stal-02'), ('Gładki antracyt RAL 7016', 'z-stal-03'), ('Srebrny RAL 9006', 'z-stal-04'), ('Biały RAL 9010', 'z-stal-05')],
    'z-staldrewno': [('Winchester', 'z-staldrewno-01'), ('Złoty dąb', 'z-staldrewno-02'), ('Orzech', 'z-staldrewno-03'), ('Dąb naturalny', 'z-staldrewno-04')],
}
PARAPETY_TYPY = {
    "wewnetrzne": [
        ("w-granit", "Granitowe", "Kamień naturalny — bardzo twardy, odporny na ścieranie, wilgoć i temperaturę. Każdy parapet ma niepowtarzalny rysunek.", "Grubość 20 lub 30 mm"),
        ("w-kwarcyt", "Kwarcytowe", "Konglomerat z 90–95% kamienia naturalnego — podwyższona odporność na zarysowania, wilgoć i wysoką temperaturę, modne jednolite barwy.", "Grubość 20 lub 30 mm"),
        ("w-marmur", "Marmurowe", "Konglomerat marmurowy — szlachetny wygląd marmuru w nowoczesnym wydaniu i szeroka paleta jasnych, ciepłych odcieni.", "Grubość 20 lub 30 mm"),
        ("w-fornir", "MDF fornirowane", "Płyta MDF z naturalną okleiną z drewna — ciepły charakter, łatwy do zgrania z podłogą, drzwiami i meblami.", "Grubość 20 mm"),
        ("w-laminat", "MDF laminowane", "Płyta MDF oklejana laminatem — odporna na zarysowania, wilgoć i UV. Ponad 20 dekorów: od bieli, przez beton, po drewno.", "Grubość 20, 25 lub 30 mm"),
        ("w-lakier", "MDF lakierowane", "Wodoodporna płyta MDF z gładką, lakierowaną powierzchnią — biel, czerń i antracyt, w macie lub w połysku.", "Grubość 20, 25 lub 30 mm"),
        ("w-pcv", "PCV", "Komorowe profile PCV pokryte okleiną — lekkie, praktyczne i ekonomiczne rozwiązanie.", "Długość do 6 m"),
    ],
    "zewnetrzne": [
        ("z-granit", "Granitowe", "Mrozoodporny i praktycznie nienasiąkliwy granit — klasyczny, kamienny wygląd na lata, bez specjalnej konserwacji.", "Grubość 20 lub 30 mm"),
        ("z-contour", "JM External Contour", "Nowoczesne parapety z blachy aluminiowej lub stalowej o wyrazistym konturze, lakierowane proszkowo.", "Dowolny kolor z palety RAL"),
        ("z-alu", "Aluminiowe", "Lekka i trwała blacha aluminiowa 1 lub 1,5 mm, odporna na korozję. Profil Standard lub Soft.", "3 kolory podstawowe lub dowolny RAL"),
        ("z-aluplytka", "Alu-Płytka", "Aluminium z przetłoczeniami imitującymi płytkę klinkierową — świetnie pasuje do elewacji z cegły i klinkieru.", "Profil Contour lub Soft"),
        ("z-stal", "Stalowe", "Blacha stalowa 0,7 mm powlekana poliestrem — sprawdzone, ekonomiczne rozwiązanie odporne na warunki atmosferyczne.", "Szerokości 100–400 mm, także na wymiar"),
        ("z-staldrewno", "Stalowe drewnopodobne", "Stal z trwałą okleiną drewnopodobną — parapet w kolorze okien w okleinie.", "Profil Standard lub Soft"),
    ],
}
PARAPETY_ADV = [("Na wymiar", "Szerokość, długość, narożniki i wykończenie krawędzi dopasowane do okna", "ruler"),
                ("Spójne kolory", "Kamień, dekory drewnopodobne i kolory RAL zgrane ze stolarką", "palette"),
                ("Sprawdzony producent", "Parapety Jaro-Max — kamień, MDF, PCV, stal i aluminium", "shield")]
PARAPETY_FAQ = [
    ("Jaki parapet wewnętrzny wybrać?",
     "Jeśli zależy Ci na trwałości i odporności na wilgoć, np. w kuchni czy łazience, najlepiej sprawdzą się parapety kamienne — granitowe albo z konglomeratu kwarcytowego lub marmurowego. Parapety MDF i PCV to cieplejszy w odbiorze, lżejszy i bardziej ekonomiczny wybór z szeroką gamą kolorów gładkich i drewnopodobnych."),
    ("Czym różni się granit od konglomeratu?",
     "Granit to kamień w pełni naturalny — każdy parapet ma niepowtarzalny rysunek, a żyłki czy drobne przebarwienia są jego naturalną cechą. Konglomerat powstaje z kruszywa kamiennego połączonego żywicą, dzięki czemu ma bardziej jednolity, powtarzalny kolor."),
    ("Jaki parapet zewnętrzny wybrać?",
     "Najczęściej wybierane są parapety stalowe i aluminiowe — lekkie, trwałe i dostępne w wielu kolorach, także drewnopodobnych i z palety RAL. Do elewacji z cegły lub klinkieru dobrze pasuje Alu-Płytka, do nowoczesnych projektów JM External Contour, a granit tam, gdzie liczy się klasyczny, kamienny wygląd."),
    ("Czy parapety są wykonywane na wymiar?",
     "Tak. Parapety przygotowujemy na wymiar otworu okiennego — dobieramy szerokość, długość, rodzaj narożników i wykończenie krawędzi, a do parapetów zewnętrznych pasujące zaślepki i łączniki."),
    ("Czy warto zamówić parapety razem z oknami?",
     "Tak — wtedy łatwiej zgrać kolor parapetów ze stolarką i elewacją oraz dopasować ich wymiary do okien. Wszystko ustalisz w jednym miejscu, u jednego doradcy."),
]


def build_parapety():
    def grupa(key, title, lead):
        typy = PARAPETY_TYPY[key]
        cards = "".join(f"""<article class="sill-card">
        <img src="assets/img/parapety/{k}.jpg" alt="{title} — {n.lower()}" loading="lazy">
        <div><h3>{n}</h3><p>{d}</p><small>{t}</small></div>
      </article>""" for k, n, d, t in typy)
        tabs = '<div class="chips chips--tabs" role="tablist">' + "".join(
            f'<button type="button" class="{"is-active" if i == 0 else ""}" data-filter-btn="{k}">{n}</button>'
            for i, (k, n, _d, _t) in enumerate(typy)) + "</div>"
        grid = '<div class="sill-swatches" data-filter-grid>' + "".join(
            f'<figure data-filter="{k}"{"" if i == 0 else " hidden"}><img src="assets/img/parapety/kolor-{f}.jpg" alt="{n}" loading="lazy"><figcaption>{n}</figcaption></figure>'
            for i, (k, _n, _d, _t) in enumerate(typy) for n, f in PARAPETY_KOLORY[k]) + "</div>"
        return f"""<div class="section-header"><div class="section-header__left"><h2 class="h-sec">{title}</h2></div></div>
    <p class="sill-lead">{lead}</p>
    <div class="sill-types{" sill-types--3" if len(typy) % 3 == 0 else ""}">{cards}</div>
    <h4 class="palette-title">Dostępne kolory</h4>
    <div>{tabs}{grid}</div>"""

    adv = "".join(f"""<div class="adv"><span class="adv__icon">{I[ic]}</span>
      <div><h3>{t}</h3><p>{d}</p></div></div>""" for t, d, ic in PARAPETY_ADV)
    faq = "".join(f"""<div class="faq__row">
      <button class="faq__q"><span>{q}</span><span>+</span></button>
      <div class="faq__a"><p>{a}</p></div>
    </div>""" for q, a in PARAPETY_FAQ)
    rel = ""
    for sl in ["okna", "rolety-zewnetrzne", "moskitiery"]:
        rel += f"""<a href="{sl}.html"><article class="card">
        <img src="assets/img/{PROD_IMG[sl]}.jpg" alt="{PROD_LABEL[sl]}" style="height:150px;object-fit:cover;border-radius:var(--r-md)">
        <div><h3>{PROD_LABEL[sl]}</h3></div>
        <span class="card__more">Zobacz ofertę {I['arrow']}</span>
      </article></a>"""

    body = pagehero("parapety/hero", "Parapety Jaro-Max – praktyczne i piękne wykończenie okna",
                    "Parapety wewnętrzne i zewnętrzne z kamienia, konglomeratu, MDF, PCV, stali i aluminium — dopasujesz je do stolarki okiennej, elewacji i charakteru wnętrza.", None)
    body += f"""<section class="section">
  <div class="container">
    {grupa("wewnetrzne", "Parapety wewnętrzne", "Parapety wewnętrzne wykańczają ścianę pod oknem i są ważnym elementem aranżacji. Do wyboru kamień naturalny, konglomeraty oraz ciepłe w odbiorze MDF i PCV.")}
  </div>
</section>
<section class="section section--soft">
  <div class="container">
    {grupa("zewnetrzne", "Parapety zewnętrzne", "Parapet zewnętrzny odprowadza wodę z dala od elewacji i chroni ją przed zawilgoceniem, dlatego musi być trwały i odporny na warunki atmosferyczne.")}
    <p class="colors-note">Parapety aluminiowe, stalowe i External Contour mogą być też lakierowane proszkowo na dowolny kolor z palety RAL — w macie, satynie lub strukturze.</p>
  </div>
</section>
<section class="advantages"><div class="container advantages__inner">{adv}</div></section>

<section class="section">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Warto wiedzieć przed zakupem</h2></div></div>
    <div class="faq">{faq}</div>
  </div>
</section>

{cta("Doradztwo i wycena", "Dobierzemy parapety do Twoich okien",
     "Skontaktuj się z nami — doradzimy technicznie i przygotujemy kalkulację cenową.")}

<section class="section related">
  <div class="container">
    <h2 class="h-sec" style="margin-bottom:32px">Sprawdź również inne systemy</h2>
    <div class="grid-3">{rel}</div>
  </div>
</section>
"""
    write("parapety.html", head("Parapety wewnętrzne i zewnętrzne Jaro-Max | PROMYK Wieluń",
                                "Parapety Jaro-Max: granitowe, kwarcytowe, marmurowe, MDF, PCV, stalowe, aluminiowe, Alu-Płytka i External Contour. Kolory i wymiary na zamówienie — PROMYK Wieluń.")
          + nav("parapety") + body + footer())


if __name__ == "__main__":
    print("Generuję strony PROMYK...")
    build_index()
    build_onas()
    build_oferta()
    build_konfigurator()
    build_inwestor()
    build_galeria()
    build_kontakt()
    for slug, meta in PRODUCT_DATA.items():
        if slug == "okna":
            build_okna()          # własny układ wg uwag klienta
        elif slug == "drzwi-zewnetrzne":
            build_drzwi_zewnetrzne()
        elif slug == "drzwi-wewnetrzne":
            build_drzwi_wewnetrzne()
        elif slug == "rolety-zewnetrzne":
            build_rolety_zewnetrzne()
        else:
            product_page(slug, meta)
    build_parapety()
    build_subpages()
    print("Gotowe.")
