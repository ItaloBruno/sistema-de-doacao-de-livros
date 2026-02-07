from dataclasses import dataclass

from utilitarios.objetos_de_valor.data_fundacao import DataFundacao
from utilitarios.objetos_de_valor.descricao import Descricao
from utilitarios.objetos_de_valor.email import Email
from utilitarios.objetos_de_valor.endereco import Endereco
from utilitarios.objetos_de_valor.nome import Nome
from utilitarios.objetos_de_valor.senha_hash import SenhaHash
from utilitarios.objetos_de_valor.site import Site
from utilitarios.objetos_de_valor.telefone import Telefone
from utilitarios.objetos_de_valor.url_arquivo_salvo import UrlArquivoSalvo
from utilitarios.sqlalchemy.identificador_uuid import IdentificadorUuid


@dataclass(frozen=True, slots=True)
class NomeInstituicao(Nome):
    pass


@dataclass(frozen=True, slots=True)
class EmailInstituicao(Email):
    pass


@dataclass(frozen=True, slots=True)
class TelefoneInstituicao(Telefone):
    pass


@dataclass(frozen=True, slots=True)
class SenhaInstituicao(SenhaHash):
    pass


@dataclass(frozen=True, slots=True)
class FotoInstituicao(UrlArquivoSalvo):
    pass


@dataclass(frozen=True, slots=True)
class DescricaoInstituicao(Descricao):
    pass


@dataclass(frozen=True, slots=True)
class EnderecoInstituicao(Endereco):
    pass


@dataclass(frozen=True, slots=True)
class SiteInstituicao(Site):
    pass


@dataclass(frozen=True, slots=True)
class DataFundacaoInstituicao(DataFundacao):
    pass


@dataclass(frozen=True, slots=True)
class InstituicaoId(IdentificadorUuid):
    pass


@dataclass(frozen=True, slots=True)
class DadosParaCriacaoInstituicao:
    nome: NomeInstituicao
    email: EmailInstituicao
    telefone: TelefoneInstituicao
    senha: SenhaInstituicao
    descricao: DescricaoInstituicao
    data_fundacao: DataFundacaoInstituicao
    endereco: EnderecoInstituicao
    site: SiteInstituicao | None = None
    foto: FotoInstituicao | None = None


@dataclass(frozen=True, slots=True)
class DadosParaEdicaoInstituicao:
    senha_atual: SenhaInstituicao
    nome: NomeInstituicao
    email: EmailInstituicao
    telefone: TelefoneInstituicao
    descricao: DescricaoInstituicao
    data_fundacao: DataFundacaoInstituicao
    endereco: EnderecoInstituicao
    site: SiteInstituicao | None = None
    foto: FotoInstituicao | None = None
    nova_senha: SenhaInstituicao | None = None
