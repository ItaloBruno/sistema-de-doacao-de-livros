import pytest
from fastapi.testclient import TestClient

from sistema_de_doacao_de_livros.app import app


@pytest.fixture
def cliente():
    return TestClient(app)
