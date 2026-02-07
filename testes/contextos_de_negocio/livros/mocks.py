import pytest

from contextos_de_negocio.livros.dominio.entidades import Livro
from contextos_de_negocio.livros.dominio.objetos_de_valor import (
    AutoresLivro,
    FotoUrlLivro,
    IsbnLivro,
    LivroId,
    ObservacaoLivro,
    SubtituloLivro,
    TituloLivro,
)


@pytest.fixture
def obter_mock_livro():
    def _criar(id: LivroId | None = None, **kwargs):
        titulo = TituloLivro(kwargs.get("titulo", "O Senhor dos Anéis"))
        autores = AutoresLivro(kwargs.get("autores", ["J.R.R. Tolkien"]))
        subtitulo = SubtituloLivro(
            kwargs.get("subtitulo", "A Sociedade do Anel")
        )
        isbn = IsbnLivro(kwargs.get("isbn", "978-0544003415"))
        foto_url = FotoUrlLivro(kwargs.get("foto_url", None))
        observacao = ObservacaoLivro(
            kwargs.get("observacao", "Primeira edição")
        )

        if id is None:
            return Livro.criar(
                titulo=titulo,
                autores=autores,
                subtitulo=subtitulo,
                isbn=isbn,
                foto_url=foto_url,
                observacao=observacao,
            )

        return Livro(
            id=id,
            titulo=titulo,
            autores=autores,
            subtitulo=subtitulo,
            isbn=isbn,
            foto_url=foto_url,
            observacao=observacao,
        )

    return _criar


@pytest.fixture
def obter_mock_livro_no_banco(uow, obter_mock_livro):
    def _inserir(id: LivroId | None = None, **kwargs) -> Livro:
        livro = obter_mock_livro(id=id, **kwargs)

        livro_criado = uow.repositorio_livros.adicionar(livro)
        uow.commit()
        return livro_criado

    return _inserir
