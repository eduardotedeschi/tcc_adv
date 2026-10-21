"""
Exemplo de teste automatizado. Rodar com: python -m pytest
Como os validators são funções puras (sem tkinter, sem banco), dá para
testar sem precisar abrir a interface gráfica.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validators import validar_cpf, limpar_numeros, validar_campos_obrigatorios


def test_cpf_valido():
    assert validar_cpf("111.444.777-35") is True


def test_cpf_invalido_sequencia_repetida():
    assert validar_cpf("111.111.111-11") is False


def test_cpf_invalido_tamanho_errado():
    assert validar_cpf("123") is False


def test_limpar_numeros():
    assert limpar_numeros("(19) 99876-5432") == "19998765432"


def test_campos_obrigatorios_detecta_vazio():
    faltando = validar_campos_obrigatorios({"Nome": "Caio", "CPF": "", "RG": "   "})
    assert faltando == ["CPF", "RG"]
