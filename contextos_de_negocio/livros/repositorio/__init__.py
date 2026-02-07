from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.orm import Session

from contextos_de_negocio.livros.dominio.entidades import Livro
from contextos_de_negocio.livros.dominio.objetos_de_valor import LivroId
from contextos_de_negocio.livros.repositorio.orm import tabela_livros
from utilitarios.objetos_de_valor.filtragem import ConjuntoFiltros
from utilitarios.objetos_de_valor.paginacao import (
    ItensPorPagina,
    NumeroPagina,
)
from utilitarios.objetos_de_valor.resultado_paginado import ResultadoPaginado
from utilitarios.sqlalchemy.filtragem import FiltragemSQLAlchemy
from utilitarios.sqlalchemy.ordenador import OrdenadorSQLAlchemy
from utilitarios.sqlalchemy.paginador import PaginadorSQLAlchemy
from utilitarios.sqlalchemy.projetor import ProjetorSQLAlchemy


class RepositorioLivrosAbstrato(ABC):
    @abstractmethod
    def buscar_por_id(self, livro_id: LivroId) -> Livro | None:
        pass

    @abstractmethod
    def adicionar(self, livro: Livro) -> Livro:
        pass

    @abstractmethod
    def deletar(self, livro: Livro) -> None:
        pass

    @abstractmethod
    def listar_com_filtros(
        self,
        filtros: ConjuntoFiltros,
        pagina: NumeroPagina,
        itens_por_pagina: ItensPorPagina,
        ordem: str | None = None,
        campos: str | None = None,
    ) -> ResultadoPaginado:
        pass


class RepositorioLivros(RepositorioLivrosAbstrato):
    def __init__(self, sessao: Session):
        self._sessao = sessao

    def buscar_por_id(self, livro_id: LivroId) -> Livro | None:
        return self._sessao.get(Livro, str(livro_id.valor))

    def adicionar(self, livro: Livro) -> Livro:
        livro_atualizado = self._sessao.merge(livro)
        self._sessao.flush()
        return livro_atualizado

    def deletar(self, livro: Livro) -> None:
        self._sessao.delete(livro)
        self._sessao.flush()

    def listar_com_filtros(
        self,
        filtros: ConjuntoFiltros,
        pagina: NumeroPagina,
        itens_por_pagina: ItensPorPagina,
        ordem: str | None = None,
        campos: str | None = None,
    ) -> ResultadoPaginado:
        projetor = ProjetorSQLAlchemy(tabela_livros)
        colunas = projetor.construir_projecoes(campos)

        if colunas:
            query = select(*colunas)
        else:
            query = select(*list(tabela_livros.c))

        filtragem = FiltragemSQLAlchemy(tabela_livros)
        query = filtragem.aplicar_filtros(query, filtros.para_dict())

        ordenador = OrdenadorSQLAlchemy(tabela_livros)
        query = ordenador.aplicar_ordenacao(query, ordem)

        paginador = PaginadorSQLAlchemy(
            self._sessao,
            pagina=pagina.valor,
            itens_por_pagina=itens_por_pagina.valor,
        )
        return paginador.paginar(query)
