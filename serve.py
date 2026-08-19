# -*- coding: utf-8 -*-
"""Lokalny serwer podglądu z endpointem POST /upload (zapis zrzutów z przeglądarki)."""
import http.server, base64, os, socketserver

ROOT = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(ROOT, "_shots")
os.makedirs(SHOTS, exist_ok=True)

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def do_POST(self):
        if self.path.startswith("/upload"):
            n = int(self.headers.get("Content-Length", 0))
            data = self.rfile.read(n).decode()
            name = self.headers.get("X-Name", "shot.jpg")
            b64 = data.split(",", 1)[1] if "," in data else data
            with open(os.path.join(SHOTS, os.path.basename(name)), "wb") as f:
                f.write(base64.b64decode(b64))
            self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
        else:
            self.send_response(404); self.end_headers()

    def log_message(self, *a): pass

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", 8777), H) as srv:
    srv.serve_forever()
