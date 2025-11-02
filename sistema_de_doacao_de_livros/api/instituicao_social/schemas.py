from datetime import date

from pydantic import (
    BaseModel,
    EmailStr,
    HttpUrl,
    PastDate,
    constr,
    field_validator,
)
from pydantic_extra_types.phone_numbers import PhoneNumber

from sistema_de_doacao_de_livros.constantes import (
    ESTADOS_VALIDOS,
    TAMANHO_MINIMO_DO_CEP,
)


class Endereco(BaseModel):
    logradouro: constr(min_length=3, strip_whitespace=True)
    # aceita 12345-678 ou 12345678
    cep: constr(regex=r"^\d{5}-?\d{3}$")
    # ex: "123", "123A", "45-B"
    numero: constr(regex=r"^\d+[A-Za-z\-]*$")
    complemento: str | None = None
    bairro: constr(min_length=2, strip_whitespace=True)
    cidade: constr(min_length=2, strip_whitespace=True)
    # UF: SP, RJ, etc.
    estado: constr(min_length=2, max_length=2, strip_whitespace=True)

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, estado: str) -> str:
        """Valida que o estado é uma sigla brasileira válida."""
        estado = estado.upper()
        if estado not in ESTADOS_VALIDOS:
            raise ValueError(
                f"UF inválida: '{estado}' - "
                f"use siglas como 'SP', 'RJ', 'BA'..."
            )
        return estado

    @field_validator("cep")
    @classmethod
    def normalizar_cep(cls, cep: str) -> str:
        """
        Remove caracteres não numéricos e normaliza o CEP
        para o formato 12345-678.
        """
        numeros = "".join(filter(str.isdigit, cep))
        if len(numeros) != TAMANHO_MINIMO_DO_CEP:
            raise ValueError("CEP deve ter 8 dígitos numéricos.")
        return f"{numeros[:5]}-{numeros[5:]}"


class InstituicaoSocial(BaseModel):
    nome: str
    email_para_contato: EmailStr
    data_de_fundacao: PastDate
    descricao: str
    foto_representativa: None | HttpUrl
    endereco: Endereco
    site: None | HttpUrl
    telefone_para_contato: PhoneNumber


class InstituicaoSocialSalvaNoBanco(InstituicaoSocial):
    id: int
    data_de_registro: date


class CriacaoDeInstituicaoSocial(InstituicaoSocial):
    pass


class InstituicaoSocialRetornadaPelasAPIs(InstituicaoSocialSalvaNoBanco):
    pass


class InstituicaoSocialCriada(InstituicaoSocialRetornadaPelasAPIs):
    pass
