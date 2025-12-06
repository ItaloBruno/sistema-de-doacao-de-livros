from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from sistema_de_doacao_de_livros import banco_de_dados
from sistema_de_doacao_de_livros.schemas import (
    LoginRequest,
    LoginResponse,
    TipoUsuario,
)

rotas_api_autenticacao = APIRouter()


@rotas_api_autenticacao.post("/login", response_model=LoginResponse)
def fazer_login(dados: LoginRequest):
    doador = banco_de_dados.buscar_doador_por_email(dados.email)
    if doador and doador.senha == dados.senha:
        return LoginResponse(
            usuario_id=doador.id,
            nome=doador.nome,
            email=doador.email,
            tipo=TipoUsuario.DOADOR,
            mensagem="Login realizado com sucesso",
        )

    instituicao = banco_de_dados.buscar_instituicao_por_email(dados.email)
    if instituicao and instituicao.senha == dados.senha:
        return LoginResponse(
            usuario_id=instituicao.id,
            nome=instituicao.nome,
            email=instituicao.email,
            tipo=TipoUsuario.INSTITUICAO,
            mensagem="Login realizado com sucesso",
        )

    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Email ou senha incorretos",
    )
