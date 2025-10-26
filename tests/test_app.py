from http import HTTPStatus

from fastapi.testclient import TestClient

from sistema_de_doacao_de_livros.app import app


def test_pagina_inicial_deve_retornar_ok_e_ola_mundo():
    cliente = TestClient(app)

    resposta = cliente.get('/api/')

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {'message': 'Olá Mundo!'}
