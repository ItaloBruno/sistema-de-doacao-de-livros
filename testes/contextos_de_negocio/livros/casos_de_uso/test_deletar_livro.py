import pytest

from contextos_de_negocio.livros.casos_de_uso.deletar_livro import (
    DeletarLivro,
)
from contextos_de_negocio.livros.casos_de_uso.dtos import (
    EntradaDeletarLivroCasoDeUso,
)
from contextos_de_negocio.livros.dominio.objetos_de_valor import LivroId
from contextos_de_negocio.livros.excecoes import LivroNaoEncontrado
from testes.contextos_de_negocio.livros.casos_de_uso import (
    UnidadeDeTrabalhoFake,
    obter_uow_fake,
)


def test_deve_deletar_livro_com_sucesso(obter_mock_livro):
    uow = UnidadeDeTrabalhoFake()
    livro = obter_mock_livro()
    uow.repositorio_livros.adicionar(livro)

    def obter_uow_com_livro():
        return uow

    entrada = EntradaDeletarLivroCasoDeUso(livro_id=str(livro.id))

    caso_de_uso = DeletarLivro(entrada, obter_uow_com_livro)
    caso_de_uso.executar()

    livro_deletado = uow.repositorio_livros.buscar_por_id(livro.id)
    assert livro_deletado is None


def test_deve_lancar_excecao_quando_livro_nao_encontrado():
    entrada = EntradaDeletarLivroCasoDeUso(livro_id=str(LivroId.gerar()))
    caso_de_uso = DeletarLivro(entrada, obter_uow_fake)

    with pytest.raises(LivroNaoEncontrado):
        caso_de_uso.executar()
