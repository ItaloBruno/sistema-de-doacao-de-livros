# import json
# import uuid
# from datetime import datetime
# from http import HTTPStatus
# from pathlib import Path

# from fastapi import APIRouter, File, Form, HTTPException, UploadFile

# from sistema_de_doacao_de_livros import banco_de_dados
# from sistema_de_doacao_de_livros.pontos_de_entrada.esquemas.api import (
#     doacoes as esquemas,
# )
# from sistema_de_doacao_de_livros.schemas import DoacaoDB, DoadorDB

# rotas_api_doacoes = APIRouter(tags=["Doações"])


# @rotas_api_doacoes.post(
#     "/doacoes",
#     status_code=HTTPStatus.CREATED,
#     response_model=esquemas.RespostaCriarDoacao,
# )
# async def criar_doacao(  # noqa: PLR0913, PLR0917
#     instituicao_id: int = Form(...),
#     doador_id: int | None = Form(None),
#     doador_nome: str | None = Form(None),
#     doador_email: str | None = Form(None),
#     doador_telefone: str | None = Form(None),
#     doador_senha: str | None = Form(None),
#     livros_json: str = Form(...),
#     foto_arquivos: list[UploadFile] = File(default=[]),
# ):
#     try:
#         livros_data = json.loads(livros_json)
#     except json.JSONDecodeError:
#         raise HTTPException(
#             status_code=HTTPStatus.BAD_REQUEST,
#             detail="Formato de livros inválido",
#         )

#     livros = []
#     for livro_item in livros_data:
#         livros.append(
#             esquemas.EntradaLivroNaDoacao(livro_id=livro_item["livro_id"])
#         )

#     dados = esquemas.EntradaCriarDoacao(
#         instituicao_id=instituicao_id,
#         doador_id=doador_id,
#         doador_nome=doador_nome,
#         doador_email=doador_email,
#         doador_telefone=doador_telefone,
#         doador_senha=doador_senha,
#         livros=livros,
#     )

#     uploads_dir = Path(
#         "sistema_de_doacao_de_livros/pontos_de_entrada/estatico/uploads"
#     )
#     uploads_dir.mkdir(parents=True, exist_ok=True)

#     foto_urls_uploaded = {}
#     for idx, arquivo in enumerate(foto_arquivos):
#         if arquivo.filename:
#             extensao = Path(arquivo.filename).suffix
#             nome_arquivo = f"{uuid.uuid4()}{extensao}"
#             caminho_arquivo = uploads_dir / nome_arquivo

#             conteudo = await arquivo.read()
#             with open(caminho_arquivo, "wb") as f:
#                 f.write(conteudo)

#             try:
#                 livro_idx = int(arquivo.filename)
#                 foto_urls_uploaded[livro_idx] = (
#                     f"/static/uploads/{nome_arquivo}"
#                 )
#             except ValueError:
#                 foto_urls_uploaded[idx] = f"/static/uploads/{nome_arquivo}"

#     return _processar_doacao(dados, foto_urls_uploaded)


# def _processar_doacao(
#     dados: esquemas.EntradaCriarDoacao, foto_urls_uploaded: dict
# ):
#     instituicao = banco_de_dados.buscar_instituicao_por_id(
#         dados.instituicao_id
#     )
#     if not instituicao:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND,
#             detail="Instituição não encontrada",
#         )

#     if dados.doador_id:
#         doador = banco_de_dados.buscar_doador_por_id(dados.doador_id)
#         if not doador:
#             raise HTTPException(
#                 status_code=HTTPStatus.NOT_FOUND,
#                 detail="Doador não encontrado",
#             )
#         doador_id = dados.doador_id
#     else:
#         if not dados.doador_nome:
#             raise HTTPException(
#                 status_code=HTTPStatus.BAD_REQUEST,
#                 detail="Nome do doador é obrigatório",
#             )
#         if not dados.doador_email:
#             raise HTTPException(
#                 status_code=HTTPStatus.BAD_REQUEST,
#                 detail="Email do doador é obrigatório",
#             )
#         if not dados.doador_senha:
#             raise HTTPException(
#                 status_code=HTTPStatus.BAD_REQUEST,
#                 detail="Senha do doador é obrigatória",
#             )
#         if not dados.doador_telefone:
#             raise HTTPException(
#                 status_code=HTTPStatus.BAD_REQUEST,
#                 detail="Telefone do doador é obrigatório",
#             )

