import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
#Import corrected below:
from BancoDeDados import BancoDeDados  
from JanelaHistorico import JanelaHistorico

class JanelaPrincipal:
    def __init__(self, master):
        self.master = master

class JanelaPrincipal:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Gestão de Estoque - Restaurante")
        # self.master.attributes('-fullscreen', True)  # Removed fullscreen attribute
        self.master.geometry("1366x768")  # Set a specific window size
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

        # Botão para fazer pedidos
        self.botao_pedido = tk.Button(self.master, text="Fazer Pedido", bg="#FF5722", fg="white", command=self.fazer_pedido)
        self.botao_pedido.place(x=50, y=190, width=200, height=50)

    def criar_lista_estoque(self):
        # Configuração da tabela de ingredientes
        self.treeview_estoque = ttk.Treeview(self.master, columns=("ID", "Nome", "Categoria", "Quantidade", "Preço/Kg", "Data Recebimento", "Quant. Mínima"), show="headings")
        self.treeview_estoque.heading("ID", text="ID")
        self.treeview_estoque.heading("Nome", text="Nome")
        self.treeview_estoque.heading("Categoria", text="Categoria")
        self.treeview_estoque.heading("Quantidade", text="Quantidade")
        self.treeview_estoque.heading("Preço/Kg", text="Preço/Kg")
        self.treeview_estoque.heading("Data Recebimento", text="Data Recebimento")
        self.treeview_estoque.heading("Quant. Mínima", text="Quant. Mínima")
        self.treeview_estoque.place(x=300, y=50, width=1000, height=500)
        self.treeview_estoque.column("#0", width=0, stretch=False)  # Hide default column

        # Carrega os ingredientes da base de dados
        self.carregar_ingredientes()

    def carregar_ingredientes(self):
        # Limpa a tabela antes de atualizar
        for row in self.treeview_estoque.get_children():
            self.treeview_estoque.delete(row)

        ingredientes = self.banco_dados.buscar_ingredientes()
        if ingredientes:
            for ingrediente in ingredientes:
                # Correctly order the data for Treeview insertion
                values = (ingrediente['id_ingrediente'], ingrediente['nome'], ingrediente['categoria'], ingrediente['quantidade'], ingrediente['preco_quilo'], ingrediente['data_recebimento'], ingrediente['quantidade_minima'])
                self.treeview_estoque.insert("", "end", values=values)

    def adicionar_ingrediente(self):
        nova_janela = tk.Toplevel(self.master)
        nova_janela.title("Adicionar Ingrediente")
        nova_janela.geometry("400x400")

        labels = ["Nome", "Categoria", "Quantidade", "Preço por Kg", "Data de Recebimento (AAAA-MM-DD)", "Quantidade Mínima"]
        entries = []
        for i, label_text in enumerate(labels):
            tk.Label(nova_janela, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            entry = tk.Entry(nova_janela)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        def salvar():
            data = [entry.get() for entry in entries]
            if all(data):
                try:
                    quantidade = float(data[2])
                    preco_quilo = float(data[3])
                    quantidade_minima = float(data[5])
                    self.banco_dados.adicionar_ou_atualizar_ingrediente(data)
                    messagebox.showinfo("Sucesso", "Ingrediente adicionado/atualizado com sucesso!")
                    nova_janela.destroy()
                    self.carregar_ingredientes()
                except ValueError:
                    messagebox.showerror("Erro", "Quantidade, Preço por Kg e Quantidade Mínima devem ser números!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao adicionar/atualizar ingrediente: {e}")
            else:
                messagebox.showerror("Erro", "Preencha todos os campos!")

        salvar_button = tk.Button(nova_janela, text="Salvar", command=salvar)
        salvar_button.grid(row=len(labels), column=1, pady=20)

    def abrir_historico(self):
        nova_janela = tk.Toplevel(self.master)
        app_historico = JanelaHistorico(nova_janela)

    def fazer_pedido(self):
        self.nova_janela = tk.Toplevel(self.master)
        self.nova_janela.title("Fazer Pedido")
        self.nova_janela.geometry("600x400")

        lanches = [
            "Hot-Dog",
            "X-burguer",
            "X-salada",
            "Misto-quente",
            "Bauru",
            "X-egg",
            "X-milho",
            "X-calabresa",
            "X-bacon",
            "X-frango"
        ]

        pedidos_frame = tk.Frame(self.nova_janela)
        pedidos_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        labels = ["Lanche", "Quantidade"]
        for i, label in enumerate(labels):
            tk.Label(pedidos_frame, text=label).grid(row=0, column=i, padx=10, pady=10)

        self.lanche_vars = []
        self.quantidade_entries = []

        def adicionar_pedido():
            row = len(self.lanche_vars) + 1
            lanche_var = tk.StringVar()
            lanche_combobox = ttk.Combobox(pedidos_frame, textvariable=lanche_var, values=lanches)
            lanche_combobox.grid(row=row, column=0, padx=10, pady=10)

            quantidade_entry = tk.Entry(pedidos_frame)
            quantidade_entry.grid(row=row, column=1, padx=10, pady=10)

            self.lanche_vars.append(lanche_var)
            self.quantidade_entries.append(quantidade_entry)

        def salvar_pedidos():
            errors = []
            for lanche_var, quantidade_entry in zip(self.lanche_vars, self.quantidade_entries):
                lanche = lanche_var.get()
                quantidade = quantidade_entry.get()

                if not lanche or not quantidade:
                    errors.append("Preencha todos os campos de cada pedido!")
                    continue

                try:
                    self.banco_dados.adicionar_pedido(lanche, quantidade)
                except Exception as e:
                    errors.append(f"Erro ao adicionar pedido {lanche}: {e}")

            if errors:
                messagebox.showerror("Erro", "\n".join(errors))
            else:
                messagebox.showinfo("Sucesso", "Pedidos realizados com sucesso!")
                self.nova_janela.destroy()
                self.abrir_historico()

        adicionar_pedido_button = tk.Button(self.nova_janela, text="Adicionar Pedido", command=adicionar_pedido)
        adicionar_pedido_button.pack(side=tk.LEFT, padx=10, pady=10)

        salvar_pedidos_button = tk.Button(self.nova_janela, text="Salvar Pedidos", command=salvar_pedidos)
        salvar_pedidos_button.pack(side=tk.RIGHT, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = JanelaPrincipal(root)
    root.mainloop()