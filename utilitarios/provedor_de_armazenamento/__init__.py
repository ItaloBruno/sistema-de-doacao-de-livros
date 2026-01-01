from utilitarios.provedor_de_armazenamento.estrategia_de_armazenamento import (
    EstrategiaDeArmazenamento,
)


class ProvedorDeArmazenamento:
    def __init__(self, estrategia: EstrategiaDeArmazenamento):
        self.estrategia = estrategia

    def fazer_upload(self, conteudo: bytes, nome_arquivo: str) -> str:
        return self.estrategia.fazer_upload(conteudo, nome_arquivo)

    def fazer_download(self, caminho: str) -> bytes:
        return self.estrategia.fazer_download(caminho)
