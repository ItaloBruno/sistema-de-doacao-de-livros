from dataclasses import dataclass

from contextos_de_negocio.livros.dominio.objetos_de_valor import LivroId
from utilitarios.sqlalchemy.identificador_uuid import IdentificadorUuid


@dataclass(frozen=True, slots=True)
class DoacaoId(IdentificadorUuid):
    pass


@dataclass
class LivroNaDoacao:
    livro_id: LivroId
