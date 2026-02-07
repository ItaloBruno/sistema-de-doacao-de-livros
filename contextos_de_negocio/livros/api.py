# import json
# import uuid
# from http import HTTPStatus
# from pathlib import Path

# from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile

# from sistema_de_doacao_de_livros import banco_de_dados
# from sistema_de_doacao_de_livros.pontos_de_entrada.esquemas.api import (
#     livros as esquemas,
# )
# from sistema_de_doacao_de_livros.schemas import LivroDB

# rotas_api_livros = APIRouter(tags=["Livros"])


# @rotas_api_livros.post(
#     "/livros",
#     status_code=HTTPStatus.CREATED,
#     response_model=esquemas.RespostaCriarLivro,
# )
# async def criar_livro(
#     titulo: str = Form(...),
#     autores: str = Form(...),
#     subtitulo: str = Form(None),
#     isbn: str = Form(None),
#     observacao: str = Form(None),
#     foto: UploadFile = File(None),
# ):
#     try:
#         autores_list = json.loads(autores)
#     except json.JSONDecodeError:
#         raise HTTPException(
#             status_code=HTTPStatus.BAD_REQUEST,
#             detail="Formato de autores inválido",
#         )

#     foto_url = None
#     if foto and foto.filename:
#         fotos_dir = Path("/tmp/sistema-de-doacao-de-livros/fotos_livros")
#         fotos_dir.mkdir(parents=True, exist_ok=True)

#         extensao = Path(foto.filename).suffix
#         nome_arquivo = f"{uuid.uuid4()}{extensao}"
#         caminho_arquivo = fotos_dir / nome_arquivo

#         conteudo = await foto.read()
#         with open(caminho_arquivo, "wb") as f:
#             f.write(conteudo)

#         foto_url = (
#             f"/tmp/sistema-de-doacao-de-livros/fotos_livros/{nome_arquivo}"
#         )

#     livro_db = LivroDB(
#         id=len(banco_de_dados.livros) + 1,
#         titulo=titulo,
#         subtitulo=subtitulo if subtitulo else None,
#         autores=autores_list,
#         isbn=isbn if isbn else None,
#         foto_url=foto_url,
#         observacao=observacao if observacao else None,
#     )

#     banco_de_dados.livros.append(livro_db)

#     return esquemas.RespostaCriarLivro(
#         id=livro_db.id,
#         titulo=livro_db.titulo,
#         subtitulo=livro_db.subtitulo,
#         autores=livro_db.autores,
#         isbn=livro_db.isbn,
#         foto_url=livro_db.foto_url,
#         observacao=livro_db.observacao,
#     )


# @rotas_api_livros.get(
#     "/livros", response_model=list[esquemas.RespostaListarLivros]
# )
# def listar_livros():
#     return [
#         esquemas.RespostaListarLivros(
#             id=livro.id,
#             titulo=livro.titulo,
#             subtitulo=livro.subtitulo,
#             autores=livro.autores,
#             isbn=livro.isbn,
#             foto_url=livro.foto_url,
#             observacao=livro.observacao,
#             em_doacao_pendente=banco_de_dados.livro_esta_em_doacao_pendente(
#                 livro.id
#             ),
#         )
#         for livro in banco_de_dados.livros
#     ]


# @rotas_api_livros.get(
#     "/livros/buscar",
#     response_model=list[esquemas.RespostaBuscarLivrosPorTitulo],
# )
# def buscar_livros(titulo: str = Query(..., min_length=1)):
#     livros_encontrados = banco_de_dados.buscar_livros_por_titulo(titulo)

#     return [
#         esquemas.RespostaBuscarLivrosPorTitulo(
#             id=livro.id,
#             titulo=livro.titulo,
#             subtitulo=livro.subtitulo,
#             autores=livro.autores,
#             isbn=livro.isbn,
#             foto_url=livro.foto_url,
#             observacao=livro.observacao,
#         )
#         for livro in livros_encontrados
#     ]


# @rotas_api_livros.get(
#     "/livros/{livro_id}", response_model=esquemas.RespostaBuscarLivro
# )
# def buscar_livro(livro_id: int):
#     livro = banco_de_dados.buscar_livro_por_id(livro_id)
#     if not livro:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND,
#             detail="Livro não encontrado",
#         )

#     return esquemas.RespostaBuscarLivro(
#         id=livro.id,
#         titulo=livro.titulo,
#         subtitulo=livro.subtitulo,
#         autores=livro.autores,
#         isbn=livro.isbn,
#         foto_url=livro.foto_url,
#         observacao=livro.observacao,
#     )


