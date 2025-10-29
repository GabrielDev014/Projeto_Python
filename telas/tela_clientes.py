import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from conn.conexaoMySQL import conexao

class TelaClientes(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Sistema de Clientes")
        self.geometry("500x500+350+100")
        self.transient(master)
        self.focus_force()

        self.criar_layout()

    def criar_layout(self):

        label_titulo = tk.Label(self, text="Cadastro de Clientes", font=("Segoe UI", 16, "bold"))
        label_titulo.place(x=160, y=10)

        label_id = tk.Label(self, text="ID:")
        label_id.place(x=50, y=60)
        self.entrada_id = tk.Entry(self, width=10)
        self.entrada_id.place(x=150, y=60)

        label_nome = tk.Label(self, text="Nome:")
        label_nome.place(x=50, y=100)
        self.entrada_nome = tk.Entry(self, width=45)
        self.entrada_nome.place(x=150, y=100)

        label_email = tk.Label(self, text="Email:")
        label_email.place(x=50, y=140)
        self.entrada_email = tk.Entry(self, width=45)
        self.entrada_email.place(x=150, y=140)

        label_telefone = tk.Label(self, text="Telefone:")
        label_telefone.place(x=50, y=180)
        self.entrada_telefone = tk.Entry(self, width=25)
        self.entrada_telefone.place(x=150, y=180)

        label_endereco = tk.Label(self, text="Endereço:")
        label_endereco.place(x=50, y=220)
        self.entrada_endereco = tk.Entry(self, width=45)
        self.entrada_endereco.place(x=150, y=220)

        label_cidade = tk.Label(self, text="Cidade:")
        label_cidade.place(x=50, y=260)
        self.entrada_cidade = tk.Entry(self, width=25)
        self.entrada_cidade.place(x=150, y=260)

        label_estado = tk.Label(self, text="Estado:")
        label_estado.place(x=313, y=260)
        opcoes = ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG",
                "PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"]
        self.combo_estado = ttk.Combobox(self, values=opcoes, width=6, state = "readonly")
        self.combo_estado.place(x=365, y=260)
        self.combo_estado.set("SP")

        label_crud = tk.Label(self, text="Operação desejada:", font=("Segoe UI", 11, "bold"))
        label_crud.place(x=180, y=310)

        self.operacao = tk.StringVar(value="inserir")

        radio_inserir = tk.Radiobutton(self, text="Inserir", variable=self.operacao, value="inserir")
        radio_inserir.place(x=50, y=350)

        radio_atualizar = tk.Radiobutton(self, text="Atualizar", variable=self.operacao, value="atualizar")
        radio_atualizar.place(x=150, y=350)

        radio_deletar = tk.Radiobutton(self, text="Deletar", variable=self.operacao, value="deletar")
        radio_deletar.place(x=250, y=350)

        radio_pesquisar = tk.Radiobutton(self, text="Pesquisar", variable=self.operacao, value="pesquisar")
        radio_pesquisar.place(x=350, y=350)

        self.botao_executar = tk.Button(self, text="Executar", command=self.executar_operacao, width=15)
        self.botao_executar.place(x=110, y=400)

        self.botao_fechar = tk.Button(self, text="Fechar", command=self.destroy, width=15)
        self.botao_fechar.place(x=270, y=400)

    def adicionar_cliente(self):
        nome = self.entrada_nome.get()
        email = self.entrada_email.get()
        telefone = self.entrada_telefone.get()
        endereco = self.entrada_endereco.get()
        cidade = self.entrada_cidade.get()
        estado = self.combo_estado.get()

        conexao.conectar()
        cursor = conexao.cursor
        sql = '''INSERT INTO clientes 
        (nome, email, telefone, endereco, cidade, estado) 
        VALUES (%s, %s, %s, %s, %s, %s)'''
        val = (nome, email, telefone, endereco, cidade, estado)
        cursor.execute(sql, val)
        conexao.commit()
        conexao.desconectar()

        messagebox.showinfo("Cadastrar Cliente", "Cliente cadastrado com sucesso!", parent=self)
        self.limpar_campos()
    
    def deletar_cliente(self):
        id = self.entrada_id.get()
        conexao.conectar()
        cursor = conexao.cursor
        sql = '''DELETE FROM clientes WHERE id_cliente = %s'''
        val = (id,)
        cursor.execute(sql, val)
        conexao.commit()
        conexao.desconectar()
        messagebox.showinfo("Sucesso", "Cliente deletado com sucesso!", parent=self)
        self.limpar_campos()
    
    def alterar_cliente(self):
        id = self.entrada_id.get()
        nome = self.entrada_nome.get()
        email = self.entrada_email.get()
        telefone = self.entrada_telefone.get()
        endereco = self.entrada_endereco.get()
        cidade = self.entrada_cidade.get()
        estado = self.combo_estado.get()

        conexao.conectar()
        cursor = conexao.cursor
        sql = '''UPDATE clientes SET 
        nome=%s, email=%s, telefone=%s, endereco=%s, cidade=%s, estado=%s
        WHERE id_cliente=%s'''
        val = (nome, email, telefone, endereco, cidade, estado, id)
        cursor.execute(sql, val)
        conexao.commit()
        conexao.desconectar()
        messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!", parent=self)
        self.limpar_campos()
    
    def pesquisar_cliente(self):
        id = self.entrada_id.get()
        conexao.conectar()
        cursor = conexao.cursor
        sql = '''SELECT * FROM clientes WHERE id_cliente = %s'''
        val = (id,)
        cursor.execute(sql, val)
        resultado = cursor.fetchone()
        conexao.desconectar()

        if resultado:  
            self.entrada_nome.delete(0, tk.END)
            self.entrada_nome.insert(0, resultado[1])

            self.entrada_email.delete(0, tk.END)
            self.entrada_email.insert(0, resultado[2])

            self.entrada_telefone.delete(0, tk.END)
            self.entrada_telefone.insert(0, resultado[3])

            self.entrada_endereco.delete(0, tk.END)
            self.entrada_endereco.insert(0, resultado[4])

            self.entrada_cidade.delete(0, tk.END)
            self.entrada_cidade.insert(0, resultado[5])

            self.combo_estado.delete(0, tk.END)
            self.combo_estado.insert(0, resultado[6])

        else:
            messagebox.showinfo("Pesquisar", "Cliente não encontrado!")

    def limpar_campos(self):
        self.entrada_id.delete(0, tk.END)
        self.entrada_nome.delete(0, tk.END)
        self.entrada_email.delete(0, tk.END)
        self.entrada_telefone.delete(0, tk.END)
        self.entrada_endereco.delete(0, tk.END)
        self.entrada_cidade.delete(0, tk.END)
        self.combo_estado.delete(0, tk.END)

    def executar_operacao(self):
        operacao_selecionada = self.operacao.get()
        
        if operacao_selecionada == "inserir":
            self.adicionar_cliente()
        
        if operacao_selecionada == "atualizar":
            self.alterar_cliente()

        if operacao_selecionada == "deletar":
            self.deletar_cliente()
        
        if operacao_selecionada == "pesquisar":
            self.pesquisar_cliente()