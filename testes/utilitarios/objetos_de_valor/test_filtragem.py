import pytest

from utilitarios.excecoes.filtragem import (
    FormatoFiltroInvalido,
    OperadorFiltroInvalido,
)
from utilitarios.objetos_de_valor.filtragem import ConjuntoFiltros, Filtro


def test_filtro_de_string_faz_parsing_correto():
    filtro = Filtro.de_string("titulo", "contem.Python")

    assert filtro.campo.nome == "titulo"
    assert filtro.operador.value == "contem"
    assert filtro.valor == "Python"


def test_filtro_de_string_preserva_pontos_no_valor():
    filtro = Filtro.de_string("preco", "maior-que.10.50")

    assert filtro.valor == "10.50"


def test_filtro_de_string_valida_formato():
    with pytest.raises(FormatoFiltroInvalido, match="Formato inválido"):
        Filtro.de_string("titulo", "sem_ponto")


def test_filtro_de_string_valida_operador():
    with pytest.raises(OperadorFiltroInvalido, match="operador-invalido"):
        Filtro.de_string("titulo", "operador-invalido.valor")


def test_conjunto_filtros_ignora_filtros_invalidos():
    conjunto = ConjuntoFiltros.de_dict(
        {
            "titulo": "contem.Python",
            "campo_invalido": "sem_ponto",
            "outro": "operador-invalido.valor",
        }
    )

    assert len(conjunto.filtros) == 1
    assert conjunto.filtros[0].campo.nome == "titulo"


def test_conjunto_filtros_conversao_bidirecional():
    dados_originais = {"titulo": "contem.Python", "preco": "maior-que.50"}
    conjunto = ConjuntoFiltros.de_dict(dados_originais)

    resultado = conjunto.para_dict()

    assert resultado == dados_originais
