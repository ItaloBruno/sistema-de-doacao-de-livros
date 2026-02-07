from abc import ABC, abstractmethod

from contextos_de_negocio.doador.dominio.objetos_de_valor import DoadorId
from utilitarios.objetos_de_valor.token import Token


class EstrategiaDeToken(ABC):
    @abstractmethod
    def gerar_token_de_acesso(self, id_doador: DoadorId) -> Token:
        pass

    @abstractmethod
    def gerar_token_de_renovacao(self, id_doador: DoadorId) -> Token:
        pass

    @abstractmethod
    def verificar_token_de_acesso(self, token: Token) -> DoadorId | None:
        pass

    @abstractmethod
    def renovar_token_de_acesso(
        self, token_de_renovacao: Token
    ) -> Token | None:
        pass
