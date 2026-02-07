from dataclasses import dataclass
from http import HTTPStatus

from utilitarios.excecoes.base import ExcecaoBase


@dataclass
class ExcecaoEndereco(ExcecaoBase):
    pass


@dataclass
class ExcecaoEnderecoVazio(ExcecaoEndereco):
    codigo_status: HTTPStatus = HTTPStatus.BAD_REQUEST
    descricao: str = "Endereço não pode ser vazio"
    titulo: str | None = "Endereço inválido"
    codigo_erro: str | None = "ENDERECO_VAZIO"


@dataclass
class ExcecaoEnderecoTamanhoMaximo(ExcecaoEndereco):
    codigo_status: HTTPStatus = HTTPStatus.BAD_REQUEST
    descricao: str = "Endereço deve ter no máximo 500 caracteres"
    titulo: str | None = "Endereço inválido"
    codigo_erro: str | None = "ENDERECO_TAMANHO_MAXIMO"
