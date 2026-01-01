from typing import Final

from sqlalchemy import Column, MetaData, Table
from sqlalchemy.orm import registry

from contextos_de_negocio.doador.dominio.entidades import Doador
from contextos_de_negocio.doador.dominio.objetos_de_valor import (
    DoadorId,
    EmailDoador,
    NomeDoador,
    SenhaDoador,
    TelefoneDoador,
)
from utilitarios.sqlalchemy.conversor_objeto_de_valor import (
    ConversorObjetoDeValor,
)
from utilitarios.sqlalchemy.identificador_uuid import (
    ConversorIdentificadorUuid,
)

mapper_registry: Final[registry] = registry()
metadata: Final[MetaData] = MetaData()

tabela_doadores = Table(
    "doadores",
    metadata,
    Column("id", ConversorIdentificadorUuid(DoadorId), primary_key=True),
    Column("nome", ConversorObjetoDeValor(NomeDoador, 100), nullable=False),
    Column(
        "email",
        ConversorObjetoDeValor(EmailDoador, 255),
        nullable=False,
        unique=True,
    ),
    Column("senha", ConversorObjetoDeValor(SenhaDoador, 255), nullable=False),
    Column(
        "telefone", ConversorObjetoDeValor(TelefoneDoador, 20), nullable=False
    ),
)

mapper_registry.map_imperatively(Doador, tabela_doadores)
