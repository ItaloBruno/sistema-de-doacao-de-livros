from dataclasses import dataclass
from http import HTTPStatus

from utilitarios.excecoes.base import ExcecaoBase


@dataclass
class ExcecaoDescricao(ExcecaoBase):
    pass


@dataclass
class ExcecaoDescricaoVazia(ExcecaoDescricao):
    codigo_status: HTTPStatus = HTTPStatus.BAD_REQUEST
    descricao: str = "Descrição não pode ser vazia"
    titulo: str | None = "Descrição inválida"
    codigo_erro: str | None = "DESCRICAO_VAZIA"


@dataclass
class ExcecaoDescricaoTamanhoMaximo(ExcecaoDescricao):
    codigo_status: HTTPStatus = HTTPStatus.BAD_REQUEST
    descricao: str = "Descrição deve ter no máximo 1000 caracteres"
    titulo: str | None = "Descrição inválida"
    codigo_erro: str | None = "DESCRICAO_TAMANHO_MAXIMO"
