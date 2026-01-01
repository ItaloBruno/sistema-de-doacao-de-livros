from dataclasses import dataclass

from utilitarios.sqlalchemy.identificador_uuid import IdentificadorUuid


@dataclass(frozen=True, slots=True)
class LivroId(IdentificadorUuid):
    pass


@dataclass(frozen=True, slots=True)
class TituloLivro:
    valor: str

    def __post_init__(self):
        if not self.valor or not self.valor.strip():
            raise ValueError("Título não pode ser vazio")


@dataclass(frozen=True, slots=True)
class SubtituloLivro:
    valor: str | None

    def __post_init__(self):
        if self.valor is not None and not self.valor.strip():
            raise ValueError("Subtítulo não pode ser vazio")


@dataclass(frozen=True, slots=True)
class AutoresLivro:
    valor: list[str]

    def __post_init__(self):
        if not self.valor or len(self.valor) == 0:
            raise ValueError("Livro deve ter pelo menos um autor")
        for autor in self.valor:
            if not autor or not autor.strip():
                raise ValueError("Nome de autor não pode ser vazio")


@dataclass(frozen=True, slots=True)
class IsbnLivro:
    valor: str | None

    def __post_init__(self):
        if self.valor is not None and not self.valor.strip():
            raise ValueError("ISBN não pode ser vazio")


@dataclass(frozen=True, slots=True)
class FotoUrlLivro:
    valor: str | None


@dataclass(frozen=True, slots=True)
class ObservacaoLivro:
    valor: str | None

    def __post_init__(self):
        if self.valor is not None and not self.valor.strip():
            raise ValueError("Observação não pode ser vazia")
