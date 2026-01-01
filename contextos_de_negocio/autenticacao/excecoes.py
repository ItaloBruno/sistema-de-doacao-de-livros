from dataclasses import dataclass
from http import HTTPStatus

from utilitarios.excecoes.base import ExcecaoBase


@dataclass
class CredenciaisInvalidas(ExcecaoBase):
    codigo_status: HTTPStatus = HTTPStatus.UNAUTHORIZED
    descricao: str = "Email ou senha incorretos"
    titulo: str | None = "Credenciais inválidas"
    codigo_erro: str | None = "A001"


@dataclass
class TokenInvalido(ExcecaoBase):
    codigo_status: HTTPStatus = HTTPStatus.UNAUTHORIZED
    descricao: str = "Token de renovação inválido ou expirado"
    titulo: str | None = "Token inválido"
    codigo_erro: str | None = "A002"
