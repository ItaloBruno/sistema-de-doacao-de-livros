from dataclasses import dataclass


@dataclass
class ParametroProjecao:
    campos: list[str]

    @classmethod
    def de_string(cls, parametro):
        if not parametro:
            return None

        campos = []
        for campo in parametro.split(","):
            campo_limpo = campo.strip()
            if campo_limpo:
                campos.append(campo_limpo)

        if not campos:
            return None

        return cls(campos=campos)

    def para_string(self):
        return ",".join(self.campos)

    def contem_campo(self, campo):
        return campo in self.campos
