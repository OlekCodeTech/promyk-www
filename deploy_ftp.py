"""Wgrywanie strony PROMYK na serwer (FTP z szyfrowaniem TLS) — DirectAdmin, promyk.wielun.pl.

    python deploy_ftp.py              # pyta o hasło, przenosi stary WordPress do stary-wp-RRRRMMDD i wgrywa stronę
    python deploy_ftp.py --tylko-pliki  # tylko wgrywa/aktualizuje pliki (bez ruszania starej strony)

Hasło wpisujesz sam w terminalu (nie jest nigdzie zapisywane).
Cofnięcie: w Menedżerze plików DirectAdmin zmień nazwę public_html -> public_html-nowa, a stary-wp-RRRRMMDD -> public_html.
"""
import ftplib, getpass, os, sys, datetime, posixpath, ssl

HOST = "s139.cyber-folks.pl"   # serwer cyber_Folks (certyfikat *.cyber-folks.pl)
USER = os.environ.get("PROMYK_FTP_USER", "wdrozenie@promyk.wielun.pl")
DOMAIN_DIR = "domains/promyk.wielun.pl"
ROOT = os.path.dirname(os.path.abspath(__file__))


def make_ctx():
    # TLS 1.2 + sesje po ID (bez biletów) - ProFTPD akceptuje wtedy wznowienie sesji na kanale danych
    ctx = ssl.create_default_context()
    ctx.maximum_version = ssl.TLSVersion.TLSv1_2
    ctx.options |= ssl.OP_NO_TICKET
    return ctx


class ReusedSessionFTP_TLS(ftplib.FTP_TLS):
    """ProFTPD na cyber_Folks wymaga, by kanał danych używał tej samej sesji TLS co kanał sterujący."""
    def ntransfercmd(self, cmd, rest=None):
        conn, size = ftplib.FTP.ntransfercmd(self, cmd, rest)
        if self._prot_p:
            conn = self.context.wrap_socket(conn, server_hostname=self.host, session=self.sock.session)
        return conn, size


def files_to_upload():
    import glob
    out = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.html")))
    out += ["kontakt.php", ".htaccess", "sitemap.xml", "robots.txt", "favicon.ico", "site.webmanifest"]
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
    folder = sys.argv[sys.argv.index("--do") + 1] if "--do" in sys.argv else "public_html"
    if folder != "public_html":
        only_files = True   # wgrywanie do osobnego folderu nie rusza dzialajacej strony
    print(f"Serwer: {HOST}")
    ftp = None
    for attempt in range(3):
        user = input(f"Użytkownik FTP [{USER}]: ").strip() or USER
        pwd = getpass.getpass("Hasło FTP (nie będzie widoczne; wklejaj prawym przyciskiem myszy): ")
        print(f"  (wpisano {len(pwd)} znaków)")
        if not pwd or len(pwd) > 40 or any(ch in pwd for ch in " \t\r\n\x16"):
            print("  To nie wygląda na hasło (pewnie wkleił się inny tekst ze schowka). Nie wysyłam — spróbuj jeszcze raz.")
            continue
        if any(ch in user for ch in " \t\"'()"):
            print("  Dziwna nazwa użytkownika — nie wysyłam. Spróbuj jeszcze raz."); continue
        ftp = ReusedSessionFTP_TLS(HOST, timeout=60, context=make_ctx())
        try:
            ftp.login(user, pwd)
            break
        except (ftplib.error_perm, EOFError, OSError) as e:
            print("  Nie udało się zalogować:", e)
            try: ftp.close()
            except Exception: pass
            ftp = None
    if ftp is None:
        print("Logowanie nieudane. Sprawdź login/hasło w DirectAdmin -> Zarządzanie FTP."); return
    ftp.prot_p()
    ftp.encoding = "utf-8"
    print("Zalogowano. Katalog domowy:", ftp.pwd())

    base = DOMAIN_DIR if exists(ftp, "/" + DOMAIN_DIR) else ""
    target = posixpath.join("/", base, folder)
    if not exists(ftp, target):
        ftp.mkd(target)
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
    print("\nGotowe! Wgrano do " + target + ".")


if __name__ == "__main__":
    main()
