# from fastapi import APIRouter, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates

# rotas_doacao = APIRouter(include_in_schema=False)

# templates = Jinja2Templates(
#     directory="sistema_de_doacao_de_livros/pontos_de_entrada/templates"
# )


# @rotas_doacao.get(
#     "/instituicoes/{id_instituicao}/doacao",
#     response_class=HTMLResponse,
# )
# async def pagina_doacao(id_instituicao: int, request: Request):
#     return templates.TemplateResponse(
#         "doacao_completa.html",
#         {"request": request},
#     )

# @rotas_solicitacoes.get("/solicitacoes", response_class=HTMLResponse)
# async def pagina_solicitacoes(request: Request):
#     return templates.TemplateResponse(
#         "solicitacoes.html",
#         {"request": request},
#     )
