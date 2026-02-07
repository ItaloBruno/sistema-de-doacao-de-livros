from sqlalchemy import text

from contextos_de_negocio.livros.dominio.objetos_de_valor import LivroId


def test_adicionar_livro_novo(uow, obter_mock_livro):
    livro = obter_mock_livro(id=None)

    livro_adicionado = uow.repositorio_livros.adicionar(livro)
    uow.commit()

    assert livro_adicionado.id is not None
    assert livro_adicionado.titulo == livro.titulo
    assert livro_adicionado.autores == livro.autores
    assert livro_adicionado.subtitulo == livro.subtitulo
    assert livro_adicionado.isbn == livro.isbn
    assert livro_adicionado.observacao == livro.observacao

    resultado = (
        uow.sessao_postgres.execute(
            text("SELECT * FROM livros WHERE id = :id"),
            {"id": str(livro_adicionado.id.valor)},
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


def test_adicionar_atualiza_livro_existente(uow, obter_mock_livro):
    livro_id = LivroId.gerar()
    livro_original = obter_mock_livro(id=livro_id)
    uow.sessao_postgres.execute(
        text(
            """
            INSERT INTO livros (
                id, titulo, subtitulo, autores,
                isbn, foto_url, observacao
            )
            VALUES (
                :id, :titulo, :subtitulo, :autores,
                :isbn, :foto_url, :observacao
            )
            """
        ),
        {
            "id": str(livro_original.id.valor),
            "titulo": livro_original.titulo.valor,
            "subtitulo": livro_original.subtitulo.valor,
            "autores": livro_original.autores.valor,
            "isbn": livro_original.isbn.valor,
            "foto_url": livro_original.foto_url.valor
            if livro_original.foto_url
            else None,
            "observacao": livro_original.observacao.valor,
        },
    )
    uow.commit()

    livro_atualizado_dados = obter_mock_livro(
        id=livro_id,
        titulo="Título Atualizado",
        autores=["Autor Atualizado"],
        subtitulo="Subtítulo Atualizado",
        isbn="978-1234567890",
        observacao="Observação Atualizada",
    )

    livro_atualizado = uow.repositorio_livros.adicionar(livro_atualizado_dados)
    uow.commit()

    assert livro_atualizado.id == livro_id
    assert livro_atualizado.titulo == livro_atualizado_dados.titulo
    assert livro_atualizado.autores == livro_atualizado_dados.autores
    assert livro_atualizado.subtitulo == livro_atualizado_dados.subtitulo
    assert livro_atualizado.isbn == livro_atualizado_dados.isbn

    resultado = (
        uow.sessao_postgres.execute(
            text("SELECT * FROM livros WHERE id = :id"),
            {"id": str(livro_id.valor)},
        )
        .mappings()
        .all()
    )

    assert len(resultado) == 1
    livro_no_banco = resultado[0]
    assert livro_no_banco["titulo"] == livro_atualizado_dados.titulo.valor
    assert livro_no_banco["autores"] == livro_atualizado_dados.autores.valor
    assert (
        livro_no_banco["subtitulo"] == livro_atualizado_dados.subtitulo.valor
    )
    assert livro_no_banco["isbn"] == livro_atualizado_dados.isbn.valor
    assert (
        livro_no_banco["observacao"] == livro_atualizado_dados.observacao.valor
    )


def test_buscar_por_id_encontra_livro(uow, obter_mock_livro):
    livro_id = LivroId.gerar()
    livro_mock = obter_mock_livro(id=livro_id)
    uow.sessao_postgres.execute(
        text(
            """
            INSERT INTO livros (
                id, titulo, subtitulo, autores,
                isbn, foto_url, observacao
            )
            VALUES (
                :id, :titulo, :subtitulo, :autores,
                :isbn, :foto_url, :observacao
            )
            """
        ),
        {
            "id": str(livro_mock.id.valor),
            "titulo": livro_mock.titulo.valor,
            "subtitulo": livro_mock.subtitulo.valor,
            "autores": livro_mock.autores.valor,
            "isbn": livro_mock.isbn.valor,
            "foto_url": livro_mock.foto_url.valor
            if livro_mock.foto_url
            else None,
            "observacao": livro_mock.observacao.valor,
        },
    )
    uow.commit()

    livro = uow.repositorio_livros.buscar_por_id(livro_id)

    assert livro is not None
    assert livro.id == livro_mock.id
    assert livro.titulo == livro_mock.titulo
    assert livro.autores == livro_mock.autores
    assert livro.subtitulo == livro_mock.subtitulo
    assert livro.isbn == livro_mock.isbn
    assert livro.observacao == livro_mock.observacao


def test_buscar_por_id_nao_encontra_livro(uow):
    livro_id_inexistente = LivroId.gerar()
    livro = uow.repositorio_livros.buscar_por_id(livro_id_inexistente)

    assert livro is None


def test_deletar_livro(uow, obter_mock_livro):
    livro_id = LivroId.gerar()
    livro_mock = obter_mock_livro(id=livro_id)
    uow.sessao_postgres.execute(
        text(
            """
            INSERT INTO livros (
                id, titulo, subtitulo, autores,
                isbn, foto_url, observacao
            )
            VALUES (
                :id, :titulo, :subtitulo, :autores,
                :isbn, :foto_url, :observacao
            )
            """
        ),
        {
            "id": str(livro_mock.id.valor),
            "titulo": livro_mock.titulo.valor,
            "subtitulo": livro_mock.subtitulo.valor,
            "autores": livro_mock.autores.valor,
            "isbn": livro_mock.isbn.valor,
            "foto_url": livro_mock.foto_url.valor
            if livro_mock.foto_url
            else None,
            "observacao": livro_mock.observacao.valor,
        },
    )
    uow.commit()

    livro = uow.repositorio_livros.buscar_por_id(livro_id)
    assert livro is not None

    uow.repositorio_livros.deletar(livro)
    uow.commit()

    resultado = (
        uow.sessao_postgres.execute(
            text("SELECT * FROM livros WHERE id = :id"),
            {"id": str(livro_id.valor)},
        )
        .mappings()
        .all()
    )

    assert len(resultado) == 0
