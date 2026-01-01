from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.orm import Session

from contextos_de_negocio.instituicao.dominio.entidades import Instituicao
from contextos_de_negocio.instituicao.dominio.objetos_de_valor import (
    InstituicaoId,
)
from contextos_de_negocio.instituicao.repositorio.orm import (
    tabela_instituicoes,
)


class RepositorioInstituicoesAbstrato(ABC):
    @abstractmethod
    def buscar_por_email(self, email: str) -> Instituicao | None:
        pass

    @abstractmethod
    def buscar_por_id(
        self, instituicao_id: InstituicaoId
    ) -> Instituicao | None:
        pass

    @abstractmethod
    def adicionar(self, instituicao: Instituicao) -> Instituicao:
        pass


class RepositorioInstituicoes(RepositorioInstituicoesAbstrato):
    def __init__(self, sessao: Session):
        self._sessao = sessao

    def buscar_por_email(self, email: str) -> Instituicao | None:
        return self._sessao.execute(
            select(Instituicao).where(tabela_instituicoes.c.email == email)
        ).scalar_one_or_none()

    def buscar_por_id(
        self, instituicao_id: InstituicaoId
    ) -> Instituicao | None:
        return self._sessao.get(Instituicao, str(instituicao_id.valor))

    def adicionar(self, instituicao: Instituicao) -> Instituicao:
        instituicao_atualizada = self._sessao.merge(instituicao)
        self._sessao.flush()
        return instituicao_atualizada
