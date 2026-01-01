from sqlalchemy import select

from testes.utilitarios.banco_de_dados.mocks import (
    ProdutoMock,
    tabela_produtos_mock,
)
from utilitarios.sqlalchemy.filtragem import FiltragemSQLAlchemy


def test_filtragem_operador_igual(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto A", categoria="Livros", preco=50)
    obter_mock_produto_no_banco(
        nome="Produto B", categoria="Eletrônicos", preco=100
    )
    obter_mock_produto_no_banco(nome="Produto C", categoria="Livros", preco=75)
    obter_mock_produto_no_banco(
        nome="Item Especial", categoria="Diversos", preco=50
    )

    query = select(ProdutoMock)
    filtragem = FiltragemSQLAlchemy(tabela_produtos_mock)

    query_filtrada = filtragem.aplicar_filtros(
        query, {"categoria": "igual.Livros"}
    )
    resultado = uow.sessao_postgres.execute(query_filtrada).scalars().all()

    assert len(resultado) == 2
    assert all(item.categoria == "Livros" for item in resultado)


def test_filtragem_operador_diferente(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto A", categoria="Livros", preco=50)
    obter_mock_produto_no_banco(
        nome="Produto B", categoria="Eletrônicos", preco=100
    )
    obter_mock_produto_no_banco(nome="Produto C", categoria="Livros", preco=75)
    obter_mock_produto_no_banco(
        nome="Item Especial", categoria="Diversos", preco=50
    )

    query = select(ProdutoMock)
    filtragem = FiltragemSQLAlchemy(tabela_produtos_mock)

    query_filtrada = filtragem.aplicar_filtros(
        query, {"categoria": "diferente.Livros"}
    )
    resultado = uow.sessao_postgres.execute(query_filtrada).scalars().all()

    assert len(resultado) == 2
    assert all(item.categoria != "Livros" for item in resultado)


def test_filtragem_operador_maior_que(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto A", categoria="Livros", preco=50)
    obter_mock_produto_no_banco(
        nome="Produto B", categoria="Eletrônicos", preco=100
    )
    obter_mock_produto_no_banco(nome="Produto C", categoria="Livros", preco=75)
    obter_mock_produto_no_banco(
        nome="Item Especial", categoria="Diversos", preco=50
    )

    query = select(ProdutoMock)
    filtragem = FiltragemSQLAlchemy(tabela_produtos_mock)

    query_filtrada = filtragem.aplicar_filtros(
        query, {"preco": "maior-que.50"}
    )
    resultado = uow.sessao_postgres.execute(query_filtrada).scalars().all()

    assert len(resultado) == 2
    assert all(item.preco > 50 for item in resultado)


def test_filtragem_operador_maior_ou_igual(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto A", categoria="Livros", preco=50)
    obter_mock_produto_no_banco(
        nome="Produto B", categoria="Eletrônicos", preco=100
    )
    obter_mock_produto_no_banco(nome="Produto C", categoria="Livros", preco=75)
    obter_mock_produto_no_banco(
        nome="Item Especial", categoria="Diversos", preco=50
    )

    query = select(ProdutoMock)
    filtragem = FiltragemSQLAlchemy(tabela_produtos_mock)

    query_filtrada = filtragem.aplicar_filtros(
        query, {"preco": "maior-ou-igual.50"}
    )
    resultado = uow.sessao_postgres.execute(query_filtrada).scalars().all()

    assert len(resultado) == 4


def test_filtragem_operador_menor_que(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto A", categoria="Livros", preco=50)
    obter_mock_produto_no_banco(
        nome="Produto B", categoria="Eletrônicos", preco=100
    )
    obter_mock_produto_no_banco(nome="Produto C", categoria="Livros", preco=75)
    obter_mock_produto_no_banco(
        nome="Item Especial", categoria="Diversos", preco=50
    )

    query = select(ProdutoMock)
    filtragem = FiltragemSQLAlchemy(tabela_produtos_mock)

    query_filtrada = filtragem.aplicar_filtros(
        query, {"preco": "menor-que.75"}
    )
    resultado = uow.sessao_postgres.execute(query_filtrada).scalars().all()

    assert len(resultado) == 2
    assert all(item.preco < 75 for item in resultado)


def test_filtragem_operador_menor_ou_igual(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto A", categoria="Livros", preco=50)
    obter_mock_produto_no_banco(
        nome="Produto B", categoria="Eletrônicos", preco=100
    )
    obter_mock_produto_no_banco(nome="Produto C", categoria="Livros", preco=75)
    obter_mock_produto_no_banco(
        nome="Item Especial", categoria="Diversos", preco=50
    )

    query = select(ProdutoMock)
    filtragem = FiltragemSQLAlchemy(tabela_produtos_mock)

    query_filtrada = filtragem.aplicar_filtros(
        query, {"preco": "menor-ou-igual.75"}
    )
    resultado = uow.sessao_postgres.execute(query_filtrada).scalars().all()

    assert len(resultado) == 3


def test_filtragem_operador_contem(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto A", categoria="Livros", preco=50)
    obter_mock_produto_no_banco(
        nome="Produto B", categoria="Eletrônicos", preco=100
    )
    obter_mock_produto_no_banco(nome="Produto C", categoria="Livros", preco=75)
    obter_mock_produto_no_banco(
        nome="Item Especial", categoria="Diversos", preco=50
    )

    query = select(ProdutoMock)
    filtragem = FiltragemSQLAlchemy(tabela_produtos_mock)

    query_filtrada = filtragem.aplicar_filtros(
        query, {"nome": "contem.Produto"}
    )
    resultado = uow.sessao_postgres.execute(query_filtrada).scalars().all()

    assert len(resultado) == 3
    assert all("Produto" in item.nome for item in resultado)


def test_filtragem_operador_comeca_com(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto A", categoria="Livros", preco=50)
    obter_mock_produto_no_banco(
        nome="Produto B", categoria="Eletrônicos", preco=100
    )
    obter_mock_produto_no_banco(nome="Produto C", categoria="Livros", preco=75)
    obter_mock_produto_no_banco(
        nome="Item Especial", categoria="Diversos", preco=50
    )

    query = select(ProdutoMock)
    filtragem = FiltragemSQLAlchemy(tabela_produtos_mock)

    query_filtrada = filtragem.aplicar_filtros(
        query, {"nome": "comeca-com.Produto"}
    )
    resultado = uow.sessao_postgres.execute(query_filtrada).scalars().all()

    assert len(resultado) == 3
    assert all(item.nome.startswith("Produto") for item in resultado)


def test_filtragem_operador_termina_com(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto A", categoria="Livros", preco=50)
    obter_mock_produto_no_banco(
        nome="Produto B", categoria="Eletrônicos", preco=100
    )
    obter_mock_produto_no_banco(nome="Produto C", categoria="Livros", preco=75)
    obter_mock_produto_no_banco(
        nome="Item Especial", categoria="Diversos", preco=50
    )

    query = select(ProdutoMock)
    filtragem = FiltragemSQLAlchemy(tabela_produtos_mock)

    query_filtrada = filtragem.aplicar_filtros(
        query, {"nome": "termina-com.A"}
    )
    resultado = uow.sessao_postgres.execute(query_filtrada).scalars().all()

    assert len(resultado) == 1
    assert resultado[0].nome == "Produto A"


def test_filtragem_multiplos_filtros(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto A", categoria="Livros", preco=50)
    obter_mock_produto_no_banco(
        nome="Produto B", categoria="Eletrônicos", preco=100
    )
    obter_mock_produto_no_banco(nome="Produto C", categoria="Livros", preco=75)
    obter_mock_produto_no_banco(
        nome="Item Especial", categoria="Diversos", preco=50
    )

    query = select(ProdutoMock)
    filtragem = FiltragemSQLAlchemy(tabela_produtos_mock)

    query_filtrada = filtragem.aplicar_filtros(
        query, {"categoria": "igual.Livros", "preco": "maior-que.50"}
    )
    resultado = uow.sessao_postgres.execute(query_filtrada).scalars().all()

    assert len(resultado) == 1
    assert resultado[0].nome == "Produto C"


def test_filtragem_sem_filtros(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto A", categoria="Livros", preco=50)
    obter_mock_produto_no_banco(
        nome="Produto B", categoria="Eletrônicos", preco=100
    )
    obter_mock_produto_no_banco(nome="Produto C", categoria="Livros", preco=75)
    obter_mock_produto_no_banco(
        nome="Item Especial", categoria="Diversos", preco=50
    )

    query = select(ProdutoMock)
    filtragem = FiltragemSQLAlchemy(tabela_produtos_mock)

    query_filtrada = filtragem.aplicar_filtros(query, {})
    resultado = uow.sessao_postgres.execute(query_filtrada).scalars().all()

    assert len(resultado) == 4


def test_filtragem_ignora_campo_inexistente(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto A", categoria="Livros", preco=50)
    obter_mock_produto_no_banco(
        nome="Produto B", categoria="Eletrônicos", preco=100
    )
    obter_mock_produto_no_banco(nome="Produto C", categoria="Livros", preco=75)
    obter_mock_produto_no_banco(
        nome="Item Especial", categoria="Diversos", preco=50
    )

    query = select(ProdutoMock)
    filtragem = FiltragemSQLAlchemy(tabela_produtos_mock)

    query_filtrada = filtragem.aplicar_filtros(
        query, {"campo_invalido": "igual.valor"}
    )
    resultado = uow.sessao_postgres.execute(query_filtrada).scalars().all()

    assert len(resultado) == 4


def test_filtragem_ignora_operador_invalido(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto A", categoria="Livros", preco=50)
    obter_mock_produto_no_banco(
        nome="Produto B", categoria="Eletrônicos", preco=100
    )
    obter_mock_produto_no_banco(nome="Produto C", categoria="Livros", preco=75)
    obter_mock_produto_no_banco(
        nome="Item Especial", categoria="Diversos", preco=50
    )

    query = select(ProdutoMock)
    filtragem = FiltragemSQLAlchemy(tabela_produtos_mock)

    query_filtrada = filtragem.aplicar_filtros(
        query, {"nome": "operador-invalido.valor"}
    )
    resultado = uow.sessao_postgres.execute(query_filtrada).scalars().all()

    assert len(resultado) == 4


def test_filtragem_ignora_formato_invalido(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto A", categoria="Livros", preco=50)
    obter_mock_produto_no_banco(
        nome="Produto B", categoria="Eletrônicos", preco=100
    )
    obter_mock_produto_no_banco(nome="Produto C", categoria="Livros", preco=75)
    obter_mock_produto_no_banco(
        nome="Item Especial", categoria="Diversos", preco=50
    )

    query = select(ProdutoMock)
    filtragem = FiltragemSQLAlchemy(tabela_produtos_mock)

    query_filtrada = filtragem.aplicar_filtros(query, {"nome": "sem_ponto"})
    resultado = uow.sessao_postgres.execute(query_filtrada).scalars().all()

    assert len(resultado) == 4


def test_filtragem_com_campos_excluidos(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(nome="Produto A", categoria="Livros", preco=50)
    obter_mock_produto_no_banco(
        nome="Produto B", categoria="Eletrônicos", preco=100
    )
    obter_mock_produto_no_banco(nome="Produto C", categoria="Livros", preco=75)
    obter_mock_produto_no_banco(
        nome="Item Especial", categoria="Diversos", preco=50
    )

    query = select(tabela_produtos_mock)
    filtragem = FiltragemSQLAlchemy(
        tabela_produtos_mock, campos_excluidos={"preco"}
    )

    query_filtrada = filtragem.aplicar_filtros(
        query, {"preco": "maior-que.50"}
    )
    resultado = uow.sessao_postgres.execute(query_filtrada).scalars().all()

    assert len(resultado) == 4
