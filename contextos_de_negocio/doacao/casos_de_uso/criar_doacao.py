from collections.abc import Callable
from uuid import UUID

from contextos_de_negocio.doacao.casos_de_uso.dtos import (
    EntradaCriarDoacaoCasoDeUso,
    SaidaCriarDoacao,
)
from contextos_de_negocio.doacao.dominio.entidades import Doacao
from contextos_de_negocio.doacao.dominio.objetos_de_valor import LivroNaDoacao
from contextos_de_negocio.doacao.excecoes import (
    InstituicaoNaoEncontrada,
    LivroNaoEncontrado,
)
from contextos_de_negocio.doador.dominio.objetos_de_valor import DoadorId
from contextos_de_negocio.instituicao.dominio.objetos_de_valor import (
    InstituicaoId,
)
from contextos_de_negocio.livros.dominio.objetos_de_valor import LivroId
from utilitarios.unidade_de_trabalho import (
    UnidadeDeTrabalhoAbstrata,
)


class CriarDoacao:
    def __init__(
        self,
        entrada: EntradaCriarDoacaoCasoDeUso,
        doador_id: DoadorId,
        obter_uow: Callable[[], UnidadeDeTrabalhoAbstrata],
    ):
        self.entrada = entrada
        self.doador_id = doador_id
        self.obter_uow = obter_uow

    def executar(self) -> SaidaCriarDoacao:
        with self.obter_uow() as uow:
            instituicao_id = InstituicaoId(UUID(self.entrada.instituicao_id))
            livros_ids = [
                LivroId(UUID(livro_id)) for livro_id in self.entrada.livros_ids
            ]

            self._validar_instituicao_existe(uow, instituicao_id)
            self._validar_livros_existem(uow, livros_ids)

            livros_para_doacao = [
                LivroNaDoacao(livro_id=livro_id) for livro_id in livros_ids
            ]

            doacao = Doacao.criar(
                doador_id=self.doador_id,
                instituicao_id=instituicao_id,
                livros=livros_para_doacao,
            )

            doacao_criada = uow.repositorio_doacoes.adicionar(doacao)
            uow.commit()

            return SaidaCriarDoacao(
                id=str(doacao_criada.id),
                doador_id=str(doacao_criada.doador_id),
                instituicao_id=str(doacao_criada.instituicao_id),
                livros_ids=[
                    str(livro.livro_id) for livro in doacao_criada.livros
                ],
            )

    def _validar_instituicao_existe(
        self, uow: UnidadeDeTrabalhoAbstrata, instituicao_id: InstituicaoId
    ) -> None:
        if not uow.repositorio_doacoes.instituicao_existe(instituicao_id):
            raise InstituicaoNaoEncontrada()

    def _validar_livros_existem(
        self, uow: UnidadeDeTrabalhoAbstrata, livros_ids: list[LivroId]
    ) -> None:
        if not uow.repositorio_doacoes.livros_existem(livros_ids):
            raise LivroNaoEncontrado()
