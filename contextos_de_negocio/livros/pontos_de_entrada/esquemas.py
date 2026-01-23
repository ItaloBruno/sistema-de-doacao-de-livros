from pydantic import BaseModel


class RespostaCriarLivro(BaseModel):
    id: str
    titulo: str
    autores: list[str]
    subtitulo: str | None = None
    isbn: str | None = None
    observacao: str | None = None
    foto: str | None = None


class RespostaAtualizarLivro(BaseModel):
    id: str
    titulo: str
    autores: list[str]
    subtitulo: str | None = None
    isbn: str | None = None
    observacao: str | None = None
    foto: str | None = None


class ItemLivroResposta(BaseModel):
    id: str
    titulo: str
    autores: list[str]
    subtitulo: str | None = None
    isbn: str | None = None
    observacao: str | None = None
    foto: str | None = None


class RespostaBuscarLivro(BaseModel):
    id: str
    titulo: str
    autores: list[str]
    subtitulo: str | None = None
    isbn: str | None = None
    observacao: str | None = None
    foto: str | None = None


class RespostaListarLivros(BaseModel):
    itens: list[ItemLivroResposta]
    total: int
    pagina: int
    itens_por_pagina: int
    total_paginas: int
