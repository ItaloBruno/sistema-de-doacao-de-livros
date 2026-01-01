from dataclasses import dataclass

from utilitarios.objetos_de_valor.email import Email
from utilitarios.objetos_de_valor.nome import Nome
from utilitarios.objetos_de_valor.senha_hash import SenhaHash
from utilitarios.objetos_de_valor.telefone import Telefone
from utilitarios.sqlalchemy.identificador_uuid import IdentificadorUuid


@dataclass(frozen=True, slots=True)
class NomeDoador(Nome):
    pass


@dataclass(frozen=True, slots=True)
class EmailDoador(Email):
    pass


@dataclass(frozen=True, slots=True)
class TelefoneDoador(Telefone):
    pass


@dataclass(frozen=True, slots=True)
class SenhaDoador(SenhaHash):
    pass


@dataclass(frozen=True, slots=True)
class DoadorId(IdentificadorUuid):
    pass
