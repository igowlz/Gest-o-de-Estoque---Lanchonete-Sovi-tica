import tkinter as tk
from tkinter import ttk
from BancoDeDados import BancoDeDados  # Supondo que o código BancoDeDados.py está correto

class JanelaHistorico:
    def __init__(self, master):
        self.master = master
        self.master.title("Histórico de Pedidos")
        self.master.geometry("800x600")

        self.banco_dados = BancoDeDados()

        # Criar a Treeview (tabela)
        self.treeview = ttk.Treeview(self.master, columns=("ID Pedido", "ID Lanche", "Quantidade", "Data"), show="headings")
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Definir cabeçalhos da tabela
        self.treeview.heading("ID Pedido", text="ID Pedido")
        self.treeview.heading("ID Lanche", text="ID Lanche")
        self.treeview.heading("Quantidade", text="Quantidade")
        self.treeview.heading("Data", text="Data Pedido")

        self.carregar_historico()

    def carregar_historico(self):
        """Carregar e exibir os pedidos no histórico"""
        comando = "SELECT id_pedido, id_lanche, quantidade, data_pedido FROM Pedidos"
        pedidos = self.banco_dados.executar_comando(comando)

        # Limpar a Treeview antes de adicionar novos dados
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # Inserir dados no Treeview
        for pedido in pedidos:
            self.treeview.insert("", "end", values=(pedido['id_pedido'], pedido['id_lanche'], pedido['quantidade'], pedido['data_pedido']))

# Execução do programa
root = tk.Tk()
app = JanelaHistorico(root)
root.mainloop()
