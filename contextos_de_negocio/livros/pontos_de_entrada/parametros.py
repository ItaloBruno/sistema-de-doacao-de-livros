from pydantic import BaseModel, Field


class ParametrosListagemLivros(BaseModel):
    pagina: int = Field(1, ge=1, description="Número da página")
    itens_por_pagina: int = Field(
        10, ge=1, le=100, description="Quantidade de itens por página"
    )
    ordem: str | None = Field(
        None,
        description=(
            "Ordenação: campo.direcao (ex: titulo.asc, isbn.desc). "
            "Múltiplos separados por vírgula: titulo.asc,isbn.desc"
        ),
        examples=["titulo.asc", "isbn.desc", "titulo.asc,isbn.desc"],
    )
    campos: str | None = Field(
        None,
        description="Projeção de campos separados por vírgula",
        examples=["id,titulo,autores", "id,titulo"],
    )
    titulo: str | None = Field(
        None,
        description=(
            "Filtro de título. Operadores: igual, diferente, contem, "
            "comeca-com, termina-com"
        ),
        examples=["contem.Python", "igual.Clean Code"],
    )
    autores: str | None = Field(
        None,
        description=(
            "Filtro de autores. Operadores: igual, diferente, contem, "
            "comeca-com, termina-com"
        ),
        examples=["contem.Martin", "comeca-com.Robert"],
    )
    subtitulo: str | None = Field(
        None,
        description=(
            "Filtro de subtítulo. Operadores: igual, diferente, contem, "
            "comeca-com, termina-com, e-nulo, nao-e-nulo"
        ),
        examples=["contem.Guide", "e-nulo."],
    )
    isbn: str | None = Field(
        None,
        description=(
            "Filtro de ISBN. Operadores: igual, diferente, contem, "
            "comeca-com, termina-com, e-nulo, nao-e-nulo"
        ),
        examples=["igual.978-0132350884", "nao-e-nulo."],
    )
    observacao: str | None = Field(
        None,
        description=(
            "Filtro de observação. Operadores: igual, diferente, contem, "
            "comeca-com, termina-com, e-nulo, nao-e-nulo"
        ),
        examples=["contem.usado", "e-nulo."],
    )

    def obter_filtros_dict(self) -> dict:
        filtros = {}
        if self.titulo:
            filtros["titulo"] = self.titulo
        if self.autores:
            filtros["autores"] = self.autores
        if self.subtitulo:
            filtros["subtitulo"] = self.subtitulo
        if self.isbn:
            filtros["isbn"] = self.isbn
        if self.observacao:
            filtros["observacao"] = self.observacao
        return filtros
