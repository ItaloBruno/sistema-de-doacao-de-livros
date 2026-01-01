from dataclasses import dataclass
from http import HTTPStatus

from utilitarios.excecoes.base import ExcecaoBase


@dataclass
class FormatoFiltroInvalido(ExcecaoBase):
    operador_e_valor: str = ""
    codigo_status: HTTPStatus = HTTPStatus.BAD_REQUEST
    descricao: str = ""
    titulo: str | None = "Formato de filtro inválido"
    codigo_erro: str | None = "FORMATO_FILTRO_INVALIDO"

    def __post_init__(self):
        if not self.descricao:
            self.descricao = (
                f"Formato inválido: {self.operador_e_valor}. "
                f"Esperado: 'operador.valor'"
            )


@dataclass
class OperadorFiltroInvalido(ExcecaoBase):
    operador: str = ""
    codigo_status: HTTPStatus = HTTPStatus.BAD_REQUEST
    descricao: str = ""
    titulo: str | None = "Operador de filtro inválido"
    codigo_erro: str | None = "OPERADOR_FILTRO_INVALIDO"

    def __post_init__(self):
        if not self.descricao:
            self.descricao = f"Operador inválido: {self.operador}"