#         doador_nome: str = dados.doador_nome
#         doador_email: str = dados.doador_email
#         doador_senha: str = dados.doador_senha
#         doador_telefone: str = dados.doador_telefone

#         if banco_de_dados.buscar_doador_por_email(doador_email):
#             raise HTTPException(
#                 status_code=HTTPStatus.BAD_REQUEST,
#                 detail="Email já cadastrado",
#             )

#         novo_doador = DoadorDB(
#             id=len(banco_de_dados.doadores) + 1,
#             nome=doador_nome,
#             email=doador_email,
#             senha=doador_senha,
#             telefone=doador_telefone,
#         )
#         banco_de_dados.doadores.append(novo_doador)
#         doador_id = novo_doador.id
#         doador = novo_doador

#     for livro_doacao in dados.livros:
#         livro = banco_de_dados.buscar_livro_por_id(livro_doacao.livro_id)
#         if not livro:
#             raise HTTPException(
#                 status_code=HTTPStatus.NOT_FOUND,
#               detail=f"Livro com ID {livro_doacao.livro_id} não encontrado",
#             )

#     doacao_db = DoacaoDB(
#         id=len(banco_de_dados.doacoes) + 1,
#         instituicao_id=dados.instituicao_id,
#         doador_id=doador_id,
#         data_criacao=datetime.now(),
#         status=esquemas.StatusDoacao.PENDENTE,
#     )
#     banco_de_dados.doacoes.append(doacao_db)

#     for livro_doacao in dados.livros:
#         banco_de_dados.livros_nas_doacoes.append({
#             "id": len(banco_de_dados.livros_nas_doacoes) + 1,
#             "doacao_id": doacao_db.id,
#             "livro_id": livro_doacao.livro_id,
#         })

#     return esquemas.RespostaCriarDoacao(
#         id=doacao_db.id,
#         instituicao_id=instituicao.id,
#         instituicao_nome=instituicao.nome,
#         doador_id=doador.id,
#         doador_nome=doador.nome,
#         data_criacao=doacao_db.data_criacao,
#         status=doacao_db.status,
#         quantidade_livros=len(dados.livros),
#     )


# @rotas_api_doacoes.get(
#     "/doacoes/doador/{doador_id}",
#     response_model=list[esquemas.RespostaListarDoacoesDoador],
# )
# def listar_doacoes_doador(doador_id: int):
#     doador = banco_de_dados.buscar_doador_por_id(doador_id)
#     if not doador:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND,
#             detail="Doador não encontrado",
#         )

#     doacoes_doador = banco_de_dados.buscar_doacoes_por_doador(doador_id)

#     resultado = []
#     for doacao in doacoes_doador:
#         instituicao = banco_de_dados.buscar_instituicao_por_id(
#             doacao.instituicao_id
#         )
#         if not instituicao:
#             raise ValueError(
#                 f"Instituição {doacao.instituicao_id} não encontrada"
#             )
#         quantidade_livros = banco_de_dados.contar_livros_da_doacao(doacao.id)

#         resultado.append(
#             esquemas.RespostaListarDoacoesDoador(
#                 id=doacao.id,
#                 instituicao_id=instituicao.id,
#                 instituicao_nome=instituicao.nome,
#                 doador_id=doador.id,
#                 doador_nome=doador.nome,
#                 data_criacao=doacao.data_criacao,
#                 status=doacao.status,
#                 quantidade_livros=quantidade_livros,
#             )
#         )

#     return resultado


# @rotas_api_doacoes.get(
#     "/doacoes/instituicao/{instituicao_id}",
#     response_model=list[esquemas.RespostaListarDoacoesInstituicao],
# )
# def listar_doacoes_instituicao(instituicao_id: int):
#     instituicao = banco_de_dados.buscar_instituicao_por_id(instituicao_id)
#     if not instituicao:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND,
#             detail="Instituição não encontrada",
#         )

