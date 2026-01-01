from dataclasses import dataclass
from typing import Final

from utilitarios.excecoes.descricao import (
    ExcecaoDescricaoTamanhoMaximo,
    ExcecaoDescricaoVazia,
)

TAMANHO_MAXIMO_DESCRICAO: Final[int] = 1000


@dataclass(frozen=True, slots=True)
class Descricao:
    valor: str

    def __post_init__(self) -> None:
        if not self.valor or not self.valor.strip():
            raise ExcecaoDescricaoVazia()
        if len(self.valor) > TAMANHO_MAXIMO_DESCRICAO:
            raise ExcecaoDescricaoTamanhoMaximo()

    def __str__(self) -> str:
        return self.valor
