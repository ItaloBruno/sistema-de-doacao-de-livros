from collections.abc import Callable

from contextos_de_negocio.doador.visualizadores.dtos import ItemDoador
from utilitarios.objetos_de_valor.filtragem import ConjuntoFiltros
from utilitarios.objetos_de_valor.paginacao import (
    ItensPorPagina,
    NumeroPagina,
)
from utilitarios.visualizadores.dtos import (
    ParametrosListagem,
    ResultadoListagem,
)


class Listar:
    def __init__(self, obter_uow: Callable):
        self.obter_uow = obter_uow

    def executar(self, parametros: ParametrosListagem) -> ResultadoListagem:
        filtros = ConjuntoFiltros.de_dict(parametros.filtros_dict)
        pagina = NumeroPagina(parametros.pagina)
        itens_por_pagina = ItensPorPagina(parametros.itens_por_pagina)

        with self.obter_uow() as uow:
            resultado = uow.repositorio_doadores.listar_com_filtros(
                filtros,
                pagina,
                itens_por_pagina,
                parametros.ordem,
                parametros.campos,
            )

            return ResultadoListagem(
                itens=[
                    ItemDoador(
                        id=str(doador.get("id").valor)
                        if doador.get("id")
                        else None,
                        nome=doador.get("nome").valor,
                        email=doador.get("email").valor,
                        telefone=doador.get("telefone").valor,
                    )
                    for doador in resultado.itens
                ],
                total=resultado.total,
                pagina=resultado.pagina,
                itens_por_pagina=resultado.itens_por_pagina,
                total_paginas=resultado.total_paginas,
            )
