import pytest
from fastapi.security import HTTPAuthorizationCredentials

from utilitarios.fastapi.autenticacao import obter_usuario_autenticado
from utilitarios.fastapi.excecoes import TokenInvalidoOuExpirado


def test_deve_lancar_excecao_quando_token_invalido():
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer", credentials="token_invalido"
    )
    with pytest.raises(TokenInvalidoOuExpirado):
        obter_usuario_autenticado(credentials=credentials)


def test_deve_retornar_doador_id_quando_token_valido(
    obter_mock_doador, provedor_de_token
):
    doador = obter_mock_doador()
    token = provedor_de_token.gerar_token_de_acesso(doador.id)

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer", credentials=str(token)
    )
    doador_id = obter_usuario_autenticado(credentials=credentials)

    assert doador_id == doador.id
