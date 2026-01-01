from dataclasses import dataclass


@dataclass
class EntradaCriarInstituicaoCasoDeUso:
    nome: str
    email: str
    senha: str
    telefone: str
    descricao: str
    data_fundacao: str
    endereco: str
    site: str | None = None
    foto: bytes | None = None
    nome_arquivo_foto: str | None = None


@dataclass
class SaidaCriarInstituicao:
    id: str
    nome: str
    email: str
    telefone: str
    descricao: str
    data_fundacao: str
    endereco: str
    site: str | None
    foto: str | None


@dataclass
class EntradaAtualizarInstituicaoCasoDeUso:
    instituicao_id: str
    nome: str
    email: str
    telefone: str
    senha_atual: str
    descricao: str
    data_fundacao: str
    endereco: str
    site: str | None = None
    foto: bytes | None = None
    nome_arquivo_foto: str | None = None
    nova_senha: str | None = None


@dataclass
class SaidaAtualizarInstituicao:
    id: str
    nome: str
    email: str
    telefone: str
    descricao: str
    data_fundacao: str
    endereco: str
    site: str | None
    foto: str | None
