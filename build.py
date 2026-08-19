# -*- coding: utf-8 -*-
"""
Generator statycznej strony PROMYK (Wieluń) — odwzorowanie projektu Figma.
Uruchomienie:  python build.py
Wynik: pliki .html w katalogu projektu (assets/ pozostają bez zmian).
"""
import os, io, html

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSET_VER = "16"  # podbij przy zmianach css/js (cache-busting)

PHONE = "607 941 499"
PHONE_TEL = "+48607941499"
MAIL = "info@promyk.wielun.pl"
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
    ("okna",              "Okna",               "Premium PVC / Alu",  "al39"),
    ("drzwi-zewnetrzne",  "Drzwi zewnętrzne",   "Wikęd",              "wiked30"),
    ("drzwi-wewnetrzne",  "Drzwi wewnętrzne",   "DRE",                "dre_binito50"),
    ("rolety-zewnetrzne", "Rolety zewnętrzne",  "Shading",            "al30_rol"),
    ("pergole",           "Pergole",            "Bioklimatyczne",     "pergola1"),
    ("bramy-garazowe",    "Bramy garażowe",     "Nice / Somfy",       "brama_antracyt"),
    ("markizy",           "Markizy",            "Selt",               "al25"),
    ("oslony-wewnetrzne", "Osłony wewnętrzne",  "Żaluzje i rolety",   "plisy"),
    ("oslony-zewnetrzne", "Osłony zewnętrzne",  "Refleksole",         "al27"),
    ("moskitiery",        "Moskitiery",         "Na wymiar",          "moskitiera_mrs"),
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
    ("setto", "Setto", "https://setto.pl"),
    ("wiked", "Wikęd", "https://wiked.pl"),
    ("dre", "DRE", "https://dre.pl"),
]

