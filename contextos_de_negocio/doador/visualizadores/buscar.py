from collections.abc import Callable
from uuid import UUID

from contextos_de_negocio.doador.dominio.objetos_de_valor import DoadorId
from contextos_de_negocio.doador.excecoes import DoadorNaoEncontrado
from contextos_de_negocio.doador.visualizadores.dtos import ItemDoador
from utilitarios.unidade_de_trabalho import UnidadeDeTrabalhoAbstrata


class Buscar:
    def __init__(self, obter_uow: Callable[[], UnidadeDeTrabalhoAbstrata]):
        self.obter_uow = obter_uow

    def executar(self, doador_id: str) -> ItemDoador:
        with self.obter_uow() as uow:
            doador = uow.repositorio_doadores.buscar_por_id(
                DoadorId(UUID(doador_id))
            )
            if not doador:
                raise DoadorNaoEncontrado()

            return ItemDoador(
                id=str(doador.id),
                nome=doador.nome.valor,
                email=doador.email.valor,
                telefone=doador.telefone.valor,
            )
