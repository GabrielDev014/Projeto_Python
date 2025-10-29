import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from conn.conexaoMySQL import conexao

class TelaProdutos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastro de Produtos")
        self.geometry("500x400+350+100")
        self.transient(master)
        self.focus_force()

        self.criar_layout()

    def criar_layout(self):

        label_titulo = tk.Label(self, text="Cadastro de Produtos", font=("Segoe UI", 16, "bold"))
        label_titulo.place(x=160, y=10)

        label_id = tk.Label(self, text="ID:")
        label_id.place(x=50, y=60)
        self.entrada_id = tk.Entry(self, width=10)
        self.entrada_id.place(x=150, y=60)

        label_nome = tk.Label(self, text="Nome:")
        label_nome.place(x=50, y=100)
        self.entrada_nome = tk.Entry(self, width=45)
        self.entrada_nome.place(x=150, y=100)

        label_preco = tk.Label(self, text="Preço:")
        label_preco.place(x=50, y=140)
        self.entrada_preco = tk.Entry(self, width=35)
        self.entrada_preco.place(x=150, y=140)

        label_crud = tk.Label(self, text="Operação desejada:", font=("Segoe UI", 11, "bold"))
        label_crud.place(x=180, y=210)

        self.operacao = tk.StringVar(value="inserir")

        radio_inserir = tk.Radiobutton(self, text="Inserir", variable=self.operacao, value="inserir")
        radio_inserir.place(x=50, y=250)

        radio_atualizar = tk.Radiobutton(self, text="Atualizar", variable=self.operacao, value="atualizar")
        radio_atualizar.place(x=150, y=250)

        radio_deletar = tk.Radiobutton(self, text="Deletar", variable=self.operacao, value="deletar")
        radio_deletar.place(x=250, y=250)

        radio_pesquisar = tk.Radiobutton(self, text="Pesquisar", variable=self.operacao, value="pesquisar")
        radio_pesquisar.place(x=350, y=250)

        self.botao_executar = tk.Button(self, text="Executar", command=self.executar_operacao, width=15)
        self.botao_executar.place(x=110, y=300)

        self.botao_fechar = tk.Button(self, text="Fechar", command=self.destroy, width=15)
        self.botao_fechar.place(x=270, y=300)

    def adicionar_produto(self):
        nome = self.entrada_nome.get()
        preco = self.entrada_preco.get()

        conexao.conectar()
        cursor = conexao.cursor
        sql = '''INSERT INTO produtos 
        (nome, preco) 
        VALUES (%s, %s)'''
        val = (nome, preco)
        cursor.execute(sql, val)
        conexao.commit()
        conexao.desconectar()

        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!", parent=self)
        self.limpar_campos()
    
    def deletar_produto(self):
        id = self.entrada_id.get()
        conexao.conectar()
        cursor = conexao.cursor
        sql = '''DELETE FROM produtos WHERE id_produto = %s'''
        val = (id,)
        cursor.execute(sql, val)
        conexao.commit()
        conexao.desconectar()
        messagebox.showinfo("Sucesso", "Produto deletado com sucesso!", parent=self)
        self.limpar_campos()
    
    def alterar_produto(self):
        id = self.entrada_id.get()
        nome = self.entrada_nome.get()
        preco = self.entrada_preco.get()

        conexao.conectar()
        cursor = conexao.cursor
        sql = '''UPDATE produtos SET 
        nome=%s, preco=%s
        WHERE id_produto=%s'''
        val = (nome, preco, id)
        cursor.execute(sql, val)
        conexao.commit()
        conexao.desconectar()
        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!", parent=self)
        self.limpar_campos()
    
    def pesquisar_produto(self):
        id = self.entrada_id.get()
        conexao.conectar()
        cursor = conexao.cursor
        sql = '''SELECT * FROM produtos WHERE id_produto = %s'''
        val = (id,)
        cursor.execute(sql, val)
        resultado = cursor.fetchone()
        conexao.desconectar()

        if resultado:  
            self.entrada_nome.delete(0, tk.END)
            self.entrada_nome.insert(0, resultado[1])

            self.entrada_preco.delete(0, tk.END)
            self.entrada_preco.insert(0, resultado[2])

        else:
            messagebox.showinfo("Pesquisar", "Produto não encontrado!")

    def limpar_campos(self):
        self.entrada_id.delete(0, tk.END)
        self.entrada_nome.delete(0, tk.END)
        self.entrada_preco.delete(0, tk.END)

    def executar_operacao(self):
        operacao_selecionada = self.operacao.get()
        
        if operacao_selecionada == "inserir":
            self.adicionar_produto()
        
        if operacao_selecionada == "atualizar":
            self.alterar_produto()

        if operacao_selecionada == "deletar":
            self.deletar_produto()
        
        if operacao_selecionada == "pesquisar":
            self.pesquisar_produto()