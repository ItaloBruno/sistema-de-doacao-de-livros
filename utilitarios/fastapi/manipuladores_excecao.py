import traceback
from http import HTTPStatus

from fastapi.responses import JSONResponse


async def manipulador_excecao_base(request, exc):
    return JSONResponse(
        status_code=exc.codigo_status.value,
        content={
            "titulo": exc.titulo,
            "descricao": exc.descricao,
            "codigo_erro": exc.codigo_erro,
        },
    )


async def manipulador_excecao_generica(request, exc):
    print(f"Erro não tratado: {type(exc).__name__}: {exc}")
    traceback.print_exc()

    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        content={
            "titulo": "Erro interno do servidor",
            "descricao": (
                "Ocorreu um erro inesperado. Tente novamente mais tarde."
            ),
            "codigo_erro": "ERRO_INTERNO",
        },
    )
