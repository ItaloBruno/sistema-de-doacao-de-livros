from collections.abc import Callable
from uuid import UUID

from contextos_de_negocio.doador.casos_de_uso.dtos import (
    EntradaAtualizarDoadorCasoDeUso,
    SaidaAtualizarDoador,
)
from contextos_de_negocio.doador.dominio.entidades import Doador
from contextos_de_negocio.doador.dominio.objetos_de_valor import (
    DoadorId,
    EmailDoador,
    NomeDoador,
    SenhaDoador,
    TelefoneDoador,
)
from contextos_de_negocio.doador.excecoes import (
    DoadorNaoEncontrado,
    EmailJaCadastrado,
)
from utilitarios.unidade_de_trabalho import (
    UnidadeDeTrabalhoAbstrata,
)


class AtualizarDoador:
    def __init__(
        self,
        entrada: EntradaAtualizarDoadorCasoDeUso,
        obter_uow: Callable[[], UnidadeDeTrabalhoAbstrata],
    ):
        self.entrada = entrada
        self.obter_uow = obter_uow

    def executar(self) -> SaidaAtualizarDoador:
        with self.obter_uow() as uow:
            doador = uow.repositorio_doadores.buscar_por_id(
                DoadorId(UUID(self.entrada.doador_id))
            )
            if not doador:
                raise DoadorNaoEncontrado()

            self._validar_email_disponivel(uow, doador)

            doador.editar(
                senha_atual=SenhaDoador(self.entrada.senha_atual),
                nome=NomeDoador(self.entrada.nome),
                email=EmailDoador(self.entrada.email),
                telefone=TelefoneDoador(self.entrada.telefone),
                nova_senha=SenhaDoador(self.entrada.nova_senha)
                if self.entrada.nova_senha
                else None,
            )

            doador_atualizado = uow.repositorio_doadores.adicionar(doador)
            uow.commit()

            return SaidaAtualizarDoador(
                id=str(doador_atualizado.id),
                nome=doador_atualizado.nome.valor,
                email=doador_atualizado.email.valor,
                telefone=doador_atualizado.telefone.valor,
            )

    def _validar_email_disponivel(
        self, uow: UnidadeDeTrabalhoAbstrata, doador: Doador
    ) -> None:
        if self.entrada.email != doador.email.valor:
            doador_existente = uow.repositorio_doadores.buscar_por_email(
                self.entrada.email
            )
            if doador_existente:
                raise EmailJaCadastrado()
