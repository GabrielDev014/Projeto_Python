import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


load_dotenv()

class ConectarMySQL():
    def __init__(self):
        self.host=os.getenv("DB_HOST")
        self.user=os.getenv("DB_USER")
        self.password=os.getenv("DB_PASSWORD")
        self.database=os.getenv("DB_NAME")
        self.conexao = None
        self.cursor = None
    
    def conectar(self):
        try:
            self.conexao = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.conexao.cursor()
        except Error as erro:
            print(f"Erro ao conectar ao MySQL: {erro}")

    def commit(self):
        if self.conexao:
            self.conexao.commit()

    def desconectar(self):
        if self.cursor:
            self.cursor.close()
        if self.conexao and self.conexao.is_connected():
            self.conexao.close()
            print("Conexão encerrada com sucesso.")
            
conexao = ConectarMySQL()