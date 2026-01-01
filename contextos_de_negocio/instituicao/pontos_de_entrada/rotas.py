from http import HTTPStatus
from typing import Annotated, Final
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile

from contextos_de_negocio.instituicao import casos_de_uso
from contextos_de_negocio.instituicao.casos_de_uso.dtos import (
    EntradaAtualizarInstituicaoCasoDeUso,
    EntradaCriarInstituicaoCasoDeUso,
)
from contextos_de_negocio.instituicao.dominio.objetos_de_valor import (
    InstituicaoId,
)
from contextos_de_negocio.instituicao.excecoes import InstituicaoNaoEncontrada
from contextos_de_negocio.instituicao.pontos_de_entrada.esquemas import (
    RespostaAtualizarInstituicao,
    RespostaBuscarInstituicao,
    RespostaCriarInstituicao,
)
from utilitarios.fastapi.autenticacao import obter_usuario_autenticado
from utilitarios.provedor_de_armazenamento import ProvedorDeArmazenamento
from utilitarios.provedor_de_armazenamento.armazenamento_local import (
    EstrategiaArmazenamentoLocal,
)
from utilitarios.provedor_de_hash import ProvedorDeHash
from utilitarios.provedor_de_hash.argon2 import EstrategiaArgon2
from utilitarios.unidade_de_trabalho import unidade_de_trabalho

api_instituicao: Final[APIRouter] = APIRouter(tags=["Instituição"])


@api_instituicao.get(
    "/instituicoes/{instituicao_id}",
    response_model=RespostaBuscarInstituicao,
)
def buscar_instituicao(
    instituicao_id: str,
    usuario_autenticado: Annotated[
        InstituicaoId, Depends(obter_usuario_autenticado)
    ],
):
    with unidade_de_trabalho() as uow:
        instituicao = uow.repositorio_instituicoes.buscar_por_id(
            InstituicaoId(UUID(instituicao_id))
        )
        if not instituicao:
            raise InstituicaoNaoEncontrada()

        return RespostaBuscarInstituicao(
            id=str(instituicao.id),
            nome=instituicao.nome.valor,
            email=instituicao.email.valor,
            telefone=instituicao.telefone.valor,
            descricao=instituicao.descricao.valor,
            data_fundacao=str(instituicao.data_fundacao),
            endereco=instituicao.endereco.valor,
            site=instituicao.site.valor if instituicao.site else None,
            foto=instituicao.foto.valor if instituicao.foto else None,
        )


@api_instituicao.put(
    "/instituicoes/{instituicao_id}",
    response_model=RespostaAtualizarInstituicao,
)
def atualizar_instituicao(  # noqa: PLR0913
    instituicao_id: str,
    nome: Annotated[str, Form()],
    email: Annotated[str, Form()],
    telefone: Annotated[str, Form()],
    senha_atual: Annotated[str, Form()],
    descricao: Annotated[str, Form()],
    data_fundacao: Annotated[str, Form()],
    endereco: Annotated[str, Form()],
    usuario_autenticado: Annotated[
        InstituicaoId, Depends(obter_usuario_autenticado)
    ],
    site: Annotated[str | None, Form()] = None,
    nova_senha: Annotated[str | None, Form()] = None,
    foto: Annotated[UploadFile | None, File()] = None,
):
    entrada = EntradaAtualizarInstituicaoCasoDeUso(
        instituicao_id=instituicao_id,
        nome=nome,
        email=email,
        telefone=telefone,
        senha_atual=senha_atual,
        descricao=descricao,
        data_fundacao=data_fundacao,
        endereco=endereco,
        site=site,
        nova_senha=nova_senha,
        foto=foto.file.read() if foto else None,
        nome_arquivo_foto=foto.filename if foto else None,
    )

    caso_de_uso = casos_de_uso.atualizar_instituicao.AtualizarInstituicao(
        entrada=entrada,
        obter_uow=unidade_de_trabalho,
        provedor_de_armazenamento=ProvedorDeArmazenamento(
            EstrategiaArmazenamentoLocal()
        ),
    )
    saida = caso_de_uso.executar()

    return RespostaAtualizarInstituicao(
        id=saida.id,
        nome=saida.nome,
        email=saida.email,
        telefone=saida.telefone,
        descricao=saida.descricao,
        data_fundacao=saida.data_fundacao,
        endereco=saida.endereco,
        site=saida.site,
        foto=saida.foto,
    )


@api_instituicao.post(
    "/instituicoes",
    status_code=HTTPStatus.CREATED,
    response_model=RespostaCriarInstituicao,
)
def criar_instituicao(  # noqa: PLR0913
    nome: Annotated[str, Form()],
    email: Annotated[str, Form()],
    senha: Annotated[str, Form()],
    telefone: Annotated[str, Form()],
    descricao: Annotated[str, Form()],
    data_fundacao: Annotated[str, Form()],
    endereco: Annotated[str, Form()],
    site: Annotated[str | None, Form()] = None,
    foto: Annotated[UploadFile | None, File()] = None,
):
    entrada = EntradaCriarInstituicaoCasoDeUso(
        nome=nome,
        email=email,
        senha=senha,
        telefone=telefone,
        descricao=descricao,
        data_fundacao=data_fundacao,
        endereco=endereco,
        site=site,
        foto=foto.file.read() if foto else None,
        nome_arquivo_foto=foto.filename if foto else None,
    )

    caso_de_uso = casos_de_uso.criar_instituicao.CriarInstituicao(
        entrada=entrada,
        obter_uow=unidade_de_trabalho,
        provedor_de_hash=ProvedorDeHash(EstrategiaArgon2()),
        provedor_de_armazenamento=ProvedorDeArmazenamento(
            EstrategiaArmazenamentoLocal()
        ),
    )
    saida = caso_de_uso.executar()

    return RespostaCriarInstituicao(
        id=saida.id,
        nome=saida.nome,
        email=saida.email,
        telefone=saida.telefone,
        descricao=saida.descricao,
        data_fundacao=saida.data_fundacao,
        endereco=saida.endereco,
        site=saida.site,
        foto=saida.foto,
    )
