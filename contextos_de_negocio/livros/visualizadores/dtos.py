from dataclasses import dataclass


@dataclass
class ItemLivro:
    id: str | None = None
    titulo: str | None = None
    autores: list | None = None
    subtitulo: str | None = None
    isbn: str | None = None
    observacao: str | None = None
    foto: str | None = None
