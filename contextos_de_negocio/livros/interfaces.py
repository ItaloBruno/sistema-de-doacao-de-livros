from typing import Final

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

rotas_livros: Final[APIRouter] = APIRouter(include_in_schema=False)

templates: Final[Jinja2Templates] = Jinja2Templates(
    directory="sistema_de_doacao_de_livros/pontos_de_entrada/templates"
)


@rotas_livros.get("/doador/cadastrar-livro", response_class=HTMLResponse)
async def pagina_cadastrar_livro(request: Request):
    return templates.TemplateResponse(
        "cadastrar_livro.html", {"request": request}
    )


@rotas_livros.get("/doador/editar-livro", response_class=HTMLResponse)
async def pagina_editar_livro(request: Request):
    return templates.TemplateResponse(
        "editar_livro.html", {"request": request}
    )
