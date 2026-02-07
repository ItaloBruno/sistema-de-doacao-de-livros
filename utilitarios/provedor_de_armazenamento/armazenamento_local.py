import uuid
from pathlib import Path

from utilitarios.provedor_de_armazenamento.estrategia_de_armazenamento import (
    EstrategiaDeArmazenamento,
)


class EstrategiaArmazenamentoLocal(EstrategiaDeArmazenamento):
    def __init__(
        self, diretorio_base: str = "/tmp/sistema-de-doacao-de-livros"
    ):
        self.diretorio_base = Path(diretorio_base)

    def fazer_upload(self, conteudo: bytes, nome_arquivo: str) -> str:
        self.diretorio_base.mkdir(parents=True, exist_ok=True)

        extensao = Path(nome_arquivo).suffix
        nome_unico = f"{uuid.uuid4()}{extensao}"
        caminho_arquivo = self.diretorio_base / nome_unico

        with open(caminho_arquivo, "wb") as f:
            f.write(conteudo)

        return str(caminho_arquivo)

    def fazer_download(self, caminho: str) -> bytes:
        caminho_arquivo = Path(caminho)

        if not caminho_arquivo.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

        with open(caminho_arquivo, "rb") as f:
            return f.read()
