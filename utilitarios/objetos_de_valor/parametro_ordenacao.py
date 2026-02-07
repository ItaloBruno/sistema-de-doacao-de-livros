from dataclasses import dataclass


@dataclass
class ParametroOrdenacao:
    campo: str
    direcao: str

    def __post_init__(self):
        if self.direcao not in ["asc", "desc"]:
            raise ValueError("Direção deve ser 'asc' ou 'desc'")

    @classmethod
    def de_string(cls, parametro):
        if not parametro or "." not in parametro:
            return None

        campo, direcao = parametro.split(".", 1)

        if direcao not in ["asc", "desc"]:
            return None

        return cls(campo=campo, direcao=direcao)

    @classmethod
    def de_lista_strings(cls, parametros_string):
        if not parametros_string:
            return []

        campos = parametros_string.split(",")
        parametros = []

        for campo in campos:
            parametro = cls.de_string(campo)
            if parametro:
                parametros.append(parametro)

        return parametros

    def para_string(self):
        return f"{self.campo}.{self.direcao}"
