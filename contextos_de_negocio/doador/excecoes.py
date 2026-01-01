from dataclasses import dataclass
from http import HTTPStatus

from utilitarios.excecoes.base import ExcecaoBase


@dataclass
class DoadorNaoEncontrado(ExcecaoBase):
    codigo_status: HTTPStatus = HTTPStatus.NOT_FOUND
    descricao: str = "Doador não encontrado"
    titulo: str | None = "Doador não encontrado"
    codigo_erro: str | None = "D001"


@dataclass
class EmailJaCadastrado(ExcecaoBase):
    codigo_status: HTTPStatus = HTTPStatus.BAD_REQUEST
    descricao: str = "Email já está cadastrado"
    titulo: str | None = "Email já cadastrado"
    codigo_erro: str | None = "D002"


@dataclass
class SenhaIncorreta(ExcecaoBase):
    codigo_status: HTTPStatus = HTTPStatus.UNAUTHORIZED
    descricao: str = "Senha atual incorreta"
    titulo: str | None = "Senha incorreta"
    codigo_erro: str | None = "D003"
