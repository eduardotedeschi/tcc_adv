"""
Apenas estrutura de dados
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class AreaDireito:
    nome: str
    id: Optional[int] = None

    @staticmethod
    def from_row(row) -> "AreaDireito":
        return AreaDireito(id=row["id"], nome=row["nome"])
