from pydantic import BaseModel


class EntradaCriarDoacao(BaseModel):
    instituicao_id: str
    livros_ids: list[str]


class RespostaCriarDoacao(BaseModel):
    id: str
    doador_id: str
    instituicao_id: str
    livros_ids: list[str]
