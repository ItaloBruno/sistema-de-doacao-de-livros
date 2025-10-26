from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from sistema_de_doacao_de_livros.api import router as router_api
from sistema_de_doacao_de_livros.web.rotas.inicio import (
    router as router_inicio,
)

app = FastAPI()

app.mount(
    '/static',
    StaticFiles(directory='sistema_de_doacao_de_livros/web/static'),
    name='static',
)

app.include_router(router_inicio)
app.include_router(router_api, prefix='/api')
