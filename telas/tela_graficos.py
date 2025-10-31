import tkinter as tk
import matplotlib.pyplot as plt
from conn.conexaoMySQL import conexao
from datetime import datetime
from collections import Counter

class TelaGraficos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gráficos")
        self.geometry("400x250+350+100")
        self.transient(master)
        self.focus_force()

        self.criar_layout()

    def criar_layout(self):
        label_titulo = tk.Label(self, text="Criação de Gráficos", font=("Segoe UI", 16, "bold"))
        label_titulo.place(x=103, y=10)

        self.botao_clientes_lucrativos = tk.Button(self, text="Clientes mais lucrativos", command=self.clientes_lucrativos, width=30)
        self.botao_clientes_lucrativos.place(x=90, y=70)

        self.botao_clientes_lucrativos = tk.Button(self, text="Produtos mais vendidos", command=self.produtos_vendidos, width=30)
        self.botao_clientes_lucrativos.place(x=90, y=130)

        self.botao_clientes_lucrativos = tk.Button(self, text="Vendas por mês", command=self.vendas_mes, width=30)
        self.botao_clientes_lucrativos.place(x=90, y=190)
    
    def clientes_lucrativos(self):
        conexao.conectar()
        cursor = conexao.cursor

        cursor.execute("""
            SELECT c.nome AS cliente, SUM(p.valor_total) AS total_gasto
            FROM pedidos p
            INNER JOIN clientes c ON p.id_cliente = c.id_cliente
            GROUP BY c.id_cliente
            ORDER BY total_gasto DESC
            LIMIT 10;
        """)
        dados = cursor.fetchall()
        conexao.desconectar()

        clientes = [linha[0] for linha in dados]
        totais = [float(linha[1]) for linha in dados]

        plt.figure(figsize=(12, 6))
        plt.bar(clientes, totais, color='mediumseagreen', width=0.6)

        plt.title('Top 10 Clientes Mais Lucrativos', fontsize=14, fontweight='bold')
        plt.xlabel('Clientes', fontsize=12)
        plt.ylabel('Valor Total Gasto (R$)', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.6)

        plt.ylim(0, max(totais) * 1.1)

        for i, v in enumerate(totais):
            plt.text(i, v + (max(totais) * 0.01), f"R$ {v:.2f}", ha='center', va='bottom', fontsize=9)

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        
    def produtos_vendidos(self):
        conexao.conectar()
        cursor = conexao.cursor

        cursor.execute("""
            SELECT pr.nome AS produto, SUM(i.quantidade) AS total_vendido
            FROM itens_pedido i
            INNER JOIN produtos pr ON i.id_produto = pr.id_produto
            GROUP BY pr.id_produto
            ORDER BY total_vendido DESC
            LIMIT 5;
        """)
        dados = cursor.fetchall()
        conexao.desconectar()

        produtos = [linha[0] for linha in dados]
        quantidades = [int(linha[1]) for linha in dados]

        plt.figure(figsize=(10, 6))
        plt.bar(produtos, quantidades, color='cornflowerblue', width=0.6)

        plt.title('Top 5 Produtos Mais Vendidos', fontsize=14, fontweight='bold')
        plt.xlabel('Produtos', fontsize=12)
        plt.ylabel('Quantidade Vendida', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.6)

        plt.ylim(0, max(quantidades) * 1.1)

        for i, v in enumerate(quantidades):
            plt.text(i, v + (max(quantidades) * 0.01), str(v), ha='center', va='bottom', fontsize=9)

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def vendas_mes(self):
        conexao.conectar()
        cursor = conexao.cursor

        cursor.execute("""
            SELECT id_pedido, data_pedido
            FROM pedidos
            ORDER BY data_pedido ASC;
        """)
        dados = cursor.fetchall()
        conexao.desconectar()

        meses_anos = [linha[1].strftime("%Y-%m") for linha in dados]

        contador = Counter(meses_anos)

        meses_ordenados = sorted(contador.keys())
        quantidade = [contador[m] for m in meses_ordenados]

        labels = [datetime.strptime(m, "%Y-%m").strftime("%b/%Y") for m in meses_ordenados]

        plt.figure(figsize=(12, 6))
        plt.plot(labels, quantidade, marker='o', color='mediumslateblue', linewidth=2)

        plt.title('Quantidade de Pedidos por Mês', fontsize=14, fontweight='bold')
        plt.xlabel('Mês/Ano', fontsize=12)
        plt.ylabel('Número de Pedidos', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.6)

        plt.ylim(0, max(quantidade) * 1.2)

        for i, v in enumerate(quantidade):
            plt.text(i, v + max(quantidade) * 0.03, str(v), ha='center', va='bottom', fontsize=9, color='black')

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()