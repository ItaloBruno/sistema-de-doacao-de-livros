from dataclasses import dataclass
from enum import Enum

from utilitarios.excecoes.filtragem import (
    FormatoFiltroInvalido,
    OperadorFiltroInvalido,
)


class OperadorFiltro(str, Enum):
    IGUAL = "igual"
    DIFERENTE = "diferente"
    MAIOR_QUE = "maior-que"
    MAIOR_OU_IGUAL = "maior-ou-igual"
    MENOR_QUE = "menor-que"
    MENOR_OU_IGUAL = "menor-ou-igual"
    CONTEM = "contem"
    COMECA_COM = "comeca-com"
    TERMINA_COM = "termina-com"
    EM = "em"
    NAO_EM = "nao-em"
    E_NULO = "e-nulo"
    NAO_E_NULO = "nao-e-nulo"


@dataclass(frozen=True)
class CampoFiltro:
    nome: str


@dataclass(frozen=True)
class Filtro:
    campo: CampoFiltro
    operador: OperadorFiltro
    valor: str

    @classmethod
    def de_string(cls, campo, operador_e_valor):
        if "." not in operador_e_valor:
            raise FormatoFiltroInvalido(operador_e_valor=operador_e_valor)

        operador_str, valor = operador_e_valor.split(".", 1)

        try:
            operador = OperadorFiltro(operador_str)
        except ValueError:
            raise OperadorFiltroInvalido(operador=operador_str)

        return cls(
            campo=CampoFiltro(campo),
            operador=operador,
            valor=valor,
        )


@dataclass(frozen=True)
class ConjuntoFiltros:
    filtros: tuple

    @classmethod
    def de_dict(cls, filtros_dict):
        filtros = []
        for campo, operador_e_valor in filtros_dict.items():
            try:
                filtro = Filtro.de_string(campo, operador_e_valor)
                filtros.append(filtro)
            except (
                ValueError,
                KeyError,
                FormatoFiltroInvalido,
                OperadorFiltroInvalido,
            ):
                continue
        return cls(filtros=tuple(filtros))

    def para_dict(self):
        return {
            f.campo.nome: f"{f.operador.value}.{f.valor}" for f in self.filtros
        }
