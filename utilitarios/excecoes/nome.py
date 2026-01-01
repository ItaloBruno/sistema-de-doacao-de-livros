from dataclasses import dataclass
from http import HTTPStatus

from utilitarios.excecoes.base import ExcecaoBase


@dataclass
class ExcecaoNome(ExcecaoBase):
    pass


@dataclass
class ExcecaoNomeVazio(ExcecaoNome):
    codigo_status: HTTPStatus = HTTPStatus.BAD_REQUEST
    descricao: str = "Nome não pode ser vazio"
    titulo: str | None = "Nome inválido"
    codigo_erro: str | None = "NOME_VAZIO"


@dataclass
class ExcecaoNomeTamanhoMinimo(ExcecaoNome):
    codigo_status: HTTPStatus = HTTPStatus.BAD_REQUEST
    descricao: str = "Nome deve ter pelo menos 2 caracteres"
    titulo: str | None = "Nome inválido"
    codigo_erro: str | None = "NOME_TAMANHO_MINIMO"


@dataclass
class ExcecaoNomeTamanhoMaximo(ExcecaoNome):
    codigo_status: HTTPStatus = HTTPStatus.BAD_REQUEST
    descricao: str = "Nome deve ter no máximo 100 caracteres"
    titulo: str | None = "Nome inválido"
    codigo_erro: str | None = "NOME_TAMANHO_MAXIMO"
