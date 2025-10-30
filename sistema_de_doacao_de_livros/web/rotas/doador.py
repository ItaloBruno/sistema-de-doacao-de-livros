from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

rotas_doador = APIRouter()

templates = Jinja2Templates(
    directory="sistema_de_doacao_de_livros/web/templates"
)


@rotas_doador.get("/doador", response_class=HTMLResponse)
async def pagina_doador(request: Request):
    return templates.TemplateResponse("doador.html", {"request": request})
