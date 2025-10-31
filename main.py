import tkinter as tk
from tkinter import ttk

from telas.tela_clientes import TelaClientes
from telas.tela_produtos import TelaProdutos
from telas.tela_vendas import TelaVendas
from telas.tela_relatorios import TelaRelatorios
from telas.tela_insights import TelaInsights
from telas.tela_graficos import TelaGraficos


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestão - PG Informática")
        self.state("zoomed")

        self._criar_menu_bar()

        self.label_bemvindo = ttk.Label(
            self,
            text="Bem-vindo(a) ao Sistema da PG Informática!",
            font=("Segoe UI", 18, "bold")
        )
        self.label_bemvindo.pack(expand=True)

    def _criar_menu_bar(self):
        menubar = tk.Menu(self)

        menu_cadastro = tk.Menu(menubar, tearoff=0)
        menu_cadastro.add_command(label="Clientes", command=self.abrir_clientes)
        menu_cadastro.add_command(label="Produtos", command=self.abrir_produtos)
        menubar.add_cascade(label="Cadastro", menu=menu_cadastro)

        menu_vendas = tk.Menu(menubar, tearoff=0)
        menu_vendas.add_command(label="Novo Pedido", command=self.abrir_vendas)
        menubar.add_cascade(label="Vendas", menu=menu_vendas)

        menu_relatorios = tk.Menu(menubar, tearoff=0)
        menu_relatorios.add_command(label="Exportar PDF / Excel", command=self.abrir_relatorios)
        menu_relatorios.add_command(label="Exportar Gráficos", command=self.abrir_graficos)
        menubar.add_cascade(label="Relatórios", menu=menu_relatorios)

        menu_ia = tk.Menu(menubar, tearoff=0)
        menu_ia.add_command(label="Gerar Insights com IA", command=self.abrir_insights)
        menubar.add_cascade(label="Insights IA", menu=menu_ia)

        self.config(menu=menubar)

    def abrir_clientes(self):
        TelaClientes(self)

    def abrir_produtos(self):
        TelaProdutos(self)

    def abrir_vendas(self):
        TelaVendas(self)

    def abrir_relatorios(self):
        TelaRelatorios(self)

    def abrir_insights(self):
        TelaInsights(self)

    def abrir_graficos(self):
        TelaGraficos(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()