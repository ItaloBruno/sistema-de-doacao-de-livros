from sqlalchemy import text

from contextos_de_negocio.doador.dominio.objetos_de_valor import DoadorId
from utilitarios.objetos_de_valor.filtragem import ConjuntoFiltros
from utilitarios.objetos_de_valor.paginacao import (
    ItensPorPagina,
    NumeroPagina,
)


def test_adicionar_doador_novo(uow, obter_mock_doador):
    doador = obter_mock_doador(id=None)

    doador_adicionado = uow.repositorio_doadores.adicionar(doador)
    uow.commit()

    assert doador_adicionado.id is not None
    assert doador_adicionado.nome == doador.nome
    assert doador_adicionado.email == doador.email
    assert doador_adicionado.telefone == doador.telefone

    resultado = (
        uow.sessao_postgres.execute(
            text("SELECT * FROM doadores WHERE id = :id"),
            {"id": str(doador_adicionado.id.valor)},
        )
        .mappings()
        .all()
    )

    assert len(resultado) == 1
    doador_no_banco = resultado[0]
    assert doador_no_banco["nome"] == doador.nome.valor
    assert doador_no_banco["email"] == doador.email.valor
    assert doador_no_banco["senha"] == doador.senha.valor
    assert doador_no_banco["telefone"] == doador.telefone.valor


def test_adicionar_atualiza_doador_existente(uow, obter_mock_doador):
    doador_id = DoadorId.gerar()
    doador_original = obter_mock_doador(id=doador_id)
    uow.sessao_postgres.execute(
        text(
            """
            INSERT INTO doadores (id, nome, email, senha, telefone)
            VALUES (:id, :nome, :email, :senha, :telefone)
            """
        ),
        {
            "id": str(doador_original.id.valor),
            "nome": doador_original.nome.valor,
            "email": doador_original.email.valor,
            "senha": doador_original.senha.valor,
            "telefone": doador_original.telefone.valor,
        },
    )
    uow.commit()

    doador_atualizado_dados = obter_mock_doador(
        id=doador_id,
        nome="Nome Atualizado",
        email="email.atualizado@example.com",
        senha="novasenha",
        telefone="11777777777",
    )

    doador_atualizado = uow.repositorio_doadores.adicionar(
        doador_atualizado_dados
    )
    uow.commit()

    assert doador_atualizado.id == doador_id
    assert doador_atualizado.nome == doador_atualizado_dados.nome
    assert doador_atualizado.email == doador_atualizado_dados.email
    assert doador_atualizado.telefone == doador_atualizado_dados.telefone

    resultado = (
        uow.sessao_postgres.execute(
            text("SELECT * FROM doadores WHERE id = :id"),
            {"id": str(doador_id.valor)},
        )
        .mappings()
        .all()
    )

    assert len(resultado) == 1
    doador_no_banco = resultado[0]
    assert doador_no_banco["nome"] == doador_atualizado_dados.nome.valor
    assert doador_no_banco["email"] == doador_atualizado_dados.email.valor
    assert doador_no_banco["senha"] == doador_atualizado_dados.senha.valor
    assert (
        doador_no_banco["telefone"] == doador_atualizado_dados.telefone.valor
    )


def test_buscar_por_id_encontra_doador(uow, obter_mock_doador):
    doador_id = DoadorId.gerar()
    doador_mock = obter_mock_doador(id=doador_id)
    uow.sessao_postgres.execute(
        text(
            """
            INSERT INTO doadores (id, nome, email, senha, telefone)
            VALUES (:id, :nome, :email, :senha, :telefone)
            """
        ),
        {
            "id": str(doador_mock.id.valor),
            "nome": doador_mock.nome.valor,
            "email": doador_mock.email.valor,
            "senha": doador_mock.senha.valor,
            "telefone": doador_mock.telefone.valor,
        },
    )
    uow.commit()

    doador = uow.repositorio_doadores.buscar_por_id(doador_id)

    assert doador is not None
    assert doador.id == doador_mock.id
    assert doador.nome == doador_mock.nome
    assert doador.email == doador_mock.email
    assert doador.senha == doador_mock.senha
    assert doador.telefone == doador_mock.telefone


def test_buscar_por_id_nao_encontra_doador(uow):
    doador_id_inexistente = DoadorId.gerar()
    doador = uow.repositorio_doadores.buscar_por_id(doador_id_inexistente)

    assert doador is None


def test_buscar_por_email_encontra_doador(uow, obter_mock_doador):
    doador_id = DoadorId.gerar()
    doador_mock = obter_mock_doador(id=doador_id)
    uow.sessao_postgres.execute(
        text(
            """
            INSERT INTO doadores (id, nome, email, senha, telefone)
            VALUES (:id, :nome, :email, :senha, :telefone)
            """
        ),
        {
            "id": str(doador_mock.id.valor),
            "nome": doador_mock.nome.valor,
            "email": doador_mock.email.valor,
            "senha": doador_mock.senha.valor,
            "telefone": doador_mock.telefone.valor,
        },
    )
    uow.commit()

    doador = uow.repositorio_doadores.buscar_por_email(doador_mock.email.valor)

    assert doador is not None
    assert doador.id == doador_mock.id
    assert doador.nome == doador_mock.nome
    assert doador.email == doador_mock.email
    assert doador.senha == doador_mock.senha
    assert doador.telefone == doador_mock.telefone


def test_buscar_por_email_nao_encontra_doador(uow):
    doador = uow.repositorio_doadores.buscar_por_email("naoexiste@example.com")

    assert doador is None


def test_listar_doadores_com_sucesso(uow, obter_mock_doador):
    doador1_id = DoadorId.gerar()
    doador1 = obter_mock_doador(
        id=doador1_id, nome="Ana Silva", email="ana@example.com"
    )
    doador2_id = DoadorId.gerar()
    doador2 = obter_mock_doador(
        id=doador2_id, nome="Bruno Costa", email="bruno@example.com"
    )

    uow.sessao_postgres.execute(
        text(
            """
            INSERT INTO doadores (id, nome, email, senha, telefone)
            VALUES (:id, :nome, :email, :senha, :telefone)
            """
        ),
        {
            "id": str(doador1.id.valor),
            "nome": doador1.nome.valor,
            "email": doador1.email.valor,
            "senha": doador1.senha.valor,
            "telefone": doador1.telefone.valor,
        },
    )
    uow.sessao_postgres.execute(
        text(
            """
            INSERT INTO doadores (id, nome, email, senha, telefone)
            VALUES (:id, :nome, :email, :senha, :telefone)
            """
        ),
        {
            "id": str(doador2.id.valor),
            "nome": doador2.nome.valor,
            "email": doador2.email.valor,
            "senha": doador2.senha.valor,
            "telefone": doador2.telefone.valor,
        },
    )
    uow.commit()

    resultado = uow.repositorio_doadores.listar_com_filtros(
        filtros=ConjuntoFiltros.de_dict({}),
        pagina=NumeroPagina(1),
        itens_por_pagina=ItensPorPagina(10),
    )

    assert resultado.total == 2
    assert len(resultado.itens) == 2
    assert resultado.pagina == 1
    assert resultado.itens_por_pagina == 10
    assert resultado.total_paginas == 1
