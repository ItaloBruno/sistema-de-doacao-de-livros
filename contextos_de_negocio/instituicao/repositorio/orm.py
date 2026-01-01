from typing import Final

from sqlalchemy import Column, MetaData, Table
from sqlalchemy.orm import registry

from contextos_de_negocio.instituicao.dominio.entidades import Instituicao
from contextos_de_negocio.instituicao.dominio.objetos_de_valor import (
    DescricaoInstituicao,
    EmailInstituicao,
    EnderecoInstituicao,
    FotoInstituicao,
    InstituicaoId,
    NomeInstituicao,
    SenhaInstituicao,
    SiteInstituicao,
    TelefoneInstituicao,
)
from utilitarios.sqlalchemy.conversor_data import ConversorDataFundacao
from utilitarios.sqlalchemy.conversor_objeto_de_valor import (
    ConversorObjetoDeValor,
)
from utilitarios.sqlalchemy.identificador_uuid import (
    ConversorIdentificadorUuid,
)

mapper_registry: Final[registry] = registry()
metadata: Final[MetaData] = MetaData()

tabela_instituicoes = Table(
    "instituicoes",
    metadata,
    Column("id", ConversorIdentificadorUuid(InstituicaoId), primary_key=True),
    Column(
        "nome", ConversorObjetoDeValor(NomeInstituicao, 100), nullable=False
    ),
    Column(
        "email",
        ConversorObjetoDeValor(EmailInstituicao, 255),
        nullable=False,
        unique=True,
    ),
    Column(
        "senha", ConversorObjetoDeValor(SenhaInstituicao, 255), nullable=False
    ),
    Column(
        "telefone",
        ConversorObjetoDeValor(TelefoneInstituicao, 20),
        nullable=False,
    ),
    Column(
        "foto", ConversorObjetoDeValor(FotoInstituicao, 500), nullable=True
    ),
    Column(
        "descricao",
        ConversorObjetoDeValor(DescricaoInstituicao, 1000),
        nullable=False,
    ),
    Column("data_fundacao", ConversorDataFundacao(), nullable=False),
    Column(
        "endereco",
        ConversorObjetoDeValor(EnderecoInstituicao, 500),
        nullable=False,
    ),
    Column(
        "site", ConversorObjetoDeValor(SiteInstituicao, 255), nullable=True
    ),
)

mapper_registry.map_imperatively(Instituicao, tabela_instituicoes)
