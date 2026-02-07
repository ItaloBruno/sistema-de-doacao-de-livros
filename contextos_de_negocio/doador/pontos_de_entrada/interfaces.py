# from fastapi import APIRouter, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates

# rotas_doador = APIRouter(include_in_schema=False)

# templates = Jinja2Templates(
#     directory="sistema_de_doacao_de_livros/pontos_de_entrada/templates"
# )

# @rotas_doador.get("/doador", response_class=HTMLResponse)
# async def pagina_doador(request: Request):
#     return templates.TemplateResponse("doador.html", {"request": request})

# @rotas_doador.get("/doador/editar-perfil", response_class=HTMLResponse)
# async def pagina_editar_perfil_doador(request: Request):
#     return templates.TemplateResponse(
#         "editar_perfil_doador.html", {"request": request}
#     )
