from dataclasses import dataclass
from typing import Final

from utilitarios.excecoes.endereco import (
    ExcecaoEnderecoTamanhoMaximo,
    ExcecaoEnderecoVazio,
)

TAMANHO_MAXIMO_ENDERECO: Final[int] = 500


@dataclass(frozen=True, slots=True)
class Endereco:
    valor: str

    def __post_init__(self) -> None:
        if not self.valor or not self.valor.strip():
            raise ExcecaoEnderecoVazio()
        if len(self.valor) > TAMANHO_MAXIMO_ENDERECO:
            raise ExcecaoEnderecoTamanhoMaximo()

    def __str__(self) -> str:
        return self.valor
