import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os
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
            spaceAfter=20,
            textColor=colors.darkblue
        )
        titulo = Paragraph("Relatório de Clientes", estilo_titulo)
        espacador = Spacer(1, 12)

        cabecalho = [('Id', 'Nome', 'E-mail', 'Cidade', 'Estado')]
        dados_tabela = cabecalho + dados

        tabela = Table(dados_tabela)

        estilo = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
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
            spaceAfter=20,
            textColor=colors.darkblue
        )
        titulo = Paragraph("Relatório de Produtos", estilo_titulo)
        espacador = Spacer(1, 12)

        cabecalho = [('Id', 'Nome', 'Preço')]
        dados_tabela = cabecalho + dados

        tabela = Table(dados_tabela)

        estilo = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ])
        tabela.setStyle(estilo)

        elementos = [titulo, espacador, tabela]
        pdf.build(elementos)

        messagebox.showinfo("Sucesso", f"Relatório exportado como {nome_arquivo}", parent=self)

    def exportar_pedidos_pdf(self):
        conexao.conectar()
        cursor = conexao.cursor

        cursor.execute("""
            SELECT p.id_pedido, c.nome, p.valor_total
            FROM pedidos p
            INNER JOIN clientes c ON p.id_cliente = c.id_cliente
            ORDER BY p.id_pedido
        """)
        pedidos = cursor.fetchall()

        if not pedidos:
            messagebox.showinfo("Aviso", "Nenhum pedido encontrado.", parent=self)
            conexao.desconectar()
            return
        
        pasta_relatorios = os.path.join(os.getcwd(), "relatorios")
        os.makedirs(pasta_relatorios, exist_ok=True)
        nome_arquivo = "relatorio_pedidos.pdf"
        salvar_arquivo = os.path.join(pasta_relatorios, nome_arquivo)

        pdf = SimpleDocTemplate(
            salvar_arquivo, 
            pagesize=letter
        )
        
        elementos = []
        estilos = getSampleStyleSheet()

        estilo_titulo = ParagraphStyle(
            'titulo',
            parent=estilos['Heading1'],
            alignment=1,
            fontSize=18,
            spaceAfter=20,
            textColor=colors.darkblue
        )

        estilo_subtitulo = ParagraphStyle(
            'subtitulo',
            parent=estilos['Heading2'],
            fontSize=13,
            textColor=colors.darkred,
            spaceAfter=8
        )

        estilo_produto = ParagraphStyle(
            'produto',
            fontSize=9,
            leading=11,
            alignment=0,
        )

        elementos.append(Paragraph("Relatório de Pedidos", estilo_titulo))
        elementos.append(Spacer(1, 10))

        total_geral = 0

        for pedido in pedidos:
            id_pedido, nome_cliente, valor_total = pedido
            total_geral += float(valor_total)

            cursor.execute("""
                SELECT pr.nome, i.quantidade, i.preco_unitario, i.subtotal
                FROM itens_pedido i
                INNER JOIN produtos pr ON i.id_produto = pr.id_produto
                WHERE i.id_pedido = %s
            """, (id_pedido,))
            itens = cursor.fetchall()

            elementos.append(Paragraph(f"<b>Pedido nº {id_pedido}</b>", estilo_subtitulo))
            elementos.append(Paragraph(f"<b>Cliente:</b> {nome_cliente}", estilos['Normal']))
            elementos.append(Spacer(1, 5))

            cabecalho = [("Produto", "Qtd", "Preço Unitário (R$)", "Subtotal (R$)")]
            dados_tabela = cabecalho + [
                (
                    Paragraph(item[0], estilo_produto),
                    str(item[1]),
                    f"{item[2]:.2f}",
                    f"{item[3]:.2f}"
                )
                for item in itens
            ]

            tabela = Table(dados_tabela, colWidths=[250, 50, 100, 100])
            estilo_tabela = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 4),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
            ])
            tabela.setStyle(estilo_tabela)
            elementos.append(tabela)

            elementos.append(Spacer(1, 5))
            elementos.append(Paragraph(f"<b>Total do Pedido:</b> R$ {valor_total:.2f}", estilos['Normal']))
            elementos.append(Spacer(1, 12))
            elementos.append(Table([[" "]]))

        conexao.desconectar()

        elementos.append(Spacer(1, 12))
        elementos.append(Paragraph(f"<b>Total Geral de Vendas:</b> R$ {total_geral:.2f}", estilos['Heading3']))

        pdf.build(elementos)

        messagebox.showinfo("Sucesso", f"Relatório exportado como: {nome_arquivo}", parent=self)

    def exportar_clientes_excel(self):
        pass
    def exportar_produtos_excel(self):
        pass
    def exportar_pedidos_excel(self):
        pass