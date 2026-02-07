from sqlalchemy import asc, desc

from utilitarios.banco_de_dados.ordenador import Ordenador


class OrdenadorSQLAlchemy(Ordenador):
    DIRECOES = {
        "asc": asc,
        "desc": desc,
    }

    def __init__(self, tabela, campos_excluidos=None):
        self.tabela = tabela
        self.campos_excluidos = campos_excluidos or set()

        self.colunas_disponiveis = {
            col.name: col
            for col in tabela.columns
            if col.name not in self.campos_excluidos
        }

    def construir_ordenacao_para_campo(self, campo, direcao):
        if campo not in self.colunas_disponiveis:
            return None

        if direcao not in self.DIRECOES:
            return None

        return self.DIRECOES[direcao](self.colunas_disponiveis[campo])

    def aplicar_ordenacao(self, query, parametro_ordenacao):
        ordenacoes = self.construir_ordenacoes(parametro_ordenacao)
        if ordenacoes:
            return query.order_by(*ordenacoes)
        return query
