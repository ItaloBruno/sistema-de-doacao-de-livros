from fastapi import Depends
from fastapi.security import HTTPBearer

from utilitarios.fastapi.excecoes import TokenInvalidoOuExpirado
from utilitarios.objetos_de_valor.token import Token
from utilitarios.provedor_de_token import ProvedorDeToken
from utilitarios.provedor_de_token.pyjwt import EstrategiaPyJWT

security = HTTPBearer()


def obter_usuario_autenticado(credentials=Depends(security)):
    token = Token(credentials.credentials)

    provedor_de_token = ProvedorDeToken(EstrategiaPyJWT())
    doador_id = provedor_de_token.verificar_token_de_acesso(token)

    if not doador_id:
        raise TokenInvalidoOuExpirado()

    return doador_id
