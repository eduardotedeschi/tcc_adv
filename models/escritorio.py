"""
Apenas estrutura de dados
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Escritorio:
    nome: str
    email: str
    senha_hash: str
    id: Optional[int] = None
