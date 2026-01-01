from sqlalchemy import text

from contextos_de_negocio.instituicao.dominio.objetos_de_valor import (
    InstituicaoId,
)


def test_adicionar_instituicao_nova(uow, obter_mock_instituicao):
    instituicao = obter_mock_instituicao(id=None)

    instituicao_adicionada = uow.repositorio_instituicoes.adicionar(
        instituicao
    )
    uow.commit()

    assert instituicao_adicionada.id is not None
    assert instituicao_adicionada.nome == instituicao.nome
    assert instituicao_adicionada.email == instituicao.email
    assert instituicao_adicionada.telefone == instituicao.telefone
    assert instituicao_adicionada.descricao == instituicao.descricao
    assert instituicao_adicionada.endereco == instituicao.endereco

    resultado = (
        uow.sessao_postgres.execute(
            text("SELECT * FROM instituicoes WHERE id = :id"),
            {"id": str(instituicao_adicionada.id.valor)},
        )
        .mappings()
        .all()
    )

    assert len(resultado) == 1
    instituicao_no_banco = resultado[0]
    assert instituicao_no_banco["nome"] == instituicao.nome.valor
    assert instituicao_no_banco["email"] == instituicao.email.valor
    assert instituicao_no_banco["senha"] == instituicao.senha.valor
    assert instituicao_no_banco["telefone"] == instituicao.telefone.valor
    assert instituicao_no_banco["descricao"] == instituicao.descricao.valor
    assert instituicao_no_banco["endereco"] == instituicao.endereco.valor


def test_adicionar_atualiza_instituicao_existente(uow, obter_mock_instituicao):
    instituicao_id = InstituicaoId.gerar()
    instituicao_original = obter_mock_instituicao(id=instituicao_id)
    uow.sessao_postgres.execute(
        text(
            """
            INSERT INTO instituicoes (
                id, nome, email, senha, telefone, descricao,
                data_fundacao, endereco, site, foto
            )
            VALUES (
                :id, :nome, :email, :senha, :telefone, :descricao,
                :data_fundacao, :endereco, :site, :foto
            )
            """
        ),
        {
            "id": str(instituicao_original.id.valor),
            "nome": instituicao_original.nome.valor,
            "email": instituicao_original.email.valor,
            "senha": instituicao_original.senha.valor,
            "telefone": instituicao_original.telefone.valor,
            "descricao": instituicao_original.descricao.valor,
            "data_fundacao": instituicao_original.data_fundacao.valor,
            "endereco": instituicao_original.endereco.valor,
            "site": instituicao_original.site.valor
            if instituicao_original.site
            else None,
            "foto": instituicao_original.foto.valor
            if instituicao_original.foto
            else None,
        },
    )
    uow.commit()

    instituicao_atualizada_dados = obter_mock_instituicao(
        id=instituicao_id,
        nome="Nome Atualizado",
        email="email.atualizado@instituicao.org",
        senha="novasenha",
        telefone="11777777777",
        descricao="Descrição atualizada",
        endereco="Rua Atualizada, 999",
    )

    instituicao_atualizada = uow.repositorio_instituicoes.adicionar(
        instituicao_atualizada_dados
    )
    uow.commit()

    assert instituicao_atualizada.id == instituicao_id
    assert instituicao_atualizada.nome == instituicao_atualizada_dados.nome
    assert instituicao_atualizada.email == instituicao_atualizada_dados.email
    assert (
        instituicao_atualizada.telefone
        == instituicao_atualizada_dados.telefone
    )
    assert (
        instituicao_atualizada.descricao
        == instituicao_atualizada_dados.descricao
    )
    assert (
        instituicao_atualizada.endereco
        == instituicao_atualizada_dados.endereco
    )

    resultado = (
        uow.sessao_postgres.execute(
            text("SELECT * FROM instituicoes WHERE id = :id"),
            {"id": str(instituicao_id.valor)},
        )
        .mappings()
        .all()
    )

    assert len(resultado) == 1
    instituicao_no_banco = resultado[0]
    assert (
        instituicao_no_banco["nome"] == instituicao_atualizada_dados.nome.valor
    )
    assert (
        instituicao_no_banco["email"]
        == instituicao_atualizada_dados.email.valor
    )
    assert (
        instituicao_no_banco["senha"]
        == instituicao_atualizada_dados.senha.valor
    )
    assert (
        instituicao_no_banco["telefone"]
        == instituicao_atualizada_dados.telefone.valor
    )
    assert (
        instituicao_no_banco["descricao"]
        == instituicao_atualizada_dados.descricao.valor
    )
    assert (
        instituicao_no_banco["endereco"]
        == instituicao_atualizada_dados.endereco.valor
    )


