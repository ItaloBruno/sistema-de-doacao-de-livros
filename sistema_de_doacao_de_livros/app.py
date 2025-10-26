from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from sistema_de_doacao_de_livros.schemas import (
    AtualizacaoDeUsuario,
    CriacaoDeUsuario,
    ListagemDeUsuario,
    RespostaDoSistema,
    UsuarioAtualizado,
    UsuarioCriado,
    UsuarioDB,
    UsuarioEspecifico,
)

app = FastAPI()
banco_de_dados = []


@app.get('/')
def pagina_inicial(response_model=RespostaDoSistema):
    return {'message': 'Olá Mundo!'}


@app.post(
    '/usuarios/', status_code=HTTPStatus.CREATED, response_model=UsuarioCriado
)
def criar_usuario(usuario: CriacaoDeUsuario):
    usuario_com_id = UsuarioDB(
        **usuario.model_dump(), id=len(banco_de_dados) + 1
    )

    banco_de_dados.append(usuario_com_id)

    return usuario_com_id


@app.get('/usuarios/', response_model=ListagemDeUsuario)
def buscar_usuarios():
    return {'usuarios': banco_de_dados}


@app.put('/usuarios/{id_do_usuario}', response_model=UsuarioAtualizado)
def atualizar_usuario(id_do_usuario: int, usuario: AtualizacaoDeUsuario):
    if id_do_usuario > len(banco_de_dados) or id_do_usuario < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    usuario_com_id = UsuarioDB(**usuario.model_dump(), id=id_do_usuario)
    banco_de_dados[id_do_usuario - 1] = usuario_com_id

    return usuario_com_id


@app.delete('/usuarios/{id_do_usuario}', response_model=RespostaDoSistema)
def deletar_usuario(id_do_usuario: int):
    if id_do_usuario > len(banco_de_dados) or id_do_usuario < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    del banco_de_dados[id_do_usuario - 1]

    return {'mensagem': 'Usuário deletado'}


@app.get('/usuarios/{id_do_usuario}', response_model=UsuarioEspecifico)
def buscar_usuario_especifico(id_do_usuario: int):
    if id_do_usuario > len(banco_de_dados) or id_do_usuario < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    usuario = banco_de_dados[id_do_usuario - 1]
    return usuario
