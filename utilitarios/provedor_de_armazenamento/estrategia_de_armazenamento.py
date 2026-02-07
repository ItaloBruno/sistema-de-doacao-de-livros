from abc import ABC, abstractmethod


class EstrategiaDeArmazenamento(ABC):
    @abstractmethod
    def fazer_upload(self, conteudo: bytes, nome_arquivo: str) -> str:
        pass

    @abstractmethod
    def fazer_download(self, caminho: str) -> bytes:
        pass
