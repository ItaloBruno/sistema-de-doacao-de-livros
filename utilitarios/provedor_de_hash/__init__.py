from utilitarios.provedor_de_hash.estrategia_de_hash import EstrategiaDeHash


class ProvedorDeHash:
    def __init__(self, estrategia: EstrategiaDeHash):
        self.estrategia = estrategia

    def gerar_hash(self, valor: str) -> str:
        return self.estrategia.gerar_hash(valor)

    def verificar_hash(self, valor: str, hash_gerado: str) -> bool:
        return self.estrategia.verificar_hash(valor, hash_gerado)
