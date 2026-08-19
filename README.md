# PROMYK — strona WWW (Wieluń)

Statyczna strona odwzorowująca projekt z Figmy
(`zPKPXAdqXTeOCVoHReM58U` — 17 ekranów), ze zdjęciami i logo z Dysku Google
(folder „Promyk - Materiały”) oraz tekstami z dokumentów **O nas** i **Dla Inwestora**.

## Uruchomienie

Wystarczy otworzyć `index.html` w przeglądarce (wszystkie ścieżki są względne).
Lokalny serwer (poprawne działanie mapy Google i lazy-loadingu):

```bash
python -m http.server 8777
```

## Struktura

```
index.html              strona główna (slider, statystyki, 10 kategorii, konfigurator-teaser,
                        systemy VEKA/Aluprof, o firmie, partnerzy, opinie, galeria, CTA)
o-nas.html              historia firmy — pełny tekst z dokumentu „O nas”
oferta.html             kafelki 10 kategorii + katalogi PDF do pobrania
konfigurator.html       konfigurator kolorów okien (kolor zewn./wewn., klamka, szprosy)
dla-inwestora.html      pełny tekst „Dla Inwestora” + 5 kroków, grupy odbiorców, FAQ
galeria.html            galeria z filtrami kategorii i „pokaż więcej”
kontakt.html            formularz + dane + mapa
okna.html · drzwi-zewnetrzne.html · drzwi-wewnetrzne.html · rolety-zewnetrzne.html
pergole.html · bramy-garazowe.html · markizy.html · oslony-wewnetrzne.html
oslony-zewnetrzne.html · moskitiery.html      — 10 stron produktowych

assets/css/style.css    style (tokeny 1:1 z Figmy)
assets/js/main.js       slider, menu mobilne, FAQ, filtry galerii, konfigurator
assets/img/             74 zdjęcia z Dysku Google + logo (wersja ciemna i biała)
build.py                generator stron — treść i przypisanie zdjęć w jednym miejscu
```

## Edycja treści

Cała treść i przypisanie zdjęć są w `build.py` (słowniki `PRODUCTS`,
`PRODUCT_DATA`, `GALLERY`, `REVIEWS`). Po zmianie:

```bash
python build.py
```

## Tokeny designu (z Figmy)

| element | wartość |
|---|---|
| akcent — grafit z logo (przyciski, CTA) | `#2f3237` |
| akcent hover | `#1d1f22` |
| stalowy do drobnych akcentów na białym | `#44607b` |
| ciemny (tło sekcji dark/topbar/stopka) | `#232529` |
| tekst pomocniczy | `#6c757d` |
| linie | `#e9ecef` |
| tło sekcji | `#f7f7f7` |
| gwiazdki ocen | `#eaa611` (złoto) |
| czcionka (cała strona) | Urbanist 400–900 (Google Fonts, latin-ext) |
| kontener | 1280 px, padding 80 px |

Cache-busting: linki do CSS/JS mają `?v=N` — po zmianach w assets podbij `ASSET_VER` w `build.py`.

## Do uzupełnienia po stronie klienta

- **Obsługa formularza** — `kontakt.html` ma formularz bez backendu
  (`data-demo` w `main.js` pokazuje tylko komunikat). Podłącz PHP / usługę mailową.
- **Katalogi PDF** — kafelki na `oferta.html` prowadzą do kontaktu; podmień `href`
  na realne pliki, gdy będą dostępne.
- **Zdjęcia markiz** — na Dysku nie ma zdjęć markiz; użyto najbliższych ujęć
  tarasowych/osłonowych Aluprof. Warto podmienić po otrzymaniu materiałów od Selt.
- **Facebook** — link w stopce prowadzi do `facebook.com`, podmień na profil firmy.
- **Logo** — źródło to JPG 758×120 px; wygenerowano z niego PNG z przezroczystym tłem
  (`logo-promyk.png`, `logo-promyk-white.png`). Docelowo warto wgrać wersję wektorową.
- **Loga producentów** — `assets/img/partners/*.svg` to stylizowane odwzorowania
  (VEKA, Aluprof, Somfy, Nice, Selt, Setto, Wikęd, DRE). Przed publikacją podmień je
  na oficjalne pliki z press-kitów producentów (te same nazwy plików — bez zmian w kodzie).

## Konfigurator okien (PRO)

`konfigurator.html` + `assets/js/configurator.js` — okno rysowane na żywo w SVG:

- typ konstrukcji: jednoskrzydłowe / dwuskrzydłowe / drzwi balkonowe / przesuwne HST,
- wymiary (szer./wys. w cm) z przeliczeniem powierzchni,
- kolor od zewnątrz i od wewnątrz (kolory drewnopodobne mają teksturę słojów),
- klamka (4 kolory), szprosy (brak / krzyż / poziome / wielopolowe),
- podgląd na 5 typach elewacji + przełącznik „widok z zewnątrz / od wewnątrz”,
- orientacyjna wycena aktualizowana na żywo (stawki `TYPES[].rate` w `configurator.js`),
- CTA przenosi konfigurację do formularza kontaktowego
  (`kontakt.html?konfiguracja=...` — pole wiadomości wypełnia się automatycznie).

Realizm sceny („żywy obraz”):

- pełna scena elewacji: faktura tynku/cegły/deski (feTurbulence), wnęka okienna,
  cień, parapet 3D, pas tarasu, winieta i smuga słońca,
- w szybach odbija się **prawdziwe zdjęcie** (`SKY_IMG` w `configurator.js`),
  delikatnie dryfujące — obraz stale subtelnie „żyje”,
- od wewnątrz przez okno widać **prawdziwy ogród** (`GARDEN_IMG`, kadr regulowany
  parametrem `box` w `photoInGlass()`),
- pory dnia ☀️/🌆/🌙 w pasku podglądu — nocą okno świeci ciepłym światłem
  z poświatą na elewacji i parapecie,
- parallax za kursorem (warstwy `data-lyr="bg"/"fg"`).

Tryb „📷 Okno VEKA” (fotorealistyczny):

- podgląd to **oficjalne rendery VEKA** — osobne zdjęcie okna dla każdego dekoru
  (`assets/img/veka/win/*.jpg`, 54 dekory), dokładnie jak w narzędziu na veka.pl,
- próbki kolorów to **zdjęcia prawdziwych folii dekoracyjnych**
  (`assets/img/veka/sw/*.jpg`) w 3 grupach: Paleta kolorów / Dekory drewnopodobne
  i metalopodobne / VEKA Spectral,
- dane dekorów: `assets/js/veka-data.js` (id, nazwa PL, grupa, uśredniony kolor
  do sceny SVG) — wygenerowane automatycznie z materiałów VEKA,
- scena „Wizualizacja” barwi ramę uśrednionym kolorem wybranego dekoru
  (drewnopodobne dostają teksturę słojów).

Materiały VEKA pochodzą z publicznego narzędzia kolorów veka.pl — PROMYK jest
autoryzowanym partnerem VEKA; przed publikacją warto potwierdzić zgodę na użycie
(standardowo strefa partnera na to pozwala).

Katalog `_shots/` to robocze zrzuty scen (można skasować). Lokalny podgląd:
`python serve.py` (port 8777; ma endpoint POST /upload używany do zrzutów).