GALLERY = [
    ("wiked62", "Drzwi zewnętrzne Wikęd — dąb naturalny", "drzwi"),
    ("al31_rol", "Przeszklenia HST z roletami podtynkowymi", "okna"),
    ("brama_antracyt", "Brama segmentowa antracyt + oświetlenie", "bramy"),
    ("pergola1", "Pergola bioklimatyczna z oświetleniem LED", "pergole"),
    ("wiked51", "Drzwi wejściowe w okleinie drewnopodobnej", "drzwi"),
    ("al39", "Narożne przeszklenie aluminiowe", "okna"),
    ("al30_rol", "Rolety nadstawne w elewacji drewnianej", "rolety"),
    ("plisy", "Plisy okienne — salon", "oslony"),
    ("wiked92", "Drzwi zewnętrzne z naświetlem bocznym", "drzwi"),
    ("al25", "Drzwi podnoszono-przesuwne HST na taras", "okna"),
    ("brama_avo_dom", "Brama garażowa w okleinie drewnopodobnej", "bramy"),
    ("al27", "Refleksol zewnętrzny — ochrona przed słońcem", "oslony"),
    ("wiked22", "Realizacja: dom jednorodzinny pod Wieluniem", "drzwi"),
    ("al38", "Okno kuchenne PVC z ciepłym montażem", "okna"),
    ("brama_4", "Brama roletowa — garaż o niskim nadprożu", "bramy"),
    ("al35_rol", "Sterowanie osłonami — system Somfy", "rolety"),
    ("wiked46", "Drzwi w kolorze szałwiowym", "drzwi"),
    ("moskitiera_mrs", "Moskitiery ramkowe na wymiar", "oslony"),
    ("wiked67", "Spójna kolorystyka bramy i drzwi", "bramy"),
    ("dre_binito50", "Drzwi wewnętrzne DRE — Binito 50", "drzwi"),
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
<link href="https://fonts.googleapis.com/css2?family=Urbanist:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400&display=swap&subset=latin-ext" rel="stylesheet">
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
      <a class="btn btn--primary btn--sm" href="kontakt.html">Umów pomiar {I['arrow']}</a>
      <button class="nav__burger" aria-label="Menu">{I['menu']}</button>
    </div>
  </div>
</header>
"""

def cta(tag, h2, p):
    return f"""<section class="cta">
  <div class="container cta__inner">
    <span class="tag tag--onDark">{tag}</span>
    <h2>{h2}</h2>
    <p>{p}</p>
    <div class="cta__btns">
      <a class="btn btn--primary" href="kontakt.html">Umów bezpłatny pomiar {I['cal']}</a>
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
        <a class="fb" href="https://www.facebook.com/" target="_blank" rel="noopener">{I['fb']} Obserwuj nas na Facebooku</a>
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
    return f"""<section class="pagehero">
  <img src="assets/img/{img}.jpg" alt="">
  <div class="container pagehero__body">
    <div class="crumbs"><a href="index.html">Strona główna</a> &nbsp;/&nbsp; {crumb}</div>
    <h1>{h1}</h1>
    <p>{p}</p>
  </div>
</section>
"""

def stats(three=False):
    s3 = """
      <div class="stats__div"></div>
      <div class="stat">
        <div class="stat__num">200 km</div>
        <div><div class="stat__label">Zasięg działania</div><div class="stat__desc">Montujemy systemy w całym regionie łódzkim i sąsiednich</div></div>
      </div>""" if three else ""
    return f"""<section class="stats">
  <div class="container stats__inner">
    <div class="stat">
      <div class="stat__num">150 000+</div>
      <div><div class="stat__label">zrealizowanych montaży</div><div class="stat__desc">Okna, rolety i bramy w domach naszych klientów</div></div>
    </div>
    <div class="stats__div"></div>
    <div class="stat">
      <div class="stat__num">30 lat</div>
      <div><div class="stat__label">doświadczenia na rynku</div><div class="stat__desc">Nieprzerwanie dbamy o komfort termiczny od 1997 roku</div></div>
    </div>{s3}
  </div>
</section>
"""

def partners():
    row = "".join(
        f'<a href="{url}" target="_blank" rel="noopener" aria-label="{name}">'
        f'<img src="assets/img/partners/{slug}.svg" alt="{name}" loading="lazy"></a>'
        for slug, name, url in PARTNERS)
    return f"""<section class="partners">
  <div class="container">
    <span class="tag">Zaufani producenci</span>
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
        <span class="tag">Opinie naszych klientów</span>
        <h2 class="h-sec">Zaufanie budowane przez dekady</h2>
      </div>
      <div class="rating">
        <span class="rating__num">4.9</span>
        <span><span class="stars">{I['star'] * 5}</span><br><small class="lead">średnia ocena Google</small></span>
      </div>
    </div>
    <div class="grid-3">{cards}</div>
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
        ("wiked07", ), ("al31_rol", ), ("pergola1", ),
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

    systems = [
        ("VEKA SOFTLINE 82 MD", "Niezawodne PVC klasy A",
         [("Współczynnik Uw", "od 0,67 W/m²K"), ("Liczba komór", "7 komór profilu"),
          ("System uszczelek", "3 (MD – środkowa)"), ("Klasa profilu", "Klasa A (najwyższa)")]),
        ("VEKA SOFTLINE 70 AD", "Klasyczny design &amp; trwałość",
         [("Współczynnik Uw", "od 0,88 W/m²K"), ("Liczba komór", "5 komór profilu"),
          ("System uszczelek", "2 (AD – odbojowe)"), ("Klasa profilu", "Klasa A")]),
        ("VEKAMOTION 82", "Drzwi przesuwne HST",
         [("Współczynnik Uw", "od 0,83 W/m²K"), ("Próg bezbarierowy", "Tak (0 mm)"),
          ("Głębokość zabudowy", "194 mm skrzydło"), ("Maks. gabaryty", "do 6,5 m szerokości")]),
        ("Aluprof MB-86N", "Zaawansowane aluminium",
         [("Współczynnik Uw", "od 0,72 W/m²K"), ("Izolacja termiczna", "Przekładki Aero"),
          ("Konstrukcja", "Aluminiowa ciepła"), ("Estetyka", "Ukryte skrzydło (opcja)")]),
    ]
    syscards = ""
    for name, sub, params in systems:
        rows = "".join(f'<div class="param"><span>{a}</span><span>{b}</span></div>' for a, b in params)
        syscards += f"""<article class="card">
        <div><h3>{name}</h3><div class="card__sub">{sub}</div></div>
        <div class="params">{rows}</div>
        <a class="card__more" href="okna.html">Więcej szczegółów {I['arrow']}</a>
      </article>"""

    gal = "".join(
        f'<a href="galeria.html"><img src="assets/img/{g[0]}.jpg" alt="{g[1]}"><figcaption>{g[1]}</figcaption></a>'
        for g in GALLERY[:4])

    body = f"""<section class="hero">
  <div class="hero__slides">{sl}</div>
  <div class="container hero__body">
    <div></div>
    <div class="hero__center">
      <button class="hero__arrow" data-hero="prev" aria-label="Poprzedni">{I['chevL']}</button>
      <div class="hero__text">
        <span class="tag tag--solid">Rodzinna firma od 1997 roku</span>
        <h1>Okna, drzwi i osłony na całe lata</h1>
        <p>Premium standard montażu w Wieluniu i okolicach. Wybierz jakość popartą 30-letnim doświadczeniem w branży stolarki otworowej.</p>
        <div class="hero__ctas">
          <a class="btn btn--primary" href="kontakt.html">Umów bezpłatny pomiar {I['arrow']}</a>
          <a class="btn btn--ghost" href="galeria.html">Zobacz realizacje</a>
        </div>
      </div>
      <button class="hero__arrow hero__arrow--next" data-hero="next" aria-label="Następny">{I['chevR']}</button>
    </div>
    <div class="hero__dots">{dots}</div>
  </div>
</section>

{stats()}

<section class="section section--soft">
  <div class="container">
    <div class="section-header">
      <div class="section-header__left">
        <span class="tag">Kompleksowa oferta</span>
        <h2 class="h-sec">Wybierz systemy dopasowane do Twojego projektu</h2>
      </div>
      <p class="section-header__right lead">Oferujemy najwyższej klasy okna, bezpieczne drzwi wejściowe, bramy garażowe oraz innowacyjne systemy zaciemnienia wnętrz.</p>
    </div>
    <div class="tiles">{tiles}</div>
  </div>
</section>

<section class="section">
  <div class="container split">
    <div class="split__media"><img src="assets/img/al38.jpg" alt="Konfigurator kolorów okien"></div>
    <div class="split__text">
      <span class="tag">Narzędzie online</span>
      <h2 class="h-sec">Konfigurator kolorów okien</h2>
      <p class="lead">Dobierz idealny kolor profili okiennych, dopasuj estetyczne klamki i klasyczne lub nowoczesne szprosy. Zobacz realistyczny efekt na żywo przed podjęciem ostatecznej decyzji.</p>
      <ul class="bullets">
        <li><span class="check">{I['check']}</span> Paleta ponad 50 kolorów drewnopodobnych i RAL</li>
        <li><span class="check">{I['check']}</span> Szybki podgląd na różnych typach elewacji</li>
        <li><span class="check">{I['check']}</span> Opcja bezpośredniego przesłania konfiguracji do wyceny</li>
      </ul>
      <a class="btn btn--primary" href="konfigurator.html">Otwórz konfigurator {I['win']}</a>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="container">
    <div class="section-header">
      <div class="section-header__left">
        <span class="tag">Rekomendowane profile</span>
        <h2 class="h-sec">Systemy okienne o najwyższych parametrach</h2>
      </div>
      <p class="section-header__right lead">Wyselekcjonowane, certyfikowane profile VEKA oraz Aluprof gwarantujące doskonałą izolację termiczną, akustyczną oraz odporność na włamania.</p>
    </div>
    <div class="grid-4">{syscards}</div>
  </div>
</section>

<section class="section">
  <div class="container split">
    <div class="split__text">
      <span class="tag">O firmie Promyk</span>
      <h2 class="h-sec">Od montażu rolet do lidera stolarki premium w Wieluniu</h2>
      <p class="lead">Jesteśmy rodzinnym przedsiębiorstwem działającym od 1997 roku. Nasze korzenie to montaż prostych osłon okiennych – dziś dostarczamy i instalujemy kompleksowe systemy okienne, drzwiowe oraz zaawansowane pergole bioklimatyczne.</p>
      <p class="lead">Działamy w promieniu 200 km od Wielunia. Gwarantujemy fachowe doradztwo techniczne i precyzyjny montaż z użyciem profesjonalnego sprzętu.</p>
      <div class="feature-row">
        <div class="feature"><h4>Wieluń i okolice</h4><p>Szybki dojazd, lokalny serwis gwarancyjny i pogwarancyjny.</p></div>
        <div class="feature"><h4>Ciepły montaż</h4><p>Instalacja zgodnie z rygorystycznymi wytycznymi producentów.</p></div>
      </div>
      <a class="btn btn--primary" href="o-nas.html">Poznaj nas bliżej {I['arrow']}</a>
    </div>
    <div class="split__media"><img class="about__img" src="assets/img/wiked22.jpg" alt="Realizacja Promyk"></div>
  </div>
</section>

{partners()}
{reviews()}

<section class="section section--soft">
  <div class="container">
    <div class="section-header">
      <div class="section-header__left">
        <span class="tag">Ostatnie realizacje</span>
        <h2 class="h-sec">Nasze realizacje mówią same za siebie</h2>
      </div>
      <a class="btn btn--primary" href="galeria.html">Zobacz więcej realizacji {I['arrow']}</a>
    </div>
    <div class="gallery gallery--home">{gal}</div>
  </div>
</section>

{cta("Darmowy pomiar i doradztwo", "Planujesz budowę lub wymianę okien?",
     "Umów bezpłatny pomiar na Twojej budowie. Przyjedziemy, doradzimy, dobierzemy odpowiednie rozwiązania i przygotujemy niezobowiązującą wycenę.")}
"""
    write("index.html",
          head("PROMYK Wieluń — okna, drzwi, bramy garażowe i osłony | Montaż od 1997 r.",
               "Rodzinna firma z Wielunia od 1997 r. Okna VEKA i Aluprof, drzwi Wikęd i DRE, bramy garażowe, rolety, pergole i moskitiery. Bezpłatny pomiar i ciepły montaż.")
          + nav("index") + body + footer())

# ================================================================ O NAS ----
def build_onas():
    why = [
        ("30 lat doświadczenia", "Znamy branżę od podszewki i montujemy wyłącznie sprawdzone systemy klas premium.", "shield"),
        ("Kompleksowość", "Przeprowadzimy Cię przez cały proces: od profesjonalnego pomiaru aż po precyzyjny montaż.", "cog"),
        ("Gwarancja", "Udzielamy pełnego bezpieczeństwa na zakupione u nas produkty oraz nasze usługi instalacyjne.", "lock"),
        ("Lokalność", "Jesteśmy rodzinną firmą z Wielunia. Znamy potrzeby i budownictwo naszych sąsiadów.", "leaf"),
    ]
    cards = "".join(f"""<article class="card">
      <span class="adv__icon">{I[ic]}</span>
      <div><h3>{t}</h3><p class="lead" style="margin:8px 0 0">{d}</p></div>
    </article>""" for t, d, ic in why)

    body = pagehero("wiked22", "Rodzinna firma, która buduje komfort od 1997 roku",
                    "Poznaj historię PROMYK — od pierwszego montażu żaluzji po nowoczesny showroom w Wieluniu.", "O nas")
    body += stats(three=True)

    body += f"""<section class="section">
  <div class="container split">
    <div class="split__text">
      <span class="tag">Nasza Historia</span>
      <h2 class="h-sec">Od rodzinnego rzemiosła do pozycji eksperta</h2>
      <div class="prose">
        <p><strong>PROMYK to rodzinna firma, która powstała w 1997 roku.</strong> Od ponad dwóch dekad rozwijamy się dzięki pasji, zaangażowaniu i ciężkiej pracy, dostarczając naszym klientom rozwiązania, które łączą funkcjonalność, estetykę i najwyższą jakość.</p>
        <p>Nasza historia rozpoczęła się od montażu żaluzji. To właśnie od tej usługi właściciel firmy zaczął budować doświadczenie oraz zaufanie klientów. Z czasem dołączyła do niego żona i wspólnie stworzyli dwuosobową firmę, rozpoczynając produkcję osłon okiennych w niewielkim pomieszczeniu.</p>
        <p>Kolejne lata przyniosły dynamiczny rozwój. Firma przeniosła się do siedziby przy domu, gdzie rozszerzyliśmy działalność o produkcję rolet zewnętrznych. Rosnące grono zadowolonych klientów oraz coraz szersza oferta sprawiły, że powstał samodzielny budynek, w którym oprócz osłon okiennych zaczęliśmy oferować również okna, drzwi, bramy garażowe oraz nowoczesne zewnętrzne systemy przeciwsłoneczne.</p>
      </div>
    </div>
    <div class="split__media"><img class="about__img" src="assets/img/wiked37.jpg" alt="Realizacja PROMYK"></div>
  </div>
</section>

<section class="section section--soft">
  <div class="container split">
    <div class="split__media"><img class="about__img" src="assets/img/wiked57.jpg" alt="Showroom PROMYK"></div>
    <div class="split__text">
      <span class="tag">Pokolenia i showroom</span>
      <h2 class="h-sec">Rodzinny charakter to nasza największa siła</h2>
      <div class="prose">
        <p>Rodzinny charakter naszej firmy pozostaje jej największą siłą. Do zespołu dołączył najpierw syn, a następnie córka, dzięki czemu kolejne pokolenie aktywnie uczestniczy w dalszym rozwoju przedsiębiorstwa. Łączymy wieloletnie doświadczenie z nowoczesnym podejściem, stale poszerzając ofertę i podnosząc jakość naszych usług.</p>
        <p>Dziś z dumą zapraszamy do naszego <strong>nowego showroomu</strong> – miejsca, w którym można zobaczyć najnowsze produkty, porównać dostępne rozwiązania i skorzystać z fachowego doradztwa. To kolejny etap w historii firmy PROMYK i dowód na to, że nieustannie inwestujemy w rozwój oraz komfort naszych klientów.</p>
        <p>Od pierwszego montażu żaluzji w 1997 roku po nowoczesny salon ekspozycyjny – niezmiennie kierujemy się tymi samymi wartościami: <strong>uczciwością, rzetelnością, jakością i indywidualnym podejściem</strong> do każdego klienta. To właśnie zaufanie naszych klientów pozwala nam rozwijać się już od blisko 30 lat.</p>
      </div>
      <a class="btn btn--primary" href="kontakt.html">Odwiedź nasz showroom {I['arrow']}</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header">
      <div class="section-header__left">
        <span class="tag">Zalety współpracy</span>
        <h2 class="h-sec">Dlaczego klienci wybierają Promyk?</h2>
      </div>
    </div>
    <div class="grid-4">{cards}</div>
  </div>
</section>

{partners()}
{reviews()}
{cta("Dołącz do grona zadowolonych klientów", "Chcesz dołączyć do grona zadowolonych klientów?",
     "Umów bezpłatny pomiar i przekonaj się, jak wygląda współpraca z rodzinną firmą z niemal 30-letnim doświadczeniem.")}
"""
    write("o-nas.html",
          head("O nas — rodzinna firma PROMYK od 1997 roku | Wieluń",
               "PROMYK to rodzinna firma z Wielunia działająca od 1997 roku. Od montażu żaluzji po kompleksową stolarkę otworową i nowoczesny showroom.")
          + nav("o-nas") + body + footer())

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
        ("Katalog VEKA", "Systemy profili PVC Klasy A", "PDF • 14.2 MB"),
        ("Katalog Aluprof", "Nowoczesne systemy aluminiowe", "PDF • 18.5 MB"),
        ("Katalog Wikęd", "Premium drzwi zewnętrzne", "PDF • 9.8 MB"),
        ("Katalog DRE", "Drzwi wewnętrzne i ościeżnice", "PDF • 12.1 MB"),
        ("Katalog Selt", "Pergole, markizy i żaluzje fasadowe", "PDF • 8.4 MB"),
        ("Cennik orientacyjny", "Ceny typowych rozwiązań", "PDF • 2.5 MB"),
    ]
    cat = "".join(f"""<a class="catalog" href="kontakt.html">
      <span class="catalog__icon">{I['pdf']}</span>
      <span class="catalog__info"><strong>{t}</strong><span>{s}</span></span>
      <span class="catalog__meta">{m}</span>
    </a>""" for t, s, m in catalogs)

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
        <span class="tag">Materiały informacyjne</span>
        <h2 class="h-sec">Katalogi do pobrania</h2>
        <p class="lead">Pobierz oficjalne katalogi naszych partnerów oraz orientacyjne cenniki, aby zapoznać się ze szczegółowymi specyfikacjami technicznymi.</p>
      </div>
    </div>
    <div class="stack">{cat}</div>
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
         ["Kompleksowa opieka i doradztwo", "Darmowy pomiar i precyzyjne dopasowanie", "Lokalny serwis pogwarancyjny w Wieluniu"]),
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
        ("Czy pomiar i doradztwo techniczne na budowie są bezpłatne?",
         "Tak. Podczas bezpłatnego spotkania w naszej siedzibie wspólnie przeanalizujemy projekt domu, doradzimy najlepsze rozwiązania techniczne i estetyczne oraz przygotujemy wstępną, niezobowiązującą wycenę. Po podjęciu decyzji wykonujemy dokładny pomiar na budowie — również bez dodatkowych opłat."),
        ("Jak długo trwa realizacja zamówienia od pomiaru?",
         "Standardowy termin realizacji to zwykle 4–8 tygodni od zatwierdzenia zamówienia i wykonania pomiaru. Termin zależy od producenta i stopnia personalizacji stolarki — dokładną datę potwierdzamy w umowie i dopasowujemy do harmonogramu budowy."),
        ("Czy wykonujecie montaż w innych miastach niż Wieluń?",
         "Tak. Działamy w promieniu ok. 200 km od Wielunia — obsługujemy cały region łódzki oraz województwa sąsiednie. Dojazd na pomiar w tym obszarze jest bezpłatny."),
        ("Jakiej gwarancji udzielacie na produkty i montaż?",
         "Na produkty obowiązuje gwarancja producenta (najczęściej 5–10 lat w zależności od systemu), a na wykonany przez nas montaż udzielamy własnej gwarancji. Zapewniamy też lokalny serwis gwarancyjny i pogwarancyjny."),
    ]
    fq = ""
    for k, (q, a) in enumerate(faq):
        cls = " is-open" if k == 0 else ""
        sign = "–" if k == 0 else "+"
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
               "Planujesz budowę domu? Okna, drzwi, bramy garażowe, rolety i parapety zamówisz w jednym miejscu. Bezpłatna konsultacja, pomiar i profesjonalny montaż.")
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
        <button class="btn btn--primary" style="width:100%;justify-content:center;margin-top:24px" type="submit">Wyślij bezpłatne zapytanie {I['arrow']}</button>
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
               f"Skontaktuj się z PROMYK: {ADDR1}, {ADDR2}, tel. {PHONE}. Bezpłatna wycena i pomiar stolarki otworowej.")
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
def product_page(slug, meta):
    adv = "".join(f"""<div class="adv"><span class="adv__icon">{I[ic]}</span>
      <div><h3>{t}</h3><p>{d}</p></div></div>""" for t, d, ic in meta["adv"])

    rows = ""
    for k, r in enumerate(meta["rows"]):
        title, intro, bullets, img = r
        li = "".join(f'<li><span class="check">{I["check"]}</span> {b}</li>' for b in bullets)
        intro_html = f'<p>{intro}</p>' if intro else ""
        media = f'<div><img src="assets/img/{img}.jpg" alt="{title}" loading="lazy"></div>'
        text = f"""<div class="subrow__text">
        <h2>{title}</h2>
        {intro_html}
        <ul class="bullets">{li}</ul>
        <a class="btn btn--primary btn--sm" href="kontakt.html">Zapytaj o darmową wycenę {I['arrow']}</a>
      </div>"""
        rows += f'<div class="subrow{" subrow--flip" if k % 2 else ""}">{media if k % 2 == 0 else text}{text if k % 2 == 0 else media}</div>'

    rel = ""
    for s in meta["related"]:
        rel += f"""<a href="{s}.html"><article class="card">
        <img src="assets/img/{PROD_IMG[s]}.jpg" alt="{PROD_LABEL[s]}" style="height:150px;object-fit:cover;border-radius:var(--r-md)">
        <div><h3>{PROD_LABEL[s]}</h3></div>
        <span class="card__more">Zobacz ofertę {I['arrow']}</span>
      </article></a>"""

    body = pagehero(meta["hero"], meta["h1"], meta["intro"], PROD_LABEL[slug])
    body += f"""<section class="advantages"><div class="container advantages__inner">{adv}</div></section>

<section class="section"><div class="container">{rows}</div></section>

{cta("Darmowy pomiar i doradztwo", "Planujesz inwestycję budowlaną?",
     "Umów bezpłatną wizytę naszego eksperta na Twojej budowie. Precyzyjnie zmierzymy otwory, doradzimy technicznie i przygotujemy kalkulację cenową.")}

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
  hero="al39", h1="Okna PVC i aluminiowe", title="Okna PVC i aluminiowe VEKA, Aluprof | PROMYK Wieluń",
  desc="Okna PVC VEKA Softline 82 MD i 70 AD, systemy HST VEKAMOTION oraz okna aluminiowe Aluprof MB-86N. Ciepły montaż w Wieluniu i okolicach.",
  intro="Certyfikowane profile VEKA i Aluprof o najwyższych parametrach izolacyjnych — z ciepłym montażem i gwarancją.",
  adv=[("Energooszczędność", "Współczynnik Uw od 0,67 W/m²K chroniący Twój budżet", "thermo"),
       ("Maksymalna Trwałość", "Profile wyłącznie najwyższej klasy A o grubych ściankach", "shield"),
       ("Nielimitowana Estetyka", "Szeroka paleta kolorów, oklein drewnopodobnych i matowych", "palette")],
  rows=[("VEKA SOFTLINE 82 MD", None,
         ["Zaawansowany 7-komorowy profil PVC klasy A o szerokości 82 mm",
          "Znakomita izolacja termiczna: Uw od 0,67 W/m²K",
          "Trójkomorowy system uszczelek z uszczelką środkową (MD)",
          "Dedykowany do domów pasywnych i wysoce energooszczędnych"], "al38"),
        ("VEKA SOFTLINE 70 AD", None,
         ["Klasyczny i sprawdzony 5-komorowy system o głębokości 70 mm",
          "Współczynnik przenikania ciepła Uw od 0,88 W/m²K",
          "Podwójny system uszczelek odbojowych najwyższej jakości",
          "Ekonomiczny wybór gwarantujący najwyższe standardy wykonania klasy A"], "abm_okno2"),
        ("VEKAMOTION 82 HST", None,
         ["Innowacyjny system podnoszono-przesuwny do spektakularnych przeszkleń",
          "Superniski próg bezbarierowy (0 mm) ułatwiający przechodzenie",
          "Bardzo niski profil skrzydła maksymalizujący ilość światła dziennego",
          "Szerokość konstrukcji nawet do 6,5 metra dla pełnej harmonii z tarasem"], "al25"),
        ("Aluprof MB-86N", None,
         ["Zaawansowany system aluminiowy o wybitnych właściwościach termicznych",
          "Uw od 0,72 W/m²K dzięki innowacyjnym przekładkom Aero",
          "Ekstremalna sztywność pozwalająca na tworzenie wielkich, nowoczesnych ram",
          "Nowoczesny, płaski i geometryczny design pożądany przez architektów"], "al39")],
  related=["rolety-zewnetrzne", "moskitiery", "oslony-wewnetrzne"]),