#     doacoes_instituicao = banco_de_dados.buscar_doacoes_por_instituicao(
#         instituicao_id
#     )

#     resultado = []
#     for doacao in doacoes_instituicao:
#         doador = banco_de_dados.buscar_doador_por_id(doacao.doador_id)
#         if not doador:
#             raise ValueError(f"Doador {doacao.doador_id} não encontrado")
#         quantidade_livros = banco_de_dados.contar_livros_da_doacao(doacao.id)

#         resultado.append(
#             esquemas.RespostaListarDoacoesInstituicao(
#                 id=doacao.id,
#                 instituicao_id=instituicao.id,
#                 instituicao_nome=instituicao.nome,
#                 doador_id=doador.id,
#                 doador_nome=doador.nome,
#                 data_criacao=doacao.data_criacao,
#                 status=doacao.status,
#                 quantidade_livros=quantidade_livros,
#             )
#         )

#     return resultado


# @rotas_api_doacoes.get(
#     "/doacoes/{doacao_id}",
#     response_model=esquemas.RespostaBuscarDoacaoCompleta,
# )
# def buscar_doacao_completa(doacao_id: int):
#     doacao = banco_de_dados.buscar_doacao_por_id(doacao_id)
#     if not doacao:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND,
#             detail="Doação não encontrada",
#         )

#     instituicao = banco_de_dados.buscar_instituicao_por_id(
#         doacao.instituicao_id
#     )
#     doador = banco_de_dados.buscar_doador_por_id(doacao.doador_id)
#     if not doador:
#         raise ValueError(f"Doador {doacao.doador_id} não encontrado")
#     livros_doacao = banco_de_dados.buscar_livros_da_doacao(doacao.id)

#     livros_completos = []
#     for livro_doacao in livros_doacao:
#         livro = banco_de_dados.buscar_livro_por_id(livro_doacao["livro_id"])
#         if not livro:
#             raise ValueError(
#                 f"Livro {livro_doacao['livro_id']} não encontrado"
#             )
#         livros_completos.append(
#             esquemas.LivroNaDoacaoCompleto(
#                 id=livro_doacao["id"],
#                 livro=esquemas.LivroDetalhado(
#                     id=livro.id,
#                     titulo=livro.titulo,
#                     subtitulo=livro.subtitulo,
#                     autores=livro.autores,
#                     isbn=livro.isbn,
#                     foto_url=livro.foto_url,
#                     observacao=livro.observacao,
#                 ),
#             )
#         )

#     if not instituicao:
#       raise ValueError(f"Instituição {doacao.instituicao_id} não encontrada")

#     return esquemas.RespostaBuscarDoacaoCompleta(
#         id=doacao.id,
#         instituicao=esquemas.InstituicaoNaDoacao(
#             id=instituicao.id,
#             nome=instituicao.nome,
#             email=instituicao.email,
#             descricao=instituicao.descricao,
#             data_fundacao=instituicao.data_fundacao,
#             data_registro=instituicao.data_registro,
#             livros_recebidos=instituicao.livros_recebidos,
#             foto_url=instituicao.foto_url,
#             site=instituicao.site,
#             endereco=instituicao.endereco,
#         ),
#         doador=esquemas.DoadorNaDoacao(
#             id=doador.id,
#             nome=doador.nome,
#             email=doador.email,
#             telefone=doador.telefone,
#         ),
#         data_criacao=doacao.data_criacao,
#         status=doacao.status,
#         livros=livros_completos,
#     )


# @rotas_api_doacoes.patch(
#     "/doacoes/{doacao_id}/status",
#     response_model=esquemas.RespostaAtualizarStatusDoacao,
# )
# def atualizar_status_doacao(
#     doacao_id: int, dados: esquemas.EntradaAtualizarStatusDoacao
# ):
#     doacao = banco_de_dados.buscar_doacao_por_id(doacao_id)
#     if not doacao:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND,
#             detail="Doação não encontrada",
#         )

#     doacao.status = dados.status

