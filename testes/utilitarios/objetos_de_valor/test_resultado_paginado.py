from utilitarios.objetos_de_valor.resultado_paginado import ResultadoPaginado


def test_resultado_paginado_calcula_total_paginas():
    resultado = ResultadoPaginado(
        itens=[1, 2, 3], total=10, pagina=1, itens_por_pagina=3
    )

    assert resultado.total_paginas == 4


def test_resultado_paginado_total_paginas_exato():
    resultado = ResultadoPaginado(
        itens=[1, 2, 3], total=9, pagina=1, itens_por_pagina=3
    )

    assert resultado.total_paginas == 3


def test_resultado_paginado_total_paginas_com_zero_itens():
    resultado = ResultadoPaginado(
        itens=[], total=0, pagina=1, itens_por_pagina=10
    )

    assert resultado.total_paginas == 0


def test_resultado_paginado_total_paginas_com_itens_por_pagina_zero():
    resultado = ResultadoPaginado(
        itens=[], total=10, pagina=1, itens_por_pagina=0
    )

    assert resultado.total_paginas == 0


def test_resultado_paginado_uma_pagina():
    resultado = ResultadoPaginado(
        itens=[1, 2, 3], total=3, pagina=1, itens_por_pagina=10
    )

    assert resultado.total_paginas == 1
