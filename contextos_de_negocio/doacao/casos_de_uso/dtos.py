from dataclasses import dataclass


@dataclass
class EntradaCriarDoacaoCasoDeUso:
    instituicao_id: str
    livros_ids: list[str]


@dataclass
class SaidaCriarDoacao:
    id: str
    doador_id: str
    instituicao_id: str
    livros_ids: list[str]
