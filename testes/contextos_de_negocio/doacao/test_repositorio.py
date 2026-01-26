from sqlalchemy import text

from contextos_de_negocio.doacao.dominio.objetos_de_valor import DoacaoId
from contextos_de_negocio.livros.dominio.objetos_de_valor import LivroId


def test_adicionar_doacao_nova(
    uow,
    obter_mock_doacao,
    obter_mock_doador_no_banco,
    obter_mock_instituicao_no_banco,
    obter_mock_livro_no_banco,
):
    doador = obter_mock_doador_no_banco()
    instituicao = obter_mock_instituicao_no_banco()
    livro_1 = obter_mock_livro_no_banco()
    livro_2 = obter_mock_livro_no_banco()

    doacao = obter_mock_doacao(
        doador_id=doador.id,
        instituicao_id=instituicao.id,
        livros_ids=[livro_1.id, livro_2.id],
    )

    doacao_adicionada = uow.repositorio_doacoes.adicionar(doacao)
    uow.commit()

    assert doacao_adicionada.id is not None
    assert doacao_adicionada.doador_id == doador.id
    assert doacao_adicionada.instituicao_id == instituicao.id
    assert len(doacao_adicionada.livros) == 2
    livros_ids_adicionados = [
        livro.livro_id for livro in doacao_adicionada.livros
    ]
    assert livro_1.id in livros_ids_adicionados
    assert livro_2.id in livros_ids_adicionados

    resultado = (
        uow.sessao_postgres.execute(
            text("SELECT * FROM doacoes WHERE id = :id"),
            {"id": str(doacao_adicionada.id.valor)},
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
            {"doacao_id": str(doacao_adicionada.id.valor)},
        )
        .mappings()
        .all()
    )

    assert len(resultado_livros) == 2
    livros_ids_no_banco = [
        LivroId(row["livro_id"]) for row in resultado_livros
    ]
    assert livro_1.id in livros_ids_no_banco
    assert livro_2.id in livros_ids_no_banco


def test_buscar_por_id_encontra_doacao(
    uow,
    obter_mock_doacao_no_banco,
    obter_mock_doador_no_banco,
    obter_mock_instituicao_no_banco,
    obter_mock_livro_no_banco,
):
    doador = obter_mock_doador_no_banco()
    instituicao = obter_mock_instituicao_no_banco()
    livro = obter_mock_livro_no_banco()

    doacao_criada = obter_mock_doacao_no_banco(
        doador_id=doador.id,
        instituicao_id=instituicao.id,
        livros_ids=[livro.id],
    )

    doacao = uow.repositorio_doacoes.buscar_por_id(doacao_criada.id)

    assert doacao is not None
    assert doacao.id == doacao_criada.id
    assert doacao.doador_id == doador.id
    assert doacao.instituicao_id == instituicao.id
    assert len(doacao.livros) == 1
    assert doacao.livros[0].livro_id == livro.id


def test_buscar_por_id_nao_encontra_doacao(uow):
    doacao_id_inexistente = DoacaoId.gerar()
    doacao = uow.repositorio_doacoes.buscar_por_id(doacao_id_inexistente)

    assert doacao is None


def test_instituicao_existe(uow, obter_mock_instituicao_no_banco):
    instituicao = obter_mock_instituicao_no_banco()

    existe = uow.repositorio_doacoes.instituicao_existe(instituicao.id)

    assert existe is True


def test_livros_existem(uow, obter_mock_livro_no_banco):
    livro_1 = obter_mock_livro_no_banco()
    livro_2 = obter_mock_livro_no_banco()

    existem = uow.repositorio_doacoes.livros_existem([livro_1.id, livro_2.id])

    assert existem is True
