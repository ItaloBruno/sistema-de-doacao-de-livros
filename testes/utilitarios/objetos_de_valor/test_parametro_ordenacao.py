import pytest

from utilitarios.objetos_de_valor.parametro_ordenacao import ParametroOrdenacao


def test_criar_parametro_ordenacao_ascendente():
    parametro = ParametroOrdenacao(campo="nome", direcao="asc")

    assert parametro.campo == "nome"
    assert parametro.direcao == "asc"


def test_criar_parametro_ordenacao_descendente():
    parametro = ParametroOrdenacao(campo="preco", direcao="desc")

    assert parametro.campo == "preco"
    assert parametro.direcao == "desc"


def test_criar_parametro_ordenacao_com_direcao_invalida():
    with pytest.raises(ValueError, match="Direção deve ser 'asc' ou 'desc'"):
        ParametroOrdenacao(campo="nome", direcao="invalido")


def test_de_string_com_formato_valido_asc():
    parametro = ParametroOrdenacao.de_string("nome.asc")

    assert parametro.campo == "nome"
    assert parametro.direcao == "asc"


def test_de_string_com_formato_valido_desc():
    parametro = ParametroOrdenacao.de_string("preco.desc")

    assert parametro.campo == "preco"
    assert parametro.direcao == "desc"


def test_de_string_sem_ponto():
    parametro = ParametroOrdenacao.de_string("nome")

    assert parametro is None


def test_de_string_com_direcao_invalida():
    parametro = ParametroOrdenacao.de_string("nome.invalido")

    assert parametro is None


def test_de_string_vazio():
    parametro = ParametroOrdenacao.de_string("")

    assert parametro is None


def test_de_string_none():
    parametro = ParametroOrdenacao.de_string(None)

    assert parametro is None


def test_de_lista_strings_com_multiplos_campos():
    parametros = ParametroOrdenacao.de_lista_strings("nome.asc,preco.desc")

    assert len(parametros) == 2
    assert parametros[0].campo == "nome"
    assert parametros[0].direcao == "asc"
    assert parametros[1].campo == "preco"
    assert parametros[1].direcao == "desc"


def test_de_lista_strings_com_campo_unico():
    parametros = ParametroOrdenacao.de_lista_strings("nome.asc")

    assert len(parametros) == 1
    assert parametros[0].campo == "nome"
    assert parametros[0].direcao == "asc"


def test_de_lista_strings_com_campos_invalidos():
    parametros = ParametroOrdenacao.de_lista_strings(
        "nome,preco.invalido,categoria.asc"
    )

    assert len(parametros) == 1
    assert parametros[0].campo == "categoria"
    assert parametros[0].direcao == "asc"


def test_de_lista_strings_vazio():
    parametros = ParametroOrdenacao.de_lista_strings("")

    assert parametros == []


def test_de_lista_strings_none():
    parametros = ParametroOrdenacao.de_lista_strings(None)

    assert parametros == []


def test_para_string():
    parametro = ParametroOrdenacao(campo="nome", direcao="asc")

    assert parametro.para_string() == "nome.asc"


def test_para_string_desc():
    parametro = ParametroOrdenacao(campo="preco", direcao="desc")

    assert parametro.para_string() == "preco.desc"
