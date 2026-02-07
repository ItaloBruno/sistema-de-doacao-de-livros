# import uuid
# from datetime import date as date_type
# from datetime import datetime
# from http import HTTPStatus
# from pathlib import Path

# from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile

# from sistema_de_doacao_de_livros import banco_de_dados
# from sistema_de_doacao_de_livros.pontos_de_entrada.esquemas.api import (
#     instituicoes as esquemas,
# )
# from sistema_de_doacao_de_livros.schemas import InstituicaoDB

# rotas_api_instituicoes = APIRouter(tags=["Instituições"])


# @rotas_api_instituicoes.post(
#     "/instituicoes",
#     status_code=HTTPStatus.CREATED,
#     response_model=esquemas.RespostaCriarInstituicao,
# )
# def criar_instituicao(dados: esquemas.EntradaCriarInstituicao):
#     if banco_de_dados.buscar_instituicao_por_email(dados.email):
#         raise HTTPException(
#             status_code=HTTPStatus.BAD_REQUEST,
#             detail="Email já cadastrado",
#         )

#     if banco_de_dados.buscar_doador_por_email(dados.email):
#         raise HTTPException(
#             status_code=HTTPStatus.BAD_REQUEST,
#             detail="Email já cadastrado como doador",
#         )

#     instituicao_db = InstituicaoDB(
#         **dados.model_dump(),
#         id=len(banco_de_dados.instituicoes) + 1,
#         data_registro=datetime.now(),
#         livros_recebidos=0,
#     )

#     banco_de_dados.instituicoes.append(instituicao_db)

#     return esquemas.RespostaCriarInstituicao(
#         id=instituicao_db.id,
#         nome=instituicao_db.nome,
#         email=instituicao_db.email,
#         descricao=instituicao_db.descricao,
#         data_fundacao=instituicao_db.data_fundacao,
#         data_registro=instituicao_db.data_registro,
#         livros_recebidos=instituicao_db.livros_recebidos,
#         foto_url=instituicao_db.foto_url,
#         site=instituicao_db.site,
#         endereco=instituicao_db.endereco,
#     )


# @rotas_api_instituicoes.get(
#     "/instituicoes", response_model=esquemas.RespostaListarInstituicoes
# )
# def listar_instituicoes(
#     pagina: int = Query(1, ge=1),
#     tamanho_pagina: int = Query(10, ge=1, le=50),
# ):
#     total = len(banco_de_dados.instituicoes)
#     inicio = (pagina - 1) * tamanho_pagina
#     fim = inicio + tamanho_pagina

#     instituicoes_pagina = banco_de_dados.instituicoes[inicio:fim]

#     instituicoes_lista = [
#         esquemas.ItemInstituicao(
#             id=inst.id,
#             nome=inst.nome,
#             email=inst.email,
#             descricao=inst.descricao,
#             data_fundacao=inst.data_fundacao,
#             data_registro=inst.data_registro,
#             livros_recebidos=inst.livros_recebidos,
#             foto_url=inst.foto_url,
#             site=inst.site,
#             endereco=inst.endereco,
#         )
#         for inst in instituicoes_pagina
#     ]

#     return esquemas.RespostaListarInstituicoes(
#         instituicoes=instituicoes_lista,
#         total=total,
#         pagina=pagina,
#         tamanho_pagina=tamanho_pagina,
#     )


# @rotas_api_instituicoes.get(
#     "/instituicoes/{instituicao_id}",
#     response_model=esquemas.RespostaBuscarInstituicao,
# )
# def buscar_instituicao(instituicao_id: int):
#   instituicao = banco_de_dados.buscar_instituicao_por_id(instituicao_id)
#     if not instituicao:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND,
#             detail="Instituição não encontrada",
#         )

#     return esquemas.RespostaBuscarInstituicao(
#         id=instituicao.id,
#         nome=instituicao.nome,
#         email=instituicao.email,
#         descricao=instituicao.descricao,
#         data_fundacao=instituicao.data_fundacao,
#         data_registro=instituicao.data_registro,
#         livros_recebidos=instituicao.livros_recebidos,
#         foto_url=instituicao.foto_url,
#         site=instituicao.site,
#         endereco=instituicao.endereco,
#     )


