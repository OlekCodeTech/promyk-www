/* PROMYK — Konfigurator okien PRO
   Naturalna, "żywa" scena: elewacja z fakturą, w szybach odbicie PRAWDZIWEGO
   nieba (wolno dryfujące), od wewnątrz widok prawdziwego ogrodu ze zdjęcia,
   pory dnia (dzień/zmierzch/noc — nocą okno świeci), parallax za kursorem. */
(function () {
  'use strict';

  var root = document.querySelector('[data-config]');
  if (!root) return;

  /* ------------------------------------------------------------ dane ---- */
  var COLORS = {
    'Biel':       { base: '#f4f4f1', dark: '#cfcfc9', wood: false },
    'Antracyt':   { base: '#3d4348', dark: '#24282c', wood: false },
    'Czerń':      { base: '#1e2022', dark: '#0e0f10', wood: false },
    'Brąz':       { base: '#5a3820', dark: '#3a2310', wood: false },
    'Złoty dąb':  { base: '#a8712f', dark: '#7a4e1c', wood: true  },
    'Orzech':     { base: '#54341d', dark: '#372011', wood: true  },
    'Winchester': { base: '#7a5638', dark: '#553922', wood: true  }
  };
  var HANDLES = {
    'Biała': '#f2f2ef', 'Srebrna': '#b9bec4', 'Czarna': '#232426', 'Złota': '#c79a4b'
  };
  var TYPES = {
    jedno:  { label: 'Jednoskrzydłowe', w: 120, h: 140, rate: 1400 },
    dwa:    { label: 'Dwuskrzydłowe',   w: 180, h: 150, rate: 1600 },
    balkon: { label: 'Drzwi balkonowe', w: 100, h: 220, rate: 1700 },
    hst:    { label: 'Przesuwne HST',   w: 300, h: 230, rate: 3200 }
  };
  var SCENES = {
    plaster:    { label: 'Tynk biały',  wall: '#e9e5dc', joint: null },
    grey:       { label: 'Tynk szary',  wall: '#b6b9bc', joint: null },
    anthracite: { label: 'Antracyt',    wall: '#4c5156', joint: null },
    brick:      { label: 'Cegła',       wall: '#a2593f', joint: 'brick' },
    wood:       { label: 'Deska',       wall: '#a97a4d', joint: 'planks' }
  };
  /* zdjęcia użyte jako materiały sceny */
  var SKY_IMG = 'assets/img/brama_avo_dom.jpg';   // niebo z chmurami do odbić w szybie
  var GARDEN_IMG = 'assets/img/al31_rol.jpg';     // widok ogrodu zza okna (wnętrze)

  var TIMES = {
    day:   { overlay: null },
    dusk:  { overlay: ['#e8823c', 0.13] },
    night: { overlay: ['#080e22', 0.44] }
  };

  /* WYŁĄCZNIE zdjęcia OKIEN w zbliżonym odcieniu — bez drzwi i bram. */
  var PHOTO_SETS = {
    biel:     ['wiked03', 'al28', 'al29'],
    antracyt: ['al39', 'al31_rol', 'wiked79'],
    czern:    ['al25', 'al26', 'al27'],
    braz:     ['moskitiera_mrs', 'wiked08', 'abm_okno1']
  };
  function photosFor(id) {
    if (WHITE_IDS[id]) return PHOTO_SETS.biel;
    if (/anthrazit|schiefergrau|quarzgrau|basaltgrau|fernstergrau/.test(id)) return PHOTO_SETS.antracyt;
    if (/graphitschwarz|schwarzbraun/.test(id)) return PHOTO_SETS.czern;
    if (/braun|mooreiche|mahagoni|nussbaum|macor|umbra/.test(id)) return PHOTO_SETS.braz;
    return [];
  }

  var state = {
    type: 'dwa', out: '02_anthrazitgrau', inn: 'Biel', handle: 'Czarna',
    bars: 'Brak', scene: 'plaster', view: 'out', time: 'day', mode: 'scene', w: 180, h: 150
  };

  var preview = root.querySelector('.preview');
  var stageBox = root.querySelector('[data-svg]');
  var VB_W = 1000, VB_H = 700;
  var winGlass = null; // wspólny obszar szklenia całego okna (spójny obraz w wielu skrzydłach)

  /* ---- dekory VEKA (oficjalne rendery okien + próbki folii) ---- */
  var DECORS = window.VEKA_DECORS || [];
  var DECOR = {};
  DECORS.forEach(function (d) { DECOR[d.id] = d; });
  var WHITE_IDS = { '59_papyrusweiss':1, '60_hellelfenbein':1, '61_cremeweiss':1, '62_weiss':1,
    '08_vekaspectral_weiss_ultramatt':1, '09_vekaspectral_reinweiss_ultramatt':1 };
  var GROUP_LABEL = { uni: 'Paleta kolorów', dekor: 'Dekory drewnopodobne i metalopodobne', spectral: 'VEKA Spectral (ultramat)' };

  /* zbuduj karuzele próbek (jak w narzędziu VEKA) */
  root.querySelectorAll('[data-vekagroup]').forEach(function (row) {
    var grp = row.getAttribute('data-vekagroup');
    row.innerHTML = DECORS.filter(function (d) { return d.group === grp; }).map(function (d) {
      return '<button type="button" class="veka-chip" data-value="' + d.id + '" title="' + d.name + '">' +
        '<img src="assets/img/veka/sw/' + d.id + '.jpg" alt="' + d.name + '" loading="lazy"><span>' + d.name + '</span></button>';
    }).join('');
  });

  function renderPhoto() {
    var d = DECOR[state.out];
    if (!d) return;
    stageBox.innerHTML = '<div class="veka-photo"><img src="assets/img/veka/win/' + d.id + '.jpg" alt="Okno VEKA — ' + d.name + '"></div>';
  }

  /* ------------------------------------------------- pomocnicze SVG ---- */
  function woodPattern(id, c) {
    return '<pattern id="' + id + '" width="26" height="220" patternUnits="userSpaceOnUse">' +
      '<rect width="26" height="220" fill="' + c.base + '"/>' +
      '<rect x="3"  width="2.2" height="220" fill="' + c.dark + '" opacity=".38"/>' +
      '<rect x="9"  width="1.2" height="220" fill="' + c.dark + '" opacity=".22"/>' +
      '<rect x="14" width="3"   height="220" fill="' + c.dark + '" opacity=".30"/>' +
      '<rect x="21" width="1.6" height="220" fill="' + c.dark + '" opacity=".18"/>' +
      '</pattern>';
  }

  function frameFill(c, id) {
    if (c.wood) return { defs: woodPattern(id, c), fill: 'url(#' + id + ')', edge: c.dark };
    return { defs: '', fill: c.base, edge: c.dark };
  }

  function shade(hex, f) {
    var n = parseInt(hex.slice(1), 16), r = n >> 16, g = (n >> 8) & 255, b = n & 255;
    r = Math.round(Math.min(255, r * f)); g = Math.round(Math.min(255, g * f)); b = Math.round(Math.min(255, b * f));
    return '#' + (1 << 24 | r << 16 | g << 8 | b).toString(16).slice(1);
  }

  var uid = 0;
  function clip(x, y, w, h, inner) {
    var id = 'c' + (++uid);
    return '<clipPath id="' + id + '"><rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '"/></clipPath>' +
      '<g clip-path="url(#' + id + ')">' + inner + '</g>';
  }

  /* obraz fotograficzny wypełniający obszar całego szklenia (widziany przez wycinek skrzydła);
     box = kadr względem szklenia: {sx, sy, sw, sh} — pozwala celować w konkretny fragment zdjęcia */
  function photoInGlass(href, blur, opacity, pan, box) {
    var g = winGlass;
    box = box || { sx: -0.125, sy: -0.125, sw: 1.25, sh: 1.25 };
    var img = '<image href="' + href + '" x="' + (g.x + g.w * box.sx) + '" y="' + (g.y + g.h * box.sy) +
      '" width="' + (g.w * box.sw) + '" height="' + (g.h * box.sh) + '" preserveAspectRatio="xMidYMid slice"' +
      (blur ? ' filter="url(#refBlur)"' : '') + ' opacity="' + opacity + '">';
    if (pan) {
      img += '<animateTransform attributeName="transform" type="translate" values="0 0;' +
        (-g.w * 0.08) + ' 0;0 0" dur="70s" repeatCount="indefinite"/>';
    }
    return img + '</image>';
  }

  /* ----------------------------------------------------------- szyba ---- */
  function glass(x, y, w, h, interior) {
    var g = '';
    if (interior) {
      /* widok przez szybę na prawdziwy ogród (kadr na trawnik i zieleń) */
      g += '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" fill="#cfd8d3"/>';
      g += photoInGlass(GARDEN_IMG, false, 1, false, { sx: -1.62, sy: -0.6, sw: 2.7, sh: 2.3 });
      if (state.time === 'dusk') g += '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" fill="#c76b2e" opacity=".22"/>';
      if (state.time === 'night') g += '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" fill="#0a1226" opacity=".78"/>';
      g += '<polygon points="' + (x + w * 0.1) + ',' + y + ' ' + (x + w * 0.22) + ',' + y + ' ' + (x + w * 0.02) + ',' + (y + h) + ' ' + x + ',' + (y + h) + '" fill="#fff" opacity=".07"/>';
    } else if (state.time === 'night') {
      /* noc: okno świeci ciepłym światłem od środka */
      g += '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" fill="url(#warmGlass)"/>';
      g += '<ellipse cx="' + (x + w * 0.5) + '" cy="' + (y + h * 0.4) + '" rx="' + w * 0.62 + '" ry="' + h * 0.52 + '" fill="#fff2cf" opacity=".3"/>';
      g += '<polygon points="' + (x + w * 0.14) + ',' + y + ' ' + (x + w * 0.28) + ',' + y + ' ' + (x + w * 0.05) + ',' + (y + h) + ' ' + (x - w * 0.02) + ',' + (y + h) + '" fill="#fff" opacity=".10"/>';
    } else {
      /* dzień/zmierzch: w szybie odbija się prawdziwe niebo (delikatnie dryfuje) */
      g += '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" fill="url(#skyBase)"/>';
      g += photoInGlass(SKY_IMG, true, 0.5, true);
      g += '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" fill="url(#skyBase)" opacity=".35"/>';
      if (state.time === 'dusk') {
        g += '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" fill="#d97638" opacity=".28"/>';
      }
      g += '<polygon points="' + (x + w * 0.14) + ',' + y + ' ' + (x + w * 0.3) + ',' + y + ' ' + (x + w * 0.06) + ',' + (y + h) + ' ' + (x - w * 0.02) + ',' + (y + h) + '" fill="#fff" opacity=".14"/>';
      g += '<polygon points="' + (x + w * 0.44) + ',' + y + ' ' + (x + w * 0.5) + ',' + y + ' ' + (x + w * 0.2) + ',' + (y + h) + ' ' + (x + w * 0.16) + ',' + (y + h) + '" fill="#fff" opacity=".08"/>';
      g += '<rect x="' + x + '" y="' + (y + h * 0.55) + '" width="' + w + '" height="' + (h * 0.45) + '" fill="#1c2126" opacity=".18"/>';
    }
    /* wewnętrzny cień szklenia — głębia osadzenia */
    g += '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + Math.min(10, h * 0.06) + '" fill="#000" opacity=".16"/>';
    g += '<rect x="' + x + '" y="' + y + '" width="' + Math.min(7, w * 0.04) + '" height="' + h + '" fill="#000" opacity=".10"/>';
    return clip(x, y, w, h, g);
  }

  /* --------------------------------------------------------- klamka ---- */
  function handleSvg(cx, cy, color) {
    return '<g filter="url(#tinyShadow)">' +
      '<rect x="' + (cx - 5) + '" y="' + (cy - 15) + '" width="10" height="30" rx="4" fill="' + color + '" stroke="rgba(0,0,0,.4)" stroke-width=".7"/>' +
      '<rect x="' + (cx - 4) + '" y="' + (cy - 3) + '" width="8" height="40" rx="4" fill="' + color + '" stroke="rgba(0,0,0,.4)" stroke-width=".7"/>' +
      '<rect x="' + (cx - 2.6) + '" y="' + (cy - 1) + '" width="2.4" height="34" rx="1.2" fill="#fff" opacity=".22"/>' +
      '</g>';
  }

  /* ------------------------------------------------------- szprosy ---- */
  function barsRects(x, y, w, h, kind, t, fill) {
    var out = '';
    function rect(rx, ry, rw, rh) {
      out += '<rect x="' + rx + '" y="' + ry + '" width="' + rw + '" height="' + rh +
        '" fill="' + fill + '" stroke="rgba(0,0,0,.3)" stroke-width=".6"/>';
    }
    if (kind === 'Krzyż' || kind === 'Poziome') rect(x, y + h / 2 - t / 2, w, t);
    if (kind === 'Krzyż') rect(x + w / 2 - t / 2, y, t, h);
    if (kind === 'Wielopolowe') {
      rect(x + w / 3 - t / 2, y, t, h); rect(x + 2 * w / 3 - t / 2, y, t, h);
      rect(x, y + h / 3 - t / 2, w, t); rect(x, y + 2 * h / 3 - t / 2, w, t);
    }
    return out;
  }

  /* ------------------------------------------------------- skrzydło ---- */
  function sash(x, y, w, h, ff, sashW, interior, withHandle, handleSide, barsKind) {
    var s = '';
    s += '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" fill="' + ff.fill + '" stroke="' + ff.edge + '" stroke-width="1.2"/>';
    s += '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="2.4" fill="#fff" opacity=".20"/>';
    s += '<rect x="' + x + '" y="' + y + '" width="2.4" height="' + h + '" fill="#fff" opacity=".14"/>';
    s += '<rect x="' + x + '" y="' + (y + h - 2.4) + '" width="' + w + '" height="2.4" fill="#000" opacity=".26"/>';
    s += '<rect x="' + (x + w - 2.4) + '" y="' + y + '" width="2.4" height="' + h + '" fill="#000" opacity=".2"/>';
    var gx = x + sashW, gy = y + sashW, gw = w - 2 * sashW, gh = h - 2 * sashW;
    s += '<rect x="' + (x + sashW * 0.45) + '" y="' + (y + sashW * 0.45) + '" width="' + (w - sashW * 0.9) + '" height="' + (h - sashW * 0.9) + '" fill="none" stroke="rgba(0,0,0,.28)" stroke-width="1"/>';
    s += glass(gx, gy, gw, gh, interior);
    s += '<rect x="' + gx + '" y="' + gy + '" width="' + gw + '" height="' + gh + '" fill="none" stroke="rgba(0,0,0,.38)" stroke-width="1.1"/>';
    if (barsKind && barsKind !== 'Brak') s += barsRects(gx, gy, gw, gh, barsKind, 5, ff.fill);
    if (withHandle) {
      var hx = handleSide === 'left' ? x + sashW / 2 : x + w - sashW / 2;
      s += handleSvg(hx, y + h / 2, HANDLES[state.handle]);
    }
    return s;
  }

  /* ------------------------------------------------------- samo okno ---- */
  function windowSvg(W, H, interior) {
    var spec = interior ? COLORS[state.inn] : (DECOR[state.out] || COLORS['Antracyt']);
    var ff = frameFill(spec, 'wf');
    var FR = Math.max(12, Math.min(20, W * 0.045));
    var SW = FR * 0.9;
    var svg = ff.defs;
    svg += '<rect x="0" y="0" width="' + W + '" height="' + H + '" rx="2" fill="' + ff.fill + '" stroke="' + ff.edge + '" stroke-width="1.4"/>';
    svg += '<rect x="0" y="0" width="' + W + '" height="2.6" fill="#fff" opacity=".22"/>';
    svg += '<rect x="0" y="' + (H - 2.6) + '" width="' + W + '" height="2.6" fill="#000" opacity=".28"/>';
    var ix = FR, iy = FR, iw = W - 2 * FR, ih = H - 2 * FR;
    winGlass = { x: ix, y: iy, w: iw, h: ih };

    if (state.type === 'jedno' || state.type === 'balkon') {
      svg += sash(ix, iy, iw, ih, ff, SW, interior, true, 'right', state.bars);
    } else if (state.type === 'dwa') {
      var half = iw / 2;
      svg += sash(ix, iy, half - 1, ih, ff, SW, interior, true, 'right', state.bars);
      svg += sash(ix + half + 1, iy, half - 1, ih, ff, SW, interior, true, 'left', state.bars);
      svg += '<rect x="' + (ix + half - 2.5) + '" y="' + iy + '" width="5" height="' + ih + '" fill="' + ff.edge + '" opacity=".55"/>';
    } else if (state.type === 'hst') {
      var fixed = iw * 0.55, slide = iw * 0.45;
      svg += sash(ix, iy, fixed, ih, ff, SW * 0.66, interior, false, null, state.bars);
      svg += '<g transform="translate(0,-3)">' +
        '<rect x="' + (ix + fixed - 8) + '" y="' + (iy + 2) + '" width="' + (slide + 8) + '" height="' + (ih + 4) + '" fill="rgba(0,0,0,.24)" rx="2"/>' +
        sash(ix + fixed - 4, iy - 2, slide + 4, ih + 6, ff, SW * 0.85, interior, true, 'left', state.bars) +
        '</g>';
    }
    return svg;
  }

  /* ------------------------------------------------------ cała scena ---- */
  function drawScene() {
    uid = 0;
    var interior = state.view === 'in';
    var sc = SCENES[state.scene];
    var T = TIMES[state.time];

    var maxW = VB_W * (state.type === 'hst' ? 0.62 : 0.5);
    var maxH = VB_H * 0.58;
    var pxPerCm = Math.min(maxW / state.w, maxH / state.h);
    var W = state.w * pxPerCm, H = state.h * pxPerCm;
    var groundY = VB_H * 0.80;
    var x = (VB_W - W) / 2;
    var isDoor = (state.type === 'balkon' || state.type === 'hst');
    var y = interior
      ? (isDoor ? VB_H * 0.74 - H : VB_H * 0.70 - H)
      : (isDoor ? groundY - H + 6 : groundY - H - 56);

    var defs = '<defs>' +
      '<linearGradient id="skyBase" x1="0" y1="0" x2=".35" y2="1">' +
      '<stop offset="0" stop-color="#aecfe3"/><stop offset=".45" stop-color="#cfe4ef"/><stop offset="1" stop-color="#8fb0c4"/></linearGradient>' +
      '<linearGradient id="warmGlass" x1="0" y1="0" x2=".3" y2="1">' +
      '<stop offset="0" stop-color="#ffe6ab"/><stop offset=".6" stop-color="#f7c368"/><stop offset="1" stop-color="#dfa244"/></linearGradient>' +
      '<linearGradient id="sunlight" x1="0" y1="0" x2="1" y2="1">' +
      '<stop offset="0" stop-color="#fff" stop-opacity=".14"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>' +
      '<radialGradient id="vignette" cx=".5" cy=".45" r=".75">' +
      '<stop offset=".62" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".16"/></radialGradient>' +
      '<linearGradient id="pave" x1="0" y1="0" x2="0" y2="1">' +
      '<stop offset="0" stop-color="#c9c5bc"/><stop offset="1" stop-color="#aaa79f"/></linearGradient>' +
      '<linearGradient id="floorG" x1="0" y1="0" x2="0" y2="1">' +
      '<stop offset="0" stop-color="#c09468"/><stop offset="1" stop-color="#8f6a42"/></linearGradient>' +
      '<linearGradient id="sillShade" x1="0" y1="0" x2="0" y2="1">' +
      '<stop offset="0" stop-color="#000" stop-opacity=".3"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>' +
      '<filter id="grain" x="0" y="0" width="100%" height="100%">' +
      '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/>' +
      '<feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .05 0"/></filter>' +
      '<filter id="blotch" x="0" y="0" width="100%" height="100%">' +
      '<feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="3" stitchTiles="stitch"/>' +
      '<feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .04 0"/></filter>' +
      '<filter id="winShadow" x="-20%" y="-20%" width="140%" height="150%">' +
      '<feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#000" flood-opacity=".34"/></filter>' +
      '<filter id="tinyShadow" x="-60%" y="-60%" width="220%" height="220%">' +
      '<feDropShadow dx="1" dy="2" stdDeviation="1.6" flood-color="#000" flood-opacity=".35"/></filter>' +
      '<filter id="refBlur"><feGaussianBlur stdDeviation="1.4"/></filter>' +
      '<filter id="blurGlow" x="-60%" y="-60%" width="220%" height="220%">' +
      '<feGaussianBlur stdDeviation="26"/></filter>' +
      '</defs>';

    var s = '';

    if (interior) {
      /* ---------- WNĘTRZE ---------- */
      var floorY = VB_H * 0.72;
      s += '<g data-lyr="bg">';
      s += '<rect x="-40" y="-40" width="' + (VB_W + 80) + '" height="' + (VB_H + 80) + '" fill="#efe9e0"/>';
      s += '<rect x="-40" y="-40" width="' + (VB_W + 80) + '" height="' + (floorY + 40) + '" filter="url(#grain)"/>';
      s += '<rect x="-40" y="-40" width="' + (VB_W + 80) + '" height="' + (floorY + 40) + '" filter="url(#blotch)"/>';
      s += '<rect x="-40" y="' + floorY + '" width="' + (VB_W + 80) + '" height="' + (VB_H - floorY + 40) + '" fill="url(#floorG)"/>';
      for (var i = 0; i < 6; i++) {
        var fy = floorY + (VB_H - floorY) * (i / 6);
        s += '<rect x="-40" y="' + fy + '" width="' + (VB_W + 80) + '" height="1.2" fill="#5f4630" opacity="' + (0.25 + i * 0.04) + '"/>';
      }
      for (var j = 0; j < 9; j++) {
        s += '<rect x="' + ((j * 137 + (j % 2) * 60) % VB_W) + '" y="' + (floorY + (VB_H - floorY) * ((j % 3) / 3)) + '" width="1" height="' + (VB_H - floorY) / 3 + '" fill="#5f4630" opacity=".2"/>';
      }
      s += '<rect x="-40" y="' + (floorY - 9) + '" width="' + (VB_W + 80) + '" height="9" fill="#e6dfd4"/><rect x="-40" y="' + (floorY - 9) + '" width="' + (VB_W + 80) + '" height="1.4" fill="#000" opacity=".12"/>';
      s += '<ellipse cx="' + (x + W / 2) + '" cy="' + (floorY + (VB_H - floorY) * 0.45) + '" rx="' + W * 0.72 + '" ry="' + (VB_H - floorY) * 0.42 + '" fill="' + (state.time === 'night' ? '#ffdf9e' : '#fff') + '" opacity="' + (state.time === 'night' ? '.1' : '.06') + '"/>';
      s += '</g>';

      s += '<g data-lyr="fg">';
      s += '<rect x="' + (x - 7) + '" y="' + (y - 7) + '" width="' + (W + 14) + '" height="' + (H + 14) + '" fill="#d8d1c5"/>';
      s += '<rect x="' + (x - 7) + '" y="' + (y - 7) + '" width="' + (W + 14) + '" height="3" fill="#000" opacity=".18"/>';
      s += '<g filter="url(#winShadow)" transform="translate(' + x + ',' + y + ')">' + windowSvg(W, H, true) + '</g>';
      if (!isDoor) {
        s += '<rect x="' + (x - 20) + '" y="' + (y + H + 7) + '" width="' + (W + 40) + '" height="13" rx="2" fill="#f3efe8" stroke="#cfc8bb" stroke-width="1"/>';
        s += '<rect x="' + (x - 20) + '" y="' + (y + H + 20) + '" width="' + (W + 40) + '" height="16" fill="url(#sillShade)" opacity=".5"/>';
      }
      s += '</g>';
      if (state.time === 'night') s += '<rect x="-40" y="-40" width="' + (VB_W + 80) + '" height="' + (VB_H + 80) + '" fill="#1a1206" opacity=".18"/>';
      if (state.time === 'dusk') s += '<rect x="-40" y="-40" width="' + (VB_W + 80) + '" height="' + (VB_H + 80) + '" fill="#e88f4e" opacity=".08"/>';
    } else {
      /* ---------- ELEWACJA ---------- */
      s += '<g data-lyr="bg">';
      s += '<rect x="-40" y="-40" width="' + (VB_W + 80) + '" height="' + (VB_H + 80) + '" fill="' + sc.wall + '"/>';
      if (sc.joint === 'brick') {
        var bw = 64, bh = 26;
        for (var r = 0; r * bh < groundY + bh; r++) {
          s += '<rect x="-40" y="' + (r * bh) + '" width="' + (VB_W + 80) + '" height="1.6" fill="#7c4630" opacity=".55"/>';
          var off = (r % 2) * (bw / 2);
          for (var q = 0; q * bw < VB_W + bw; q++) {
            s += '<rect x="' + (q * bw + off - 40) + '" y="' + (r * bh) + '" width="1.6" height="' + bh + '" fill="#7c4630" opacity=".45"/>';
          }
        }
      } else if (sc.joint === 'planks') {
        for (var p = 0; p * 46 < VB_W + 86; p++) {
          s += '<rect x="' + (p * 46 - 40) + '" y="-40" width="2" height="' + (groundY + 40) + '" fill="#7d5836" opacity=".5"/>';
          s += '<rect x="' + (p * 46 - 20) + '" y="-40" width="1" height="' + (groundY + 40) + '" fill="#7d5836" opacity=".22"/>';
        }
      }
      s += '<rect x="-40" y="-40" width="' + (VB_W + 80) + '" height="' + (groundY + 40) + '" filter="url(#grain)"/>';
      s += '<rect x="-40" y="-40" width="' + (VB_W + 80) + '" height="' + (groundY + 40) + '" filter="url(#blotch)"/>';
      // przybrudzenie przy gruncie — naturalne ślady
      s += '<rect x="-40" y="' + (groundY - 26) + '" width="' + (VB_W + 80) + '" height="26" fill="#000" opacity=".05"/>';
      s += '<rect x="-40" y="' + groundY + '" width="' + (VB_W + 80) + '" height="' + (VB_H - groundY + 40) + '" fill="url(#pave)"/>';
      s += '<rect x="-40" y="' + groundY + '" width="' + (VB_W + 80) + '" height="4" fill="#000" opacity=".22"/>';
      for (var k = 0; k < 8; k++) {
        s += '<rect x="' + (k * 140 + 30) + '" y="' + groundY + '" width="1.4" height="' + (VB_H - groundY) + '" fill="#8b877e" opacity=".6"/>';
      }
      s += '<rect x="-40" y="' + (groundY + (VB_H - groundY) * 0.5) + '" width="' + (VB_W + 80) + '" height="1.4" fill="#8b877e" opacity=".6"/>';
      s += '</g>';

      s += '<g data-lyr="fg">';
      if (state.time === 'night') {
        s += '<rect x="' + (x - 30) + '" y="' + (y - 24) + '" width="' + (W + 60) + '" height="' + (H + 70) + '" rx="18" fill="#ffcf7e" opacity=".38" filter="url(#blurGlow)"/>';
      }
      s += '<rect x="' + (x - 8) + '" y="' + (y - 8) + '" width="' + (W + 16) + '" height="' + (H + 16) + '" fill="' + shade(sc.wall, 0.72) + '"/>';
      s += '<rect x="' + (x - 8) + '" y="' + (y - 8) + '" width="' + (W + 16) + '" height="4" fill="#000" opacity=".22"/>';
      s += '<g filter="url(#winShadow)" transform="translate(' + x + ',' + y + ')">' + windowSvg(W, H, false) + '</g>';
      var sy = y + H + 8;
      s += '<rect x="' + (x - 14) + '" y="' + (sy - 3) + '" width="' + (W + 28) + '" height="4" fill="#d8dadc"/>';
      s += '<rect x="' + (x - 14) + '" y="' + (sy + 1) + '" width="' + (W + 28) + '" height="9" rx="1.5" fill="#b9bdc1" stroke="#96999d" stroke-width=".8"/>';
      s += '<rect x="' + (x - 14) + '" y="' + (sy + 10) + '" width="' + (W + 28) + '" height="22" fill="url(#sillShade)"/>';
      if (state.time === 'night') {
        s += '<ellipse cx="' + (x + W / 2) + '" cy="' + (groundY + 8) + '" rx="' + (W * 0.75) + '" ry="16" fill="#ffcf7e" opacity=".18" filter="url(#blurGlow)"/>';
      }
      s += '</g>';

      if (state.time === 'day') s += '<rect x="-40" y="-40" width="' + (VB_W + 80) + '" height="' + (VB_H + 80) + '" fill="url(#sunlight)"/>';
      if (T.overlay) s += '<rect x="-40" y="-40" width="' + (VB_W + 80) + '" height="' + (VB_H + 80) + '" fill="' + T.overlay[0] + '" opacity="' + T.overlay[1] + '"/>';
    }
    s += '<rect x="-40" y="-40" width="' + (VB_W + 80) + '" height="' + (VB_H + 80) + '" fill="url(#vignette)"/>';

    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + VB_W + ' ' + VB_H + '" preserveAspectRatio="xMidYMid slice">' + defs + s + '</svg>';
  }

  /* ------------------------------------------------------ wycena ---- */
  function estimate() {
    var area = Math.max(0.5, (state.w * state.h) / 10000);
    var mult = 1;
    if (!WHITE_IDS[state.out]) mult += 0.12;
    if (state.inn !== 'Biel') mult += 0.08;
    var price = TYPES[state.type].rate * area * mult;
    if (state.bars !== 'Brak') price += 160;
    if (state.handle === 'Złota') price += 60;
    return { area: area, price: Math.round(price / 10) * 10 };
  }

  /* ------------------------------------------------------ render ---- */
  function summaryText() {
    return TYPES[state.type].label + ' ' + state.w + '×' + state.h + ' cm | Zewn.: ' + (DECOR[state.out] ? DECOR[state.out].name : state.out) +
      ' | Wewn.: ' + state.inn + ' | Klamka: ' + state.handle + ' | Szprosy: ' + state.bars;
  }

  function render() {
    var e = estimate();
    var dims = root.querySelector('[data-dims]');

    root.classList.toggle('is-photo-mode', state.mode === 'photo');
    if (state.mode === 'photo') {
      preview.className = 'preview is-photo';
      renderPhoto();
      if (dims) dims.innerHTML = 'Okno VEKA — dekor: <span>' + (DECOR[state.out] ? DECOR[state.out].name : '') + '</span>';
    } else {
      stageBox.innerHTML = drawScene();
      preview.className = 'preview' + (state.view === 'in' ? ' is-interior' : '');
      if (dims) dims.innerHTML = '<span>' + state.w + ' × ' + state.h + ' cm</span> &nbsp;•&nbsp; ' + e.area.toFixed(2).replace('.', ',') + ' m²';
    }

    root.querySelectorAll('[data-price]').forEach(function (est) {
      est.textContent = 'od ' + e.price.toLocaleString('pl-PL') + ' zł';
    });

    var rc = root.querySelector('[data-recap]');
    if (rc) {
      rc.innerHTML =
        '<dt>Typ konstrukcji</dt><dd>' + TYPES[state.type].label + '</dd>' +
        '<dt>Wymiary</dt><dd>' + state.w + ' × ' + state.h + ' cm (' + e.area.toFixed(2).replace('.', ',') + ' m²)</dd>' +
        '<dt>Kolor zewnętrzny</dt><dd>' + (DECOR[state.out] ? DECOR[state.out].name : state.out) + '</dd>' +
        '<dt>Kolor wewnętrzny</dt><dd>' + state.inn + '</dd>' +
        '<dt>Klamka</dt><dd>' + state.handle + '</dd>' +
        '<dt>Szprosy</dt><dd>' + state.bars + '</dd>';
    }

    root.querySelectorAll('[data-group]').forEach(function (g) {
      var key = g.getAttribute('data-group');
      var lbl = g.querySelector('.picked');
      if (!lbl) return;
      var map = { type: TYPES[state.type].label, out: (DECOR[state.out] ? DECOR[state.out].name : state.out), in: state.inn, handle: state.handle, bars: state.bars };
      if (map[key]) lbl.textContent = map[key];
    });

    var ph = root.querySelector('[data-photos]');
    if (ph) {
      var imgs = photosFor(state.out);
      var wrap = ph.closest('.cfg-photos');
      if (wrap) wrap.classList.toggle('is-empty', imgs.length === 0);
      ph.innerHTML = imgs.map(function (n) {
        return '<a href="assets/img/' + n + '.jpg" target="_blank" rel="noopener">' +
          '<img src="assets/img/' + n + '.jpg" alt="Okno w kolorze ' + state.out + '" loading="lazy"></a>';
      }).join('');
      var pc = root.querySelector('[data-photocolor]');
      if (pc) pc.textContent = (DECOR[state.out] ? DECOR[state.out].name : state.out);
    }

    root.querySelectorAll('[data-cta]').forEach(function (cta) {
      cta.href = 'kontakt.html?konfiguracja=' + encodeURIComponent(summaryText());
    });
  }

  /* ------------------------------------------------------ zdarzenia ---- */
  root.querySelectorAll('[data-group]').forEach(function (group) {
    var key = group.getAttribute('data-group');
    group.querySelectorAll('[data-value]').forEach(function (opt) {
      opt.addEventListener('click', function () {
        group.querySelectorAll('[data-value]').forEach(function (o) { o.classList.remove('is-active'); });
        opt.classList.add('is-active');
        var v = opt.getAttribute('data-value');
        if (key === 'type') {
          state.type = v;
          state.w = TYPES[v].w; state.h = TYPES[v].h;
          var wi = root.querySelector('[data-w]'), hi = root.querySelector('[data-h]');
          if (wi) wi.value = state.w;
          if (hi) hi.value = state.h;
        }
        else if (key === 'out') state.out = v;
        else if (key === 'in') state.inn = v;
        else if (key === 'handle') state.handle = v;
        else if (key === 'bars') state.bars = v;
        render();
      });
    });
  });

  root.querySelectorAll('[data-scene]').forEach(function (b) {
    b.addEventListener('click', function () {
      root.querySelectorAll('[data-scene]').forEach(function (o) { o.classList.remove('is-active'); });
      b.classList.add('is-active');
      state.scene = b.getAttribute('data-scene');
      if (state.view === 'in') { state.view = 'out'; syncView(); }
      render();
    });
  });

  /* tryb podglądu: scena / żywe zdjęcie */
  root.querySelectorAll('[data-mode]').forEach(function (b) {
    b.addEventListener('click', function () {
      root.querySelectorAll('[data-mode]').forEach(function (o) { o.classList.remove('is-active'); });
      b.classList.add('is-active');
      state.mode = b.getAttribute('data-mode');
      render();
    });
  });

  /* pora dnia */
  root.querySelectorAll('[data-time]').forEach(function (b) {
    b.addEventListener('click', function () {
      root.querySelectorAll('[data-time]').forEach(function (o) { o.classList.remove('is-active'); });
      b.classList.add('is-active');
      state.time = b.getAttribute('data-time');
      render();
    });
  });

  function syncView() {
    root.querySelectorAll('[data-view]').forEach(function (b) {
      b.classList.toggle('is-active', b.getAttribute('data-view') === state.view);
    });
  }
  root.querySelectorAll('[data-view]').forEach(function (b) {
    b.addEventListener('click', function () {
      state.view = b.getAttribute('data-view');
      syncView();
      render();
    });
  });

  var wIn = root.querySelector('[data-w]'), hIn = root.querySelector('[data-h]');
  function clamp(v, lo, hi) { v = parseInt(v, 10); if (isNaN(v)) return lo; return Math.max(lo, Math.min(hi, v)); }
  if (wIn) wIn.addEventListener('input', function () { state.w = clamp(wIn.value, 50, 400); render(); });
  if (hIn) hIn.addEventListener('input', function () { state.h = clamp(hIn.value, 50, 280); render(); });

  /* parallax podążający za kursorem — obraz delikatnie „żyje” */
  preview.addEventListener('mousemove', function (ev) {
    var r = preview.getBoundingClientRect();
    var dx = (ev.clientX - r.left) / r.width - 0.5;
    var dy = (ev.clientY - r.top) / r.height - 0.5;
    var bg = preview.querySelector('[data-lyr="bg"]');
    var fg = preview.querySelector('[data-lyr="fg"]');
    if (bg) bg.setAttribute('transform', 'translate(' + (-dx * 8).toFixed(1) + ',' + (-dy * 4).toFixed(1) + ')');
    if (fg) fg.setAttribute('transform', 'translate(' + (-dx * 18).toFixed(1) + ',' + (-dy * 9).toFixed(1) + ')');
  });
  preview.addEventListener('mouseleave', function () {
    ['bg', 'fg'].forEach(function (n) {
      var g = preview.querySelector('[data-lyr="' + n + '"]');
      if (g) g.setAttribute('transform', 'translate(0,0)');
    });
  });

  render();
})();
