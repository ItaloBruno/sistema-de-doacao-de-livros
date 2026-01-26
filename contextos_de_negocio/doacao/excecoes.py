from dataclasses import dataclass
from http import HTTPStatus

from utilitarios.excecoes.base import ExcecaoBase


@dataclass
class DoacaoNaoEncontrada(ExcecaoBase):
    codigo_status: HTTPStatus = HTTPStatus.NOT_FOUND
    descricao: str = "Doação não encontrada"
    titulo: str | None = "Doação não encontrada"
    codigo_erro: str | None = "D001"


@dataclass
class InstituicaoNaoEncontrada(ExcecaoBase):
    codigo_status: HTTPStatus = HTTPStatus.NOT_FOUND
    descricao: str = "Instituição não encontrada"
    titulo: str | None = "Instituição não encontrada"
    codigo_erro: str | None = "D002"


@dataclass
class LivroNaoEncontrado(ExcecaoBase):
    codigo_status: HTTPStatus = HTTPStatus.NOT_FOUND
    descricao: str = "Livro não encontrado"
    titulo: str | None = "Livro não encontrado"
    codigo_erro: str | None = "D003"
