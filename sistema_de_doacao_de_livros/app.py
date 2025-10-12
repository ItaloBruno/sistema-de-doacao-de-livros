from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def pagina_inicial():
    return {'message': 'Olá Mundo!'}
