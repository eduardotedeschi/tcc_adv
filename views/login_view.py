import tkinter as tk
from tkinter import messagebox, ttk

from controllers.auth_controller import AuthController
from config import APP_TITLE, APP_VERSION
from utils.ui_helpers import aplicar_geometria_responsiva


class LoginView(ttk.Frame):
    """
    Tela de login (RF08 / tela 'Tela de Login' do escopo).
    on_login_sucesso: callback chamado quando a autenticação der certo,
    para o main_window trocar de tela.
    """

    def __init__(self, parent, on_login_sucesso):
        super().__init__(parent, style="Card.TFrame")
        self.controller = AuthController()
        self.on_login_sucesso = on_login_sucesso
        self._criar_widgets()

    def _criar_widgets(self):
        ttk.Label(self, text=APP_TITLE, font=("Helvetica", 22, "bold")).place(
            relx=0.5, rely=0.25, anchor="center")
        ttk.Label(self, text=f"versão {APP_VERSION}").place(relx=0.5, rely=0.31, anchor="center")

        ttk.Label(self, text="E-mail").place(relx=0.35, rely=0.4)
        self.email_entry = ttk.Entry(self)
        self.email_entry.place(relx=0.35, rely=0.44, relwidth=0.3)

        ttk.Label(self, text="Senha").place(relx=0.35, rely=0.5)
        self.senha_entry = ttk.Entry(self, show="•")
        self.senha_entry.place(relx=0.35, rely=0.54, relwidth=0.3)
        self.senha_entry.bind("<Return>", lambda e: self._entrar())

        ttk.Button(self, text="Entrar", style="Accent.TButton",
                   command=self._entrar).place(relx=0.35, rely=0.62, relwidth=0.3)
        ttk.Button(self, text="Criar cadastro de escritório",
                   command=self._abrir_cadastro).place(relx=0.35, rely=0.68, relwidth=0.3)

    def _entrar(self):
        sucesso, mensagem = self.controller.autenticar(
            self.email_entry.get(), self.senha_entry.get())
        if not sucesso:
            messagebox.showerror("Login", mensagem)
            return
        self.on_login_sucesso()

    def _abrir_cadastro(self):
        janela = tk.Toplevel(self)
        janela.title("Cadastro de Escritório")
        aplicar_geometria_responsiva(
            janela,
            largura_pct=0.25,
            altura_pct=0.30,
            min_w=360,
            min_h=260,
        )
        ttk.Label(janela, text="Nome do Escritório").pack(pady=(15, 0))
        nome_entry = ttk.Entry(janela)
        nome_entry.pack(fill="x", padx=20)

        ttk.Label(janela, text="E-mail").pack(pady=(10, 0))
        email_entry = ttk.Entry(janela)
        email_entry.pack(fill="x", padx=20)

        ttk.Label(janela, text="Senha").pack(pady=(10, 0))
        senha_entry = ttk.Entry(janela, show="•")
        senha_entry.pack(fill="x", padx=20)

        def salvar():
            sucesso, mensagem = self.controller.cadastrar_escritorio(
                nome_entry.get(), email_entry.get(), senha_entry.get())
            messagebox.showinfo("Cadastro", mensagem) if sucesso \
                else messagebox.showerror("Cadastro", mensagem)
            if sucesso:
                janela.destroy()

        ttk.Button(janela, text="Salvar", style="Accent.TButton",
                   command=salvar).pack(pady=15)
