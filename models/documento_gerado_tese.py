"""
Apenas estrutura de dados
registra quais teses compõem uma petição e em que sequência elas entram no documento final
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DocumentoGeradoTese:
    documento_gerado_id: int
    tese_id: int
    ordem: int = 1
    id: Optional[int] = None

    @staticmethod
    def from_row(row) -> "DocumentoGeradoTese":
        return DocumentoGeradoTese(
            id=row["id"],
            documento_gerado_id=row["documento_gerado_id"],
            tese_id=row["tese_id"],
            ordem=row["ordem"],
        )
