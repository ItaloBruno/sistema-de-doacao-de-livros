from utilitarios.objetos_de_valor.parametro_projecao import (
    ParametroProjecao,
)


def test_criar_parametro_projecao_com_um_campo():
    parametro = ParametroProjecao(campos=["nome"])

    assert parametro.campos == ["nome"]


def test_criar_parametro_projecao_com_multiplos_campos():
    parametro = ParametroProjecao(campos=["nome", "preco", "categoria"])

    assert parametro.campos == ["nome", "preco", "categoria"]


def test_de_string_com_campo_unico():
    parametro = ParametroProjecao.de_string("nome")

    assert parametro.campos == ["nome"]


def test_de_string_com_multiplos_campos():
    parametro = ParametroProjecao.de_string("nome,preco,categoria")

    assert parametro.campos == ["nome", "preco", "categoria"]


def test_de_string_com_espacos():
    parametro = ParametroProjecao.de_string("nome, preco , categoria")

    assert parametro.campos == ["nome", "preco", "categoria"]


def test_de_string_vazio():
    parametro = ParametroProjecao.de_string("")

    assert parametro is None


def test_de_string_none():
    parametro = ParametroProjecao.de_string(None)

    assert parametro is None


def test_de_string_apenas_virgulas():
    parametro = ParametroProjecao.de_string(",,,")

    assert parametro is None


def test_de_string_com_campos_vazios():
    parametro = ParametroProjecao.de_string("nome,,preco")

    assert parametro.campos == ["nome", "preco"]


def test_para_string_com_campo_unico():
    parametro = ParametroProjecao(campos=["nome"])

    assert parametro.para_string() == "nome"


def test_para_string_com_multiplos_campos():
    parametro = ParametroProjecao(campos=["nome", "preco", "categoria"])

    assert parametro.para_string() == "nome,preco,categoria"


def test_contem_campo_verdadeiro():
    parametro = ParametroProjecao(campos=["nome", "preco", "categoria"])

    assert parametro.contem_campo("nome") is True
    assert parametro.contem_campo("preco") is True


def test_contem_campo_falso():
    parametro = ParametroProjecao(campos=["nome", "preco"])

    assert parametro.contem_campo("categoria") is False
    assert parametro.contem_campo("id") is False