"drzwi-zewnetrzne": dict(
  hero="wiked22", h1="Drzwi zewnętrzne Wikęd i Aluprof", title="Drzwi zewnętrzne Wikęd, aluminiowe i HPL | PROMYK Wieluń",
  desc="Drzwi zewnętrzne stalowe Wikęd, aluminiowe Aluprof, panele HPL i modele do domów pasywnych. Klasa RC2/RC3, Ud od 0,71 W/m²K.",
  intro="Ponad 100 modeli drzwi wejściowych z zabezpieczeniami antywłamaniowymi i doskonałą termoizolacją.",
  adv=[("Klasa Bezpieczeństwa", "Zabezpieczenia antywłamaniowe w standardzie RC2 i RC3", "lock"),
       ("Termoizolacja", "Wybitny współczynnik Ud od 0,71 W/m²K chroniący przed zimnem", "thermo"),
       ("Bogate Wzornictwo", "Ponad 100 unikalnych modeli z naświetlami i przeszkleniami", "sparkle")],
  rows=[("Drzwi stalowe Wikęd", None,
         ["Niezwykle solidna i stabilna konstrukcja z blachy ocynkowanej",
          "Odporność na odkształcenia i najtrudniejsze warunki atmosferyczne",
          "Szeroki wybór przetłoczeń, od klasycznych po ultra-nowoczesne",
          "Najlepszy stosunek wysokiej jakości zabezpieczeń do przystępnej ceny"], "wiked51"),
        ("Drzwi aluminiowe Aluprof", None,
         ["Luksusowa linia oparta na ciepłych profilach aluminiowych",
          "Skrzydła zlicowane z ościeżnicą tworzące jednolitą, elegancką płaszczyznę",
          "Możliwość zintegrowania czytnika linii papilarnych i systemów Smart Home",
          "Imponujące, wielkogabarytowe konstrukcje szyte na miarę"], "wiked35"),
        ("Drzwi z panelem HPL", None,
         ["Powłoki zewnętrzne z niezwykle trwałego tworzywa żywicznego HPL",
          "Absolutna odporność na promieniowanie UV, wilgoć i zarysowania",
          "Ekskluzywne wykończenia do złudzenia przypominające naturalne usłojenie drewna",
          "Dedykowane dla inwestorów oczekujących bezobsługowej wieloletniej trwałości"], "wiked92"),
        ("Drzwi do domów pasywnych", None,
         ["Grubość skrzydła do 90 mm z wypełnieniem pianką poliuretanową",
          "Niewiarygodny parametr izolacyjności termicznej: Ud od 0,71 W/m²K",
          "Ciepła ościeżnica z przegrodą termiczną eliminującą mostki termiczne",
          "Spełnia najwyższe normy dofinansowania w programie Czyste Powietrze"], "wiked26")],
  related=["drzwi-wewnetrzne", "okna", "moskitiery"]),

