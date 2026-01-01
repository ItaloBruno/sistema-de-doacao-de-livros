from contextos_de_negocio.livros.casos_de_uso.criar_livro import CriarLivro
from contextos_de_negocio.livros.casos_de_uso.dtos import (
    EntradaCriarLivroCasoDeUso,
)
from testes.contextos_de_negocio.livros.casos_de_uso import (
    obter_uow_fake,
)
from utilitarios.provedor_de_armazenamento import (
    EstrategiaDeArmazenamento,
    ProvedorDeArmazenamento,
)


class EstrategiaDeArmazenamentoFake(EstrategiaDeArmazenamento):
    def fazer_upload(self, conteudo: bytes, nome_arquivo: str) -> str:
        return f"/fake/path/{nome_arquivo}"

    def fazer_download(self, caminho: str) -> bytes:
        return b"fake file content"


provedor_de_armazenamento_fake = ProvedorDeArmazenamento(
    EstrategiaDeArmazenamentoFake()
)


def test_deve_criar_livro_com_sucesso(obter_mock_livro):
    livro = obter_mock_livro()
    entrada = EntradaCriarLivroCasoDeUso(
        titulo=livro.titulo.valor,
        autores=livro.autores.valor,
        subtitulo=livro.subtitulo.valor,
        isbn=livro.isbn.valor,
        observacao=livro.observacao.valor,
        foto=None,
        nome_arquivo_foto=None,
    )

    caso_de_uso = CriarLivro(
        entrada, obter_uow_fake, provedor_de_armazenamento_fake
    )
    saida = caso_de_uso.executar()

    assert saida.titulo == livro.titulo.valor
    assert saida.autores == livro.autores.valor
    assert saida.subtitulo == livro.subtitulo.valor
    assert saida.isbn == livro.isbn.valor
    assert saida.observacao == livro.observacao.valor
    assert saida.foto is None


def test_deve_criar_livro_com_foto(obter_mock_livro):
    livro = obter_mock_livro()
    foto_bytes = b"fake image bytes"
    nome_arquivo = "capa.jpg"

    entrada = EntradaCriarLivroCasoDeUso(
        titulo=livro.titulo.valor,
        autores=livro.autores.valor,
        subtitulo=livro.subtitulo.valor,
        isbn=livro.isbn.valor,
        observacao=livro.observacao.valor,
        foto=foto_bytes,
        nome_arquivo_foto=nome_arquivo,
    )

    caso_de_uso = CriarLivro(
        entrada, obter_uow_fake, provedor_de_armazenamento_fake
    )
    saida = caso_de_uso.executar()

    assert saida.titulo == livro.titulo.valor
    assert saida.autores == livro.autores.valor
    assert saida.foto == f"/fake/path/{nome_arquivo}"


def test_deve_criar_livro_sem_campos_opcionais():
    entrada = EntradaCriarLivroCasoDeUso(
        titulo="Clean Code",
        autores=["Robert C. Martin"],
        subtitulo=None,
        isbn=None,
        observacao=None,
        foto=None,
        nome_arquivo_foto=None,
    )

    caso_de_uso = CriarLivro(
        entrada, obter_uow_fake, provedor_de_armazenamento_fake
    )
    saida = caso_de_uso.executar()

    assert saida.titulo == "Clean Code"
    assert saida.autores == ["Robert C. Martin"]
    assert saida.subtitulo is None
    assert saida.isbn is None
    assert saida.observacao is None
    assert saida.foto is None
