from http import HTTPStatus
from typing import Annotated, Final

from fastapi import APIRouter, Depends

from contextos_de_negocio.doador.casos_de_uso.atualizar_doador import (
    AtualizarDoador,
    EntradaAtualizarDoadorCasoDeUso,
)
from contextos_de_negocio.doador.casos_de_uso.criar_doador import (
    CriarDoador,
    EntradaCriarDoadorCasoDeUso,
)
from contextos_de_negocio.doador.dominio.objetos_de_valor import DoadorId
from contextos_de_negocio.doador.pontos_de_entrada.esquemas import (
    EntradaAtualizarDoador,
    EntradaCriarDoador,
    ItemDoadorResposta,
    RespostaAtualizarDoador,
    RespostaBuscarDoador,
    RespostaCriarDoador,
    RespostaListarDoadores,
)
from contextos_de_negocio.doador.pontos_de_entrada.parametros import (
    ParametrosListagemDoadores,
)
from contextos_de_negocio.doador.visualizadores.buscar import Buscar
from contextos_de_negocio.doador.visualizadores.listar import Listar
from utilitarios.fastapi.autenticacao import obter_usuario_autenticado
from utilitarios.provedor_de_hash import ProvedorDeHash
from utilitarios.provedor_de_hash.argon2 import EstrategiaArgon2
from utilitarios.unidade_de_trabalho import unidade_de_trabalho
from utilitarios.visualizadores.dtos import ParametrosListagem

api_doador: Final[APIRouter] = APIRouter(tags=["Doador"])


@api_doador.get(
    "/doadores",
    status_code=HTTPStatus.OK,
    response_model=RespostaListarDoadores,
)
def listar_doadores(
    parametros: ParametrosListagemDoadores = Depends(),
):
    visualizador = Listar(obter_uow=unidade_de_trabalho)
    resultado = visualizador.executar(
        ParametrosListagem(
            filtros_dict=parametros.obter_filtros_dict(),
            pagina=parametros.pagina,
            itens_por_pagina=parametros.itens_por_pagina,
            ordem=parametros.ordem,
            campos=parametros.campos,
        )
    )

    return RespostaListarDoadores(
        itens=[
            ItemDoadorResposta(
                id=item.id,
                nome=item.nome,
                email=item.email,
                telefone=item.telefone,
            )
            for item in resultado.itens
        ],
        total=resultado.total,
        pagina=resultado.pagina,
        itens_por_pagina=resultado.itens_por_pagina,
        total_paginas=resultado.total_paginas,
    )


@api_doador.get(
    "/doadores/{doador_id}",
    response_model=RespostaBuscarDoador,
)
def buscar_doador(
    doador_id: str,
    usuario_autenticado: Annotated[
        DoadorId, Depends(obter_usuario_autenticado)
    ],
):
    visualizador = Buscar(obter_uow=unidade_de_trabalho)
    item = visualizador.executar(doador_id)

    return RespostaBuscarDoador(
        id=item.id,
        nome=item.nome,
        email=item.email,
        telefone=item.telefone,
    )


@api_doador.put(
    "/doadores/{doador_id}",
    response_model=RespostaAtualizarDoador,
)
def atualizar_doador(
    doador_id: str,
    corpo_da_requisicao: EntradaAtualizarDoador,
    usuario_autenticado: Annotated[
        DoadorId, Depends(obter_usuario_autenticado)
    ],
):
    entrada = EntradaAtualizarDoadorCasoDeUso(
        doador_id=doador_id,
        nome=corpo_da_requisicao.nome,
        email=str(corpo_da_requisicao.email),
        telefone=corpo_da_requisicao.telefone,
        senha_atual=corpo_da_requisicao.senha_atual,
        nova_senha=corpo_da_requisicao.nova_senha,
    )

    caso_de_uso = AtualizarDoador(
        entrada=entrada,
        obter_uow=unidade_de_trabalho,
    )
    saida = caso_de_uso.executar()

    return RespostaAtualizarDoador(
        id=saida.id,
        nome=saida.nome,
        email=saida.email,
        telefone=saida.telefone,
    )


@api_doador.post(
    "/doadores",
    status_code=HTTPStatus.CREATED,
    response_model=RespostaCriarDoador,
)
def criar_doador(corpo_da_requisicao: EntradaCriarDoador):
    entrada = EntradaCriarDoadorCasoDeUso(
        nome=corpo_da_requisicao.nome,
        email=str(corpo_da_requisicao.email),
        senha=corpo_da_requisicao.senha,
        telefone=corpo_da_requisicao.telefone,
    )

    caso_de_uso = CriarDoador(
        entrada=entrada,
        obter_uow=unidade_de_trabalho,
        provedor_de_hash=ProvedorDeHash(EstrategiaArgon2()),
    )
    saida = caso_de_uso.executar()

    return RespostaCriarDoador(
        id=saida.id,
        nome=saida.nome,
        email=saida.email,
        telefone=saida.telefone,
    )
