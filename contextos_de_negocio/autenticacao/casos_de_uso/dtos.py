from dataclasses import dataclass


@dataclass
class EntradaFazerLoginCasoDeUso:
    email: str
    senha: str


@dataclass
class SaidaFazerLogin:
    id: str
    nome: str
    email: str
    telefone: str
    token_de_acesso: str
    token_de_renovacao: str


@dataclass
class EntradaRenovarTokenCasoDeUso:
    token_de_renovacao: str


@dataclass
class SaidaRenovarToken:
    token_de_acesso: str
