from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Query

from sistema_de_doacao_de_livros import banco_de_dados
from sistema_de_doacao_de_livros.schemas import (
    CriacaoDeLivro,
    Livro,
    LivroDB,
)

rotas_api_livros = APIRouter()


@rotas_api_livros.post(
    "/livros", status_code=HTTPStatus.CREATED, response_model=Livro
)
def criar_livro(dados: CriacaoDeLivro):
    livro_db = LivroDB(
        **dados.model_dump(),
        id=len(banco_de_dados.livros) + 1,
    )

    banco_de_dados.livros.append(livro_db)

    return Livro(
        id=livro_db.id,
        titulo=livro_db.titulo,
        subtitulo=livro_db.subtitulo,
        autores=livro_db.autores,
        isbn=livro_db.isbn,
    )


@rotas_api_livros.get("/livros/buscar", response_model=list[Livro])
def buscar_livros(titulo: str = Query(..., min_length=1)):
    livros_encontrados = banco_de_dados.buscar_livros_por_titulo(titulo)

    return [
        Livro(
            id=livro.id,
            titulo=livro.titulo,
            subtitulo=livro.subtitulo,
            autores=livro.autores,
            isbn=livro.isbn,
        )
        for livro in livros_encontrados
    ]


@rotas_api_livros.get("/livros/{livro_id}", response_model=Livro)
def buscar_livro(livro_id: int):
    livro = banco_de_dados.buscar_livro_por_id(livro_id)
    if not livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Livro não encontrado",
        )

    return Livro(
        id=livro.id,
        titulo=livro.titulo,
        subtitulo=livro.subtitulo,
        autores=livro.autores,
        isbn=livro.isbn,
    )
