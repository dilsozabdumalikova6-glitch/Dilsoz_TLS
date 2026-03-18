from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from argon2 import PasswordHasher
import ssl

ph = PasswordHasher()

accounts = {
    "admin": {
        "password_hash": ph.hash("1234"),
        "role": "admin"
    },
    "user": {
        "password_hash": ph.hash("1234"),
        "role": "user"
    }
}


class SecureLoginHandler(BaseHTTPRequestHandler):

    def send_html(self, html, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def load_login_page(self):
        with open("login.html", "r", encoding="utf-8") as f:
            return f.read()

    def do_GET(self):
        if self.path == "/":
            self.send_html(self.load_login_page())

        elif self.path == "/admin":
            self.send_html("""
                <h1>Admin panel</h1>
                <p>Bu sahifa administrator uchun mo‘ljallangan.</p>
            """)

        elif self.path == "/user":
            self.send_html("""
                <h1>User panel</h1>
                <p>Bu sahifa oddiy foydalanuvchi uchun mo‘ljallangan.</p>
            """)

        else:
            self.send_html("<h1>404</h1><p>Sahifa topilmadi</p>", 404)

    def do_POST(self):
        if self.path != "/login":
            self.send_html("<h1>400</h1><p>Noto‘g‘ri so‘rov</p>", 400)
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        form_data = parse_qs(body)

        username = form_data.get("username", [""])[0].strip()
        password = form_data.get("password", [""])[0]

        if username not in accounts:
            self.send_html("<h1>Login failed</h1><p>Foydalanuvchi topilmadi</p>", 401)
            return

        try:
            ph.verify(accounts[username]["password_hash"], password)
            role = accounts[username]["role"]

            if role == "admin":
                self.send_html("""
                    <h1>Welcome Admin</h1>
                    <p>Siz administrator sifatida tizimga muvaffaqiyatli kirdingiz.</p>
                """)
            else:
                self.send_html("""
                    <h1>Welcome User</h1>
                    <p>Siz oddiy foydalanuvchi sifatida tizimga muvaffaqiyatli kirdingiz.</p>
                """)

        except Exception:
            self.send_html("<h1>Login failed</h1><p>Parol noto‘g‘ri</p>", 401)


HOST = "0.0.0.0"
PORT = 4443

server = ThreadingHTTPServer((HOST, PORT), SecureLoginHandler)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(
    certfile="C:/Users/admin/TLS_project_Dilsuz/server.crt",
    keyfile="C:/Users/admin/TLS_project_Dilsuz/server.key"
)

server.socket = ssl_context.wrap_socket(server.socket, server_side=True)

print(f"Dilsoz server ishga tushdi: https://localhost:{PORT}")

server.serve_forever()