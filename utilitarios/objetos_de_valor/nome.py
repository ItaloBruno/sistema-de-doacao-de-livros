from dataclasses import dataclass
from typing import Final

from utilitarios.excecoes.nome import (
    ExcecaoNomeTamanhoMaximo,
    ExcecaoNomeTamanhoMinimo,
    ExcecaoNomeVazio,
)

TAMANHO_MINIMO_NOME: Final[int] = 2
TAMANHO_MAXIMO_NOME: Final[int] = 100


@dataclass(frozen=True, slots=True)
class Nome:
    valor: str

    def __post_init__(self) -> None:
        if not self.valor or not self.valor.strip():
            raise ExcecaoNomeVazio()
        if len(self.valor) < TAMANHO_MINIMO_NOME:
            raise ExcecaoNomeTamanhoMinimo()
        if len(self.valor) > TAMANHO_MAXIMO_NOME:
            raise ExcecaoNomeTamanhoMaximo()

    def __str__(self) -> str:
        return self.valor
