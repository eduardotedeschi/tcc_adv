"""
Regras de negócio da tela de Teses (mesmo padrão de ModeloDocumentoController,
mas para a tabela `tese`, separada de `modelo_documento` no schema).
"""
import os
import shutil
from typing import List, Tuple

from config import TEMPLATES_DIR
from models.tese import Tese
from repositories.tese_repository import TeseRepository


class TeseController:

    def __init__(self):
        self.repo = TeseRepository()
        self.pasta_destino = os.path.join(TEMPLATES_DIR, "teses")

    def importar(self, nome: str, caminho_origem: str, area_direito_id: int = None) -> Tuple[bool, str]:
        if not nome.strip():
            return False, "O nome da tese é obrigatório."
        if not caminho_origem or not os.path.isfile(caminho_origem):
            return False, "Selecione um arquivo .docx válido."
        if not caminho_origem.lower().endswith(".docx"):
            return False, "O arquivo precisa estar no formato .docx (RF09)."

        os.makedirs(self.pasta_destino, exist_ok=True)
        caminho_destino = os.path.join(self.pasta_destino, os.path.basename(caminho_origem))
        shutil.copy2(caminho_origem, caminho_destino)

        tese = Tese(nome=nome.strip(), caminho_arquivo=caminho_destino, area_direito_id=area_direito_id)
        self.repo.inserir(tese)
        return True, "Tese importada com sucesso."

    def remover(self, tese_id: int, apagar_arquivo: bool = False) -> Tuple[bool, str]:
        tese = self.repo.buscar_por_id(tese_id)
        if not tese:
            return False, "Tese não encontrada."
        self.repo.deletar(tese_id)
        if apagar_arquivo and os.path.isfile(tese.caminho_arquivo):
            os.remove(tese.caminho_arquivo)
        return True, "Tese removida com sucesso."

    def listar(self) -> List[Tese]:
        return self.repo.listar_todas()

    def listar_por_area(self, area_direito_id: int) -> List[Tese]:
        return self.repo.listar_por_area(area_direito_id)
