from contextos_de_negocio.livros.dominio.entidades import Livro
from contextos_de_negocio.livros.dominio.objetos_de_valor import LivroId
from contextos_de_negocio.livros.repositorio import RepositorioLivrosAbstrato
from utilitarios.objetos_de_valor.resultado_paginado import ResultadoPaginado
from utilitarios.unidade_de_trabalho import (
    UnidadeDeTrabalhoAbstrata,
)


class RepositorioLivrosFake(RepositorioLivrosAbstrato):
    def __init__(self):
        self._livros: dict[LivroId, Livro] = {}

    def buscar_por_id(self, livro_id: LivroId) -> Livro | None:
        return self._livros.get(livro_id)

    def adicionar(self, livro: Livro) -> Livro:
        self._livros[livro.id] = livro
        return livro

    def deletar(self, livro: Livro) -> None:
        if livro.id in self._livros:
            del self._livros[livro.id]

    def listar_com_filtros(
        self, filtros, pagina, itens_por_pagina, ordem, campos
    ):
        todos_livros = list(self._livros.values())
        livros_como_dicionarios = self._converter_livros_para_dicionarios(
            todos_livros
        )

        offset = (pagina.valor - 1) * itens_por_pagina.valor
        livros_paginados = livros_como_dicionarios[
            offset : offset + itens_por_pagina.valor
        ]

        return ResultadoPaginado(
            itens=livros_paginados,
            total=len(livros_como_dicionarios),
            pagina=pagina.valor,
            itens_por_pagina=itens_por_pagina.valor,
        )

    def _converter_livros_para_dicionarios(self, livros):
        livros_como_dicionarios = []

        for livro in livros:
            livro_dicionario = {
                "id": livro.id,
                "titulo": livro.titulo,
                "subtitulo": livro.subtitulo if livro.subtitulo else None,
                "autores": livro.autores,
                "isbn": livro.isbn if livro.isbn else None,
                "foto_url": livro.foto_url if livro.foto_url else None,
                "observacao": livro.observacao if livro.observacao else None,
            }
            livros_como_dicionarios.append(livro_dicionario)

        return livros_como_dicionarios


class UnidadeDeTrabalhoFake(UnidadeDeTrabalhoAbstrata):
    def __init__(self):
        self.repositorio_livros = RepositorioLivrosFake()
        self._committed = False
        self._rolled_back = False

    def commit(self):
        self._committed = True

    def rollback(self):
        self._rolled_back = False

    def __enter__(self):
        return self

    def __exit__(self, tipo_excecao, valor_excecao, traceback_excecao):
        if tipo_excecao is not None:
            self.rollback()


def obter_uow_fake():
    return UnidadeDeTrabalhoFake()
