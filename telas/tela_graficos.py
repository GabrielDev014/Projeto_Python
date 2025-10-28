import tkinter as tk
from tkinter import ttk

class TelaGraficos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gráficos")
        self.geometry("600x400")
        self.configure(bg="#ffffff")

        ttk.Label(self, text="Criação de Gráficos", font=("Segoe UI", 14, "bold")).pack(pady=20)
        ttk.Button(self, text="Fechar", command=self.destroy).pack(pady=10)


