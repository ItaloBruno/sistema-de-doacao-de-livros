from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from sistema_de_doacao_de_livros import banco_de_dados
from sistema_de_doacao_de_livros.schemas import (
    AtualizacaoStatusDoacao,
    CriacaoDeDoacao,
    Doacao,
    DoacaoCompleta,
    DoacaoDB,
    Doador,
    DoadorDB,
    Instituicao,
    Livro,
    LivroNaDoacaoCompleto,
    RespostaDoSistema,
    StatusDoacao,
)

rotas_api_doacoes = APIRouter()


@rotas_api_doacoes.post(
    "/doacoes", status_code=HTTPStatus.CREATED, response_model=Doacao
)
def criar_doacao(dados: CriacaoDeDoacao):
    instituicao = banco_de_dados.buscar_instituicao_por_id(
        dados.instituicao_id
    )
    if not instituicao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Instituição não encontrada",
        )

    if dados.doador_id:
        doador = banco_de_dados.buscar_doador_por_id(dados.doador_id)
        if not doador:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Doador não encontrado",
            )
        doador_id = dados.doador_id
    else:
        if not all([
            dados.doador_nome,
            dados.doador_email,
            dados.doador_senha,
            dados.doador_telefone,
        ]):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Dados do doador são obrigatórios",
            )

        if banco_de_dados.buscar_doador_por_email(dados.doador_email):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Email já cadastrado",
            )

        novo_doador = DoadorDB(
            id=len(banco_de_dados.doadores) + 1,
            nome=dados.doador_nome,
            email=dados.doador_email,
            senha=dados.doador_senha,
            telefone=dados.doador_telefone,
        )
        banco_de_dados.doadores.append(novo_doador)
        doador_id = novo_doador.id
        doador = novo_doador

    for livro_doacao in dados.livros:
        livro = banco_de_dados.buscar_livro_por_id(livro_doacao.livro_id)
        if not livro:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Livro com ID {livro_doacao.livro_id} não encontrado",
            )

    doacao_db = DoacaoDB(
        id=len(banco_de_dados.doacoes) + 1,
        instituicao_id=dados.instituicao_id,
        doador_id=doador_id,
        data_criacao=datetime.now(),
        status=StatusDoacao.PENDENTE,
    )
    banco_de_dados.doacoes.append(doacao_db)

    for livro_doacao in dados.livros:
        banco_de_dados.livros_nas_doacoes.append({
            "id": len(banco_de_dados.livros_nas_doacoes) + 1,
            "doacao_id": doacao_db.id,
            "livro_id": livro_doacao.livro_id,
            "foto_url": livro_doacao.foto_url,
            "observacao": livro_doacao.observacao,
        })

    return Doacao(
        id=doacao_db.id,
        instituicao_id=instituicao.id,
        instituicao_nome=instituicao.nome,
        doador_id=doador.id,
        doador_nome=doador.nome,
        data_criacao=doacao_db.data_criacao,
        status=doacao_db.status,
        quantidade_livros=len(dados.livros),
    )


@rotas_api_doacoes.get(
    "/doacoes/doador/{doador_id}", response_model=list[Doacao]
)
def listar_doacoes_doador(doador_id: int):
    doador = banco_de_dados.buscar_doador_por_id(doador_id)
    if not doador:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Doador não encontrado",
        )

    doacoes_doador = banco_de_dados.buscar_doacoes_por_doador(doador_id)

    resultado = []
    for doacao in doacoes_doador:
        instituicao = banco_de_dados.buscar_instituicao_por_id(
            doacao.instituicao_id
        )
        quantidade_livros = banco_de_dados.contar_livros_da_doacao(doacao.id)

        resultado.append(
            Doacao(
                id=doacao.id,
                instituicao_id=instituicao.id,
                instituicao_nome=instituicao.nome,
                doador_id=doador.id,
                doador_nome=doador.nome,
                data_criacao=doacao.data_criacao,
                status=doacao.status,
                quantidade_livros=quantidade_livros,
            )
        )

    return resultado


