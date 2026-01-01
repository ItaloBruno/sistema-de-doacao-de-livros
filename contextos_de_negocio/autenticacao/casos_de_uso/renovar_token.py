from contextos_de_negocio.autenticacao.casos_de_uso.dtos import (
    EntradaRenovarTokenCasoDeUso,
    SaidaRenovarToken,
)
from contextos_de_negocio.autenticacao.excecoes import TokenInvalido
from utilitarios.objetos_de_valor.token import Token
from utilitarios.provedor_de_token import ProvedorDeToken


class RenovarToken:
    def __init__(
        self,
        entrada: EntradaRenovarTokenCasoDeUso,
        provedor_de_token: ProvedorDeToken,
    ):
        self.entrada = entrada
        self.provedor_de_token = provedor_de_token

    def executar(self) -> SaidaRenovarToken:
        token_de_renovacao = Token(self.entrada.token_de_renovacao)

        novo_token_de_acesso = self.provedor_de_token.renovar_token_de_acesso(
            token_de_renovacao
        )

        if not novo_token_de_acesso:
            raise TokenInvalido()

        return SaidaRenovarToken(
            token_de_acesso=str(novo_token_de_acesso),
        )
