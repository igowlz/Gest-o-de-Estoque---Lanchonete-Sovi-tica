class Ingrediente:
    def __init__(self, nome, categoria, quantidade, preco_quilo, data_recebimento, quantidade_minima):
        self.nome = nome
        self.categoria = categoria
        self.quantidade = quantidade
        self.preco_quilo = preco_quilo
        self.data_recebimento = data_recebimento
        self.quantidade_minima = quantidade_minima

    def __str__(self):
        """ Representação em string do ingrediente"""
        return f"{self.nome} - {self.quantidade} unidades, Validade: {self.validade.strftime('%Y-%m-%d')} "
    
        
    def atualizar_estoque(self, quantidade):
        """Método para dar baixa ou adicionar no estoque"""
        self.quantidade += quantidade
        if self.quantidade < self.quantidade_minima:
            print(f"Alerta: o estoque de {self.nome} está abaixo do mínimo.")