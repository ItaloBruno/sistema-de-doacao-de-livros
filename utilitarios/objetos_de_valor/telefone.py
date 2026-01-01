import re
from dataclasses import dataclass
from typing import Final

from utilitarios.excecoes.telefone import (
    ExcecaoTelefoneInvalido,
    ExcecaoTelefoneVazio,
)

TAMANHO_MINIMO_TELEFONE: Final[int] = 10
TAMANHO_MAXIMO_TELEFONE: Final[int] = 11


@dataclass(frozen=True, slots=True)
class Telefone:
    valor: str

    def __post_init__(self) -> None:
        if not self.valor:
            raise ExcecaoTelefoneVazio()
        digitos = re.sub(r"\D", "", self.valor)
        if (
            len(digitos) < TAMANHO_MINIMO_TELEFONE
            or len(digitos) > TAMANHO_MAXIMO_TELEFONE
        ):
            raise ExcecaoTelefoneInvalido()

    @property
    def apenas_digitos(self) -> str:
        return re.sub(r"\D", "", self.valor)

    def __str__(self) -> str:
        return self.valor
