class Pedido:
    def __init__(self, id_pedido, id_lanche, quantidade):
        self.id_pedido = id_pedido
        self.id_lanche = id_lanche
        self.quantidade = quantidade

    def processar_pedido(self, banco_dados):
        """Método para processar o pedido, incluindo a atualização do estoque"""
        # 1. Buscar a receita do lanche
        comando_receita = "SELECT id_ingrediente, quantidade_ingrediente FROM Receita WHERE id_lanche = %s"
        ingredientes = banco_dados.executar_comando(comando_receita, (self.id_lanche,))

        # 2. Atualizar o estoque conforme os ingredientes
        for ingrediente in ingredientes:
            id_ingrediente = ingrediente['id_ingrediente']
            quantidade_necessaria = ingrediente['quantidade_ingrediente'] * self.quantidade

            # 3. Verificar se há estoque suficiente e atualizar
            comando_estoque = "SELECT quantidade FROM Ingredientes WHERE id_ingrediente = %s"
            estoque = banco_dados.executar_comando(comando_estoque, (id_ingrediente,))[0]['quantidade']

            if estoque < quantidade_necessaria:
                print("Estoque insuficiente para o ingrediente:", id_ingrediente)
                return False

            # 4. Atualizar o estoque
            comando_update = "UPDATE Ingredientes SET quantidade = quantidade - %s WHERE id_ingrediente = %s"
            banco_dados.executar_comando(comando_update, (quantidade_necessaria, id_ingrediente))

        # 5. Registrar o pedido
        comando_pedido = "INSERT INTO Pedidos (id_lanche, quantidade) VALUES (%s, %s)"
        banco_dados.executar_comando(comando_pedido, (self.id_lanche, self.quantidade))

        print(f"Pedido {self.id_pedido} registrado e estoque atualizado.")
        return True
