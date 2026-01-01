from dataclasses import dataclass
from http import HTTPStatus

from utilitarios.excecoes.base import ExcecaoBase


@dataclass
class TokenNaoFornecido(ExcecaoBase):
    codigo_status: HTTPStatus = HTTPStatus.UNAUTHORIZED
    descricao: str = "É necessário fornecer um token de autenticação"
    titulo: str | None = "Token não fornecido"
    codigo_erro: str | None = "A003"


@dataclass
class FormatoTokenInvalido(ExcecaoBase):
    codigo_status: HTTPStatus = HTTPStatus.UNAUTHORIZED
    descricao: str = "O token deve estar no formato 'Bearer <token>'"
    titulo: str | None = "Formato de token inválido"
    codigo_erro: str | None = "A004"


@dataclass
class TokenInvalidoOuExpirado(ExcecaoBase):
    codigo_status: HTTPStatus = HTTPStatus.UNAUTHORIZED
    descricao: str = "O token fornecido é inválido ou expirou"
    titulo: str | None = "Token inválido ou expirado"
    codigo_erro: str | None = "A005"
