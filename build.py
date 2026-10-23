# -*- coding: utf-8 -*-
"""
Generator statycznej strony PROMYK (Wieluń) — odwzorowanie projektu Figma.
Uruchomienie:  python build.py
Wynik: pliki .html w katalogu projektu (assets/ pozostają bez zmian).
"""
import os, io, html, re

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSET_VER = "68"  # podbij przy zmianach css/js (cache-busting)

PHONE = "607 941 499"
PHONE_TEL = "+48607941499"
PHONE2 = "43 843 65 43"
PHONE2_TEL = "+48438436543"
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
    ("pergole",           "Pergole",            "Aluprof",            "perg/sb400"),
    ("bramy-garazowe",    "Bramy garażowe",     "AVO / Aluprof",      "brama_antracyt"),
    ("markizy",           "Markizy",            "Aluprof",            "mark/hero"),
    ("oslony-wewnetrzne", "Osłony wewnętrzne",  "Produkcja własna",   "osl/hero"),
    ("oslony-zewnetrzne", "Osłony zewnętrzne",  "Aluprof",            "ozew/refleksole"),
    ("zaluzje-fasadowe",  "Żaluzje fasadowe",   "Aluprof",            "fasad/hero"),
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

GALLERY = [('gal/r01', 'Pergola lamelowa w ogrodzie', 'pergole'), ('gal/r02', 'Markiza tarasowa przy domu', 'markizy'), ('gal/r03', 'Drzwi wewnętrzne białe z czarną klamką', 'drzwi-wewnetrzne'), ('gal/r04', 'Żaluzje drewniane w salonie', 'oslony-wewnetrzne'), ('gal/r05', 'Okna w domu parterowym', 'okna'), ('gal/r06', 'Rolety zewnętrzne przy tarasie', 'rolety-zewnetrzne'), ('gal/r07', 'Drzwi zewnętrzne', 'drzwi-zewnetrzne'), ('gal/r08', 'Refleksol przy tarasie', 'oslony-zewnetrzne'), ('gal/r09', 'Żaluzje fasadowe na elewacji', 'zaluzje-fasadowe'), ('gal/r10', 'Moskitiera plisowana do drzwi tarasowych', 'moskitiery'), ('gal/r11', 'Brama garażowa antracytowa', 'bramy-garazowe'), ('gal/r12', 'Pergola nad strefą wypoczynku', 'pergole'), ('gal/r13', 'Markiza nad tarasem', 'markizy'), ('gal/r14', 'Drzwi wewnętrzne w czerni', 'drzwi-wewnetrzne'), ('gal/r15', 'Roleta rzymska w kuchni', 'oslony-wewnetrzne'), ('gal/r16', 'Okna i balkon', 'okna'), ('gal/r17', 'Rolety zewnętrzne', 'rolety-zewnetrzne'), ('gal/r18', 'Drzwi zewnętrzne drewnopodobne', 'drzwi-zewnetrzne'), ('gal/r19', 'Refleksole na elewacji', 'oslony-zewnetrzne'), ('gal/r20', 'Żaluzja fasadowa w oknie tarasowym', 'zaluzje-fasadowe'), ('gal/r21', 'Moskitiera plisowana', 'moskitiery'), ('gal/r22', 'Brama garażowa biała', 'bramy-garazowe'), ('gal/r23', 'Pergola — widok na lamele', 'pergole'), ('gal/r24', 'Markiza i strefa wypoczynku', 'markizy'), ('gal/r25', 'Drzwi wewnętrzne białe', 'drzwi-wewnetrzne'), ('gal/r26', 'Roleta materiałowa', 'oslony-wewnetrzne'), ('gal/r27', 'Przeszklenia od strony ogrodu', 'okna'), ('gal/r28', 'Rolety zewnętrzne na elewacji', 'rolety-zewnetrzne'), ('gal/r29', 'Drzwi zewnętrzne z przeszkleniem', 'drzwi-zewnetrzne'), ('gal/r30', 'Żaluzje fasadowe — widok od wewnątrz', 'zaluzje-fasadowe'), ('gal/r31', 'Moskitiera drzwiowa', 'moskitiery'), ('gal/r32', 'Brama garażowa segmentowa', 'bramy-garazowe'), ('gal/r33', 'Dach lamelowy pergoli', 'pergole'), ('gal/r34', 'Markiza nad tarasem — widok spod', 'markizy'), ('gal/r35', 'Drzwi wewnętrzne w korytarzu', 'drzwi-wewnetrzne'), ('gal/r36', 'Żaluzje drewnopodobne w narożnym oknie', 'oslony-wewnetrzne'), ('gal/r37', 'Przeszklenie w szczycie domu', 'okna'), ('gal/r38', 'Rolety zewnętrzne w domu jednorodzinnym', 'rolety-zewnetrzne'), ('gal/r39', 'Drzwi zewnętrzne antracyt + drewno', 'drzwi-zewnetrzne'), ('gal/r40', 'Brama garażowa w kolorze czerwonym', 'bramy-garazowe'), ('gal/r41', 'Markiza nad tarasem z zielenią', 'markizy'), ('gal/r42', 'Drzwi wewnętrzne w jasnym wnętrzu', 'drzwi-wewnetrzne'), ('gal/r43', 'Rolety dzień-noc', 'oslony-wewnetrzne'), ('gal/r44', 'Okna łukowe w nowym domu', 'okna'), ('gal/r45', 'Rolety zewnętrzne przy balkonie', 'rolety-zewnetrzne'), ('gal/r46', 'Drzwi zewnętrzne antracytowe', 'drzwi-zewnetrzne'), ('gal/r47', 'Brama garażowa w nowym domu', 'bramy-garazowe'), ('gal/r48', 'Markiza kasetowa na elewacji', 'markizy'), ('gal/r49', 'Drzwi wewnętrzne drewnopodobne', 'drzwi-wewnetrzne'), ('gal/r50', 'Rolety rzymskie w kuchni', 'oslony-wewnetrzne'), ('gal/r51', 'Okna łukowe — montaż', 'okna'), ('gal/r52', 'Roleta zewnętrzna w oknie', 'rolety-zewnetrzne'), ('gal/r53', 'Drzwi zewnętrzne zielone', 'drzwi-zewnetrzne'), ('gal/r54', 'Markiza tarasowa — widok z boku', 'markizy'), ('gal/r55', 'Drzwi wewnętrzne do łazienki', 'drzwi-wewnetrzne'), ('gal/r56', 'Żaluzje w jadalni', 'oslony-wewnetrzne'), ('gal/r57', 'Duże przeszklenie w szczycie', 'okna'), ('gal/r58', 'Drzwi zewnętrzne białe', 'drzwi-zewnetrzne'), ('gal/r59', 'Drzwi wewnętrzne frezowane', 'drzwi-wewnetrzne'), ('gal/r60', 'Rolety dzień-noc w salonie', 'oslony-wewnetrzne'), ('gal/r61', 'Okna w domu parterowym — montaż', 'okna'), ('gal/r62', 'Drzwi zewnętrzne z doświetlem', 'drzwi-zewnetrzne'), ('gal/r63', 'Roleta rzymska', 'oslony-wewnetrzne'), ('gal/r64', 'Drzwi zewnętrzne złoty dąb', 'drzwi-zewnetrzne'), ('gal/r65', 'Żaluzje w kuchni', 'oslony-wewnetrzne'), ('gal/r66', 'Drzwi zewnętrzne z przeszkleniami', 'drzwi-zewnetrzne'), ('gal/r67', 'Rolety rzymskie', 'oslony-wewnetrzne'), ('gal/r68', 'Żaluzje drewnopodobne', 'oslony-wewnetrzne'), ('gal/r69', 'Żaluzje przy drzwiach tarasowych', 'oslony-wewnetrzne'), ('gal/r70', 'Roleta rzymska w oknie', 'oslony-wewnetrzne'), ('gal/r71', 'Roleta rzymska — tkanina', 'oslony-wewnetrzne'), ('gal/r72', 'Żaluzje przy drzwiach balkonowych', 'oslony-wewnetrzne'), ('gal/r73', 'Żaluzje drewniane w kuchni', 'oslony-wewnetrzne'), ('gal/r74', 'Żaluzje aluminiowe w dużym oknie', 'oslony-wewnetrzne'), ('gal/r75', 'Żaluzje drewniane nad zlewem', 'oslony-wewnetrzne'), ('gal/r76', 'Żaluzje w ciemnym kolorze', 'oslony-wewnetrzne'), ('gal/r77', 'Żaluzje drewniane w oknie tarasowym', 'oslony-wewnetrzne'), ('gal/r78', 'Żaluzje aluminiowe w jadalni', 'oslony-wewnetrzne'), ('gal/r79', 'Żaluzje aluminiowe w oknie', 'oslony-wewnetrzne'), ('gal/r80', 'Żaluzje drewniane w narożnej kuchni', 'oslony-wewnetrzne')]

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
      <a href="konfigurator.html"{cls('konfigurator')}>Konfigurator okien</a>
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
    <figure class="split__media about__fig"><img class="about__img about__img--full" src="assets/img/onas/promyk-firma.jpg" alt="Siedziba PROMYK w Wieluniu"><figcaption>Nasza obecna siedziba w Wieluniu</figcaption></figure>
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
        ("Aluprof Sun Shading Solutions — pergole 2026", "Pergole lamelowe SB400, SB350, SB400R i doposażenia", "katalog-aluprof-pergole.pdf"),
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
                    "Wszystko, czego potrzebujesz do swojego domu, w jednym miejscu – od okien i drzwi po bramy garażowe i nowoczesne osłony okienne.", None)
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

{partners()}

<section class="section section--soft">
  <div class="container">
    <div class="section-header">
      <div class="section-header__left">
        <span class="tag">Materiały informacyjne</span>
        <h2 class="h-sec">Katalogi do pobrania</h2>
        <p class="lead">Pobierz oficjalne katalogi naszych partnerów, aby zapoznać się ze szczegółowymi specyfikacjami technicznymi.</p>
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

GAL_BY_CAP = {c: im.split("/")[1] for im, c, _k in GALLERY}

def _inv_house():
    """Animowany dom: po kolei pojawiają się elementy, które zamówisz w PROMYK (zsynchronizowane z listą obok)."""
    return """<figure class="inv-house" aria-label="Symulacja: komplet stolarki dla domu">
  <svg viewBox="0 0 640 470" role="img">
    <defs>
      <linearGradient id="ihSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#dfe9f2"/><stop offset="1" stop-color="#f6f8fa"/></linearGradient>
      <linearGradient id="ihGlass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b9cfe0"/><stop offset=".55" stop-color="#e8f0f6"/><stop offset="1" stop-color="#9fb8cc"/></linearGradient>
      <pattern id="ihSeg" width="10" height="16" patternUnits="userSpaceOnUse"><rect width="10" height="16" fill="#3a3d42"/><path d="M0 15.5h10" stroke="#2a2c30" stroke-width="1.4"/></pattern>
      <pattern id="ihLam" width="10" height="9" patternUnits="userSpaceOnUse"><rect width="10" height="9" fill="#4b4f55"/><path d="M0 8.5h10" stroke="#2c2f33" stroke-width="1.6"/></pattern>
      <pattern id="ihRol" width="10" height="7" patternUnits="userSpaceOnUse"><rect width="10" height="7" fill="#5a5e64"/><path d="M0 6.5h10" stroke="#3b3e43" stroke-width="1.2"/></pattern>
      <clipPath id="ihRolClip"><rect x="232" y="206" width="78" height="96"/></clipPath>
    </defs>
    <rect width="640" height="470" fill="url(#ihSky)"/>
    <circle class="ih-sun" cx="560" cy="70" r="30" fill="#f6d27a" opacity=".85"/>
    <rect y="402" width="640" height="68" fill="#cfd8c4"/>
    <!-- bryła -->
    <path d="M60 402V210l170-118 170 118v192z" fill="#fbfaf7" stroke="#d6d2c9" stroke-width="2"/>
    <path d="M40 222 230 86l190 136" fill="none" stroke="#3a3d42" stroke-width="16" stroke-linejoin="round"/>
    <rect x="400" y="262" width="200" height="140" fill="#f3f1ec" stroke="#d6d2c9" stroke-width="2"/>
    <rect x="392" y="250" width="216" height="16" fill="#3a3d42"/>
    <!-- okna -->
    <g class="ih-el" data-k="okna" style="--i:0">
      <rect x="200" y="140" width="60" height="46" rx="2" fill="url(#ihGlass)" stroke="#3a3d42" stroke-width="5"/><path d="M230 140v46" stroke="#3a3d42" stroke-width="4"/>
      <rect x="88" y="214" width="96" height="88" fill="url(#ihGlass)" stroke="#3a3d42" stroke-width="6"/><path d="M136 214v88" stroke="#3a3d42" stroke-width="5"/>
      <rect x="232" y="206" width="78" height="96" fill="url(#ihGlass)" stroke="#3a3d42" stroke-width="6"/><path d="M271 206v96" stroke="#3a3d42" stroke-width="5"/>
      <rect x="330" y="214" width="52" height="170" fill="url(#ihGlass)" stroke="#3a3d42" stroke-width="6"/>
      <path class="ih-shine" d="M96 296 128 222M240 296 262 214" stroke="#fff" stroke-width="6" opacity=".55"/>
    </g>
    <!-- parapety -->
    <g class="ih-el" data-k="parapety" style="--i:6">
      <rect x="80" y="301" width="112" height="9" rx="2" fill="#8d9299"/><rect x="224" y="301" width="94" height="9" rx="2" fill="#8d9299"/><rect x="193" y="185" width="74" height="8" rx="2" fill="#8d9299"/><rect x="322" y="383" width="68" height="8" rx="2" fill="#8d9299"/>
    </g>
    <!-- rolety zewnętrzne (pancerz zjeżdża w pętli) -->
    <g class="ih-el" data-k="rolety" style="--i:3">
      <rect x="226" y="194" width="90" height="13" rx="2" fill="#4b4f55"/>
      <g clip-path="url(#ihRolClip)"><rect class="ih-rol" x="232" y="206" width="78" height="96" fill="url(#ihRol)"/></g>
      <rect x="82" y="202" width="108" height="13" rx="2" fill="#4b4f55"/>
    </g>
    <!-- żaluzje fasadowe na wysokim przeszkleniu -->
    <g class="ih-el" data-k="fasad" style="--i:4">
      <rect x="324" y="202" width="64" height="12" rx="2" fill="#3a3d42"/>
      <rect class="ih-fasad" x="330" y="214" width="52" height="110" fill="url(#ihLam)" opacity=".95"/>
    </g>
    <!-- drzwi zewnętrzne -->
    <g class="ih-el" data-k="drzwi" style="--i:1">
      <rect x="146" y="318" width="54" height="84" rx="2" fill="#8a5a33" stroke="#3a3d42" stroke-width="4"/>
      <path d="M156 326v68M164 326v68M172 326v68" stroke="#6e4524" stroke-width="2"/><rect x="186" y="332" width="5" height="56" rx="2" fill="#d9d9d9"/>
      <rect x="140" y="400" width="66" height="6" fill="#9aa0a6"/>
    </g>
    <!-- drzwi wewnętrzne (widok przez okno) -->
    <g class="ih-el" data-k="dw" style="--i:5">
      <rect x="248" y="232" width="20" height="62" fill="#f4f1ea" stroke="#8d8f93" stroke-width="1.5"/><circle cx="264" cy="264" r="1.8" fill="#333"/>
    </g>
    <!-- brama garażowa -->
    <g class="ih-el" data-k="brama" style="--i:2">
      <rect x="430" y="290" width="140" height="112" fill="url(#ihSeg)" stroke="#2a2c30" stroke-width="4"/>
      <rect x="440" y="300" width="120" height="6" fill="#55595f"/>
    </g>
    <!-- pergola / osłony przeciwsłoneczne -->
    <g class="ih-el" data-k="oslony" style="--i:7">
      <path d="M-10 300h66" stroke="#3a3d42" stroke-width="8"/><path d="M6 300v102" stroke="#3a3d42" stroke-width="6"/>
      <path class="ih-blades" d="M-4 292l10 8M8 292l10 8M20 292l10 8M32 292l10 8M44 292l10 8" stroke="#55595f" stroke-width="4"/>
    </g>
    <path d="M0 402h640" stroke="#b9c3ad" stroke-width="3"/>
  </svg>
  <figcaption>Wszystko dla Twojego domu w jednym miejscu — najedź na pozycję z listy, aby zobaczyć ją na wizualizacji.</figcaption>
</figure>"""

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
        ("02", "Dobór i wycena", "Konfigurujemy najlepsze profile i przygotowujemy przejrzysty kosztorys."),
        ("03", "Pomiar na budowie", "Wykonujemy precyzyjne pomiary otworów przy użyciu profesjonalnego lasera."),
        ("04", "Produkcja", "Zamawiamy spersonalizowaną stolarkę u czołowych producentów (VEKA, Wikęd, DRE)."),
        ("05", "Montaż", "Montaż wykonują nasze doświadczone ekipy — starannie, czysto i zgodnie ze sztuką."),
    ]
    st = "".join(f'<article class="step" style="--i:{k}"><div class="step__no">{n}</div><h3>{t}</h3><p>{d}</p></article>' for k, (n, t, d) in enumerate(steps))

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
         "Najlepszym momentem jest etap stanu surowego otwartego, tuż po ukończeniu ścian i dachu. Pozwala to na precyzyjny pomiar przed tynkami oraz odpowiednie zaplanowanie montażu oraz osłon zewnętrznych (żaluzji, rolet)."),
        ("Na jakim etapie inwestycji najlepiej się z Wami skontaktować?",
         "Najlepiej zgłosić się do nas już na etapie projektu domu – im wcześniej rozpoczniemy współpracę, tym większe możliwości doboru optymalnych rozwiązań."),
        ("Czy doradztwo techniczne jest bezpłatne?",
         "Tak. Podczas bezpłatnego spotkania w naszej siedzibie wspólnie przeanalizujemy projekt domu, doradzimy najlepsze rozwiązania techniczne i estetyczne oraz przygotujemy wstępną, niezobowiązującą wycenę. Po podjęciu decyzji wykonujemy dokładny pomiar na budowie."),
        ("Jak długo trwa realizacja zamówienia od pomiaru?",
         "Standardowy termin realizacji to zwykle 4–8 tygodni od zatwierdzenia zamówienia i wykonania pomiaru. Termin zależy od producenta i stopnia personalizacji stolarki — dokładną datę potwierdzamy w umowie i dopasowujemy do harmonogramu budowy."),
        ("Czy wykonujecie montaż w innych miastach niż Wieluń?",
         "Tak. Działamy w promieniu ok. 200 km od Wielunia — obsługujemy cały region łódzki oraz województwa sąsiednie."),
        ("Czy możecie przygotować ofertę na podstawie projektu?",
         "Tak, możemy przygotować ofertę na podstawie projektu budowlanego. Dzięki temu już na wczesnym etapie inwestycji możemy dobrać odpowiednie rozwiązania w zakresie okien, drzwi, bram, parapetów i osłon, dopasowane do założeń projektu oraz potrzeb inwestora."),
        ("Czy oferujecie korzystne warunki współpracy przy większych zamówieniach?",
         "Tak, przy większych zamówieniach przygotowujemy indywidualne oferty dopasowane do zakresu inwestycji. Zależy nam na długofalowej współpracy, dlatego stawiamy na korzystne warunki, kompleksową obsługę i rozwiązania dopasowane do potrzeb inwestora."),
    ]
    fq = ""
    for k, (q, a) in enumerate(faq):
        cls = ""
        sign = "+"
        fq += f"""<div class="faq__row{cls}">
      <button class="faq__q"><span>{q}</span><span>{sign}</span></button>
      <div class="faq__a">{a}</div>
    </div>"""

    body = pagehero("inw/projekt", "Kompleksowe rozwiązania dla Twojej inwestycji — od etapu projektu po realizację",
                    "Budowa domu to wiele ważnych decyzji. Wybór okien, drzwi, bramy czy rolet wpływa nie tylko na wygląd budynku, ale również na komfort, bezpieczeństwo i koszty jego użytkowania przez wiele lat.", None)

    flow_items = [
        (["inw/konsultacja"], "Bezpłatna konsultacja",
         "Spotykamy się w naszym salonie w Wieluniu. Analizujemy projekt architektoniczny, pytamy o Twoje oczekiwania, styl domu i budżet. Podpowiadamy, o czym warto pomyśleć już na etapie projektu — np. o wielkości przeszkleń czy miejscu na rolety i żaluzje fasadowe."),
        (["veka_profil"], "Dobór i wycena",
         "Dobieramy systemy profili, pakiety szybowe, okucia i kolory — przekroje profili i próbki kolorów pokazujemy na żywo. Na tej podstawie przygotowujemy przejrzystą, niezobowiązującą wycenę całego zamówienia: okien, drzwi, bramy, rolet i osłon."),
        (["inw/pomiar"], "Pomiar na budowie",
         "Gdy otwory są gotowe, nasz specjalista przyjeżdża na budowę i wykonuje dokładny pomiar dalmierzem laserowym. Sprawdzamy też warunki montażu, aby każdy element pasował idealnie i nie wymagał przeróbek."),
        (["inw/produkcja"], "Produkcja",
         "Stolarkę zamawiamy u sprawdzonych producentów (VEKA, Wikęd, DRE, Aluprof), a rolety, moskitiery i osłony wykonujemy w naszej pracowni. Termin dostawy dopasowujemy do harmonogramu Twojej budowy."),
        (["inw/montaz"], "Montaż",
         "Montaż wykonują nasze doświadczone ekipy — starannie, czysto i zgodnie ze sztuką. Po zakończeniu prac sprawdzamy działanie każdego elementu, regulujemy okucia i pokazujemy, jak dbać o nowe okna i drzwi."),
        (["gal/" + GAL_BY_CAP["Pergola lamelowa w ogrodzie"], "gal/" + GAL_BY_CAP["Żaluzje drewniane w salonie"]], "Zapraszamy ponownie",
         "Gdy dom jest już gotowy, nadal jesteśmy do Twojej dyspozycji: urządzimy wnętrza osłonami — roletami, żaluzjami i plisami — a ogród i taras pergolą, markizą, refleksolami lub sunbreakerem."),
    ]
    def _imgs(ims, t):
        return "".join(f'<img src="assets/img/{im}.jpg" alt="{t}" loading="lazy">' for im in ims)
    flow = "".join(f"""<article class="inv-card" style="--i:{k}">
      <div class="inv-card__img{' inv-card__img--duo' if len(ims) > 1 else ''}">{_imgs(ims, t)}<span class="inv-card__no">0{k + 1}</span></div>
      <div class="inv-card__body"><h3>{t}</h3><p>{d}</p></div>
    </article>""" for k, (ims, t, d) in enumerate(flow_items))

    body += f"""<section class="section">
  <div class="container split split--inv">
    <div class="split__text">
      <h2 class="h-sec">Wszystko zamówisz w jednym miejscu</h2>
      <div class="prose">
        <p>Warto zgłosić się do nas już na etapie projektu domu. Im wcześniej rozpoczniemy współpracę, tym większe możliwości doboru optymalnych rozwiązań oraz lepszego zaplanowania całej inwestycji.</p>
        <p>Oferujemy kompleksową obsługę inwestorów – od pierwszej konsultacji aż po profesjonalny montaż. W jednym miejscu mogą Państwo zamówić:</p>
        <ul class="inv-list">
          <li data-k="okna" style="--i:0"><span class="check">{I['check']}</span> okna</li>
          <li data-k="drzwi" style="--i:1"><span class="check">{I['check']}</span> drzwi zewnętrzne</li>
          <li data-k="brama" style="--i:2"><span class="check">{I['check']}</span> bramy garażowe</li>
          <li data-k="rolety" style="--i:3"><span class="check">{I['check']}</span> rolety zewnętrzne</li>
          <li data-k="fasad" style="--i:4"><span class="check">{I['check']}</span> żaluzje fasadowe</li>
          <li data-k="dw" style="--i:5"><span class="check">{I['check']}</span> drzwi wewnętrzne</li>
          <li data-k="parapety" style="--i:6"><span class="check">{I['check']}</span> parapety zewnętrzne i wewnętrzne</li>
          <li data-k="oslony" style="--i:7"><span class="check">{I['check']}</span> osłony przeciwsłoneczne</li>
        </ul>
      </div>
      <a class="btn btn--primary" href="kontakt.html">Umów bezpłatną konsultację {I['arrow']}</a>
    </div>
    <div class="split__media">{_inv_house()}</div>
  </div>
</section>

<section class="section section--soft">
  <div class="container">
    <div class="section-header">
      <div class="section-header__left">
        <h2 class="h-sec">Od projektu po montaż — krok po kroku</h2>
      </div>
    </div>
    <div class="inv-flow inv-flow--steps">{flow}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header">
      <div class="section-header__left">
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
        <h2 class="h-sec">Baza wiedzy inwestora (FAQ)</h2>
      </div>
    </div>
    <div class="faq">{fq}</div>
  </div>
</section>

{cta(None, "Rozpocznij planowanie już teraz",
     "Nie zwlekaj do ostatniej chwili. Skonsultuj z nami swój projekt, aby uniknąć błędów projektowych i zaoszczędzić na budowie.")}
"""
    write("dla-inwestora.html",
          head("Dla Inwestora — kompleksowa obsługa budowy | PROMYK Wieluń",
               "Planujesz budowę domu? Okna, drzwi, bramy garażowe, rolety i parapety zamówisz w jednym miejscu. Bezpłatna konsultacja i profesjonalny montaż.")
          + nav("dla-inwestora") + body + footer())

