class ItemMenu:
    """
    Essa classe representa os lanches no menu da lanchonete
    """
    def __init__(self, id_lanche, nome, ingredientes):
        self.id_lanche = id_lanche
        self.nome = nome
        self.ingredientes = ingredientes  # Lista de objetos Ingrediente

    def calcular_ingredientes(self, quantidade):
        """Método para calcular a quantidade de cada ingrediente baseado no pedido"""
        ingredientes_necessarios = {}
        for ingrediente in self.ingredientes:
            ingredientes_necessarios[ingrediente.nome] = ingrediente.quantidade * quantidade
        return ingredientes_necessarios
