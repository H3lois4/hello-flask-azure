from flask import Flask

app = Flask(__name__)


@app.get("/")
def hello():
    return "<h1>Hello World!</h1><p>Aplicação Flask publicada no Azure App Service com CI/CD.</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
