import pytest

from contextos_de_negocio.doador.dominio.entidades import Doador
from contextos_de_negocio.doador.dominio.objetos_de_valor import (
    DoadorId,
    EmailDoador,
    NomeDoador,
    SenhaDoador,
    TelefoneDoador,
)


@pytest.fixture
def obter_mock_doador():
    def _criar(id: DoadorId | None = None, **kwargs):
        nome = NomeDoador(kwargs.get("nome", "João da Silva"))
        email = EmailDoador(kwargs.get("email", "joao.silva@example.com"))
        senha = SenhaDoador(kwargs.get("senha", "senha123"))
        telefone = TelefoneDoador(kwargs.get("telefone", "11999999999"))

        if id is None:
            return Doador.criar(
                nome=nome,
                email=email,
                senha=senha,
                telefone=telefone,
            )

        return Doador(
            id=id,
            nome=nome,
            email=email,
            senha=senha,
            telefone=telefone,
        )

    return _criar


@pytest.fixture
def obter_mock_doador_no_banco(uow, obter_mock_doador):
    def _inserir(id: DoadorId | None = None, **kwargs) -> Doador:
        doador = obter_mock_doador(id=id, **kwargs)

        doador_criado = uow.repositorio_doadores.adicionar(doador)
        uow.commit()
        return doador_criado

    return _inserir
