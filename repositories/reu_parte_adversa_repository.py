from typing import List

from database.connection import db_cursor
from models.reu_parte_adversa import ReuParteAdversa


class ReuParteAdversaRepository:

    def inserir(self, reu: ReuParteAdversa) -> int:
        with db_cursor() as cur:
            cur.execute(
                """INSERT INTO reu_parte_adversa (nome, cnpj_cpf, documento_gerado_id)
                   VALUES (?,?,?)""",
                (reu.nome, reu.cnpj_cpf, reu.documento_gerado_id),
            )
            return cur.lastrowid

    def listar_por_documento(self, documento_gerado_id: int) -> List[ReuParteAdversa]:
        with db_cursor() as cur:
            cur.execute(
                "SELECT * FROM reu_parte_adversa WHERE documento_gerado_id=?",
                (documento_gerado_id,),
            )
            return [ReuParteAdversa.from_row(r) for r in cur.fetchall()]
