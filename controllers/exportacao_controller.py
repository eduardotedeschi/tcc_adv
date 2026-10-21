"""
Exportação do documento final (RF14). Conversão para PDF depende de um
motor externo (ex.: docx2pdf no Windows, ou LibreOffice headless em
outros SOs) — deixado como TODO porque a escolha depende do ambiente
de cada máquina do time.
"""
import os
import shutil
from typing import Tuple


class ExportacaoController:

    def exportar_docx(self, caminho_origem: str, pasta_destino: str) -> Tuple[bool, str]:
        if not os.path.isfile(caminho_origem):
            return False, "Documento de origem não encontrado."
        os.makedirs(pasta_destino, exist_ok=True)
        destino = os.path.join(pasta_destino, os.path.basename(caminho_origem))
        shutil.copy2(caminho_origem, destino)
        return True, f"Documento exportado para: {destino}"

    def exportar_pdf(self, caminho_origem: str, pasta_destino: str) -> Tuple[bool, str]:
        # TODO: integrar biblioteca de conversão .docx -> .pdf
        # (ex.: docx2pdf no Windows ou `soffice --headless --convert-to pdf`
        # via LibreOffice em Linux/Mac). Decisão de equipe pendente.
        return False, "Exportação em PDF ainda não implementada."
