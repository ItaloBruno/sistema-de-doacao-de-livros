from dataclasses import dataclass


@dataclass
class EntradaCriarDoadorCasoDeUso:
    nome: str
    email: str
    senha: str
    telefone: str


@dataclass
class SaidaCriarDoador:
    id: str
    nome: str
    email: str
    telefone: str


@dataclass
class EntradaAtualizarDoadorCasoDeUso:
    doador_id: str
    nome: str
    email: str
    telefone: str
    senha_atual: str
    nova_senha: str | None = None


@dataclass
class SaidaAtualizarDoador:
    id: str
    nome: str
    email: str
    telefone: str
