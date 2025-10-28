from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from sistema_de_doacao_de_livros.app import app


@pytest.fixture
def cliente():
    return TestClient(app)


def test_pagina_inicial_deve_retornar_ok_e_ola_mundo(cliente):
    resposta = cliente.get("/api/")

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {"message": "Olá Mundo!"}


def teste_criar_usuario(cliente):
    resposta = cliente.post(
        "/api/usuarios/",
        json={
            "nome": "alice",
            "email": "alice@example.com",
            "senha": "secret",
        },
    )
    assert resposta.status_code == HTTPStatus.CREATED
    assert resposta.json() == {
        "nome": "alice",
        "email": "alice@example.com",
        "id": 1,
    }


def teste_buscar_usuarios(cliente):
    resposta = cliente.get("/api/usuarios/")
    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {
        "usuarios": [
            {
                "nome": "alice",
                "email": "alice@example.com",
                "id": 1,
            }
        ]
    }


def teste_atualizar_usuario(cliente):
    resposta = cliente.put(
        "/api/usuarios/1",
        json={
            "nome": "bob",
            "email": "bob@example.com",
            "senha": "mynewpassword",
        },
    )
    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {
        "nome": "bob",
        "email": "bob@example.com",
        "id": 1,
    }


def teste_erro_usuario_nao_encontrado_ao_atualizar_usuario(cliente):
    resposta = cliente.put(
        "/api/usuarios/5",
        json={
            "nome": "bob",
            "email": "bob@example.com",
            "senha": "mynewpassword",
        },
    )
    assert resposta.status_code == HTTPStatus.NOT_FOUND
    assert resposta.json() == {"detail": "Usuário não encontrado"}


def teste_buscar_usuario_especifico(cliente):
    resposta = cliente.get("/api/usuarios/1")
    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {
        "nome": "bob",
        "email": "bob@example.com",
        "id": 1,
    }


def teste_erro_usuario_nao_encontrado_ao_buscar_usuario_especifico(cliente):
    resposta = cliente.get("/api/usuarios/5")
    assert resposta.status_code == HTTPStatus.NOT_FOUND
    assert resposta.json() == {"detail": "Usuário não encontrado"}


def teste_deletar_usuario(cliente):
    resposta = cliente.delete("/api/usuarios/1")

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {"mensagem": "Usuário deletado"}


def teste_erro_usuario_nao_encontrado_ao_deletar_usuario(cliente):
    resposta = cliente.delete(
        "/api/usuarios/5",
    )
    assert resposta.status_code == HTTPStatus.NOT_FOUND
    assert resposta.json() == {"detail": "Usuário não encontrado"}
