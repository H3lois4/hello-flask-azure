from app import app


def test_hello_world():
    resposta = app.test_client().get("/")
    assert resposta.status_code == 200
    assert b"Hello World!" in resposta.data
