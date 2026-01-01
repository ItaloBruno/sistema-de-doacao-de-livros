from dataclasses import dataclass
from typing import Final

from utilitarios.excecoes.site import ExcecaoSiteTamanhoMaximo

TAMANHO_MAXIMO_SITE: Final[int] = 255


@dataclass(frozen=True, slots=True)
class Site:
    valor: str

    def __post_init__(self) -> None:
        if len(self.valor) > TAMANHO_MAXIMO_SITE:
            raise ExcecaoSiteTamanhoMaximo()

    def __str__(self) -> str:
        return self.valor
