from sqlalchemy import TypeDecorator
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.types import String


class ConversorArrayObjetoDeValor(TypeDecorator):
    impl = ARRAY
    cache_ok = True

    def __init__(self, classe_objeto_de_valor, *args, **kwargs):
        self.classe_objeto_de_valor = classe_objeto_de_valor
        super().__init__(String, *args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if hasattr(value, "valor"):
            return value.valor
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self.classe_objeto_de_valor(value)