"drzwi-wewnetrzne": dict(
  hero="dre_saraeco2", h1="Drzwi wewnętrzne DRE", title="Drzwi wewnętrzne DRE — ramiakowe, bezprzylgowe, przesuwne | PROMYK",
  desc="Drzwi wewnętrzne DRE: ramiakowe, bezprzylgowe z ukrytymi zawiasami, przesuwne i techniczne. Pomiar i profesjonalny montaż w Wieluniu.",
  intro="Setki modeli renomowanego polskiego producenta DRE — z pomiarem i montażem wykonanym przez nasze ekipy.",
  adv=[("Lider Jakości", "Precyzyjne polskie wykonanie od renomowanego producenta DRE", "shield"),
       ("Niezliczony Wybór", "Setki modnych modeli, struktur i kolorów dopasowanych do wnętrz", "palette"),
       ("Kompleksowy Montaż", "Profesjonalny montaż i pomiar gwarantujący idealne działanie", "ruler")],
  rows=[("Drzwi ramiakowe", None,
         ["Niezwykle solidna i stabilna konstrukcja oparta na ramiakach z MDF",
          "Brak widocznych łączeń okleiny na krawędziach skrzydeł",
          "Wysoka odporność na uderzenia mechaniczne i codzienne użytkowanie",
          "Klasyczna elegancja z możliwością wstawienia szyb matowych"], "dre_nestor11"),
        ("Drzwi bezprzylgowe", None,
         ["Ukryte zawiasy dające efekt całkowitego zlicowania skrzydła z ościeżnicą",
          "Niezwykle minimalistyczny, nowoczesny i czysty wygląd we wnętrzu",
          "Magnetyczny zamek gwarantujący ciche i komfortowe zamykanie",
          "Idealne rozwiązanie do loftów i projektów o wysokim standardzie"], "dre_saraeco"),
        ("Drzwi przesuwne", None,
         ["Systemy naścienne z estetyczną maskownicą lub chowane bezpośrednio w ścianę",
          "Maksymalna oszczędność miejsca w małych i wąskich pokojach",
          "Wygodny mechanizm jezdny z systemem spowalniającym zamykanie (soft-close)",
          "Szerokie skrzydła idealnie dzielące przestrzeń np. salonu i jadalni"], "dre_seco1"),
        ("Drzwi techniczne i specjalne", None,
         ["Wzmocnione konstrukcje o podwyższonej odporności na wilgoć oraz akustykę",
          "Dedykowane do kotłowni, spiżarni, łazienek oraz biur domowych",
          "Skrzydła z wypełnieniem płytą wiórową otworową dla najwyższej stabilności",
          "Spełniają rygorystyczne przepisy budowlane dotyczące bezpieczeństwa"], "dre_binito10")],
  related=["drzwi-zewnetrzne", "okna", "oslony-wewnetrzne"]),

