"""
Integração com a API ViaCEP (REST), citada na Sprint II.docx.
Atende RF13: preenchimento automático de endereço a partir do CEP.
"""
import requests

from utils.validators import limpar_numeros


class CepInvalido(Exception):
    pass


class CepNaoEncontrado(Exception):
    pass


def buscar_endereco_por_cep(cep: str) -> dict:
    """
    Retorna {"rua": ..., "bairro": ..., "cidade": ..., "uf": ...}
    Lança CepInvalido ou CepNaoEncontrado em caso de erro, para a
    view decidir qual mensagem mostrar ao usuário.
    """
    cep_numeros = limpar_numeros(cep)
    if len(cep_numeros) != 8:
        raise CepInvalido("CEP deve conter 8 dígitos.")

    resposta = requests.get(f"https://viacep.com.br/ws/{cep_numeros}/json/", timeout=5)
    resposta.raise_for_status()
    dados = resposta.json()

    if dados.get("erro"):
        raise CepNaoEncontrado(f"CEP {cep_numeros} não encontrado.")

    return {
        "rua": dados.get("logradouro", ""),
        "bairro": dados.get("bairro", ""),
        "cidade": dados.get("localidade", ""),
        "uf": dados.get("uf", ""),
    }
