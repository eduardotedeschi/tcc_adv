"""
Funções puras de validação
"""
import re
from typing import Dict, List


def limpar_numeros(texto: str) -> str:
    return re.sub(r"\D", "", texto or "")


def limpar_espacos(texto: str) -> str:
    return re.sub(r"\s+", " ", (texto or "").strip())


def validar_cpf(cpf: str) -> bool:
    cpf = limpar_numeros(cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    for i in (9, 10):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(i))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True


def validar_campos_obrigatorios(campos: Dict[str, str]) -> List[str]:
    
    return [nome for nome, valor in campos.items() if not str(valor or "").strip()]
