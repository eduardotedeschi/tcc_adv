"""
Checklist de itens com ordem de seleção — usado na tela de composição
de petição (RF02) para marcar teses e preservar a ordem em que foram
clicadas (necessária para RF03, seção de Pedidos).
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Tuple


class ChecklistTeses(ttk.Frame):
    def __init__(self, parent, itens: List[Tuple[int, str]], on_change: Callable = None):
        """itens: lista de (id, nome_exibido)."""
        super().__init__(parent)
        self.on_change = on_change
        self._variaveis = {}
        self._ordem_selecao: List[int] = []

        canvas = tk.Canvas(self, highlightthickness=0)
        scroll = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        frame_interno = ttk.Frame(canvas)

        frame_interno.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame_interno, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)

        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        for item_id, nome in itens:
            var = tk.BooleanVar(value=False)
            self._variaveis[item_id] = var
            ttk.Checkbutton(
                frame_interno, text=nome, variable=var,
                command=lambda i=item_id: self._on_toggle(i),
            ).pack(anchor="w", padx=5, pady=2)

    def _on_toggle(self, item_id: int):
        if self._variaveis[item_id].get():
            if item_id not in self._ordem_selecao:
                self._ordem_selecao.append(item_id)
        else:
            if item_id in self._ordem_selecao:
                self._ordem_selecao.remove(item_id)
        if self.on_change:
            self.on_change(self._ordem_selecao)

    def obter_selecionados_em_ordem(self) -> List[int]:
        return list(self._ordem_selecao)
