from abc import ABC, abstractmethod


class EstrategiaDeHash(ABC):
    @abstractmethod
    def gerar_hash(self, valor: str) -> str:
        pass

    @abstractmethod
    def verificar_hash(self, valor: str, hash_gerado: str) -> bool:
        pass
