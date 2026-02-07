from contextos_de_negocio.doador.dominio.objetos_de_valor import DoadorId
from utilitarios.objetos_de_valor.token import Token
from utilitarios.provedor_de_token.estrategia_de_token import EstrategiaDeToken


class ProvedorDeToken:
    def __init__(self, estrategia: EstrategiaDeToken):
        self.estrategia = estrategia

    def gerar_token_de_acesso(self, id_doador: DoadorId) -> Token:
        return self.estrategia.gerar_token_de_acesso(id_doador)

    def gerar_token_de_renovacao(self, id_doador: DoadorId) -> Token:
        return self.estrategia.gerar_token_de_renovacao(id_doador)

    def verificar_token_de_acesso(self, token: Token) -> DoadorId | None:
        return self.estrategia.verificar_token_de_acesso(token)

    def renovar_token_de_acesso(
        self, token_de_renovacao: Token
    ) -> Token | None:
        return self.estrategia.renovar_token_de_acesso(token_de_renovacao)
