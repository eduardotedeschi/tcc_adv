"""
Widget reutilizável — mesma lógica do adv_software.py original,
só que isolado em seu próprio módulo para poder ser importado por
qualquer tela (cliente, documento etc.) sem duplicar código.
"""
from tkinter import END, LEFT, X, Listbox
from tkinter import ttk


class SearchableComboBox:
    def __init__(self, parent, options, x, y, w) -> None:
        self.dropdown_id = None
        self.options = options

        wrapper = ttk.Frame(parent)
        wrapper.place(relx=x, rely=y, relwidth=w)

        self.entry = ttk.Entry(wrapper, width=14)
        self.entry.bind("<KeyRelease>", self.on_entry_key)
        self.entry.bind("<FocusIn>", self.show_dropdown)
        self.entry.pack(side=LEFT, fill=X, expand=True)

        self.listbox = Listbox(parent, height=5, width=30)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        for option in self.options:
            self.listbox.insert(END, option)

    def get(self) -> str:
        return self.entry.get()

    def clear(self) -> None:
        self.entry.delete(0, END)

    def set(self, valor: str) -> None:
        self.entry.delete(0, END)
        self.entry.insert(0, valor)

    def on_entry_key(self, event):
        typed_value = event.widget.get().strip().lower()
        self.listbox.delete(0, END)
        filtered = self.options if not typed_value else [
            o for o in self.options if o.lower().startswith(typed_value)
        ]
        for option in filtered:
            self.listbox.insert(END, option)
        self.show_dropdown()

    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.set(self.listbox.get(selected_index))

    def show_dropdown(self, event=None):
        self.listbox.place(in_=self.entry, x=0, rely=1, relwidth=1.0, anchor="nw")
        self.listbox.lift()
        if self.dropdown_id:
            self.listbox.after_cancel(self.dropdown_id)
        self.dropdown_id = self.listbox.after(2000, self.hide_dropdown)

    def hide_dropdown(self):
        self.listbox.place_forget()
