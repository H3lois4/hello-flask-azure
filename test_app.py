import pytest

import app as api


@pytest.fixture
def cliente():
    return api.app.test_client()


def test_inicio_descreve_a_api(cliente):
    assert cliente.get("/").json["api"] == "Livraria"


def test_listar(cliente):
    resposta = cliente.get("/api/livros")
    assert resposta.status_code == 200 and len(resposta.json) >= 3


def test_filtrar_por_autor(cliente):
    titulos = [l["titulo"] for l in cliente.get("/api/livros?autor=clarice").json]
    assert titulos == ["A Hora da Estrela"]


def test_buscar_e_404(cliente):
    assert cliente.get("/api/livros/1").json["titulo"] == "Dom Casmurro"
    assert cliente.get("/api/livros/999").status_code == 404


def test_crud_completo(cliente):
    novo = {"titulo": "Vidas Secas", "autor": "Graciliano Ramos", "preco": 45.0, "estoque": 4}
    criado = cliente.post("/api/livros", json=novo)
    assert criado.status_code == 201
    livro_id = criado.json["id"]

    atualizado = cliente.put(f"/api/livros/{livro_id}", json={"preco": 39.9})
    assert atualizado.json["preco"] == 39.9 and atualizado.json["titulo"] == "Vidas Secas"

    assert cliente.delete(f"/api/livros/{livro_id}").status_code == 204
    assert cliente.get(f"/api/livros/{livro_id}").status_code == 404


def test_validacao(cliente):
    assert cliente.post("/api/livros", json={"titulo": "Sem autor"}).status_code == 400
    assert cliente.put("/api/livros/1", json={"preco": -5}).status_code == 400
    assert cliente.post("/api/livros", data="texto").status_code == 400
