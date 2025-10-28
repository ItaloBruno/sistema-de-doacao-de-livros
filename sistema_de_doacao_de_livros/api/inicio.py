from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def api_inicio():
    return {"message": "Olá Mundo!"}
