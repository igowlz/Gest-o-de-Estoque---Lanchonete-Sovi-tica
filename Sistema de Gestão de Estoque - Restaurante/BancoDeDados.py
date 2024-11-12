import mysql.connector

class BancoDeDados:
        def __init__(self):
                self.conexao = mysql.connector.connect(
                        host ="localhost",
                        user = "admin123",
                        password = "admin123",
                        database = "Banco_Lanchonete"
                )
                self.cursor = self.conexao.cursor(dictionary=True)

                def executar_comando(self, comando, valores=None):
                        self.cursor.execute(comando, valores)
                        self.conexao.commit()
                        return self.cursor.fetchall()
                
                def adicionar_ingrediente(self, nome, categoria, quantidade, preco_quilo, data_recebimento, quantidade_minima):
                        # receber comando passado pelo usuário
                        comando = """""
                        INSERT INTO Ingredientes (nome, categoria, quantidade, preco_quilo, data_recebimento, quantidade_minima)
                        VALUES (%s, %s, %s, %s, %s. %s)

                        """
                        valores = (nome, categoria, quantidade, preco_quilo, data_recebimento, quantidade_minima)
                        self.executar_comando(comando, valores)

                def registrar_pedido(self, banco_dados, id_lanche, quantidade):
                        # obter a receita do lanche
                        comando_receita = "SELECT id_ingrediente, quantidade_ingrediente FROM Receita WHERE id_lanche = %s"
                        ingredientes = banco_dados.executar_comando(comando_receita, (id_lanche,))

                        # verificar e atualizar estoque
                        for ingrediente in ingredientes:
                                id_ingrediente = ingrediente['id_ingrediente']
                                quantidade_necessaria = ingrediente['quantidade_ingrediente'] * quantidade

                                # verifica o estoque
                                comando_estoque = "SELECT quantidade FROM Ingredientes WHERE id_ingrediente = %s"
                                estoque = banco_dados.executar_comando(comando_estoque, (id_ingrediente,))[0]['quantidade']

                                if (estoque < quantidade_necessaria):
                                        print("Estoque insuficiente para o ingrediente: ", id_ingrediente)
                                        return False
                            
                                # da baixa no estoque
                                comando_update = "UPDATE Ingredientes SET quantidade = quantidade - %s WHERE id_ingrediente = %s"
                                banco_dados.executar_comando(comando_update, (quantidade_necessaria, id_ingrediente))

                        #registrar o pedido
                        comando_pedido = "INSERT INTO Pedidos (id_lanche, quantidade, data_pedido) VALUES (%s, %s, CURRENT_TIMESTAMP)"
                        banco_dados.executar_comando(comando_pedido, (id_lanche, quantidade))
                        

                        print("Pedido registrado com sucesso!")
                        return True