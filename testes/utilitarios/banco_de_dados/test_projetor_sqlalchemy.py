from sqlalchemy import select

from testes.utilitarios.banco_de_dados.mocks import (
    ProdutoMock,
    tabela_produtos_mock,
)
from utilitarios.sqlalchemy.projetor import ProjetorSQLAlchemy


def test_projetar_campo_unico(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(
        nome="Produto A", categoria="Livros", preco=100
    )

    query = select(ProdutoMock)
    projetor = ProjetorSQLAlchemy(tabela_produtos_mock)

    query_projetada = projetor.aplicar_projecao(query, "nome")
    resultado = uow.sessao_postgres.execute(query_projetada).mappings().all()

    assert len(resultado) == 1
    assert "nome" in resultado[0]
    assert resultado[0]["nome"] == "Produto A"
    assert "categoria" not in resultado[0]
    assert "preco" not in resultado[0]


def test_projetar_multiplos_campos(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(
        nome="Produto A", categoria="Livros", preco=100
    )

    query = select(ProdutoMock)
    projetor = ProjetorSQLAlchemy(tabela_produtos_mock)

    query_projetada = projetor.aplicar_projecao(query, "nome,preco")
    resultado = uow.sessao_postgres.execute(query_projetada).mappings().all()

    assert len(resultado) == 1
    assert "nome" in resultado[0]
    assert "preco" in resultado[0]
    assert resultado[0]["nome"] == "Produto A"
    assert resultado[0]["preco"] == 100
    assert "categoria" not in resultado[0]


def test_projetar_todos_campos_sem_parametro(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(
        nome="Produto A", categoria="Livros", preco=100
    )

    query = select(ProdutoMock)
    projetor = ProjetorSQLAlchemy(tabela_produtos_mock)

    query_projetada = projetor.aplicar_projecao(query, None)
    resultado = uow.sessao_postgres.execute(query_projetada).mappings().all()

    assert len(resultado) == 1
    assert "id" in resultado[0]
    assert "nome" in resultado[0]
    assert "categoria" in resultado[0]
    assert "preco" in resultado[0]


def test_projetar_todos_campos_com_parametro_vazio(
    uow, obter_mock_produto_no_banco
):
    obter_mock_produto_no_banco(
        nome="Produto A", categoria="Livros", preco=100
    )

    query = select(ProdutoMock)
    projetor = ProjetorSQLAlchemy(tabela_produtos_mock)

    query_projetada = projetor.aplicar_projecao(query, "")
    resultado = uow.sessao_postgres.execute(query_projetada).mappings().all()

    assert len(resultado) == 1
    assert "id" in resultado[0]
    assert "nome" in resultado[0]
    assert "categoria" in resultado[0]
    assert "preco" in resultado[0]


def test_projetar_com_espacos(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(
        nome="Produto A", categoria="Livros", preco=100
    )

    query = select(ProdutoMock)
    projetor = ProjetorSQLAlchemy(tabela_produtos_mock)

    query_projetada = projetor.aplicar_projecao(query, "nome, preco")
    resultado = uow.sessao_postgres.execute(query_projetada).mappings().all()

    assert len(resultado) == 1
    assert "nome" in resultado[0]
    assert "preco" in resultado[0]
    assert "categoria" not in resultado[0]


def test_projetar_ignora_campo_inexistente(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(
        nome="Produto A", categoria="Livros", preco=100
    )

    query = select(ProdutoMock)
    projetor = ProjetorSQLAlchemy(tabela_produtos_mock)

    query_projetada = projetor.aplicar_projecao(query, "nome,campo_invalido")
    resultado = uow.sessao_postgres.execute(query_projetada).mappings().all()

    assert len(resultado) == 1
    assert "nome" in resultado[0]
    assert "campo_invalido" not in resultado[0]


def test_projetar_apenas_campos_invalidos_retorna_todos(
    uow, obter_mock_produto_no_banco
):
    obter_mock_produto_no_banco(
        nome="Produto A", categoria="Livros", preco=100
    )

    query = select(ProdutoMock)
    projetor = ProjetorSQLAlchemy(tabela_produtos_mock)

    query_projetada = projetor.aplicar_projecao(
        query, "campo_invalido,outro_invalido"
    )
    resultado = uow.sessao_postgres.execute(query_projetada).mappings().all()

    assert len(resultado) == 1
    assert "id" in resultado[0]
    assert "nome" in resultado[0]
    assert "categoria" in resultado[0]
    assert "preco" in resultado[0]


def test_projetar_com_campos_excluidos(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(
        nome="Produto A", categoria="Livros", preco=100
    )

    query = select(ProdutoMock)
    projetor = ProjetorSQLAlchemy(
        tabela_produtos_mock, campos_excluidos={"preco"}
    )

    query_projetada = projetor.aplicar_projecao(query, "nome,preco")
    resultado = uow.sessao_postgres.execute(query_projetada).mappings().all()

    assert len(resultado) == 1
    assert "nome" in resultado[0]
    assert "preco" not in resultado[0]


def test_projetar_sem_parametro_com_campos_excluidos(
    uow, obter_mock_produto_no_banco
):
    obter_mock_produto_no_banco(
        nome="Produto A", categoria="Livros", preco=100
    )

    query = select(ProdutoMock)
    projetor = ProjetorSQLAlchemy(
        tabela_produtos_mock, campos_excluidos={"preco"}
    )

    query_projetada = projetor.aplicar_projecao(query, None)
    resultado = uow.sessao_postgres.execute(query_projetada).mappings().all()

    assert len(resultado) == 1
    assert "id" in resultado[0]
    assert "nome" in resultado[0]
    assert "categoria" in resultado[0]
    assert "preco" not in resultado[0]


def test_projetar_multiplos_registros(uow, obter_mock_produto_no_banco):
    obter_mock_produto_no_banco(
        nome="Produto A", categoria="Livros", preco=100
    )
    obter_mock_produto_no_banco(
        nome="Produto B", categoria="Eletrônicos", preco=200
    )
    obter_mock_produto_no_banco(
        nome="Produto C", categoria="Livros", preco=150
    )

    query = select(ProdutoMock)
    projetor = ProjetorSQLAlchemy(tabela_produtos_mock)

    query_projetada = projetor.aplicar_projecao(query, "nome,categoria")
    resultado = uow.sessao_postgres.execute(query_projetada).mappings().all()

    assert len(resultado) == 3
    for item in resultado:
        assert "nome" in item
        assert "categoria" in item
        assert "preco" not in item


def test_construir_projecao_para_campo_valido(uow):
    projetor = ProjetorSQLAlchemy(tabela_produtos_mock)

    projecao = projetor.construir_projecao_para_campo("nome")

    assert projecao is not None


def test_construir_projecao_para_campo_inexistente(uow):
    projetor = ProjetorSQLAlchemy(tabela_produtos_mock)

    projecao = projetor.construir_projecao_para_campo("campo_invalido")

    assert projecao is None


def test_construir_projecoes_com_multiplos_campos(uow):
    projetor = ProjetorSQLAlchemy(tabela_produtos_mock)

    projecoes = projetor.construir_projecoes("nome,preco,categoria")

    assert len(projecoes) == 3


def test_construir_projecoes_com_campo_unico(uow):
    projetor = ProjetorSQLAlchemy(tabela_produtos_mock)

    projecoes = projetor.construir_projecoes("nome")

    assert len(projecoes) == 1


def test_construir_projecoes_sem_parametro(uow):
    projetor = ProjetorSQLAlchemy(tabela_produtos_mock)

    projecoes = projetor.construir_projecoes(None)

    assert len(projecoes) == 0


def test_construir_projecoes_com_parametro_vazio(uow):
    projetor = ProjetorSQLAlchemy(tabela_produtos_mock)

    projecoes = projetor.construir_projecoes("")

    assert len(projecoes) == 0


def test_construir_projecoes_ignora_campos_invalidos(uow):
    projetor = ProjetorSQLAlchemy(tabela_produtos_mock)

    projecoes = projetor.construir_projecoes("nome,campo_invalido,preco")

    assert len(projecoes) == 2