# @rotas_api_instituicoes.put(
#     "/instituicoes/{instituicao_id}",
#     response_model=esquemas.RespostaAtualizarInstituicao,
# )
# async def atualizar_instituicao(
#     instituicao_id: int,
#     nome: str = Form(...),
#     email: str = Form(...),
#     descricao: str = Form(...),
#     data_fundacao: str = Form(...),
#     endereco: str = Form(...),
#     senha_atual: str = Form(...),
#     site: str = Form(None),
#     nova_senha: str = Form(None),
#     foto: UploadFile = File(None),
# ):
#     instituicao = banco_de_dados.buscar_instituicao_por_id(instituicao_id)
#     if not instituicao:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND,
#             detail="Instituição não encontrada",
#         )

#     if instituicao.senha != senha_atual:
#         raise HTTPException(
#             status_code=HTTPStatus.UNAUTHORIZED,
#             detail="Senha atual incorreta",
#         )

#     if email != instituicao.email:
#         instituicao_existente = banco_de_dados.buscar_instituicao_por_email(
#             email
#         )
#         if instituicao_existente:
#             raise HTTPException(
#                 status_code=HTTPStatus.BAD_REQUEST,
#                 detail="Email já cadastrado",
#             )

#         doador_existente = banco_de_dados.buscar_doador_por_email(email)
#         if doador_existente:
#             raise HTTPException(
#                 status_code=HTTPStatus.BAD_REQUEST,
#                 detail="Email já cadastrado como doador",
#             )

#     foto_url = instituicao.foto_url
#     if foto and foto.filename:
#       fotos_dir = Path("/tmp/sistema-de-doacao-de-livros/fotos_instituicoes")
#         fotos_dir.mkdir(parents=True, exist_ok=True)

#         extensao = Path(foto.filename).suffix
#         nome_arquivo = f"{uuid.uuid4()}{extensao}"
#         caminho_arquivo = fotos_dir / nome_arquivo

#         conteudo = await foto.read()
#         with open(caminho_arquivo, "wb") as f:
#             f.write(conteudo)

#         foto_url = (
#             f"/tmp/sistema-de-doacao-de-livros/fotos_instituicoes/"
#             f"{nome_arquivo}"
#         )

#     data_fundacao_parsed = date_type.fromisoformat(data_fundacao)

#     instituicao_atualizada = banco_de_dados.atualizar_instituicao(
#         instituicao_id=instituicao_id,
#         nome=nome,
#         email=email,
#         descricao=descricao,
#         data_fundacao=data_fundacao_parsed,
#         endereco=endereco,
#         foto_url=foto_url,
#         site=site if site else None,
#         senha=nova_senha if nova_senha else None,
#     )

#     return esquemas.RespostaAtualizarInstituicao(
#         id=instituicao_atualizada.id,
#         nome=instituicao_atualizada.nome,
#         email=instituicao_atualizada.email,
#         descricao=instituicao_atualizada.descricao,
#         data_fundacao=instituicao_atualizada.data_fundacao,
#         data_registro=instituicao_atualizada.data_registro,
#         livros_recebidos=instituicao_atualizada.livros_recebidos,
#         foto_url=instituicao_atualizada.foto_url,
#         site=instituicao_atualizada.site,
#         endereco=instituicao_atualizada.endereco,
#     )

# from datetime import date, datetime

# from pydantic import BaseModel, EmailStr


# class EntradaCriarInstituicao(BaseModel):
#     nome: str
#     email: EmailStr
#     senha: str
#     descricao: str
#     data_fundacao: date
#     foto_url: str | None = None
#     site: str | None = None
#     endereco: str


# class RespostaCriarInstituicao(BaseModel):
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


# class RespostaBuscarInstituicao(BaseModel):
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


# class RespostaListarInstituicoes(BaseModel):
#     instituicoes: list["ItemInstituicao"]
#     total: int
#     pagina: int
#     tamanho_pagina: int


# class ItemInstituicao(BaseModel):
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


# class RespostaAtualizarInstituicao(BaseModel):
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
