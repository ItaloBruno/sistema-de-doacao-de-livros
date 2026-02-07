import pytest

from contextos_de_negocio.instituicao.casos_de_uso.criar_instituicao import (
    CriarInstituicao,
)
from contextos_de_negocio.instituicao.casos_de_uso.dtos import (
    EntradaCriarInstituicaoCasoDeUso,
)
from contextos_de_negocio.instituicao.excecoes import EmailJaCadastrado
from testes.contextos_de_negocio.instituicao.casos_de_uso import (
    UnidadeDeTrabalhoFake,
    obter_uow_fake,
)
from utilitarios.provedor_de_armazenamento import ProvedorDeArmazenamento
from utilitarios.provedor_de_armazenamento.armazenamento_local import (
    EstrategiaArmazenamentoLocal,
)
from utilitarios.provedor_de_hash import EstrategiaDeHash, ProvedorDeHash


class EstrategiaDeHashFake(EstrategiaDeHash):
    def gerar_hash(self, valor: str) -> str:
        return f"hash_{valor}"

    def verificar_hash(self, valor: str, hash_gerado: str) -> bool:
        return hash_gerado == f"hash_{valor}"


provedor_de_hash_fake = ProvedorDeHash(EstrategiaDeHashFake())
provedor_de_armazenamento_fake = ProvedorDeArmazenamento(
    EstrategiaArmazenamentoLocal()
)


def test_deve_criar_instituicao_com_sucesso(obter_mock_instituicao):
    instituicao = obter_mock_instituicao()
    entrada = EntradaCriarInstituicaoCasoDeUso(
        nome=instituicao.nome.valor,
        email=instituicao.email.valor,
        senha=instituicao.senha.valor,
        telefone=instituicao.telefone.valor,
        descricao=instituicao.descricao.valor,
        data_fundacao=str(instituicao.data_fundacao.valor),
        endereco=instituicao.endereco.valor,
        site=instituicao.site.valor if instituicao.site else None,
        foto=None,
        nome_arquivo_foto=None,
    )

    caso_de_uso = CriarInstituicao(
        entrada,
        obter_uow_fake,
        provedor_de_hash_fake,
        provedor_de_armazenamento_fake,
    )
    saida = caso_de_uso.executar()

    assert saida.nome == instituicao.nome.valor
    assert saida.email == instituicao.email.valor
    assert saida.telefone == instituicao.telefone.valor
    assert saida.descricao == instituicao.descricao.valor
    assert saida.endereco == instituicao.endereco.valor


def test_deve_lancar_excecao_quando_email_ja_cadastrado(
    obter_mock_instituicao,
):
    uow = UnidadeDeTrabalhoFake()
    instituicao_existente = obter_mock_instituicao(email="contato@exemplo.org")
    uow.repositorio_instituicoes.adicionar(instituicao_existente)

    def obter_uow_com_instituicao_existente():
        return uow

    entrada = EntradaCriarInstituicaoCasoDeUso(
        nome="Nova Instituição",
        email="contato@exemplo.org",
        senha="senha123",
        telefone="11999999999",
        descricao="Descrição da nova instituição",
        data_fundacao="2021-01-01",
        endereco="Rua Nova, 456",
        site=None,
        foto=None,
        nome_arquivo_foto=None,
    )
    caso_de_uso = CriarInstituicao(
        entrada,
        obter_uow_com_instituicao_existente,
        provedor_de_hash_fake,
        provedor_de_armazenamento_fake,
    )

    with pytest.raises(EmailJaCadastrado):
        caso_de_uso.executar()
