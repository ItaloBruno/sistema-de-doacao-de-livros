from http import HTTPStatus

from fastapi import APIRouter

from .schemas import (
    CriacaoDeInstituicaoSocial,
    InstituicaoSocialCriada,
    InstituicaoSocialSalvaNoBanco,
)

rotas_api_instituicao_social = APIRouter()

banco_de_dados: list[InstituicaoSocialSalvaNoBanco] = []


@rotas_api_instituicao_social.post(
    "/instituicao-social/",
    status_code=HTTPStatus.CREATED,
    response_model=InstituicaoSocialCriada,
)
def criar_instituicao_social(instituicao_social: CriacaoDeInstituicaoSocial):
    instituicao_social_com_id = InstituicaoSocialSalvaNoBanco(
        **instituicao_social.model_dump(), id=len(banco_de_dados) + 1
    )

    banco_de_dados.append(instituicao_social_com_id)

    return instituicao_social_com_id
