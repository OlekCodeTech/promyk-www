"""Wgrywanie strony PROMYK na serwer (FTP z szyfrowaniem TLS) — DirectAdmin, promyk.wielun.pl.

    python deploy_ftp.py              # pyta o hasło, przenosi stary WordPress do stary-wp-RRRRMMDD i wgrywa stronę
    python deploy_ftp.py --tylko-pliki  # tylko wgrywa/aktualizuje pliki (bez ruszania starej strony)

Hasło wpisujesz sam w terminalu (nie jest nigdzie zapisywane).
Cofnięcie: w Menedżerze plików DirectAdmin zmień nazwę public_html -> public_html-nowa, a stary-wp-RRRRMMDD -> public_html.
"""
import ftplib, getpass, os, sys, datetime, posixpath

HOST = "promyk.wielun.pl"
USER = os.environ.get("PROMYK_FTP_USER", "promyk")
DOMAIN_DIR = "domains/promyk.wielun.pl"
ROOT = os.path.dirname(os.path.abspath(__file__))


def files_to_upload():
    import glob
    out = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.html")))
    out += ["kontakt.php", ".htaccess", "sitemap.xml", "robots.txt"]
    for base, _d, fns in os.walk(os.path.join(ROOT, "assets")):
        for fn in sorted(fns):
            out.append(os.path.relpath(os.path.join(base, fn), ROOT).replace(os.sep, "/"))
    return out


def exists(ftp, path):
    try:
        ftp.cwd(path); ftp.cwd("/"); return True
    except ftplib.error_perm:
        return False


def main():
    only_files = "--tylko-pliki" in sys.argv
    print(f"Serwer: {HOST}, użytkownik: {USER}")
    pwd = getpass.getpass("Hasło FTP (nie będzie widoczne): ")
    ftp = ftplib.FTP_TLS(HOST, timeout=60)
    ftp.login(USER, pwd)
    ftp.prot_p()
    ftp.encoding = "utf-8"
    print("Zalogowano. Katalog domowy:", ftp.pwd())

    base = DOMAIN_DIR if exists(ftp, "/" + DOMAIN_DIR) else ""
    target = posixpath.join("/", base, "public_html")
    print("Docelowy katalog strony:", target)

    if not only_files:
        stamp = datetime.date.today().strftime("%Y%m%d")
        backup = posixpath.join("/", base, f"stary-wp-{stamp}")
        if exists(ftp, backup):
            print(f"Kopia {backup} już istnieje — nie przenoszę ponownie.")
        else:
            print(f"\nStara strona (WordPress) zostanie PRZENIESIONA (nie usunięta): {target} -> {backup}")
            if input("Wpisz TAK, aby kontynuować: ").strip().upper() != "TAK":
                print("Przerwano."); ftp.quit(); return
            ftp.rename(target, backup)
            ftp.mkd(target)
            print("Przeniesiono. Utworzono pusty", target)

    files = files_to_upload()
    made = set()
    for i, rel in enumerate(files, 1):
        remote = posixpath.join(target, rel)
        d = posixpath.dirname(remote)
        parts = []
        while d not in made and d != target and d != "/":
            parts.append(d); d = posixpath.dirname(d)
        for p in reversed(parts):
            try: ftp.mkd(p)
            except ftplib.error_perm: pass
            made.add(p)
        with open(os.path.join(ROOT, rel), "rb") as fh:
            ftp.storbinary("STOR " + remote, fh)
        if i % 50 == 0 or i == len(files):
            print(f"  wgrano {i}/{len(files)}")
    ftp.quit()
    print("\nGotowe! Sprawdź: https://promyk.wielun.pl (odśwież Ctrl+F5).")


if __name__ == "__main__":
    main()
