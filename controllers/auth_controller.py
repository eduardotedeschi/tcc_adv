"""
Regras de autenticação. Usa hashlib.pbkdf2 (biblioteca padrão do Python,
sem dependência extra) para nunca guardar senha em texto puro no banco —
importante para RNF05 (compatibilidade/segurança) do levantamento de
requisitos.
"""
import hashlib
import hmac
import os
from typing import Tuple

from repositories.escritorio_repository import EscritorioRepository

_ITERACOES = 200_000


def _gerar_hash(senha: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", senha.encode(), salt, _ITERACOES).hex()


def criar_hash_senha(senha: str) -> str:
    salt = os.urandom(16)
    return f"{salt.hex()}${_gerar_hash(senha, salt)}"


def verificar_senha(senha: str, hash_armazenado: str) -> bool:
    salt_hex, hash_esperado = hash_armazenado.split("$")
    hash_calculado = _gerar_hash(senha, bytes.fromhex(salt_hex))
    return hmac.compare_digest(hash_calculado, hash_esperado)


class AuthController:

    def __init__(self):
        self.repo = EscritorioRepository()

    def cadastrar_escritorio(self, nome: str, email: str, senha: str) -> Tuple[bool, str]:
        if not nome.strip() or not email.strip() or not senha:
            return False, "Preencha nome, e-mail e senha."
        if len(senha) < 6:
            return False, "A senha deve ter pelo menos 6 caracteres."
        if self.repo.buscar_por_email(email.strip().lower()):
            return False, "Já existe um escritório cadastrado com este e-mail."

        self.repo.criar(nome.strip(), email.strip().lower(), criar_hash_senha(senha))
        return True, "Escritório cadastrado com sucesso."

    def autenticar(self, email: str, senha: str) -> Tuple[bool, str]:
        escritorio = self.repo.buscar_por_email(email.strip().lower())
        if not escritorio or not verificar_senha(senha, escritorio["senha_hash"]):
            return False, "E-mail ou senha inválidos."
        return True, "Login realizado com sucesso."
