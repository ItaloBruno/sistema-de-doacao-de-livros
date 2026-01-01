from datetime import date

import pytest

from contextos_de_negocio.instituicao.dominio.entidades import Instituicao
from contextos_de_negocio.instituicao.dominio.objetos_de_valor import (
    DadosParaCriacaoInstituicao,
    DataFundacaoInstituicao,
    DescricaoInstituicao,
    EmailInstituicao,
    EnderecoInstituicao,
    FotoInstituicao,
    InstituicaoId,
    NomeInstituicao,
    SenhaInstituicao,
    SiteInstituicao,
    TelefoneInstituicao,
)


@pytest.fixture
def obter_mock_instituicao():
    def _criar(id: InstituicaoId | None = None, **kwargs):
        dados = DadosParaCriacaoInstituicao(
            nome=NomeInstituicao(kwargs.get("nome", "Instituição Exemplo")),
            email=EmailInstituicao(
                kwargs.get("email", "contato@instituicao.org")
            ),
            senha=SenhaInstituicao(kwargs.get("senha", "senha123")),
            telefone=TelefoneInstituicao(
                kwargs.get("telefone", "11999999999")
            ),
            descricao=DescricaoInstituicao(
                kwargs.get("descricao", "Descrição da instituição")
            ),
            data_fundacao=DataFundacaoInstituicao(
                kwargs.get("data_fundacao", date(2020, 1, 1))
            ),
            endereco=EnderecoInstituicao(
                kwargs.get("endereco", "Rua Exemplo, 123")
            ),
            site=SiteInstituicao(kwargs["site"])
            if "site" in kwargs and kwargs["site"]
            else None,
            foto=FotoInstituicao(kwargs["foto"])
            if "foto" in kwargs and kwargs["foto"]
            else None,
        )

        if id is None:
            return Instituicao.criar(dados)

        return Instituicao(
            id=id,
            nome=dados.nome,
            email=dados.email,
            senha=dados.senha,
            telefone=dados.telefone,
            descricao=dados.descricao,
            data_fundacao=dados.data_fundacao,
            endereco=dados.endereco,
            site=dados.site,
            foto=dados.foto,
        )

    return _criar


@pytest.fixture
def obter_mock_instituicao_no_banco(uow, obter_mock_instituicao):
    def _inserir(id: InstituicaoId | None = None, **kwargs) -> Instituicao:
        instituicao = obter_mock_instituicao(id=id, **kwargs)

        instituicao_criada = uow.repositorio_instituicoes.adicionar(
            instituicao
        )
        uow.commit()
        return instituicao_criada

    return _inserir
