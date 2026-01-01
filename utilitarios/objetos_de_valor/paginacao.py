from dataclasses import dataclass


@dataclass(frozen=True)
class NumeroPagina:
    valor: int

    def __post_init__(self):
        if self.valor < 1:
            raise ValueError(f"Página deve ser >= 1, recebido: {self.valor}")


@dataclass(frozen=True)
class ItensPorPagina:
    valor: int
    MAXIMO = 100
    MINIMO = 1

    def __post_init__(self):
        if self.valor < self.MINIMO:
            raise ValueError(
                f"Itens por página deve ser >= {self.MINIMO}, "
                f"recebido: {self.valor}"
            )
        if self.valor > self.MAXIMO:
            raise ValueError(
                f"Itens por página deve ser <= {self.MAXIMO}, "
                f"recebido: {self.valor}"
            )
