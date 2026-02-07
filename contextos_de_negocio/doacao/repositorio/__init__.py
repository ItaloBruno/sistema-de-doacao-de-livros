from abc import ABC, abstractmethod

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from contextos_de_negocio.doacao.dominio.entidades import Doacao
from contextos_de_negocio.doacao.dominio.objetos_de_valor import (
    DoacaoId,
    LivroNaDoacao,
)
from contextos_de_negocio.doacao.repositorio.orm import tabela_doacoes_livros
from contextos_de_negocio.instituicao.dominio.objetos_de_valor import (
    InstituicaoId,
)
from contextos_de_negocio.instituicao.repositorio.orm import (
    tabela_instituicoes,
)
from contextos_de_negocio.livros.dominio.objetos_de_valor import LivroId
from contextos_de_negocio.livros.repositorio.orm import tabela_livros


class RepositorioDoacoesAbstrato(ABC):
    @abstractmethod
    def buscar_por_id(self, doacao_id: DoacaoId) -> Doacao | None:
        pass

    @abstractmethod
    def adicionar(self, doacao: Doacao) -> Doacao:
        pass

    @abstractmethod
    def instituicao_existe(self, instituicao_id: InstituicaoId) -> bool:
        pass

    @abstractmethod
    def livros_existem(self, livros_ids: list[LivroId]) -> bool:
        pass


class RepositorioDoacoes(RepositorioDoacoesAbstrato):
    def __init__(self, sessao: Session):
        self._sessao = sessao

    def buscar_por_id(self, doacao_id: DoacaoId) -> Doacao | None:
        doacao = self._sessao.get(Doacao, str(doacao_id.valor))
        if not doacao:
            return None

        query = select(tabela_doacoes_livros.c.livro_id).where(
            tabela_doacoes_livros.c.doacao_id == str(doacao_id.valor)
        )
        livros_ids_resultado = self._sessao.execute(query).scalars().all()
        doacao.livros = [
            LivroNaDoacao(livro_id=LivroId(livro_id))
            for livro_id in livros_ids_resultado
        ]

        return doacao

    def adicionar(self, doacao: Doacao) -> Doacao:
        doacao_atualizada = self._sessao.merge(doacao)
        self._sessao.flush()
        return doacao_atualizada

    def instituicao_existe(self, instituicao_id: InstituicaoId) -> bool:
        query = (
            select(func.count())
            .select_from(tabela_instituicoes)
            .where(tabela_instituicoes.c.id == str(instituicao_id.valor))
        )
        resultado = self._sessao.execute(query).scalar()
        return resultado > 0

    def livros_existem(self, livros_ids: list[LivroId]) -> bool:
        livros_ids_str = [str(livro_id.valor) for livro_id in livros_ids]

        query = (
            select(func.count())
            .select_from(tabela_livros)
            .where(tabela_livros.c.id.in_(livros_ids_str))
        )
        resultado = self._sessao.execute(query).scalar()
        return resultado == len(livros_ids)
