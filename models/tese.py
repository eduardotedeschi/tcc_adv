from dataclasses import dataclass
from typing import Optional


@dataclass
class Tese:
    nome: str
    caminho_arquivo: str
    area_direito_id: Optional[int] = None
    id: Optional[int] = None

    @staticmethod
    def from_row(row) -> "Tese":
        return Tese(
            id=row["id"],
            nome=row["nome"],
            caminho_arquivo=row["caminho_arquivo"],
            area_direito_id=row["area_direito_id"],
        )
