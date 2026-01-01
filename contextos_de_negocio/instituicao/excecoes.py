from dataclasses import dataclass
from http import HTTPStatus

from utilitarios.excecoes.base import ExcecaoBase


@dataclass
class InstituicaoNaoEncontrada(ExcecaoBase):
    codigo_status: HTTPStatus = HTTPStatus.NOT_FOUND
    descricao: str = "Instituição não encontrada"
    titulo: str | None = "Instituição não encontrada"
    codigo_erro: str | None = "I001"


@dataclass
class EmailJaCadastrado(ExcecaoBase):
    codigo_status: HTTPStatus = HTTPStatus.BAD_REQUEST
    descricao: str = "Email já está cadastrado"
    titulo: str | None = "Email já cadastrado"
    codigo_erro: str | None = "I002"


@dataclass
class SenhaIncorreta(ExcecaoBase):
    codigo_status: HTTPStatus = HTTPStatus.UNAUTHORIZED
    descricao: str = "Senha atual incorreta"
    titulo: str | None = "Senha incorreta"
    codigo_erro: str | None = "I003"