"rolety-zewnetrzne": dict(
  hero="al30_rol", h1="Rolety zewnętrzne", title="Rolety zewnętrzne nadstawne, podtynkowe i adaptacyjne | PROMYK Wieluń",
  desc="Rolety zewnętrzne aluminiowe: nadstawne, podtynkowe i adaptacyjne. Automatyka Somfy i Nice, sterowanie smartfonem. Montaż Wieluń.",
  intro="Aluminiowe rolety zewnętrzne z automatyką Somfy i Nice — termoizolacja, bezpieczeństwo i pełna kontrola światła.",
  adv=[("Termoizolacja", "Redukcja strat ciepła zimą oraz ochrona przed nagrzewaniem do 30%", "thermo"),
       ("Bezpieczeństwo", "Wzmocnione profile aluminiowe z blokadą rygla chroniące dom", "lock"),
       ("Automatyka", "Intuicyjne i niezawodne inteligentne sterowanie Somfy oraz Nice", "cog")],
  rows=[("Rolety nadstawne", None,
         ["Montaż zintegrowany bezpośrednio z oknem na etapie budowy lub wymiany",
          "Doskonałe parametry izolacji termicznej i akustycznej dzięki nowoczesnym materiałom",
          "Kompaktowa, estetyczna skrzynka niewidoczna od zewnątrz po ociepleniu",
          "Możliwość zintegrowania z moskitierą rolowaną w jednej obudowie"], "al30_rol"),
        ("Rolety podtynkowe", None,
         ["Idealne rozwiązanie do nowo wznoszonych budynków energooszczędnych i pasywnych",
          "Skrzynka montowana pod tynk, co zapewnia całkowitą integrację z elewacją",
          "Brak ingerencji w strukturę okna, eliminujący powstawanie mostków termicznych",
          "Wygodny i łatwy dostęp serwisowy od dołu skrzynki na zewnątrz budynku"], "al31_rol"),
        ("Rolety adaptacyjne", None,
         ["Zaprojektowane z myślą o już wybudowanych, gotowych domach i mieszkaniach",
          "Szybki i nieinwazyjny montaż bezpośrednio na elewacji lub we wnęce okiennej",
          "Wytrzymały pancerz z wysokogatunkowego aluminium wypełniony pianką PU",
          "Szeroki wachlarz kształtów skrzynek (okrągłe, półokrągłe, ścięte pod kątem 45°)"], "al41"),
        ("Sterowanie i Smart Home", None,
         ["Pełna automatyzacja procesów dzięki zaawansowanym napędom Somfy IO oraz Nice",
          "Zdalne zarządzanie za pomocą aplikacji na smartfona z dowolnego miejsca na ziemi",
          "Inteligentne czujniki wiatru, słońca i temperatury automatycznie dbające o klimat",
          "Możliwość tworzenia spersonalizowanych scenariuszy i harmonogramów dobowych"], "al35_rol")],
  related=["okna", "oslony-zewnetrzne", "moskitiery"]),

