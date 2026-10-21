"""
Testes de integração leves do ClienteController, usando um banco SQLite
temporário (não mexe no banco real de desenvolvimento).
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
config.DATABASE_PATH = os.path.join(tempfile.gettempdir(), "test_sistema_advogados.db")

from database.connection import init_db
from controllers.cliente_controller import ClienteController

CLIENTE_VALIDO = {
    "nome": "Maria da Silva",
    "nacionalidade": "brasileira",
    "estado_civil": "solteira",
    "profissao": "advogada",
    "rg": "12.345.678-9",
    "cpf": "111.444.777-35",
    "cep": "13000-000",
    "uf": "SP",
    "cidade": "Americana",
    "rua": "Rua das Flores",
    "numero": "100",
    "bairro": "Centro",
}


def setup_function():
    if os.path.exists(config.DATABASE_PATH):
        os.remove(config.DATABASE_PATH)
    init_db()


def test_cadastrar_cliente_valido():
    controller = ClienteController()
    sucesso, mensagem = controller.cadastrar(CLIENTE_VALIDO)
    assert sucesso is True
    assert len(controller.listar()) == 1


def test_cadastrar_cliente_cpf_invalido():
    controller = ClienteController()
    dados = dict(CLIENTE_VALIDO, cpf="111.111.111-11")
    sucesso, mensagem = controller.cadastrar(dados)
    assert sucesso is False
    assert "CPF" in mensagem


def test_cadastrar_cliente_campo_obrigatorio_faltando():
    controller = ClienteController()
    dados = dict(CLIENTE_VALIDO, nome="")
    sucesso, mensagem = controller.cadastrar(dados)
    assert sucesso is False


def test_nao_permite_cpf_duplicado():
    controller = ClienteController()
    controller.cadastrar(CLIENTE_VALIDO)
    sucesso, mensagem = controller.cadastrar(CLIENTE_VALIDO)
    assert sucesso is False
    assert "CPF" in mensagem
