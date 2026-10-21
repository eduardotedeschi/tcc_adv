"""
Tela de composição de petição: seleciona cliente + teses via checklist
e gera a petição unificada (RF01, RF02, RF03).
"""
from tkinter import messagebox, ttk

from controllers.cliente_controller import ClienteController
from controllers.gerar_peticao_controller import GerarPeticaoController
from controllers.tese_controller import TeseController
from views.widgets.checklist_teses import ChecklistTeses


class GerarPeticaoView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame")
        self.controller = GerarPeticaoController()
        self.cliente_controller = ClienteController()
        self.tese_controller = TeseController()
        self._cliente_id_selecionado = None
        self._criar_widgets()

    def _criar_widgets(self):
        ttk.Label(self, text="Cliente").place(relx=0.02, rely=0.02)
        self.lista_clientes = ttk.Treeview(self, columns=("nome", "cpf"), show="headings", height=8)
        self.lista_clientes.heading("nome", text="Nome")
        self.lista_clientes.heading("cpf", text="CPF")
        self.lista_clientes.place(relx=0.02, rely=0.06, relwidth=0.45, relheight=0.35)
        self.lista_clientes.bind("<<TreeviewSelect>>", self._selecionar_cliente)
        for c in self.cliente_controller.listar():
            self.lista_clientes.insert("", "end", iid=str(c.id), values=(c.nome, c.cpf))

        ttk.Label(self, text="Teses jurídicas (marque na ordem desejada)").place(relx=0.5, rely=0.02)
        itens = [(t.id, t.nome) for t in self.tese_controller.listar()]
        self.checklist = ChecklistTeses(self, itens)
        self.checklist.place(relx=0.5, rely=0.06, relwidth=0.45, relheight=0.5)

        ttk.Button(self, text="Gerar Petição", style="Accent.TButton",
                   command=self._gerar).place(relx=0.02, rely=0.45, relwidth=0.3)

    def _selecionar_cliente(self, event):
        selecionado = self.lista_clientes.selection()
        self._cliente_id_selecionado = int(selecionado[0]) if selecionado else None

    def _gerar(self):
        if not self._cliente_id_selecionado:
            messagebox.showwarning("Gerar Petição", "Selecione um cliente.")
            return
        teses_selecionadas = self.checklist.obter_selecionados_em_ordem()
        sucesso, mensagem = self.controller.gerar(self._cliente_id_selecionado, teses_selecionadas)
        messagebox.showinfo("Gerar Petição", mensagem) if sucesso \
            else messagebox.showerror("Gerar Petição", mensagem)
