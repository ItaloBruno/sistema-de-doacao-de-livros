from http import HTTPStatus
from typing import Annotated, Final

from fastapi import APIRouter, Depends

from contextos_de_negocio.doacao.casos_de_uso.criar_doacao import CriarDoacao
from contextos_de_negocio.doacao.casos_de_uso.dtos import (
    EntradaCriarDoacaoCasoDeUso,
)
from contextos_de_negocio.doacao.pontos_de_entrada.esquemas import (
    EntradaCriarDoacao,
    RespostaCriarDoacao,
)
from contextos_de_negocio.doador.dominio.objetos_de_valor import DoadorId
from utilitarios.fastapi.autenticacao import obter_usuario_autenticado
from utilitarios.unidade_de_trabalho import unidade_de_trabalho

api_doacao: Final[APIRouter] = APIRouter(tags=["Doação"])


@api_doacao.post(
    "/doacoes",
    status_code=HTTPStatus.CREATED,
    response_model=RespostaCriarDoacao,
)
def criar_doacao(
    corpo_da_requisicao: EntradaCriarDoacao,
    usuario_autenticado: Annotated[
        DoadorId, Depends(obter_usuario_autenticado)
    ],
):
    entrada = EntradaCriarDoacaoCasoDeUso(
        instituicao_id=corpo_da_requisicao.instituicao_id,
        livros_ids=corpo_da_requisicao.livros_ids,
    )

    caso_de_uso = CriarDoacao(
        entrada=entrada,
        doador_id=usuario_autenticado,
        obter_uow=unidade_de_trabalho,
    )
    saida = caso_de_uso.executar()

    return RespostaCriarDoacao(
        id=saida.id,
        doador_id=saida.doador_id,
        instituicao_id=saida.instituicao_id,
        livros_ids=saida.livros_ids,
    )
