from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

rotas_inicio = APIRouter()

templates = Jinja2Templates(
    directory="sistema_de_doacao_de_livros/web/templates"
)


@rotas_inicio.get("/", response_class=HTMLResponse)
async def pagina_inicial(request: Request):
    return templates.TemplateResponse("inicio.html", {"request": request})
