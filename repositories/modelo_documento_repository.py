from typing import List, Optional

from database.connection import db_cursor
from models.modelo_documento import ModeloDocumento


class ModeloDocumentoRepository:

    def inserir(self, modelo: ModeloDocumento) -> int:
        with db_cursor() as cur:
            cur.execute(
                """INSERT INTO modelo_documento (nome, tipo, caminho_arquivo, area_direito_id)
                   VALUES (?,?,?,?)""",
                (modelo.nome, modelo.tipo, modelo.caminho_arquivo, modelo.area_direito_id),
            )
            return cur.lastrowid

    def deletar(self, modelo_id: int) -> None:
        with db_cursor() as cur:
            cur.execute("DELETE FROM modelo_documento WHERE id=?", (modelo_id,))

    def listar_todos(self) -> List[ModeloDocumento]:
        with db_cursor() as cur:
            cur.execute("SELECT * FROM modelo_documento ORDER BY nome")
            return [ModeloDocumento.from_row(r) for r in cur.fetchall()]

    def buscar(self, termo: str) -> List[ModeloDocumento]:
        with db_cursor() as cur:
            cur.execute(
                "SELECT * FROM modelo_documento WHERE LOWER(nome) LIKE ? ORDER BY nome",
                (f"%{termo.lower()}%",),
            )
            return [ModeloDocumento.from_row(r) for r in cur.fetchall()]

    def buscar_por_id(self, modelo_id: int) -> Optional[ModeloDocumento]:
        with db_cursor() as cur:
            cur.execute("SELECT * FROM modelo_documento WHERE id=?", (modelo_id,))
            row = cur.fetchone()
            return ModeloDocumento.from_row(row) if row else None
