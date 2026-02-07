from dataclasses import dataclass


@dataclass
class ParametrosListagem:
    filtros_dict: dict
    pagina: int
    itens_por_pagina: int
    ordem: str | None = None
    campos: str | None = None


@dataclass
class ResultadoListagem:
    itens: list
    total: int
    pagina: int
    itens_por_pagina: int
    total_paginas: int
