from typing import Final

from fastapi import APIRouter

from contextos_de_negocio.autenticacao.casos_de_uso.fazer_login import (
    EntradaFazerLoginCasoDeUso,
    FazerLogin,
)
from contextos_de_negocio.autenticacao.casos_de_uso.renovar_token import (
    EntradaRenovarTokenCasoDeUso,
    RenovarToken,
)
from contextos_de_negocio.autenticacao.pontos_de_entrada.esquemas import (
    EntradaLogin,
    EntradaRenovarToken,
    RespostaLogin,
    RespostaRenovarToken,
)
from utilitarios.provedor_de_hash import ProvedorDeHash
from utilitarios.provedor_de_hash.argon2 import EstrategiaArgon2
from utilitarios.provedor_de_token import ProvedorDeToken
from utilitarios.provedor_de_token.pyjwt import EstrategiaPyJWT
from utilitarios.unidade_de_trabalho import unidade_de_trabalho

api_autenticacao: Final[APIRouter] = APIRouter(tags=["Autenticação"])


@api_autenticacao.post("/autenticacao/login", response_model=RespostaLogin)
def fazer_login(corpo_da_requisicao: EntradaLogin):
    entrada = EntradaFazerLoginCasoDeUso(
        email=str(corpo_da_requisicao.email),
        senha=corpo_da_requisicao.senha,
    )

    caso_de_uso = FazerLogin(
        entrada=entrada,
        obter_uow=unidade_de_trabalho,
        provedor_de_hash=ProvedorDeHash(EstrategiaArgon2()),
        provedor_de_token=ProvedorDeToken(EstrategiaPyJWT()),
    )
    saida = caso_de_uso.executar()

    return RespostaLogin(
        id=saida.id,
        nome=saida.nome,
        email=saida.email,
        telefone=saida.telefone,
        token_de_acesso=saida.token_de_acesso,
        token_de_renovacao=saida.token_de_renovacao,
    )


@api_autenticacao.post(
    "/autenticacao/renovar-token", response_model=RespostaRenovarToken
)
def renovar_token(corpo_da_requisicao: EntradaRenovarToken):
    entrada = EntradaRenovarTokenCasoDeUso(
        token_de_renovacao=corpo_da_requisicao.token_de_renovacao,
    )

    caso_de_uso = RenovarToken(
        entrada=entrada,
        provedor_de_token=ProvedorDeToken(EstrategiaPyJWT()),
    )
    saida = caso_de_uso.executar()

    return RespostaRenovarToken(
        token_de_acesso=saida.token_de_acesso,
    )
