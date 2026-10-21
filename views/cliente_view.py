"""
View = só interface gráfica. Toda regra de negócio foi movida para
ClienteController; esta classe apenas:
  1. desenha os widgets;
  2. lê o que o usuário digitou;
  3. chama o controller;
  4. mostra o resultado (mensagem de erro/sucesso, atualiza a tabela).
"""
import tkinter as tk
from tkinter import messagebox, ttk

from controllers.cliente_controller import ClienteController
from utils.cep_service import CepInvalido, CepNaoEncontrado, buscar_endereco_por_cep
from utils.formatters import mascara_cep, mascara_cpf, mascara_telefone
from utils.opcoes import ESTADOS_CIVIS, NACIONALIDADES
from views.widgets.searchable_combobox import SearchableComboBox


class ClienteView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame")
        self.controller = ClienteController()
        self.cliente_selecionado_id = None

        self._criar_formulario()
        self._criar_botoes()
        self._criar_tabela()
        self._carregar_clientes()

    # ---------- construção da UI ----------

    def _criar_formulario(self):
        style = ttk.Style()
        style.configure("Big.TEntry", font=("Helvetica", 14))

        ttk.Label(self, text="Nome Completo*").place(relx=0.02, rely=0.02)
        self.nome_entry = ttk.Entry(self, style="Big.TEntry")
        self.nome_entry.place(relx=0.02, rely=0.05, relwidth=0.35)

        ttk.Label(self, text="Nacionalidade*").place(relx=0.40, rely=0.02)
        self.nacionalidade_combo = SearchableComboBox(self, NACIONALIDADES, 0.40, 0.05, 0.15)

        ttk.Label(self, text="Estado Civil*").place(relx=0.58, rely=0.02)
        self.estado_civil_combo = SearchableComboBox(self, ESTADOS_CIVIS, 0.58, 0.05, 0.15)

        ttk.Label(self, text="Profissão*").place(relx=0.78, rely=0.02)
        self.profissao_entry = ttk.Entry(self, style="Big.TEntry")
        self.profissao_entry.place(relx=0.78, rely=0.05, relwidth=0.18)

        ttk.Label(self, text="RG*").place(relx=0.02, rely=0.11)
        self.rg_entry = ttk.Entry(self, style="Big.TEntry")
        self.rg_entry.place(relx=0.02, rely=0.14, relwidth=0.15)

        ttk.Label(self, text="CPF*").place(relx=0.20, rely=0.11)
        self.cpf_entry = ttk.Entry(self, style="Big.TEntry")
        self.cpf_entry.place(relx=0.20, rely=0.14, relwidth=0.15)
        self.cpf_entry.bind("<KeyRelease>", lambda e: mascara_cpf(self.cpf_entry))

        ttk.Label(self, text="CEP*").place(relx=0.38, rely=0.11)
        self.cep_entry = ttk.Entry(self, style="Big.TEntry")
        self.cep_entry.place(relx=0.38, rely=0.14, relwidth=0.12)
        self.cep_entry.bind("<KeyRelease>", lambda e: mascara_cep(self.cep_entry))
        self.cep_entry.bind("<FocusOut>", lambda e: self._autocompletar_endereco())

        ttk.Label(self, text="UF*").place(relx=0.53, rely=0.11)
        self.uf_entry = ttk.Entry(self, style="Big.TEntry")
        self.uf_entry.place(relx=0.53, rely=0.14, relwidth=0.05)

        ttk.Label(self, text="Cidade*").place(relx=0.61, rely=0.11)
        self.cidade_entry = ttk.Entry(self, style="Big.TEntry")
        self.cidade_entry.place(relx=0.61, rely=0.14, relwidth=0.18)

        ttk.Label(self, text="Rua*").place(relx=0.02, rely=0.20)
        self.rua_entry = ttk.Entry(self, style="Big.TEntry")
        self.rua_entry.place(relx=0.02, rely=0.23, relwidth=0.3)

        ttk.Label(self, text="Nº Rua*").place(relx=0.35, rely=0.20)
        self.n_rua_entry = ttk.Entry(self, style="Big.TEntry")
        self.n_rua_entry.place(relx=0.35, rely=0.23, relwidth=0.1)

        ttk.Label(self, text="Bairro*").place(relx=0.48, rely=0.20)
        self.bairro_entry = ttk.Entry(self, style="Big.TEntry")
        self.bairro_entry.place(relx=0.48, rely=0.23, relwidth=0.25)

        ttk.Label(self, text="Telefone").place(relx=0.76, rely=0.20)
        self.telefone_entry = ttk.Entry(self, style="Big.TEntry")
        self.telefone_entry.place(relx=0.76, rely=0.23, relwidth=0.2)
        self.telefone_entry.bind("<KeyRelease>", lambda e: mascara_telefone(self.telefone_entry))

        ttk.Label(self, text="Email").place(relx=0.02, rely=0.29)
        self.email_entry = ttk.Entry(self, style="Big.TEntry")
        self.email_entry.place(relx=0.02, rely=0.32, relwidth=0.3)

        ttk.Label(self, text="Nome Completo Réu").place(relx=0.35, rely=0.29)
        self.nome_reu_entry = ttk.Entry(self, style="Big.TEntry")
        self.nome_reu_entry.place(relx=0.35, rely=0.32, relwidth=0.35)

        ttk.Label(self, text="CNPJ/CPF Réu").place(relx=0.73, rely=0.29)
        self.cnpj_reu_entry = ttk.Entry(self, style="Big.TEntry")
        self.cnpj_reu_entry.place(relx=0.73, rely=0.32, relwidth=0.23)

    def _criar_botoes(self):
        ttk.Button(self, text="Adicionar Cliente", style="Accent.TButton",
                   command=self._adicionar).place(relx=0.02, rely=0.40, relwidth=0.17)
        ttk.Button(self, text="Atualizar Cliente", style="Accent.TButton",
                   command=self._atualizar).place(relx=0.21, rely=0.40, relwidth=0.17)
        ttk.Button(self, text="Deletar Cliente", style="Accent.TButton",
                   command=self._deletar).place(relx=0.40, rely=0.40, relwidth=0.17)
        ttk.Button(self, text="Limpar", command=self._limpar_formulario
                   ).place(relx=0.59, rely=0.40, relwidth=0.12)

        ttk.Label(self, text="Buscar por nome/CPF").place(relx=0.73, rely=0.37)
        self.busca_entry = ttk.Entry(self, style="Big.TEntry")
        self.busca_entry.place(relx=0.73, rely=0.40, relwidth=0.25)
        self.busca_entry.bind("<KeyRelease>", lambda e: self._buscar())

    def _criar_tabela(self):
        colunas = ("id", "nome", "cpf", "telefone", "cidade", "uf")
        self.tabela = ttk.Treeview(self, columns=colunas, show="headings", height=12)
        cabecalhos = {
            "id": "Código", "nome": "Nome Completo", "cpf": "CPF",
            "telefone": "Telefone", "cidade": "Cidade", "uf": "UF",
        }
        larguras = {"id": 60, "nome": 300, "cpf": 130, "telefone": 130, "cidade": 200, "uf": 50}
        for col in colunas:
            self.tabela.heading(col, text=cabecalhos[col])
            self.tabela.column(col, width=larguras[col])

        self.tabela.place(relx=0.02, rely=0.45, relwidth=0.95, relheight=0.5)
        self.tabela.bind("<<TreeviewSelect>>", self._selecionar_linha)

        scroll_y = ttk.Scrollbar(self, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scroll_y.set)
        scroll_y.place(relx=0.97, rely=0.45, relwidth=0.02, relheight=0.5)

    # ---------- ações ----------

    def _dados_formulario(self) -> dict:
        return {
            "nome": self.nome_entry.get(),
            "nacionalidade": self.nacionalidade_combo.get(),
            "estado_civil": self.estado_civil_combo.get(),
            "profissao": self.profissao_entry.get(),
            "rg": self.rg_entry.get(),
            "cpf": self.cpf_entry.get(),
            "cep": self.cep_entry.get(),
            "uf": self.uf_entry.get(),
            "cidade": self.cidade_entry.get(),
            "rua": self.rua_entry.get(),
            "numero": self.n_rua_entry.get(),
            "bairro": self.bairro_entry.get(),
            "telefone": self.telefone_entry.get(),
            "email": self.email_entry.get(),
            "nome_reu": self.nome_reu_entry.get(),
            "cnpj_reu": self.cnpj_reu_entry.get(),
        }

    def _adicionar(self):
        sucesso, mensagem = self.controller.cadastrar(self._dados_formulario())
        messagebox.showinfo("Cadastro de Cliente", mensagem) if sucesso \
            else messagebox.showerror("Erro ao cadastrar", mensagem)
        if sucesso:
            self._limpar_formulario()
            self._carregar_clientes()

    def _atualizar(self):
        if self.cliente_selecionado_id is None:
            messagebox.showwarning("Atualizar Cliente", "Selecione um cliente na tabela primeiro.")
            return
        sucesso, mensagem = self.controller.atualizar(self.cliente_selecionado_id, self._dados_formulario())
        messagebox.showinfo("Atualizar Cliente", mensagem) if sucesso \
            else messagebox.showerror("Erro ao atualizar", mensagem)
        if sucesso:
            self._limpar_formulario()
            self._carregar_clientes()

    def _deletar(self):
        if self.cliente_selecionado_id is None:
            messagebox.showwarning("Deletar Cliente", "Selecione um cliente na tabela primeiro.")
            return
        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja remover este cliente?"):
            return
        sucesso, mensagem = self.controller.deletar(self.cliente_selecionado_id)
        messagebox.showinfo("Deletar Cliente", mensagem) if sucesso \
            else messagebox.showerror("Erro ao deletar", mensagem)
        if sucesso:
            self._limpar_formulario()
            self._carregar_clientes()

    def _buscar(self):
        termo = self.busca_entry.get()
        self._preencher_tabela(self.controller.buscar(termo))

    def _autocompletar_endereco(self):
        cep = self.cep_entry.get()
        if not cep.strip():
            return
        try:
            endereco = buscar_endereco_por_cep(cep)
        except (CepInvalido, CepNaoEncontrado) as erro:
            messagebox.showwarning("CEP", str(erro))
            return
        except Exception:
            messagebox.showwarning("CEP", "Não foi possível consultar o CEP agora. Verifique sua conexão.")
            return

        for entry, chave in (
            (self.rua_entry, "rua"), (self.bairro_entry, "bairro"),
            (self.cidade_entry, "cidade"), (self.uf_entry, "uf"),
        ):
            entry.delete(0, tk.END)
            entry.insert(0, endereco[chave])

    def _selecionar_linha(self, event):
        selecionado = self.tabela.selection()
        if not selecionado:
            return
        cliente_id = int(selecionado[0])
        cliente = self.controller.repo.buscar_por_id(cliente_id)
        if not cliente:
            return

        self.cliente_selecionado_id = cliente.id
        self.nome_entry.delete(0, tk.END); self.nome_entry.insert(0, cliente.nome)
        self.nacionalidade_combo.set(cliente.nacionalidade)
        self.estado_civil_combo.set(cliente.estado_civil)
        self.profissao_entry.delete(0, tk.END); self.profissao_entry.insert(0, cliente.profissao)
        self.rg_entry.delete(0, tk.END); self.rg_entry.insert(0, cliente.rg)
        self.cpf_entry.delete(0, tk.END); self.cpf_entry.insert(0, cliente.cpf)
        self.cep_entry.delete(0, tk.END); self.cep_entry.insert(0, cliente.cep)
        self.uf_entry.delete(0, tk.END); self.uf_entry.insert(0, cliente.uf)
        self.cidade_entry.delete(0, tk.END); self.cidade_entry.insert(0, cliente.cidade)
        self.rua_entry.delete(0, tk.END); self.rua_entry.insert(0, cliente.rua)
        self.n_rua_entry.delete(0, tk.END); self.n_rua_entry.insert(0, cliente.numero)
        self.bairro_entry.delete(0, tk.END); self.bairro_entry.insert(0, cliente.bairro)
        self.telefone_entry.delete(0, tk.END); self.telefone_entry.insert(0, cliente.telefone)
        self.email_entry.delete(0, tk.END); self.email_entry.insert(0, cliente.email)
        self.nome_reu_entry.delete(0, tk.END); self.nome_reu_entry.insert(0, cliente.nome_reu)
        self.cnpj_reu_entry.delete(0, tk.END); self.cnpj_reu_entry.insert(0, cliente.cnpj_reu)

    def _limpar_formulario(self):
        self.cliente_selecionado_id = None
        for entry in (
            self.nome_entry, self.profissao_entry, self.rg_entry, self.cpf_entry,
            self.cep_entry, self.uf_entry, self.cidade_entry, self.rua_entry,
            self.n_rua_entry, self.bairro_entry, self.telefone_entry,
            self.email_entry, self.nome_reu_entry, self.cnpj_reu_entry,
        ):
            entry.delete(0, tk.END)
        self.nacionalidade_combo.clear()
        self.estado_civil_combo.clear()

    def _carregar_clientes(self):
        self._preencher_tabela(self.controller.listar())

    def _preencher_tabela(self, clientes):
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        for c in clientes:
            self.tabela.insert("", "end", iid=str(c.id),
                                values=(c.id, c.nome, c.cpf, c.telefone, c.cidade, c.uf))
