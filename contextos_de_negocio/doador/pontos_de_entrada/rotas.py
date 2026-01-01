from http import HTTPStatus
from typing import Annotated, Final
from uuid import UUID

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
from contextos_de_negocio.doador.excecoes import DoadorNaoEncontrado
from contextos_de_negocio.doador.pontos_de_entrada.esquemas import (
    EntradaAtualizarDoador,
    EntradaCriarDoador,
    RespostaAtualizarDoador,
    RespostaBuscarDoador,
    RespostaCriarDoador,
)
from utilitarios.fastapi.autenticacao import obter_usuario_autenticado
from utilitarios.provedor_de_hash import ProvedorDeHash
from utilitarios.provedor_de_hash.argon2 import EstrategiaArgon2
from utilitarios.unidade_de_trabalho import unidade_de_trabalho

api_doador: Final[APIRouter] = APIRouter(tags=["Doador"])


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
    with unidade_de_trabalho() as uow:
        doador = uow.repositorio_doadores.buscar_por_id(
            DoadorId(UUID(doador_id))
        )
        if not doador:
            raise DoadorNaoEncontrado()

        return RespostaBuscarDoador(
            id=str(doador.id),
            nome=doador.nome.valor,
            email=doador.email.valor,
            telefone=doador.telefone.valor,
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
