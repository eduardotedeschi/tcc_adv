"""
Funções puras de validação — sem tkinter, sem banco, fáceis de testar
isoladamente (ver tests/test_validators.py).
Atende RF10, RF11 e RF12 do levantamento de requisitos.
"""
import re
from typing import Dict, List


def limpar_numeros(texto: str) -> str:
    """Remove tudo que não for dígito. Ex: '123.456.789-00' -> '12345678900'"""
    return re.sub(r"\D", "", texto or "")


def limpar_espacos(texto: str) -> str:
    """Remove espaços duplicados e nas pontas (RF11)."""
    return re.sub(r"\s+", " ", (texto or "").strip())


def validar_cpf(cpf: str) -> bool:
    """Valida CPF pelo algoritmo oficial dos dígitos verificadores (RF12)."""
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
    """
    Recebe {"Nome do campo": valor, ...} e devolve a lista dos que
    estão vazios — para exibir na tela algo como:
    "Campos obrigatórios não preenchidos: CPF, CEP".
    """
    return [nome for nome, valor in campos.items() if not str(valor or "").strip()]
