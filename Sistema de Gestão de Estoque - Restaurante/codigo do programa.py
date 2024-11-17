import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

class Ingrediente:
    def __init__(self, nome, categoria, quantidade, unidade, quantidade_minima):
        self.nome = nome
        self.categoria = categoria
        self.quantidade = quantidade  # Pode ser float ou int, dependendo do ingrediente
        self.unidade = unidade
        self.quantidade_minima = quantidade_minima

    def __str__(self):
        return f"{self.nome.capitalize()} - {self.quantidade} {self.unidade}(s) (Min: {self.quantidade_minima})"


# Quantidades dos ingredientes por lanche (considerando as quantidades de cada ingrediente por lanche)
quantidades_ingredientes_por_lanche = {
    "Hot Dog": {"pão": 1, "salsicha": 0.112, "vinagrete": 0.050, "ketchup": 0.040, "mostarda": 0.030, "maionese": 0.040, "batata palha": 0.010},
    "X Burguer": {"pão": 1, "hamburguer": 0.110, "queijo": 0.090, "ketchup": 0.040, "maionese": 0.040, "mostarda": 0.030},
    "X Salada": {"pão": 1, "hamburguer": 0.110, "tomate": 0.030, "presunto": 0.120, "queijo": 0.090, "alface": 0.030, "maionese": 0.040, "ketchup": 0.040, "mostarda": 0.030},
    "Misto Quente": {"pão": 1, "presunto": 0.120, "queijo": 0.090, "batata palha": 0.010},
    "Bauru": {"pão": 1, "presunto": 0.120, "queijo": 0.090, "tomate": 0.030, "maionese": 0.040, "ketchup": 0.040, "mostarda": 0.030},
    "Xegg": {"pão": 1, "hamburguer": 0.110, "ovo": 2, "presunto": 0.120, "queijo": 0.090, "alface": 0.030, "vinagrete": 0.050, "maionese": 0.040, "mostarda": 0.030},
    "Xmilho": {"pão": 1, "hamburguer": 0.110, "milho": 0.040, "queijo": 0.090, "presunto": 0.120, "vinagrete": 0.050, "alface": 0.030, "maionese": 0.040, "ketchup": 0.040, "mostarda": 0.030},
    "X Calabresa": {"pão": 1, "calabresa": 0.050, "queijo": 0.090, "maionese": 0.040, "mostarda": 0.030, "ketchup": 0.040, "vinagrete": 0.050, "alface": 0.030},
    "Xbacon": {"pão": 1, "hamburguer": 0.110, "bacon": 0.050, "queijo": 0.090, "vinagrete": 0.050, "alface": 0.030, "maionese": 0.040, "mostarda": 0.030, "ketchup": 0.040},
    "Xfrango": {"pão": 1, "frango": 0.120, "presunto": 0.120, "queijo": 0.090, "maionese": 0.040, "ketchup": 0.040, "alface": 0.030, "vinagrete": 0.050}
}

