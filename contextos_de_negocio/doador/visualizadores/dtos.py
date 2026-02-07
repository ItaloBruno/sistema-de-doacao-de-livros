from dataclasses import dataclass


@dataclass
class ItemDoador:
    id: str | None = None
    nome: str | None = None
    email: str | None = None
    telefone: str | None = None
