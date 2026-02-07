from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from utilitarios.provedor_de_hash.estrategia_de_hash import EstrategiaDeHash
from utilitarios.variaveis_de_ambiente import VariaveisDeAmbiente


class EstrategiaArgon2(EstrategiaDeHash):
    def __init__(self):
        self.chave_secreta = VariaveisDeAmbiente.CHAVE_SECRETA_HASH
        self.hasher = PasswordHasher()

    def gerar_hash(self, valor: str) -> str:
        valor_com_chave = f"{valor}{self.chave_secreta}"
        return self.hasher.hash(valor_com_chave)

    def verificar_hash(self, valor: str, hash_gerado: str) -> bool:
        valor_com_chave = f"{valor}{self.chave_secreta}"
        try:
            self.hasher.verify(hash_gerado, valor_com_chave)
            return True
        except VerifyMismatchError:
            return False
