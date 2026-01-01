from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.orm import Session

from contextos_de_negocio.doador.dominio.entidades import Doador
from contextos_de_negocio.doador.dominio.objetos_de_valor import DoadorId
from contextos_de_negocio.doador.repositorio.orm import tabela_doadores


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
