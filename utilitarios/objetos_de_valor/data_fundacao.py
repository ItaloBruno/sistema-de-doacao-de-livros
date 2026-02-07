from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class DataFundacao:
    valor: date

    def __str__(self) -> str:
        return self.valor.isoformat()
