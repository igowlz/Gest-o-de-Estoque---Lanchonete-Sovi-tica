import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from BancoDeDados import BancoDeDados

class JanelaPrincipal:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Gestão de Estoque - Restaurante")
        self.master.attributes('-fullscreen', True)
        self.master.configure(bg="#e6e6e6")

        self.banco_dados = BancoDeDados()

        # Configuração dos botões
        self.criar_botoes()
        self.criar_lista_estoque()

    def criar_botoes(self):
        # Botão para adicionar ingrediente
        self.botao_adicionar = tk.Button(self.master, text="Adicionar Ingrediente", bg="#4CAF50", fg="white", command=self.adicionar_ingrediente)
        self.botao_adicionar.place(x=50, y=50, width=200, height=50)

        # Botão para abrir o histórico
        self.botao_historico = tk.Button(self.master, text="Ver Histórico de Pedidos", bg="#2196F3", fg="white", command=self.abrir_historico)
        self.botao_historico.place(x=50, y=120, width=200, height=50)

    def criar_lista_estoque(self):
        # Configuração da tabela de ingredientes
        self.treeview_estoque = ttk.Treeview(self.master, columns=("ID", "Nome", "Quantidade", "Unidade", "Categoria"), show="headings")
        self.treeview_estoque.heading("ID", text="ID")
        self.treeview_estoque.heading("Nome", text="Nome")
        self.treeview_estoque.heading("Quantidade", text="Quantidade")
        self.treeview_estoque.heading("Unidade", text="Unidade")
        self.treeview_estoque.heading("Categoria", text="Categoria")
        self.treeview_estoque.place(x=300, y=50, width=1000, height=500)

        # Carrega os ingredientes da base de dados
        self.carregar_ingredientes()

    def carregar_ingredientes(self):
        # Limpa a tabela antes de atualizar
        for row in self.treeview_estoque.get_children():
            self.treeview_estoque.delete(row)

        # Consulta ingredientes no banco de dados
        ingredientes = self.banco_dados.buscar_ingredientes()
        if ingredientes:
            for ingrediente in ingredientes:
                self.treeview_estoque.insert("", "end", values=ingrediente)

    def adicionar_ingrediente(self):
        # Janela para inserir novo ingrediente
        nova_janela = tk.Toplevel(self.master)
        nova_janela.title("Adicionar Ingrediente")
        nova_janela.geometry("400x400")

        # Labels e entradas para os dados do ingrediente
        tk.Label(nova_janela, text="Nome").grid(row=0, column=0, padx=10, pady=10)
        nome_entry = tk.Entry(nova_janela)
        nome_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(nova_janela, text="Quantidade").grid(row=1, column=0, padx=10, pady=10)
        quantidade_entry = tk.Entry(nova_janela)
        quantidade_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(nova_janela, text="Unidade").grid(row=2, column=0, padx=10, pady=10)
        unidade_entry = tk.Entry(nova_janela)
        unidade_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(nova_janela, text="Categoria").grid(row=3, column=0, padx=10, pady=10)
        categoria_entry = tk.Entry(nova_janela)
        categoria_entry.grid(row=3, column=1, padx=10, pady=10)

        def salvar():
            nome = nome_entry.get()
            quantidade = quantidade_entry.get()
            unidade = unidade_entry.get()
            categoria = categoria_entry.get()

            if nome and quantidade and unidade and categoria:
                self.banco_dados.adicionar_ingrediente(nome, quantidade, unidade, categoria)
                messagebox.showinfo("Sucesso", "Ingrediente adicionado com sucesso!")
                nova_janela.destroy()
                self.carregar_ingredientes()
            else:
                messagebox.showerror("Erro", "Preencha todos os campos!")

        # Botão para salvar o ingrediente
        salvar_button = tk.Button(nova_janela, text="Salvar", command=salvar)
        salvar_button.grid(row=4, column=1, pady=20)

    def abrir_historico(self):
        # Janela para mostrar o histórico
        nova_janela = tk.Toplevel(self.master)
        nova_janela.title("Histórico de Pedidos")
        nova_janela.geometry("600x400")

        # Tabela para exibir o histórico de pedidos
        treeview_historico = ttk.Treeview(nova_janela, columns=("ID Pedido", "Lanche", "Quantidade", "Data"), show="headings")
        treeview_historico.heading("ID Pedido", text="ID Pedido")
        treeview_historico.heading("Lanche", text="Lanche")
        treeview_historico.heading("Quantidade", text="Quantidade")
        treeview_historico.heading("Data", text="Data")
        treeview_historico.pack(fill="both", expand=True)

        # Carrega o histórico de pedidos
        pedidos = self.banco_dados.buscar_pedidos()
        if pedidos:
            for pedido in pedidos:
                treeview_historico.insert("", "end", values=pedido)

if __name__ == "__main__":
    root = tk.Tk()
    app = JanelaPrincipal(root)
    root.mainloop()
