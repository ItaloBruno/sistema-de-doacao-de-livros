from contextos_de_negocio.doacao.dominio.entidades import Doacao
from contextos_de_negocio.doacao.dominio.objetos_de_valor import DoacaoId
from contextos_de_negocio.doacao.repositorio import RepositorioDoacoesAbstrato
from contextos_de_negocio.instituicao.dominio.objetos_de_valor import (
    InstituicaoId,
)
from contextos_de_negocio.livros.dominio.objetos_de_valor import LivroId
from utilitarios.unidade_de_trabalho import (
    UnidadeDeTrabalhoAbstrata,
)


class RepositorioDoacoesFake(RepositorioDoacoesAbstrato):
    def __init__(self):
        self._doacoes: dict[DoacaoId, Doacao] = {}
        self._instituicoes_existentes: set[InstituicaoId] = set()
        self._livros_existentes: set[LivroId] = set()

    def buscar_por_id(self, doacao_id: DoacaoId) -> Doacao | None:
        return self._doacoes.get(doacao_id)

    def adicionar(self, doacao: Doacao) -> Doacao:
        self._doacoes[doacao.id] = doacao
        return doacao

    def instituicao_existe(self, instituicao_id: InstituicaoId) -> bool:
        return instituicao_id in self._instituicoes_existentes

    def livros_existem(self, livros_ids: list[LivroId]) -> bool:
        return all(
            livro_id in self._livros_existentes for livro_id in livros_ids
        )

    def adicionar_instituicao_existente(self, instituicao_id: InstituicaoId):
        self._instituicoes_existentes.add(instituicao_id)

    def adicionar_livro_existente(self, livro_id: LivroId):
        self._livros_existentes.add(livro_id)


class UnidadeDeTrabalhoFake(UnidadeDeTrabalhoAbstrata):
    def __init__(self):
        self.repositorio_doacoes = RepositorioDoacoesFake()
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
