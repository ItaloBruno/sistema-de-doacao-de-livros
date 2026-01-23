from collections.abc import Callable
from uuid import UUID

from contextos_de_negocio.livros.dominio.objetos_de_valor import LivroId
from contextos_de_negocio.livros.excecoes import LivroNaoEncontrado
from contextos_de_negocio.livros.visualizadores.dtos import ItemLivro
from utilitarios.unidade_de_trabalho import UnidadeDeTrabalhoAbstrata


class Buscar:
    def __init__(self, obter_uow: Callable[[], UnidadeDeTrabalhoAbstrata]):
        self.obter_uow = obter_uow

    def executar(self, livro_id: str) -> ItemLivro:
        with self.obter_uow() as uow:
            livro = uow.repositorio_livros.buscar_por_id(
                LivroId(UUID(livro_id))
            )
            if not livro:
                raise LivroNaoEncontrado()

            return ItemLivro(
                id=str(livro.id),
                titulo=livro.titulo.valor,
                autores=livro.autores.valor,
                subtitulo=livro.subtitulo.valor,
                isbn=livro.isbn.valor,
                observacao=livro.observacao.valor,
                foto=livro.foto_url.valor if livro.foto_url else None,
            )
