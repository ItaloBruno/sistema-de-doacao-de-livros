from dataclasses import dataclass
from http import HTTPStatus

from utilitarios.excecoes.base import ExcecaoBase


@dataclass
class ExcecaoTelefone(ExcecaoBase):
    pass


@dataclass
class ExcecaoTelefoneVazio(ExcecaoTelefone):
    codigo_status: HTTPStatus = HTTPStatus.BAD_REQUEST
    descricao: str = "Telefone não pode ser vazio"
    titulo: str | None = "Telefone inválido"
    codigo_erro: str | None = "TELEFONE_VAZIO"


@dataclass
class ExcecaoTelefoneInvalido(ExcecaoTelefone):
    codigo_status: HTTPStatus = HTTPStatus.BAD_REQUEST
    descricao: str = "Telefone deve ter 10 ou 11 dígitos"
    titulo: str | None = "Telefone inválido"
    codigo_erro: str | None = "TELEFONE_INVALIDO"
