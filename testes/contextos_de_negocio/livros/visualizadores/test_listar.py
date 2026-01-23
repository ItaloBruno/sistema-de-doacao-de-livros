from contextos_de_negocio.livros.visualizadores.listar import Listar
from testes.contextos_de_negocio.livros.casos_de_uso import obter_uow_fake
from utilitarios.visualizadores.dtos import ParametrosListagem


def test_deve_listar_livros_com_sucesso(obter_mock_livro):
    uow = obter_uow_fake()
    livro1 = obter_mock_livro()
    livro2 = obter_mock_livro()
    uow.repositorio_livros.adicionar(livro1)
    uow.repositorio_livros.adicionar(livro2)

    def obter_uow_com_livros():
        return uow

    visualizador = Listar(obter_uow=obter_uow_com_livros)
    resultado = visualizador.executar(
        ParametrosListagem(filtros_dict={}, pagina=1, itens_por_pagina=10)
    )

    assert len(resultado.itens) == 2
    assert resultado.total == 2
    assert resultado.pagina == 1
    assert resultado.itens_por_pagina == 10
    assert resultado.total_paginas == 1


def test_deve_retornar_lista_vazia_quando_nao_ha_livros():
    visualizador = Listar(obter_uow=obter_uow_fake)
    resultado = visualizador.executar(
        ParametrosListagem(filtros_dict={}, pagina=1, itens_por_pagina=10)
    )

    assert len(resultado.itens) == 0
    assert resultado.total == 0
    assert resultado.pagina == 1
    assert resultado.itens_por_pagina == 10
    assert resultado.total_paginas == 0


def test_deve_transformar_livros_em_itens(obter_mock_livro):
    uow = obter_uow_fake()
    livro = obter_mock_livro()
    uow.repositorio_livros.adicionar(livro)

    def obter_uow_com_livro():
        return uow

    visualizador = Listar(obter_uow=obter_uow_com_livro)
    resultado = visualizador.executar(
        ParametrosListagem(filtros_dict={}, pagina=1, itens_por_pagina=10)
    )

    item = resultado.itens[0]
    assert item.id == str(livro.id)
    assert item.titulo == livro.titulo.valor
    assert item.autores == livro.autores.valor
    assert item.subtitulo == livro.subtitulo.valor
    assert item.isbn == livro.isbn.valor
    assert item.observacao == livro.observacao.valor
