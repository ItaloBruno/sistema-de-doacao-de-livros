from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship

from contextos_de_negocio.doacao.dominio.entidades import Doacao
from contextos_de_negocio.doacao.dominio.objetos_de_valor import (
    DoacaoId,
    LivroNaDoacao,
)
from contextos_de_negocio.doador.dominio.objetos_de_valor import DoadorId
from contextos_de_negocio.instituicao.dominio.objetos_de_valor import (
    InstituicaoId,
)
from contextos_de_negocio.livros.dominio.objetos_de_valor import LivroId
from utilitarios.sqlalchemy import mapper_registry, metadata
from utilitarios.sqlalchemy.identificador_uuid import (
    ConversorIdentificadorUuid,
)

tabela_doacoes = Table(
    "doacoes",
    metadata,
    Column("id", ConversorIdentificadorUuid(DoacaoId), primary_key=True),
    Column("doador_id", ConversorIdentificadorUuid(DoadorId), nullable=False),
    Column(
        "instituicao_id",
        ConversorIdentificadorUuid(InstituicaoId),
        nullable=False,
    ),
)

tabela_doacoes_livros = Table(
    "doacoes_livros",
    metadata,
    Column(
        "doacao_id",
        ConversorIdentificadorUuid(DoacaoId),
        ForeignKey("doacoes.id"),
        primary_key=True,
    ),
    Column(
        "livro_id",
        ConversorIdentificadorUuid(LivroId),
        ForeignKey("livros.id"),
        primary_key=True,
    ),
)

mapper_registry.map_imperatively(
    LivroNaDoacao,
    tabela_doacoes_livros,
)
mapper_registry.map_imperatively(
    Doacao,
    tabela_doacoes,
    properties={
        "livros": relationship(
            LivroNaDoacao,
            cascade="all, delete-orphan",
            primaryjoin=tabela_doacoes.c.id
            == tabela_doacoes_livros.c.doacao_id,
        )
    },
)
