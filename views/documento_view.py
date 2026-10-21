"""
Tela de gerenciamento de modelos (importar/remover .docx). Segue o
mesmo padrão de cliente_view.py: só UI, toda regra fica no controller.
"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from controllers.modelo_documento_controller import ModeloDocumentoController
from utils.opcoes import TIPOS_DOCUMENTO
from views.widgets.searchable_combobox import SearchableComboBox


class DocumentoView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame")
        self.controller = ModeloDocumentoController()
        self._criar_formulario()
        self._criar_tabela()
        self._carregar()

    def _criar_formulario(self):
        ttk.Label(self, text="Nome do Documento*").place(relx=0.02, rely=0.02)
        self.nome_entry = ttk.Entry(self)
        self.nome_entry.place(relx=0.02, rely=0.06, relwidth=0.35)

        ttk.Label(self, text="Tipo*").place(relx=0.40, rely=0.02)
        self.tipo_combo = SearchableComboBox(self, TIPOS_DOCUMENTO, 0.40, 0.06, 0.15)

        ttk.Label(self, text="Caminho do arquivo*").place(relx=0.02, rely=0.12)
        self.caminho_entry = ttk.Entry(self)
        self.caminho_entry.place(relx=0.22, rely=0.12, relwidth=0.55)
        ttk.Button(self, text="Escolher Arquivo", command=self._escolher_arquivo).place(
            relx=0.80, rely=0.12, relwidth=0.17)

        ttk.Button(self, text="Adicionar Documento", style="Accent.TButton",
                   command=self._adicionar).place(relx=0.02, rely=0.2, relwidth=0.2)
        ttk.Button(self, text="Remover Selecionado", style="Accent.TButton",
                   command=self._remover).place(relx=0.24, rely=0.2, relwidth=0.2)

        ttk.Label(self, text="Buscar por nome").place(relx=0.55, rely=0.17)
        self.busca_entry = ttk.Entry(self)
        self.busca_entry.place(relx=0.55, rely=0.2, relwidth=0.4)
        self.busca_entry.bind("<KeyRelease>", lambda e: self._buscar())

    def _criar_tabela(self):
        colunas = ("id", "nome", "tipo")
        self.tabela = ttk.Treeview(self, columns=colunas, show="headings", height=12)
        for col, texto, largura in (("id", "Código", 60), ("nome", "Nome", 400), ("tipo", "Tipo", 150)):
            self.tabela.heading(col, text=texto)
            self.tabela.column(col, width=largura)
        self.tabela.place(relx=0.02, rely=0.3, relwidth=0.95, relheight=0.65)

    def _escolher_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecione um documento",
            filetypes=[("Documentos Word", "*.docx"), ("Todos os arquivos", "*.*")],
        )
        if caminho:
            self.caminho_entry.delete(0, tk.END)
            self.caminho_entry.insert(0, caminho)

    def _adicionar(self):
        sucesso, mensagem = self.controller.importar(
            self.nome_entry.get(), self.tipo_combo.get(), self.caminho_entry.get())
        messagebox.showinfo("Modelos", mensagem) if sucesso else messagebox.showerror("Modelos", mensagem)
        if sucesso:
            self.nome_entry.delete(0, tk.END)
            self.tipo_combo.clear()
            self.caminho_entry.delete(0, tk.END)
            self._carregar()

    def _remover(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Modelos", "Selecione um modelo na tabela.")
            return
        sucesso, mensagem = self.controller.remover(int(selecionado[0]))
        messagebox.showinfo("Modelos", mensagem) if sucesso else messagebox.showerror("Modelos", mensagem)
        if sucesso:
            self._carregar()

    def _buscar(self):
        self._preencher(self.controller.buscar(self.busca_entry.get()))

    def _carregar(self):
        self._preencher(self.controller.listar())

    def _preencher(self, modelos):
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        for m in modelos:
            self.tabela.insert("", "end", iid=str(m.id), values=(m.id, m.nome, m.tipo))
