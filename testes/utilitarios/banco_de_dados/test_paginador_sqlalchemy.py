from sqlalchemy import select

from testes.utilitarios.banco_de_dados.mocks import (
    ProdutoMock,
    tabela_produtos_mock,
)
from utilitarios.sqlalchemy.paginador import PaginadorSQLAlchemy


def test_paginador_retorna_primeira_pagina(uow, obter_mock_produto_no_banco):
    for i in range(15):
        obter_mock_produto_no_banco(
            nome=f"Produto {i + 1}",
            categoria="Categoria A" if i % 2 == 0 else "Categoria B",
            preco=(i + 1) * 10,
        )

    query = select(ProdutoMock)
    paginador = PaginadorSQLAlchemy(
        uow.sessao_postgres, pagina=1, itens_por_pagina=5
    )

    resultado = paginador.paginar(query)

    assert len(resultado.itens) == 5
    assert resultado.total == 15
    assert resultado.pagina == 1
    assert resultado.itens_por_pagina == 5
    assert resultado.total_paginas == 3


def test_paginador_retorna_segunda_pagina(uow, obter_mock_produto_no_banco):
    for i in range(15):
        obter_mock_produto_no_banco(nome=f"Produto {i + 1}")

    query = select(ProdutoMock)
    paginador = PaginadorSQLAlchemy(
        uow.sessao_postgres, pagina=2, itens_por_pagina=5
    )

    resultado = paginador.paginar(query)

    assert len(resultado.itens) == 5
    assert resultado.total == 15
    assert resultado.pagina == 2


def test_paginador_retorna_ultima_pagina_incompleta(
    uow, obter_mock_produto_no_banco
):
    for i in range(15):
        obter_mock_produto_no_banco(nome=f"Produto {i + 1}")

    query = select(ProdutoMock)
    paginador = PaginadorSQLAlchemy(
        uow.sessao_postgres, pagina=3, itens_por_pagina=5
    )

    resultado = paginador.paginar(query)

    assert len(resultado.itens) == 5
    assert resultado.total == 15
    assert resultado.pagina == 3


def test_paginador_com_query_vazia(uow):
    query = select(ProdutoMock).where(ProdutoMock.nome == "Inexistente")
    paginador = PaginadorSQLAlchemy(
        uow.sessao_postgres, pagina=1, itens_por_pagina=10
    )

    resultado = paginador.paginar(query)

    assert len(resultado.itens) == 0
    assert resultado.total == 0
    assert resultado.total_paginas == 0


def test_paginador_com_um_item_por_pagina(uow, obter_mock_produto_no_banco):
    for i in range(15):
        obter_mock_produto_no_banco(nome=f"Produto {i + 1}")

    query = select(ProdutoMock)
    paginador = PaginadorSQLAlchemy(
        uow.sessao_postgres, pagina=1, itens_por_pagina=1
    )

    resultado = paginador.paginar(query)

    assert len(resultado.itens) == 1
    assert resultado.total == 15
    assert resultado.total_paginas == 15


def test_paginador_com_todos_itens_em_uma_pagina(
    uow, obter_mock_produto_no_banco
):
    for i in range(15):
        obter_mock_produto_no_banco(nome=f"Produto {i + 1}")

    query = select(ProdutoMock)
    paginador = PaginadorSQLAlchemy(
        uow.sessao_postgres, pagina=1, itens_por_pagina=20
    )

    resultado = paginador.paginar(query)

    assert len(resultado.itens) == 15
    assert resultado.total == 15
    assert resultado.total_paginas == 1


def test_paginador_retorna_itens_corretos_por_pagina(
    uow, obter_mock_produto_no_banco
):
    ids_criados = []
    for i in range(10):
        produto = obter_mock_produto_no_banco(
            nome=f"Produto {i + 1}", preco=(i + 1) * 10
        )
        ids_criados.append(produto.id)

    query = select(tabela_produtos_mock).order_by(tabela_produtos_mock.c.preco)
    paginador_pagina_1 = PaginadorSQLAlchemy(
        uow.sessao_postgres, pagina=1, itens_por_pagina=3
    )
    paginador_pagina_2 = PaginadorSQLAlchemy(
        uow.sessao_postgres, pagina=2, itens_por_pagina=3
    )

    resultado_pagina_1 = paginador_pagina_1.paginar(query)
    resultado_pagina_2 = paginador_pagina_2.paginar(query)

    assert len(resultado_pagina_1.itens) == 3
    assert str(resultado_pagina_1.itens[0]["id"]) == ids_criados[0]
    assert resultado_pagina_1.itens[0]["nome"] == "Produto 1"
    assert resultado_pagina_1.itens[0]["preco"] == 10
    assert str(resultado_pagina_1.itens[1]["id"]) == ids_criados[1]
    assert resultado_pagina_1.itens[1]["nome"] == "Produto 2"
    assert str(resultado_pagina_1.itens[2]["id"]) == ids_criados[2]
    assert resultado_pagina_1.itens[2]["nome"] == "Produto 3"

    assert len(resultado_pagina_2.itens) == 3
    assert str(resultado_pagina_2.itens[0]["id"]) == ids_criados[3]
    assert resultado_pagina_2.itens[0]["nome"] == "Produto 4"
    assert resultado_pagina_2.itens[0]["preco"] == 40
    assert str(resultado_pagina_2.itens[1]["id"]) == ids_criados[4]
    assert str(resultado_pagina_2.itens[2]["id"]) == ids_criados[5]
