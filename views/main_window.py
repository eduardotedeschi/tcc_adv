"""
Orquestra a navegação entre telas. Equivale à antiga classe App do
arquivo monolítico, mas sem misturar widgets de negócio aqui dentro —
cada tela é uma classe própria em views/.
"""
import tkinter as tk
from tkinter import ttk

import sv_ttk

from config import APP_TITLE, WINDOW_LARGURA_PCT, WINDOW_MIN_SIZE, WINDOW_ALTURA_PCT
from utils.ui_helpers import aplicar_geometria_responsiva
from views.cliente_view import ClienteView
from views.clientes_documentos_view import ClientesDocumentosView
from views.configuracoes_view import ConfiguracoesView
from views.documento_view import DocumentoView
from views.gerar_documento_view import GerarDocumentoView
from views.gerar_peticao_view import GerarPeticaoView
from views.home_view import HomeView
from views.login_view import LoginView
from views.suporte_view import SuporteView


class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self._configurar_janela()
        self._montar_login()

    def _configurar_janela(self):
        self.root.title(APP_TITLE)
        sv_ttk.set_theme("light")
        aplicar_geometria_responsiva(
            self.root,
            largura_pct=WINDOW_LARGURA_PCT,
            altura_pct=WINDOW_ALTURA_PCT,
            min_w=WINDOW_MIN_SIZE[0],
            min_h=WINDOW_MIN_SIZE[1],
        )

    def _montar_login(self):
        self.login_view = LoginView(self.root, on_login_sucesso=self._entrar_no_sistema)
        self.login_view.place(relx=0, rely=0, relwidth=1, relheight=1)

    def _entrar_no_sistema(self):
        self.login_view.destroy()
        self._montar_menu_principal()

    def _montar_menu_principal(self):
        self.frame_menu = ttk.Frame(self.root, style="Card.TFrame")
        self.frame_menu.place(relx=0.02, rely=0.02, relwidth=0.2, relheight=0.96)

        self.container_telas = ttk.Frame(self.root, style="Card.TFrame")
        self.container_telas.place(relx=0.24, rely=0.02, relwidth=0.74, relheight=0.96)

        # Cada tela nova do time segue este padrão:
        # 1. criar a classe em views/nome_view.py
        # 2. registrar aqui dentro de self.telas
        self.telas = {
            "home": HomeView(self.container_telas),
            "clientes": ClienteView(self.container_telas),
            "documentos": DocumentoView(self.container_telas),
            "gerar_documento": GerarDocumentoView(self.container_telas),
            "gerar_peticao": GerarPeticaoView(self.container_telas),
            "clientes_doc": ClientesDocumentosView(self.container_telas),
            "suporte": SuporteView(self.container_telas),
            "configuracoes": ConfiguracoesView(self.container_telas),
        }
        for tela in self.telas.values():
            tela.place(relx=0, rely=0, relwidth=1, relheight=1)

        botoes = [
            ("Início", "home"),
            ("Gerenciar Clientes", "clientes"),
            ("Gerenciar Modelos", "documentos"),
            ("Gerar Documento", "gerar_documento"),
            ("Gerar Petição", "gerar_peticao"),
            ("Clientes/Documentos", "clientes_doc"),
            ("Suporte / FAQ", "suporte"),
            ("Configurações", "configuracoes"),
        ]
        for i, (texto, chave) in enumerate(botoes):
            ttk.Button(
                self.frame_menu, text=texto,
                command=lambda k=chave: self._exibir_tela(k),
            ).place(relx=0.05, rely=0.05 + i * 0.07, relwidth=0.9, relheight=0.05)

        ttk.Button(self.frame_menu, text="Sair", style="Accent.TButton",
                   command=self.root.destroy).place(relx=0.05, rely=0.93, relwidth=0.9, relheight=0.05)

        self._exibir_tela("home")

    def _exibir_tela(self, chave: str):
        tela = self.telas.get(chave)
        if tela is not None:
            tela.lift()
