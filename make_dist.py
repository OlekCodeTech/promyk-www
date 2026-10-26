"""Paczka produkcyjna PROMYK dla hostingu home.pl (https://promyk.wielun.pl).

Uruchom po `python build.py`:
    python make_dist.py            # sitemap.xml + robots.txt + lista plików do wgrania
    python make_dist.py --zip D:\\  # dodatkowo ZIP do wgrania (zapisany we wskazanym folderze)

Na serwer (public_html) wgrywamy: wszystkie *.html, kontakt.php, .htaccess, sitemap.xml, robots.txt i folder assets/.
NIE wgrywamy: build.py, make_dist.py, serve.py, README.md, _shots/, .git/.
"""
import os, sys, zipfile, glob, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://promyk.wielun.pl"

pages = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.html")))
today = datetime.date.today().isoformat()
urls = []
for p in pages:
    if p == "404.html":
        continue
    loc = DOMAIN + "/" + ("" if p == "index.html" else p)
    prio = "1.0" if p == "index.html" else ("0.3" if p.startswith("polityka") else "0.8")
    urls.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><priority>{prio}</priority></url>")
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")
with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")

files = pages + ["kontakt.php", ".htaccess", "sitemap.xml", "robots.txt", "favicon.ico", "site.webmanifest"]
for base, _dirs, fns in os.walk(os.path.join(ROOT, "assets")):
    for fn in fns:
        files.append(os.path.relpath(os.path.join(base, fn), ROOT).replace(os.sep, "/"))
size = sum(os.path.getsize(os.path.join(ROOT, f)) for f in files)
print(f"Do wgrania: {len(files)} plików ({len(pages)} stron), {size / 1e6:.0f} MB")

if "--zip" in sys.argv:
    out_dir = sys.argv[sys.argv.index("--zip") + 1]
    zp = os.path.join(out_dir, "promyk-produkcja.zip")
    # ZIP przez zipfile (ścieżki z ukośnikami /), z kontrolą testzip()
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            z.write(os.path.join(ROOT, f), f)
    with zipfile.ZipFile(zp) as z:
        assert z.testzip() is None
    print(f"ZIP: {zp} ({os.path.getsize(zp) / 1e6:.0f} MB)")
