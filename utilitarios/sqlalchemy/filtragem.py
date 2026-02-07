from sqlalchemy import and_, not_

from utilitarios.banco_de_dados.filtrador import Filtrador


class FiltragemSQLAlchemy(Filtrador):
    OPERADORES = {
        "igual": lambda campo, valor: campo == valor,
        "diferente": lambda campo, valor: campo != valor,
        "maior-que": lambda campo, valor: campo > valor,
        "maior-ou-igual": lambda campo, valor: campo >= valor,
        "menor-que": lambda campo, valor: campo < valor,
        "menor-ou-igual": lambda campo, valor: campo <= valor,
        "contem": lambda campo, valor: campo.ilike(f"%{valor}%"),
        "comeca-com": lambda campo, valor: campo.ilike(f"{valor}%"),
        "termina-com": lambda campo, valor: campo.ilike(f"%{valor}"),
        "em": lambda campo, valor: campo.in_(valor.split(",")),
        "nao-em": lambda campo, valor: not_(campo.in_(valor.split(","))),
        "e-nulo": lambda campo, _: campo.is_(None),
        "nao-e-nulo": lambda campo, _: campo.isnot(None),
    }

    def __init__(self, tabela, campos_excluidos=None):
        self.tabela = tabela
        self.campos_excluidos = campos_excluidos or set()

        self.colunas_disponiveis = {
            col.name: col
            for col in tabela.columns
            if col.name not in self.campos_excluidos
        }

    def construir_filtro_para_campo(self, coluna, operador, valor):
        if coluna not in self.colunas_disponiveis:
            return None

        if operador not in self.OPERADORES:
            return None

        return self.OPERADORES[operador](
            self.colunas_disponiveis[coluna], valor
        )

    def aplicar_filtros(self, query, parametros):
        filtros = self.construir_filtros(parametros)
        if filtros:
            return query.where(and_(*filtros))
        return query
