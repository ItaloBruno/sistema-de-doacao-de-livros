from sqlalchemy import select

from testes.utilitarios.banco_de_dados.mocks import (
    ProdutoMock,
    tabela_produtos_mock,
)
from utilitarios.sqlalchemy.ordenador import OrdenadorSQLAlchemy


def test_ordenar_por_campo_ascendente(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto C", preco=300)
    obter_mock_produto_no_banco(nome="Produto A", preco=100)
    obter_mock_produto_no_banco(nome="Produto B", preco=200)

    query = select(ProdutoMock)
    ordenador = OrdenadorSQLAlchemy(tabela_produtos_mock)

    query_ordenada = ordenador.aplicar_ordenacao(query, "nome.asc")
    resultado = uow.sessao_postgres.execute(query_ordenada).scalars().all()

    assert len(resultado) == 3
    assert resultado[0].nome == "Produto A"
    assert resultado[1].nome == "Produto B"
    assert resultado[2].nome == "Produto C"


def test_ordenar_por_campo_descendente(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto C", preco=300)
    obter_mock_produto_no_banco(nome="Produto A", preco=100)
    obter_mock_produto_no_banco(nome="Produto B", preco=200)

    query = select(ProdutoMock)
    ordenador = OrdenadorSQLAlchemy(tabela_produtos_mock)

    query_ordenada = ordenador.aplicar_ordenacao(query, "nome.desc")
    resultado = uow.sessao_postgres.execute(query_ordenada).scalars().all()

    assert len(resultado) == 3
    assert resultado[0].nome == "Produto C"
    assert resultado[1].nome == "Produto B"
    assert resultado[2].nome == "Produto A"


def test_ordenar_por_preco_ascendente(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto C", preco=300)
    obter_mock_produto_no_banco(nome="Produto A", preco=100)
    obter_mock_produto_no_banco(nome="Produto B", preco=200)

    query = select(ProdutoMock)
    ordenador = OrdenadorSQLAlchemy(tabela_produtos_mock)

    query_ordenada = ordenador.aplicar_ordenacao(query, "preco.asc")
    resultado = uow.sessao_postgres.execute(query_ordenada).scalars().all()

    assert len(resultado) == 3
    assert resultado[0].preco == 100
    assert resultado[1].preco == 200
    assert resultado[2].preco == 300


def test_ordenar_por_preco_descendente(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto C", preco=300)
    obter_mock_produto_no_banco(nome="Produto A", preco=100)
    obter_mock_produto_no_banco(nome="Produto B", preco=200)

    query = select(ProdutoMock)
    ordenador = OrdenadorSQLAlchemy(tabela_produtos_mock)

    query_ordenada = ordenador.aplicar_ordenacao(query, "preco.desc")
    resultado = uow.sessao_postgres.execute(query_ordenada).scalars().all()

    assert len(resultado) == 3
    assert resultado[0].preco == 300
    assert resultado[1].preco == 200
    assert resultado[2].preco == 100


def test_ordenar_por_multiplos_campos(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(
        nome="Produto A", categoria="Livros", preco=100
    )
    obter_mock_produto_no_banco(
        nome="Produto B", categoria="Livros", preco=200
    )
    obter_mock_produto_no_banco(
        nome="Produto C", categoria="Eletrônicos", preco=150
    )
    obter_mock_produto_no_banco(
        nome="Produto D", categoria="Eletrônicos", preco=50
    )

    query = select(ProdutoMock)
    ordenador = OrdenadorSQLAlchemy(tabela_produtos_mock)

    query_ordenada = ordenador.aplicar_ordenacao(
        query, "categoria.asc,preco.asc"
    )
    resultado = uow.sessao_postgres.execute(query_ordenada).scalars().all()

    assert len(resultado) == 4
    assert resultado[0].categoria == "Eletrônicos"
    assert resultado[0].preco == 50
    assert resultado[1].categoria == "Eletrônicos"
    assert resultado[1].preco == 150
    assert resultado[2].categoria == "Livros"
    assert resultado[2].preco == 100
    assert resultado[3].categoria == "Livros"
    assert resultado[3].preco == 200


def test_ordenar_por_multiplos_campos_direcoes_diferentes(
    uow, obter_mock_produto_no_banco
):
    obter_mock_produto_no_banco(
        nome="Produto A", categoria="Livros", preco=100
    )
    obter_mock_produto_no_banco(
        nome="Produto B", categoria="Livros", preco=200
    )
    obter_mock_produto_no_banco(
        nome="Produto C", categoria="Eletrônicos", preco=150
    )
    obter_mock_produto_no_banco(
        nome="Produto D", categoria="Eletrônicos", preco=50
    )

    query = select(ProdutoMock)
    ordenador = OrdenadorSQLAlchemy(tabela_produtos_mock)

    query_ordenada = ordenador.aplicar_ordenacao(
        query, "categoria.asc,preco.desc"
    )
    resultado = uow.sessao_postgres.execute(query_ordenada).scalars().all()

    assert len(resultado) == 4
    assert resultado[0].categoria == "Eletrônicos"
    assert resultado[0].preco == 150
    assert resultado[1].categoria == "Eletrônicos"
    assert resultado[1].preco == 50
    assert resultado[2].categoria == "Livros"
    assert resultado[2].preco == 200
    assert resultado[3].categoria == "Livros"
    assert resultado[3].preco == 100


def test_ordenar_sem_parametro(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto C", preco=300)
    obter_mock_produto_no_banco(nome="Produto A", preco=100)
    obter_mock_produto_no_banco(nome="Produto B", preco=200)

    query = select(ProdutoMock)
    ordenador = OrdenadorSQLAlchemy(tabela_produtos_mock)

    query_ordenada = ordenador.aplicar_ordenacao(query, None)
    resultado = uow.sessao_postgres.execute(query_ordenada).scalars().all()

    assert len(resultado) == 3


def test_ordenar_com_parametro_vazio(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto C", preco=300)
    obter_mock_produto_no_banco(nome="Produto A", preco=100)
    obter_mock_produto_no_banco(nome="Produto B", preco=200)

    query = select(ProdutoMock)
    ordenador = OrdenadorSQLAlchemy(tabela_produtos_mock)

    query_ordenada = ordenador.aplicar_ordenacao(query, "")
    resultado = uow.sessao_postgres.execute(query_ordenada).scalars().all()

    assert len(resultado) == 3


def test_ordenar_ignora_campo_inexistente(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto C", preco=300)
    obter_mock_produto_no_banco(nome="Produto A", preco=100)
    obter_mock_produto_no_banco(nome="Produto B", preco=200)

    query = select(ProdutoMock)
    ordenador = OrdenadorSQLAlchemy(tabela_produtos_mock)

    query_ordenada = ordenador.aplicar_ordenacao(query, "campo_invalido.asc")
    resultado = uow.sessao_postgres.execute(query_ordenada).scalars().all()

    assert len(resultado) == 3


def test_ordenar_ignora_direcao_invalida(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto C", preco=300)
    obter_mock_produto_no_banco(nome="Produto A", preco=100)
    obter_mock_produto_no_banco(nome="Produto B", preco=200)

    query = select(ProdutoMock)
    ordenador = OrdenadorSQLAlchemy(tabela_produtos_mock)

    query_ordenada = ordenador.aplicar_ordenacao(query, "nome.invalido")
    resultado = uow.sessao_postgres.execute(query_ordenada).scalars().all()

    assert len(resultado) == 3


def test_ordenar_ignora_formato_invalido(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto C", preco=300)
    obter_mock_produto_no_banco(nome="Produto A", preco=100)
    obter_mock_produto_no_banco(nome="Produto B", preco=200)

    query = select(ProdutoMock)
    ordenador = OrdenadorSQLAlchemy(tabela_produtos_mock)

    query_ordenada = ordenador.aplicar_ordenacao(query, "nome")
    resultado = uow.sessao_postgres.execute(query_ordenada).scalars().all()

    assert len(resultado) == 3


def test_ordenar_com_campos_excluidos(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto C", preco=300)
    obter_mock_produto_no_banco(nome="Produto A", preco=100)
    obter_mock_produto_no_banco(nome="Produto B", preco=200)

    query = select(ProdutoMock)
    ordenador = OrdenadorSQLAlchemy(
        tabela_produtos_mock, campos_excluidos={"preco"}
    )

    query_ordenada = ordenador.aplicar_ordenacao(query, "preco.asc")
    resultado = uow.sessao_postgres.execute(query_ordenada).scalars().all()

    assert len(resultado) == 3


def test_ordenar_com_campo_valido_e_invalido(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto C", preco=300)
    obter_mock_produto_no_banco(nome="Produto A", preco=100)
    obter_mock_produto_no_banco(nome="Produto B", preco=200)

    query = select(ProdutoMock)
    ordenador = OrdenadorSQLAlchemy(tabela_produtos_mock)

    query_ordenada = ordenador.aplicar_ordenacao(
        query, "campo_invalido.asc,nome.asc"
    )
    resultado = uow.sessao_postgres.execute(query_ordenada).scalars().all()

    assert len(resultado) == 3
    assert resultado[0].nome == "Produto A"
    assert resultado[1].nome == "Produto B"
    assert resultado[2].nome == "Produto C"


def test_construir_ordenacao_para_campo_valido_asc(uow):
    ordenador = OrdenadorSQLAlchemy(tabela_produtos_mock)

    ordenacao = ordenador.construir_ordenacao_para_campo("nome", "asc")

    assert ordenacao is not None


def test_construir_ordenacao_para_campo_valido_desc(uow):
    ordenador = OrdenadorSQLAlchemy(tabela_produtos_mock)

    ordenacao = ordenador.construir_ordenacao_para_campo("nome", "desc")

    assert ordenacao is not None


def test_construir_ordenacao_para_campo_inexistente(uow):
    ordenador = OrdenadorSQLAlchemy(tabela_produtos_mock)

    ordenacao = ordenador.construir_ordenacao_para_campo(
        "campo_invalido", "asc"
    )

    assert ordenacao is None


def test_construir_ordenacao_para_direcao_invalida(uow):
    ordenador = OrdenadorSQLAlchemy(tabela_produtos_mock)

    ordenacao = ordenador.construir_ordenacao_para_campo("nome", "invalido")

    assert ordenacao is None


def test_construir_ordenacoes_com_multiplos_campos(uow):
    ordenador = OrdenadorSQLAlchemy(tabela_produtos_mock)

    ordenacoes = ordenador.construir_ordenacoes("nome.asc,preco.desc")

    assert len(ordenacoes) == 2


def test_construir_ordenacoes_com_campo_unico(uow):
    ordenador = OrdenadorSQLAlchemy(tabela_produtos_mock)

    ordenacoes = ordenador.construir_ordenacoes("nome.asc")

    assert len(ordenacoes) == 1


def test_construir_ordenacoes_sem_parametro(uow):
    ordenador = OrdenadorSQLAlchemy(tabela_produtos_mock)

    ordenacoes = ordenador.construir_ordenacoes(None)

    assert len(ordenacoes) == 0


def test_construir_ordenacoes_com_parametro_vazio(uow):
    ordenador = OrdenadorSQLAlchemy(tabela_produtos_mock)

    ordenacoes = ordenador.construir_ordenacoes("")

    assert len(ordenacoes) == 0
