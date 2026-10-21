"""
Regras de negócio da tela "Geração de Documento" (RF04, tela de geração
de documento do escopo).
"""
import os
from dataclasses import asdict
from typing import Tuple

from config import DOCUMENTOS_GERADOS_DIR
from models.documento_gerado import DocumentoGerado
from repositories.cliente_repository import ClienteRepository
from repositories.documento_gerado_repository import DocumentoGeradoRepository
from repositories.modelo_documento_repository import ModeloDocumentoRepository
from utils.docx_variaveis import extrair_variaveis, substituir_variaveis


class GerarDocumentoController:

    def __init__(self):
        self.repo_documento = DocumentoGeradoRepository()
        self.repo_modelo = ModeloDocumentoRepository()
        self.repo_cliente = ClienteRepository()

    def variaveis_pendentes(self, modelo_id: int) -> set:
        """Lista as variáveis {{campo}} do template que não existem como
        atributo do Cliente — úteis para a view avisar o usuário."""
        modelo = self.repo_modelo.buscar_por_id(modelo_id)
        variaveis_template = extrair_variaveis(modelo.caminho_arquivo)
        campos_cliente = set(asdict(self.repo_cliente.listar_todos()[0]).keys()) \
            if self.repo_cliente.listar_todos() else set()
        return variaveis_template - campos_cliente

    def gerar(self, cliente_id: int, modelo_id: int) -> Tuple[bool, str]:
        cliente = self.repo_cliente.buscar_por_id(cliente_id)
        modelo = self.repo_modelo.buscar_por_id(modelo_id)
        if not cliente or not modelo:
            return False, "Selecione um cliente e um modelo válidos."

        valores = {f"cliente_{campo}": valor for campo, valor in asdict(cliente).items()}
        # também disponibiliza sem o prefixo "cliente_", para templates simples
        valores.update(asdict(cliente))

        os.makedirs(DOCUMENTOS_GERADOS_DIR, exist_ok=True)
        nome_arquivo = f"{modelo.nome}_{cliente.nome}.docx".replace(" ", "_")
        caminho_saida = os.path.join(DOCUMENTOS_GERADOS_DIR, nome_arquivo)

        substituir_variaveis(modelo.caminho_arquivo, caminho_saida, valores)

        documento = DocumentoGerado(
            cliente_id=cliente.id, modelo_id=modelo.id,
            nome_documento=nome_arquivo, tipo_documento=modelo.tipo,
            caminho_arquivo=caminho_saida,
        )
        self.repo_documento.inserir(documento)
        return True, f"Documento gerado em: {caminho_saida}"
