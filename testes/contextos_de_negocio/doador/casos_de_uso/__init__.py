from contextos_de_negocio.doador.dominio.entidades import Doador
from contextos_de_negocio.doador.dominio.objetos_de_valor import DoadorId
from contextos_de_negocio.doador.repositorio import RepositorioDoadoresAbstrato
from utilitarios.objetos_de_valor.resultado_paginado import (
    ResultadoPaginado,
)
from utilitarios.unidade_de_trabalho import (
    UnidadeDeTrabalhoAbstrata,
)


class RepositorioDoadoresFake(RepositorioDoadoresAbstrato):
    def __init__(self):
        self._doadores: dict[DoadorId, Doador] = {}
        self._doadores_por_email: dict[str, Doador] = {}

    def buscar_por_email(self, email: str) -> Doador | None:
        return self._doadores_por_email.get(email)

    def buscar_por_id(self, doador_id) -> Doador | None:
        return self._doadores.get(doador_id)

    def adicionar(self, doador: Doador) -> Doador:
        if doador.id is None:
            doador.id = DoadorId.gerar()

        self._doadores[doador.id] = doador
        self._doadores_por_email[doador.email.valor] = doador
        return doador

    def listar_com_filtros(
        self, filtros, pagina, itens_por_pagina, ordem, campos
    ):
        todos_doadores = list(self._doadores.values())
        doadores_como_dicionarios = self._converter_doadores_para_dicionarios(
            todos_doadores
        )

        offset = (pagina.valor - 1) * itens_por_pagina.valor
        doadores_paginados = doadores_como_dicionarios[
            offset : offset + itens_por_pagina.valor
        ]

        return ResultadoPaginado(
            itens=doadores_paginados,
            total=len(doadores_como_dicionarios),
            pagina=pagina.valor,
            itens_por_pagina=itens_por_pagina.valor,
        )

    def _converter_doadores_para_dicionarios(self, doadores):
        doadores_como_dicionarios = []

        for doador in doadores:
            doador_dicionario = {
                "id": doador.id,
                "nome": doador.nome,
                "email": doador.email,
                "telefone": doador.telefone,
            }
            doadores_como_dicionarios.append(doador_dicionario)

        return doadores_como_dicionarios


class UnidadeDeTrabalhoFake(UnidadeDeTrabalhoAbstrata):
    def __init__(self):
        self.repositorio_doadores = RepositorioDoadoresFake()
        self._committed = False
        self._rolled_back = False

    def commit(self):
        self._committed = True

    def rollback(self):
        self._rolled_back = False

    def __enter__(self):
        return self

    def __exit__(self, tipo_excecao, valor_excecao, traceback_excecao):
        if tipo_excecao is not None:
            self.rollback()


def obter_uow_fake():
    return UnidadeDeTrabalhoFake()
