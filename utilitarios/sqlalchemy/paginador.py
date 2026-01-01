from sqlalchemy import func, select

from utilitarios.banco_de_dados.paginador import Paginador
from utilitarios.objetos_de_valor.resultado_paginado import ResultadoPaginado


class PaginadorSQLAlchemy(Paginador):
    def __init__(self, sessao, pagina=1, itens_por_pagina=10):
        super().__init__(pagina, itens_por_pagina)
        self.sessao = sessao

    def paginar(self, query):
        total = self.sessao.execute(
            select(func.count()).select_from(query.subquery())
        ).scalar()

        offset = (self.pagina - 1) * self.itens_por_pagina
        itens = (
            self.sessao.execute(
                query.limit(self.itens_por_pagina).offset(offset)
            )
            .mappings()
            .all()
        )

        return ResultadoPaginado(
            itens=list(itens),
            total=total,
            pagina=self.pagina,
            itens_por_pagina=self.itens_por_pagina,
        )
