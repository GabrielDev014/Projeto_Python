import tkinter as tk
from tkinter import ttk, messagebox

# Importa as telas (ainda serão criadas)
from telas.tela_clientes import TelaClientes
from telas.tela_produtos import TelaProdutos
from telas.tela_vendas import TelaVendas
from telas.tela_relatorios import TelaRelatorios
from telas.tela_insights import TelaInsights
from telas.tela_graficos import TelaGraficos


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configuração da janela principal
        self.title("Sistema de Vendas - Python + MySQL")
        self.geometry("800x600")
        self.configure(bg="#f8f9fa")

        # Criação do menu superior
        self._criar_menu_bar()

        # Label inicial
        self.label_bemvindo = ttk.Label(
            self,
            text="Bem-vindo ao Sistema de Vendas",
            font=("Segoe UI", 18, "bold"),
            background="#f8f9fa",
        )
        self.label_bemvindo.pack(expand=True)

    # -------------------------
    # MENU SUPERIOR
    # -------------------------
    def _criar_menu_bar(self):
        menubar = tk.Menu(self)

        # Menu Cadastro
        menu_cadastro = tk.Menu(menubar, tearoff=0)
        menu_cadastro.add_command(label="Clientes", command=self.abrir_clientes)
        menu_cadastro.add_command(label="Produtos", command=self.abrir_produtos)
        menubar.add_cascade(label="Cadastro", menu=menu_cadastro)

        # Menu Vendas
        menu_vendas = tk.Menu(menubar, tearoff=0)
        menu_vendas.add_command(label="Novo Pedido", command=self.abrir_vendas)
        menubar.add_cascade(label="Vendas", menu=menu_vendas)

        # Menu Relatórios
        menu_relatorios = tk.Menu(menubar, tearoff=0)
        menu_relatorios.add_command(label="Exportar PDF / Excel", command=self.abrir_relatorios)
        menu_relatorios.add_command(label="Exportar Gráficos", command=self.abrir_graficos)
        menubar.add_cascade(label="Relatórios", menu=menu_relatorios)

        # Menu Insights IA
        menu_ia = tk.Menu(menubar, tearoff=0)
        menu_ia.add_command(label="Gerar Insights com IA", command=self.abrir_insights)
        menubar.add_cascade(label="Insights IA", menu=menu_ia)

        # Aplica o menu
        self.config(menu=menubar)

    # -------------------------
    # FUNÇÕES DE ABERTURA DAS TELAS
    # -------------------------
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