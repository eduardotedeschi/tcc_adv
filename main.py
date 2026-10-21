"""
Ponto de entrada único da aplicação.
Rodar com: python main.py
"""
import tkinter as tk

from database.connection import init_db
from views.main_window import MainWindow


def main():
    init_db()
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