@rotas_api_doacoes.get(
    "/doacoes/instituicao/{instituicao_id}", response_model=list[Doacao]
)
def listar_doacoes_instituicao(instituicao_id: int):
    instituicao = banco_de_dados.buscar_instituicao_por_id(instituicao_id)
    if not instituicao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Instituição não encontrada",
        )

    doacoes_instituicao = banco_de_dados.buscar_doacoes_por_instituicao(
        instituicao_id
    )

    resultado = []
    for doacao in doacoes_instituicao:
        doador = banco_de_dados.buscar_doador_por_id(doacao.doador_id)
        quantidade_livros = banco_de_dados.contar_livros_da_doacao(doacao.id)

        resultado.append(
            Doacao(
                id=doacao.id,
                instituicao_id=instituicao.id,
                instituicao_nome=instituicao.nome,
                doador_id=doador.id,
                doador_nome=doador.nome,
                data_criacao=doacao.data_criacao,
                status=doacao.status,
                quantidade_livros=quantidade_livros,
            )
        )

    return resultado


@rotas_api_doacoes.get("/doacoes/{doacao_id}", response_model=DoacaoCompleta)
def buscar_doacao_completa(doacao_id: int):
    doacao = banco_de_dados.buscar_doacao_por_id(doacao_id)
    if not doacao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Doação não encontrada",
        )

    instituicao = banco_de_dados.buscar_instituicao_por_id(
        doacao.instituicao_id
    )
    doador = banco_de_dados.buscar_doador_por_id(doacao.doador_id)
    livros_doacao = banco_de_dados.buscar_livros_da_doacao(doacao.id)

    livros_completos = []
    for livro_doacao in livros_doacao:
        livro = banco_de_dados.buscar_livro_por_id(livro_doacao["livro_id"])
        livros_completos.append(
            LivroNaDoacaoCompleto(
                id=livro_doacao["id"],
                livro=Livro(
                    id=livro.id,
                    titulo=livro.titulo,
                    subtitulo=livro.subtitulo,
                    autores=livro.autores,
                    isbn=livro.isbn,
                ),
                foto_url=livro_doacao["foto_url"],
                observacao=livro_doacao["observacao"],
            )
        )

    return DoacaoCompleta(
        id=doacao.id,
        instituicao=Instituicao(
            id=instituicao.id,
            nome=instituicao.nome,
            email=instituicao.email,
            descricao=instituicao.descricao,
            data_fundacao=instituicao.data_fundacao,
            data_registro=instituicao.data_registro,
            livros_recebidos=instituicao.livros_recebidos,
            foto_url=instituicao.foto_url,
            site=instituicao.site,
            endereco=instituicao.endereco,
        ),
        doador=Doador(
            id=doador.id,
            nome=doador.nome,
            email=doador.email,
            telefone=doador.telefone,
        ),
        data_criacao=doacao.data_criacao,
        status=doacao.status,
        livros=livros_completos,
    )


@rotas_api_doacoes.patch(
    "/doacoes/{doacao_id}/status", response_model=RespostaDoSistema
)
def atualizar_status_doacao(doacao_id: int, dados: AtualizacaoStatusDoacao):
    doacao = banco_de_dados.buscar_doacao_por_id(doacao_id)
    if not doacao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Doação não encontrada",
        )

    doacao.status = dados.status

    if dados.status == StatusDoacao.CONCLUIDA:
        quantidade_livros = banco_de_dados.contar_livros_da_doacao(doacao_id)
        banco_de_dados.incrementar_livros_recebidos_instituicao(
            doacao.instituicao_id, quantidade_livros
        )

    return RespostaDoSistema(mensagem="Status atualizado com sucesso")


@rotas_api_doacoes.delete(
    "/doacoes/{doacao_id}", response_model=RespostaDoSistema
)
def deletar_doacao(doacao_id: int):
    doacao = banco_de_dados.buscar_doacao_por_id(doacao_id)
    if not doacao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Doação não encontrada",
        )

    if doacao.status != StatusDoacao.PENDENTE:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Apenas doações pendentes podem ser excluídas",
        )

    banco_de_dados.doacoes.remove(doacao)
    banco_de_dados.livros_nas_doacoes = [
        livro
        for livro in banco_de_dados.livros_nas_doacoes
        if livro["doacao_id"] != doacao_id
    ]

    return RespostaDoSistema(mensagem="Doação excluída com sucesso")
