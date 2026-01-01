from utilitarios.banco_de_dados.projetor import Projetor


class ProjetorSQLAlchemy(Projetor):
    def __init__(self, tabela, campos_excluidos=None):
        self.tabela = tabela
        self.campos_excluidos = campos_excluidos or set()

        self.colunas_disponiveis = {
            col.name: col
            for col in tabela.columns
            if col.name not in self.campos_excluidos
        }

    def construir_projecao_para_campo(self, campo):
        if campo not in self.colunas_disponiveis:
            return None

        return self.colunas_disponiveis[campo]

    def aplicar_projecao(self, query, parametro_projecao):
        projecoes = self.construir_projecoes(parametro_projecao)

        if not projecoes:
            return query.with_only_columns(
                *list(self.colunas_disponiveis.values())
            )

        return query.with_only_columns(*projecoes)