# ================================================================ GALERIA ----
def build_galeria():
    cats = [("all", "Wszystkie")] + [(sl, t) for sl, t, _b, _i in PRODUCTS if sl != "parapety"]
    fl = "".join(f'<button class="filter{" is-active" if c == "all" else ""}" data-filter="{c}">{t}</button>' for c, t in cats)
    items = ""
    for k, (img, cap, cat) in enumerate(GALLERY):
        hid = " is-hidden" if k >= 24 else ""
        style = ' style="display:none"' if k >= 24 else ""
        items += f'<a href="assets/img/{img}.jpg" target="_blank" data-cat="{cat}" class="{hid.strip()}"{style}><img src="assets/img/{img}.jpg" alt="{cap}" loading="lazy"></a>'

    body = pagehero("wiked67", "Galeria realizacji",
                    "Zobacz, jak nasze produkty wyglądają w prawdziwych domach naszych klientów — od okien i drzwi po bramy, pergole i osłony.", None)
    body += f"""<section class="section" style="padding-bottom:0">
  <div class="container"><div class="filters">{fl}</div></div>
</section>

<section class="section">
  <div class="container">
    <div class="gallery">{items}</div>
    <div style="text-align:center;margin-top:48px">
      <button class="btn btn--outline" data-more>Pokaż więcej realizacji {I['chevD']}</button>
      <div class="gal-social">
        <a class="btn btn--primary" href="{FB_URL}" target="_blank" rel="noopener">{I['fb']} Więcej realizacji na Facebooku</a>
        <a class="btn btn--ig" href="{IG_URL}" target="_blank" rel="noopener">{I['ig']} Zobacz nas na Instagramie</a>
      </div>
    </div>
  </div>
</section>

{cta("Precyzja i profesjonalizm", "Chcesz podobny efekt u siebie?",
     "Zadbamy o każdy detal — od dokładnego pomiaru laserowego na Twojej budowie po czysty i bezbłędny montaż z gwarancją premium.")}
"""
    write("galeria.html",
          head("Galeria realizacji — okna, drzwi, pergole i osłony | PROMYK Wieluń",
               "Galeria realizacji firmy PROMYK: montaż okien, drzwi zewnętrznych i wewnętrznych, bram garażowych, rolet, pergoli i osłon przeciwsłonecznych.")
          + nav("galeria") + body + footer())