"pergole": dict(
  hero="pergola1", h1="Pergole bioklimatyczne i tarasowe", title="Pergole bioklimatyczne i tarasowe | PROMYK Wieluń",
  desc="Pergole bioklimatyczne z ruchomymi lamelami, pergole tarasowe i wolnostojące. Oświetlenie LED, promienniki, screeny ZIP. Montaż Wieluń.",
  intro="Aluminiowe pergole z regulacją lameli 0–135°, wodoszczelnym dachem i pełnym wyposażeniem dodatkowym.",
  adv=[("Pełna Regulacja", "Ruchome lamele aluminiowe pozwalają płynnie kontrolować słońce i deszcz", "sun"),
       ("Ekstremalna Trwałość", "Konstrukcja w 100% z ekstrudowanego aluminium odporna na silny wiatr i śnieg", "shield"),
       ("Nowoczesny Design", "Minimalistyczna bryła idealnie komponująca się z architekturą premium", "sparkle")],
  rows=[("Pergole bioklimatyczne", None,
         ["Sterowane elektrycznie lamele obracające się w zakresie od 0° do 135°",
          "Skuteczna naturalna wentylacja i precyzyjne dozowanie światła słonecznego",
          "W 100% wodoszczelny dach po całkowitym zamknięciu lameli",
          "Niewidoczny, zintegrowany w słupach system odprowadzania wody opadowej"], "pergola1"),
        ("Pergole tarasowe", None,
         ["Trwała konstrukcja z dachem tkaninowym (tkanina Tech-protect wysokiej gramatury)",
          "Możliwość całkowitego zsunięcia zadaszenia dla odsłonięcia nieba",
          "Wysoka odporność na promieniowanie UV oraz silne nagrzewanie",
          "Doskonała baza pod doposażenie w systemy bocznych rolet ZIP i przeszklenia"], "al25"),
        ("Pergole wolnostojące", None,
         ["Niezależna i stabilna konstrukcja przeznaczona do ogrodów lub przy basenie",
          "Duże możliwości gabarytowe pozwalające na zadaszenie przestrzeni lounge",
          "Szeroki wybór kolorów konstrukcji z palety strukturalnej RAL",
          "Opcja modułowego łączenia kolejnych segmentów pergoli"], "al26"),
        ("Akcesoria i wyposażenie", None,
         ["Zintegrowane, energooszczędne oświetlenie LED z możliwością ściemniania",
          "Wydajne promienniki podczerwieni dające przyjemne ciepło w chłodne wieczory",
          "Boczne przesłony screen ZIP redukujące wiatr i oślepiające słońce",
          "Przesuwne panele szklane chroniące przed deszczem bez utraty widoku na ogród"], "al35_rol")],
  related=["markizy", "oslony-zewnetrzne", "rolety-zewnetrzne"]),

