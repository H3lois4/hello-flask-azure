"""API RESTful da Livraria em Flask.

Recurso: /api/livros
  GET    /api/livros          lista os livros (filtro opcional: ?autor=machado)
  GET    /api/livros/<id>     busca um livro
  POST   /api/livros          cria um livro
  PUT    /api/livros/<id>     atualiza um livro
  DELETE /api/livros/<id>     remove um livro
"""
from flask import Flask, jsonify, request

app = Flask(__name__)
app.json.ensure_ascii = False

CAMPOS = {"titulo": str, "autor": str, "preco": (int, float), "estoque": int}

livros = {
    1: {"id": 1, "titulo": "Dom Casmurro", "autor": "Machado de Assis", "preco": 29.90, "estoque": 3},
    2: {"id": 2, "titulo": "A Hora da Estrela", "autor": "Clarice Lispector", "preco": 39.90, "estoque": 5},
    3: {"id": 3, "titulo": "Grande Sertão: Veredas", "autor": "João Guimarães Rosa", "preco": 89.00, "estoque": 2},
}
proximo_id = 4


def erro(mensagem, status):
    return jsonify({"erro": mensagem}), status


def validar(dados, parcial=False):
    """Confere os campos do corpo JSON. Retorna uma mensagem de erro ou None."""
    if not isinstance(dados, dict):
        return "Envie um corpo JSON"
    if not parcial:
        faltando = [c for c in CAMPOS if c not in dados]
        if faltando:
            return f"Campos obrigatórios: {', '.join(faltando)}"
    for campo, valor in dados.items():
        if campo not in CAMPOS:
            return f"Campo desconhecido: {campo}"
        if isinstance(valor, bool) or not isinstance(valor, CAMPOS[campo]):
            return f"Valor inválido para {campo}"
        if campo in ("preco", "estoque") and valor < 0:
            return f"{campo} não pode ser negativo"
        if campo in ("titulo", "autor") and not valor.strip():
            return f"{campo} não pode ser vazio"
    return None


@app.get("/")
def inicio():
    return jsonify({
        "api": "Livraria",
        "rotas": {
            "GET /api/livros": "lista os livros (filtro opcional ?autor=)",
            "GET /api/livros/<id>": "busca um livro",
            "POST /api/livros": "cria um livro",
            "PUT /api/livros/<id>": "atualiza um livro",
            "DELETE /api/livros/<id>": "remove um livro",
        },
    })


@app.get("/api/livros")
def listar():
    autor = request.args.get("autor", "").lower()
    resultado = [l for l in livros.values() if autor in l["autor"].lower()]
    return jsonify(resultado)


@app.get("/api/livros/<int:livro_id>")
def buscar(livro_id):
    livro = livros.get(livro_id)
    if livro is None:
        return erro("Livro não encontrado", 404)
    return jsonify(livro)


@app.post("/api/livros")
def criar():
    global proximo_id
    dados = request.get_json(silent=True)
    mensagem = validar(dados)
    if mensagem:
        return erro(mensagem, 400)
    livro = {"id": proximo_id, **{c: dados[c] for c in CAMPOS}}
    livros[proximo_id] = livro
    proximo_id += 1
    return jsonify(livro), 201, {"Location": f"/api/livros/{livro['id']}"}


@app.put("/api/livros/<int:livro_id>")
def atualizar(livro_id):
    livro = livros.get(livro_id)
    if livro is None:
        return erro("Livro não encontrado", 404)
    dados = request.get_json(silent=True)
    mensagem = validar(dados, parcial=True)
    if mensagem:
        return erro(mensagem, 400)
    livro.update(dados)
    return jsonify(livro)


@app.delete("/api/livros/<int:livro_id>")
def remover(livro_id):
    if livros.pop(livro_id, None) is None:
        return erro("Livro não encontrado", 404)
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
