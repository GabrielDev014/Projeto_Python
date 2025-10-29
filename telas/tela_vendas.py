import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from conn.conexaoMySQL import conexao
from datetime import datetime

class TelaVendas(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Novo Pedido")
        self.geometry("840x650+200+30")
        self.transient(master)
        self.focus_force()

        self.produtos = []
        self.itens_venda = []
        self.valor_total = tk.DoubleVar(value=0.00)

        self.criar_layout()
        self.carregar_produtos()
        self.carregar_clientes()

    def criar_layout(self):
        label_titulo = tk.Label(self, text="Tela de Vendas", font=("Segoe UI", 14, "bold"))
        label_titulo.place(x=160, y=10)

        label_produtos = ttk.Label(self, text="Produtos disponíveis")
        label_produtos.place(x=10, y=60)

        self.tabela_produtos = ttk.Treeview(self, columns=("ID", "Nome", "Preço"), show="headings")
        self.tabela_produtos.heading("ID", text="ID")
        self.tabela_produtos.heading("Nome", text="Nome")
        self.tabela_produtos.heading("Preço", text="Preço (R$)")
        self.tabela_produtos.column("ID", width=50)
        self.tabela_produtos.column("Nome", width=200)
        self.tabela_produtos.column("Preço", width=100)
        self.tabela_produtos.place(x=10, y=80)

        label_clientes = ttk.Label(self, text="Clientes")
        label_clientes.place(x=450, y=60)

        self.tabela_clientes = ttk.Treeview(self, columns=("ID", "Nome", "Telefone"), show="headings")
        self.tabela_clientes.heading("ID", text="ID")
        self.tabela_clientes.heading("Nome", text="Nome")
        self.tabela_clientes.heading("Telefone", text="Telefone")
        self.tabela_clientes.column("ID", width=50)
        self.tabela_clientes.column("Nome", width=200)
        self.tabela_clientes.column("Telefone", width=100)
        self.tabela_clientes.place(x=450, y=80)

        label_quantidade = tk.Label(self, text="Quantidade:")
        label_quantidade.place(x=10, y=330)
        self.quantidade_entrada = ttk.Entry(self, width=10)
        self.quantidade_entrada.place(x=80, y=330)
        self.botao_adicionar = ttk.Button(self, text="Adicionar à Venda", command=self.adicionar_item)
        self.botao_adicionar.place(x=150, y=330)
        
        # Lista de itens da venda
        label_itens_venda = tk.Label(self, text="Itens da Venda")
        label_itens_venda.place(x=10, y=370)
        self.tabela_itens = ttk.Treeview(self, columns=("Produto", "Qtd", "Unitário", "Subtotal"), show="headings")
        self.tabela_itens.heading("Produto", text="Produto")
        self.tabela_itens.heading("Qtd", text="Qtd")
        self.tabela_itens.heading("Unitário", text="Unitário (R$)")
        self.tabela_itens.heading("Subtotal", text="Subtotal (R$)")
        self.tabela_itens.column("Produto", width=200)
        self.tabela_itens.column("Qtd", width=50)
        self.tabela_itens.column("Unitário", width=100)
        self.tabela_itens.column("Subtotal", width=100)
        self.tabela_itens.place(x=10, y=390)

        self.botao_remover = ttk.Button(self, text="Remover Item", command=self.remover_item)
        self.botao_remover.place(x=470, y=410)

        self.label_valor = tk.Label(self, text="Total: R$", font=("Arial", 14))
        self.label_valor.place(x=650, y=540)
        self.label_total = tk.Label(self, textvariable=self.valor_total, font=("Arial", 16, "bold"))
        self.label_total.place(x=700, y=540)
        self.botao_finalizar = ttk.Button(self, text="Finalizar Venda", command=self.finalizar_venda)
        self.botao_finalizar.place(x=650, y=590)

    def carregar_produtos(self):
        conexao.conectar()
        cursor = conexao.cursor
        cursor.execute("SELECT id_produto, nome, preco FROM produtos")
        for row in cursor.fetchall():
            self.tabela_produtos.insert("", tk.END, values=row)
    
    def carregar_clientes(self):
        conexao.conectar()
        cursor = conexao.cursor
        cursor.execute("SELECT id_cliente, nome, telefone FROM clientes")
        for row in cursor.fetchall():
            self.tabela_clientes.insert("", tk.END, values=row)

    def adicionar_item(self):
        try:
            item_selecionado = self.tabela_produtos.focus()
            dados = self.tabela_produtos.item(item_selecionado)["values"]

            if not dados:
                messagebox.showwarning("Aviso", "Selecione um produto primeiro.", parent=self)
                return

            id_produto, nome, preco = dados
            qtd = int(self.quantidade_entrada.get())

            subtotal = qtd * float(preco)
            self.itens_venda.append((id_produto, nome, qtd, preco, subtotal))

            self.tabela_itens.insert("", tk.END, values=(nome, qtd, preco, f"{subtotal:.2f}"))
            total = self.valor_total.get() + subtotal
            self.valor_total.set(f"{total:.2f}")

            self.quantidade_entrada.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Digite uma quantidade válida.", parent=self)

    def remover_item(self):
        selecionado = self.tabela_itens.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para remover.", parent=self)
            return

        for item in selecionado:
            valores = self.tabela_itens.item(item, "values")
            subtotal = float(valores[3])
            novo_total = float(self.valor_total.get()) - subtotal
            self.valor_total.set(f"{novo_total:.2f}")
            self.tabela_itens.delete(item)

        self.lbl_total.config(text=f"Total: R$ {self.valor_total:.2f}")

    def finalizar_venda(self):
        cliente_selecionado = self.tabela_clientes.focus()
        cliente_dados = self.tabela_clientes.item(cliente_selecionado)["values"]
        id_cliente = cliente_dados[0]

        if not self.itens_venda:
            messagebox.showwarning("Aviso", "Nenhum item adicionado à venda.", parent=self)
            return

        try:
            conexao.conectar()
            cursor = conexao.cursor
            data_pedido = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql_venda = "INSERT INTO pedidos (id_cliente, data_pedido, valor_total) VALUES (%s, %s, %s)"
            cursor.execute(sql_venda, (id_cliente, data_pedido, self.valor_total.get()))
            conexao.commit()

            id_pedido = cursor.lastrowid

            for id_produto, nome, qtd, preco, subtotal in self.itens_venda:
                sql_item = "INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario, subtotal) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql_item, (id_pedido, id_produto, qtd, preco, subtotal))

            conexao.commit()
            messagebox.showinfo("Sucesso", f"Venda {id_pedido} finalizada com sucesso!", parent=self)
            conexao.desconectar()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao finalizar venda:\n{e}", parent=self)
