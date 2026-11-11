"""
Apenas estrutura de dados
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ReuParteAdversa:

    nome: str
    documento_gerado_id: int
    cnpj_cpf: str = ""
    id: Optional[int] = None

    @staticmethod
    def from_row(row) -> "ReuParteAdversa":
        return ReuParteAdversa(
            id=row["id"],
            nome=row["nome"],
            cnpj_cpf=row["cnpj_cpf"],
            documento_gerado_id=row["documento_gerado_id"],
        )
