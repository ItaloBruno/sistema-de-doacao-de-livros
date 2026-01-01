from typing import Final

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

rotas_inicio: Final[APIRouter] = APIRouter(include_in_schema=False)

templates: Final[Jinja2Templates] = Jinja2Templates(
    directory="sistema_de_doacao_de_livros/pontos_de_entrada/templates"
)


@rotas_inicio.get("/", response_class=HTMLResponse)
async def pagina_inicial(request: Request):
    return templates.TemplateResponse("inicio.html", {"request": request})
