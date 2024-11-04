class Ingrediente:
    def __init__(self, nome, categoria, quantidade, preco, lote, validade, fornecedor, quantidade_minima, nota_fiscal):
        self.nome = nome
        self.categoria = categoria
        self.quantidade = quantidade
        self.lote = lote
        self.validade = validade
        self.fornecedor = fornecedor
        self.quantidade_minima = quantidade_minima
        self.nota_fiscal = nota_fiscal
        self.lista = []

    def __str__(self):
        """ Representação em string do ingrediente"""
        return f"{self.nome} - {self.quantidade} unidades, Validade: {self.validade.strftime('%Y-%m-%d')} "
    
        
    