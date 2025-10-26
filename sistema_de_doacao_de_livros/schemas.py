from pydantic import BaseModel, EmailStr


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


class RespostaDoSistema(BaseModel):
    mensagem: str
