from collections.abc import Callable

from contextos_de_negocio.livros.visualizadores.dtos import ItemLivro
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
            resultado = uow.repositorio_livros.listar_com_filtros(
                filtros,
                pagina,
                itens_por_pagina,
                parametros.ordem,
                parametros.campos,
            )

            return ResultadoListagem(
                itens=[
                    ItemLivro(
                        id=str(livro.get("id").valor)
                        if livro.get("id")
                        else None,
                        titulo=livro.get("titulo").valor,
                        autores=[
                            autor for autor in livro.get("autores").valor
                        ],
                        subtitulo=livro.get("subtitulo").valor,
                        isbn=livro.get("isbn").valor,
                        observacao=livro.get("observacao").valor,
                        foto=livro.get("foto_url").valor
                        if livro.get("foto_url")
                        else None,
                    )
                    for livro in resultado.itens
                ],
                total=resultado.total,
                pagina=resultado.pagina,
                itens_por_pagina=resultado.itens_por_pagina,
                total_paginas=resultado.total_paginas,
            )