# @rotas_api_livros.put(
#     "/livros/{livro_id}", response_model=esquemas.RespostaAtualizarLivro
# )
# async def atualizar_livro(
#     livro_id: int,
#     titulo: str = Form(...),
#     autores: str = Form(...),
#     subtitulo: str = Form(None),
#     isbn: str = Form(None),
#     observacao: str = Form(None),
#     foto: UploadFile = File(None),
# ):
#     livro = banco_de_dados.buscar_livro_por_id(livro_id)
#     if not livro:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND,
#             detail="Livro não encontrado",
#         )

#     if banco_de_dados.livro_esta_em_doacao_pendente(livro_id):
#         raise HTTPException(
#             status_code=HTTPStatus.BAD_REQUEST,
#             detail=(
#                 "Não é possível editar este livro pois ele está "
#                 "em uma doação pendente"
#             ),
#         )

#     try:
#         autores_list = json.loads(autores)
#     except json.JSONDecodeError:
#         raise HTTPException(
#             status_code=HTTPStatus.BAD_REQUEST,
#             detail="Formato de autores inválido",
#         )

#     foto_url = livro.foto_url
#     if foto and foto.filename:
#         fotos_dir = Path("/tmp/sistema-de-doacao-de-livros/fotos_livros")
#         fotos_dir.mkdir(parents=True, exist_ok=True)

#         extensao = Path(foto.filename).suffix
#         nome_arquivo = f"{uuid.uuid4()}{extensao}"
#         caminho_arquivo = fotos_dir / nome_arquivo

#         conteudo = await foto.read()
#         with open(caminho_arquivo, "wb") as f:
#             f.write(conteudo)

#         foto_url = (
#             f"/tmp/sistema-de-doacao-de-livros/fotos_livros/{nome_arquivo}"
#         )

#     livro.titulo = titulo
#     livro.subtitulo = subtitulo if subtitulo else None
#     livro.autores = autores_list
#     livro.isbn = isbn if isbn else None
#     livro.foto_url = foto_url
#     livro.observacao = observacao if observacao else None

#     return esquemas.RespostaAtualizarLivro(
#         id=livro.id,
#         titulo=livro.titulo,
#         subtitulo=livro.subtitulo,
#         autores=livro.autores,
#         isbn=livro.isbn,
#         foto_url=livro.foto_url,
#         observacao=livro.observacao,
#     )


# @rotas_api_livros.delete(
#     "/livros/{livro_id}", status_code=HTTPStatus.NO_CONTENT
# )
# def excluir_livro(livro_id: int):
#     livro = banco_de_dados.buscar_livro_por_id(livro_id)
#     if not livro:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND,
#             detail="Livro não encontrado",
#         )

#     if banco_de_dados.livro_esta_em_doacao_pendente(livro_id):
#         raise HTTPException(
#             status_code=HTTPStatus.BAD_REQUEST,
#             detail=(
#                 "Não é possível excluir este livro pois ele está "
#                 "em uma doação pendente"
#             ),
#         )

#     banco_de_dados.livros.remove(livro)

# from pydantic import BaseModel


# class RespostaCriarLivro(BaseModel):
#     id: int
#     titulo: str
#     subtitulo: str | None = None
#     autores: list[str]
#     isbn: str | None = None
#     foto_url: str | None = None
#     observacao: str | None = None


# class RespostaBuscarLivro(BaseModel):
#     id: int
#     titulo: str
#     subtitulo: str | None = None
#     autores: list[str]
#     isbn: str | None = None
#     foto_url: str | None = None
#     observacao: str | None = None


# class RespostaListarLivros(BaseModel):
#     id: int
#     titulo: str
#     subtitulo: str | None = None
#     autores: list[str]
#     isbn: str | None = None
#     foto_url: str | None = None
#     observacao: str | None = None
#     em_doacao_pendente: bool = False


# class RespostaBuscarLivrosPorTitulo(BaseModel):
#     id: int
#     titulo: str
#     subtitulo: str | None = None
#     autores: list[str]
#     isbn: str | None = None
#     foto_url: str | None = None
#     observacao: str | None = None


# class RespostaAtualizarLivro(BaseModel):
#     id: int
#     titulo: str
#     subtitulo: str | None = None
#     autores: list[str]
#     isbn: str | None = None
#     foto_url: str | None = None
#     observacao: str | None = None
