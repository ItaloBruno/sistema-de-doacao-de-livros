from dataclasses import dataclass

from contextos_de_negocio.doacao.dominio.objetos_de_valor import (
    DoacaoId,
    LivroNaDoacao,
)
from contextos_de_negocio.doador.dominio.objetos_de_valor import DoadorId
from contextos_de_negocio.instituicao.dominio.objetos_de_valor import (
    InstituicaoId,
)


@dataclass
class Doacao:
    doador_id: DoadorId
    instituicao_id: InstituicaoId
    livros: list[LivroNaDoacao]
    id: DoacaoId | None = None

    @staticmethod
    def criar(
        doador_id: DoadorId,
        instituicao_id: InstituicaoId,
        livros: list[LivroNaDoacao],
    ) -> "Doacao":
        if not livros:
            raise ValueError("Doação deve ter pelo menos um livro")

        return Doacao(
            id=DoacaoId.gerar(),
            doador_id=doador_id,
            instituicao_id=instituicao_id,
            livros=livros,
        )