def test_buscar_por_id_encontra_instituicao(uow, obter_mock_instituicao):
    instituicao_id = InstituicaoId.gerar()
    instituicao_mock = obter_mock_instituicao(id=instituicao_id)
    uow.sessao_postgres.execute(
        text(
            """
            INSERT INTO instituicoes (
                id, nome, email, senha, telefone, descricao,
                data_fundacao, endereco, site, foto
            )
            VALUES (
                :id, :nome, :email, :senha, :telefone, :descricao,
                :data_fundacao, :endereco, :site, :foto
            )
            """
        ),
        {
            "id": str(instituicao_mock.id.valor),
            "nome": instituicao_mock.nome.valor,
            "email": instituicao_mock.email.valor,
            "senha": instituicao_mock.senha.valor,
            "telefone": instituicao_mock.telefone.valor,
            "descricao": instituicao_mock.descricao.valor,
            "data_fundacao": instituicao_mock.data_fundacao.valor,
            "endereco": instituicao_mock.endereco.valor,
            "site": instituicao_mock.site.valor
            if instituicao_mock.site
            else None,
            "foto": instituicao_mock.foto.valor
            if instituicao_mock.foto
            else None,
        },
    )
    uow.commit()

    instituicao = uow.repositorio_instituicoes.buscar_por_id(instituicao_id)

    assert instituicao is not None
    assert instituicao.id == instituicao_mock.id
    assert instituicao.nome == instituicao_mock.nome
    assert instituicao.email == instituicao_mock.email
    assert instituicao.senha == instituicao_mock.senha
    assert instituicao.telefone == instituicao_mock.telefone
    assert instituicao.descricao == instituicao_mock.descricao
    assert instituicao.endereco == instituicao_mock.endereco


def test_buscar_por_id_nao_encontra_instituicao(uow):
    instituicao_id_inexistente = InstituicaoId.gerar()
    instituicao = uow.repositorio_instituicoes.buscar_por_id(
        instituicao_id_inexistente
    )

    assert instituicao is None


def test_buscar_por_email_encontra_instituicao(uow, obter_mock_instituicao):
    instituicao_id = InstituicaoId.gerar()
    instituicao_mock = obter_mock_instituicao(id=instituicao_id)
    uow.sessao_postgres.execute(
        text(
            """
            INSERT INTO instituicoes (
                id, nome, email, senha, telefone, descricao,
                data_fundacao, endereco, site, foto
            )
            VALUES (
                :id, :nome, :email, :senha, :telefone, :descricao,
                :data_fundacao, :endereco, :site, :foto
            )
            """
        ),
        {
            "id": str(instituicao_mock.id.valor),
            "nome": instituicao_mock.nome.valor,
            "email": instituicao_mock.email.valor,
            "senha": instituicao_mock.senha.valor,
            "telefone": instituicao_mock.telefone.valor,
            "descricao": instituicao_mock.descricao.valor,
            "data_fundacao": instituicao_mock.data_fundacao.valor,
            "endereco": instituicao_mock.endereco.valor,
            "site": instituicao_mock.site.valor
            if instituicao_mock.site
            else None,
            "foto": instituicao_mock.foto.valor
            if instituicao_mock.foto
            else None,
        },
    )
    uow.commit()

    instituicao = uow.repositorio_instituicoes.buscar_por_email(
        instituicao_mock.email.valor
    )

    assert instituicao is not None
    assert instituicao.id == instituicao_mock.id
    assert instituicao.nome == instituicao_mock.nome
    assert instituicao.email == instituicao_mock.email
    assert instituicao.senha == instituicao_mock.senha
    assert instituicao.telefone == instituicao_mock.telefone
    assert instituicao.descricao == instituicao_mock.descricao
    assert instituicao.endereco == instituicao_mock.endereco


def test_buscar_por_email_nao_encontra_instituicao(uow):
    instituicao = uow.repositorio_instituicoes.buscar_por_email(
        "naoexiste@instituicao.org"
    )

    assert instituicao is None
