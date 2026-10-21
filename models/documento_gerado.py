from dataclasses import dataclass
from typing import Optional


@dataclass
class DocumentoGerado:
    cliente_id: int
    nome_documento: str
    modelo_id: Optional[int] = None
    area_direito_id: Optional[int] = None
    tipo_documento: str = ""
    caminho_arquivo: str = ""
    data_gerada: str = ""
    id: Optional[int] = None

    @staticmethod
    def from_row(row) -> "DocumentoGerado":
        return DocumentoGerado(
            id=row["id"],
            cliente_id=row["cliente_id"],
            modelo_id=row["modelo_id"],
            area_direito_id=row["area_direito_id"],
            nome_documento=row["nome_documento"],
            tipo_documento=row["tipo_documento"],
            caminho_arquivo=row["caminho_arquivo"],
            data_gerada=row["data_gerada"],
        )
