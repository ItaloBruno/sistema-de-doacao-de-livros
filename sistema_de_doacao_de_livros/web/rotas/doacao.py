from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

rotas_doacao = APIRouter()

templates = Jinja2Templates(
    directory="sistema_de_doacao_de_livros/web/templates"
)


@rotas_doacao.get(
    "/instituicoes/{id_instituicao}/doacao",
    response_class=HTMLResponse,
)
async def pagina_doacao(id_instituicao: int, request: Request):
    return templates.TemplateResponse(
        "doacao.html",
        {"request": request},
    )
