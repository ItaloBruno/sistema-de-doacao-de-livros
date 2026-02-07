import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from sistema_de_doacao_de_livros import banco_de_dados
from sistema_de_doacao_de_livros.api.autenticacao import rotas_api_autenticacao
from sistema_de_doacao_de_livros.api.doacoes import rotas_api_doacoes
from sistema_de_doacao_de_livros.api.doadores import rotas_api_doadores
from sistema_de_doacao_de_livros.api.instituicoes import rotas_api_instituicoes
from sistema_de_doacao_de_livros.api.livros import rotas_api_livros
from sistema_de_doacao_de_livros.api.usuarios import rotas_api_usuarios
from sistema_de_doacao_de_livros.web.rotas.autenticacao import (
    rotas_autenticacao,
)
from sistema_de_doacao_de_livros.web.rotas.avaliacao import rotas_solicitacoes
from sistema_de_doacao_de_livros.web.rotas.doacao import rotas_doacao
from sistema_de_doacao_de_livros.web.rotas.doador import rotas_doador
from sistema_de_doacao_de_livros.web.rotas.inicio import rotas_inicio
from sistema_de_doacao_de_livros.web.rotas.instituicoes import (
    rotas_instituicoes,
)

app = FastAPI()

banco_de_dados.inicializar_dados_teste()

app.mount(
    "/static",
    StaticFiles(directory="sistema_de_doacao_de_livros/web/static"),
    name="static",
)

uploads_dir = "sistema_de_doacao_de_livros/web/static/uploads"
os.makedirs(uploads_dir, exist_ok=True)

fotos_livros_dir = "/tmp/sistema-de-doacao-de-livros/fotos_livros"
os.makedirs(fotos_livros_dir, exist_ok=True)
app.mount(
    "/tmp/sistema-de-doacao-de-livros/fotos_livros",
    StaticFiles(directory=fotos_livros_dir),
    name="fotos_livros",
)

fotos_instituicoes_dir = "/tmp/sistema-de-doacao-de-livros/fotos_instituicoes"
os.makedirs(fotos_instituicoes_dir, exist_ok=True)
app.mount(
    "/tmp/sistema-de-doacao-de-livros/fotos_instituicoes",
    StaticFiles(directory=fotos_instituicoes_dir),
    name="fotos_instituicoes",
)

app.include_router(rotas_inicio)
app.include_router(rotas_instituicoes)
app.include_router(rotas_autenticacao)
app.include_router(rotas_doacao)
app.include_router(rotas_doador)
app.include_router(rotas_solicitacoes)

app.include_router(rotas_api_usuarios, prefix="/api")
app.include_router(rotas_api_autenticacao, prefix="/api")
app.include_router(rotas_api_doadores, prefix="/api")
app.include_router(rotas_api_instituicoes, prefix="/api")
app.include_router(rotas_api_livros, prefix="/api")
app.include_router(rotas_api_doacoes, prefix="/api")
