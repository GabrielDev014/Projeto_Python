import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class TelaClientes(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Sistema de Clientes")
        self.geometry("500x500")

        self.criar_layout()

    def criar_layout(self):

        label_titulo = tk.Label(self, text="Sistema de Clientes", font=("Segoe UI", 16, "bold"))
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
        self.combo = ttk.Combobox(self, values=opcoes, width=6, state="readonly")
        self.combo.place(x=365, y=260)
        self.combo.set("SP")

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

    def executar_operacao(self):
        operacao_selecionada = self.operacao.get()
        messagebox.showinfo("Operação", f"Operação selecionada: {operacao_selecionada}")
