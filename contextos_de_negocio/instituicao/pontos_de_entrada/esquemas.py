from pydantic import BaseModel

from utilitarios.pydantic.tipos import (
    DataFundacao,
    Descricao,
    Email,
    Endereco,
    Foto,
    Id,
    Nome,
    Senha,
    Site,
    Telefone,
)


class EntradaCriarInstituicao(BaseModel):
    nome: Nome
    email: Email
    senha: Senha
    telefone: Telefone
    descricao: Descricao
    data_fundacao: DataFundacao
    endereco: Endereco
    site: Site | None = None


class RespostaCriarInstituicao(BaseModel):
    id: Id
    nome: Nome
    email: Email
    telefone: Telefone
    descricao: Descricao
    data_fundacao: DataFundacao
    endereco: Endereco
    site: Site | None
    foto: Foto | None


class RespostaBuscarInstituicao(BaseModel):
    id: Id
    nome: Nome
    email: Email
    telefone: Telefone
    descricao: Descricao
    data_fundacao: DataFundacao
    endereco: Endereco
    site: Site | None
    foto: Foto | None


class EntradaAtualizarInstituicao(BaseModel):
    nome: Nome
    email: Email
    telefone: Telefone
    senha_atual: Senha
    descricao: Descricao
    data_fundacao: DataFundacao
    endereco: Endereco
    site: Site | None = None
    nova_senha: Senha | None = None


class RespostaAtualizarInstituicao(BaseModel):
    id: Id
    nome: Nome
    email: Email
    telefone: Telefone
    descricao: Descricao
    data_fundacao: DataFundacao
    endereco: Endereco
    site: Site | None
    foto: Foto | None
