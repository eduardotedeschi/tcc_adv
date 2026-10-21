"""
Tela de geração de documento: seleciona cliente + modelo e gera o
arquivo final com as variáveis substituídas (RF04).
"""
from tkinter import messagebox, ttk

from controllers.cliente_controller import ClienteController
from controllers.gerar_documento_controller import GerarDocumentoController
from controllers.modelo_documento_controller import ModeloDocumentoController


class GerarDocumentoView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame")
        self.controller = GerarDocumentoController()
        self.cliente_controller = ClienteController()
        self.modelo_controller = ModeloDocumentoController()
        self._cliente_id_selecionado = None
        self._modelo_id_selecionado = None
        self._criar_widgets()
        self._carregar_listas()

    def _criar_widgets(self):
        ttk.Label(self, text="Cliente").place(relx=0.02, rely=0.02)
        self.lista_clientes = ttk.Treeview(self, columns=("nome", "cpf"), show="headings", height=10)
        self.lista_clientes.heading("nome", text="Nome")
        self.lista_clientes.heading("cpf", text="CPF")
        self.lista_clientes.place(relx=0.02, rely=0.06, relwidth=0.45, relheight=0.4)
        self.lista_clientes.bind("<<TreeviewSelect>>", self._selecionar_cliente)

        ttk.Label(self, text="Modelo de Documento").place(relx=0.5, rely=0.02)
        self.lista_modelos = ttk.Treeview(self, columns=("nome", "tipo"), show="headings", height=10)
        self.lista_modelos.heading("nome", text="Nome")
        self.lista_modelos.heading("tipo", text="Tipo")
        self.lista_modelos.place(relx=0.5, rely=0.06, relwidth=0.45, relheight=0.4)
        self.lista_modelos.bind("<<TreeviewSelect>>", self._selecionar_modelo)

        ttk.Button(self, text="Gerar Documento", style="Accent.TButton",
                   command=self._gerar).place(relx=0.02, rely=0.5, relwidth=0.3)

    def _carregar_listas(self):
        for c in self.cliente_controller.listar():
            self.lista_clientes.insert("", "end", iid=str(c.id), values=(c.nome, c.cpf))
        for m in self.modelo_controller.listar():
            self.lista_modelos.insert("", "end", iid=str(m.id), values=(m.nome, m.tipo))

    def _selecionar_cliente(self, event):
        selecionado = self.lista_clientes.selection()
        self._cliente_id_selecionado = int(selecionado[0]) if selecionado else None

    def _selecionar_modelo(self, event):
        selecionado = self.lista_modelos.selection()
        self._modelo_id_selecionado = int(selecionado[0]) if selecionado else None

    def _gerar(self):
        if not self._cliente_id_selecionado or not self._modelo_id_selecionado:
            messagebox.showwarning("Gerar Documento", "Selecione um cliente e um modelo.")
            return
        sucesso, mensagem = self.controller.gerar(
            self._cliente_id_selecionado, self._modelo_id_selecionado)
        messagebox.showinfo("Gerar Documento", mensagem) if sucesso \
            else messagebox.showerror("Gerar Documento", mensagem)
