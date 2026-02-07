from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

rotas_doador = APIRouter(include_in_schema=False)

templates = Jinja2Templates(
    directory="sistema_de_doacao_de_livros/web/templates"
)


@rotas_doador.get("/doador", response_class=HTMLResponse)
async def pagina_doador(request: Request):
    return templates.TemplateResponse("doador.html", {"request": request})


@rotas_doador.get("/doador/cadastrar-livro", response_class=HTMLResponse)
async def pagina_cadastrar_livro(request: Request):
    return templates.TemplateResponse("cadastrar_livro.html", {"request": request})


@rotas_doador.get("/doador/editar-livro", response_class=HTMLResponse)
async def pagina_editar_livro(request: Request):
    return templates.TemplateResponse("editar_livro.html", {"request": request})


@rotas_doador.get("/doador/editar-perfil", response_class=HTMLResponse)
async def pagina_editar_perfil_doador(request: Request):
    return templates.TemplateResponse(
        "editar_perfil_doador.html", {"request": request}
    )
