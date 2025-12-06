from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Query

from sistema_de_doacao_de_livros import banco_de_dados
from sistema_de_doacao_de_livros.schemas import (
    CriacaoDeInstituicao,
    Instituicao,
    InstituicaoDB,
    ListagemDeInstituicoes,
)

rotas_api_instituicoes = APIRouter()


@rotas_api_instituicoes.post(
    "/instituicoes", status_code=HTTPStatus.CREATED, response_model=Instituicao
)
def criar_instituicao(dados: CriacaoDeInstituicao):
    if banco_de_dados.buscar_instituicao_por_email(dados.email):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Email já cadastrado",
        )

    if banco_de_dados.buscar_doador_por_email(dados.email):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Email já cadastrado como doador",
        )

    instituicao_db = InstituicaoDB(
        **dados.model_dump(),
        id=len(banco_de_dados.instituicoes) + 1,
        data_registro=datetime.now(),
        livros_recebidos=0,
    )

    banco_de_dados.instituicoes.append(instituicao_db)

    return Instituicao(
        id=instituicao_db.id,
        nome=instituicao_db.nome,
        email=instituicao_db.email,
        descricao=instituicao_db.descricao,
        data_fundacao=instituicao_db.data_fundacao,
        data_registro=instituicao_db.data_registro,
        livros_recebidos=instituicao_db.livros_recebidos,
        foto_url=instituicao_db.foto_url,
        site=instituicao_db.site,
        endereco=instituicao_db.endereco,
    )


@rotas_api_instituicoes.get(
    "/instituicoes", response_model=ListagemDeInstituicoes
)
def listar_instituicoes(
    pagina: int = Query(1, ge=1),
    tamanho_pagina: int = Query(10, ge=1, le=50),
):
    total = len(banco_de_dados.instituicoes)
    inicio = (pagina - 1) * tamanho_pagina
    fim = inicio + tamanho_pagina

    instituicoes_pagina = banco_de_dados.instituicoes[inicio:fim]

    instituicoes_lista = [
        Instituicao(
            id=inst.id,
            nome=inst.nome,
            email=inst.email,
            descricao=inst.descricao,
            data_fundacao=inst.data_fundacao,
            data_registro=inst.data_registro,
            livros_recebidos=inst.livros_recebidos,
            foto_url=inst.foto_url,
            site=inst.site,
            endereco=inst.endereco,
        )
        for inst in instituicoes_pagina
    ]

    return ListagemDeInstituicoes(
        instituicoes=instituicoes_lista,
        total=total,
        pagina=pagina,
        tamanho_pagina=tamanho_pagina,
    )


@rotas_api_instituicoes.get(
    "/instituicoes/{instituicao_id}", response_model=Instituicao
)
def buscar_instituicao(instituicao_id: int):
    instituicao = banco_de_dados.buscar_instituicao_por_id(instituicao_id)
    if not instituicao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Instituição não encontrada",
        )

    return Instituicao(
        id=instituicao.id,
        nome=instituicao.nome,
        email=instituicao.email,
        descricao=instituicao.descricao,
        data_fundacao=instituicao.data_fundacao,
        data_registro=instituicao.data_registro,
        livros_recebidos=instituicao.livros_recebidos,
        foto_url=instituicao.foto_url,
        site=instituicao.site,
        endereco=instituicao.endereco,
    )
