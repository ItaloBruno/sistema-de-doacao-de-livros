from .autenticacao import rotas_autenticacao
from .avaliacao import rotas_solicitacoes
from .doacao import rotas_doacao
from .doador import rotas_doador
from .inicio import rotas_inicio
from .instituicoes import rotas_instituicoes

__all__ = [
    "rotas_inicio",
    "rotas_instituicoes",
    "rotas_autenticacao",
    "rotas_doacao",
    "rotas_doador",
    "rotas_solicitacoes",
]
