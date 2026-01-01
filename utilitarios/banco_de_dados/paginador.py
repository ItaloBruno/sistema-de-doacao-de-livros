from abc import ABC, abstractmethod

from utilitarios.objetos_de_valor.resultado_paginado import ResultadoPaginado


class Paginador(ABC):
    def __init__(self, pagina=1, itens_por_pagina=10):
        self.pagina = pagina
        self.itens_por_pagina = itens_por_pagina

    @abstractmethod
    def paginar(self, query) -> ResultadoPaginado:
        pass
