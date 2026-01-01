import json
from http import HTTPStatus
from io import BytesIO

from sqlalchemy import text

from contextos_de_negocio.livros.dominio.objetos_de_valor import LivroId


def test_criar_livro_sem_foto(cliente_api, obter_mock_livro, uow):
    livro = obter_mock_livro()

    resposta = cliente_api.post(
        "/api/livros",
        data={
            "titulo": livro.titulo.valor,
            "autores": json.dumps(livro.autores.valor),
            "subtitulo": livro.subtitulo.valor,
            "isbn": livro.isbn.valor,
            "observacao": livro.observacao.valor,
        },
    )

    assert resposta.status_code == HTTPStatus.CREATED

    corpo_da_resposta = resposta.json()
    assert corpo_da_resposta["titulo"] == livro.titulo.valor
    assert corpo_da_resposta["autores"] == livro.autores.valor
    assert corpo_da_resposta["subtitulo"] == livro.subtitulo.valor
    assert corpo_da_resposta["isbn"] == livro.isbn.valor
    assert corpo_da_resposta["observacao"] == livro.observacao.valor
    assert "id" in corpo_da_resposta
    assert corpo_da_resposta["foto"] is None

    livro_id = corpo_da_resposta["id"]
    resultado = (
        uow.sessao_postgres.execute(
            text("SELECT * FROM livros WHERE id = :id"), {"id": livro_id}
        )
        .mappings()
        .all()
    )

    assert len(resultado) == 1
    livro_no_banco = resultado[0]
    assert livro_no_banco["titulo"] == livro.titulo.valor
    assert livro_no_banco["autores"] == livro.autores.valor
    assert livro_no_banco["subtitulo"] == livro.subtitulo.valor
    assert livro_no_banco["isbn"] == livro.isbn.valor
    assert livro_no_banco["observacao"] == livro.observacao.valor


def test_criar_livro_com_foto(cliente_api, obter_mock_livro, uow):
    livro = obter_mock_livro()
    foto_bytes = b"fake image content"
    foto_arquivo = BytesIO(foto_bytes)

    resposta = cliente_api.post(
        "/api/livros",
        data={
            "titulo": livro.titulo.valor,
            "autores": json.dumps(livro.autores.valor),
            "subtitulo": livro.subtitulo.valor,
            "isbn": livro.isbn.valor,
            "observacao": livro.observacao.valor,
        },
        files={"foto": ("capa.jpg", foto_arquivo, "image/jpeg")},
    )

    assert resposta.status_code == HTTPStatus.CREATED

    corpo_da_resposta = resposta.json()
    assert corpo_da_resposta["titulo"] == livro.titulo.valor
    assert corpo_da_resposta["autores"] == livro.autores.valor
    assert "id" in corpo_da_resposta
    assert corpo_da_resposta["foto"] is not None
    assert corpo_da_resposta["foto"].endswith(".jpg")


def test_criar_livro_sem_campos_opcionais(cliente_api, uow):
    resposta = cliente_api.post(
        "/api/livros",
        data={
            "titulo": "Clean Code",
            "autores": json.dumps(["Robert C. Martin"]),
        },
    )

    assert resposta.status_code == HTTPStatus.CREATED

    corpo_da_resposta = resposta.json()
    assert corpo_da_resposta["titulo"] == "Clean Code"
    assert corpo_da_resposta["autores"] == ["Robert C. Martin"]
    assert corpo_da_resposta["subtitulo"] is None
    assert corpo_da_resposta["isbn"] is None
    assert corpo_da_resposta["observacao"] is None
    assert corpo_da_resposta["foto"] is None
    assert "id" in corpo_da_resposta

    livro_id = corpo_da_resposta["id"]
    resultado = (
        uow.sessao_postgres.execute(
            text("SELECT * FROM livros WHERE id = :id"), {"id": livro_id}
        )
        .mappings()
        .all()
    )

    assert len(resultado) == 1
    livro_no_banco = resultado[0]
    assert livro_no_banco["titulo"] == "Clean Code"
    assert livro_no_banco["autores"] == ["Robert C. Martin"]
    assert livro_no_banco["subtitulo"] is None
    assert livro_no_banco["isbn"] is None
    assert livro_no_banco["observacao"] is None


