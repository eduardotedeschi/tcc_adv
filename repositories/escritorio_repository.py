from typing import Optional

from database.connection import db_cursor


class EscritorioRepository:

    def criar(self, nome: str, email: str, senha_hash: str) -> int:
        with db_cursor() as cur:
            cur.execute(
                "INSERT INTO escritorio (nome, email, senha_hash) VALUES (?,?,?)",
                (nome, email, senha_hash),
            )
            return cur.lastrowid

    def buscar_por_email(self, email: str) -> Optional[dict]:
        with db_cursor() as cur:
            cur.execute("SELECT * FROM escritorio WHERE email = ?", (email,))
            row = cur.fetchone()
            return dict(row) if row else None
