import json
from http import HTTPStatus
from typing import Annotated, Final

from fastapi import APIRouter, Depends, File, Form, UploadFile

from contextos_de_negocio.livros.casos_de_uso.atualizar_livro import (
    AtualizarLivro,
    EntradaAtualizarLivroCasoDeUso,
)
from contextos_de_negocio.livros.casos_de_uso.criar_livro import (
    CriarLivro,
    EntradaCriarLivroCasoDeUso,
)
from contextos_de_negocio.livros.casos_de_uso.deletar_livro import (
    DeletarLivro,
    EntradaDeletarLivroCasoDeUso,
)
from contextos_de_negocio.livros.pontos_de_entrada.esquemas import (
    ItemLivroResposta,
    RespostaAtualizarLivro,
    RespostaCriarLivro,
    RespostaListarLivros,
)
from contextos_de_negocio.livros.pontos_de_entrada.parametros import (
    ParametrosListagemLivros,
)
from contextos_de_negocio.livros.visualizadores.listar import Listar
from utilitarios.provedor_de_armazenamento import ProvedorDeArmazenamento
from utilitarios.provedor_de_armazenamento.armazenamento_local import (
    EstrategiaArmazenamentoLocal,
)
from utilitarios.unidade_de_trabalho import unidade_de_trabalho
from utilitarios.visualizadores.dtos import ParametrosListagem

api_livros: Final[APIRouter] = APIRouter(tags=["Livros"])


@api_livros.get(
    "/livros",
    status_code=HTTPStatus.OK,
    response_model=RespostaListarLivros,
)
def listar_livros(
    parametros: ParametrosListagemLivros = Depends(),
):
    visualizador = Listar(obter_uow=unidade_de_trabalho)
    resultado = visualizador.executar(
        ParametrosListagem(
            filtros_dict=parametros.obter_filtros_dict(),
            pagina=parametros.pagina,
            itens_por_pagina=parametros.itens_por_pagina,
            ordem=parametros.ordem,
            campos=parametros.campos,
        )
    )

    return RespostaListarLivros(
        itens=[
            ItemLivroResposta(
                id=item.id,
                titulo=item.titulo,
                autores=item.autores,
                subtitulo=item.subtitulo,
                isbn=item.isbn,
                observacao=item.observacao,
                foto=item.foto,
            )
            for item in resultado.itens
        ],
        total=resultado.total,
        pagina=resultado.pagina,
        itens_por_pagina=resultado.itens_por_pagina,
        total_paginas=resultado.total_paginas,
    )


@api_livros.post(
    "/livros",
    status_code=HTTPStatus.CREATED,
    response_model=RespostaCriarLivro,
)
def criar_livro(
    titulo: Annotated[str, Form()],
    autores: Annotated[str, Form()],
    subtitulo: Annotated[str | None, Form()] = None,
    isbn: Annotated[str | None, Form()] = None,
    observacao: Annotated[str | None, Form()] = None,
    foto: Annotated[UploadFile | None, File()] = None,
):
    try:
        autores_list = json.loads(autores)
    except json.JSONDecodeError:
        autores_list = [autores]

    entrada = EntradaCriarLivroCasoDeUso(
        titulo=titulo,
        autores=autores_list,
        subtitulo=subtitulo,
        isbn=isbn,
        observacao=observacao,
        foto=foto.file.read() if foto else None,
        nome_arquivo_foto=foto.filename if foto else None,
    )

    caso_de_uso = CriarLivro(
        entrada=entrada,
        obter_uow=unidade_de_trabalho,
        provedor_de_armazenamento=ProvedorDeArmazenamento(
            EstrategiaArmazenamentoLocal()
        ),
    )
    saida = caso_de_uso.executar()

    return RespostaCriarLivro(
        id=saida.id,
        titulo=saida.titulo,
        autores=saida.autores,
        subtitulo=saida.subtitulo,
        isbn=saida.isbn,
        observacao=saida.observacao,
        foto=saida.foto,
    )


@api_livros.put(
    "/livros/{livro_id}",
    status_code=HTTPStatus.OK,
    response_model=RespostaAtualizarLivro,
)
def atualizar_livro(
    livro_id: str,
    titulo: Annotated[str, Form()],
    autores: Annotated[str, Form()],
    subtitulo: Annotated[str | None, Form()] = None,
    isbn: Annotated[str | None, Form()] = None,
    observacao: Annotated[str | None, Form()] = None,
    foto: Annotated[UploadFile | None, File()] = None,
):
    try:
        autores_list = json.loads(autores)
    except json.JSONDecodeError:
        autores_list = [autores]

    entrada = EntradaAtualizarLivroCasoDeUso(
        livro_id=livro_id,
        titulo=titulo,
        autores=autores_list,
        subtitulo=subtitulo,
        isbn=isbn,
        observacao=observacao,
        foto=foto.file.read() if foto else None,
        nome_arquivo_foto=foto.filename if foto else None,
    )

    caso_de_uso = AtualizarLivro(
        entrada=entrada,
        obter_uow=unidade_de_trabalho,
        provedor_de_armazenamento=ProvedorDeArmazenamento(
            EstrategiaArmazenamentoLocal()
        ),
    )
    saida = caso_de_uso.executar()

    return RespostaAtualizarLivro(
        id=saida.id,
        titulo=saida.titulo,
        autores=saida.autores,
        subtitulo=saida.subtitulo,
        isbn=saida.isbn,
        observacao=saida.observacao,
        foto=saida.foto,
    )


@api_livros.delete(
    "/livros/{livro_id}",
    status_code=HTTPStatus.NO_CONTENT,
)
def deletar_livro(livro_id: str):
    entrada = EntradaDeletarLivroCasoDeUso(livro_id=livro_id)

    caso_de_uso = DeletarLivro(entrada=entrada, obter_uow=unidade_de_trabalho)
    caso_de_uso.executar()
