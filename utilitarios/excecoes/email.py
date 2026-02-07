from dataclasses import dataclass
from http import HTTPStatus

from utilitarios.excecoes.base import ExcecaoBase


@dataclass
class ExcecaoEmail(ExcecaoBase):
    pass


@dataclass
class ExcecaoEmailVazio(ExcecaoEmail):
    codigo_status: HTTPStatus = HTTPStatus.BAD_REQUEST
    descricao: str = "Email não pode ser vazio"
    titulo: str | None = "Email inválido"
    codigo_erro: str | None = "EMAIL_VAZIO"


@dataclass
class ExcecaoEmailInvalido(ExcecaoEmail):
    codigo_status: HTTPStatus = HTTPStatus.BAD_REQUEST
    descricao: str = "Email inválido"
    titulo: str | None = "Email inválido"
    codigo_erro: str | None = "EMAIL_INVALIDO"
