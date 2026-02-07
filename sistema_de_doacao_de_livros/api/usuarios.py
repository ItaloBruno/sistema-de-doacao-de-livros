from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from .schemas import (
    AtualizacaoDeUsuario,
    CriacaoDeUsuario,
    ListagemDeUsuario,
    RespostaDoSistema,
    UsuarioAtualizado,
    UsuarioCriado,
    UsuarioDB,
    UsuarioEspecifico,
)

rotas_api_usuarios = APIRouter()

banco_de_dados: list[UsuarioDB] = []


@rotas_api_usuarios.post(
    "/usuarios/", status_code=HTTPStatus.CREATED, response_model=UsuarioCriado
)
def criar_usuario(usuario: CriacaoDeUsuario):
    usuario_com_id = UsuarioDB(
        **usuario.model_dump(), id=len(banco_de_dados) + 1
    )

    banco_de_dados.append(usuario_com_id)

    return usuario_com_id


@rotas_api_usuarios.get("/usuarios/", response_model=ListagemDeUsuario)
def buscar_usuarios():
    return {"usuarios": banco_de_dados}


@rotas_api_usuarios.put(
    "/usuarios/{id_do_usuario}", response_model=UsuarioAtualizado
)
def atualizar_usuario(id_do_usuario: int, usuario: AtualizacaoDeUsuario):
    if id_do_usuario > len(banco_de_dados) or id_do_usuario < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado"
        )

    usuario_com_id = UsuarioDB(**usuario.model_dump(), id=id_do_usuario)
    banco_de_dados[id_do_usuario - 1] = usuario_com_id

    return usuario_com_id


@rotas_api_usuarios.delete(
    "/usuarios/{id_do_usuario}", response_model=RespostaDoSistema
)
def deletar_usuario(id_do_usuario: int):
    if id_do_usuario > len(banco_de_dados) or id_do_usuario < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado"
        )

    del banco_de_dados[id_do_usuario - 1]

    return {"mensagem": "Usuário deletado"}


@rotas_api_usuarios.get(
    "/usuarios/{id_do_usuario}", response_model=UsuarioEspecifico
)
def buscar_usuario_especifico(id_do_usuario: int):
    if id_do_usuario > len(banco_de_dados) or id_do_usuario < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado"
        )

    usuario = banco_de_dados[id_do_usuario - 1]
    return usuario
