from collections.abc import Callable

from contextos_de_negocio.doador.casos_de_uso.dtos import (
    EntradaCriarDoadorCasoDeUso,
    SaidaCriarDoador,
)
from contextos_de_negocio.doador.dominio.entidades import Doador
from contextos_de_negocio.doador.dominio.objetos_de_valor import (
    EmailDoador,
    NomeDoador,
    SenhaDoador,
    TelefoneDoador,
)
from contextos_de_negocio.doador.excecoes import EmailJaCadastrado
from utilitarios.provedor_de_hash import ProvedorDeHash
from utilitarios.unidade_de_trabalho import (
    UnidadeDeTrabalhoAbstrata,
)


class CriarDoador:
    def __init__(
        self,
        entrada: EntradaCriarDoadorCasoDeUso,
        obter_uow: Callable[[], UnidadeDeTrabalhoAbstrata],
        provedor_de_hash: ProvedorDeHash,
    ):
        self.entrada = entrada
        self.obter_uow = obter_uow
        self.provedor_de_hash = provedor_de_hash

    def executar(self) -> SaidaCriarDoador:
        with self.obter_uow() as uow:
            self._validar_email_disponivel(uow)

            senha_hash = self.provedor_de_hash.gerar_hash(self.entrada.senha)

            doador = Doador.criar(
                nome=NomeDoador(self.entrada.nome),
                email=EmailDoador(self.entrada.email),
                telefone=TelefoneDoador(self.entrada.telefone),
                senha=SenhaDoador(senha_hash),
            )

            doador_criado = uow.repositorio_doadores.adicionar(doador)
            uow.commit()

            return SaidaCriarDoador(
                id=str(doador_criado.id),
                nome=doador_criado.nome.valor,
                email=doador_criado.email.valor,
                telefone=doador_criado.telefone.valor,
            )

    def _validar_email_disponivel(
        self, uow: UnidadeDeTrabalhoAbstrata
    ) -> None:
        doador_existente = uow.repositorio_doadores.buscar_por_email(
            self.entrada.email
        )
        if doador_existente:
            raise EmailJaCadastrado()
