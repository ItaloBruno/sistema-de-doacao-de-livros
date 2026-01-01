from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Final, Self

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from contextos_de_negocio.doador.repositorio import (
    RepositorioDoadores,
    RepositorioDoadoresAbstrato,
)
from contextos_de_negocio.doador.repositorio.orm import (
    metadata as metadata_doador,
)
from contextos_de_negocio.instituicao.repositorio import (
    RepositorioInstituicoes,
    RepositorioInstituicoesAbstrato,
)
from contextos_de_negocio.instituicao.repositorio.orm import (
    metadata as metadata_instituicao,
)
from contextos_de_negocio.livros.repositorio import (
    RepositorioLivros,
    RepositorioLivrosAbstrato,
)
from contextos_de_negocio.livros.repositorio.orm import (
    metadata as metadata_livros,
)
from utilitarios.variaveis_de_ambiente import (
    VariaveisDeAmbiente,
)


class UnidadeDeTrabalhoAbstrata(ABC):
    repositorio_doadores: RepositorioDoadoresAbstrato
    repositorio_instituicoes: RepositorioInstituicoesAbstrato
    repositorio_livros: RepositorioLivrosAbstrato

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def __enter__(self) -> Self:
        pass

    @abstractmethod
    def __exit__(self, tipo_excecao, valor_excecao, traceback_excecao):
        pass


class UnidadeDeTrabalho(UnidadeDeTrabalhoAbstrata):
    def __init__(self, fabrica_sessao: Callable[[], Session]):
        self._fabrica_sessao = fabrica_sessao
        self._sessao_postgres: Session | None = None

    def __enter__(self) -> Self:
        self._sessao_postgres = self._fabrica_sessao()
        self.repositorio_doadores = RepositorioDoadores(self._sessao_postgres)
        self.repositorio_instituicoes = RepositorioInstituicoes(
            self._sessao_postgres
        )
        self.repositorio_livros = RepositorioLivros(self._sessao_postgres)
        return self

    def __exit__(self, tipo_excecao, valor_excecao, traceback_excecao) -> None:
        if tipo_excecao is not None:
            self.rollback()
        self.sessao_postgres.close()

    @property
    def sessao_postgres(self) -> Session:
        if self._sessao_postgres is None:
            raise ValueError("Sessão não foi inicializada")
        return self._sessao_postgres

    def commit(self) -> None:
        self.sessao_postgres.commit()

    def rollback(self) -> None:
        self.sessao_postgres.rollback()


class _GerenciadorMotor:
    def __init__(self):
        self._motor = None

    def obter_motor(self):
        if not self._motor:
            url = VariaveisDeAmbiente.URL_POSTGRES
            self._motor = create_engine(url)
            metadata_doador.create_all(self._motor)
            metadata_instituicao.create_all(self._motor)
            metadata_livros.create_all(self._motor)
        return self._motor


_gerenciador: Final[_GerenciadorMotor] = _GerenciadorMotor()


def unidade_de_trabalho() -> UnidadeDeTrabalho:
    motor = _gerenciador.obter_motor()
    fabrica_sessao = sessionmaker(bind=motor, expire_on_commit=False)
    return UnidadeDeTrabalho(fabrica_sessao)