"bramy-garazowe": dict(
  hero="brama_antracyt_lampy", h1="Bramy garażowe segmentowe i roletowe", title="Bramy garażowe segmentowe i roletowe, napędy Somfy i Nice | PROMYK",
  desc="Bramy garażowe segmentowe i roletowe z ciepłymi panelami 40–60 mm, napędy Somfy i Nice, drzwi boczne w tej samej kolorystyce.",
  intro="Ciepłe bramy garażowe z automatyką sterowaną smartfonem oraz dopasowane drzwi boczne.",
  adv=[("Bezpieczeństwo", "Wbudowane zabezpieczenia przed pęknięciem sprężyn i systemy antywłamaniowe", "lock"),
       ("Doskonała Izolacja", "Ciepłe panele o grubości 40-60 mm wypełnione twardą pianką poliuretanową", "thermo"),
       ("Niezawodne Napędy", "Komfortowa automatyka Somfy i Nice sterowana smartfonem i pilotem", "cog")],
  rows=[("Bramy segmentowe", None,
         ["Panele stalowe o doskonałym współczynniku przenikania ciepła",
          "Szeroki wybór przetłoczeń: wysokie, bez przetłoczeń, kasetony lub klasyczne",
          "Opcja wbudowania przeszkleń oraz drzwi przejściowych dla wygody",
          "Podwójne uszczelnienie wargowe na całym obwodzie bramy eliminujące przewiewy"], "brama_avo_dom"),
        ("Bramy roletowe", None,
         ["Idealne rozwiązanie do garaży o ograniczonej przestrzeni pod sufitem",
          "Brama nawija się pionowo na wał umieszczony w kompaktowej skrzynce",
          "Pancerz wykonany z profili aluminiowych najwyższej jakości wypełnionych pianką",
          "Standardowo wyposażone w napęd elektryczny z awaryjnym otwieraniem"], "brama_4"),
        ("Napędy i automatyka", None,
         ["Szybkie, ciche i bezawaryjne napędy nowej generacji z paskiem kevlarowym",
          "Amperometryczne wykrywanie przeszkód — brama zatrzyma się przed przeszkodą",
          "Integracja z systemami smart home Somfy TaHoma (obsługa głosowa i geolokalizacja)",
          "Wytrzymałe piloty wielokanałowe z kodem dynamicznie zmiennym"], "brama_antracyt"),
        ("Drzwi boczne", None,
         ["Dedykowane drzwi wejściowe montowane obok bramy w bryle budynku",
          "Identyczne przetłoczenia, struktura paneli oraz kolorystyka dopasowana do bramy",
          "Wysoka izolacja termiczna dzięki ciepłym profilom aluminiowym lub stalowym",
          "Wielopunktowe zamki ryglujące zapewniające wysoki standard antywłamaniowy"], "wiked67")],
  related=["okna", "drzwi-zewnetrzne", "rolety-zewnetrzne"]),

"markizy": dict(
  hero="al25", h1="Markizy tarasowe i balkonowe", title="Markizy tarasowe, balkonowe i przyścienne Selt | PROMYK Wieluń",
  desc="Markizy tarasowe w pełnej kasecie, markizy balkonowe i przyścienne. Tkaniny akrylowe, automatyka Somfy z czujnikami wiatru i słońca.",
  intro="Markizy z tkanin akrylowych o wysięgu do 6 m, z automatyką Somfy i czujnikami pogodowymi.",
  adv=[("Komfort", "Maksymalna ochrona przed szkodliwym promieniowaniem UV oraz nagrzewaniem tarasu i wnętrza", "sun"),
       ("Automatyka", "Zintegrowane czujniki wiatru, słońca oraz deszczu Somfy chroniące konstrukcję automatycznie", "wind"),
       ("Trwałość", "Tkaniny akrylowe impregnowane, odporne na płowienie, zabrudzenia i trudne warunki atmosferyczne", "shield")],
  rows=[("Markizy tarasowe",
         "Służą do zacieniania dużych powierzchni wypoczynkowych. Wyposażone w stabilną kasetę chroniącą poszycie po zwinięciu.",
         ["Konstrukcja w pełnej kasecie lub bezkasetowa o wzmocnionym profilu",
          "Możliwość regulacji kąta nachylenia dla optymalnego zacienienia",
          "Rozpiętości i wysięgi ramion dostosowane na wymiar do 6 metrów"], "al25"),
        ("Markizy balkonowe",
         "Kompaktowe i estetyczne systemy idealnie dopasowane do mniejszych przestrzeni, takich jak balkony w budownictwie wielorodzinnym.",
         ["Lekka, lecz wyjątkowo stabilna konstrukcja aluminiowa",
          "Szybki i nieinwazyjny montaż ścienny lub sufitowy",
          "Szeroka paleta odpornych na blaknięcie tkanin w modnych odcieniach"], "al26"),
        ("Markizy przyścienne",
         "Pionowe osłony tkaninowe instalowane do ścian bocznych, tworzące doskonałą barierę przed nisko świecącym słońcem i wiatrem.",
         ["Pionowa regulacja i stabilne naprężenie tkaniny",
          "Efektowna i elegancka alternatywa dla klasycznych refleksoli",
          "Dodatkowa ochrona prywatności przed sąsiadami"], "al27"),
        ("Automatyka i sterowanie",
         "Bezpieczeństwo i najwyższy standard obsługi dzięki niezawodnym silnikom i inteligentnemu systemowi sterowania pogodowego.",
         ["Wysokiej klasy napędy radiowe i przewodowe Somfy",
          "Automatyczne czujniki wiatru zwijające markizę przy silnym podmuchu",
          "Integracja z systemem smart home, sterowanie pilotem lub smartfonem"], "al35_rol")],
  related=["pergole", "oslony-zewnetrzne", "rolety-zewnetrzne"]),

"oslony-wewnetrzne": dict(
  hero="plisy", h1="Osłony wewnętrzne — żaluzje, plisy, rolety", title="Żaluzje, plisy i rolety wewnętrzne | PROMYK Wieluń",
  desc="Żaluzje aluminiowe, drewniane i pionowe, plisy, rolety dzień-noc, materiałowe i rzymskie. Pomiar i montaż w Wieluniu i okolicach.",
  intro="Pełna gama osłon wewnętrznych — od klasycznych żaluzji po plisy i rolety typu blackout.",
  adv=[("Estetyka", "Perfekcyjne dopełnienie i dopasowanie do każdego stylu aranżacji wnętrza", "sparkle"),
       ("Prywatność", "Precyzyjna, płynna regulacja stopnia zaciemnienia i ochrona przed wzrokiem z zewnątrz", "shield"),
       ("Łatwość", "Intuicyjna obsługa ręczna lub zaawansowane sterowanie elektryczne i radiowe", "cog")],
  rows=[("Żaluzje aluminiowe", None,
         ["Klasyczne i niezwykle precyzyjne lamele o szerokościach 25 mm oraz 50 mm",
          "Wysoka odporność na wilgoć — idealne rozwiązanie do kuchni i łazienek",
          "Szeroka paleta kolorów, w tym wykończenia matowe, perforowane i metaliczne"], "al27"),
        ("Żaluzje drewniane i bambusowe", None,
         ["Ekologiczne, naturalne materiały nadające wnętrzu wyjątkowo przytulny klimat",
          "Elegancki, prestiżowy wygląd pasujący do gabinetów i nowoczesnych salonów",
          "Lamele bambusowe o zmniejszonej grubości, zapewniające lekkość konstrukcji"], "abm_okno1"),
        ("Żaluzje pionowe (verticale)", None,
         ["Klasyczny system dedykowany do spektakularnych przeszkleń i nowoczesnych biur",
          "Komfortowa regulacja kąta obrotu pasów tkaniny pionowej",
          "Szeroki wybór atestowanych materiałów trudnopalnych i higienicznych"], "al26"),
        ("Plisy", None,
         ["Innowacyjny, harmonijkowy system umożliwiający zasłonięcie dowolnego fragmentu okna",
          "Unikalny system góra-dół (dwukierunkowy) zapewniający pełną swobodę aranżacji",
          "Możliwość zastosowania materiałów odbijających promienie słoneczne (powłoka perłowa)"], "plisy"),
        ("Rolety dzień-noc", None,
         ["Naprzemienne pasy materiału transparentnego i zaciemniającego",
          "Płynna regulacja dopływu światła bez konieczności pełnego podnoszenia rolety",
          "Nowoczesny design i szeroka gama stylowych tkanin strukturalnych"], "al28"),
        ("Rolety materiałowe", None,
         ["Klasyczne rolety wolnowiszące lub w eleganckich kasetach z prowadnicami",
          "Tkaniny typu blackout gwarantujące 100% zaciemnienia idealne do sypialni",
          "Materiały półprzezroczyste i dekoracyjne pięknie rozpraszające światło"], "al29"),
        ("Rolety rzymskie", None,
         ["Efektowne i dekoracyjne fałdy materiału powstające podczas podnoszenia",
          "Łatwy demontaż tkaniny do prania i konserwacji",
          "Bogata kolekcja tkanin naturalnych — od lnu po luksusowe welury"], "al38")],
  related=["okna", "moskitiery", "oslony-zewnetrzne"]),

