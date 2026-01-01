from collections.abc import Callable

from contextos_de_negocio.autenticacao.casos_de_uso.dtos import (
    EntradaFazerLoginCasoDeUso,
    SaidaFazerLogin,
)
from contextos_de_negocio.autenticacao.excecoes import CredenciaisInvalidas
from utilitarios.provedor_de_hash import ProvedorDeHash
from utilitarios.provedor_de_token import ProvedorDeToken
from utilitarios.unidade_de_trabalho import UnidadeDeTrabalhoAbstrata


class FazerLogin:
    def __init__(
        self,
        entrada: EntradaFazerLoginCasoDeUso,
        obter_uow: Callable[[], UnidadeDeTrabalhoAbstrata],
        provedor_de_hash: ProvedorDeHash,
        provedor_de_token: ProvedorDeToken,
    ):
        self.entrada = entrada
        self.obter_uow = obter_uow
        self.provedor_de_hash = provedor_de_hash
        self.provedor_de_token = provedor_de_token

    def executar(self) -> SaidaFazerLogin:
        with self.obter_uow() as uow:
            doador = uow.repositorio_doadores.buscar_por_email(
                self.entrada.email
            )

            if not doador:
                raise CredenciaisInvalidas()

            if not self.provedor_de_hash.verificar_hash(
                self.entrada.senha, doador.senha.valor
            ):
                raise CredenciaisInvalidas()

            if not doador.id:
                raise CredenciaisInvalidas()

            token_de_acesso = self.provedor_de_token.gerar_token_de_acesso(
                doador.id
            )
            token_de_renovacao = (
                self.provedor_de_token.gerar_token_de_renovacao(doador.id)
            )

            return SaidaFazerLogin(
                id=str(doador.id),
                nome=doador.nome.valor,
                email=doador.email.valor,
                telefone=doador.telefone.valor,
                token_de_acesso=str(token_de_acesso),
                token_de_renovacao=str(token_de_renovacao),
            )
