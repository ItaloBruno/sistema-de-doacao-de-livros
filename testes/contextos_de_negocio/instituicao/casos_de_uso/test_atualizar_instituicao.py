import pytest

from contextos_de_negocio.instituicao.casos_de_uso import (
    atualizar_instituicao,
)
from contextos_de_negocio.instituicao.casos_de_uso.dtos import (
    EntradaAtualizarInstituicaoCasoDeUso,
)
from contextos_de_negocio.instituicao.dominio.objetos_de_valor import (
    InstituicaoId,
)
from contextos_de_negocio.instituicao.excecoes import (
    EmailJaCadastrado,
    InstituicaoNaoEncontrada,
    SenhaIncorreta,
)
from testes.contextos_de_negocio.instituicao.casos_de_uso import (
    UnidadeDeTrabalhoFake,
    obter_uow_fake,
)
from utilitarios.provedor_de_armazenamento import ProvedorDeArmazenamento
from utilitarios.provedor_de_armazenamento.armazenamento_local import (
    EstrategiaArmazenamentoLocal,
)

provedor_de_armazenamento_fake = ProvedorDeArmazenamento(
    EstrategiaArmazenamentoLocal()
)


def test_deve_atualizar_instituicao_com_sucesso(obter_mock_instituicao):
    uow = UnidadeDeTrabalhoFake()
    instituicao = obter_mock_instituicao()
    uow.repositorio_instituicoes.adicionar(instituicao)

    def obter_uow_com_instituicao():
        return uow

    entrada = EntradaAtualizarInstituicaoCasoDeUso(
        instituicao_id=str(instituicao.id),
        nome="Instituição Atualizada",
        email="novo@instituicao.org",
        telefone="11888888888",
        senha_atual=instituicao.senha.valor,
        descricao="Nova descrição",
        data_fundacao="2021-06-15",
        endereco="Rua Nova, 789",
        site="https://novositе.org",
        nova_senha=None,
        foto=None,
        nome_arquivo_foto=None,
    )

    caso_de_uso = atualizar_instituicao.AtualizarInstituicao(
        entrada, obter_uow_com_instituicao, provedor_de_armazenamento_fake
    )
    saida = caso_de_uso.executar()

    assert saida.id == str(instituicao.id)
    assert saida.nome == "Instituição Atualizada"
    assert saida.email == "novo@instituicao.org"
    assert saida.telefone == "11888888888"
    assert saida.descricao == "Nova descrição"
    assert saida.endereco == "Rua Nova, 789"


def test_deve_lancar_excecao_quando_instituicao_nao_encontrada(
    obter_mock_instituicao,
):
    instituicao = obter_mock_instituicao()
    entrada = EntradaAtualizarInstituicaoCasoDeUso(
        instituicao_id=str(InstituicaoId.gerar()),
        nome=instituicao.nome.valor,
        email=instituicao.email.valor,
        telefone=instituicao.telefone.valor,
        senha_atual=instituicao.senha.valor,
        descricao=instituicao.descricao.valor,
        data_fundacao=str(instituicao.data_fundacao.valor),
        endereco=instituicao.endereco.valor,
        site=None,
        nova_senha=None,
        foto=None,
        nome_arquivo_foto=None,
    )
    caso_de_uso = atualizar_instituicao.AtualizarInstituicao(
        entrada, obter_uow_fake, provedor_de_armazenamento_fake
    )

    with pytest.raises(InstituicaoNaoEncontrada):
        caso_de_uso.executar()


def test_deve_lancar_excecao_quando_senha_incorreta(obter_mock_instituicao):
    uow = UnidadeDeTrabalhoFake()
    instituicao = obter_mock_instituicao()
    uow.repositorio_instituicoes.adicionar(instituicao)

    def obter_uow_com_instituicao():
        return uow

    entrada = EntradaAtualizarInstituicaoCasoDeUso(
        instituicao_id=str(instituicao.id),
        nome=instituicao.nome.valor,
        email=instituicao.email.valor,
        telefone=instituicao.telefone.valor,
        senha_atual="senha_errada",
        descricao=instituicao.descricao.valor,
        data_fundacao=str(instituicao.data_fundacao.valor),
        endereco=instituicao.endereco.valor,
        site=None,
        nova_senha=None,
        foto=None,
        nome_arquivo_foto=None,
    )
    caso_de_uso = atualizar_instituicao.AtualizarInstituicao(
        entrada, obter_uow_com_instituicao, provedor_de_armazenamento_fake
    )

    with pytest.raises(SenhaIncorreta):
        caso_de_uso.executar()


def test_deve_lancar_excecao_quando_novo_email_ja_cadastrado(
    obter_mock_instituicao,
):
    uow = UnidadeDeTrabalhoFake()
    instituicao1 = obter_mock_instituicao(
        id=InstituicaoId.gerar(), email="inst1@exemplo.org"
    )
    instituicao2 = obter_mock_instituicao(
        id=InstituicaoId.gerar(), email="inst2@exemplo.org"
    )
    uow.repositorio_instituicoes.adicionar(instituicao1)
    uow.repositorio_instituicoes.adicionar(instituicao2)

    def obter_uow_com_instituicoes():
        return uow

    entrada = EntradaAtualizarInstituicaoCasoDeUso(
        instituicao_id=str(instituicao1.id),
        nome=instituicao1.nome.valor,
        email=instituicao2.email.valor,
        telefone=instituicao1.telefone.valor,
        senha_atual=instituicao1.senha.valor,
        descricao=instituicao1.descricao.valor,
        data_fundacao=str(instituicao1.data_fundacao.valor),
        endereco=instituicao1.endereco.valor,
        site=None,
        nova_senha=None,
        foto=None,
        nome_arquivo_foto=None,
    )
    caso_de_uso = atualizar_instituicao.AtualizarInstituicao(
        entrada, obter_uow_com_instituicoes, provedor_de_armazenamento_fake
    )

    with pytest.raises(EmailJaCadastrado):
        caso_de_uso.executar()


def test_deve_atualizar_senha_quando_nova_senha_fornecida(
    obter_mock_instituicao,
):
    uow = UnidadeDeTrabalhoFake()
    instituicao = obter_mock_instituicao()
    uow.repositorio_instituicoes.adicionar(instituicao)

    def obter_uow_com_instituicao():
        return uow

    entrada = EntradaAtualizarInstituicaoCasoDeUso(
        instituicao_id=str(instituicao.id),
        nome=instituicao.nome.valor,
        email=instituicao.email.valor,
        telefone=instituicao.telefone.valor,
        senha_atual=instituicao.senha.valor,
        descricao=instituicao.descricao.valor,
        data_fundacao=str(instituicao.data_fundacao.valor),
        endereco=instituicao.endereco.valor,
        site=None,
        nova_senha="nova_senha456",
        foto=None,
        nome_arquivo_foto=None,
    )

    caso_de_uso = atualizar_instituicao.AtualizarInstituicao(
        entrada, obter_uow_com_instituicao, provedor_de_armazenamento_fake
    )
    caso_de_uso.executar()

    instituicao_atualizada = uow.repositorio_instituicoes.buscar_por_id(
        instituicao.id
    )
    assert instituicao_atualizada is not None
    assert instituicao_atualizada.senha.valor == "nova_senha456"