def test_criar_livro_com_multiplos_autores(cliente_api, uow):
    autores = ["J.R.R. Tolkien", "Christopher Tolkien"]

    resposta = cliente_api.post(
        "/api/livros",
        data={
            "titulo": "O Silmarillion",
            "autores": json.dumps(autores),
        },
    )

    assert resposta.status_code == HTTPStatus.CREATED

    corpo_da_resposta = resposta.json()
    assert corpo_da_resposta["titulo"] == "O Silmarillion"
    assert corpo_da_resposta["autores"] == autores
    assert "id" in corpo_da_resposta

    livro_id = corpo_da_resposta["id"]
    resultado = (
        uow.sessao_postgres.execute(
            text("SELECT * FROM livros WHERE id = :id"), {"id": livro_id}
        )
        .mappings()
        .all()
    )

    assert len(resultado) == 1
    livro_no_banco = resultado[0]
    assert livro_no_banco["autores"] == autores


def test_atualizar_livro_sem_foto(cliente_api, obter_mock_livro_no_banco, uow):
    livro = obter_mock_livro_no_banco()

    novo_titulo = "Título Atualizado"
    novos_autores = ["Autor Atualizado"]
    novo_subtitulo = "Subtítulo Atualizado"
    novo_isbn = "978-9999999999"
    nova_observacao = "Observação Atualizada"

    resposta = cliente_api.put(
        f"/api/livros/{livro.id}",
        data={
            "titulo": novo_titulo,
            "autores": json.dumps(novos_autores),
            "subtitulo": novo_subtitulo,
            "isbn": novo_isbn,
            "observacao": nova_observacao,
        },
    )

    assert resposta.status_code == HTTPStatus.OK

    corpo_da_resposta = resposta.json()
    assert corpo_da_resposta["titulo"] == novo_titulo
    assert corpo_da_resposta["autores"] == novos_autores
    assert corpo_da_resposta["subtitulo"] == novo_subtitulo
    assert corpo_da_resposta["isbn"] == novo_isbn
    assert corpo_da_resposta["observacao"] == nova_observacao
    assert corpo_da_resposta["id"] == str(livro.id)

    resultado = (
        uow.sessao_postgres.execute(
            text("SELECT * FROM livros WHERE id = :id"),
            {"id": str(livro.id.valor)},
        )
        .mappings()
        .all()
    )

    assert len(resultado) == 1
    livro_no_banco = resultado[0]
    assert livro_no_banco["titulo"] == novo_titulo
    assert livro_no_banco["autores"] == novos_autores
    assert livro_no_banco["subtitulo"] == novo_subtitulo
    assert livro_no_banco["isbn"] == novo_isbn
    assert livro_no_banco["observacao"] == nova_observacao


def test_atualizar_livro_com_nova_foto(
    cliente_api, obter_mock_livro_no_banco, uow
):
    livro = obter_mock_livro_no_banco()
    foto_bytes = b"nova foto content"
    foto_arquivo = BytesIO(foto_bytes)

    resposta = cliente_api.put(
        f"/api/livros/{livro.id}",
        data={
            "titulo": livro.titulo.valor,
            "autores": json.dumps(livro.autores.valor),
            "subtitulo": livro.subtitulo.valor,
            "isbn": livro.isbn.valor,
            "observacao": livro.observacao.valor,
        },
        files={"foto": ("nova_capa.jpg", foto_arquivo, "image/jpeg")},
    )

    assert resposta.status_code == HTTPStatus.OK

    corpo_da_resposta = resposta.json()
    assert corpo_da_resposta["id"] == str(livro.id)
    assert corpo_da_resposta["foto"] is not None
    assert corpo_da_resposta["foto"].endswith(".jpg")


