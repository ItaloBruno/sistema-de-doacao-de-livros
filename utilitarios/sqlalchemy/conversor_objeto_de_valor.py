from sqlalchemy import String, TypeDecorator


class ConversorObjetoDeValor(TypeDecorator):
    impl = String
    cache_ok = True

    def __init__(
        self, classe_objeto_de_valor, tamanho_maximo=255, *args, **kwargs
    ):
        self.classe_objeto_de_valor = classe_objeto_de_valor
        super().__init__(tamanho_maximo, *args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if hasattr(value, "valor"):
            return value.valor
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self.classe_objeto_de_valor(value)
