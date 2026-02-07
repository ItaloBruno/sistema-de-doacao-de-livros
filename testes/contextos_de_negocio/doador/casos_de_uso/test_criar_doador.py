import pytest

from contextos_de_negocio.doador.casos_de_uso.criar_doador import CriarDoador
from contextos_de_negocio.doador.casos_de_uso.dtos import (
    EntradaCriarDoadorCasoDeUso,
)
from contextos_de_negocio.doador.excecoes import EmailJaCadastrado
from testes.contextos_de_negocio.doador.casos_de_uso import (
    UnidadeDeTrabalhoFake,
    obter_uow_fake,
)
from utilitarios.provedor_de_hash import EstrategiaDeHash, ProvedorDeHash


class EstrategiaDeHashFake(EstrategiaDeHash):
    def gerar_hash(self, valor: str) -> str:
        return f"hash_{valor}"

    def verificar_hash(self, valor: str, hash_gerado: str) -> bool:
        return hash_gerado == f"hash_{valor}"


provedor_de_hash_fake = ProvedorDeHash(EstrategiaDeHashFake())


def test_deve_criar_doador_com_sucesso(obter_mock_doador):
    doador = obter_mock_doador()
    entrada = EntradaCriarDoadorCasoDeUso(
        nome=doador.nome.valor,
        email=doador.email.valor,
        senha=doador.senha.valor,
        telefone=doador.telefone.valor,
    )

    caso_de_uso = CriarDoador(entrada, obter_uow_fake, provedor_de_hash_fake)
    saida = caso_de_uso.executar()

    assert saida.nome == doador.nome.valor
    assert saida.email == doador.email.valor
    assert saida.telefone == doador.telefone.valor


def test_deve_lancar_excecao_quando_email_ja_cadastrado(obter_mock_doador):
    uow = UnidadeDeTrabalhoFake()
    doador_existente = obter_mock_doador(email="maria@example.com")
    uow.repositorio_doadores.adicionar(doador_existente)

    def obter_uow_com_doador_existente():
        return uow

    entrada = EntradaCriarDoadorCasoDeUso(
        nome="João Silva",
        email="maria@example.com",
        senha="senha123",
        telefone="11999999999",
    )
    caso_de_uso = CriarDoador(
        entrada, obter_uow_com_doador_existente, provedor_de_hash_fake
    )

    with pytest.raises(EmailJaCadastrado):
        caso_de_uso.executar()
