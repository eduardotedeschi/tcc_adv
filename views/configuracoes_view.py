"""
Tela de configurações: alternância de tema (RNF08). Usa sv_ttk para
aplicar o tema e darkdetect para o modo "automático".
"""
import darkdetect
import sv_ttk
from tkinter import ttk


class ConfiguracoesView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame")
        ttk.Label(self, text="Configurações", font=("Helvetica", 18, "bold")).place(relx=0.02, rely=0.02)

        ttk.Label(self, text="Tema").place(relx=0.02, rely=0.1)
        ttk.Button(self, text="Claro", command=lambda: self._aplicar_tema("light")).place(
            relx=0.02, rely=0.15, relwidth=0.15)
        ttk.Button(self, text="Escuro", command=lambda: self._aplicar_tema("dark")).place(
            relx=0.19, rely=0.15, relwidth=0.15)
        ttk.Button(self, text="Automático (SO)", command=lambda: self._aplicar_tema("auto")).place(
            relx=0.36, rely=0.15, relwidth=0.2)

    def _aplicar_tema(self, escolha: str):
        if escolha == "auto":
            tema = "dark" if darkdetect.isDark() else "light"
        else:
            tema = escolha
        sv_ttk.set_theme(tema)
