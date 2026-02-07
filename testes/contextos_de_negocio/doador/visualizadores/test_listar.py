from contextos_de_negocio.doador.visualizadores.listar import Listar
from testes.contextos_de_negocio.doador.casos_de_uso import obter_uow_fake
from utilitarios.visualizadores.dtos import ParametrosListagem


def test_deve_transformar_doadores_em_itens(obter_mock_doador):
    uow = obter_uow_fake()
    doador = obter_mock_doador()
    uow.repositorio_doadores.adicionar(doador)

    def obter_uow_com_doador():
        return uow

    visualizador = Listar(obter_uow=obter_uow_com_doador)
    resultado = visualizador.executar(
        ParametrosListagem(filtros_dict={}, pagina=1, itens_por_pagina=10)
    )

    item = resultado.itens[0]
    assert item.id == str(doador.id)
    assert item.nome == doador.nome.valor
    assert item.email == doador.email.valor
    assert item.telefone == doador.telefone.valor
