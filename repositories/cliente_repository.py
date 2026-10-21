"""
Repository = única camada que fala SQL.
Se amanhã vocês trocarem SQLite por outro banco, só este arquivo muda —
controllers e views nem percebem a diferença.
"""
from typing import List, Optional

from database.connection import db_cursor
from models.cliente import Cliente


class ClienteRepository:

    def inserir(self, cliente: Cliente) -> int:
        with db_cursor() as cur:
            cur.execute(
                """
                INSERT INTO cliente
                    (nome, nacionalidade, estado_civil, profissao, rg, cpf, cep,
                     uf, cidade, rua, numero, bairro, telefone, email,
                     nome_reu, cnpj_reu)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    cliente.nome, cliente.nacionalidade, cliente.estado_civil,
                    cliente.profissao, cliente.rg, cliente.cpf, cliente.cep,
                    cliente.uf, cliente.cidade, cliente.rua, cliente.numero,
                    cliente.bairro, cliente.telefone, cliente.email,
                    cliente.nome_reu, cliente.cnpj_reu,
                ),
            )
            return cur.lastrowid

    def atualizar(self, cliente: Cliente) -> None:
        with db_cursor() as cur:
            cur.execute(
                """
                UPDATE cliente SET
                    nome=?, nacionalidade=?, estado_civil=?, profissao=?, rg=?,
                    cpf=?, cep=?, uf=?, cidade=?, rua=?, numero=?, bairro=?,
                    telefone=?, email=?, nome_reu=?, cnpj_reu=?
                WHERE id=?
                """,
                (
                    cliente.nome, cliente.nacionalidade, cliente.estado_civil,
                    cliente.profissao, cliente.rg, cliente.cpf, cliente.cep,
                    cliente.uf, cliente.cidade, cliente.rua, cliente.numero,
                    cliente.bairro, cliente.telefone, cliente.email,
                    cliente.nome_reu, cliente.cnpj_reu, cliente.id,
                ),
            )

    def deletar(self, cliente_id: int) -> None:
        with db_cursor() as cur:
            cur.execute("DELETE FROM cliente WHERE id=?", (cliente_id,))

    def listar_todos(self) -> List[Cliente]:
        with db_cursor() as cur:
            cur.execute("SELECT * FROM cliente ORDER BY nome")
            return [Cliente.from_row(r) for r in cur.fetchall()]

    def buscar(self, termo: str) -> List[Cliente]:
        with db_cursor() as cur:
            termo = termo.strip()
            if termo.isdigit():
                cur.execute(
                    "SELECT * FROM cliente WHERE cpf LIKE ? OR id = ? ORDER BY nome",
                    (f"%{termo}%", termo),
                )
            else:
                cur.execute(
                    "SELECT * FROM cliente WHERE LOWER(nome) LIKE ? ORDER BY nome",
                    (f"%{termo.lower()}%",),
                )
            return [Cliente.from_row(r) for r in cur.fetchall()]

    def buscar_por_cpf(self, cpf: str) -> Optional[Cliente]:
        with db_cursor() as cur:
            cur.execute("SELECT * FROM cliente WHERE cpf = ?", (cpf,))
            row = cur.fetchone()
            return Cliente.from_row(row) if row else None

    def buscar_por_id(self, cliente_id: int) -> Optional[Cliente]:
        with db_cursor() as cur:
            cur.execute("SELECT * FROM cliente WHERE id = ?", (cliente_id,))
            row = cur.fetchone()
            return Cliente.from_row(row) if row else None
