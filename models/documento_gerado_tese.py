from dataclasses import dataclass
from typing import Optional


@dataclass
class DocumentoGeradoTese:
    """
    Tabela de junção (N:N com atributo `ordem`): registra quais teses
    compõem uma petição e em que sequência elas entram no documento
    final (usado para montar a seção de Pedidos na ordem certa).
    """
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
