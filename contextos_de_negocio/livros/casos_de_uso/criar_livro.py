from collections.abc import Callable

from contextos_de_negocio.livros.casos_de_uso.dtos import (
    EntradaCriarLivroCasoDeUso,
    SaidaCriarLivro,
)
from contextos_de_negocio.livros.dominio.entidades import Livro
from contextos_de_negocio.livros.dominio.objetos_de_valor import (
    AutoresLivro,
    FotoUrlLivro,
    IsbnLivro,
    ObservacaoLivro,
    SubtituloLivro,
    TituloLivro,
)
from utilitarios.provedor_de_armazenamento import ProvedorDeArmazenamento
from utilitarios.unidade_de_trabalho import (
    UnidadeDeTrabalhoAbstrata,
)


class CriarLivro:
    def __init__(
        self,
        entrada: EntradaCriarLivroCasoDeUso,
        obter_uow: Callable[[], UnidadeDeTrabalhoAbstrata],
        provedor_de_armazenamento: ProvedorDeArmazenamento,
    ):
        self.entrada = entrada
        self.obter_uow = obter_uow
        self.provedor_de_armazenamento = provedor_de_armazenamento

    def executar(self) -> SaidaCriarLivro:
        with self.obter_uow() as uow:
            foto_obj = self._fazer_upload_foto()

            livro = Livro.criar(
                titulo=TituloLivro(self.entrada.titulo),
                autores=AutoresLivro(self.entrada.autores),
                subtitulo=SubtituloLivro(self.entrada.subtitulo),
                isbn=IsbnLivro(self.entrada.isbn),
                foto_url=foto_obj,
                observacao=ObservacaoLivro(self.entrada.observacao),
            )

            livro_criado = uow.repositorio_livros.adicionar(livro)
            uow.commit()

            return SaidaCriarLivro(
                id=str(livro_criado.id),
                titulo=livro_criado.titulo.valor,
                autores=livro_criado.autores.valor,
                subtitulo=livro_criado.subtitulo.valor,
                isbn=livro_criado.isbn.valor,
                observacao=livro_criado.observacao.valor,
                foto=livro_criado.foto_url.valor
                if livro_criado.foto_url
                else None,
            )

    def _fazer_upload_foto(self) -> FotoUrlLivro | None:
        if self.entrada.foto and self.entrada.nome_arquivo_foto:
            caminho_foto = self.provedor_de_armazenamento.fazer_upload(
                self.entrada.foto, self.entrada.nome_arquivo_foto
            )
            return FotoUrlLivro(caminho_foto)
        return None
