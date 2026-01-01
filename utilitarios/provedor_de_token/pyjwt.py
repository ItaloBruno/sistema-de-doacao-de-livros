from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt

from contextos_de_negocio.doador.dominio.objetos_de_valor import DoadorId
from utilitarios.objetos_de_valor.token import Token
from utilitarios.provedor_de_token.estrategia_de_token import EstrategiaDeToken
from utilitarios.variaveis_de_ambiente import VariaveisDeAmbiente


class EstrategiaPyJWT(EstrategiaDeToken):
    def __init__(self):
        self.chave_secreta = VariaveisDeAmbiente.CHAVE_SECRETA_JWT
        self.algoritmo = "HS256"
        self.expiracao_acesso = timedelta(minutes=30)
        self.expiracao_renovacao = timedelta(days=7)

    def gerar_token_de_acesso(self, id_doador: DoadorId) -> Token:
        agora = datetime.now(timezone.utc)
        payload = {
            "id_doador": str(id_doador),
            "tipo": "acesso",
            "iat": agora,
            "exp": agora + self.expiracao_acesso,
        }
        token_jwt = jwt.encode(
            payload, self.chave_secreta, algorithm=self.algoritmo
        )
        return Token(token_jwt)

    def gerar_token_de_renovacao(self, id_doador: DoadorId) -> Token:
        agora = datetime.now(timezone.utc)
        payload = {
            "id_doador": str(id_doador),
            "tipo": "renovacao",
            "iat": agora,
            "exp": agora + self.expiracao_renovacao,
        }
        token_jwt = jwt.encode(
            payload, self.chave_secreta, algorithm=self.algoritmo
        )
        return Token(token_jwt)

    def verificar_token_de_acesso(self, token: Token) -> DoadorId | None:
        try:
            payload = jwt.decode(
                token.valor, self.chave_secreta, algorithms=[self.algoritmo]
            )

            if payload.get("tipo") != "acesso":
                return None

            id_doador_str = payload.get("id_doador")
            if not id_doador_str:
                return None

            return DoadorId(UUID(id_doador_str))
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError):
            return None

    def renovar_token_de_acesso(
        self, token_de_renovacao: Token
    ) -> Token | None:
        try:
            payload = jwt.decode(
                token_de_renovacao.valor,
                self.chave_secreta,
                algorithms=[self.algoritmo],
            )

            if payload.get("tipo") != "renovacao":
                return None

            id_doador_str = payload.get("id_doador")
            if not id_doador_str:
                return None

            id_doador = DoadorId(UUID(id_doador_str))
            return self.gerar_token_de_acesso(id_doador)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError):
            return None
