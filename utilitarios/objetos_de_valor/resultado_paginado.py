import math
from dataclasses import dataclass


@dataclass
class ResultadoPaginado:
    itens: list
    total: int
    pagina: int
    itens_por_pagina: int

    @property
    def total_paginas(self):
        if self.itens_por_pagina == 0:
            return 0
        return math.ceil(self.total / self.itens_por_pagina)
