from dataclasses import dataclass

from utilitarios.excecoes.email import ExcecaoEmailVazio
from utilitarios.pydantic.validador_email import validar_email


@dataclass(frozen=True, slots=True)
class Email:
    valor: str

    def __post_init__(self) -> None:
        if not self.valor:
            raise ExcecaoEmailVazio()
        validar_email(self.valor)

    def __str__(self) -> str:
        return self.valor
