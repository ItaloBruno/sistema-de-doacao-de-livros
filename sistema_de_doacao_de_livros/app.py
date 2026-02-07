from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from sistema_de_doacao_de_livros.api.inicio import rotas_api_inicio
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

app.mount(
    "/static",
    StaticFiles(directory="sistema_de_doacao_de_livros/web/static"),
    name="static",
)

app.include_router(rotas_inicio)
app.include_router(rotas_instituicoes)
app.include_router(rotas_autenticacao)
app.include_router(rotas_doacao)
app.include_router(rotas_doador)
app.include_router(rotas_solicitacoes)
app.include_router(rotas_api_inicio, prefix="/api")
app.include_router(rotas_api_usuarios, prefix="/api")
