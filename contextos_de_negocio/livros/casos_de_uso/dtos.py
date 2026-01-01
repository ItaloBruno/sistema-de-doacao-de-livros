from dataclasses import dataclass


@dataclass
class EntradaCriarLivroCasoDeUso:
    titulo: str
    autores: list[str]
    subtitulo: str | None
    isbn: str | None
    observacao: str | None
    foto: bytes | None = None
    nome_arquivo_foto: str | None = None


@dataclass
class SaidaCriarLivro:
    id: str
    titulo: str
    autores: list[str]
    subtitulo: str | None
    isbn: str | None
    observacao: str | None
    foto: str | None


@dataclass
class EntradaAtualizarLivroCasoDeUso:
    livro_id: str
    titulo: str
    autores: list[str]
    subtitulo: str | None
    isbn: str | None
    observacao: str | None
    foto: bytes | None = None
    nome_arquivo_foto: str | None = None


@dataclass
class SaidaAtualizarLivro:
    id: str
    titulo: str
    autores: list[str]
    subtitulo: str | None
    isbn: str | None
    observacao: str | None
    foto: str | None


@dataclass
class EntradaDeletarLivroCasoDeUso:
    livro_id: str
