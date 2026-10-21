from typing import List

from database.connection import db_cursor
from models.documento_gerado_tese import DocumentoGeradoTese


class DocumentoGeradoTeseRepository:

    def inserir_varias(self, documento_gerado_id: int, tese_ids: List[int]) -> None:
        """
        Grava as teses selecionadas para uma petição, preservando a ordem
        em que foram escolhidas (necessário para RF03 — seção de Pedidos
        seguir a ordem das teses no documento).
        """
        with db_cursor() as cur:
            for ordem, tese_id in enumerate(tese_ids, start=1):
                cur.execute(
                    """INSERT INTO documento_gerado_tese
                        (documento_gerado_id, tese_id, ordem) VALUES (?,?,?)""",
                    (documento_gerado_id, tese_id, ordem),
                )

    def listar_por_documento(self, documento_gerado_id: int) -> List[DocumentoGeradoTese]:
        with db_cursor() as cur:
            cur.execute(
                """SELECT * FROM documento_gerado_tese
                   WHERE documento_gerado_id=? ORDER BY ordem""",
                (documento_gerado_id,),
            )
            return [DocumentoGeradoTese.from_row(r) for r in cur.fetchall()]
