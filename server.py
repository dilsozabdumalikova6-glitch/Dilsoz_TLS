from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Salom, HTTPS ishlayapti!"

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=4443,
        ssl_context=(
            "C:\\tls_project\\rootCA\\server.crt",
            "C:\\tls_project\\rootCA\\server.key"
        )
    )