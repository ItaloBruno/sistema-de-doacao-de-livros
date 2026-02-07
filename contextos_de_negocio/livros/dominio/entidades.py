from dataclasses import dataclass

from contextos_de_negocio.livros.dominio.objetos_de_valor import (
    AutoresLivro,
    FotoUrlLivro,
    IsbnLivro,
    LivroId,
    ObservacaoLivro,
    SubtituloLivro,
    TituloLivro,
)


@dataclass
class Livro:
    id: LivroId
    titulo: TituloLivro
    autores: AutoresLivro
    subtitulo: SubtituloLivro
    isbn: IsbnLivro
    foto_url: FotoUrlLivro | None
    observacao: ObservacaoLivro

    @staticmethod
    def criar(
        titulo: TituloLivro,
        autores: AutoresLivro,
        subtitulo: SubtituloLivro,
        isbn: IsbnLivro,
        foto_url: FotoUrlLivro | None,
        observacao: ObservacaoLivro,
    ) -> "Livro":
        return Livro(
            id=LivroId.gerar(),
            titulo=titulo,
            autores=autores,
            subtitulo=subtitulo,
            isbn=isbn,
            foto_url=foto_url,
            observacao=observacao,
        )

    def editar(
        self,
        titulo: TituloLivro,
        autores: AutoresLivro,
        subtitulo: SubtituloLivro,
        isbn: IsbnLivro,
        foto_url: FotoUrlLivro | None,
        observacao: ObservacaoLivro,
    ) -> None:
        self.titulo = titulo
        self.autores = autores
        self.subtitulo = subtitulo
        self.isbn = isbn
        self.foto_url = foto_url
        self.observacao = observacao
