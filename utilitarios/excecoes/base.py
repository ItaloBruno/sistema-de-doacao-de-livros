from dataclasses import dataclass
from http import HTTPStatus


@dataclass
class ExcecaoBase(Exception):
    codigo_status: HTTPStatus
    descricao: str
    titulo: str | None = None
    codigo_erro: str | None = None

    def __str__(self) -> str:
        return self.descricao
