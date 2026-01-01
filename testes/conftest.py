import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from contextos_de_negocio.app import app
from contextos_de_negocio.doador.repositorio.orm import (
    metadata as metadata_doador,
)
from contextos_de_negocio.instituicao.repositorio.orm import (
    metadata as metadata_instituicao,
)
from contextos_de_negocio.livros.repositorio.orm import (
    metadata as metadata_livros,
)
from testes.contextos_de_negocio.doador.mocks import (
    obter_mock_doador,
    obter_mock_doador_no_banco,
)
from testes.contextos_de_negocio.instituicao.mocks import (
    obter_mock_instituicao,
    obter_mock_instituicao_no_banco,
)
from testes.contextos_de_negocio.livros.mocks import (
    obter_mock_livro,
    obter_mock_livro_no_banco,
)
from testes.utilitarios.banco_de_dados.mocks import (
    metadata_produtos_mock,
    obter_mock_produto_no_banco,
)
from utilitarios.provedor_de_hash import ProvedorDeHash
from utilitarios.provedor_de_hash.argon2 import EstrategiaArgon2
from utilitarios.provedor_de_token import ProvedorDeToken
from utilitarios.provedor_de_token.pyjwt import EstrategiaPyJWT
from utilitarios.unidade_de_trabalho import (
    unidade_de_trabalho,
)
from utilitarios.variaveis_de_ambiente import VariaveisDeAmbiente

__all__ = [
    "obter_mock_doador",
    "obter_mock_doador_no_banco",
    "obter_mock_instituicao",
    "obter_mock_instituicao_no_banco",
    "obter_mock_livro",
    "obter_mock_livro_no_banco",
    "obter_mock_produto_no_banco",
]


@pytest.fixture(scope="session")
def motor_banco():
    url = VariaveisDeAmbiente.URL_POSTGRES
    motor = create_engine(url)
    metadata_doador.drop_all(motor)
    metadata_instituicao.drop_all(motor)
    metadata_livros.drop_all(motor)
    metadata_produtos_mock.drop_all(motor)
    metadata_doador.create_all(motor)
    metadata_instituicao.create_all(motor)
    metadata_livros.create_all(motor)
    metadata_produtos_mock.create_all(motor)

    yield motor

    motor.dispose()


@pytest.fixture
def limpa_tabelas(motor_banco):
    with motor_banco.begin() as conexao:
        conexao.execute(text("DELETE FROM livros;"))
        conexao.execute(text("DELETE FROM instituicoes;"))
        conexao.execute(text("DELETE FROM doadores;"))
        conexao.execute(text("DELETE FROM produtos_mock;"))

    yield

    with motor_banco.begin() as conexao:
        conexao.execute(text("DELETE FROM livros;"))
        conexao.execute(text("DELETE FROM instituicoes;"))
        conexao.execute(text("DELETE FROM doadores;"))
        conexao.execute(text("DELETE FROM produtos_mock;"))


@pytest.fixture
def cliente_api(limpa_tabelas):
    with TestClient(app) as cliente:
        yield cliente


@pytest.fixture
def uow(limpa_tabelas):
    unidade = unidade_de_trabalho()

    with unidade:
        yield unidade


@pytest.fixture
def provedor_de_hash():
    return ProvedorDeHash(EstrategiaArgon2())


@pytest.fixture
def provedor_de_token():
    return ProvedorDeToken(EstrategiaPyJWT())


@pytest.fixture
def obter_token_autenticacao(provedor_de_token):
    def _obter_token(doador_id):
        return provedor_de_token.gerar_token_de_acesso(doador_id)

    return _obter_token