def test_atualizar_livro_inexistente(cliente_api, uow):
    livro_id_inexistente = str(LivroId.gerar())

    resposta = cliente_api.put(
        f"/api/livros/{livro_id_inexistente}",
        data={
            "titulo": "Título",
            "autores": json.dumps(["Autor"]),
        },
    )

    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_deletar_livro_com_sucesso(
    cliente_api, obter_mock_livro_no_banco, uow
):
    livro = obter_mock_livro_no_banco()

    resposta = cliente_api.delete(f"/api/livros/{livro.id}")

    assert resposta.status_code == HTTPStatus.NO_CONTENT

    resultado = (
        uow.sessao_postgres.execute(
            text("SELECT * FROM livros WHERE id = :id"),
            {"id": str(livro.id.valor)},
        )
        .mappings()
        .all()
    )

    assert len(resultado) == 0


def test_deletar_livro_inexistente(cliente_api, uow):
    livro_id_inexistente = str(LivroId.gerar())

    resposta = cliente_api.delete(f"/api/livros/{livro_id_inexistente}")

    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_listar_livros_retorna_lista_vazia(cliente_api):
    resposta = cliente_api.get("/api/livros")

    assert resposta.status_code == HTTPStatus.OK
    dados = resposta.json()
    assert dados["itens"] == []
    assert dados["total"] == 0
    assert dados["pagina"] == 1
    assert dados["itens_por_pagina"] == 10
    assert dados["total_paginas"] == 0


def test_listar_livros_retorna_todos_livros(
    cliente_api, obter_mock_livro_no_banco
):
    obter_mock_livro_no_banco()
    obter_mock_livro_no_banco()

    resposta = cliente_api.get("/api/livros")

    assert resposta.status_code == HTTPStatus.OK
    dados = resposta.json()
    assert len(dados["itens"]) == 2
    assert dados["total"] == 2
    assert dados["pagina"] == 1
    assert dados["itens_por_pagina"] == 10


def test_listar_livros_com_paginacao(cliente_api, obter_mock_livro_no_banco):
    for _ in range(5):
        obter_mock_livro_no_banco()

    resposta = cliente_api.get("/api/livros?pagina=1&itens_por_pagina=2")

    assert resposta.status_code == HTTPStatus.OK
    dados = resposta.json()
    assert len(dados["itens"]) == 2
    assert dados["total"] == 5
    assert dados["pagina"] == 1
    assert dados["itens_por_pagina"] == 2
    assert dados["total_paginas"] == 3


def test_listar_livros_segunda_pagina(cliente_api, obter_mock_livro_no_banco):
    for _ in range(5):
        obter_mock_livro_no_banco()

    resposta = cliente_api.get("/api/livros?pagina=2&itens_por_pagina=2")

    assert resposta.status_code == HTTPStatus.OK
    dados = resposta.json()
    assert len(dados["itens"]) == 2
    assert dados["total"] == 5
    assert dados["pagina"] == 2
    assert dados["itens_por_pagina"] == 2


def test_listar_livros_com_filtro_por_titulo(
    cliente_api, obter_mock_livro_no_banco
):
    obter_mock_livro_no_banco(titulo="Dom Casmurro")
    obter_mock_livro_no_banco(titulo="Memórias Póstumas")

    resposta = cliente_api.get("/api/livros?titulo=contem.Casmurro")

    assert resposta.status_code == HTTPStatus.OK
    dados = resposta.json()
    assert len(dados["itens"]) == 1
    assert dados["itens"][0]["titulo"] == "Dom Casmurro"


def test_listar_livros_estrutura_item(cliente_api, obter_mock_livro_no_banco):
    livro = obter_mock_livro_no_banco()

    resposta = cliente_api.get("/api/livros")

    assert resposta.status_code == HTTPStatus.OK
    dados = resposta.json()
    item = dados["itens"][0]
    assert item["id"] == str(livro.id)
    assert item["titulo"] == livro.titulo.valor
    assert item["autores"] == livro.autores.valor
    assert item["subtitulo"] == livro.subtitulo.valor
    assert item["isbn"] == livro.isbn.valor
    assert item["observacao"] == livro.observacao.valor
