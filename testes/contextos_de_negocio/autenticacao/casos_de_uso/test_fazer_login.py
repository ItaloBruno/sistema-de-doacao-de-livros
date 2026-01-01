import pytest

from contextos_de_negocio.autenticacao.casos_de_uso.fazer_login import (
    EntradaFazerLoginCasoDeUso,
    FazerLogin,
)
from contextos_de_negocio.autenticacao.excecoes import CredenciaisInvalidas
from contextos_de_negocio.doador.dominio.objetos_de_valor import DoadorId
from testes.contextos_de_negocio.doador.casos_de_uso import (
    UnidadeDeTrabalhoFake,
    obter_uow_fake,
)
from utilitarios.objetos_de_valor.token import Token
from utilitarios.provedor_de_hash import EstrategiaDeHash, ProvedorDeHash
from utilitarios.provedor_de_token import ProvedorDeToken
from utilitarios.provedor_de_token.estrategia_de_token import EstrategiaDeToken


class EstrategiaDeHashFake(EstrategiaDeHash):
    def gerar_hash(self, valor: str) -> str:
        return f"hash_{valor}"

    def verificar_hash(self, valor: str, hash_gerado: str) -> bool:
        return hash_gerado == f"hash_{valor}"


class EstrategiaDeTokenFake(EstrategiaDeToken):
    def gerar_token_de_acesso(self, id_doador: DoadorId) -> Token:
        return Token(f"token_acesso_{id_doador}")

    def gerar_token_de_renovacao(self, id_doador: DoadorId) -> Token:
        return Token(f"token_renovacao_{id_doador}")

    def verificar_token_de_acesso(self, token: Token) -> DoadorId | None:
        return None

    def renovar_token_de_acesso(
        self, token_de_renovacao: Token
    ) -> Token | None:
        return None


provedor_de_hash_fake = ProvedorDeHash(EstrategiaDeHashFake())
provedor_de_token_fake = ProvedorDeToken(EstrategiaDeTokenFake())


def test_deve_fazer_login_com_sucesso(obter_mock_doador):
    uow = UnidadeDeTrabalhoFake()
    doador = obter_mock_doador(
        email="joao@example.com",
        senha="hash_senha123",
    )
    uow.repositorio_doadores.adicionar(doador)

    def obter_uow_com_doador():
        return uow

    entrada = EntradaFazerLoginCasoDeUso(
        email="joao@example.com",
        senha="senha123",
    )
    caso_de_uso = FazerLogin(
        entrada,
        obter_uow_com_doador,
        provedor_de_hash_fake,
        provedor_de_token_fake,
    )
    saida = caso_de_uso.executar()

    assert saida.id == str(doador.id)
    assert saida.nome == doador.nome.valor
    assert saida.email == doador.email.valor
    assert saida.telefone == doador.telefone.valor
    assert saida.token_de_acesso.startswith("token_acesso_")
    assert saida.token_de_renovacao.startswith("token_renovacao_")


def test_deve_lancar_excecao_quando_email_nao_existe():
    entrada = EntradaFazerLoginCasoDeUso(
        email="naoexiste@example.com",
        senha="senha123",
    )
    caso_de_uso = FazerLogin(
        entrada, obter_uow_fake, provedor_de_hash_fake, provedor_de_token_fake
    )

    with pytest.raises(CredenciaisInvalidas):
        caso_de_uso.executar()


def test_deve_lancar_excecao_quando_senha_incorreta(obter_mock_doador):
    uow = UnidadeDeTrabalhoFake()
    doador = obter_mock_doador(
        email="joao@example.com",
        senha="hash_senha123",
    )
    uow.repositorio_doadores.adicionar(doador)

    def obter_uow_com_doador():
        return uow

    entrada = EntradaFazerLoginCasoDeUso(
        email="joao@example.com",
        senha="senha_errada",
    )
    caso_de_uso = FazerLogin(
        entrada,
        obter_uow_com_doador,
        provedor_de_hash_fake,
        provedor_de_token_fake,
    )

    with pytest.raises(CredenciaisInvalidas):
        caso_de_uso.executar()
