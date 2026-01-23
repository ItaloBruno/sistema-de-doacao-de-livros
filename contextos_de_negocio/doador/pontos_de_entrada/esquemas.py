from pydantic import BaseModel

from utilitarios.pydantic.tipos import Email, Nome, Senha, Telefone


class EntradaCriarDoador(BaseModel):
    nome: Nome
    email: Email
    senha: Senha
    telefone: Telefone


class RespostaCriarDoador(BaseModel):
    id: str
    nome: Nome
    email: Email
    telefone: Telefone


class RespostaBuscarDoador(BaseModel):
    id: str
    nome: Nome
    email: Email
    telefone: Telefone


class EntradaAtualizarDoador(BaseModel):
    nome: Nome
    email: Email
    telefone: Telefone
    senha_atual: Senha
    nova_senha: Senha | None = None


class RespostaAtualizarDoador(BaseModel):
    id: str
    nome: Nome
    email: Email
    telefone: Telefone


class ItemDoadorResposta(BaseModel):
    id: str
    nome: Nome
    email: Email
    telefone: Telefone


class RespostaListarDoadores(BaseModel):
    itens: list[ItemDoadorResposta]
    total: int
    pagina: int
    itens_por_pagina: int
    total_paginas: int
