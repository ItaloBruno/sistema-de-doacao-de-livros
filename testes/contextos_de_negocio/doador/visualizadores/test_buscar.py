import pytest

from contextos_de_negocio.doador.excecoes import DoadorNaoEncontrado
from contextos_de_negocio.doador.visualizadores.buscar import Buscar
from testes.contextos_de_negocio.doador.casos_de_uso import obter_uow_fake


def test_deve_retornar_doador_por_id_com_sucesso(obter_mock_doador):
    uow = obter_uow_fake()
    doador = obter_mock_doador()
    uow.repositorio_doadores.adicionar(doador)

    def obter_uow_com_doador():
        return uow

    visualizador = Buscar(obter_uow=obter_uow_com_doador)
    resultado = visualizador.executar(str(doador.id))

    assert resultado.id == str(doador.id)
    assert resultado.nome == doador.nome.valor
    assert resultado.email == doador.email.valor
    assert resultado.telefone == doador.telefone.valor


def test_deve_lancar_excecao_quando_doador_nao_existe():
    visualizador = Buscar(obter_uow=obter_uow_fake)

    with pytest.raises(DoadorNaoEncontrado):
        visualizador.executar("00000000-0000-0000-0000-000000000000")
