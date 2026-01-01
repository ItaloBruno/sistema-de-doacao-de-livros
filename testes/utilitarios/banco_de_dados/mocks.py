from dataclasses import dataclass
from typing import Final
from uuid import uuid4

import pytest
from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry

mapper_registry: Final[registry] = registry()
metadata_produtos_mock: Final[MetaData] = MetaData()

tabela_produtos_mock = Table(
    "produtos_mock",
    metadata_produtos_mock,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("nome", String),
    Column("categoria", String),
    Column("preco", Integer),
)


@dataclass
class ProdutoMock:
    id: str
    nome: str
    categoria: str
    preco: int


mapper_registry.map_imperatively(ProdutoMock, tabela_produtos_mock)


def obter_mock_produto(**kwargs):
    return ProdutoMock(
        id=str(uuid4()),
        nome=kwargs.get("nome", "Produto Teste"),
        categoria=kwargs.get("categoria", "Categoria A"),
        preco=kwargs.get("preco", 100),
    )


@pytest.fixture
def obter_mock_produto_no_banco(uow):
    def _inserir(**kwargs):
        produto = obter_mock_produto(**kwargs)

        produto_adicionado = uow.sessao_postgres.merge(produto)
        uow.commit()

        return produto_adicionado

    return _inserir
