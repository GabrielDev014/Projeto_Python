import tkinter as tk
from tkinter import ttk

class TelaProdutos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastro de Produtos")
        self.geometry("600x400")
        self.configure(bg="#ffffff")

        ttk.Label(self, text="Tela de Cadastro de Produtos", font=("Segoe UI", 14, "bold")).pack(pady=20)
        ttk.Button(self, text="Fechar", command=self.destroy).pack(pady=10)
