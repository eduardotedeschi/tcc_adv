from dataclasses import dataclass
from typing import Optional


@dataclass
class ModeloDocumento:
    nome: str
    tipo: str  # "Contrato" | "Declaração" | "Procuração" ...
    caminho_arquivo: str
    area_direito_id: Optional[int] = None
    id: Optional[int] = None

    @staticmethod
    def from_row(row) -> "ModeloDocumento":
        return ModeloDocumento(
            id=row["id"],
            nome=row["nome"],
            tipo=row["tipo"],
            caminho_arquivo=row["caminho_arquivo"],
            area_direito_id=row["area_direito_id"],
        )
