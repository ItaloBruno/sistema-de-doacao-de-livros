from dataclasses import dataclass
from http import HTTPStatus

from utilitarios.excecoes.base import ExcecaoBase


@dataclass
class LivroNaoEncontrado(ExcecaoBase):
    codigo_status: HTTPStatus = HTTPStatus.NOT_FOUND
    descricao: str = "Livro não encontrado"
    titulo: str | None = "Livro não encontrado"
    codigo_erro: str | None = "L001"
