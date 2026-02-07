from pydantic import BaseModel

from utilitarios.pydantic.tipos import Email, Nome, Senha, Telefone, Token


class EntradaLogin(BaseModel):
    email: Email
    senha: Senha


class RespostaLogin(BaseModel):
    id: str
    nome: Nome
    email: Email
    telefone: Telefone
    token_de_acesso: Token
    token_de_renovacao: Token


class EntradaRenovarToken(BaseModel):
    token_de_renovacao: Token


class RespostaRenovarToken(BaseModel):
    token_de_acesso: Token
