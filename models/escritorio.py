from dataclasses import dataclass
from typing import Optional


@dataclass
class Escritorio:
    nome: str
    email: str
    senha_hash: str  # já contém "salt$hash" — ver controllers/auth_controller.py
    id: Optional[int] = None
