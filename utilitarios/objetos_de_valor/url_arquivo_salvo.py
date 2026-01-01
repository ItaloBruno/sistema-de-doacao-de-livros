from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UrlArquivoSalvo:
    valor: str

    def __str__(self) -> str:
        return self.valor
