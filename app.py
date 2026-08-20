# -*- coding: utf-8 -*-
"""
Serviço Railway do Painel de OS (rota GitHub).

O painel_os.html vive no próprio repositório. O robô faz commit/push do
arquivo a cada baixa; o Railway detecta o commit, refaz o deploy e passa a
servir a versão nova.

Rotas:
  GET /        -> mostra o painel_os.html do repositório (público, sem senha)
  GET /saude   -> checagem simples de status
"""

import os
from flask import Flask, Response

app = Flask(__name__)

# painel_os.html fica na mesma pasta deste app, dentro do repositório.
ARQUIVO_PAINEL = os.path.join(os.path.dirname(__file__), "painel_os.html")

PAGINA_VAZIA = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Painel de OS</title>
<style>body{font-family:'Segoe UI',system-ui,sans-serif;background:#f4f6f9;color:#12233b;
display:flex;min-height:100vh;align-items:center;justify-content:center;text-align:center;margin:0}
.box{background:#fff;border:1px solid #dce3ec;border-radius:12px;padding:40px;max-width:420px}
h1{font-size:20px;margin:0 0 8px}p{color:#4a5a6e;font-size:14px;line-height:1.5}</style>
</head><body><div class="box"><h1>Painel de OS</h1>
<p>O <b>painel_os.html</b> ainda não está no repositório. Rode o
<b>atualizador.bat</b> na máquina do robô para publicar a primeira versão.</p>
</div></body></html>"""


@app.route("/")
def home():
    if os.path.exists(ARQUIVO_PAINEL):
        with open(ARQUIVO_PAINEL, "r", encoding="utf-8") as f:
            html = f.read()
        resp = Response(html, mimetype="text/html")
        resp.headers["Cache-Control"] = "no-store, must-revalidate"
        return resp
    return Response(PAGINA_VAZIA, mimetype="text/html")


@app.route("/saude")
def saude():
    return {"status": "ok", "painel_publicado": os.path.exists(ARQUIVO_PAINEL)}, 200


if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=porta)
