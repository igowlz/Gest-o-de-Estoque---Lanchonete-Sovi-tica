import tkinter as tk
from tkinter import ttk
from BancoDeDados import BancoDeDados

class JanelaHistorico:
    def __init__(self, master):
        self.master = master
        self.master.title("Histórico de Pedidos")
        self.master.geometry("800x600")

        self.banco_dados = BancoDeDados()

        self.treeview = ttk.Treeview(self.master, columns=("ID Pedido", "Lanche", "Quantidade", "Data"), show="headings")
        self.treeview.heading("ID Pedido", text="ID Pedido")
        self.treeview.heading("Lanche", text="Lanche")
        self.treeview.heading("Quantidade", text="Quantidade")
        self.treeview.heading("Data", text="Data do Pedido")
        self.treeview.pack(fill=tk.BOTH, expand=True)

        self.carregar_historico()

    def carregar_historico(self):
        self.treeview.delete(*self.treeview.get_children())
        comando_sql = """
            SELECT 
                p.id_pedido, 
                l.nome AS lanche, 
                p.quantidade, 
                p.data_pedido,
                p.id_lanche
            FROM Pedidos p
            JOIN Lanches l ON p.id_lanche = l.id_lanche;
        """
        pedidos = self.banco_dados.executar_comando(comando_sql)
        print("Dados recebidos do banco de dados:", pedidos) #This line added to check the data
        if pedidos:
            for pedido in pedidos:
                try:
                    self.treeview.insert("", "end", values=(pedido['id_pedido'], pedido['lanche'], pedido['quantidade'], pedido['data_pedido']))
                except KeyError as e:
                    print(f"Erro ao inserir dados no Treeview: {e}. Dados do pedido: {pedido}")
        if pedidos:
            for pedido in pedidos:
                self.treeview.insert("", "end", values=(pedido['id_pedido'], pedido['id_lanche'], pedido['quantidade'], pedido['data_pedido']))

# Execução do programa
if __name__ == "__main__":
    root = tk.Tk()
    app = JanelaHistorico(root)
    root.mainloop()
