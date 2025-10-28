from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

rotas_instituicoes = APIRouter()

templates = Jinja2Templates(
    directory="sistema_de_doacao_de_livros/web/templates"
)


@rotas_instituicoes.get("/instituicoes", response_class=HTMLResponse)
async def pagina_instituicoes(request: Request):
    return templates.TemplateResponse(
        "instituicoes.html", {"request": request}
    )
