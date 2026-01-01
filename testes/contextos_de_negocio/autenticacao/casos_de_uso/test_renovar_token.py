from uuid import UUID

import pytest

from contextos_de_negocio.autenticacao.casos_de_uso.renovar_token import (
    EntradaRenovarTokenCasoDeUso,
    RenovarToken,
)
from contextos_de_negocio.autenticacao.excecoes import TokenInvalido
from contextos_de_negocio.doador.dominio.objetos_de_valor import DoadorId
from utilitarios.objetos_de_valor.token import Token
from utilitarios.provedor_de_token import ProvedorDeToken
from utilitarios.provedor_de_token.estrategia_de_token import EstrategiaDeToken


class EstrategiaDeTokenFake(EstrategiaDeToken):
    def __init__(self):
        self.tokens_validos = {}

    def gerar_token_de_acesso(self, id_doador: DoadorId) -> Token:
        return Token(f"token_acesso_{id_doador}")

    def gerar_token_de_renovacao(self, id_doador: DoadorId) -> Token:
        token = Token(f"token_renovacao_{id_doador}")
        self.tokens_validos[token.valor] = id_doador
        return token

    def verificar_token_de_acesso(self, token: Token) -> DoadorId | None:
        if token.valor.startswith("token_acesso_"):
            id_str = token.valor.replace(
                "token_acesso_DoadorId(valor=UUID('", ""
            ).replace("'))", "")
            return DoadorId(UUID(id_str))
        return None

    def renovar_token_de_acesso(
        self, token_de_renovacao: Token
    ) -> Token | None:
        id_doador = self.tokens_validos.get(token_de_renovacao.valor)
        if id_doador:
            return self.gerar_token_de_acesso(id_doador)
        return None


def test_deve_renovar_token_com_sucesso(obter_mock_doador):
    doador = obter_mock_doador()
    estrategia_fake = EstrategiaDeTokenFake()
    provedor_de_token = ProvedorDeToken(estrategia_fake)

    token_de_renovacao = provedor_de_token.gerar_token_de_renovacao(doador.id)

    entrada = EntradaRenovarTokenCasoDeUso(
        token_de_renovacao=str(token_de_renovacao),
    )
    caso_de_uso = RenovarToken(entrada, provedor_de_token)
    saida = caso_de_uso.executar()

    assert saida.token_de_acesso is not None
    assert saida.token_de_acesso.startswith("token_acesso_")


def test_deve_lancar_excecao_quando_token_invalido():
    estrategia_fake = EstrategiaDeTokenFake()
    provedor_de_token = ProvedorDeToken(estrategia_fake)

    entrada = EntradaRenovarTokenCasoDeUso(
        token_de_renovacao="token_invalido",
    )
    caso_de_uso = RenovarToken(entrada, provedor_de_token)

    with pytest.raises(TokenInvalido):
        caso_de_uso.executar()
