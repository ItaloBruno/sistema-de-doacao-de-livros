from http import HTTPStatus


def test_fazer_login_com_sucesso(
    cliente_api, obter_mock_doador_no_banco, provedor_de_hash
):
    senha_original = "senha123"
    senha_hash = provedor_de_hash.gerar_hash(senha_original)

    doador = obter_mock_doador_no_banco(
        email="joao@example.com",
        senha=senha_hash,
    )

    resposta = cliente_api.post(
        "/api/autenticacao/login",
        json={
            "email": str(doador.email),
            "senha": senha_original,
        },
    )

    assert resposta.status_code == HTTPStatus.OK

    corpo_da_resposta = resposta.json()
    assert corpo_da_resposta["id"] == str(doador.id)
    assert corpo_da_resposta["nome"] == str(doador.nome)
    assert corpo_da_resposta["email"] == str(doador.email)
    assert corpo_da_resposta["telefone"] == str(doador.telefone)
    assert "token_de_acesso" in corpo_da_resposta
    assert "token_de_renovacao" in corpo_da_resposta
    assert corpo_da_resposta["token_de_acesso"] != ""
    assert corpo_da_resposta["token_de_renovacao"] != ""
    assert "senha" not in corpo_da_resposta


def test_fazer_login_com_email_inexistente(cliente_api):
    resposta = cliente_api.post(
        "/api/autenticacao/login",
        json={
            "email": "naoexiste@example.com",
            "senha": "senha123",
        },
    )

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED

    corpo_da_resposta = resposta.json()
    assert corpo_da_resposta["codigo_erro"] == "A001"
    assert "Credenciais inválidas" in corpo_da_resposta["titulo"]


def test_fazer_login_com_senha_incorreta(
    cliente_api, obter_mock_doador_no_banco, provedor_de_hash
):
    senha_original = "senha123"
    senha_hash = provedor_de_hash.gerar_hash(senha_original)

    doador = obter_mock_doador_no_banco(
        email="joao@example.com",
        senha=senha_hash,
    )

    resposta = cliente_api.post(
        "/api/autenticacao/login",
        json={
            "email": str(doador.email),
            "senha": "senha_errada",
        },
    )

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED

    corpo_da_resposta = resposta.json()
    assert corpo_da_resposta["codigo_erro"] == "A001"
    assert "Credenciais inválidas" in corpo_da_resposta["titulo"]


def test_renovar_token_com_sucesso(
    cliente_api, obter_mock_doador_no_banco, provedor_de_hash
):
    senha_original = "senha123"
    senha_hash = provedor_de_hash.gerar_hash(senha_original)

    doador = obter_mock_doador_no_banco(
        email="joao@example.com",
        senha=senha_hash,
    )

    resposta_login = cliente_api.post(
        "/api/autenticacao/login",
        json={
            "email": str(doador.email),
            "senha": senha_original,
        },
    )

    assert resposta_login.status_code == HTTPStatus.OK
    token_de_renovacao = resposta_login.json()["token_de_renovacao"]

    resposta = cliente_api.post(
        "/api/autenticacao/renovar-token",
        json={
            "token_de_renovacao": token_de_renovacao,
        },
    )

    assert resposta.status_code == HTTPStatus.OK

    corpo_da_resposta = resposta.json()
    assert "token_de_acesso" in corpo_da_resposta
    assert corpo_da_resposta["token_de_acesso"] != ""


def test_renovar_token_com_token_invalido(cliente_api):
    resposta = cliente_api.post(
        "/api/autenticacao/renovar-token",
        json={
            "token_de_renovacao": "token_invalido_qualquer",
        },
    )

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED

    corpo_da_resposta = resposta.json()
    assert corpo_da_resposta["codigo_erro"] == "A002"
    assert "Token inválido" in corpo_da_resposta["titulo"]
