from collections.abc import Callable
from uuid import UUID

from contextos_de_negocio.livros.casos_de_uso.dtos import (
    EntradaAtualizarLivroCasoDeUso,
    SaidaAtualizarLivro,
)
from contextos_de_negocio.livros.dominio.objetos_de_valor import (
    AutoresLivro,
    FotoUrlLivro,
    IsbnLivro,
    LivroId,
    ObservacaoLivro,
    SubtituloLivro,
    TituloLivro,
)
from contextos_de_negocio.livros.excecoes import LivroNaoEncontrado
from utilitarios.provedor_de_armazenamento import ProvedorDeArmazenamento
from utilitarios.unidade_de_trabalho import (
    UnidadeDeTrabalhoAbstrata,
)


class AtualizarLivro:
    def __init__(
        self,
        entrada: EntradaAtualizarLivroCasoDeUso,
        obter_uow: Callable[[], UnidadeDeTrabalhoAbstrata],
        provedor_de_armazenamento: ProvedorDeArmazenamento,
    ):
        self.entrada = entrada
        self.obter_uow = obter_uow
        self.provedor_de_armazenamento = provedor_de_armazenamento

    def executar(self) -> SaidaAtualizarLivro:
        with self.obter_uow() as uow:
            livro = uow.repositorio_livros.buscar_por_id(
                LivroId(UUID(self.entrada.livro_id))
            )
            if not livro:
                raise LivroNaoEncontrado()

            foto_obj = self._fazer_upload_foto()

            livro.editar(
                titulo=TituloLivro(self.entrada.titulo),
                autores=AutoresLivro(self.entrada.autores),
                subtitulo=SubtituloLivro(self.entrada.subtitulo),
                isbn=IsbnLivro(self.entrada.isbn),
                foto_url=foto_obj if foto_obj else livro.foto_url,
                observacao=ObservacaoLivro(self.entrada.observacao),
            )

            livro_atualizado = uow.repositorio_livros.adicionar(livro)
            uow.commit()

            return SaidaAtualizarLivro(
                id=str(livro_atualizado.id),
                titulo=livro_atualizado.titulo.valor,
                autores=livro_atualizado.autores.valor,
                subtitulo=livro_atualizado.subtitulo.valor,
                isbn=livro_atualizado.isbn.valor,
                observacao=livro_atualizado.observacao.valor,
                foto=livro_atualizado.foto_url.valor
                if livro_atualizado.foto_url
                else None,
            )

    def _fazer_upload_foto(self) -> FotoUrlLivro | None:
        if self.entrada.foto and self.entrada.nome_arquivo_foto:
            caminho_foto = self.provedor_de_armazenamento.fazer_upload(
                self.entrada.foto, self.entrada.nome_arquivo_foto
            )
            return FotoUrlLivro(caminho_foto)
        return None
