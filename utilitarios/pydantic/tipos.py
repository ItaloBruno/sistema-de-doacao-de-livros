import re
from typing import Annotated

from pydantic import EmailStr, StringConstraints


def validar_telefone(valor):
    digitos = re.sub(r"\D", "", valor)
    if not valor:
        raise ValueError("Telefone não pode ser vazio")
    if len(digitos) < 10 or len(digitos) > 11:
        raise ValueError("Telefone deve ter 10 ou 11 dígitos")
    return valor


Nome = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=2,
        max_length=100,
    ),
]

Senha = Annotated[
    str,
    StringConstraints(min_length=6, max_length=100),
]

Telefone = Annotated[
    str,
    validar_telefone,
]

Email = Annotated[
    EmailStr,
    StringConstraints(
        strip_whitespace=True,
        min_length=3,
        max_length=255,
    ),
]

Token = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
    ),
]

Descricao = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=1000,
    ),
]

Endereco = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=500,
    ),
]

Site = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        max_length=255,
    ),
]

Id = str

DataFundacao = str

Foto = str
