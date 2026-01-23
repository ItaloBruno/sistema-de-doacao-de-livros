from http import HTTPStatus

from sqlalchemy import text


def test_criar_doador(cliente_api, obter_mock_doador, uow, provedor_de_hash):
    doador = obter_mock_doador()

    resposta = cliente_api.post(
        "/api/doadores",
        json={
            "nome": str(doador.nome),
            "email": str(doador.email),
            "senha": doador.senha.valor,
            "telefone": str(doador.telefone),
        },
    )

    assert resposta.status_code == HTTPStatus.CREATED

    corpo_da_resposta = resposta.json()
    assert corpo_da_resposta["nome"] == str(doador.nome)
    assert corpo_da_resposta["email"] == str(doador.email)
    assert corpo_da_resposta["telefone"] == str(doador.telefone)
    assert "id" in corpo_da_resposta
    assert "senha" not in corpo_da_resposta

    doador_id = corpo_da_resposta["id"]
    resultado = (
        uow.sessao_postgres.execute(
            text("SELECT * FROM doadores WHERE id = :id"), {"id": doador_id}
        )
        .mappings()
        .all()
    )

    assert len(resultado) == 1
    doador_no_banco = resultado[0]
    assert doador_no_banco["nome"] == str(doador.nome)
    assert doador_no_banco["email"] == str(doador.email)
    assert doador_no_banco["telefone"] == str(doador.telefone)
    assert provedor_de_hash.verificar_hash(
        doador.senha.valor, doador_no_banco["senha"]
    )


def test_atualizar_doador(
    cliente_api, obter_mock_doador_no_banco, uow, obter_token_autenticacao
):
    doador = obter_mock_doador_no_banco()
    token = obter_token_autenticacao(doador.id)

    novo_nome = "Nome Atualizado"
    novo_email = "novo.email@example.com"
    novo_telefone = "11987654321"

    resposta = cliente_api.put(
        f"/api/doadores/{doador.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome": novo_nome,
            "email": novo_email,
            "telefone": novo_telefone,
            "senha_atual": doador.senha.valor,
        },
    )

    assert resposta.status_code == HTTPStatus.OK

    corpo_da_resposta = resposta.json()
    assert corpo_da_resposta["nome"] == novo_nome
    assert corpo_da_resposta["email"] == novo_email
    assert corpo_da_resposta["telefone"] == novo_telefone
    assert corpo_da_resposta["id"] == str(doador.id)
    assert "senha" not in corpo_da_resposta

    resultado = (
        uow.sessao_postgres.execute(
            text("SELECT * FROM doadores WHERE id = :id"),
            {"id": str(doador.id.valor)},
        )
        .mappings()
        .all()
    )

    assert len(resultado) == 1
    doador_no_banco = resultado[0]
    assert doador_no_banco["nome"] == novo_nome
    assert doador_no_banco["email"] == novo_email
    assert doador_no_banco["telefone"] == novo_telefone


def test_obter_doador(
    cliente_api, obter_mock_doador_no_banco, uow, obter_token_autenticacao
):
    doador = obter_mock_doador_no_banco()
    token = obter_token_autenticacao(doador.id)

    resultado = (
        uow.sessao_postgres.execute(
            text("SELECT * FROM doadores WHERE id = :id"),
            {"id": str(doador.id.valor)},
        )
        .mappings()
        .all()
    )

    assert len(resultado) == 1
    doador_no_banco = resultado[0]

    resposta = cliente_api.get(
        f"/api/doadores/{doador.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == HTTPStatus.OK

    corpo_da_resposta = resposta.json()
    assert corpo_da_resposta["nome"] == doador_no_banco["nome"]
    assert corpo_da_resposta["email"] == doador_no_banco["email"]
    assert corpo_da_resposta["telefone"] == doador_no_banco["telefone"]
    assert corpo_da_resposta["id"] == str(doador_no_banco["id"])
    assert "senha" not in corpo_da_resposta


def test_listar_doadores_com_sucesso(cliente_api, obter_mock_doador_no_banco):
    obter_mock_doador_no_banco(nome="Ana Silva", email="ana.silva@example.com")
    obter_mock_doador_no_banco(
        nome="Bruno Costa", email="bruno.costa@example.com"
    )

    resposta = cliente_api.get("/api/doadores")

    assert resposta.status_code == HTTPStatus.OK
    dados = resposta.json()
    assert dados["total"] == 2
    assert dados["pagina"] == 1
    assert dados["itens_por_pagina"] == 10
    assert dados["total_paginas"] == 1
    assert len(dados["itens"]) == 2


def test_listar_doadores_estrutura_item(
    cliente_api, obter_mock_doador_no_banco
):
    doador = obter_mock_doador_no_banco()

    resposta = cliente_api.get("/api/doadores")

    assert resposta.status_code == HTTPStatus.OK
    dados = resposta.json()
    item = dados["itens"][0]
    assert item["id"] == str(doador.id)
    assert item["nome"] == doador.nome.valor
    assert item["email"] == doador.email.valor
    assert item["telefone"] == doador.telefone.valor
    assert "senha" not in item
