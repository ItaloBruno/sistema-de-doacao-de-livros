from abc import ABC, abstractmethod


class Filtrador(ABC):
    @abstractmethod
    def construir_filtro_para_campo(self, coluna, operador, valor):
        pass

    @abstractmethod
    def aplicar_filtros(self, query, parametros):
        pass

    def construir_filtros(self, parametros):
        filtros = []

        for coluna, operador_e_valor in parametros.items():
            if not isinstance(operador_e_valor, str):
                continue

            if "." not in operador_e_valor:
                continue

            operador, valor = operador_e_valor.split(".", 1)

            filtro = self.construir_filtro_para_campo(coluna, operador, valor)
            if filtro is not None:
                filtros.append(filtro)

        return filtros
