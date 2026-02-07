import pytest

from contextos_de_negocio.livros.casos_de_uso.atualizar_livro import (
    AtualizarLivro,
)
from contextos_de_negocio.livros.casos_de_uso.dtos import (
    EntradaAtualizarLivroCasoDeUso,
)
from contextos_de_negocio.livros.dominio.objetos_de_valor import LivroId
from contextos_de_negocio.livros.excecoes import LivroNaoEncontrado
from testes.contextos_de_negocio.livros.casos_de_uso import (
    UnidadeDeTrabalhoFake,
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


def test_deve_atualizar_livro_com_sucesso(obter_mock_livro):
    uow = UnidadeDeTrabalhoFake()
    livro = obter_mock_livro()
    uow.repositorio_livros.adicionar(livro)

    def obter_uow_com_livro():
        return uow

    entrada = EntradaAtualizarLivroCasoDeUso(
        livro_id=str(livro.id),
        titulo="Título Atualizado",
        autores=["Autor Atualizado"],
        subtitulo="Subtítulo Atualizado",
        isbn="978-9999999999",
        observacao="Observação Atualizada",
        foto=None,
        nome_arquivo_foto=None,
    )

    caso_de_uso = AtualizarLivro(
        entrada, obter_uow_com_livro, provedor_de_armazenamento_fake
    )
    saida = caso_de_uso.executar()

    assert saida.id == str(livro.id)
    assert saida.titulo == "Título Atualizado"
    assert saida.autores == ["Autor Atualizado"]
    assert saida.subtitulo == "Subtítulo Atualizado"
    assert saida.isbn == "978-9999999999"
    assert saida.observacao == "Observação Atualizada"


def test_deve_lancar_excecao_quando_livro_nao_encontrado(obter_mock_livro):
    livro = obter_mock_livro()
    entrada = EntradaAtualizarLivroCasoDeUso(
        livro_id=str(LivroId.gerar()),
        titulo=livro.titulo.valor,
        autores=livro.autores.valor,
        subtitulo=livro.subtitulo.valor,
        isbn=livro.isbn.valor,
        observacao=livro.observacao.valor,
        foto=None,
        nome_arquivo_foto=None,
    )
    caso_de_uso = AtualizarLivro(
        entrada, obter_uow_fake, provedor_de_armazenamento_fake
    )

    with pytest.raises(LivroNaoEncontrado):
        caso_de_uso.executar()


def test_deve_atualizar_livro_com_nova_foto(obter_mock_livro):
    uow = UnidadeDeTrabalhoFake()
    livro = obter_mock_livro()
    uow.repositorio_livros.adicionar(livro)

    def obter_uow_com_livro():
        return uow

    foto_bytes = b"nova foto bytes"
    nome_arquivo = "nova_capa.jpg"

    entrada = EntradaAtualizarLivroCasoDeUso(
        livro_id=str(livro.id),
        titulo=livro.titulo.valor,
        autores=livro.autores.valor,
        subtitulo=livro.subtitulo.valor,
        isbn=livro.isbn.valor,
        observacao=livro.observacao.valor,
        foto=foto_bytes,
        nome_arquivo_foto=nome_arquivo,
    )

    caso_de_uso = AtualizarLivro(
        entrada, obter_uow_com_livro, provedor_de_armazenamento_fake
    )
    saida = caso_de_uso.executar()

    assert saida.id == str(livro.id)
    assert saida.foto == f"/fake/path/{nome_arquivo}"


def test_deve_manter_foto_existente_quando_nao_enviar_nova(obter_mock_livro):
    uow = UnidadeDeTrabalhoFake()
    livro = obter_mock_livro(foto_url="/caminho/antigo/foto.jpg")
    uow.repositorio_livros.adicionar(livro)

    def obter_uow_com_livro():
        return uow

    entrada = EntradaAtualizarLivroCasoDeUso(
        livro_id=str(livro.id),
        titulo="Novo Título",
        autores=["Novo Autor"],
        subtitulo=livro.subtitulo.valor,
        isbn=livro.isbn.valor,
        observacao=livro.observacao.valor,
        foto=None,
        nome_arquivo_foto=None,
    )

    caso_de_uso = AtualizarLivro(
        entrada, obter_uow_com_livro, provedor_de_armazenamento_fake
    )
    saida = caso_de_uso.executar()

    assert saida.id == str(livro.id)
    assert saida.foto == "/caminho/antigo/foto.jpg"
