import pytest

from contextos_de_negocio.livros.excecoes import LivroNaoEncontrado
from contextos_de_negocio.livros.visualizadores.buscar import Buscar
from testes.contextos_de_negocio.livros.casos_de_uso import obter_uow_fake


def test_deve_retornar_livro_por_id_com_sucesso(obter_mock_livro):
    uow = obter_uow_fake()
    livro = obter_mock_livro()
    uow.repositorio_livros.adicionar(livro)

    def obter_uow_com_livro():
        return uow

    visualizador = Buscar(obter_uow=obter_uow_com_livro)
    resultado = visualizador.executar(str(livro.id))

    assert resultado.id == str(livro.id)
    assert resultado.titulo == livro.titulo.valor
    assert resultado.autores == livro.autores.valor
    assert resultado.subtitulo == livro.subtitulo.valor
    assert resultado.isbn == livro.isbn.valor
    assert resultado.observacao == livro.observacao.valor
    assert resultado.foto == livro.foto_url.valor if livro.foto_url else None


def test_deve_lancar_excecao_quando_livro_nao_existe():
    visualizador = Buscar(obter_uow=obter_uow_fake)

    with pytest.raises(LivroNaoEncontrado):
        visualizador.executar("00000000-0000-0000-0000-000000000000")
