from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr


class TipoUsuario(str, Enum):
    DOADOR = "doador"
    INSTITUICAO = "instituicao"


class StatusDoacao(str, Enum):
    PENDENTE = "pendente"
    ACEITA = "aceita"
    REJEITADA = "rejeitada"
    CONCLUIDA = "concluida"


class DadosParaRealizarOperacoesEmUsuario(BaseModel):
    nome: str
    email: EmailStr
    senha: str


class CriacaoDeUsuario(DadosParaRealizarOperacoesEmUsuario):
    pass


class AtualizacaoDeUsuario(DadosParaRealizarOperacoesEmUsuario):
    pass


class Usuario(BaseModel):
    id: int
    nome: str
    email: EmailStr


class UsuarioCriado(Usuario):
    pass


class UsuarioAtualizado(Usuario):
    pass


class UsuarioDB(CriacaoDeUsuario):
    id: int


class ListagemDeUsuario(BaseModel):
    usuarios: list[Usuario]


class UsuarioEspecifico(Usuario):
    pass


class CriacaoDeDoador(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    telefone: str


class Doador(BaseModel):
    id: int
    nome: str
    email: EmailStr
    telefone: str


class DoadorDB(CriacaoDeDoador):
    id: int


class CriacaoDeInstituicao(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    descricao: str
    data_fundacao: date
    foto_url: Optional[str] = None
    site: Optional[str] = None
    endereco: str


class Instituicao(BaseModel):
    id: int
    nome: str
    email: EmailStr
    descricao: str
    data_fundacao: date
    data_registro: datetime
    livros_recebidos: int
    foto_url: Optional[str] = None
    site: Optional[str] = None
    endereco: str


class InstituicaoDB(CriacaoDeInstituicao):
    id: int
    data_registro: datetime
    livros_recebidos: int


class ListagemDeInstituicoes(BaseModel):
    instituicoes: list[Instituicao]
    total: int
    pagina: int
    tamanho_pagina: int


class CriacaoDeLivro(BaseModel):
    titulo: str
    subtitulo: Optional[str] = None
    autores: list[str]
    isbn: Optional[str] = None


class Livro(BaseModel):
    id: int
    titulo: str
    subtitulo: Optional[str] = None
    autores: list[str]
    isbn: Optional[str] = None


class LivroDB(CriacaoDeLivro):
    id: int


class LivroNaDoacao(BaseModel):
    livro_id: int
    foto_url: Optional[str] = None
    observacao: Optional[str] = None


class LivroNaDoacaoCompleto(BaseModel):
    id: int
    livro: Livro
    foto_url: Optional[str] = None
    observacao: Optional[str] = None


class CriacaoDeDoacao(BaseModel):
    instituicao_id: int
    doador_id: Optional[int] = None
    doador_nome: Optional[str] = None
    doador_email: Optional[EmailStr] = None
    doador_senha: Optional[str] = None
    doador_telefone: Optional[str] = None
    livros: list[LivroNaDoacao]


class Doacao(BaseModel):
    id: int
    instituicao_id: int
    instituicao_nome: str
    doador_id: int
    doador_nome: str
    data_criacao: datetime
    status: StatusDoacao
    quantidade_livros: int


class DoacaoCompleta(BaseModel):
    id: int
    instituicao: Instituicao
    doador: Doador
    data_criacao: datetime
    status: StatusDoacao
    livros: list[LivroNaDoacaoCompleto]


class DoacaoDB(BaseModel):
    id: int
    instituicao_id: int
    doador_id: int
    data_criacao: datetime
    status: StatusDoacao


class AtualizacaoStatusDoacao(BaseModel):
    status: StatusDoacao


class ListagemDeDoacoes(BaseModel):
    doacoes: list[Doacao]


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class LoginResponse(BaseModel):
    usuario_id: int
    nome: str
    email: EmailStr
    tipo: TipoUsuario
    mensagem: str


class RespostaDoSistema(BaseModel):
    mensagem: str
