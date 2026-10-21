from typing import List, Optional

from database.connection import db_cursor
from models.documento_gerado import DocumentoGerado


class DocumentoGeradoRepository:

    def inserir(self, doc: DocumentoGerado) -> int:
        with db_cursor() as cur:
            cur.execute(
                """INSERT INTO documento_gerado
                    (cliente_id, modelo_id, area_direito_id, nome_documento,
                     tipo_documento, caminho_arquivo)
                   VALUES (?,?,?,?,?,?)""",
                (doc.cliente_id, doc.modelo_id, doc.area_direito_id,
                 doc.nome_documento, doc.tipo_documento, doc.caminho_arquivo),
            )
            return cur.lastrowid

    def deletar(self, documento_id: int) -> None:
        with db_cursor() as cur:
            cur.execute("DELETE FROM documento_gerado WHERE id=?", (documento_id,))

    def listar_por_cliente(self, cliente_id: int) -> List[DocumentoGerado]:
        with db_cursor() as cur:
            cur.execute(
                "SELECT * FROM documento_gerado WHERE cliente_id=? ORDER BY data_gerada DESC",
                (cliente_id,),
            )
            return [DocumentoGerado.from_row(r) for r in cur.fetchall()]

    def buscar_por_cpf_cliente(self, cpf: str) -> List[DocumentoGerado]:
        """Atende RF07: consulta de documentos vinculados a um cliente por CPF."""
        with db_cursor() as cur:
            cur.execute(
                """SELECT documento_gerado.* FROM documento_gerado
                   JOIN cliente ON cliente.id = documento_gerado.cliente_id
                   WHERE cliente.cpf = ?
                   ORDER BY documento_gerado.data_gerada DESC""",
                (cpf,),
            )
            return [DocumentoGerado.from_row(r) for r in cur.fetchall()]

    def buscar_por_id(self, documento_id: int) -> Optional[DocumentoGerado]:
        with db_cursor() as cur:
            cur.execute("SELECT * FROM documento_gerado WHERE id=?", (documento_id,))
            row = cur.fetchone()
            return DocumentoGerado.from_row(row) if row else None
