from contextos_de_negocio.instituicao.dominio.entidades import Instituicao
from contextos_de_negocio.instituicao.dominio.objetos_de_valor import (
    InstituicaoId,
)
from contextos_de_negocio.instituicao.repositorio import (
    RepositorioInstituicoesAbstrato,
)
from utilitarios.unidade_de_trabalho import (
    UnidadeDeTrabalhoAbstrata,
)


class RepositorioInstituicoesFake(RepositorioInstituicoesAbstrato):
    def __init__(self):
        self._instituicoes: dict[InstituicaoId, Instituicao] = {}
        self._instituicoes_por_email: dict[str, Instituicao] = {}

    def buscar_por_email(self, email: str) -> Instituicao | None:
        return self._instituicoes_por_email.get(email)

    def buscar_por_id(self, instituicao_id) -> Instituicao | None:
        return self._instituicoes.get(instituicao_id)

    def adicionar(self, instituicao: Instituicao) -> Instituicao:
        if instituicao.id is None:
            instituicao.id = InstituicaoId.gerar()

        self._instituicoes[instituicao.id] = instituicao
        self._instituicoes_por_email[instituicao.email.valor] = instituicao
        return instituicao


class UnidadeDeTrabalhoFake(UnidadeDeTrabalhoAbstrata):
    def __init__(self):
        self.repositorio_instituicoes = RepositorioInstituicoesFake()
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
