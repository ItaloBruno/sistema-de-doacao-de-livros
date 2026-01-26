from http import HTTPStatus

from sqlalchemy import text


def test_criar_doacao_com_sucesso(
    cliente_api,
    uow,
    obter_token_autenticacao,
    obter_mock_doador_no_banco,
    obter_mock_instituicao_no_banco,
    obter_mock_livro_no_banco,
):
    doador = obter_mock_doador_no_banco()
    instituicao = obter_mock_instituicao_no_banco()
    livro_1 = obter_mock_livro_no_banco()
    livro_2 = obter_mock_livro_no_banco()

    token = obter_token_autenticacao(str(doador.id))

    resposta = cliente_api.post(
        "/api/doacoes",
        json={
            "instituicao_id": str(instituicao.id),
            "livros_ids": [str(livro_1.id), str(livro_2.id)],
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == HTTPStatus.CREATED

    corpo_da_resposta = resposta.json()
    assert corpo_da_resposta["doador_id"] == str(doador.id)
    assert corpo_da_resposta["instituicao_id"] == str(instituicao.id)
    assert len(corpo_da_resposta["livros_ids"]) == 2
    assert str(livro_1.id) in corpo_da_resposta["livros_ids"]
    assert str(livro_2.id) in corpo_da_resposta["livros_ids"]
    assert "id" in corpo_da_resposta

    doacao_id = corpo_da_resposta["id"]
    resultado = (
        uow.sessao_postgres.execute(
            text("SELECT * FROM doacoes WHERE id = :id"), {"id": doacao_id}
        )
        .mappings()
        .all()
    )

    assert len(resultado) == 1
    doacao_no_banco = resultado[0]
    assert str(doacao_no_banco["doador_id"]) == str(doador.id.valor)
    assert str(doacao_no_banco["instituicao_id"]) == str(instituicao.id.valor)

    resultado_livros = (
        uow.sessao_postgres.execute(
            text(
                """
                SELECT livro_id
                FROM doacoes_livros
                WHERE doacao_id = :doacao_id
                """
            ),
            {"doacao_id": doacao_id},
        )
        .mappings()
        .all()
    )

    assert len(resultado_livros) == 2
    livros_ids_no_banco = [linha["livro_id"] for linha in resultado_livros]
    assert str(livro_1.id.valor) in [
        str(livro_id) for livro_id in livros_ids_no_banco
    ]
    assert str(livro_2.id.valor) in [
        str(livro_id) for livro_id in livros_ids_no_banco
    ]
