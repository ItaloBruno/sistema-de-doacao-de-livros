import pytest

from contextos_de_negocio.doador.casos_de_uso.atualizar_doador import (
    AtualizarDoador,
)
from contextos_de_negocio.doador.casos_de_uso.dtos import (
    EntradaAtualizarDoadorCasoDeUso,
)
from contextos_de_negocio.doador.dominio.objetos_de_valor import DoadorId
from contextos_de_negocio.doador.excecoes import (
    DoadorNaoEncontrado,
    EmailJaCadastrado,
    SenhaIncorreta,
)
from testes.contextos_de_negocio.doador.casos_de_uso import (
    UnidadeDeTrabalhoFake,
    obter_uow_fake,
)


def test_deve_atualizar_doador_com_sucesso(obter_mock_doador):
    uow = UnidadeDeTrabalhoFake()
    doador = obter_mock_doador()
    uow.repositorio_doadores.adicionar(doador)

    def obter_uow_com_doador():
        return uow

    entrada = EntradaAtualizarDoadorCasoDeUso(
        doador_id=str(doador.id),
        nome="João Silva Atualizado",
        email="joao.novo@example.com",
        telefone="11888888888",
        senha_atual=doador.senha.valor,
        nova_senha=None,
    )

    caso_de_uso = AtualizarDoador(entrada, obter_uow_com_doador)
    saida = caso_de_uso.executar()

    assert saida.id == str(doador.id)
    assert saida.nome == "João Silva Atualizado"
    assert saida.email == "joao.novo@example.com"
    assert saida.telefone == "11888888888"


def test_deve_lancar_excecao_quando_doador_nao_encontrado(obter_mock_doador):
    doador = obter_mock_doador()
    entrada = EntradaAtualizarDoadorCasoDeUso(
        doador_id=str(DoadorId.gerar()),
        nome=doador.nome.valor,
        email=doador.email.valor,
        telefone=doador.telefone.valor,
        senha_atual=doador.senha.valor,
        nova_senha=None,
    )
    caso_de_uso = AtualizarDoador(entrada, obter_uow_fake)

    with pytest.raises(DoadorNaoEncontrado):
        caso_de_uso.executar()


def test_deve_lancar_excecao_quando_senha_incorreta(obter_mock_doador):
    uow = UnidadeDeTrabalhoFake()
    doador = obter_mock_doador()
    uow.repositorio_doadores.adicionar(doador)

    def obter_uow_com_doador():
        return uow

    entrada = EntradaAtualizarDoadorCasoDeUso(
        doador_id=str(doador.id),
        nome=doador.nome.valor,
        email=doador.email.valor,
        telefone=doador.telefone.valor,
        senha_atual="senha_errada",
        nova_senha=None,
    )
    caso_de_uso = AtualizarDoador(entrada, obter_uow_com_doador)

    with pytest.raises(SenhaIncorreta):
        caso_de_uso.executar()


def test_deve_lancar_excecao_quando_novo_email_ja_cadastrado(
    obter_mock_doador,
):
    uow = UnidadeDeTrabalhoFake()
    doador1 = obter_mock_doador(id=DoadorId.gerar(), email="joao@example.com")
    doador2 = obter_mock_doador(id=DoadorId.gerar(), email="maria@example.com")
    uow.repositorio_doadores.adicionar(doador1)
    uow.repositorio_doadores.adicionar(doador2)

    def obter_uow_com_doadores():
        return uow

    entrada = EntradaAtualizarDoadorCasoDeUso(
        doador_id=str(doador1.id),
        nome=doador1.nome.valor,
        email=doador2.email.valor,
        telefone=doador1.telefone.valor,
        senha_atual=doador1.senha.valor,
        nova_senha=None,
    )
    caso_de_uso = AtualizarDoador(entrada, obter_uow_com_doadores)

    with pytest.raises(EmailJaCadastrado):
        caso_de_uso.executar()


def test_deve_atualizar_senha_quando_nova_senha_fornecida(obter_mock_doador):
    uow = UnidadeDeTrabalhoFake()
    doador = obter_mock_doador()
    uow.repositorio_doadores.adicionar(doador)

    def obter_uow_com_doador():
        return uow

    entrada = EntradaAtualizarDoadorCasoDeUso(
        doador_id=str(doador.id),
        nome=doador.nome.valor,
        email=doador.email.valor,
        telefone=doador.telefone.valor,
        senha_atual=doador.senha.valor,
        nova_senha="nova_senha456",
    )

    caso_de_uso = AtualizarDoador(entrada, obter_uow_com_doador)
    caso_de_uso.executar()

    doador_atualizado = uow.repositorio_doadores.buscar_por_id(doador.id)
    assert doador_atualizado is not None
    assert doador_atualizado.senha.valor == "nova_senha456"