class InterfaceSistema:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Gestão de Pedidos - Lanchonete")
        self.master.geometry("1200x700")  # Ajustei a largura para dar mais espaço
        self.master.config(bg="#f4f4f9")

        self.ingredientes = [
            Ingrediente("pão", "Alimento", 50, "unidade", 10),
            Ingrediente("salsicha", "Alimento", 3.36, "kg", 0.5),
            Ingrediente("vinagrete", "Condimento", 1000, "g", 0.5),
            Ingrediente("maionese", "Condimento", 1000, "ml", 0.5),
            Ingrediente("ketchup", "Condimento", 1000, "ml", 0.5),
            Ingrediente("mostarda", "Condimento", 1000, "ml", 0.5),
            Ingrediente("batata palha", "Alimento", 200, "g", 0.5),
            Ingrediente("hamburguer", "Carne", 2.2, "kg", 0.5),
            Ingrediente("queijo", "Lácteo", 4.5, "kg", 0.5),
            Ingrediente("presunto", "Carne", 3.6, "kg", 0.5),
            Ingrediente("tomate", "Legume", 1, "kg", 0.5),
            Ingrediente("alface", "Legume", 1, "kg", 0.5),
            Ingrediente("ovo", "Alimento", 30, "unidade", 0.5),
            Ingrediente("milho", "Legume", 1, "kg", 0.5),
            Ingrediente("calabresa", "Carne", 1, "kg", 0.5),
            Ingrediente("bacon", "Carne", 1, "kg", 0.5),
            Ingrediente("frango", "Carne", 1.44, "kg", 0.5)
        ]

        self.pedidos = []  # Lista para armazenar lanches e suas quantidades
        self.historico_pedidos = []  # Lista para armazenar o histórico de pedidos
        self.criar_componentes()

    def criar_componentes(self):
        # Layout Grid para melhor organização
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=2)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=3)
        self.master.grid_rowconfigure(2, weight=1)

        # Estoque à esquerda
        self.estoque_frame = tk.Frame(self.master, bg="#f4f4f9", bd=2, relief="solid")
        self.estoque_frame.grid(row=0, column=0, rowspan=3, padx=20, pady=20, sticky="nsew")

        # Título da Tabela de Estoque
        tk.Label(self.estoque_frame, text="Estoque de Ingredientes", font=("Arial", 12, "bold"), bg="#f4f4f9").pack(pady=10)

        # Criação da Tabela de Estoque com Treeview
        self.treeview = ttk.Treeview(self.estoque_frame, columns=("Ingrediente", "Quantidade"), show="headings", height=15)
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Definir as colunas
        self.treeview.heading("Ingrediente", text="Ingrediente")
        self.treeview.heading("Quantidade", text="Quantidade")
        self.treeview.column("Ingrediente", width=120, anchor=tk.W)
        self.treeview.column("Quantidade", width=100, anchor=tk.CENTER)

        # Carregar dados do estoque na tabela
        self.atualizar_estoque_tabela()

        # Painel de pedidos à direita (onde ficará o resumo do pedido e a confirmação)
        self.pedido_frame = tk.Frame(self.master, bg="#f4f4f9", bd=2, relief="solid")
        self.pedido_frame.grid(row=0, column=1, rowspan=3, padx=20, pady=20, sticky="nsew")

        # Título do painel de pedidos
        tk.Label(self.pedido_frame, text="Pedido", font=("Arial", 14, "bold"), bg="#f4f4f9").grid(row=0, column=0, pady=10)

        # Seção de Seleção de Lanches
        self.lanche_selecionado = ""
        row = 1
        for lanche in quantidades_ingredientes_por_lanche.keys():
            btn = tk.Button(self.pedido_frame, text=lanche, command=lambda lanche=lanche: self.selecionar_lanche(lanche), font=("Arial", 9), width=20, relief="solid", bg="#4CAF50", fg="white")
            btn.grid(row=row, column=0, pady=2, padx=10, sticky="ew")
            row += 1

        # Quantidade do Lanche
        self.quantidade_var = tk.IntVar(value=1)
        self.quantidade_label = tk.Label(self.pedido_frame, textvariable=self.quantidade_var, font=("Arial", 14), bg="#f4f4f9")
        self.quantidade_label.grid(row=row, column=0, pady=5)
        row += 1

        # Botões para aumentar ou diminuir a quantidade
        tk.Button(self.pedido_frame, text="-", command=self.diminuir_quantidade, font=("Arial", 9), width=4).grid(row=row, column=0, pady=5, padx=5, sticky="w")
        tk.Button(self.pedido_frame, text="+", command=self.aumentar_quantidade, font=("Arial", 9), width=4).grid(row=row, column=1, pady=5, padx=5, sticky="w")
        row += 1

        # Botão para adicionar ao pedido
        self.adicionar_btn = tk.Button(self.pedido_frame, text="Adicionar ao Pedido", command=self.adicionar_ao_pedido, bg="#4CAF50", fg="white", font=("Arial", 9), relief="solid", width=14)
        self.adicionar_btn.grid(row=row, column=0, pady=10, padx=10, sticky="ew")
        row += 1

        # Resumo do pedido e botão "Confirmar Pedido" lado a lado
        row += 1
        frame_resumo = tk.Frame(self.pedido_frame, bg="#f4f4f9")
        frame_resumo.grid(row=row, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        self.resumo_text = tk.Text(frame_resumo, height=10, width=30, font=("Arial", 12), state=tk.DISABLED)
        self.resumo_text.pack(side="left", fill="both", expand=True)

        # Botão de confirmação ao lado do resumo
        self.confirmar_btn = tk.Button(frame_resumo, text="Confirmar Pedido", command=self.confirmar_pedido, bg="#4CAF50", fg="white", font=("Arial", 9), relief="solid", width=14)
        self.confirmar_btn.pack(side="right", padx=10)

        # Botão de histórico de pedidos
        self.historico_btn = tk.Button(self.pedido_frame, text="Histórico de Pedidos", command=self.mostrar_historico, bg="#FF5722", fg="white", font=("Arial", 9), relief="solid", width=20)
        self.historico_btn.grid(row=row + 1, column=0, pady=10, padx=10, sticky="ew")

    def selecionar_lanche(self, lanche):
        """Seleciona o lanche e atualiza a quantidade para 1"""
        self.lanche_selecionado = lanche
        self.quantidade_var.set(1)  # Reset quantity to 1 when selecting a new lanche
        self.atualizar_resumo_pedido()

    def adicionar_ao_pedido(self):
        """Adiciona o lanche ao pedido"""
        lanche = self.lanche_selecionado
        quantidade = self.quantidade_var.get()

        if lanche:
            self.pedidos.append((lanche, quantidade))
            self.atualizar_resumo_pedido()
        else:
            messagebox.showwarning("Seleção de Lanche", "Por favor, selecione um lanche!")

    def atualizar_resumo_pedido(self):
        """Atualiza o resumo do pedido com os lanches e quantidades"""
        resumo = "Resumo do Pedido:\n"
        for lanche, quantidade in self.pedidos:
            resumo += f"- {lanche} (x{quantidade})\n"
        self.resumo_text.config(state=tk.NORMAL)
        self.resumo_text.delete(1.0, tk.END)
        self.resumo_text.insert(tk.END, resumo)
        self.resumo_text.config(state=tk.DISABLED)

    def aumentar_quantidade(self):
        """Aumenta a quantidade de lanches no pedido"""
        self.quantidade_var.set(self.quantidade_var.get() + 1)
        self.atualizar_resumo_pedido()

    def diminuir_quantidade(self):
        """Diminui a quantidade de lanches no pedido"""
        if self.quantidade_var.get() > 1:
            self.quantidade_var.set(self.quantidade_var.get() - 1)
            self.atualizar_resumo_pedido()

    def confirmar_pedido(self):
        """Confirma e registra o pedido, retirando os ingredientes do estoque"""
        if self.pedidos:
            # Verificar se o estoque é suficiente para o pedido
            for lanche, quantidade in self.pedidos:
                ingredientes_necessarios = quantidades_ingredientes_por_lanche[lanche]
                for ingrediente_nome, quantidade_necessaria in ingredientes_necessarios.items():
                    ingrediente = next((i for i in self.ingredientes if i.nome == ingrediente_nome), None)
                    if ingrediente:
                        if isinstance(quantidade_necessaria, int):  # Para ingredientes em unidades
                            if ingrediente.quantidade >= quantidade_necessaria * quantidade:
                                ingrediente.quantidade -= quantidade_necessaria * quantidade
                            else:
                                messagebox.showwarning("Estoque Insuficiente", f"Estoque insuficiente para {ingrediente_nome}.")
                                return
                        elif isinstance(quantidade_necessaria, (float, int)):  # Para ingredientes em gramas ou mililitros
                            if ingrediente.quantidade >= quantidade_necessaria * quantidade:
                                ingrediente.quantidade -= quantidade_necessaria * quantidade
                            else:
                                messagebox.showwarning("Estoque Insuficiente", f"Estoque insuficiente para {ingrediente_nome}.")
                                return

            # Adicionar ao histórico de pedidos com a data atual
            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.historico_pedidos.append((data_atual, self.pedidos.copy()))
            
            # Atualizar a Tabela de Estoque e mostrar confirmação
            self.atualizar_estoque_tabela()
            messagebox.showinfo("Pedido Confirmado", f"Seu pedido de {len(self.pedidos)} lanche(s) foi registrado com sucesso!")
            self.pedidos.clear()
            self.atualizar_resumo_pedido()
        else:
            messagebox.showwarning("Pedido Vazio", "Não há lanches no pedido para confirmar.")

    def atualizar_estoque_tabela(self):
        """Atualiza a Tabela de Estoque"""
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        for ingrediente in self.ingredientes:
            self.treeview.insert("", "end", values=(ingrediente.nome.capitalize(), f"{ingrediente.quantidade}"))

    def mostrar_historico(self):
        """Exibe a janela com o histórico de pedidos"""
        historico_window = tk.Toplevel(self.master)
        historico_window.title("Histórico de Pedidos")
        historico_window.geometry("400x400")
        historico_window.config(bg="#f4f4f9")

        # Título
        tk.Label(historico_window, text="Histórico de Pedidos", font=("Arial", 14, "bold"), bg="#f4f4f9").pack(pady=10)

        # Exibir os pedidos
        if not self.historico_pedidos:
            messagebox.showinfo("Histórico", "Nenhum pedido realizado.")
        else:
            texto_historico = ""
            for data, pedido in self.historico_pedidos:
                texto_historico += f"{data}\n"
                for lanche, quantidade in pedido:
                    texto_historico += f"  - {lanche} (x{quantidade})\n"
                texto_historico += "\n"
            tk.Label(historico_window, text=texto_historico, font=("Arial", 12), bg="#f4f4f9").pack(pady=10)

# Inicialização da janela principal
root = tk.Tk()
app = InterfaceSistema(root)
root.mainloop()
