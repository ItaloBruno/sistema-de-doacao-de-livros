from dataclasses import dataclass
from http import HTTPStatus

from utilitarios.excecoes.base import ExcecaoBase


@dataclass
class ExcecaoSite(ExcecaoBase):
    pass


@dataclass
class ExcecaoSiteTamanhoMaximo(ExcecaoSite):
    codigo_status: HTTPStatus = HTTPStatus.BAD_REQUEST
    descricao: str = "Site deve ter no máximo 255 caracteres"
    titulo: str | None = "Site inválido"
    codigo_erro: str | None = "SITE_TAMANHO_MAXIMO"
