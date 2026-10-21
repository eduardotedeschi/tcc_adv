"""
Une o conteúdo de vários .docx (teses selecionadas) em um único arquivo,
na ordem informada. Atende RF01.

Observação: a biblioteca python-docx sozinha não faz merge nativo, então
usamos a técnica de copiar os elementos XML do corpo (`body`) de cada
documento de origem para o documento final.
"""
from typing import List

from docx import Document


def unir_documentos(caminhos_teses: List[str], caminho_saida: str, quebrar_pagina: bool = True) -> None:
    """
    caminhos_teses: lista de caminhos .docx JÁ NA ORDEM desejada
    (ver documento_gerado_tese.ordem).
    """
    if not caminhos_teses:
        raise ValueError("É necessário ao menos uma tese para gerar a petição (RF02).")

    documento_final = Document(caminhos_teses[0])

    for caminho in caminhos_teses[1:]:
        if quebrar_pagina:
            documento_final.add_page_break()
        documento_origem = Document(caminho)
        for elemento in documento_origem.element.body:
            documento_final.element.body.append(elemento)

    documento_final.save(caminho_saida)


def gerar_secao_pedidos(nomes_teses_em_ordem: List[str]) -> str:
    """
    Gera o texto da seção "Pedidos" a partir dos nomes das teses, na
    ordem em que aparecem no documento (RF03). Implementação inicial
    simples — o time deve refinar o texto jurídico conforme o padrão
    de petição usado pelo escritório.
    """
    linhas = ["Diante do exposto, requer-se:", ""]
    for i, nome_tese in enumerate(nomes_teses_em_ordem, start=1):
        linhas.append(f"{i}. Seja acolhido o pedido referente a: {nome_tese};")
    return "\n".join(linhas)
