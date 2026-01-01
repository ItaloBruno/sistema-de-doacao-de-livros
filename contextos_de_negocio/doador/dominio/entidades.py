from dataclasses import dataclass

from contextos_de_negocio.doador.dominio.objetos_de_valor import (
    DoadorId,
    EmailDoador,
    NomeDoador,
    SenhaDoador,
    TelefoneDoador,
)
from contextos_de_negocio.doador.excecoes import SenhaIncorreta


@dataclass
class Doador:
    nome: NomeDoador
    email: EmailDoador
    telefone: TelefoneDoador
    senha: SenhaDoador
    id: DoadorId | None = None

    @staticmethod
    def criar(
        nome: NomeDoador,
        email: EmailDoador,
        telefone: TelefoneDoador,
        senha: SenhaDoador,
    ) -> "Doador":
        return Doador(
            id=DoadorId.gerar(),
            nome=nome,
            email=email,
            telefone=telefone,
            senha=senha,
        )

    def editar(
        self,
        senha_atual: SenhaDoador,
        nome: NomeDoador,
        email: EmailDoador,
        telefone: TelefoneDoador,
        nova_senha: SenhaDoador | None = None,
    ) -> None:
        if self.senha != senha_atual:
            raise SenhaIncorreta()

        self.nome = nome
        self.email = email
        self.telefone = telefone

        if nova_senha is not None:
            self.senha = nova_senha
