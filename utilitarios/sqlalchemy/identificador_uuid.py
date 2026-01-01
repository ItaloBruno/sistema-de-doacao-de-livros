from dataclasses import dataclass
from uuid import UUID, uuid4

from sqlalchemy import TypeDecorator
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


@dataclass(frozen=True, slots=True)
class IdentificadorUuid:
    valor: UUID

    def __post_init__(self):
        if not isinstance(self.valor, UUID):
            object.__setattr__(self, "valor", UUID(str(self.valor)))

    def __str__(self):
        return str(self.valor)

    def __eq__(self, other):
        if isinstance(other, IdentificadorUuid):
            return self.valor == other.valor
        return False

    def __hash__(self):
        return hash(self.valor)

    @classmethod
    def gerar(cls):
        return cls(uuid4())


class ConversorIdentificadorUuid(TypeDecorator):
    impl = PG_UUID(as_uuid=True)
    cache_ok = True

    def __init__(self, classe_identificador, *args, **kwargs):
        self.classe_identificador = classe_identificador
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if hasattr(value, "valor"):
            return value.valor
        return UUID(str(value))

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self.classe_identificador(value)
