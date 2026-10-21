from typing import List, Optional

from database.connection import db_cursor
from models.tese import Tese


class TeseRepository:

    def inserir(self, tese: Tese) -> int:
        with db_cursor() as cur:
            cur.execute(
                "INSERT INTO tese (nome, caminho_arquivo, area_direito_id) VALUES (?,?,?)",
                (tese.nome, tese.caminho_arquivo, tese.area_direito_id),
            )
            return cur.lastrowid

    def deletar(self, tese_id: int) -> None:
        with db_cursor() as cur:
            cur.execute("DELETE FROM tese WHERE id=?", (tese_id,))

    def listar_todas(self) -> List[Tese]:
        with db_cursor() as cur:
            cur.execute("SELECT * FROM tese ORDER BY nome")
            return [Tese.from_row(r) for r in cur.fetchall()]

    def listar_por_area(self, area_direito_id: int) -> List[Tese]:
        with db_cursor() as cur:
            cur.execute(
                "SELECT * FROM tese WHERE area_direito_id=? ORDER BY nome",
                (area_direito_id,),
            )
            return [Tese.from_row(r) for r in cur.fetchall()]

    def buscar_por_id(self, tese_id: int) -> Optional[Tese]:
        with db_cursor() as cur:
            cur.execute("SELECT * FROM tese WHERE id=?", (tese_id,))
            row = cur.fetchone()
            return Tese.from_row(row) if row else None

    def buscar_por_ids(self, tese_ids: List[int]) -> List[Tese]:
        """Usado pelo gerar_peticao_controller para carregar as teses selecionadas."""
        if not tese_ids:
            return []
        with db_cursor() as cur:
            marcadores = ",".join("?" * len(tese_ids))
            cur.execute(f"SELECT * FROM tese WHERE id IN ({marcadores})", tese_ids)
            return [Tese.from_row(r) for r in cur.fetchall()]
