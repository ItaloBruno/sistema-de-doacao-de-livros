# from typing import Final

# from fastapi import APIRouter, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates

# rotas_autenticacao: Final[APIRouter] = APIRouter(include_in_schema=False)

# templates: Final[Jinja2Templates] = Jinja2Templates(
#     directory="sistema_de_doacao_de_livros/pontos_de_entrada/templates"
# )


# @rotas_autenticacao.get("/entrar", response_class=HTMLResponse)
# async def pagina_entrar(request: Request):
#     return templates.TemplateResponse("entrar.html", {"request": request})


# @rotas_autenticacao.get("/registrar", response_class=HTMLResponse)
# async def pagina_registrar(request: Request):
#     return templates.TemplateResponse("registrar.html", {"request": request})
