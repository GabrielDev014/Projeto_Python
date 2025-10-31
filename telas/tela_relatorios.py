import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os
import pandas as pd
from conn.conexaoMySQL import conexao

class TelaRelatorios(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Relatórios e Exportações")
        self.geometry("400x300+350+100")
        self.transient(master)
        self.focus_force()

        self.criar_layout()
    
    def criar_layout(self):
        label_titulo = tk.Label(self, text="Relatórios em PDF / Excel", font=("Segoe UI", 16, "bold"))
        label_titulo.place(x=60, y=10)

        label_relatorios = tk.Label(self, text="Formato:")
        label_relatorios.place(x=120, y=80)
        opcoes = ["PDF", "Excel"] 
        self.combo_relatorios = ttk.Combobox(self, values=opcoes, width=6, state = "readonly")
        self.combo_relatorios.place(x=180, y=80)
        self.combo_relatorios.set("PDF")

        label_relatorios = tk.Label(self, text="Relatório Desejado:", font=("Segoe UI", 11, "bold"))
        label_relatorios.place(x=120, y=130)

        self.operacao = tk.StringVar(value="clientes")

        radio_clientes = tk.Radiobutton(self, text="Clientes", variable=self.operacao, value="clientes")
        radio_clientes.place(x=40, y=180)

        radio_atualizar = tk.Radiobutton(self, text="Produtos", variable=self.operacao, value="produtos")
        radio_atualizar.place(x=160, y=180)

        radio_deletar = tk.Radiobutton(self, text="Pedidos", variable=self.operacao, value="pedidos")
        radio_deletar.place(x=280, y=180)

        self.botao_executar = tk.Button(self, text="Executar", command=self.executar_operacao, width=15)
        self.botao_executar.place(x=140, y=250)

    def executar_operacao(self):
        operacao_selecionada = self.operacao.get()
        formato_selecionado = self.combo_relatorios.get()

        if formato_selecionado == "PDF":
            if operacao_selecionada == "clientes":
                self.exportar_clientes_pdf()
            elif operacao_selecionada == "produtos":
                self.exportar_produtos_pdf()
            elif operacao_selecionada == "pedidos":
                self.exportar_pedidos_pdf()

        elif formato_selecionado == "Excel":
            if operacao_selecionada == "clientes":
                self.exportar_clientes_excel()
            elif operacao_selecionada == "produtos":
                self.exportar_produtos_excel()
            elif operacao_selecionada == "pedidos":
                self.exportar_pedidos_excel()

    def exportar_clientes_pdf(self):
        conexao.conectar()
        cursor = conexao.cursor
        cursor.execute('SELECT id_cliente, nome, email, cidade, estado FROM clientes')
        dados = cursor.fetchall()
        conexao.desconectar()

        pasta_relatorios = os.path.join(os.getcwd(), "relatorios")
        os.makedirs(pasta_relatorios, exist_ok=True)  

        nome_arquivo = "relatorio_clientes.pdf"
        salvar_arquivo = os.path.join(pasta_relatorios, nome_arquivo)

        pdf = SimpleDocTemplate(
            salvar_arquivo,
            pageSize=letter
        )

        estilos = getSampleStyleSheet()
        estilo_titulo = ParagraphStyle(
            'titulo',
            parent=estilos['Heading1'],
            alignment=1,
            fontSize=18,
            spaceAfter=20
        )
        titulo = Paragraph("Relatório de Clientes", estilo_titulo)
        espacador = Spacer(1, 12)

        cabecalho = [('Id', 'Nome', 'E-mail', 'Cidade', 'Estado')]
        dados_tabela = cabecalho + dados

        tabela = Table(dados_tabela)

        estilo = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige]),
        ])
        tabela.setStyle(estilo)

        elementos = [titulo, espacador, tabela]
        pdf.build(elementos)

        messagebox.showinfo("Sucesso", f"Relatório exportado como {nome_arquivo}", parent=self)

    def exportar_produtos_pdf(self):
        conexao.conectar()
        cursor = conexao.cursor
        cursor.execute('SELECT * FROM produtos')
        dados = cursor.fetchall()
        conexao.desconectar()

        pasta_relatorios = os.path.join(os.getcwd(), "relatorios")
        os.makedirs(pasta_relatorios, exist_ok=True)

        nome_arquivo = "relatorio_produtos.pdf"
        salvar_arquivo = os.path.join(pasta_relatorios, nome_arquivo)

        pdf = SimpleDocTemplate(
            salvar_arquivo,
            pageSize=letter
        )

        estilos = getSampleStyleSheet()
        estilo_titulo = ParagraphStyle(
            'titulo',
            parent=estilos['Heading1'],
            alignment=1,
            fontSize=18,
            spaceAfter=20
        )
        titulo = Paragraph("Relatório de Produtos", estilo_titulo)
        espacador = Spacer(1, 12)

        cabecalho = [('Id', 'Nome', 'Preço')]
        dados_tabela = cabecalho + dados

        tabela = Table(dados_tabela)

        estilo = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige]),
        ])
        tabela.setStyle(estilo)

        elementos = [titulo, espacador, tabela]
        pdf.build(elementos)

        messagebox.showinfo("Sucesso", f"Relatório exportado como {nome_arquivo}", parent=self)

    def exportar_pedidos_pdf(self):

        conexao.conectar()
        cursor = conexao.cursor

        cursor.execute("""
            SELECT 
                p.id_pedido,
                c.nome AS cliente,
                pr.nome AS produto,
                i.quantidade,
                i.preco_unitario,
                i.subtotal,
                p.valor_total
            FROM pedidos p
            INNER JOIN clientes c ON p.id_cliente = c.id_cliente
            INNER JOIN itens_pedido i ON p.id_pedido = i.id_pedido
            INNER JOIN produtos pr ON i.id_produto = pr.id_produto
            ORDER BY p.id_pedido;
        """)
        pedidos = cursor.fetchall()
        conexao.desconectar()

        pasta_relatorios = os.path.join(os.getcwd(), "relatorios")
        os.makedirs(pasta_relatorios, exist_ok=True)
        nome_arquivo = "relatorio_pedidos.pdf"
        salvar_arquivo = os.path.join(pasta_relatorios, nome_arquivo)

        pdf = SimpleDocTemplate(
            salvar_arquivo, 
            pagesize=landscape(letter)
        )
        estilos = getSampleStyleSheet()
        elementos = []

        titulo = Paragraph("Relatório de Pedidos", estilos['Title'])
        elementos.append(titulo)
        elementos.append(Spacer(1, 12))

        estilo_tabela = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige]),
        ])

        pedido_atual = None
        dados_pedido = []

        for p in pedidos:
            id_pedido, cliente, produto, quantidade, preco_unitario, subtotal, total_pedido = p

            if pedido_atual is not None and id_pedido != pedido_atual:
        
                tabela = Table(dados_pedido, colWidths=[68, 100, 215, 70, 100, 80])
                tabela.setStyle(estilo_tabela)
                elementos.append(tabela)

                elementos.append(Spacer(1, 5))
                elementos.append(Paragraph(f"<b>Total do Pedido:</b> R$ {ultimo_total:.2f}", estilos['Normal']))
                elementos.append(Spacer(1, 12))

                elementos.append(Paragraph("<br/>", estilos['Normal']))

                dados_pedido = []

            if id_pedido != pedido_atual:

                cabecalho = [
                    ["ID Pedido", "Cliente", "Produto", "Quantidade", "Preço Unitário (R$)", "Subtotal (R$)"]
                ]
                dados_pedido = cabecalho

            dados_pedido.append([
                id_pedido,
                cliente,
                produto,
                quantidade,
                f"{preco_unitario:.2f}",
                f"{subtotal:.2f}"
            ])

            pedido_atual = id_pedido
            ultimo_total = total_pedido

        if dados_pedido:
            tabela = Table(dados_pedido, colWidths=[68, 100, 215, 70, 100, 80])
            tabela.setStyle(estilo_tabela)
            elementos.append(tabela)
            elementos.append(Spacer(1, 5))
            elementos.append(Paragraph(f"<b>Total do Pedido:</b> R$ {ultimo_total:.2f}", estilos['Normal']))

        pdf.build(elementos)

        messagebox.showinfo("Sucesso", f"Relatório exportado como: {nome_arquivo}", parent=self)

    def exportar_clientes_excel(self):
        try:
            conexao.conectar()
            cursor = conexao.cursor
            cursor.execute("SELECT id_cliente, nome, email, cidade, estado FROM clientes")
            dados = cursor.fetchall()
            conexao.desconectar()

            colunas = ["ID Cliente", "Nome", "E-mail", "Cidade", "Estado"]
            df = pd.DataFrame(dados, columns = colunas)

            pasta_relatorios = os.path.join(os.getcwd(), "relatorios")
            os.makedirs(pasta_relatorios, exist_ok=True)
            nome_arquivo = "relatorio_clientes.xlsx"
            salvar_arquivo = os.path.join(pasta_relatorios, nome_arquivo)

            df.to_excel(salvar_arquivo, index=False, engine='openpyxl')
            messagebox.showinfo("Sucesso", f"Relatório exportado como {nome_arquivo}")

        except Exception as e:
            messagebox.showinfo("Erro", f"Erro ao exportar para Excel: {e}")

    def exportar_produtos_excel(self):
        try:
            conexao.conectar()
            cursor = conexao.cursor
            cursor.execute("SELECT * FROM produtos")
            dados = cursor.fetchall()
            conexao.desconectar()

            colunas = ["ID Produto", "Nome", "Preço"]
            df = pd.DataFrame(dados, columns = colunas)

            pasta_relatorios = os.path.join(os.getcwd(), "relatorios")
            os.makedirs(pasta_relatorios, exist_ok=True)
            nome_arquivo = "relatorio_produtos.xlsx"
            salvar_arquivo = os.path.join(pasta_relatorios, nome_arquivo)

            df.to_excel(salvar_arquivo, index=False, engine='openpyxl')
            messagebox.showinfo("Sucesso", f"Relatório exportado como {nome_arquivo}")

        except Exception as e:
            messagebox.showinfo("Erro", f"Erro ao exportar para Excel: {e}")

    def exportar_pedidos_excel(self):
        try:
            conexao.conectar()
            cursor = conexao.cursor

            sql = """
            SELECT 
                p.id_pedido AS 'ID Pedido',
                c.nome AS 'Cliente',
                pr.nome AS 'Produto',
                i.quantidade AS 'Quantidade',
                i.preco_unitario AS 'Preço Unitário',
                i.subtotal AS 'Subtotal',
                p.valor_total AS 'Total do Pedido'
            FROM pedidos p
            INNER JOIN clientes c ON p.id_cliente = c.id_cliente
            INNER JOIN itens_pedido i ON p.id_pedido = i.id_pedido
            INNER JOIN produtos pr ON i.id_produto = pr.id_produto
            ORDER BY p.id_pedido;
            """

            cursor.execute(sql)
            dados = cursor.fetchall()
            conexao.desconectar()

            colunas = [
                "ID Pedido",
                "Cliente",
                "Produto",
                "Quantidade",
                "Preço Unitário",
                "Subtotal",
                "Total do Pedido"
            ]
            df = pd.DataFrame(dados, columns=colunas)

            pasta_relatorios = os.path.join(os.getcwd(), "relatorios")
            os.makedirs(pasta_relatorios, exist_ok=True)

            nome_arquivo = "relatorio_pedidos.xlsx"
            salvar_arquivo = os.path.join(pasta_relatorios, nome_arquivo)
            df.to_excel(salvar_arquivo, index=False, engine='openpyxl')

            messagebox.showinfo("Sucesso", f"Relatório exportado como {nome_arquivo}")

        except Exception as e:
            messagebox.showinfo("Erro", f"Erro ao exportar para Excel: {e}")