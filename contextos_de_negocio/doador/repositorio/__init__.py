from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.orm import Session

from contextos_de_negocio.doador.dominio.entidades import Doador
from contextos_de_negocio.doador.dominio.objetos_de_valor import DoadorId
from contextos_de_negocio.doador.repositorio.orm import tabela_doadores
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


class RepositorioDoadoresAbstrato(ABC):
    @abstractmethod
    def buscar_por_email(self, email: str) -> Doador | None:
        pass

    @abstractmethod
    def buscar_por_id(self, doador_id: DoadorId) -> Doador | None:
        pass

    @abstractmethod
    def adicionar(self, doador: Doador) -> Doador:
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


class RepositorioDoadores(RepositorioDoadoresAbstrato):
    def __init__(self, sessao: Session):
        self._sessao = sessao

    def buscar_por_email(self, email: str) -> Doador | None:
        return self._sessao.execute(
            select(Doador).where(tabela_doadores.c.email == email)
        ).scalar_one_or_none()

    def buscar_por_id(self, doador_id: DoadorId) -> Doador | None:
        return self._sessao.get(Doador, str(doador_id.valor))

    def adicionar(self, doador: Doador) -> Doador:
        doador_atualizado = self._sessao.merge(doador)
        self._sessao.flush()
        return doador_atualizado

    def listar_com_filtros(
        self,
        filtros: ConjuntoFiltros,
        pagina: NumeroPagina,
        itens_por_pagina: ItensPorPagina,
        ordem: str | None = None,
        campos: str | None = None,
    ) -> ResultadoPaginado:
        projetor = ProjetorSQLAlchemy(tabela_doadores)
        colunas = projetor.construir_projecoes(campos)

        if colunas:
            query = select(*colunas)
        else:
            query = select(*list(tabela_doadores.c))

        filtragem = FiltragemSQLAlchemy(tabela_doadores)
        query = filtragem.aplicar_filtros(query, filtros.para_dict())

        ordenador = OrdenadorSQLAlchemy(tabela_doadores)
        query = ordenador.aplicar_ordenacao(query, ordem)

        paginador = PaginadorSQLAlchemy(
            self._sessao,
            pagina=pagina.valor,
            itens_por_pagina=itens_por_pagina.valor,
        )
        return paginador.paginar(query)
