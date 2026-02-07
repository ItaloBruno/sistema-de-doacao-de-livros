import pytest

from contextos_de_negocio.doacao.dominio.entidades import Doacao
from contextos_de_negocio.doacao.dominio.objetos_de_valor import (
    DoacaoId,
    LivroNaDoacao,
)
from contextos_de_negocio.doador.dominio.objetos_de_valor import DoadorId
from contextos_de_negocio.instituicao.dominio.objetos_de_valor import (
    InstituicaoId,
)
from contextos_de_negocio.livros.dominio.objetos_de_valor import LivroId


@pytest.fixture
def obter_mock_doacao():
    def _criar(id: DoacaoId | None = None, **kwargs):
        doador_id = kwargs.get("doador_id", DoadorId.gerar())
        instituicao_id = kwargs.get("instituicao_id", InstituicaoId.gerar())
        livros_ids = kwargs.get("livros_ids", [LivroId.gerar()])

        livros = [LivroNaDoacao(livro_id=livro_id) for livro_id in livros_ids]

        if id is None:
            return Doacao.criar(
                doador_id=doador_id,
                instituicao_id=instituicao_id,
                livros=livros,
            )

        return Doacao(
            id=id,
            doador_id=doador_id,
            instituicao_id=instituicao_id,
            livros=livros,
        )

    return _criar


@pytest.fixture
def obter_mock_doacao_no_banco(uow, obter_mock_doacao):
    def _inserir(id: DoacaoId | None = None, **kwargs) -> Doacao:
        doacao = obter_mock_doacao(id=id, **kwargs)

        doacao_criada = uow.repositorio_doacoes.adicionar(doacao)
        uow.commit()
        return doacao_criada

    return _inserir
