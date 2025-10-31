import os
import tkinter as tk
from tkinter import ttk
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd
from conn.conexaoMySQL import conexao


load_dotenv()

class TelaInsights(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Insights com IA (Gemini)")
        self.geometry("630x480+300+100")
        self.resizable(False, False)
        self.transient(master)
        self.focus_force()

        label_titulo = tk.Label(self, text="Gere Insights com Gemini Flash 2.5", font=("Helvetica", 16, "bold"))
        label_titulo.place(x=10, y=15)

        label_prompt = tk.Label(self, text="Prompt: ")
        label_prompt.place(x=10, y=50)

        self.prompt_entrada = tk.Entry(self, width=50)
        self.prompt_entrada.place(x=70, y=53)

        botao_executar = ttk.Button(self, text="Perguntar", command=self.executar_prompt)
        botao_executar.place(x=380, y=50)

        self.caixa_scroll = tk.Scrollbar(self)
        self.caixa_scroll.place(x=570, y=130, height=300)

        self.caixa_resposta = tk.Text(self, wrap=tk.WORD, yscrollcommand=self.caixa_scroll.set, width=68, height=20)
        self.caixa_resposta.place(x=10, y=130)
        self.caixa_scroll.config(command=self.caixa_resposta.yview)


    def executar_prompt(self):
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            genai.configure(api_key=api_key)
        except AttributeError:
            print("Erro: A chave da API não foi encontrada.")
            print("Por favor, defina a variável de ambiente 'GOOGLE_API_KEY'.")
            exit()

        generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
        }

        safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        ]

        model = genai.GenerativeModel(model_name="gemini-2.5-flash",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        conexao.conectar()
        conn = conexao.conexao
        prompt_sql = f"""
        Você é um assistente de dados.
        Gere uma consulta SQL compatível com MySQL para responder a seguinte pergunta:
        "{self.prompt_entrada.get()}"

        Use as tabelas e colunas abaixo:

        Tabelas:
        - clientes(id_cliente, nome, email, telefone, endereco, cidade, estado)
        - produtos(id_produto, nome, preco)
        - pedidos(id_pedido, id_cliente, data_pedido, valor_total)
        - itens_pedido(id_item, id_pedido, id_produto, quantidade, preco_unitario, subtotal)

        Retorne apenas a query SQL, sem explicações.
        """

        res_sql = model.generate_content(prompt_sql)

        sql_gerado = res_sql.text.strip()
        
        sql_gerado = sql_gerado.strip("`").strip()
        sql_gerado = sql_gerado[3:].strip()

        df_resultado = pd.read_sql(sql_gerado, conn)
        conexao.desconectar()

        prompt_insight = f"""
        Aqui estão os resultados da consulta que responde à pergunta:
        {self.prompt_entrada.get()}

        {df_resultado.head(30).to_string(index=False)}

        Gere insights e observações relevantes.
        """
        response = model.generate_content(prompt_insight)

        self.caixa_resposta.delete("1.0", tk.END)
        self.caixa_resposta.insert(tk.END, response.text)