"oslony-zewnetrzne": dict(
  hero="al27", h1="Osłony zewnętrzne — refleksole, żaluzje fasadowe, sunbreaker",
  title="Refleksole, żaluzje fasadowe i sunbreaker | PROMYK Wieluń",
  desc="Zewnętrzne osłony przeciwsłoneczne: refleksole (screen ZIP), żaluzje fasadowe i systemy sunbreaker. Automatyka Somfy, montaż Wieluń.",
  intro="Zatrzymują energię cieplną przed szybą — najskuteczniejsza ochrona przed przegrzewaniem wnętrz.",
  adv=[("Efektywność", "Zatrzymanie promieni słonecznych i energii cieplnej bezpośrednio PRZED szybą okienną", "sun"),
       ("Energooszczędność", "Wielokrotna redukcja kosztów klimatyzacji pomieszczeń podczas upalnych miesięcy letnich", "thermo"),
       ("Nowoczesność", "Automatyczne sterowanie oparte na systemach Somfy i czujnikach nasłonecznienia", "cog")],
  rows=[("Refleksole (screen zewnętrzny)",
         "Nowoczesne pionowe rolety tkaninowe przeznaczone do montażu zewnętrznego na budynkach mieszkalnych i komercyjnych.",
         ["Zaawansowana tkanina screen redukująca refleksy świetlne bez utraty widoku na zewnątrz",
          "Szeroki wybór prowadnic, w tym system ZIP działający jako szczelna moskitiera",
          "Wysoka odporność na silne parcie wiatru i nagłe zmiany pogody"], "al27"),
        ("Żaluzje fasadowe",
         "Służą do płynnego i bardzo precyzyjnego regulowania ilości światła wpadającego do nowoczesnych wnętrz.",
         ["Aluminiowe, trwałe lamele lakierowane proszkowo o przekroju C lub Z",
          "Doskonała izolacja termiczna redukująca konieczność chłodzenia",
          "Wyjątkowy efekt wizualny nadający elewacji modernistyczny charakter"], "al41"),
        ("Sunbreaker",
         "Wielkogabarytowy system przeciwsłoneczny będący integralnym, prestiżowym elementem architektonicznym budynku.",
         ["Lamele aluminiowe stałe lub ruchome z pełnym zakresem obrotu do 90 stopni",
          "Trwała, sztywna konstrukcja odporna na ekstremalne warunki pogodowe",
          "Doskonałe rozwiązanie do osłony rozległych przeszkleń pionowych i poziomych"], "al26")],
  related=["rolety-zewnetrzne", "pergole", "markizy"]),

"moskitiery": dict(
  hero="moskitiera_mrs", h1="Moskitiery na wymiar", title="Moskitiery ramkowe, drzwiowe, rolowane i plisowane | PROMYK Wieluń",
  desc="Moskitiery na wymiar: ramkowe, drzwiowe z samozamykaczem, rolowane w kasecie i plisowane do drzwi HST. Pomiar i montaż w Wieluniu.",
  intro="Produkowane na indywidualny wymiar dla każdego typu okna i drzwi — z siatką o swobodnym przepływie powietrza.",
  adv=[("Ochrona", "Pełna i niezwykle skuteczna bariera przed komarami, muchami oraz mniejszymi insektami", "bug"),
       ("Wentylacja", "Specjalny splot siatki gwarantuje swobodny przepływ świeżego powietrza do wnętrza", "wind"),
       ("Dopasowanie", "Produkowane wyłącznie na indywidualny wymiar dla każdego typu okna i drzwi", "ruler")],
  rows=[("Moskitiery ramkowe",
         "Klasyczne i najbardziej popularne zabezpieczenie do okien rozwiernych i uchylnych.",
         ["Lekka rama aluminiowa montowana bezinwazyjnie na obrzeżu okna za pomocą uchwytów",
          "Bardzo szybki demontaż na okres zimowy w celu czyszczenia i konserwacji",
          "Możliwość zastosowania siatki stalowej o podwyższonej odporności na zwierzęta domowe"], "moskitiera_mrs"),
        ("Moskitiery drzwiowe",
         "Wygodne osłony montowane na zawiasach, stworzone z myślą o przejściach na balkon lub taras.",
         ["Własna, stabilna ościeżnica z ergonomicznym samozamykaczem drzwiowym",
          "Specjalna uszczelka szczotkowa chroniąca próg przed drobnymi owadami",
          "Dyskretne magnesy trzymające moskitierę stabilnie w pozycji zamkniętej"], "al39"),
        ("Moskitiery rolowane",
         "Systemy wyposażone w kasetę górną lub boczną, działające podobnie jak rolety materiałowe.",
         ["Możliwość natychmiastowego schowania siatki do kasety w dowolnym momencie",
          "Prowadnice z uszczelnieniem szczotkowym zabezpieczające krawędzie boczne",
          "Dedykowane również do okien dachowych (dachowe moskitiery rolowane)"], "al28"),
        ("Moskitiery plisowane",
         "Luksusowe osłony harmonijkowe idealne do wielkogabarytowych drzwi przesuwnych typu HST.",
         ["Siatka składa się estetycznie w harmonijkę i chowa w profilu bocznym",
          "Superniski próg ułatwiający swobodne przechodzenie na taras",
          "Brak mechanizmu sprężynowego — zatrzymanie moskitiery w dowolnym położeniu"], "al25")],
  related=["okna", "rolety-zewnetrzne", "oslony-wewnetrzne"]),
}

# ---------------------------------------------------------------------------
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
        product_page(slug, meta)
    print("Gotowe.")
