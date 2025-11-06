from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

rotas_solicitacoes = APIRouter(include_in_schema=False)

templates = Jinja2Templates(
    directory="sistema_de_doacao_de_livros/web/templates"
)


@rotas_solicitacoes.get("/solicitacoes", response_class=HTMLResponse)
async def pagina_solicitacoes(request: Request):
    return templates.TemplateResponse(
        "solicitacoes.html",
        {"request": request},
    )
