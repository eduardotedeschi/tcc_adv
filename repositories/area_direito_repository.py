from typing import List, Optional

from database.connection import db_cursor
from models.area_direito import AreaDireito


class AreaDireitoRepository:

    def inserir(self, nome: str) -> int:
        with db_cursor() as cur:
            cur.execute("INSERT INTO area_direito (nome) VALUES (?)", (nome,))
            return cur.lastrowid

    def deletar(self, area_id: int) -> None:
        with db_cursor() as cur:
            cur.execute("DELETE FROM area_direito WHERE id=?", (area_id,))

    def listar_todas(self) -> List[AreaDireito]:
        with db_cursor() as cur:
            cur.execute("SELECT * FROM area_direito ORDER BY nome")
            return [AreaDireito.from_row(r) for r in cur.fetchall()]

    def buscar_por_id(self, area_id: int) -> Optional[AreaDireito]:
        with db_cursor() as cur:
            cur.execute("SELECT * FROM area_direito WHERE id=?", (area_id,))
            row = cur.fetchone()
            return AreaDireito.from_row(row) if row else None