#     if dados.status == esquemas.StatusDoacao.CONCLUIDA:
#         quantidade_livros = banco_de_dados.contar_livros_da_doacao(doacao_id)
#         banco_de_dados.incrementar_livros_recebidos_instituicao(
#             doacao.instituicao_id, quantidade_livros
#         )

#     return esquemas.RespostaAtualizarStatusDoacao(
#         mensagem="Status atualizado com sucesso"
#     )


# @rotas_api_doacoes.delete(
#     "/doacoes/{doacao_id}", response_model=esquemas.RespostaDeletarDoacao
# )
# def deletar_doacao(doacao_id: int):
#     doacao = banco_de_dados.buscar_doacao_por_id(doacao_id)
#     if not doacao:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND,
#             detail="Doação não encontrada",
#         )

#     if doacao.status != esquemas.StatusDoacao.PENDENTE:
#         raise HTTPException(
#             status_code=HTTPStatus.BAD_REQUEST,
#             detail="Apenas doações pendentes podem ser excluídas",
#         )

#     banco_de_dados.doacoes.remove(doacao)
#     banco_de_dados.livros_nas_doacoes = [
#         livro
#         for livro in banco_de_dados.livros_nas_doacoes
#         if livro["doacao_id"] != doacao_id
#     ]

#     return esquemas.RespostaDeletarDoacao(
#         mensagem="Doação excluída com sucesso"
#     )

# from datetime import date, datetime
# from enum import Enum

# from pydantic import BaseModel, EmailStr


# class StatusDoacao(str, Enum):
#     PENDENTE = "pendente"
#     ACEITA = "aceita"
#     REJEITADA = "rejeitada"
#     CONCLUIDA = "concluida"


# class EntradaLivroNaDoacao(BaseModel):
#     livro_id: int


# class EntradaCriarDoacao(BaseModel):
#     instituicao_id: int
#     doador_id: int | None = None
#     doador_nome: str | None = None
#     doador_email: EmailStr | None = None
#     doador_senha: str | None = None
#     doador_telefone: str | None = None
#     livros: list[EntradaLivroNaDoacao]


# class RespostaCriarDoacao(BaseModel):
#     id: int
#     instituicao_id: int
#     instituicao_nome: str
#     doador_id: int
#     doador_nome: str
#     data_criacao: datetime
#     status: StatusDoacao
#     quantidade_livros: int


# class RespostaListarDoacoesDoador(BaseModel):
#     id: int
#     instituicao_id: int
#     instituicao_nome: str
#     doador_id: int
#     doador_nome: str
#     data_criacao: datetime
#     status: StatusDoacao
#     quantidade_livros: int


# class RespostaListarDoacoesInstituicao(BaseModel):
#     id: int
#     instituicao_id: int
#     instituicao_nome: str
#     doador_id: int
#     doador_nome: str
#     data_criacao: datetime
#     status: StatusDoacao
#     quantidade_livros: int


# class RespostaBuscarDoacaoCompleta(BaseModel):
#     id: int
#     instituicao: "InstituicaoNaDoacao"
#     doador: "DoadorNaDoacao"
#     data_criacao: datetime
#     status: StatusDoacao
#     livros: list["LivroNaDoacaoCompleto"]


# class InstituicaoNaDoacao(BaseModel):
#     id: int
#     nome: str
#     email: EmailStr
#     descricao: str
#     data_fundacao: date
#     data_registro: datetime
#     livros_recebidos: int
#     foto_url: str | None = None
#     site: str | None = None
#     endereco: str


# class DoadorNaDoacao(BaseModel):
#     id: int
#     nome: str
#     email: EmailStr
#     telefone: str


# class LivroNaDoacaoCompleto(BaseModel):
#     id: int
#     livro: "LivroDetalhado"


# class LivroDetalhado(BaseModel):
#     id: int
#     titulo: str
#     subtitulo: str | None = None
#     autores: list[str]
#     isbn: str | None = None
#     foto_url: str | None = None
#     observacao: str | None = None


# class EntradaAtualizarStatusDoacao(BaseModel):
#     status: StatusDoacao


# class RespostaAtualizarStatusDoacao(BaseModel):
#     mensagem: str


# class RespostaDeletarDoacao(BaseModel):
#     mensagem: str
