from collections.abc import Callable
from uuid import UUID

from contextos_de_negocio.livros.casos_de_uso.dtos import (
    EntradaDeletarLivroCasoDeUso,
)
from contextos_de_negocio.livros.dominio.objetos_de_valor import LivroId
from contextos_de_negocio.livros.excecoes import LivroNaoEncontrado
from utilitarios.unidade_de_trabalho import (
    UnidadeDeTrabalhoAbstrata,
)


class DeletarLivro:
    def __init__(
        self,
        entrada: EntradaDeletarLivroCasoDeUso,
        obter_uow: Callable[[], UnidadeDeTrabalhoAbstrata],
    ):
        self.entrada = entrada
        self.obter_uow = obter_uow

    def executar(self) -> None:
        with self.obter_uow() as uow:
            livro = uow.repositorio_livros.buscar_por_id(
                LivroId(UUID(self.entrada.livro_id))
            )
            if not livro:
                raise LivroNaoEncontrado()

            uow.repositorio_livros.deletar(livro)
            uow.commit()
