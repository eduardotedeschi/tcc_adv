"""
Regras de negócio da tela "Gerenciamento de Modelos" (RF05, RF09).
"""
import os
import shutil
from typing import List, Tuple

from config import TEMPLATES_DIR
from models.modelo_documento import ModeloDocumento
from repositories.modelo_documento_repository import ModeloDocumentoRepository


class ModeloDocumentoController:

    def __init__(self):
        self.repo = ModeloDocumentoRepository()
        self.pasta_destino = os.path.join(TEMPLATES_DIR, "modelos")

    def importar(self, nome: str, tipo: str, caminho_origem: str,
                  area_direito_id: int = None) -> Tuple[bool, str]:
        if not nome.strip() or not tipo.strip():
            return False, "Nome e tipo são obrigatórios."
        if not caminho_origem or not os.path.isfile(caminho_origem):
            return False, "Selecione um arquivo .docx válido."
        if not caminho_origem.lower().endswith(".docx"):
            return False, "O arquivo precisa estar no formato .docx (RF09)."

        os.makedirs(self.pasta_destino, exist_ok=True)
        caminho_destino = os.path.join(self.pasta_destino, os.path.basename(caminho_origem))
        shutil.copy2(caminho_origem, caminho_destino)

        modelo = ModeloDocumento(
            nome=nome.strip(), tipo=tipo.strip(),
            caminho_arquivo=caminho_destino, area_direito_id=area_direito_id,
        )
        self.repo.inserir(modelo)
        return True, "Modelo importado com sucesso."

    def remover(self, modelo_id: int, apagar_arquivo: bool = False) -> Tuple[bool, str]:
        modelo = self.repo.buscar_por_id(modelo_id)
        if not modelo:
            return False, "Modelo não encontrado."
        self.repo.deletar(modelo_id)
        if apagar_arquivo and os.path.isfile(modelo.caminho_arquivo):
            os.remove(modelo.caminho_arquivo)
        return True, "Modelo removido com sucesso."

    def listar(self) -> List[ModeloDocumento]:
        return self.repo.listar_todos()

    def buscar(self, termo: str) -> List[ModeloDocumento]:
        return self.repo.buscar(termo) if termo.strip() else self.listar()
