from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

rotas_autenticacao = APIRouter()

templates = Jinja2Templates(
    directory="sistema_de_doacao_de_livros/web/templates"
)


@rotas_autenticacao.get("/entrar", response_class=HTMLResponse)
async def pagina_entrar(request: Request):
    return templates.TemplateResponse("entrar.html", {"request": request})


@rotas_autenticacao.get("/registrar", response_class=HTMLResponse)
async def pagina_registrar(request: Request):
    return templates.TemplateResponse("registrar.html", {"request": request})
