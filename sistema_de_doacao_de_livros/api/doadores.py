from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from sistema_de_doacao_de_livros import banco_de_dados
from sistema_de_doacao_de_livros.schemas import (
    AtualizacaoDeDoador,
    CriacaoDeDoador,
    Doador,
    DoadorDB,
)

rotas_api_doadores = APIRouter(tags=["Doadores"])


@rotas_api_doadores.post(
    "/doadores", status_code=HTTPStatus.CREATED, response_model=Doador
)
def criar_doador(dados: CriacaoDeDoador):
    if banco_de_dados.buscar_doador_por_email(dados.email):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Email já cadastrado",
        )

    if banco_de_dados.buscar_instituicao_por_email(dados.email):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Email já cadastrado como instituição",
        )

    doador_db = DoadorDB(
        **dados.model_dump(),
        id=len(banco_de_dados.doadores) + 1,
    )

    banco_de_dados.doadores.append(doador_db)

    return Doador(
        id=doador_db.id,
        nome=doador_db.nome,
        email=doador_db.email,
        telefone=doador_db.telefone,
    )


@rotas_api_doadores.get("/doadores/{doador_id}", response_model=Doador)
def buscar_doador(doador_id: int):
    doador = banco_de_dados.buscar_doador_por_id(doador_id)
    if not doador:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Doador não encontrado",
        )

    return Doador(
        id=doador.id,
        nome=doador.nome,
        email=doador.email,
        telefone=doador.telefone,
    )


@rotas_api_doadores.put("/doadores/{doador_id}", response_model=Doador)
def atualizar_doador(doador_id: int, dados: AtualizacaoDeDoador):
    doador = banco_de_dados.buscar_doador_por_id(doador_id)
    if not doador:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Doador não encontrado",
        )

    if doador.senha != dados.senha_atual:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Senha atual incorreta",
        )

    if dados.email != doador.email:
        doador_existente = banco_de_dados.buscar_doador_por_email(dados.email)
        if doador_existente:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Email já cadastrado",
            )

        instituicao_existente = banco_de_dados.buscar_instituicao_por_email(
            dados.email
        )
        if instituicao_existente:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Email já cadastrado como instituição",
            )

    doador_atualizado = banco_de_dados.atualizar_doador(
        doador_id=doador_id,
        nome=dados.nome,
        email=dados.email,
        telefone=dados.telefone,
        senha=dados.nova_senha,
    )

    return Doador(
        id=doador_atualizado.id,
        nome=doador_atualizado.nome,
        email=doador_atualizado.email,
        telefone=doador_atualizado.telefone,
    )
