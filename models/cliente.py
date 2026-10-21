"""
Models = apenas estrutura de dados (dataclasses).
NUNCA colocar acesso a banco ou validação de regra de negócio aqui —
isso é papel do repository e do controller, respectivamente.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Cliente:
    nome: str
    cpf: str
    nacionalidade: str = ""
    estado_civil: str = ""
    profissao: str = ""
    rg: str = ""
    cep: str = ""
    uf: str = ""
    cidade: str = ""
    rua: str = ""
    numero: str = ""
    bairro: str = ""
    telefone: str = ""
    email: str = ""
    nome_reu: str = ""
    cnpj_reu: str = ""
    id: Optional[int] = None

    @staticmethod
    def from_row(row) -> "Cliente":
        """Converte uma sqlite3.Row em um objeto Cliente."""
        return Cliente(
            id=row["id"],
            nome=row["nome"],
            cpf=row["cpf"],
            nacionalidade=row["nacionalidade"],
            estado_civil=row["estado_civil"],
            profissao=row["profissao"],
            rg=row["rg"],
            cep=row["cep"],
            uf=row["uf"],
            cidade=row["cidade"],
            rua=row["rua"],
            numero=row["numero"],
            bairro=row["bairro"],
            telefone=row["telefone"],
            email=row["email"],
            nome_reu=row["nome_reu"],
            cnpj_reu=row["cnpj_reu"],
        )
