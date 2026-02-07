from abc import ABC, abstractmethod


class Ordenador(ABC):
    @abstractmethod
    def construir_ordenacao_para_campo(self, campo, direcao):
        pass

    @abstractmethod
    def aplicar_ordenacao(self, query, parametro_ordenacao):
        pass

    def construir_ordenacoes(self, parametro_ordenacao):
        ordenacoes = []

        if not parametro_ordenacao:
            return ordenacoes

        campos_ordenacao = parametro_ordenacao.split(",")

        for campo_ordenacao in campos_ordenacao:
            if "." not in campo_ordenacao:
                continue

            campo, direcao = campo_ordenacao.split(".", 1)

            ordenacao = self.construir_ordenacao_para_campo(campo, direcao)
            if ordenacao is not None:
                ordenacoes.append(ordenacao)

        return ordenacoes
