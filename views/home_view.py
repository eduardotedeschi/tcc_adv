"""
Tela inicial (RNF03): informações sobre funcionamento, versão do sistema
e orientações de prevenção de erros, exibida antes/depois do login.
"""
from tkinter import ttk

from config import APP_TITLE, APP_VERSION

TEXTO_INSTRUCOES = (
    "Bem-vindo(a) ao {titulo} — versão {versao}.\n\n"
    "Antes de começar:\n"
    "• Cadastre o cliente antes de gerar qualquer documento.\n"
    "• Os modelos precisam estar no formato .docx com variáveis no "
    "padrão {{{{campo}}}} (ex.: {{{{nome}}}}, {{{{cpf}}}}).\n"
    "• Confira sempre o documento gerado antes de exportar."
).format(titulo=APP_TITLE, versao=APP_VERSION)


class HomeView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame")
        ttk.Label(self, text=APP_TITLE, font=("Helvetica", 20, "bold")).place(relx=0.05, rely=0.05)
        ttk.Label(self, text=TEXTO_INSTRUCOES, justify="left", wraplength=700).place(
            relx=0.05, rely=0.15)
