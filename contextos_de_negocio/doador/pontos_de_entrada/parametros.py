from pydantic import BaseModel, Field


class ParametrosListagemDoadores(BaseModel):
    pagina: int = Field(1, ge=1, description="Número da página")
    itens_por_pagina: int = Field(
        10, ge=1, le=100, description="Quantidade de itens por página"
    )
    ordem: str | None = Field(
        None,
        description=(
            "Ordenação: campo.direcao (ex: nome.asc, email.desc). "
            "Múltiplos separados por vírgula: nome.asc,email.desc"
        ),
        examples=["nome.asc", "email.desc", "nome.asc,email.desc"],
    )
    campos: str | None = Field(
        None,
        description="Projeção de campos separados por vírgula",
        examples=["id,nome,email", "id,nome"],
    )
    nome: str | None = Field(
        None,
        description=(
            "Filtro de nome. Operadores: igual, diferente, contem, "
            "comeca-com, termina-com"
        ),
        examples=["contem.Silva", "igual.João da Silva"],
    )
    email: str | None = Field(
        None,
        description=(
            "Filtro de email. Operadores: igual, diferente, contem, "
            "comeca-com, termina-com"
        ),
        examples=["contem.@gmail.com", "comeca-com.joao"],
    )
    telefone: str | None = Field(
        None,
        description=(
            "Filtro de telefone. Operadores: igual, diferente, contem, "
            "comeca-com, termina-com"
        ),
        examples=["contem.11", "comeca-com.119"],
    )

    def obter_filtros_dict(self) -> dict:
        filtros = {}
        if self.nome:
            filtros["nome"] = self.nome
        if self.email:
            filtros["email"] = self.email
        if self.telefone:
            filtros["telefone"] = self.telefone
        return filtros
