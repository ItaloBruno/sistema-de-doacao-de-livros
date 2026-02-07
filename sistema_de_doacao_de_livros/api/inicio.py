from fastapi import APIRouter

rotas_api_inicio = APIRouter()


@rotas_api_inicio.get("/")
def api_inicio():
    return {"message": "Olá Mundo!"}
