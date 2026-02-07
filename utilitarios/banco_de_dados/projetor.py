from abc import ABC, abstractmethod


class Projetor(ABC):
    @abstractmethod
    def construir_projecao_para_campo(self, campo):
        pass

    @abstractmethod
    def aplicar_projecao(self, query, parametro_projecao):
        pass

    def construir_projecoes(self, parametro_projecao):
        if not parametro_projecao:
            return []

        projecoes = []
        campos = parametro_projecao.split(",")

        for campo in campos:
            campo_limpo = campo.strip()
            if not campo_limpo:
                continue

            projecao = self.construir_projecao_para_campo(campo_limpo)
            if projecao is not None:
                projecoes.append(projecao)

        return projecoes
