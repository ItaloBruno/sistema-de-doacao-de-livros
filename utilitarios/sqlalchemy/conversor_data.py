from sqlalchemy import Date, TypeDecorator

from contextos_de_negocio.instituicao.dominio.objetos_de_valor import (
    DataFundacaoInstituicao,
)


class ConversorDataFundacao(TypeDecorator):
    impl = Date
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, DataFundacaoInstituicao):
            return value.valor
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return DataFundacaoInstituicao(value)
