"""
Regras de negócio da tela "Composição de Petição" (RF01, RF02, RF03).
Esta é a parte mais complexa do MVP: valida a seleção de teses, une os
arquivos .docx na ordem escolhida e gera a seção de Pedidos.
"""
import os
from typing import List, Tuple

from config import DOCUMENTOS_GERADOS_DIR
from models.documento_gerado import DocumentoGerado
from repositories.cliente_repository import ClienteRepository
from repositories.documento_gerado_repository import DocumentoGeradoRepository
from repositories.documento_gerado_tese_repository import DocumentoGeradoTeseRepository
from repositories.tese_repository import TeseRepository
from utils.docx_merge import gerar_secao_pedidos, unir_documentos


class GerarPeticaoController:

    def __init__(self):
        self.repo_tese = TeseRepository()
        self.repo_cliente = ClienteRepository()
        self.repo_documento = DocumentoGeradoRepository()
        self.repo_documento_tese = DocumentoGeradoTeseRepository()

    def gerar(self, cliente_id: int, tese_ids_em_ordem: List[int]) -> Tuple[bool, str]:
        # RF02 / cardinalidade mínima 1:N — aplicada aqui, não no banco.
        if not tese_ids_em_ordem:
            return False, "Selecione ao menos uma tese pelo checklist."

        cliente = self.repo_cliente.buscar_por_id(cliente_id)
        if not cliente:
            return False, "Cliente inválido."

        teses = self.repo_tese.buscar_por_ids(tese_ids_em_ordem)
        # reordena conforme a ordem escolhida pelo usuário, não a ordem do banco
        teses_ordenadas = sorted(teses, key=lambda t: tese_ids_em_ordem.index(t.id))

        os.makedirs(DOCUMENTOS_GERADOS_DIR, exist_ok=True)
        nome_arquivo = f"Peticao_{cliente.nome}.docx".replace(" ", "_")
        caminho_saida = os.path.join(DOCUMENTOS_GERADOS_DIR, nome_arquivo)

        unir_documentos([t.caminho_arquivo for t in teses_ordenadas], caminho_saida)
        # TODO: acrescentar a seção de Pedidos (gerar_secao_pedidos) ao
        # final do documento unido — próximo passo, usando python-docx
        # para adicionar um parágrafo novo em `caminho_saida`.
        _ = gerar_secao_pedidos([t.nome for t in teses_ordenadas])

        documento = DocumentoGerado(
            cliente_id=cliente.id, nome_documento=nome_arquivo,
            tipo_documento="Petição", caminho_arquivo=caminho_saida,
        )
        documento_id = self.repo_documento.inserir(documento)
        self.repo_documento_tese.inserir_varias(documento_id, [t.id for t in teses_ordenadas])

        return True, f"Petição gerada em: {caminho_saida}"
