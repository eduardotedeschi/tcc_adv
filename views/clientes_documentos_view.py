"""
Tela "documentos do cliente": lista os documentos gerados vinculados a
um cliente específico, com opção de exportação (RF06, RF07, RF14).
"""
from tkinter import filedialog, messagebox, ttk

from controllers.exportacao_controller import ExportacaoController
from repositories.documento_gerado_repository import DocumentoGeradoRepository


class ClientesDocumentosView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame")
        self.repo = DocumentoGeradoRepository()
        self.exportacao_controller = ExportacaoController()
        self._criar_widgets()

    def _criar_widgets(self):
        ttk.Label(self, text="Buscar por CPF do cliente").place(relx=0.02, rely=0.02)
        self.cpf_entry = ttk.Entry(self)
        self.cpf_entry.place(relx=0.02, rely=0.06, relwidth=0.3)
        ttk.Button(self, text="Buscar", command=self._buscar).place(relx=0.33, rely=0.06, relwidth=0.1)

        colunas = ("id", "nome", "tipo", "data")
        self.tabela = ttk.Treeview(self, columns=colunas, show="headings", height=14)
        for col, texto, largura in (
            ("id", "Código", 60), ("nome", "Nome Documento", 300),
            ("tipo", "Tipo", 120), ("data", "Data Gerada", 150),
        ):
            self.tabela.heading(col, text=texto)
            self.tabela.column(col, width=largura)
        self.tabela.place(relx=0.02, rely=0.15, relwidth=0.95, relheight=0.6)

        ttk.Button(self, text="Exportar .docx", style="Accent.TButton",
                   command=self._exportar_docx).place(relx=0.02, rely=0.8, relwidth=0.2)
        ttk.Button(self, text="Exportar .pdf", style="Accent.TButton",
                   command=self._exportar_pdf).place(relx=0.24, rely=0.8, relwidth=0.2)

    def _buscar(self):
        cpf = self.cpf_entry.get().strip()
        if not cpf:
            messagebox.showwarning("Documentos", "Informe o CPF do cliente.")
            return
        documentos = self.repo.buscar_por_cpf_cliente(cpf)
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        for d in documentos:
            self.tabela.insert("", "end", iid=str(d.id),
                                values=(d.id, d.nome_documento, d.tipo_documento, d.data_gerada))

    def _documento_selecionado(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Documentos", "Selecione um documento na tabela.")
            return None
        return self.repo.buscar_por_id(int(selecionado[0]))

    def _exportar_docx(self):
        documento = self._documento_selecionado()
        if not documento:
            return
        pasta = filedialog.askdirectory(title="Escolha a pasta de destino")
        if not pasta:
            return
        sucesso, mensagem = self.exportacao_controller.exportar_docx(documento.caminho_arquivo, pasta)
        messagebox.showinfo("Exportar", mensagem) if sucesso else messagebox.showerror("Exportar", mensagem)

    def _exportar_pdf(self):
        documento = self._documento_selecionado()
        if not documento:
            return
        pasta = filedialog.askdirectory(title="Escolha a pasta de destino")
        if not pasta:
            return
        sucesso, mensagem = self.exportacao_controller.exportar_pdf(documento.caminho_arquivo, pasta)
        messagebox.showinfo("Exportar", mensagem) if sucesso else messagebox.showerror("Exportar", mensagem)