# ================================================================ KONTAKT ----
def build_kontakt():
    opts = "".join(f"<option>{t}</option>" for t in
                   ["Wycena stolarki okiennej", "Drzwi zewnętrzne", "Drzwi wewnętrzne", "Bramy garażowe",
                    "Rolety i osłony", "Pergole i markizy", "Moskitiery", "Serwis i reklamacja", "Inne pytanie"])
    body = f"""<section class="section" style="padding-bottom:0">
  <div class="container contact-head">
    <h1>Jesteśmy tutaj dla Ciebie</h1>
    <p>Masz pytania dotyczące naszych produktów, montażu lub możliwości współpracy? Zadzwoń, napisz lub odwiedź nasz salon.</p>
  </div>
  <div class="container contact-quick contact-quick--3">
    <a class="contact-quick__item" href="tel:{PHONE_TEL}"><span class="contact-quick__icon">{I['phone']}</span><span><small>Zadzwoń — komórka</small><strong>{PHONE}</strong></span></a>
    <a class="contact-quick__item" href="tel:{PHONE2_TEL}"><span class="contact-quick__icon">{I['phone']}</span><span><small>Zadzwoń — biuro</small><strong>{PHONE2}</strong></span></a>
    <a class="contact-quick__item" href="mailto:{MAIL}"><span class="contact-quick__icon">{I['mail']}</span><span><small>Napisz e-mail</small><strong>{MAIL}</strong></span></a>
  </div>
  <div class="container contact-intro">
    <h2>Zapraszamy do kontaktu</h2>
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
        <p><strong>Z.P.H.U. „PROMYK” Krystyna i Grzegorz Czyż s.c.</strong></p>
        <p>ul. Michała Wołodyjowskiego 15</p>
        <p>{ADDR2}</p>
      </div>
      <figure class="contact-photo"><img src="assets/img/onas/promyk-firma.jpg" alt="Siedziba PROMYK w Wieluniu" loading="lazy"><figcaption>Nasza siedziba w Wieluniu</figcaption></figure>
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
    opens = [("RU", "Rozwierno-uchylne", '<svg viewBox="0 0 44 44"><rect x="6" y="4" width="32" height="36" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M38 4 6 22l32 18M6 40l16-36 16 36" stroke="currentColor" stroke-width="1.4" fill="none" stroke-dasharray="3 2"/></svg>'),
             ("R", "Rozwierne", '<svg viewBox="0 0 44 44"><rect x="6" y="4" width="32" height="36" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M38 4 6 22l32 18" stroke="currentColor" stroke-width="1.4" fill="none" stroke-dasharray="3 2"/></svg>'),
             ("U", "Uchylne", '<svg viewBox="0 0 44 44"><rect x="6" y="4" width="32" height="36" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M6 40l16-36 16 36" stroke="currentColor" stroke-width="1.4" fill="none" stroke-dasharray="3 2"/></svg>'),
             ("FIX", "Stałe (FIX)", '<svg viewBox="0 0 44 44"><rect x="6" y="4" width="32" height="36" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M16 22h12M22 16v12" stroke="currentColor" stroke-width="2"/></svg>')]
    op = "".join(
        f'<button type="button" class="optcard{" is-active" if k == "RU" else ""}" data-value="{k}">{svg}{n}</button>'
        for k, n, svg in opens)
    gl = "".join(
        f'<button type="button" class="optcard{" is-active" if k == "3" else ""}" data-value="{k}"><svg viewBox="0 0 44 44">' +
        "".join(f'<path d="M{12 + 8 * i} 6v32" stroke="currentColor" stroke-width="2.4"/>' for i in range(int(k))) +
        f'</svg>{k}-szybowy</button>' for k in ("2", "3"))

    scenes = [("plaster", "Tynk biały", "#ece9e2"), ("grey", "Tynk szary", "#b7babd"),
              ("anthracite", "Antracyt", "#43484d"), ("brick", "Cegła", "#a75d45"), ("wood", "Deska", "#a97b4e")]
    sc = "".join(
        f'<button type="button" data-scene="{k}" title="Elewacja: {n}" aria-label="Elewacja: {n}"'
        f'{" class=is-active" if k == "plaster" else ""} style="background:{c}"></button>'
        for k, n, c in scenes)

    body = f"""<section class="section" style="padding-block:56px 0">
  <div class="container">
    <h1 class="h-sec" style="margin:0 0 10px">Konfigurator okien</h1>
    <p class="lead lead--lg" style="max-width:760px">Złóż swoje okno na żywo — wybierz konstrukcję, sposób otwierania, kolory, klamkę i szprosy, sprawdź wygląd na różnych elewacjach, dodaj kolejne pozycje i wyślij zapytanie o wycenę.</p>
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
      <div class="alert">💡 <strong>Wskazówka:</strong> kolory drewnopodobne (Złoty dąb, Orzech, Winchester) doskonale pasują do nowoczesnego budownictwa i elewacji z elementami naturalnego drewna.</div>
    </div>

    <div class="cfg-panel">
      <div class="optgroup cfg-only-scene" data-group="type">
        <h3><span class="no">1</span> Typ konstrukcji <span class="picked"></span></h3>
        <div class="optcards optcards--3">{ty}</div>
      </div>
      <div class="optgroup cfg-only-scene" data-group="open">
        <h3><span class="no">2</span> Sposób otwierania <span class="picked"></span></h3>
        <div class="optcards" data-open-options></div>
      </div>
      <div class="optgroup cfg-only-scene">
        <h3><span class="no">3</span> Wymiary okna</h3>
        <div class="dims">
          <div><label for="cfg-w" data-wlabel>Szerokość</label><div class="dim-wrap"><input id="cfg-w" data-w type="number" min="50" max="200" step="5" value="160"><span class="unit">cm</span></div></div>
          <div><label for="cfg-h" data-hlabel>Wysokość</label><div class="dim-wrap"><input id="cfg-h" data-h type="number" min="50" max="280" step="5" value="150"><span class="unit">cm</span></div></div>
        </div>
      </div>
      <div class="optgroup cfg-only-scene" data-group="glass">
        <h3><span class="no">4</span> Pakiet szybowy <span class="picked"></span></h3>
        <div class="optcards optcards--2">{gl}</div>
      </div>
      <div class="optgroup" data-group="out">
        <h3><span class="no">5</span> Kolor od zewnątrz (dekory VEKA) <span class="picked"></span></h3>
        <div class="veka-cat veka-cat--std">★ Kolory standardowe</div>
        <div class="veka-row veka-row--std" data-vekagroup="std"></div>
        <div class="veka-cat">Paleta kolorów (na zamówienie)</div>
        <div class="veka-row" data-vekagroup="uni"></div>
        <div class="veka-cat">Dekory drewnopodobne i metalopodobne</div>
        <div class="veka-row" data-vekagroup="dekor"></div>
        <div class="veka-cat">VEKA Spectral (ultramat)</div>
        <div class="veka-row" data-vekagroup="spectral"></div>
      </div>
      <div class="optgroup cfg-only-scene" data-group="in">
        <h3><span class="no">6</span> Kolor od wewnątrz <span class="picked"></span></h3>
        <div class="veka-row veka-row--std" data-instd></div>
      </div>
      <div class="optgroup cfg-only-scene" data-group="handle">
        <h3><span class="no">7</span> Klamka okienna <span class="picked"></span></h3>
        <div class="optcards">{hd}</div>
      </div>
      <div class="optgroup cfg-only-scene" data-group="bars">
        <h3><span class="no">8</span> Szprosy (szczebliny) <span class="picked"></span></h3>
        <div class="optcards">{bd}</div>
      </div>
      <div class="recap">
        <h3>Twoja konfiguracja</h3>
        <dl data-recap></dl>
        <div class="qty-row">
          <label for="cfg-qty">Ilość sztuk</label>
          <div class="dim-wrap"><input id="cfg-qty" data-qty type="number" min="1" max="99" step="1" value="1"><span class="unit">szt.</span></div>
        </div>
        <button type="button" class="btn btn--outline btn--sm" data-add>+ Dodaj pozycję do zapytania</button>
        <div class="positions is-empty">
          <h4>Pozycje w zapytaniu</h4>
          <ol data-positions></ol>
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
               "Interaktywny konfigurator okien: typ konstrukcji, sposób otwierania, pakiet szybowy, kolory, klamka i szprosy. Dodaj kilka pozycji i wyślij zapytanie o wycenę.")
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
  hero="katalog/markiza-palladio-taras", h1="Markizy tarasowe i balkonowe Aluprof", title="Markizy tarasowe Aluprof — kaseta pełna, wysięg do 4 m, Somfy | PROMYK Wieluń",
  desc="Markizy tarasowe Aluprof w pełnej kasecie (wysięg do 4 m), balkonowe i pionowe. Tkanina akrylowa 300 g/m², automatyka Somfy.",
  intro="Markizy Aluprof z tkaniną akrylową 300 g/m² i napędami Somfy z czujnikami pogodowymi.",
  producers=["aluprof", "somfy"],
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
  intro="Osłony zatrzymujące ciepło przed szybą (Aluprof) — najskuteczniejsza ochrona przed przegrzewaniem.",
  producers=["aluprof", "somfy"],
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
    ("aluprof", "Aluprof", [
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
    ("aluprof", "Aluprof", [
      "Refleksole screen z prowadnicami ZIP — do 6 m szerokości",
      "Tkaniny serge o różnym stopniu otwarcia (1–5%), kasety 85–150 mm, kolory RAL",
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
  specs=dict(title="Dobór moskitiery do stolarki", cols=["Typ", "Zastosowanie", "Cechy"],
    rows=[["Ramkowa", "okna rozwierne i uchylne", "montaż bez wiercenia, demontaż na zimę"],
          ["Drzwiowa", "balkon, taras", "zawiasy, domykanie magnetyczne"],
          ["Rolowana", "okna rozwierne, okna dachowe", "kaseta, możliwość schowania siatki"],
          ["Plisowana", "HST, okno z ruchomym słupkiem, drzwi zewnętrzne", "niski próg, po złożeniu zajmuje niewiele miejsca"]]),
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
        if parent in ("okna", "drzwi-zewnetrzne", "drzwi-wewnetrzne", "rolety-zewnetrzne", "pergole", "bramy-garazowe", "markizy", "oslony-wewnetrzne", "oslony-zewnetrzne", "moskitiery"):   # bez podstron 3. poziomu (uwagi klienta)
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
{_anim_section(_okno_anim(), "Jak działa okno rozwierno-uchylne?", "Jedno skrzydło, dwie funkcje: klamka ustawiona poziomo pozwala otworzyć okno na całą szerokość, a skierowana do góry — uchylić je do wietrzenia. Okucia obwiedniowe dociskają skrzydło do ramy w wielu punktach, dzięki czemu okno pozostaje szczelne i bezpieczne.")}
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
      "Dostęp serwisowy przez klapę rewizyjną"], "rol/podtynkowe-elewacja"),
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

    body = pagehero("rol/hero-wnetrze", "Rolety zewnętrzne Aluprof – nowoczesne rozwiązania dla Twojego domu",
                    "Aluminiowe profile wypełnione pianką pomagają ograniczyć straty ciepła, chronią przed nadmiernym nasłonecznieniem i zapewniają mieszkańcom większy komfort na co dzień.", None)
    body += f"""<section class="section section--tight-bottom"><div class="container">{rows}</div></section>
<section class="advantages"><div class="container advantages__inner">{adv}</div></section>
{_anim_section(_roleta_anim(), "Jak działa roleta zewnętrzna?", "Pancerz z profili aluminiowych zwija się w skrzynce nad oknem i zjeżdża w prowadnicach. Opuszczona roleta zaciemnia wnętrze, chroni przed nagrzewaniem latem, ogranicza straty ciepła zimą i utrudnia włamanie. Sterujesz nią ręcznie, przyciskiem, pilotem albo z telefonu.")}
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
    'w-granit': [('Vanga', 'w-granit-01'), ('Blue Night', 'w-granit-02'), ('Colonial White', 'w-granit-03'), ('Royal Black', 'w-granit-04'), ('Nero Impala', 'w-granit-05'), ('Tan Brown', 'w-granit-06'), ('China Cristal', 'w-granit-07'), ('Steel Grey', 'w-granit-08'), ('Yellow Pink', 'w-granit-09'), ('Rosa Beta', 'w-granit-10')],
    'w-kwarcyt': [('Bianchissimo', 'w-kwarcyt-01'), ('Vittoria White', 'w-kwarcyt-02'), ('Navona', 'w-kwarcyt-03'), ('Blanco Paloma', 'w-kwarcyt-04'), ('Gris Ceniza', 'w-kwarcyt-06'), ('Black Nimbus', 'w-kwarcyt-07'), ('City Dark', 'w-kwarcyt-08'), ('Gris Antracita', 'w-kwarcyt-09'), ('Black Mamba', 'w-kwarcyt-10')],
    'w-marmur': [('Polare', 'w-marmur-01'), ('Monte Bianco', 'w-marmur-02'), ('Bianco Carrara', 'w-marmur-03'), ('Perla Arte', 'w-marmur-04'), ('Beige Marfil', 'w-marmur-05'), ('Marmo White', 'w-marmur-06'), ('Baltic Grey', 'w-marmur-07'), ('Crystal White', 'w-marmur-08'), ('Botticino', 'w-marmur-09'), ('Breccia Aurora', 'w-marmur-10'), ('Calacatta Gold', 'w-marmur-11'), ('Perlato Appia', 'w-marmur-12'), ('Rosso Asiago', 'w-marmur-13'), ('Beige Luna', 'w-marmur-14'), ('Giorgione', 'w-marmur-15'), ('White Iceberg', 'w-marmur-16'), ('Cotone', 'w-marmur-18')],
    'w-fornir': [('Dąb naturalny', 'w-fornir-01'), ('Winchester', 'w-fornir-02'), ('Złoty dąb', 'w-fornir-03'), ('Dąb orzech', 'w-fornir-04'), ('Stary złoty dąb', 'w-fornir-05'), ('Dąb orzech ciemny', 'w-fornir-06'), ('Dąb mahoń', 'w-fornir-07'), ('Dąb bielony', 'w-fornir-08'), ('Dąb grafit', 'w-fornir-09')],
    'w-laminat': [('Cream Beige', 'w-laminat-01'), ('Subtle Nude', 'w-laminat-02'), ('Subtle Taupe', 'w-laminat-03'), ('Biały mat', 'w-laminat-04'), ('Biały połysk', 'w-laminat-05'), ('Marmur jasny', 'w-laminat-06'), ('Beton ciemny', 'w-laminat-07'), ('Granit szary', 'w-laminat-08'), ('Dąb Ribbeck', 'w-laminat-09'), ('Jasny dąb', 'w-laminat-10'), ('Dąb Sonoma', 'w-laminat-11'), ('Dąb naturalny', 'w-laminat-12'), ('Orzech Lanzado', 'w-laminat-13'), ('Winchester', 'w-laminat-14'), ('Beton', 'w-laminat-15'), ('Dąb vintage', 'w-laminat-16'), ('Białe drewno', 'w-laminat-17'), ('Dąb Watan', 'w-laminat-18'), ('Dąb London', 'w-laminat-19'), ('Dąb Argos', 'w-laminat-20'), ('Jabłoń', 'w-laminat-21'), ('Złoty dąb', 'w-laminat-22'), ('Antracyt', 'w-laminat-23')],
    'w-lakier': [('Perła łuska', 'w-lakier-01'), ('Biały mat', 'w-lakier-02'), ('Biały połysk', 'w-lakier-03'), ('Biały wysoki połysk', 'w-lakier-04'), ('Czarny mat', 'w-lakier-05'), ('Marmurek czarny', 'w-lakier-06'), ('Marmurek biały', 'w-lakier-07'), ('Antracyt RAL 7016 półmat', 'w-lakier-08')],
    'w-pcv': [('Biały', 'w-pcv-01'), ('Marmur', 'w-pcv-02'), ('Orzech', 'w-pcv-03'), ('Złoty dąb', 'w-pcv-04'), ('Dąb skandynawski', 'w-pcv-05'), ('Grafit', 'w-pcv-07')],
    'z-granit': [('Vanga', 'z-granit-01'), ('Blue Night', 'z-granit-02'), ('Colonial White', 'z-granit-03'), ('Royal Black', 'z-granit-04'), ('Nero Impala', 'z-granit-05'), ('Tan Brown', 'z-granit-06'), ('China Cristal', 'z-granit-07'), ('Steel Grey', 'z-granit-08'), ('Yellow Pink', 'z-granit-09'), ('Rosa Beta', 'z-granit-10'), ('Imperial White', 'z-granit-11')],
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
    ("Kiedy najlepiej zamontować parapety zewnętrzne?",
     "Parapety zewnętrzne najlepiej zamontować na etapie ocieplania elewacji, przed wykonaniem końcowej warstwy tynku. Pozwala to prawidłowo osadzić parapet, wykonać szczelne połączenia i ograniczyć ryzyko przedostawania się wody pod ocieplenie."),
]


def build_parapety():
    def grupa(key, title, lead):
        typy = PARAPETY_TYPY[key]
        cards = "".join(f"""<article class="sill-card">
        <a href="assets/img/parapety/{k}.jpg" data-lightbox-item><img src="assets/img/parapety/{k}.jpg" alt="{title} — {n.lower()}" loading="lazy"></a>
        <div><h3>{n}</h3><p>{d}</p><small>{t}</small></div>
      </article>""" for k, n, d, t in typy)
        tabs = '<div class="chips chips--tabs" role="tablist">' + "".join(
            f'<button type="button" class="{"is-active" if i == 0 else ""}" data-filter-btn="{k}">{n}</button>'
            for i, (k, n, _d, _t) in enumerate(typy)) + "</div>"
        grid = '<div class="sill-swatches" data-filter-grid data-lightbox>' + "".join(
            f'<a href="assets/img/parapety/kolor-{f}-lg.jpg" data-lightbox-item data-caption="{_n} — {n}" data-filter="{k}"{"" if i == 0 else " hidden"}><img src="assets/img/parapety/kolor-{f}.jpg" alt="{_n} — {n}" loading="lazy"><span>{n}</span></a>'
            for i, (k, _n, _d, _t) in enumerate(typy) for n, f in PARAPETY_KOLORY[k]) + "</div>"
        return f"""<div class="section-header"><div class="section-header__left"><h2 class="h-sec">{title}</h2></div></div>
    <p class="sill-lead">{lead}</p>
    <div class="sill-types{" sill-types--3" if len(typy) % 3 == 0 else ""}" data-lightbox>{cards}</div>
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

    body = pagehero("parapety/hero-parapet", "Parapety Jaro-Max – praktyczne i piękne wykończenie okna",
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
          + nav("parapety") + body.replace('<section class="pagehero">', '<section class="pagehero pagehero--sill">', 1) + footer())


# ================================================================ PERGOLE (uwagi klienta 20.10.2026) ----
PERG_ROWS = [
    ("Pergola SB400",
     ["Lamele aluminiowe sterowane elektrycznie w zakresie 0–120°",
      "Konstrukcja z profili aluminiowych, przekrój słupa 85 mm x 150 mm",
      "Wbudowany system odprowadzania wody",
      "Możliwość zastosowania oświetlenia LED",
      "Sterowanie za pomocą pilota, istnieje możliwość podłączenia pod smart home",
      "W standardzie występuje w trzech kolorach: białym, grafitowym i antracytowym. Istnieje również możliwość zamówienia pergoli w innym wybranym kolorze z palety RAL.",
      "Możliwość wykonania na indywidualny wymiar"], "perg/sb400"),
    ("Pergola SB350",
     ["Lamele aluminiowe sterowane elektrycznie w zakresie 0–120°",
      "Konstrukcja z profili aluminiowych, przekrój słupa 85 mm x 150 mm",
      "Wbudowany system odprowadzania wody",
      "Sterowanie za pomocą pilota, istnieje możliwość podłączenia pod smart home",
      "Występuje w dwóch kolorach: białym i antracytowym.",
      "Dostępna wyłącznie w określonych wariantach wymiarowych"], "perg/sb350"),
    ("Pergola SB400R",
     ["Moduł dachowy z ramą",
      "Produkt przeznaczony do montażu na istniejącej zabudowie, bez własnej konstrukcji nośnej",
      "Lamele z aluminium o regulacji 0–120°",
      "Sterowanie za pomocą pilota, istnieje możliwość podłączenia pod smart home",
      "W standardzie występuje w trzech kolorach: białym, grafitowym i antracytowym. Istnieje również możliwość zamówienia w innym wybranym kolorze z palety RAL.",
      "Możliwość wykonania na indywidualny wymiar"], "perg/sb400r"),
]
PERG_ADV = [("Regulacja", "Lamele obrotowe 0–120° — dozowanie światła i wentylacji", "sun"),
            ("Wytrzymałość", "Aluminium ekstrudowane, odporność na silny wiatr", "shield"),
            ("Rozbudowa", "Screeny ZIP, przeszklenia i oświetlenie LED", "cog")]
PERG_FAQ = [
    ("Czy pergola chroni przed deszczem i słońcem?",
     "Tak, pergole Aluprof Sun Shading Solutions zapewniają ochronę przed słońcem, a dzięki ruchomym lamelom dachowym pozwalają regulować ilość światła docierającego na taras. Po zamknięciu lameli dach tworzy osłonę przed deszczem, a odpowiednio zaprojektowany system odprowadzania wody pomaga odprowadzić ją poza zadaszoną przestrzeń. Dzięki temu możesz korzystać z tarasu w różnych warunkach pogodowych."),
    ("W jakich wymiarach dostępne są pergole?",
     "Pergola SB 350 występuje w standardowych wymiarach: szerokość 3,5 m, a do wyboru są cztery wysięgi: 3,6 m, 4,0 m, 4,4 m oraz 4,8 m. Pergola SB 400 może zostać wykonana na indywidualny wymiar - pojedynczy moduł może mieć szerokość do 4 m i wysięg do 7 m."),
    ("Czy pergolę można zamontować przy istniejącym tarasie?",
     "Tak, pergolę można zamontować przy istniejącym tarasie. Przed montażem należy jednak sprawdzić, czy podłoże jest odpowiednio stabilne i wytrzymałe, aby zapewnić bezpieczne zamocowanie konstrukcji. Sposób montażu dobieramy do warunków na miejscu oraz możliwości technicznych."),
    ("Czy do pergoli można zamontować osłony boczne?",
     "Tak, pergole można wyposażyć w dodatkowe osłony boczne, które zwiększają komfort korzystania z tarasu. Do wyboru są m.in. refleksole typu ZIP, chroniące przed słońcem i wiatrem."),
    ("Pergola SB 350 a SB 400 – czym się różnią?",
     "Główna różnica polega na możliwościach dopasowania wymiarów i sposobie montażu. SB 350 to model o standardowych wymiarach, natomiast SB 400 można wykonać na indywidualny wymiar."),
    ("Czy na dachu pergoli gromadzi się woda deszczowa?",
     "Nie, przy prawidłowo działającym systemie odwodnienia woda deszczowa nie powinna zalegać na dachu pergoli. Po zamknięciu lameli woda spływa do zintegrowanych rynien, a następnie jest odprowadzana przez system odpływowy ukryty w konstrukcji."),
]
PERG_INSPIRACJE = [f"perg/insp-{i:02d}" for i in (1, 2, 3, 4, 13, 6, 7, 8, 9, 10, 11, 12)]  # 05 = V ZiiiP, nie w ofercie


def build_pergole():
    rows = ""
    for k, (title, bullets, img) in enumerate(PERG_ROWS):
        li = "".join(f'<li><span class="check">{I["check"]}</span> {b}</li>' for b in bullets)
        media = f'<div><img src="assets/img/{img}.jpg" alt="{title} — Aluprof Sun Shading Solutions" loading="lazy"></div>'
        text = f"""<div class="subrow__text">
        <h2>{title}</h2>
        <ul class="bullets">{li}</ul>
        <a class="btn btn--primary btn--sm" href="kontakt.html">Zapytaj o wycenę {I['arrow']}</a>
      </div>"""
        flip = k % 2
        rows += f'<div class="subrow{" subrow--flip" if flip else ""}">{media if not flip else text}{text if not flip else media}</div>'

    adv = "".join(f"""<div class="adv"><span class="adv__icon">{I[ic]}</span>
      <div><h3>{t}</h3><p>{d}</p></div></div>""" for t, d, ic in PERG_ADV)
    faq = "".join(f"""<div class="faq__row">
      <button class="faq__q"><span>{q}</span><span>+</span></button>
      <div class="faq__a"><p>{a}</p></div>
    </div>""" for q, a in PERG_FAQ)
    insp = '<div class="gallery gallery--okna" data-lightbox>' + "".join(
        f'<a href="assets/img/{g}.jpg" data-lightbox-item><img src="assets/img/{g}.jpg" alt="Pergola Aluprof Sun Shading Solutions — inspiracja" loading="lazy"></a>'
        for g in PERG_INSPIRACJE) + "</div>"
    rel = ""
    for sl in ["markizy", "oslony-zewnetrzne", "rolety-zewnetrzne"]:
        rel += f"""<a href="{sl}.html"><article class="card">
        <img src="assets/img/{PROD_IMG[sl]}.jpg" alt="{PROD_LABEL[sl]}" style="height:150px;object-fit:cover;border-radius:var(--r-md)">
        <div><h3>{PROD_LABEL[sl]}</h3></div>
        <span class="card__more">Zobacz ofertę {I['arrow']}</span>
      </article></a>"""

    body = pagehero("perg/hero", "Pergole Aluprof Sun Shading Solutions",
                    "Wyposażone w ruchome lamele dachowe, umożliwiają regulację ilości światła słonecznego. Więcej cienia, więcej komfortu i więcej przyjemności z wypoczynku na tarasie.", None)
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

{cta("Doradztwo i wycena", "Planujesz zadaszenie tarasu?",
     "Skontaktuj się z nami — doradzimy technicznie i przygotujemy kalkulację cenową.")}

<section class="section related">
  <div class="container">
    <h2 class="h-sec" style="margin-bottom:32px">Sprawdź również inne systemy</h2>
    <div class="grid-3">{rel}</div>
  </div>
</section>
"""
    write("pergole.html", head("Pergole Aluprof Sun Shading Solutions — SB400, SB350, SB400R | PROMYK Wieluń",
                               "Pergole lamelowe Aluprof Sun Shading Solutions: SB400, SB350 i moduł dachowy SB400R. Lamele 0–120°, odprowadzanie wody, LED, smart home — PROMYK Wieluń.")
          + nav("pergole") + body + footer())


# ================================================================ BRAMY GARAŻOWE (uwagi klienta 21.10.2026) ----
BR_AVO_KOLORY = [('podst', 'RAL 7016', 'avo-kolor-01'), ('podst', 'RAL 9016', 'avo-kolor-02'), ('pref', '703M', 'avo-kolor-03'), ('pref', 'RAL 8014', 'avo-kolor-04'), ('pref', 'RAL 9005', 'avo-kolor-05'), ('pref', 'RAL 9006', 'avo-kolor-06'), ('pref', 'RAL 9007', 'avo-kolor-07'), ('avo', 'Antracyt okienny', 'avo-kolor-08'), ('avo', 'Orzech', 'avo-kolor-09'), ('avo', 'Złoty dąb', 'avo-kolor-10'), ('g1', 'Antracyt gładki', 'avo-kolor-11'), ('g1', 'Brąz czekoladowy', 'avo-kolor-12'), ('g1', 'Cedr szary / Dąb antyczny', 'avo-kolor-13'), ('g1', 'Espresso Ash 3D', 'avo-kolor-14'), ('g1', 'Złoty dąb jasny', 'avo-kolor-15'), ('g1', 'Ciemny dąb', 'avo-kolor-16'), ('g1', 'Dąb bagienny', 'avo-kolor-17'), ('g1', 'Dąb naturalny', 'avo-kolor-18'), ('g1', 'Mahoń', 'avo-kolor-19'), ('g1', 'Sosna antyczna', 'avo-kolor-20'), ('g1', 'Szary', 'avo-kolor-21'), ('g1', 'Winchester', 'avo-kolor-22'), ('g1', 'Bazaltowoszary', 'avo-kolor-23'), ('g2', 'Antracytowoszary mat', 'avo-kolor-24'), ('g2', 'Beżowoszary mat', 'avo-kolor-25'), ('g2', 'Kasztanowy brąz mat', 'avo-kolor-26'), ('g2', 'Zielonoszary mat', 'avo-kolor-27'), ('g2', 'Antracyt szczotkowany', 'avo-kolor-28'), ('g2', 'Biały mat', 'avo-kolor-29'), ('g2', 'Czarny mat', 'avo-kolor-30'), ('g2', 'Dąb czarny palony', 'avo-kolor-31'), ('g2', 'Dąb Shefield', 'avo-kolor-32'), ('g2', 'Kremowy gładki', 'avo-kolor-33'), ('g2', 'Szary mat', 'avo-kolor-34'), ('g2', 'Umbra brąz mat', 'avo-kolor-35'), ('g2', 'Ciemnoszary mat DB 703', 'avo-kolor-36'), ('g2', 'Woodec Dąb Turner Malt', 'avo-kolor-37'), ('g2', 'Woodec Dąb Turner Toffee', 'avo-kolor-38'), ('g2', 'Woodec Sosna Jura', 'avo-kolor-39'), ('g2', 'Kwarcowoszary gładki', 'avo-kolor-40')]
BR_AVO_GRUPY = [("podst", "Podstawowe"), ("pref", "Preferowane"), ("avo", "Dekory AVO"), ("g1", "Dekory grupa I"), ("g2", "Dekory grupa II")]
BR_ROL_KOLORY = [("bialy", "Biały"), ("srebrny", "Srebrny"), ("brazowy", "Brązowy"), ("ciemnobrazowy", "Ciemnobrązowy"),
                 ("antracyt", "Szary antracyt"), ("szary", "Szary"), ("zloty-dab", "Złoty dąb"), ("orzech", "Orzech")]
BR_ROWS = [
    ("Bramy segmentowe",
     ["Panel o grubości 40 lub 60mm wypełniony pianką poliuretanową",
      "Sposób otwierania – brama unosi się pionowo i przesuwa pod sufitem",
      "Otwieranie ręczne lub automatyczne",
      "Szeroki wybór wykończeń i kolorów"], "brama_antracyt_lampy", "bramy-garazowe--bramy-segmentowe"),
    ("Bramy rolowane",
     ["Pancerz aluminiowy z pianką PU nawijany na wał w skrzynce",
      "Możliwość montażu skrzynki z pancerzem po wewnętrznej lub zewnętrznej stronie garażu",
      "Napęd rurowy z awaryjnym otwieraniem korbą w standardzie",
      "Brak prowadnic pod sufitem sprawia, że brama sprawdza się w garażach z ograniczoną przestrzenią."], "bramy/rolowane-aluprof", "bramy-garazowe--bramy-rolowane"),
]
BR_ADV = [("Ciepło i komfort", "Panele i pancerze wypełnione pianką poliuretanową", "thermo"),
          ("Bezpieczeństwo", "Solidna konstrukcja i zabezpieczenia na co dzień", "lock"),
          ("Wygodna obsługa", "Ręcznie, pilotem lub z aplikacji smart home", "cog")]
BR_POROWNANIE = [
    ["Sposób otwierania", "Brama unosi się pionowo i przesuwa pod sufitem", "Pancerz zwija się do skrzynki nad otworem"],
    ["Konstrukcja", "Panele 40 lub 60 mm wypełnione pianką poliuretanową", "Profile aluminiowe PA 77 wypełnione pianką poliuretanową"],
    ["Izolacja termiczna", "Bardzo dobra", "Dobra"],
    ["Montaż", "Wewnątrz garażu, na prowadnicach", "Skrzynka po wewnętrznej lub zewnętrznej stronie garażu"],
    ["Obsługa", "Ręczna lub automatyczna — napęd paskowy", "Napęd rurowy z awaryjnym otwieraniem korbą"],
]
BR_FAQ = [
    ("Jaką bramę wybrać - segmentową czy rolowaną?",
     "Bramy segmentowe zapewniają bardzo dobrą izolację termiczną i szerokie możliwości dopasowania do wyglądu budynku, ale wymagają odpowiedniej przestrzeni pod sufitem i nad otworem. Bramy rolowane zajmują mniej miejsca, ponieważ pancerz chowa się w skrzynce nad wjazdem. To praktyczna opcja przy niskim nadprożu lub ograniczonej przestrzeni w garażu."),
    ("Czy bramę garażową można dopasować kolorystycznie do okien i drzwi?",
     "Tak, bramę garażową można dopasować kolorystycznie do okien, drzwi i pozostałych elementów stolarki. Dostępna paleta kolorów, różne struktury powierzchni oraz wzory pozwalają stworzyć spójną aranżację elewacji i podkreślić styl budynku."),
    ("Czy brama garażowa może być wyposażona w przeszklenia?",
     "Tak, wybrane modele bram garażowych można wyposażyć w przeszklenia, które doświetlają wnętrze garażu naturalnym światłem. Dostępne są różne kształty i układy przeszkleń, dzięki czemu można dopasować ich wygląd do stylu budynku."),
    ("Jak przygotować garaż do montażu bramy segmentowej?",
     "Przed montażem bramy garażowej należy odpowiednio przygotować otwór – ściany po bokach i nadproże powinny być równe, stabilne i wykończone zgodnie z wymaganiami montażowymi. Warto również sprawdzić wymiary otworu oraz zapewnić wolną przestrzeń w garażu, niezbędną do prawidłowego montażu bramy."),
    ("Co zrobić, gdy zabraknie prądu?",
     "W przypadku braku prądu bramę rolowaną można otworzyć korbą, korzystając z mechanizmu awaryjnego. Natomiast bramę segmentową można otworzyć ręcznie od środka. Jeśli nie ma innego wejścia do garażu, warto przy zakupie bramy dokupić dodatkową opcję: akumulator bądź wysprzęglenie awaryjne pozwalające otworzyć bramę z zewnątrz."),
    ("Jaka brama garażowa sprawdzi się w garażu ogrzewanym?",
     "W ogrzewanym garażu najlepiej sprawdzi się brama segmentowa z panelami o dobrych właściwościach termoizolacyjnych."),
]
BR_INSPIRACJE = ["brama_antracyt", "bramy/insp-nice-1", "bramy/insp-avo-garaz", "bramy/insp-nice-2",
                 "bramy/insp-aluprof-dom", "realizacje/bramy", "brama_avo_dom", "bramy/segmentowe-wnetrze"]



def _anim_section(svg, h2, txt, soft=False):
    return f"""<section class="section{' section--soft' if soft else ''}">
  <div class="container">
    <div class="garage-anim-wrap">
      <div>{svg}</div>
      <div class="subrow__text prose-text">
        <h2>{h2}</h2>
        <p>{txt}</p>
      </div>
    </div>
  </div>
</section>
"""


def _okno_anim():
    """Okno RU: klamka w poziomie — rozwarcie, klamka w górę — uchył (SVG/SMIL)."""
    kt = "0;0.08;0.14;0.3;0.4;0.52;0.58;0.64;0.76;0.86;0.94;1"
    closed = "200,60 440,60 440,300 200,300"
    turn = "200,60 330,84 330,276 200,300"
    tilt = "214,96 426,96 440,300 200,300"
    pts = ";".join([closed, closed, closed, turn, turn, closed, closed, closed, tilt, tilt, closed, closed])
    hx = ";".join(["0 0"] * 3 + ["-104 0"] * 2 + ["0 0"] * 7)
    rot = ";".join(f"{a} 425 182" for a in [0, 0, 90, 90, 90, 90, 90, 180, 180, 180, 180, 0])
    vis = lambda on: ";".join("1" if x else "0" for x in on)
    return f"""<svg class="garage-anim" viewBox="0 0 640 360" role="img" aria-label="Animacja: okno rozwierno-uchylne — rozwarcie i uchył">
  <rect x="186" y="46" width="268" height="268" rx="3" class="ow-frame"/>
  <rect x="200" y="60" width="240" height="240" class="ow-hole"/>
  <polygon class="ow-sash" points="{closed}"><animate attributeName="points" values="{pts}" keyTimes="{kt}" dur="12s" repeatCount="indefinite"/></polygon>
  <g><animateTransform attributeName="transform" type="translate" values="{hx}" keyTimes="{kt}" dur="12s" repeatCount="indefinite"/>
    <g><animateTransform attributeName="transform" type="rotate" values="{rot}" keyTimes="{kt}" dur="12s" repeatCount="indefinite"/>
      <rect x="421" y="176" width="8" height="12" rx="2" class="ow-handle"/><rect x="422" y="182" width="6" height="34" rx="3" class="ow-handle"/>
    </g>
  </g>
  <rect x="176" y="314" width="288" height="10" rx="2" class="ga-wall"/>
  <text x="480" y="120" class="ga-label">rozwarcie<animate attributeName="opacity" values="{vis([0,0,1,1,1,1,0,0,0,0,0,0])}" keyTimes="{kt}" dur="12s" repeatCount="indefinite"/></text>
  <text x="480" y="120" class="ga-label" opacity="0">uchył<animate attributeName="opacity" values="{vis([0,0,0,0,0,0,0,1,1,1,1,0])}" keyTimes="{kt}" dur="12s" repeatCount="indefinite"/></text>
  <text x="480" y="150" class="ga-label ga-label--sm">klamka poziomo:</text>
  <text x="480" y="166" class="ga-label ga-label--sm">rozwarcie</text>
  <text x="480" y="190" class="ga-label ga-label--sm">klamka w górę:</text>
  <text x="480" y="206" class="ga-label ga-label--sm">uchył</text>
  <text x="40" y="345" class="ga-label">widok od wewnątrz</text>
</svg>"""


def _roleta_anim():
    """Roleta zewnętrzna: pancerz zjeżdża w prowadnicach, w pokoju robi się wieczór (SVG/SMIL)."""
    kt = "0;0.15;0.45;0.65;0.95;1"
    ys = "-236;-236;0;0;-236;-236"
    return f"""<svg class="garage-anim" viewBox="0 0 640 360" role="img" aria-label="Animacja: roleta zewnętrzna opuszcza się i podnosi">
  <defs>
    <pattern id="rlSlat" width="20" height="13" patternUnits="userSpaceOnUse"><rect width="20" height="13" fill="#8d949b"/><rect y="10.5" width="20" height="2.5" fill="#5e656c"/></pattern>
    <clipPath id="rlClip"><rect x="206" y="66" width="228" height="236"/></clipPath>
  </defs>
  <rect x="150" y="20" width="340" height="310" class="rl-wall"/>
  <rect x="206" y="66" width="228" height="236" class="rl-glass"><animate attributeName="fill" values="#cfe3f0;#cfe3f0;#f3c56b;#f3c56b;#cfe3f0;#cfe3f0" keyTimes="{kt}" dur="10s" repeatCount="indefinite"/></rect>
  <path d="M320 66v236M206 184h228" stroke="#3a3f45" stroke-width="6"/>
  <g clip-path="url(#rlClip)"><rect x="206" y="66" width="228" height="236" fill="url(#rlSlat)"><animateTransform attributeName="transform" type="translate" values="0 -236;0 -236;0 0;0 0;0 -236;0 -236" keyTimes="{kt}" dur="10s" repeatCount="indefinite"/></rect>
    <rect x="206" y="296" width="228" height="6" fill="#3a3f45"><animateTransform attributeName="transform" type="translate" values="0 -236;0 -236;0 0;0 0;0 -236;0 -236" keyTimes="{kt}" dur="10s" repeatCount="indefinite"/></rect></g>
  <rect x="196" y="40" width="248" height="28" rx="3" class="ga-motor"/>
  <rect x="196" y="66" width="10" height="240" class="rl-guide"/><rect x="434" y="66" width="10" height="240" class="rl-guide"/>
  <rect x="190" y="304" width="260" height="8" rx="2" class="ga-wall"/>
  <circle cx="560" cy="60" r="24" class="sb-sun"><animate attributeName="opacity" values="1;1;.15;.15;1;1" keyTimes="{kt}" dur="10s" repeatCount="indefinite"/></circle>
  <text x="456" y="58" class="ga-label ga-label--sm">skrzynka z napędem</text>
  <text x="456" y="200" class="ga-label ga-label--sm">prowadnice</text>
  <text x="456" y="220" class="ga-label ga-label--sm">pancerz aluminiowy</text>
  <text x="40" y="345" class="ga-label">dzień → wieczór: pełne zaciemnienie i prywatność</text>
</svg>"""


def _markiza_anim():
    """Markiza tarasowa w przekroju: ramiona łamane wysuwają tkaninę, na tarasie rośnie cień (SVG/SMIL)."""
    kt = "0;0.12;0.42;0.66;0.94;1"
    arm = ";".join(["124,108 140,104 156,100"] * 2 + ["124,108 330,150 520,150"] * 2 + ["124,108 140,104 156,100"] * 2)
    fab = ";".join(["124,92 156,100"] * 2 + ["124,92 520,150"] * 2 + ["124,92 156,100"] * 2)
    return f"""<svg class="garage-anim" viewBox="0 0 640 360" role="img" aria-label="Animacja: markiza tarasowa rozwija się nad tarasem">
  <rect x="96" y="30" width="28" height="290" class="ga-wall"/>
  <line x1="40" y1="320" x2="620" y2="320" class="ga-ground"/>
  <rect x="150" y="314" width="0" height="10" rx="4" class="mk-shadow"><animate attributeName="width" values="0;0;380;380;0;0" keyTimes="{kt}" dur="11s" repeatCount="indefinite"/></rect>
  <polyline class="mk-fabric" points="124,92 156,100"><animate attributeName="points" values="{fab}" keyTimes="{kt}" dur="11s" repeatCount="indefinite"/></polyline>
  <polyline class="mk-arm" points="124,108 140,104 156,100"><animate attributeName="points" values="{arm}" keyTimes="{kt}" dur="11s" repeatCount="indefinite"/></polyline>
  <rect x="120" y="82" width="34" height="22" rx="5" class="ga-motor"/>
  <g class="mk-chair"><path d="M392 320v-46h44v46M380 280h68" fill="none" stroke="#6b737b" stroke-width="5" stroke-linecap="round"/><path d="M470 320v-30h28v30M460 290h50" fill="none" stroke="#6b737b" stroke-width="5" stroke-linecap="round"/></g>
  <circle cx="575" cy="58" r="24" class="sb-sun"/>
  <path class="sb-ray" d="M556 76 476 156M548 66 420 196"><animate attributeName="opacity" values=".8;.8;.15;.15;.8;.8" keyTimes="{kt}" dur="11s" repeatCount="indefinite"/></path>
  <text x="160" y="76" class="ga-label ga-label--sm">kaseta</text>
  <text x="300" y="196" class="ga-label ga-label--sm">ramiona łamane</text>
  <text x="40" y="345" class="ga-label">cień na tarasie — dokładnie tam, gdzie go potrzebujesz</text>
</svg>"""


def _plisa_anim():
    """Moskitiera plisowana: siatka rozkłada się w otworze HST, owady zostają na zewnątrz, powietrze przepływa (SVG/SMIL)."""
    kt = "0;0.12;0.42;0.66;0.94;1"
    flies = ""
    for i, (x, y, d) in enumerate([(70, 120, 0), (110, 200, 1.3), (60, 260, 2.1), (130, 90, .7)]):
        flies += (f'<circle r="3.5" class="ms-fly"><animateMotion dur="{3.2 + i * .6:.1f}s" begin="{d}s" repeatCount="indefinite" '
                  f'path="M{x},{y} q50,-30 80,10 q-30,40 -80,-10"/></circle>')
    return f"""<svg class="garage-anim" viewBox="0 0 640 360" role="img" aria-label="Animacja: moskitiera plisowana zamyka otwór drzwi tarasowych">
  <defs>
    <pattern id="msMesh" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0 0h6M0 0v6" stroke="#5d646b" stroke-width=".7"/></pattern>
    <pattern id="msPleat" width="14" height="10" patternUnits="userSpaceOnUse"><path d="M0 0h7M7 0v10" stroke="#5d646b" stroke-width="1"/></pattern>
  </defs>
  <rect x="190" y="40" width="300" height="280" class="rl-glass"/>
  <rect x="180" y="30" width="320" height="10" class="ga-motor"/><rect x="180" y="320" width="320" height="6" class="ga-motor"/>
  <rect x="180" y="30" width="10" height="296" class="ga-motor"/><rect x="490" y="30" width="10" height="296" class="ga-motor"/>
  <rect x="190" y="40" width="8" height="280" fill="url(#msMesh)" opacity=".9"><animate attributeName="width" values="8;8;292;292;8;8" keyTimes="{kt}" dur="10s" repeatCount="indefinite"/></rect>
  <rect x="190" y="40" width="8" height="280" fill="url(#msPleat)" opacity=".35"><animate attributeName="width" values="8;8;292;292;8;8" keyTimes="{kt}" dur="10s" repeatCount="indefinite"/></rect>
  <rect x="194" y="40" width="8" height="280" rx="2" class="ow-handle"><animate attributeName="x" values="194;194;478;478;194;194" keyTimes="{kt}" dur="10s" repeatCount="indefinite"/></rect>
  <path class="ms-air" d="M60 170H600M60 230H600"/>
  {flies}
  <text x="40" y="30" class="ga-label ga-label--sm">na zewnątrz</text>
  <text x="520" y="30" class="ga-label ga-label--sm">wnętrze</text>
  <text x="40" y="345" class="ga-label">siatka zatrzymuje owady, a powietrze swobodnie przepływa</text>
</svg>"""


def _bramy_anim():
    """Przekrój garażu: segmenty bramy jadą prowadnicą w górę i pod sufit (SVG/SMIL)."""
    L = 320 + 3.14159 * 40 / 2 + 200      # długość prowadnicy (poziom + łuk + pion)
    segs = ""
    for i in range(4):
        closed = (L - 25 - 50 * i) / L
        opened = (L - 25 - 50 * i - 380) / L
        kp = f"{closed:.4f};{closed:.4f};{opened:.4f};{opened:.4f};{closed:.4f};{closed:.4f}"
        segs += (f'<rect class="ga-seg" x="-24" y="-6" width="48" height="12" rx="2">'
                 f'<animateMotion dur="10s" repeatCount="indefinite" rotate="auto" calcMode="spline" keyPoints="{kp}" '
                 f'keyTimes="0;0.12;0.45;0.6;0.93;1" keySplines="0 0 1 1;.45 0 .25 1;0 0 1 1;.45 0 .25 1;0 0 1 1">'
                 f'<mpath href="#ga-track"/></animateMotion></rect>')
    return f"""<svg class="garage-anim" viewBox="0 0 640 360" role="img" aria-label="Animacja: brama segmentowa unosi się pionowo i przesuwa pod sufitem">
  <path id="ga-track" d="M500,80 L180,80 A40,40 0 0 0 140,120 L140,320" class="ga-track"/>
  <line x1="40" y1="320" x2="600" y2="320" class="ga-ground"/>
  <rect x="104" y="40" width="16" height="70" class="ga-wall"/>
  <line x1="120" y1="56" x2="600" y2="56" class="ga-ceiling"/>
  <rect x="104" y="30" width="496" height="10" class="ga-wall"/>
  <rect x="510" y="60" width="64" height="14" rx="3" class="ga-motor"/>
  <line x1="180" y1="67" x2="510" y2="67" class="ga-belt"/>
  {segs}
  <text x="60" y="345" class="ga-label">na zewnątrz</text>
  <text x="380" y="345" class="ga-label">wnętrze garażu</text>
  <text x="330" y="108" class="ga-label ga-label--sm">prowadnica pod sufitem</text>
  <text x="518" y="96" class="ga-label ga-label--sm">napęd paskowy</text>
</svg>"""


def _br_related(cur):
    out = ""
    for slug, title, img in [("bramy-garazowe--bramy-segmentowe", "Bramy segmentowe", "brama_antracyt_lampy"),
                             ("bramy-garazowe--bramy-rolowane", "Bramy rolowane", "bramy/rolowane-aluprof"),
                             ("bramy-garazowe", "Wszystkie bramy garażowe", "bramy/hero")]:
        if slug == cur: continue
        out += f"""<a href="{slug}.html"><article class="card">
        <img src="assets/img/{img}.jpg" alt="{title}" style="height:150px;object-fit:cover;border-radius:var(--r-md)" loading="lazy">
        <div><h3>{title}</h3></div>
        <span class="card__more">Zobacz {I['arrow']}</span>
      </article></a>"""
    return out


def build_bramy():
    # ---- strona główna kategorii
    rows = ""
    for k, (title, bullets, img, more) in enumerate(BR_ROWS):
        li = "".join(f'<li><span class="check">{I["check"]}</span> {b}</li>' for b in bullets)
        media = f'<div><img src="assets/img/{img}.jpg" alt="{title}" loading="lazy"></div>'
        text = f"""<div class="subrow__text">
        <h2>{title}</h2>
        <ul class="bullets">{li}</ul>
        <div style="display:flex;gap:12px;flex-wrap:wrap">
          <a class="btn btn--primary btn--sm" href="{more}.html">Więcej o tym rozwiązaniu {I['arrow']}</a>
          <a class="btn btn--outline btn--sm" href="kontakt.html">Zapytaj o wycenę {I['arrow']}</a>
        </div>
      </div>"""
        flip = k % 2
        rows += f'<div class="subrow{" subrow--flip" if flip else ""}">{media if not flip else text}{text if not flip else media}</div>'
    adv = "".join(f"""<div class="adv"><span class="adv__icon">{I[ic]}</span>
      <div><h3>{t}</h3><p>{d}</p></div></div>""" for t, d, ic in BR_ADV)
    th = "".join(f"<th>{c}</th>" for c in ["", "Brama segmentowa", "Brama rolowana"])
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in BR_POROWNANIE)
    faq = "".join(f"""<div class="faq__row">
      <button class="faq__q"><span>{q}</span><span>+</span></button>
      <div class="faq__a"><p>{a}</p></div>
    </div>""" for q, a in BR_FAQ)
    insp = '<div class="gallery gallery--okna" data-lightbox>' + "".join(
        f'<a href="assets/img/{g}.jpg" data-lightbox-item><img src="assets/img/{g}.jpg" alt="Brama garażowa — inspiracja" loading="lazy"></a>'
        for g in BR_INSPIRACJE) + "</div>"
    rel = ""
    for sl in ["drzwi-zewnetrzne", "okna", "rolety-zewnetrzne"]:
        rel += f"""<a href="{sl}.html"><article class="card">
        <img src="assets/img/{PROD_IMG[sl]}.jpg" alt="{PROD_LABEL[sl]}" style="height:150px;object-fit:cover;border-radius:var(--r-md)">
        <div><h3>{PROD_LABEL[sl]}</h3></div>
        <span class="card__more">Zobacz ofertę {I['arrow']}</span>
      </article></a>"""
    body = pagehero("bramy/hero-brama", "Bramy garażowe segmentowe i rolowane",
                    "Nowoczesne rozwiązania, które łączą wygodę użytkowania, estetykę i bezpieczeństwo Twojego garażu.", None)
    body += f"""<section class="section section--tight-bottom"><div class="container">{rows}</div></section>
<section class="advantages"><div class="container advantages__inner">{adv}</div></section>

<section class="section section--soft">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Brama segmentowa czy rolowana?</h2></div></div>
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
    {insp}
  </div>
</section>

{cta("Doradztwo i wycena", "Planujesz nową bramę garażową?",
     "Skontaktuj się z nami — doradzimy technicznie i przygotujemy kalkulację cenową.")}

<section class="section related">
  <div class="container">
    <h2 class="h-sec" style="margin-bottom:32px">Sprawdź również inne systemy</h2>
    <div class="grid-3">{rel}</div>
  </div>
</section>
"""
    body = body.replace('<section class="pagehero">', '<section class="pagehero pagehero--low">', 1)
    write("bramy-garazowe.html", head("Bramy garażowe segmentowe i rolowane — AVO i Aluprof | PROMYK Wieluń",
                                      "Bramy garażowe segmentowe AVO (panel 40 lub 60 mm) i rolowane Aluprof. Porównanie, kolory, przeszklenia, napędy i smart home — PROMYK Wieluń.")
          + nav("bramy-garazowe") + body + footer())

    # ---- podstrona: bramy segmentowe
    panele = '<div class="panel-types" data-lightbox>' + "".join(
        f'<a href="assets/img/bramy/{f}.jpg" data-lightbox-item><img src="assets/img/bramy/{f}.jpg" alt="Brama segmentowa — {n.lower()}" loading="lazy"><span>{n}</span></a>'
        for n, f in [("Bez przetłoczeń", "panel-bez"), ("Z jednym przetłoczeniem", "panel-jedno"), ("Z wieloma przetłoczeniami", "panel-wiele")]) + "</div>"
    tabs = '<div class="chips chips--tabs" role="tablist">' + "".join(
        f'<button type="button" class="{"is-active" if i == 0 else ""}" data-filter-btn="{g}">{n}</button>'
        for i, (g, n) in enumerate(BR_AVO_GRUPY)) + "</div>"
    kolory = '<div class="swatches-grid" data-filter-grid>' + "".join(
        f'<figure data-filter="{g}"{"" if g == BR_AVO_GRUPY[0][0] else " hidden"}><img src="assets/img/bramy/{f}.jpg" alt="{n}" loading="lazy"><figcaption>{n}</figcaption></figure>'
        for g, n, f in BR_AVO_KOLORY) + "</div>"
    body = pagehero("bramy/segmentowe-noc", "Bramy segmentowe",
                    "Funkcjonalne rozwiązania, dobra izolacja termiczna i szeroki wybór wzorów oraz kolorów dopasowanych do stylu Twojego domu.", None)
    body += f"""<section class="section">
  <div class="container">
    <div class="subrow">
      <div class="subrow__text prose-text">
        <p>Bramy segmentowe to jedno z najpopularniejszych rozwiązań stosowanych w garażach, cenione za wygodę użytkowania i funkcjonalną konstrukcję. Podczas otwierania panele przesuwają się po prowadnicach pod sufitem, dzięki czemu brama nie zajmuje miejsca przed garażem.</p>
        <p>W zależności od modelu segmenty mają grubość 40 lub 60 mm. Do wyboru są panele gładkie, bez przetłoczeń, z jednym przetłoczeniem lub z wieloma przetłoczeniami. Bramę można również wyposażyć w przeszklenia, zapewniające dostęp światła dziennego, oraz drzwi przejściowe, umożliwiające wejście do garażu bez otwierania całej bramy.</p>
        <a class="btn btn--primary btn--sm" href="kontakt.html">Zapytaj o wycenę {I['arrow']}</a>
      </div>
      <div><img src="assets/img/bramy/hero.jpg" alt="Brama segmentowa w okleinie drewnopodobnej" loading="lazy"></div>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Wzory paneli</h2></div></div>
    {panele}
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Kolorystyka bram AVO</h2></div></div>
    <div>{tabs}{kolory}</div>
    <p class="colors-note">Oprócz pokazanych kolorów dostępne są ponad 200 kolorów z palety RAL (także w lakierowaniu strukturalnym), okleiny drewnopodobne oraz lakierowanie na kolor z palety NCS.</p>
  </div>
</section>

<section class="section section--soft">
  <div class="container">
    <div class="garage-anim-wrap">
      <div>{_bramy_anim()}</div>
      <div class="subrow__text prose-text">
        <h2>Jak otwiera się brama segmentowa?</h2>
        <p>Panele unoszą się pionowo, a następnie przesuwają po prowadnicach pod sufitem — brama nie zajmuje miejsca przed garażem ani na podjeździe.</p>
        <p>Bramy segmentowe otwierane automatycznie wyposażone są w napęd paskowy, który zapewnia płynną i cichą pracę. Istnieje również możliwość zastosowania rozwiązań Somfy Smart Home, dzięki którym bramą można sterować zdalnie i zintegrować ją z inteligentnym systemem zarządzania domem.</p>
      </div>
    </div>
  </div>
</section>

{cta("Doradztwo i wycena", "Dobierzemy bramę do Twojego garażu",
     "Skontaktuj się z nami — doradzimy technicznie i przygotujemy kalkulację cenową.")}

<section class="section related">
  <div class="container">
    <h2 class="h-sec" style="margin-bottom:32px">Zobacz również</h2>
    <div class="grid-3">{_br_related("bramy-garazowe--bramy-segmentowe")}</div>
  </div>
</section>
"""
    body = body.replace('<section class="pagehero">', '<section class="pagehero pagehero--low">', 1)
    write("bramy-garazowe--bramy-segmentowe.html", head("Bramy segmentowe AVO — panele 40 i 60 mm, wzory i kolory | PROMYK Wieluń",
                                                         "Bramy segmentowe AVO: panele 40 lub 60 mm z pianką PU, gładkie, z jednym lub wieloma przetłoczeniami, kolory RAL i okleiny, napęd paskowy i Somfy Smart Home.")
          + nav("bramy-garazowe") + body + footer())

    # ---- podstrona: bramy rolowane
    rk = '<div class="swatches-grid">' + "".join(
        f'<figure><img src="assets/img/rol/kolor-{f}.jpg" alt="{n}" loading="lazy"><figcaption>{n}</figcaption></figure>'
        for f, n in BR_ROL_KOLORY) + "</div>"
    body = pagehero("bramy/rolowane-aluprof", "Bramy rolowane",
                    "Oszczędność miejsca, wygodna obsługa i funkcjonalne rozwiązania dopasowane do różnych rodzajów garaży.", None)
    body += f"""<section class="section">
  <div class="container">
    <div class="subrow">
      <div class="subrow__text prose-text">
        <p>Bramy rolowane Aluprof to praktyczne rozwiązanie, które sprawdzi się zarówno w nowych, jak i modernizowanych garażach. Pancerz bramy zwija się do skrzynki umieszczonej nad otworem, dzięki czemu nie zajmuje miejsca pod sufitem i pozwala w pełni wykorzystać przestrzeń garażu.</p>
        <p>Pancerz wykonany jest z aluminiowych profili PA 77 o wysokości 77 mm, wypełnionych pianką poliuretanową. W zależności od wymiarów i konfiguracji bramy można zastosować skrzynkę o wysokości 250 lub 300 mm. Standardowo bramy rolowane Aluprof wyposażone są w napęd rurowy z awaryjnym otwieraniem za pomocą korby. Dzięki temu bramę można obsługiwać elektrycznie na co dzień, a w przypadku braku zasilania otworzyć ją ręcznie. To praktyczne rozwiązanie, które zwiększa wygodę użytkowania i zapewnia możliwość korzystania z bramy również w awaryjnych sytuacjach.</p>
        <a class="btn btn--primary btn--sm" href="kontakt.html">Zapytaj o wycenę {I['arrow']}</a>
      </div>
      <div><img class="img-contain" src="assets/img/bramy/rolowane-konstrukcja.jpg" alt="Brama rolowana Aluprof — pancerz i skrzynka" loading="lazy"></div>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Kolory bram rolowanych</h2></div></div>
    {rk}
  </div>
</section>

{cta("Doradztwo i wycena", "Dobierzemy bramę do Twojego garażu",
     "Skontaktuj się z nami — doradzimy technicznie i przygotujemy kalkulację cenową.")}

<section class="section related">
  <div class="container">
    <h2 class="h-sec" style="margin-bottom:32px">Zobacz również</h2>
    <div class="grid-3">{_br_related("bramy-garazowe--bramy-rolowane")}</div>
  </div>
</section>
"""
    write("bramy-garazowe--bramy-rolowane.html", head("Bramy rolowane Aluprof — pancerz PA 77, skrzynka 250/300 mm | PROMYK Wieluń",
                                                       "Bramy rolowane Aluprof: pancerz z profili PA 77 z pianką PU, skrzynka 250 lub 300 mm, napęd rurowy z awaryjną korbą. Kolory standardowe i drewnopodobne.")
          + nav("bramy-garazowe") + body + footer())


# ================================================================ MARKIZY (uwagi klienta 21.10.2026) ----
MK_ROWS = [
    ("Markizy tarasowe",
     ["Solidna konstrukcja z ekstrudowanego aluminium",
      "Sterowanie ręczne lub elektryczne",
      "Duże możliwości wymiarowe: szerokość do 7&nbsp;m i wysięg do 3,6&nbsp;m",
      "Możliwość dopasowania kąta nachylenia",
      "Szeroki wybór kolorów i tkanin",
      "Rozwiązania do tarasów przydomowych i lokali usługowych"], "mark/tarasowe", "markizy--markizy-tarasowe"),
    ("Markizy balkonowe",
     ["Montaż do balustrady balkonowej",
      "Regulacja kąta nachylenia tkaniny",
      "Możliwość dopasowania wymiarów do balkonu",
      "Wygodna obsługa ręczna",
      "Szeroki wybór kolorów tkanin",
      "Rozwiązanie idealne na balkony w budynkach mieszkalnych"], "mark/balkonowe", "markizy--markizy-balkonowe"),
    ("Automatyka Somfy",
     ["Wygodne rozwijanie i zwijanie bez użycia korby",
      "Sterowanie markizą za pomocą pilota",
      "Możliwość integracji z systemem Smart Home",
      "Czujnik wstrząsowy zwiększający ochronę markizy",
      "Awaryjne zwijanie markizy korbą - w przypadku braku prądu"], "mark/automatyka", None),
]
MK_ADV = [("Ochrona przed słońcem", "Komfortowy cień na tarasie i balkonie", "sun"),
          ("Wygodna obsługa", "Korba, pilot lub sterowanie Smart Home", "cog"),
          ("Trwałe tkaniny", "Szeroki wybór kolorów, odporność na płowienie", "shield")]
MK_FAQ = [
    ("Kaseta pełna, półkaseta czy markiza otwarta?",
     "Pełna kaseta chroni tkaninę i ramiona całkowicie po zwinięciu — najdłuższa żywotność poszycia. Półkaseta osłania tkaninę od góry, jest lżejsza i tańsza. Otwarta sprawdza się pod zadaszeniem, gdzie poszycie nie moknie."),
    ("Jak dobrać wymiary markizy do tarasu?",
     "Szerokość markizy powinna być dopasowana do wielkości tarasu i strefy, którą ma osłaniać, a jej wysięg – do oczekiwanego zakresu cienia. Przy wyborze warto uwzględnić rozmieszczenie mebli, nasłonecznienie oraz miejsce montażu. Przed zamówieniem należy upewnić się, że konstrukcja zmieści się na elewacji."),
    ("Jak wybrać kolor tkaniny markizy?",
     "Kolor tkaniny markizy warto dopasować do elewacji, stolarki okiennej i aranżacji tarasu. Jasne odcienie nadają przestrzeni lekkości, natomiast ciemniejsze mogą mocniej ograniczać ilość światła pod markizą."),
    ("Czy markizę można zamontować na ocieplonej elewacji?",
     "Tak, markizę można zamontować na ocieplonej elewacji, pod warunkiem zastosowania odpowiednich mocowań dostosowanych do rodzaju ściany i grubości ocieplenia."),
    ("Czy markizę należy zwijać podczas silnego wiatru?",
     "Tak, podczas silnego wiatru markizę należy zwinąć, aby uniknąć uszkodzenia tkaniny i konstrukcji. Markizy są narażone na duże obciążenia spowodowane podmuchami, dlatego należy przestrzegać zaleceń producenta dotyczących odporności na wiatr. Dodatkową ochronę może zapewnić automatyka Somfy z czujnikiem wstrząsowym, który uruchamia zwijanie markizy po wykryciu określonych warunków."),
    ("Czy markiza chroni przed deszczem?",
     "Markiza zapewnia przede wszystkim ochronę przed słońcem, a jej odporność na deszcz zależy od rodzaju tkaniny i konstrukcji. Nie jest przeznaczona do użytkowania podczas intensywnych opadów, które mogą obciążać materiał i prowadzić do uszkodzeń. W czasie deszczu i silnego wiatru zaleca się zwinięcie markizy zgodnie z zaleceniami producenta."),
]
MK_TARASOWE = [
    ("Australia", "bez kasety", "mark/australia",
     "Markiza bezkasetowa — prosta, lekka konstrukcja, która świetnie sprawdza się we wnękach i pod zadaszeniem. Montaż do ściany, sufitu lub krokwi, regulacja kąta 5–60°.",
     "Szerokość do 7&nbsp;m, wysięg do 3,6&nbsp;m"),
    ("Palladio", "półkaseta", "mark/palladio",
     "Częściowo zabudowana kaseta o minimalistycznym kształcie osłania zwiniętą tkaninę od góry. Kąt nachylenia regulowany w zakresie 5–50°, opcjonalne oświetlenie LED w ramionach.",
     "Szerokość do 7&nbsp;m, wysięg do 3,6&nbsp;m"),
    ("Dakar", "pełna kaseta", "mark/dakar",
     "Pełna kaseta o zaokrąglonym kształcie z uszczelką — po zwinięciu tkanina i ramiona są całkowicie schowane i chronione przed deszczem i zabrudzeniami. Kąt nachylenia 5–40°.",
     "Szerokość do 6&nbsp;m, wysięg do 3,6&nbsp;m"),
]
MK_INSPIRACJE = [f"mark/insp-{i:02d}" for i in (1, 2, 3, 4, 9, 6, 7, 8)]  # 05 = markiza pionowa, nie w ofercie


def _mk_related(cur):
    out = ""
    for slug, title, img in [("markizy--markizy-tarasowe", "Markizy tarasowe", "mark/tarasowe"),
                             ("markizy--markizy-balkonowe", "Markizy balkonowe", "mark/balkonowe"),
                             ("markizy", "Wszystkie markizy", "mark/hero")]:
        if slug == cur: continue
        out += f"""<a href="{slug}.html"><article class="card">
        <img src="assets/img/{img}.jpg" alt="{title}" style="height:150px;object-fit:cover;border-radius:var(--r-md)" loading="lazy">
        <div><h3>{title}</h3></div>
        <span class="card__more">Zobacz {I['arrow']}</span>
      </article></a>"""
    return out


def build_markizy():
    rows = ""
    for k, (title, bullets, img, more) in enumerate(MK_ROWS):
        li = "".join(f'<li><span class="check">{I["check"]}</span> {b}</li>' for b in bullets)
        media = f'<div><img src="assets/img/{img}.jpg" alt="{title}" loading="lazy"></div>'
        btn_more = f'<a class="btn btn--primary btn--sm" href="{more}.html">Więcej o tym rozwiązaniu {I["arrow"]}</a>' if more else ""
        text = f"""<div class="subrow__text">
        <h2>{title}</h2>
        <ul class="bullets">{li}</ul>
        <div style="display:flex;gap:12px;flex-wrap:wrap">
          {btn_more}
          <a class="btn btn--{"outline" if more else "primary"} btn--sm" href="kontakt.html">Zapytaj o wycenę {I['arrow']}</a>
        </div>
      </div>"""
        flip = k % 2
        rows += f'<div class="subrow{" subrow--flip" if flip else ""}">{media if not flip else text}{text if not flip else media}</div>'
    adv = "".join(f"""<div class="adv"><span class="adv__icon">{I[ic]}</span>
      <div><h3>{t}</h3><p>{d}</p></div></div>""" for t, d, ic in MK_ADV)
    faq = "".join(f"""<div class="faq__row">
      <button class="faq__q"><span>{q}</span><span>+</span></button>
      <div class="faq__a"><p>{a}</p></div>
    </div>""" for q, a in MK_FAQ)
    insp = '<div class="gallery gallery--okna" data-lightbox>' + "".join(
        f'<a href="assets/img/{g}.jpg" data-lightbox-item><img src="assets/img/{g}.jpg" alt="Markiza Aluprof Sun Shading Solutions — inspiracja" loading="lazy"></a>'
        for g in MK_INSPIRACJE) + "</div>"
    rel = ""
    for sl in ["pergole", "oslony-zewnetrzne", "rolety-zewnetrzne"]:
        rel += f"""<a href="{sl}.html"><article class="card">
        <img src="assets/img/{PROD_IMG[sl]}.jpg" alt="{PROD_LABEL[sl]}" style="height:150px;object-fit:cover;border-radius:var(--r-md)">
        <div><h3>{PROD_LABEL[sl]}</h3></div>
        <span class="card__more">Zobacz ofertę {I['arrow']}</span>
      </article></a>"""
    body = pagehero("mark/hero", "Markizy Aluprof Sun Shading Solutions",
                    "Komfortowy cień i skuteczna ochrona przed słońcem, dzięki którym możesz cieszyć się wypoczynkiem na tarasie lub balkonie nawet w upalne dni.", None)
    body += f"""<section class="section section--tight-bottom"><div class="container">{rows}</div></section>
<section class="advantages"><div class="container advantages__inner">{adv}</div></section>
{_anim_section(_markiza_anim(), "Jak działa markiza tarasowa?", "Tkanina nawinięta jest na rurę w kasecie przy ścianie. Ramiona łamane wysuwają ją nad taras i utrzymują w napięciu, a Ty decydujesz, jak duży ma być cień. Z czujnikiem wiatru markiza zwija się sama, gdy pogoda się zmienia.")}
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

{cta("Doradztwo i wycena", "Planujesz markizę na taras lub balkon?",
     "Skontaktuj się z nami — doradzimy technicznie i przygotujemy kalkulację cenową.")}

<section class="section related">
  <div class="container">
    <h2 class="h-sec" style="margin-bottom:32px">Sprawdź również inne systemy</h2>
    <div class="grid-3">{rel}</div>
  </div>
</section>
"""
    write("markizy.html", head("Markizy Aluprof Sun Shading Solutions — tarasowe i balkonowe | PROMYK Wieluń",
                               "Markizy tarasowe i balkonowe Aluprof Sun Shading Solutions: bez kasety, w półkasecie i pełnej kasecie, automatyka Somfy z czujnikiem wstrząsowym — PROMYK Wieluń.")
          + nav("markizy") + body + footer())

    # ---- podstrona: markizy tarasowe
    cards = "".join(f"""<article class="sill-card">
        <a href="assets/img/{img}.jpg" data-lightbox-item><img src="assets/img/{img}.jpg" alt="Markiza {n} — {typ}" loading="lazy"></a>
        <div><h3>{n} <span class="mk-type">{typ}</span></h3><p>{d}</p><small>{dim}</small></div>
      </article>""" for n, typ, img, d, dim in MK_TARASOWE)
    body = pagehero("mark/tarasowe", "Markizy tarasowe",
                    "Dostępne w wersji bez kasety, z półkasetą lub w pełnej kasecie – wybierz markizę dopasowaną do Twoich potrzeb", None)
    body += f"""<section class="section">
  <div class="container">
    <p class="sill-lead">Montujemy trzy rodzaje markiz tarasowych Aluprof Sun Shading Solutions. Różnią się stopniem osłonięcia zwiniętej tkaniny — od lekkiej markizy bez kasety, przez półkasetę, po pełną kasetę, która chroni tkaninę i ramiona po zwinięciu. Każdą z nich można obsługiwać ręcznie korbą lub elektrycznie, także z automatyką Somfy.</p>
    <div class="sill-types sill-types--3" data-lightbox>{cards}</div>
  </div>
</section>

{cta("Doradztwo i wycena", "Dobierzemy markizę do Twojego tarasu",
     "Skontaktuj się z nami — doradzimy technicznie i przygotujemy kalkulację cenową.")}

<section class="section related">
  <div class="container">
    <h2 class="h-sec" style="margin-bottom:32px">Zobacz również</h2>
    <div class="grid-3">{_mk_related("markizy--markizy-tarasowe")}</div>
  </div>
</section>
"""
    write("markizy--markizy-tarasowe.html", head("Markizy tarasowe Aluprof — Australia, Palladio, Dakar | PROMYK Wieluń",
                                                  "Markizy tarasowe Aluprof Sun Shading Solutions: Australia (bez kasety), Palladio (półkaseta) i Dakar (pełna kaseta). Szerokość do 7 m, wysięg do 3,6 m.")
          + nav("markizy") + body + footer())

    # ---- podstrona: markizy balkonowe
    body = pagehero("mark/balkonowe", "Markizy balkonowe",
                    "Lekka markiza montowana do balustrady — przyjemny cień i więcej prywatności na Twoim balkonie.", None)
    body += f"""<section class="section">
  <div class="container">
    <div class="subrow">
      <div class="subrow__text prose-text">
        <h2>Italia poręczowa</h2>
        <p>Markiza Italia poręczowa to lekka, bezkasetowa konstrukcja z ekstrudowanego aluminium, zaprojektowana z myślą o balkonach i wnękach balkonowych. Jej aluminiowe ramiona mocuje się bezpośrednio do poręczy, a uniwersalny uchwyt pozwala na montaż ścienny lub sufitowy.</p>
        <p>Kąt nachylenia tkaniny można regulować aż do 90°, dzięki czemu markiza działa jak zadaszenie albo jak osłona od czoła balkonu. Obsługa odbywa się ręcznie, za pomocą korby. Szerokość markizy do 5 m, wysięg 0,7 m, a do wyboru jest bogata kolekcja tkanin, trzy rodzaje falban i konstrukcja w dowolnym kolorze z palety RAL.</p>
        <a class="btn btn--primary btn--sm" href="kontakt.html">Zapytaj o wycenę {I['arrow']}</a>
      </div>
      <div><img src="assets/img/mark/balkonowe.jpg" alt="Markizy balkonowe Italia poręczowa" loading="lazy"></div>
    </div>
  </div>
</section>

{cta("Doradztwo i wycena", "Dobierzemy markizę do Twojego balkonu",
     "Skontaktuj się z nami — doradzimy technicznie i przygotujemy kalkulację cenową.")}

<section class="section related">
  <div class="container">
    <h2 class="h-sec" style="margin-bottom:32px">Zobacz również</h2>
    <div class="grid-3">{_mk_related("markizy--markizy-balkonowe")}</div>
  </div>
</section>
"""
    write("markizy--markizy-balkonowe.html", head("Markizy balkonowe Aluprof — Italia poręczowa | PROMYK Wieluń",
                                                   "Markiza balkonowa Aluprof Italia poręczowa: montaż do balustrady, regulacja kąta do 90°, obsługa ręczna korbą, szerokość do 5 m.")
          + nav("markizy") + body + footer())


# ================================================================ OSŁONY WEWNĘTRZNE (uwagi klienta 21.10.2026) ----
OW_ROWS = [
    ("Żaluzje aluminiowe",
     ["Lamele 16 mm, 25 mm i 50 mm",
      "Odporne na wilgoć — kuchnie i łazienki",
      "Obsługa sznurkiem lub łańcuszkiem, opcja napędu elektrycznego",
      "Precyzyjna regulacja ilości światła",
      "Szeroka gama kolorów lameli",
      "Nowoczesny i ponadczasowy wygląd",
      "Rozwiązanie m.in. do domu, mieszkania i biura"], "osl/aluminiowe-katalog2"),
    ("Żaluzje drewniane i bambusowe",
     ["Lamele 25 mm i 50 mm",
      "Naturalny wygląd i ponadczasowy styl",
      "Precyzyjna regulacja ilości światła",
      "Bogata gama kolorów i odcieni drewna",
      "Dopasowanie do wnętrz nowoczesnych i klasycznych",
      "Możliwość sterowania ręcznego lub elektrycznego",
      "Efekt przytulnego wnętrza",
      "Rozwiązanie m.in. do salonu, sypialni i gabinetu"], "osl/drewniane"),
    ("Plisy",
     ["System dwukierunkowy góra-dół — zasłonisz dowolny fragment szyby",
      "Dopasowanie do okien o standardowych i nietypowych kształtach",
      "Tkaniny transparentne, przyciemniające i blackout z powłoką perłową",
      "Nowoczesny i minimalistyczny wygląd",
      "Rozwiązania do okien dachowych",
      "Wygodna obsługa i łatwa regulacja",
      "Większa prywatność bez całkowitego odcinania światła",
      "Rozwiązania m.in. do kuchni, łazienki, salonu i sypialni"], "osl/plisy-bez"),
    ("Rolety rzymskie",
     ["Miękkie fałdy tkaniny, demontaż do prania",
      "Szeroki wybór tkanin i kolorów",
      "Szycie na wymiar",
      "Efekt dekoracyjnych zakładek",
      "Możliwość wyboru grubości i faktury materiału",
      "Estetyczna alternatywa dla klasycznych zasłon",
      "Możliwość zdjęcia tkaniny do prania",
      "Rozwiązanie m.in. do salonu, sypialni i jadalni"], "osl/rzymskie"),
    ("Rolety materiałowe",
     ["Warianty montażu: w kasecie, nakładane na ramę okna lub na ścianie",
      "Tkaniny gładkie, wzorzyste i dekoracyjne",
      "Estetyczne osłonięcie okna bez ciężkich zasłon",
      "Połączenie funkcjonalności z prostym designem",
      "Rozwiązania do okien dachowych",
      "Różne stopnie przepuszczalności światła",
      "Rozwiązania m.in. do salonu, sypialni i biura"], "osl/materialowe"),
    ("Rolety dzień-noc",
     ["Naprzemienne pasy transparentne i zaciemniające",
      "Płynna regulacja światła bez podnoszenia rolety",
      "Szeroki wybór kolorów i wzorów",
      "Nowoczesny wygląd i dekoracyjny charakter",
      "Delikatne rozproszenie światła słonecznego",
      "Estetyczna alternatywa dla tradycyjnych firan i zasłon",
      "Montaż w kasecie, na ramie okna lub na ścianie",
      "Rozwiązanie m.in. do salonu, sypialni"], "osl/dzien-noc"),
    ("Żaluzje pionowe",
     ["Pasy 89 / 127 mm z regulacją kąta obrotu",
      "Możliwość obracania lameli o 180°",
      "Szeroki wybór kolorów i tkanin",
      "Płynne przesuwanie lameli na boki",
      "Możliwość osłonięcia przeszkleń od podłogi do sufitu",
      "Różne warianty rozsuwania lameli – jednostronnie lub na boki.",
      "Idealne rozwiązanie do dużych przeszkleń, biur i sal konferencyjnych"], "osl/pionowe"),
]
OW_ADV = [("Na wymiar", "Produkcja pod wymiar każdej wnęki i skrzydła", "ruler"),
          ("Regulacja światła", "Od pełnego zaciemnienia (blackout) po delikatne rozproszenie", "sun"),
          ("30 lat doświadczenia", "Osłony wewnętrzne produkujemy od 30 lat", "star")]
OW_FAQ = [
    ("Czym różnią się rolety, plisy i żaluzje?",
     "Rolety, plisy i żaluzje różnią się sposobem regulacji światła, budową oraz wyglądem. Rolety materiałowe tworzą jednolitą powierzchnię tkaniny i pozwalają osłonić okno, plisy można przesuwać zarówno od góry, jak i od dołu, a żaluzje umożliwiają precyzyjne sterowanie ilością światła dzięki regulowanym lamelom. Wybór zależy od oczekiwanego poziomu zaciemnienia, prywatności i stylu wnętrza."),
    ("Jakie osłony najlepiej sprawdzą się w salonie, sypialni i kuchni?",
     "W salonie świetnie sprawdzą się rolety materiałowe, rolety rzymskie lub żaluzje, które pozwalają dopasować ilość światła do potrzeb i stylu wnętrza. Do sypialni warto wybrać rolety zaciemniające, zapewniające komfortowy sen i większą prywatność. W kuchni najlepiej sprawdzą się praktyczne osłony, takie jak plisy czy żaluzje aluminiowe, które ułatwiają regulację światła i codzienną pielęgnację. W każdym pomieszczeniu warto dopasować osłonę do warunków i sposobu użytkowania."),
    ("Jak dobrać kolor osłon do okien i wystroju pomieszczenia?",
     "Kolor osłon wewnętrznych warto dopasować do odcienia okien, ścian, podłogi i mebli. Jasne tkaniny optycznie rozjaśniają wnętrze, a ciemniejsze mogą stanowić wyrazisty akcent aranżacyjny. W nowoczesnych pomieszczeniach dobrze sprawdzają się szarości, biele i beże, natomiast żaluzje drewniane wprowadzają naturalne ciepło."),
    ("Czy osłony wewnętrzne można zamontować bez wiercenia?",
     "Tak, wiele osłon wewnętrznych można zamontować bez wiercenia, np. przy użyciu specjalnych uchwytów zakładanych na ramę okna. Dostępność montażu bezinwazyjnego zależy od rodzaju osłony, konstrukcji okna oraz wybranego systemu mocowania."),
    ("Jakie osłony sprawdzą się w pomieszczeniach o podwyższonej wilgotności?",
     "Do kuchni i łazienek polecamy żaluzje aluminiowe, które dobrze sprawdzają się w pomieszczeniach narażonych na wilgoć. Są łatwe w czyszczeniu, praktyczne i pozwalają wygodnie regulować ilość światła wpadającego do wnętrza."),
    ("Jakie osłony można zamontować na oknach dachowych?",
     "Do okien dachowych można wybrać rolety materiałowe z jednolitą tkaniną lub plisy, które pozwalają osłonić wybraną część okna."),
    ("Gdzie można zobaczyć dostępne kolory i wzory osłon wewnętrznych?",
     "Osłony wewnętrzne dostępne są w bogatej gamie kolorów i wzorów – od klasycznych, stonowanych odcieni po bardziej wyraziste barwy i ciekawe struktury. Na miejscu oferujemy szeroki wybór tkanin i wzorników, dzięki którym można dopasować osłony do okien oraz wystroju wnętrza. Kolekcje są regularnie aktualizowane, dlatego warto odwiedzić nasz salon i zobaczyć aktualnie dostępne propozycje."),
]
OW_INSPIRACJE = [f"osl/insp-{i:02d}" for i in (1, 2, 17, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)]  # 03 = żaluzje na skosach, nie w ofercie


def build_oslony_wewnetrzne():
    meta = PRODUCT_DATA["oslony-wewnetrzne"]
    rows = ""
    for k, (title, bullets, img) in enumerate(OW_ROWS):
        li = "".join(f'<li><span class="check">{I["check"]}</span> {b}</li>' for b in bullets)
        media = f'<div><img src="assets/img/{img}.jpg" alt="{title}" loading="lazy"></div>'
        text = f"""<div class="subrow__text">
        <h2>{title}</h2>
        <ul class="bullets">{li}</ul>
        <a class="btn btn--primary btn--sm" href="kontakt.html">Zapytaj o wycenę {I['arrow']}</a>
      </div>"""
        flip = k % 2
        rows += f'<div class="subrow{" subrow--flip" if flip else ""}">{media if not flip else text}{text if not flip else media}</div>'
    adv = "".join(f"""<div class="adv"><span class="adv__icon">{I[ic]}</span>
      <div><h3>{t}</h3><p>{d}</p></div></div>""" for t, d, ic in OW_ADV)
    faq = "".join(f"""<div class="faq__row">
      <button class="faq__q"><span>{q}</span><span>+</span></button>
      <div class="faq__a"><p>{a}</p></div>
    </div>""" for q, a in OW_FAQ)
    insp = '<div class="gallery gallery--okna" data-lightbox>' + "".join(
        f'<a href="assets/img/{g}.jpg" data-lightbox-item><img src="assets/img/{g}.jpg" alt="Osłony wewnętrzne — inspiracja" loading="lazy"></a>'
        for g in OW_INSPIRACJE) + "</div>"
    rel = ""
    for sl in ["okna", "moskitiery", "oslony-zewnetrzne"]:
        rel += f"""<a href="{sl}.html"><article class="card">
        <img src="assets/img/{PROD_IMG[sl]}.jpg" alt="{PROD_LABEL[sl]}" style="height:150px;object-fit:cover;border-radius:var(--r-md)">
        <div><h3>{PROD_LABEL[sl]}</h3></div>
        <span class="card__more">Zobacz ofertę {I['arrow']}</span>
      </article></a>"""
    body = pagehero("osl/hero", meta["h1"],
                    "Dobierz rozwiązanie do swojego wnętrza, wybierając spośród różnych materiałów, kolorów i sposobów regulacji światła.", None)
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

{cta("Doradztwo i wycena", "Dobierzemy osłony do Twojego wnętrza",
     "Skontaktuj się z nami — doradzimy technicznie i przygotujemy kalkulację cenową.")}

<section class="section related">
  <div class="container">
    <h2 class="h-sec" style="margin-bottom:32px">Sprawdź również inne systemy</h2>
    <div class="grid-3">{rel}</div>
  </div>
</section>
"""
    write("oslony-wewnetrzne.html", head(meta["title"], meta["desc"]) + nav("oslony-wewnetrzne") + body + footer())


# ================================================================ OSŁONY ZEWNĘTRZNE + ŻALUZJE FASADOWE (uwagi klienta 21.10.2026) ----
OZ_KOLORY = ["RAL 9001 mat", "RAL 9010 mat", "RAL 9016 mat", "RAL 1013 mat", "RAL 1015 mat", "VSR 240 satyna", "RAL 7001 mat",
             "RAL 7012 mat", "RAL 7015 mat", "RAL 7016 mat", "RAL 7021 mat", "RAL 7024 mat", "RAL 7035 mat", "RAL 7037 mat",
             "RAL 9006 mat", "RAL 9007 mat", "FSM 71319 mat", "RAL 9005 mat", "VSR 780 mat", "RAL 8014 mat", "RAL 8016 mat",
             "DB 703 mat", "RAL 7022 mat", "RAL 7039 mat", "RAL 7043 mat", "RAL 8003 mat", "RAL 7016 struktura",
             "RAL 7021 struktura", "RAL 9005 struktura", "RAL 9010 struktura", "RAL 7038 mat", "RAL 7048 mat", "RAL 8003 struktura"]
OZ_SERGE = ["Antracite Grey", "Charcoal Bronze", "Charcoal", "Grey Charcoal", "Grey", "Grey White", "Linen",
            "Linen White", "Grey Sand", "Pure Black", "Sandstone", "Pearl Grey", "White"]
OZ_DREWNO = ["Mahoń", "Wiśnia", "Orzech", "Złoty dąb", "Dąb słodowy", "Winchester"]
OZ_ROWS = [
    ("Refleksole ZIIIP 120",
     ["Tkanina screen (Serge) – widok na zewnątrz przy jednoczesnym ograniczeniu intensywnego światła słonecznego.",
      "Prowadzenie tkaniny w systemie ZIP - materiał jest utrzymywany w prowadnicach bocznych",
      "Różne rodzaje tkanin – możliwość dopasowania przepuszczalności światła i widoczności na zewnątrz",
      "Szeroka gama kolorystyczna – dopasowanie osłony do elewacji i stolarki okiennej.",
      "Nowoczesny wygląd – minimalistyczna forma pasująca do współczesnej architektury.",
      "Napęd elektryczny – sterowanie pilotem",
      "Montaż na tarasie i przy oknach – możliwość osłonięcia przeszkleń oraz przestrzeni wypoczynkowej",
      "Opuszczona działa również tak jak moskitiera"], "ozew/refleksole", "oslony-zewnetrzne--refleksole-ziiip-120"),
    ("Sunbreaker 210",
     ["Regulacja kąta lameli – możliwość dopasowania osłony do położenia słońca.",
      "Nowoczesny design – podkreślenie charakteru elewacji budynku.",
      "Solidna konstrukcja aluminiowa – trwałość i odporność na warunki atmosferyczne.",
      "Różne warianty kolorystyczne – dopasowanie do stolarki okiennej i elewacji.",
      "Sterowanie ręczne lub elektryczne",
      "Element architektoniczny elewacji — montaż pionowy lub poziomy"], "ozew/sunbreaker", "oslony-zewnetrzne--sunbreaker-210"),
]
OZ_ADV = [("Ochrona przed słońcem", "Mniej nagrzewania wnętrz i tarasu", "sun"),
          ("Odporność na wiatr", "Refleksole ZIIIP w najwyższej, 6. klasie odporności na wiatr", "wind"),
          ("Wygodne sterowanie", "Napęd elektryczny i pilot", "cog")]
OZ_FAQ = [
    ("Czym różnią się refleksole od sunbreakerów?",
     "Refleksole to osłony wykonane ze specjalnej tkaniny, która ogranicza dopływ promieni słonecznych, zmniejsza nagrzewanie i może zachować widok na zewnątrz. Sunbreakery to osłony z aluminiowych lameli, które chronią przed słońcem i pozwalają kontrolować ilość światła docierającego do wnętrza. Oba rozwiązania sprawdzają się przy przeszkleniach i w przestrzeniach zewnętrznych, a wybór zależy od oczekiwanego efektu i sposobu użytkowania."),
    ("Czy refleksole można zamontować na tarasie?",
     "Tak, refleksole można zamontować na tarasie, np. jako osłony boczne, które ograniczają nasłonecznienie i poprawiają komfort wypoczynku."),
    ("Jak dobrać stopień przepuszczalności tkaniny w refleksolach?",
     "Dobór tkaniny do refleksoli zależy od stopnia nasłonecznienia oraz oczekiwanego poziomu ochrony przed słońcem. Tkaniny o większej przepuszczalności pozwalają zachować lepszy widok na zewnątrz i dostęp naturalnego światła, natomiast te o gęstszym splocie skuteczniej ograniczają ilość światła docierającego do wnętrza."),
    ("Czy refleksole i sunbreakery można zatrzymać na dowolnej wysokości?",
     "Tak, refleksole z napędem elektrycznym można zazwyczaj zatrzymać na dowolnej wysokości, dopasowując stopień osłonięcia do aktualnych potrzeb. W przypadku sunbreakerów możliwość ustawienia zależy od zastosowanego systemu – regulowane lamele pozwalają kontrolować ilość światła i stopień zacienienia. Dostępne funkcje zależą od wybranego modelu i sposobu sterowania."),
    ("Czy refleksole i sunbreakery są odporne na warunki atmosferyczne?",
     "Tak, refleksole i sunbreakery są przystosowane do użytkowania na zewnątrz i odporne na typowe warunki atmosferyczne."),
    ("Czy refleksole i sunbreakery można podnosić i opuszczać?",
     "Refleksole można podnosić i opuszczać, dostosowując poziom osłonięcia do aktualnych potrzeb. W przypadku sunbreakerów nie ma takiej możliwości. Są zamontowane na stałe, można jedynie regulować kąt nachylenia lameli."),
]
OZ_INSPIRACJE = [f"ozew/insp-{i:02d}" for i in range(1, 9)]

ZF_ROWS = [
    ("Żaluzje fasadowe adaptacyjne",
     ["Do budynków istniejących — bez ingerencji w warstwę docieplenia",
      "Skrzynka z blachy osłonowej w kilku wariantach",
      "Ochrona przed nagrzewaniem – ograniczenie dopływu promieni słonecznych",
      "Szeroka gama kolorów – dopasowanie do okien i elewacji",
      "Nowoczesny wygląd – podkreślenie charakteru fasady",
      "Sterowanie elektryczne – wygodna obsługa osłon"], "fasad/adaptacyjne"),
    ("Żaluzje fasadowe podtynkowe",
     ["Montaż na etapie budowy lub generalnego remontu",
      "Kaseta BOX całkowicie ukryta pod ociepleniem i tynkiem",
      "Minimalistyczne wykończenie elewacji",
      "Komfort we wnętrzu – możliwość dopasowania zacienienia do pory dnia.",
      "Bogata kolorystyka – dopasowanie żaluzji do okien i elewacji.",
      "Sterowanie elektryczne – wygodna obsługa osłon"], "fasad/podtynkowe"),
]
ZF_ADV = [("Kontrola światła", "Płynna regulacja kąta nachylenia lameli", "sun"),
          ("Komfort termiczny", "Ograniczają nagrzewanie pomieszczeń latem i pomagają zmniejszyć straty ciepła zimą", "thermo"),
          ("Automatyka", "Sterowanie z telefonu, automatyczne zwijanie przy wietrze", "cog")]
ZF_FAQ = [
    ("Lamela C80 czy Z90 — czym się różnią?",
     "Lamele C80 są obustronnie wywinięte, sztywne i odporne na wiatr — obracają się w zakresie 0–180°. Lamele Z90 lepiej zaciemniają, mają uszczelkę wygłuszającą i obracają się w zakresie 0–90°."),
    ("Który system żaluzji fasadowych wybrać?",
     "W nowym budynku lub przy generalnym remoncie najlepiej sprawdzą się żaluzje podtynkowe, ukryte pod ociepleniem. W budynku istniejącym wybiera się zwykle żaluzje adaptacyjne, które nie wymagają ingerencji w docieplenie."),
    ("Czy żaluzje fasadowe mogą działać automatycznie?",
     "Tak. Żaluzje fasadowe wyposaża się w napęd elektryczny, a z czujnikami pogodowymi mogą same opuszczać się w słońcu i zwijać przy silnym wietrze. Można nimi sterować także z telefonu lub tabletu."),
    ("Czym różnią się żaluzje fasadowe od rolet zewnętrznych?",
     "Żaluzje fasadowe pozwalają regulować kąt nachylenia lameli, dzięki czemu można precyzyjnie kontrolować ilość światła wpadającego do pomieszczeń, jednocześnie ograniczając ich nagrzewanie. Rolety zewnętrzne mają pełny pancerz, który po opuszczeniu skuteczniej zaciemnia wnętrze i zapewnia większą osłonę przed hałasem oraz warunkami atmosferycznymi."),
    ("Czy żaluzje fasadowe można zamontować razem z oknami?",
     "Tak, żaluzje fasadowe można zaplanować już na etapie zamawiania okien. W nowym budynku warto uwzględnić je w projekcie, aby odpowiednio przygotować miejsce na montaż i estetycznie zintegrować system z elewacją."),
    ("Jak dobrać kolor żaluzji do okien i elewacji?",
     "Kolor żaluzji fasadowych warto dopasować do stolarki okiennej i elewacji, aby całość tworzyła spójną kompozycję. Można wybrać odcień zbliżony do koloru okien, który podkreśli ich wygląd, lub postawić na kontrast, który nada budynkowi nowoczesny charakter. Warto również zwrócić uwagę na kolor pozostałych elementów, takich jak brama garażowa czy drzwi wejściowe."),
    ("Czy można zintegrować je z systemem Smart Home?",
     "Tak, żaluzje fasadowe można zintegrować z systemem Smart Home, jeśli zastosowane sterowanie jest z nim kompatybilne. Dzięki temu można nimi zarządzać za pomocą aplikacji."),
]
ZF_INSPIRACJE = [f"fasad/insp-{i:02d}" for i in (1, 2, 3, 4, 5, 6, 8, 9)]


def _sunbreaker_anim():
    """Przekrój: eliptyczne pióra Sunbreakera obracają się 0–90° (SVG/SMIL)."""
    blades = ""
    for i in range(6):
        cy = 60 + 48 * i
        blades += (f'<g transform="translate(330 {cy})"><path class="sb-blade" d="M-46,0 C-30,-11 30,-11 46,0 C30,11 -30,11 -46,0 Z">'
                   f'<animateTransform attributeName="transform" type="rotate" values="0;0;80;80;0" keyTimes="0;0.15;0.45;0.75;1" '
                   f'dur="8s" repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;.45 0 .25 1;0 0 1 1;.45 0 .25 1"/></path></g>')
    return f"""<svg class="garage-anim" viewBox="0 0 640 360" role="img" aria-label="Animacja: obrót piór Sunbreakera 210">
  <circle cx="90" cy="70" r="26" class="sb-sun"/>
  <line x1="130" y1="90" x2="250" y2="150" class="sb-ray"/><line x1="130" y1="120" x2="250" y2="210" class="sb-ray"/><line x1="120" y1="150" x2="250" y2="270" class="sb-ray"/>
  <line x1="330" y1="30" x2="330" y2="330" class="sb-guide"/>
  {blades}
  <text x="420" y="345" class="ga-label">wnętrze</text>
  <text x="60" y="345" class="ga-label">na zewnątrz</text>
  <text x="410" y="70" class="ga-label ga-label--sm">pióra obracają się o 0–90°</text>
</svg>"""


def _rel_cards(items):
    out = ""
    for slug, title, img in items:
        out += f"""<a href="{slug}.html"><article class="card">
        <img src="assets/img/{img}.jpg" alt="{title}" style="height:150px;object-fit:cover;border-radius:var(--r-md)" loading="lazy">
        <div><h3>{title}</h3></div>
        <span class="card__more">Zobacz {I['arrow']}</span>
      </article></a>"""
    return out


def _rows_html(rows, more_ok=True):
    out = ""
    for k, row in enumerate(rows):
        title, bullets, img = row[0], row[1], row[2]
        more = row[3] if len(row) > 3 else None
        li = "".join(f'<li><span class="check">{I["check"]}</span> {b}</li>' for b in bullets)
        media = f'<div><img src="assets/img/{img}.jpg" alt="{title}" loading="lazy"></div>'
        btns = (f'<a class="btn btn--primary btn--sm" href="{more}.html">Więcej o tym rozwiązaniu {I["arrow"]}</a>'
                f'<a class="btn btn--outline btn--sm" href="kontakt.html">Zapytaj o wycenę {I["arrow"]}</a>') if more else \
               f'<a class="btn btn--primary btn--sm" href="kontakt.html">Zapytaj o wycenę {I["arrow"]}</a>'
        text = f"""<div class="subrow__text">
        <h2>{title}</h2>
        <ul class="bullets">{li}</ul>
        <div style="display:flex;gap:12px;flex-wrap:wrap">{btns}</div>
      </div>"""
        flip = k % 2
        out += f'<div class="subrow{" subrow--flip" if flip else ""}">{media if not flip else text}{text if not flip else media}</div>'
    return out


def _std_sections(adv, faq, insp, cta_h, related):
    adv_h = "".join(f"""<div class="adv"><span class="adv__icon">{I[ic]}</span>
      <div><h3>{t}</h3><p>{d}</p></div></div>""" for t, d, ic in adv)
    faq_h = "".join(f"""<div class="faq__row">
      <button class="faq__q"><span>{q}</span><span>+</span></button>
      <div class="faq__a"><p>{a}</p></div>
    </div>""" for q, a in faq)
    insp_h = '<div class="gallery gallery--okna" data-lightbox>' + "".join(
        f'<a href="assets/img/{g}.jpg" data-lightbox-item><img src="assets/img/{g}.jpg" alt="Inspiracja" loading="lazy"></a>' for g in insp) + "</div>"
    rel = ""
    for sl in related:
        rel += f"""<a href="{sl}.html"><article class="card">
        <img src="assets/img/{PROD_IMG[sl]}.jpg" alt="{PROD_LABEL[sl]}" style="height:150px;object-fit:cover;border-radius:var(--r-md)">
        <div><h3>{PROD_LABEL[sl]}</h3></div>
        <span class="card__more">Zobacz ofertę {I['arrow']}</span>
      </article></a>"""
    return f"""<section class="advantages"><div class="container advantages__inner">{adv_h}</div></section>

<section class="section section--soft">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Warto wiedzieć przed zakupem</h2></div></div>
    <div class="faq">{faq_h}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Inspiracje</h2></div></div>
    {insp_h}
  </div>
</section>

{cta("Doradztwo i wycena", cta_h, "Skontaktuj się z nami — doradzimy technicznie i przygotujemy kalkulację cenową.")}

<section class="section related">
  <div class="container">
    <h2 class="h-sec" style="margin-bottom:32px">Sprawdź również inne systemy</h2>
    <div class="grid-3">{rel}</div>
  </div>
</section>
"""


def _swatch_grid(items):
    return '<div class="swatches-grid">' + "".join(
        f'<figure><img src="assets/img/{f}.jpg" alt="{n}" loading="lazy"><figcaption>{n}</figcaption></figure>' for f, n in items) + "</div>"


def build_oslony_zewnetrzne():
    body = pagehero("ozew/hero", "Osłony zewnętrzne - refleksole i sunbreaker",
                    "Skuteczna ochrona przed słońcem i nowoczesny design. Idealne rozwiązanie do osłaniania przeszkleń oraz tworzenia komfortowej, zacienionej przestrzeni na tarasie.", None)
    body += f"""<section class="section section--tight-bottom"><div class="container">{_rows_html(OZ_ROWS)}</div></section>
""" + _std_sections(OZ_ADV, OZ_FAQ, OZ_INSPIRACJE, "Planujesz osłony przy pergoli lub przeszkleniach?", ["pergole", "zaluzje-fasadowe", "markizy"])
    write("oslony-zewnetrzne.html", head("Osłony zewnętrzne — refleksole ZIIIP 120 i Sunbreaker 210 Aluprof | PROMYK Wieluń",
                                         "Refleksole ZIIIP 120 z tkaniną Serge 600 i ruchome Sunbreakery 210 Aluprof — ochrona przed słońcem przy przeszkleniach i pergolach. PROMYK Wieluń.")
          + nav("oslony-zewnetrzne") + body + footer())

    kol = [(f"ozew/kolor-{i:02d}", n) for i, n in enumerate(OZ_KOLORY, 1)]
    # ---- refleksole
    body = pagehero("ozew/refleksole", "Refleksole ZIIIP 120", "Ochrona przed słońcem bez rezygnacji z widoku na zewnątrz.", None)
    body += f"""<section class="section">
  <div class="container">
    <div class="subrow">
      <div class="subrow__text prose-text">
        <p>Refleksol to zewnętrzna roleta z tkaniny screen prowadzonej w systemie ZIP: zgrzewany brzeg tkaniny biegnie w prowadnicy, utrzymując pełne naprężenie — osłona pracuje przy silnym wietrze bez łopotania i szczelnie domyka światło przy krawędziach.</p>
        <p>Refleksole ZIIIP 120 można wykonać w szerokości do <strong>7&nbsp;m</strong> i wysokości do <strong>4&nbsp;m</strong>. Najczęściej montujemy je przy pergolach — jako boczne osłony tarasu — oraz przy dużych przeszkleniach. Całkowicie opuszczona osłona działa również jak moskitiera.</p>
        <a class="btn btn--primary btn--sm" href="kontakt.html">Zapytaj o wycenę {I['arrow']}</a>
      </div>
      <div><img src="assets/img/ozew/refleksol-wnetrze.jpg" alt="Refleksol ZIIIP 120 przy dużym przeszkleniu" loading="lazy"></div>
    </div>
  </div>
</section>
<section class="section section--soft">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Tkaniny Serge 600</h2></div></div>
    {_swatch_grid([(f"ozew/serge-{i:02d}", n) for i, n in enumerate(OZ_SERGE, 1)])}
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Kolory konstrukcji</h2></div></div>
    {_swatch_grid(kol)}
  </div>
</section>
{cta("Doradztwo i wycena", "Dobierzemy refleksole do Twojej pergoli lub okien", "Skontaktuj się z nami — doradzimy technicznie i przygotujemy kalkulację cenową.")}
<section class="section related">
  <div class="container">
    <h2 class="h-sec" style="margin-bottom:32px">Zobacz również</h2>
    <div class="grid-3">{_rel_cards([("oslony-zewnetrzne--sunbreaker-210", "Sunbreaker 210", "ozew/sunbreaker"), ("oslony-zewnetrzne", "Wszystkie osłony zewnętrzne", "ozew/hero"), ("pergole", "Pergole", "perg/sb400")])}</div>
  </div>
</section>
"""
    write("oslony-zewnetrzne--refleksole-ziiip-120.html", head("Refleksole ZIIIP 120 Aluprof — tkaniny Serge 600, kolory | PROMYK Wieluń",
                                                              "Refleksole ZIIIP 120: tkanina screen Serge 600 w prowadnicach ZIP, szerokość do 7 m, wysokość do 4 m, 33 kolory konstrukcji. Montaż przy pergolach i przeszkleniach.")
          + nav("oslony-zewnetrzne") + body + footer())

    # ---- sunbreaker
    warianty = '<div class="panel-types panel-types--2" data-lightbox>' + "".join(
        f'<a href="assets/img/{f}.jpg" data-lightbox-item><img src="assets/img/{f}.jpg" alt="Sunbreaker 210 — {n.lower()}" loading="lazy"><span>{n}</span></a>'
        for n, f in [("Montaż poziomy", "ozew/sb-poziomy"), ("Montaż pionowy", "ozew/sb-pionowy")]) + "</div>"
    body = pagehero("ozew/sunbreaker", "Sunbreaker 210", "Ruchome lamele aluminiowe — pełna kontrola nad światłem i cieniem.", None)
    body += f"""<section class="section">
  <div class="container">
    <div class="garage-anim-wrap">
      <div>{_sunbreaker_anim()}</div>
      <div class="subrow__text prose-text">
        <h2>Ruchome pióra 210 mm</h2>
        <p>Sunbreaker 210 w wersji ruchomej to zewnętrzna osłona z wielkogabarytowych, eliptycznych piór aluminiowych o szerokości 210 mm, prowadzonych w bocznych prowadnicach. Pióra obracają się w zakresie do 90° — silnikiem liniowym albo ręcznie — dzięki czemu ilość światła i cienia dopasujesz do pory dnia i położenia słońca. W pozycji zamkniętej specjalny kształt pióra chroni także przed opadami.</p>
        <p>System montuje się poziomo lub pionowo, także jako ściana pergoli. Maksymalna szerokość piór to 4&nbsp;m, a wysokość systemu do 6,02&nbsp;m.</p>
        <a class="btn btn--primary btn--sm" href="kontakt.html">Zapytaj o wycenę {I['arrow']}</a>
      </div>
    </div>
  </div>
</section>
<section class="section section--soft">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Montaż poziomy i pionowy</h2></div></div>
    {warianty}
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Kolory konstrukcji</h2></div></div>
    {_swatch_grid(kol)}
    <h4 class="palette-title">Kolory drewnopodobne (za dopłatą)</h4>
    {_swatch_grid([(f"ozew/drewno-{i:02d}", n) for i, n in enumerate(OZ_DREWNO, 1)])}
  </div>
</section>
{cta("Doradztwo i wycena", "Dobierzemy Sunbreaker do Twojej elewacji lub pergoli", "Skontaktuj się z nami — doradzimy technicznie i przygotujemy kalkulację cenową.")}
<section class="section related">
  <div class="container">
    <h2 class="h-sec" style="margin-bottom:32px">Zobacz również</h2>
    <div class="grid-3">{_rel_cards([("oslony-zewnetrzne--refleksole-ziiip-120", "Refleksole ZIIIP 120", "ozew/refleksole"), ("oslony-zewnetrzne", "Wszystkie osłony zewnętrzne", "ozew/hero"), ("pergole", "Pergole", "perg/sb400")])}</div>
  </div>
</section>
"""
    write("oslony-zewnetrzne--sunbreaker-210.html", head("Sunbreaker 210 ruchomy Aluprof — pióra 210 mm, obrót 0–90° | PROMYK Wieluń",
                                                         "Ruchomy Sunbreaker 210 Aluprof: eliptyczne pióra 210 mm z regulacją kąta do 90°, montaż poziomy lub pionowy, szerokość do 4 m, kolory RAL i drewnopodobne.")
          + nav("oslony-zewnetrzne") + body + footer())


def _fasad_anim():
    """Przekrój żaluzji fasadowej: lamele obracają się, potem podnoszą do pakietu i opadają (SVG/SMIL)."""
    out = ""
    kt = "0;0.12;0.27;0.4;0.52;0.72;0.82;1"
    for i in range(7):
        y0 = 78 + 36 * i
        dy = (54 + 7 * i) - y0
        out += (f'<g transform="translate(330 {y0})"><g>'
                f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 0;0 0;0 0;0 {dy};0 {dy};0 0" keyTimes="{kt}" dur="12s" repeatCount="indefinite"/>'
                f'<path class="sb-blade" d="M-44,-2 Q0,-12 44,-2 L44,3 Q0,-7 -44,3 Z">'
                f'<animateTransform attributeName="transform" type="rotate" values="0;0;72;72;0;0;0;0" keyTimes="{kt}" dur="12s" repeatCount="indefinite"/>'
                f'</path></g></g>')
    return f"""<svg class="garage-anim" viewBox="0 0 640 360" role="img" aria-label="Animacja: obracanie i podnoszenie lameli żaluzji fasadowej">
  <rect x="270" y="22" width="120" height="24" rx="3" class="ga-motor"/>
  <line x1="276" y1="46" x2="276" y2="330" class="sb-guide"/>
  <line x1="384" y1="46" x2="384" y2="330" class="sb-guide"/>
  <circle cx="90" cy="70" r="26" class="sb-sun"/>
  {out}
  <text x="60" y="345" class="ga-label">na zewnątrz</text>
  <text x="430" y="345" class="ga-label">wnętrze</text>
  <text x="410" y="120" class="ga-label ga-label--sm">obrót lameli</text>
  <text x="410" y="140" class="ga-label ga-label--sm">i podnoszenie pakietu</text>
</svg>"""


def build_zaluzje_fasadowe():
    body = pagehero("fasad/hero", "Żaluzje fasadowe Aluprof",
                    "Nowoczesna ochrona przed słońcem. Reguluj ilość światła wpadającego do pomieszczeń.", None)
    body += f"""<section class="section section--tight-bottom"><div class="container">{_rows_html(ZF_ROWS)}</div></section>
<section class="section section--soft">
  <div class="container">
    <div class="subrow">
      <div class="subrow__text prose-text">
        <h2>Lamele C80 i Z90</h2>
        <p>Lamele żaluzji wykonane są z blachy aluminiowej. Lamele typu C są obustronnie wywinięte, sztywne i odporne na wiatr — obracają się w zakresie 0–180°. Lamele typu Z lepiej zaciemniają, mają uszczelkę wygłuszającą i obracają się w zakresie 0–90°.</p>
        <p>Prowadnice z uszczelkami tłumiącymi ograniczają hałas pracy. Żaluzjami można sterować przewodowo za pomocą pięciopozycyjnego włącznika Somfy Smoove Uno lub radiowo – pilotem Somfy Situo Variation io z pokrętłem umożliwiającym płynną regulację kąta nachylenia lameli. Możliwe jest również sterowanie z poziomu smartfona.</p>
      </div>
      <div class="ctrl-pair">
        <figure><img src="assets/img/fasad/smoove.jpg" alt="Włącznik Somfy Smoove Uno WT 5P" loading="lazy"><figcaption>Włącznik 5-pozycyjny Somfy Smoove Uno</figcaption></figure>
        <figure><img src="assets/img/fasad/situo.jpg" alt="Pilot Somfy Situo Variation io II" loading="lazy"><figcaption>Pilot z pokrętłem Somfy Situo Variation io</figcaption></figure>
      </div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="garage-anim-wrap">
      <div>{_fasad_anim()}</div>
      <div class="subrow__text prose-text">
        <h2>Jak działają żaluzje fasadowe?</h2>
        <p>Lamele obracają się, regulując ilość światła i widok na zewnątrz, a gdy osłona nie jest potrzebna — podnoszą się i składają w pakiet pod nadprożem.</p>
      </div>
    </div>
  </div>
</section>
<section class="section section--soft">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Kolory żaluzji</h2></div></div>
    {_swatch_grid([(f"ozew/kolor-{i:02d}", n) for i, n in enumerate(OZ_KOLORY, 1) if n != "RAL 9010 struktura"])}
  </div>
</section>
""" + _std_sections(ZF_ADV, ZF_FAQ, ZF_INSPIRACJE, "Planujesz żaluzje fasadowe?", ["oslony-zewnetrzne", "rolety-zewnetrzne", "okna"])
    write("zaluzje-fasadowe.html", head("Żaluzje fasadowe Aluprof — adaptacyjne i podtynkowe | PROMYK Wieluń",
                                        "Żaluzje fasadowe Aluprof z lamelami C80 i Z90: adaptacyjne i podtynkowe, sterowanie włącznikiem, pilotem Somfy lub z telefonu. PROMYK Wieluń.")
          + nav("zaluzje-fasadowe") + body + footer())


# ================================================================ MOSKITIERY (uwagi klienta 22.10.2026) ----
MS_ROWS = [
    ("Moskitiery ramkowe",
     ["Aluminiowy profil ramki – wysoka trwałość i odporność na uszkodzenia",
      "Prosty montaż i demontaż – łatwe zakładanie i zdejmowanie np. na zimę.",
      "Różne kolory profilu - możliwość dopasowania do stolarki okiennej",
      "Łatwe czyszczenie – prosta pielęgnacja siatki i ramki",
      "Bez ingerencji w okno – montaż za pomocą odpowiednich zaczepów, bez konieczności wiercenia w ramie okiennej"], "al41", False),
    ("Moskitiery drzwiowe",
     ["Solidna aluminiowa konstrukcja – trwałość i odporność na codzienne użytkowanie",
      "Ochrona przed owadami – swobodne korzystanie z otwartych drzwi bez komarów i much",
      "Estetyczny wygląd – konstrukcja dopasowana do stolarki okiennej i drzwiowej.",
      "Otwieranie na zawiasach – wygodne przechodzenie na taras lub balkon",
      "Zamykanie magnetyczne – komfortowe domykanie moskitiery",
      "Indywidualne dopasowanie – wykonanie na wymiar"], "mosk/drzwiowa-katalog", False),
    ("Moskitiery plisowane",
     ["Harmonijkowa konstrukcja zajmuje niewiele miejsca po złożeniu",
      "Wygodna obsługa – płynne otwieranie i zamykanie moskitiery",
      "Aluminiowy profil – trwałość i odporność na codzienne użytkowanie",
      "Dopasowanie na wymiar – możliwość dostosowania do konkretnego otworu",
      "Możliwość zatrzymania siatki w wybranym położeniu",
      "Niski próg – wygodne przechodzenie na taras lub balkon"], "al25", False),
    ("Moskitiery rolowane",
     ["Wygodna obsługa – szybkie rozwijanie i zwijanie moskitiery",
      "Dopasowanie na wymiar – możliwość dostosowania do okien i wybranych drzwi",
      "Trwała konstrukcja – solidne profile przeznaczone do wieloletniego użytkowania",
      "Możliwość całkowitego zwinięcia – odsłonięcie okna, gdy moskitiera nie jest potrzebna",
      "Kaseta ochronna – zabezpiecza zwiniętą siatkę poza sezonem użytkowania",
      "Dopasowanie kolorystyczne – możliwość dobrania profili do ram okiennych"], "al28", False),
]
MS_ADV = [("Ochrona", "Siatka o drobnym oczku — bariera także dla małych owadów", "bug"),
          ("Wentylacja", "Swobodny przepływ powietrza i światła", "wind"),
          ("Własna produkcja", "Moskitiery produkujemy na wymiar w naszej pracowni", "ruler")]
MS_KOLORY = ["Biały", "Srebrny", "Szary antracyt", "Ciemnobrązowy", "Czarny", "Złoty dąb", "Orzech", "Winchester", "Dąb słodowy"]
MS_FAQ = [
    ("Czy moskitierę można zamontować na każdym oknie?",
     "Moskitiery można zamontować na większości okien, jednak wybór odpowiedniego rozwiązania zależy od konstrukcji okna, dostępnego miejsca oraz rodzaju zastosowanych osłon zewnętrznych. Przed montażem warto sprawdzić, jaki typ moskitiery będzie najlepiej dopasowany do danej stolarki."),
    ("Jak czyścić i pielęgnować moskitiery?",
     "Moskitiery najlepiej czyścić regularnie miękką szczotką lub odkurzaczem z delikatną końcówką, aby usunąć kurz i zabrudzenia. W razie potrzeby siatkę i profile można przetrzeć miękką ściereczką zwilżoną wodą z łagodnym detergentem. Należy unikać silnych środków chemicznych i szorstkich gąbek, które mogłyby uszkodzić siatkę lub powierzchnię profili. Regularna pielęgnacja pozwala zachować estetyczny wygląd i funkcjonalność moskitiery przez długi czas."),
    ("Czy moskitiery trzeba demontować na zimę?",
     "Nie wszystkie moskitiery wymagają demontażu na zimę. Moskitiery ramkowe warto zdjąć na okres jesienno-zimowy, aby ograniczyć ich narażenie na trudne warunki atmosferyczne. Moskitiery rolowane i plisowane zazwyczaj mogą pozostać zamontowane przez cały rok, zgodnie z zaleceniami producenta."),
    ("Jak działa moskitiera rolowana?",
     "Moskitiera rolowana działa podobnie do rolety – siatkę rozwija się z kasety i przesuwa w prowadnicach, aby zabezpieczyć okno lub drzwi przed owadami. Gdy nie jest potrzebna, można ją zwinąć z powrotem do kasety, dzięki czemu pozostaje schowana i jest chroniona przed zabrudzeniami. To wygodne rozwiązanie, które pozwala korzystać z moskitiery tylko wtedy, gdy jest potrzebna."),
    ("Czy można zamontować moskitierę w oknie z roletą zewnętrzną?",
     "Tak, moskitierę można zamontować w oknie wyposażonym w roletę zewnętrzną. Ważne jest jednak dobranie odpowiedniego rodzaju moskitiery oraz sprawdzenie dostępnego miejsca montażowego. W zależności od konstrukcji okna i rolety możliwe jest zastosowanie m.in. moskitiery ramkowej lub rolowanej. Najlepiej dobrać rozwiązanie już na etapie pomiaru, aby oba systemy mogły działać niezależnie i bez przeszkód."),
    ("Czy moskitiery są odporne na uszkodzenia przez zwierzęta?",
     "Standardowa siatka może ulec uszkodzeniu w kontakcie z pazurami zwierząt. Dlatego oferujemy również mocniejszą siatkę aluminiową, która charakteryzuje się większą odpornością na uszkodzenia mechaniczne."),
    ("Czy moskitiery najlepiej zamontować od razu z oknami, czy dopiero po zakończeniu budowy?",
     "Montaż najlepiej wykonać po zakończeniu prac budowlanych i wykończeniowych, co pozwoli ograniczyć ryzyko zabrudzenia lub uszkodzenia siatki. Dzięki temu moskitiery będą gotowe do użytkowania, gdy tylko zamieszkasz w nowym domu."),
]
MS_INSPIRACJE = ["al27", "al38", "al29", "moskitiera_mrs"]


def build_moskitiery():
    meta = PRODUCT_DATA["moskitiery"]
    rows = ""
    for k, (title, bullets, img, contain) in enumerate(MS_ROWS):
        li = "".join(f'<li><span class="check">{I["check"]}</span> {b}</li>' for b in bullets)
        cls = ' class="img-contain"' if contain else ""
        media = f'<div><img{cls} src="assets/img/{img}.jpg" alt="{title}" loading="lazy"></div>'
        text = f"""<div class="subrow__text">
        <h2>{title}</h2>
        <ul class="bullets">{li}</ul>
        <a class="btn btn--primary btn--sm" href="kontakt.html">Zapytaj o wycenę {I['arrow']}</a>
      </div>"""
        flip = k % 2
        rows += f'<div class="subrow{" subrow--flip" if flip else ""}">{media if not flip else text}{text if not flip else media}</div>'
    spec = PRODUCT_EXTRAS["moskitiery"]["specs"]
    th = "".join(f"<th>{c}</th>" for c in spec["cols"])
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in spec["rows"])
    kolory = _swatch_grid([(f"mosk/kolor-{i:02d}", n) for i, n in enumerate(MS_KOLORY, 1)]).replace('class="swatches-grid"', 'class="swatches-grid swatches-grid--9"', 1)
    body = pagehero(meta["hero"], meta["h1"],
                    "Moskitiery naszej produkcji — na wymiar do każdego typu okna i drzwi. Ciesz się świeżym powietrzem bez nieproszonych gości.", None)
    body += f"""<section class="section section--tight-bottom"><div class="container">{rows}</div></section>
{_anim_section(_plisa_anim(), "Jak działa moskitiera plisowana?", "Siatka złożona w harmonijkę rozkłada się płynnie w otworze — wystarczy przesunąć listwę z uchwytem. Moskitierę można zatrzymać w dowolnym miejscu, a po złożeniu zajmuje tylko kilka centymetrów. Niski próg nie przeszkadza w przechodzeniu na taras.", True)}<section class="section">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">Kolory profili</h2></div></div>
    {kolory}
  </div>
</section>
<section class="section section--soft">
  <div class="container">
    <div class="section-header"><div class="section-header__left"><h2 class="h-sec">{spec["title"]}</h2></div></div>
    <div class="spec-wrap"><table class="spec-table"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>
  </div>
</section>
""" + _std_sections(MS_ADV, MS_FAQ, MS_INSPIRACJE, "Dobierzemy moskitiery do Twoich okien i drzwi", ["okna", "rolety-zewnetrzne", "oslony-wewnetrzne"])
    write("moskitiery.html", head(meta["title"], meta["desc"]) + nav("moskitiery") + body + footer())


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
        elif slug == "pergole":
            build_pergole()
        elif slug == "bramy-garazowe":
            build_bramy()
        elif slug == "markizy":
            build_markizy()
        elif slug == "oslony-wewnetrzne":
            build_oslony_wewnetrzne()
        elif slug == "oslony-zewnetrzne":
            build_oslony_zewnetrzne()
        elif slug == "moskitiery":
            build_moskitiery()
        else:
            product_page(slug, meta)
    build_parapety()
    build_zaluzje_fasadowe()
    build_subpages()
    print("Gotowe.")
