from typing import Final

from fastapi import FastAPI
from fastapi.security import HTTPBearer

from contextos_de_negocio.autenticacao.pontos_de_entrada.rotas import (
    api_autenticacao,
)
from contextos_de_negocio.doacao.pontos_de_entrada.rotas import api_doacao
from contextos_de_negocio.doador.pontos_de_entrada.rotas import api_doador
from contextos_de_negocio.instituicao.pontos_de_entrada.rotas import (
    api_instituicao,
)
from contextos_de_negocio.livros.pontos_de_entrada.rotas import api_livros
from utilitarios.excecoes.base import ExcecaoBase
from utilitarios.fastapi.manipuladores_excecao import (
    manipulador_excecao_base,
    manipulador_excecao_generica,
)

app: Final[FastAPI] = FastAPI(
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
    },
)

security = HTTPBearer()

app.add_exception_handler(ExcecaoBase, manipulador_excecao_base)
app.add_exception_handler(Exception, manipulador_excecao_generica)


# app.mount(
#     "/static",
#     StaticFiles(
#         directory=(
#             "src/contextos_de_negocio/doacao/pontos_de_entrada/estatico"
#         )
#     ),
#     name="static",
# )

# fotos_livros_dir = "/tmp/sistema-de-doacao-de-livros/fotos_livros"
# os.makedirs(fotos_livros_dir, exist_ok=True)
# app.mount(
#     "/tmp/sistema-de-doacao-de-livros/fotos_livros",
#     StaticFiles(directory=fotos_livros_dir),
#     name="fotos_livros",
# )

# fotos_instituicoes_dir = (
#     "/tmp/sistema-de-doacao-de-livros/fotos_instituicoes"
# )
# os.makedirs(fotos_instituicoes_dir, exist_ok=True)
# app.mount(
#     "/tmp/sistema-de-doacao-de-livros/fotos_instituicoes",
#     StaticFiles(directory=fotos_instituicoes_dir),
#     name="fotos_instituicoes",
# )

# app.include_router(paginas.inicio.rotas_inicio)
# app.include_router(paginas.instituicoes.rotas_instituicoes)
# app.include_router(paginas.autenticacao.rotas_autenticacao)
# app.include_router(paginas.doacao.rotas_doacao)
# app.include_router(paginas.doador.rotas_doador)
# app.include_router(paginas.avaliacao.rotas_solicitacoes)

app.include_router(api_autenticacao, prefix="/api")
app.include_router(api_doador, prefix="/api")
app.include_router(api_instituicao, prefix="/api")
app.include_router(api_livros, prefix="/api")
app.include_router(api_doacao, prefix="/api")
