from typing import Final

from sqlalchemy import Column, MetaData, Table
from sqlalchemy.orm import registry

from contextos_de_negocio.livros.dominio.entidades import Livro
from contextos_de_negocio.livros.dominio.objetos_de_valor import (
    AutoresLivro,
    FotoUrlLivro,
    IsbnLivro,
    LivroId,
    ObservacaoLivro,
    SubtituloLivro,
    TituloLivro,
)
from utilitarios.sqlalchemy.conversor_array_objeto_de_valor import (
    ConversorArrayObjetoDeValor,
)
from utilitarios.sqlalchemy.conversor_objeto_de_valor import (
    ConversorObjetoDeValor,
)
from utilitarios.sqlalchemy.identificador_uuid import (
    ConversorIdentificadorUuid,
)

mapper_registry: Final[registry] = registry()
metadata: Final[MetaData] = MetaData()

tabela_livros = Table(
    "livros",
    metadata,
    Column("id", ConversorIdentificadorUuid(LivroId), primary_key=True),
    Column("titulo", ConversorObjetoDeValor(TituloLivro, 255), nullable=False),
    Column(
        "subtitulo", ConversorObjetoDeValor(SubtituloLivro, 255), nullable=True
    ),
    Column(
        "autores", ConversorArrayObjetoDeValor(AutoresLivro), nullable=False
    ),
    Column("isbn", ConversorObjetoDeValor(IsbnLivro, 50), nullable=True),
    Column(
        "foto_url", ConversorObjetoDeValor(FotoUrlLivro, 500), nullable=True
    ),
    Column(
        "observacao",
        ConversorObjetoDeValor(ObservacaoLivro, 1000),
        nullable=True,
    ),
)

mapper_registry.map_imperatively(Livro, tabela_livros)
