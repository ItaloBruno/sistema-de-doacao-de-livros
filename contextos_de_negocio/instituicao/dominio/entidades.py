from dataclasses import dataclass

from contextos_de_negocio.instituicao.dominio.objetos_de_valor import (
    DadosParaCriacaoInstituicao,
    DadosParaEdicaoInstituicao,
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
from contextos_de_negocio.instituicao.excecoes import SenhaIncorreta


@dataclass
class Instituicao:
    nome: NomeInstituicao
    email: EmailInstituicao
    telefone: TelefoneInstituicao
    senha: SenhaInstituicao
    descricao: DescricaoInstituicao
    data_fundacao: DataFundacaoInstituicao
    endereco: EnderecoInstituicao
    site: SiteInstituicao | None = None
    foto: FotoInstituicao | None = None
    id: InstituicaoId | None = None

    @staticmethod
    def criar(dados: DadosParaCriacaoInstituicao) -> "Instituicao":
        return Instituicao(
            id=InstituicaoId.gerar(),
            nome=dados.nome,
            email=dados.email,
            telefone=dados.telefone,
            senha=dados.senha,
            descricao=dados.descricao,
            data_fundacao=dados.data_fundacao,
            endereco=dados.endereco,
            site=dados.site,
            foto=dados.foto,
        )

    def editar(self, dados: DadosParaEdicaoInstituicao) -> None:
        if self.senha != dados.senha_atual:
            raise SenhaIncorreta()

        self.nome = dados.nome
        self.email = dados.email
        self.telefone = dados.telefone
        self.descricao = dados.descricao
        self.data_fundacao = dados.data_fundacao
        self.endereco = dados.endereco
        self.site = dados.site
        self.foto = dados.foto

        if dados.nova_senha is not None:
            self.senha = dados.nova_senha
