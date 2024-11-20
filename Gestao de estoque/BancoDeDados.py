import mysql.connector
import logging

# Configure logging (optional but recommended)
logging.basicConfig(filename='database_log.txt', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class BancoDeDados:
    def __init__(self):
        try:
            self.conexao = mysql.connector.connect(
                host="localhost",
                user="admin123",  # Substitua com seu nome de usuário
                password="admin123",  # Substitua com sua senha
                database="banco_lanchonete"  # Substitua com o nome do seu banco de dados
            )
            self.cursor = self.conexao.cursor(dictionary=True)
            print("Conexão bem-sucedida!")
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao banco de dados: {err}")
            logging.exception(f"Erro ao conectar ao banco de dados: {err}")
            self.conexao = None
            self.cursor = None

    def buscar_ingredientes(self):
        if self.cursor:
            comando = """
                SELECT id_ingrediente, nome, categoria, quantidade, preco_quilo, data_recebimento, quantidade_minima
                FROM Ingredientes
            """
            try:
                self.cursor.execute(comando)
                ingredientes = self.cursor.fetchall()
                return ingredientes
            except mysql.connector.Error as err:
                print(f"Erro ao buscar ingredientes: {err}")
                logging.exception(f"Erro ao buscar ingredientes: {err}")
                return None
        return None

    def adicionar_ou_atualizar_ingrediente(self, data):
        if self.cursor:
            nome = data[0]
            categoria = data[1]
            quantidade = float(data[2])
            preco_quilo = float(data[3])
            data_recebimento = data[4]
            quantidade_minima = float(data[5])

            comando_verificar = "SELECT id_ingrediente, quantidade FROM Ingredientes WHERE nome = %s"
            self.cursor.execute(comando_verificar, (nome,))
            resultado = self.cursor.fetchone()

            if resultado:
                id_ingrediente = resultado['id_ingrediente']
                quantidade_atual = resultado['quantidade']
                nova_quantidade = quantidade_atual + quantidade
                comando_atualizar = """
                    UPDATE Ingredientes 
                    SET quantidade = %s, preco_quilo=%s, data_recebimento=%s, quantidade_minima=%s, categoria=%s
                    WHERE id_ingrediente = %s
                """
                self.cursor.execute(comando_atualizar, (nova_quantidade, preco_quilo, data_recebimento, quantidade_minima, categoria, id_ingrediente))
            else:
                comando_inserir = """
                    INSERT INTO Ingredientes (nome, categoria, quantidade, preco_quilo, data_recebimento, quantidade_minima) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                self.cursor.execute(comando_inserir, (nome, categoria, quantidade, preco_quilo, data_recebimento, quantidade_minima))

            self.conexao.commit()

    def buscar_pedidos(self):
        if self.cursor:
            comando = "SELECT id_pedido, l.nome, quantidade, data_pedido FROM Pedidos p JOIN Lanches l ON p.id_lanche = l.id_lanche"
            try:
                self.cursor.execute(comando)
                pedidos = self.cursor.fetchall()
                return pedidos
            except mysql.connector.Error as err:
                print(f"Erro ao buscar pedidos: {err}")
                logging.exception(f"Erro ao buscar pedidos: {err}")
                return None
        return None

    def adicionar_pedido(self, id_lanche, quantidade):
        if self.cursor:
            if self.verificar_disponibilidade_ingredientes(id_lanche, quantidade):
                comando_pedido = "INSERT INTO Pedidos (id_lanche, quantidade, data_pedido) VALUES (%s, %s, NOW())"
                try:
                    self.cursor.execute(comando_pedido, (id_lanche, quantidade))
                    self.atualizar_estoque(id_lanche, quantidade)
                    self.conexao.commit()
                    logging.info(f"Pedido de lanche (ID: {id_lanche}) realizado com sucesso!")
                    return True
                except mysql.connector.Error as err:
                    logging.exception(f"Erro ao adicionar pedido: {err}")
                    return False
            else:
                return False
        return False

    def atualizar_estoque(self, id_lanche, quantidade_pedido):
        comando_receita = """
            SELECT i.nome, ri.quantidade_ingrediente 
            FROM Receita ri
            JOIN Ingredientes i ON ri.id_ingrediente = i.id_ingrediente
            WHERE ri.id_lanche = %s
        """
        try:
            self.cursor.execute(comando_receita, (id_lanche,))
            receita = self.cursor.fetchall()
            for ingrediente in receita:
                nome_ingrediente = ingrediente['nome']
                quantidade_necessaria = ingrediente['quantidade_ingrediente'] * quantidade_pedido

                comando_update = "UPDATE Ingredientes SET quantidade = quantidade - %s WHERE nome = %s"
                self.cursor.execute(comando_update, (quantidade_necessaria, nome_ingrediente))
        except mysql.connector.Error as err:
            logging.exception(f"Erro ao atualizar estoque: {err}")

    def buscar_id_lanche(self, nome_lanche):
        if self.cursor:
            comando = "SELECT id_lanche FROM Lanches WHERE nome = %s"
            try:
                self.cursor.execute(comando, (nome_lanche,))
                resultado = self.cursor.fetchone()
                if resultado:
                    return resultado['id_lanche']
                else:
                    logging.warning(f"Lanche {nome_lanche} não encontrado na tabela Lanches.")
                    return None
            except mysql.connector.Error as err:
                logging.exception(f"Erro ao buscar ID do lanche: {err}")
                return None
        return None


    def verificar_disponibilidade_ingredientes(self, id_lanche, quantidade_pedido):
        if self.cursor is None:
            return False

        comando_receita = """
            SELECT i.nome, ri.quantidade_ingrediente 
            FROM Receita ri
            JOIN Ingredientes i ON ri.id_ingrediente = i.id_ingrediente
            WHERE ri.id_lanche = %s
        """
        try:
            self.cursor.execute(comando_receita, (id_lanche,))
            receita = self.cursor.fetchall()

            for ingrediente in receita:
                nome_ingrediente = ingrediente['nome']
                quantidade_necessaria = ingrediente['quantidade_ingrediente'] * quantidade_pedido

                comando_estoque = "SELECT quantidade FROM Ingredientes WHERE nome = %s"
                self.cursor.execute(comando_estoque, (nome_ingrediente,))
                estoque = self.cursor.fetchone()

                if estoque is None or estoque['quantidade'] < quantidade_necessaria:
                    logging.warning(f"Estoque insuficiente para o ingrediente: {nome_ingrediente} (Necessário: {quantidade_necessaria}, Disponível: {estoque['quantidade'] if estoque else 0})")
                    return False

            return True
        except mysql.connector.Error as err:
            logging.exception(f"Erro ao verificar disponibilidade de ingredientes: {err}")
            return False

    def executar_comando(self, comando, params=None):
        if self.cursor:
            try:
                self.cursor.execute(comando, params)
                resultados = self.cursor.fetchall()
                return resultados
            except mysql.connector.Error as err:
                print(f"Erro ao executar comando: {err}")
                logging.exception(f"Erro ao executar comando: {err}")
                return None
"""
INSERT IGNORE INTO Lanches (nome) VALUES
('Hot-Dog'),
('X-burguer'),
('X-salada'),
('Misto-quente'),
('Bauru'),
('X-egg'),
('X-milho'),
('X-calabresa'),
('X-bacon'),
('X-frango');

"""

"""
INSERT INTO Ingredientes (nome, categoria, quantidade, preco_quilo, data_recebimento, quantidade_minima) VALUES
('pão', 'Pães', 100.00, 15.00, '2024-03-15', 50.00),
('salsicha', 'Carnes', 200.00, 25.00, '2024-03-22', 100.00),
('hambúrguer', 'Carnes', 150.00, 30.00, '2024-03-29', 75.00),
('queijo', 'Queijos', 100.00, 40.00, '2024-04-05', 50.00),
('alface', 'Verduras', 500.00, 10.00, '2024-04-12', 250.00),
('tomate', 'Verduras', 400.00, 12.00, '2024-04-19', 200.00),
('ovo', 'Ovos', 300.00, 0.50, '2024-04-26', 150.00),
('milho', 'Grãos', 2000.00, 20.00, '2024-05-03', 1000.00),
('calabresa', 'Carnes', 500.00, 35.00, '2024-05-10', 250.00),
('bacon', 'Carnes', 400.00, 50.00, '2024-05-17', 200.00),
('frango', 'Carnes', 1000.00, 22.00, '2024-05-24', 500.00),
('cebola', 'Verduras', 300.00, 8.00, '2024-05-31', 150.00),
('picles', 'Molhos', 1000.00, 18.00, '2024-06-07', 500.00),
('molho', 'Molhos', 1500.00, 10.00, '2024-06-14', 750.00),
('maionese', 'Molhos', 2000.00, 12.00, '2024-06-21', 1000.00),
('mostarda', 'Molhos', 1000.00, 15.00, '2024-06-28', 500.00),
('ketchup', 'Molhos', 1500.00, 11.00, '2024-07-05', 750.00);

"""

"""
INSERT INTO Receita (id_lanche, id_ingrediente, quantidade_ingrediente) VALUES
-- Hot-Dog
(1, 1, 1),  -- 1 pão
(1, 2, 1),  -- 1 salsicha
(1, 13, 1), -- 1 molho
(1, 12, 5), -- 5 picles
(1, 17, 1), -- 1 ketchup

-- X-burguer
(2, 1, 1),  -- 1 pão
(2, 16, 1),  -- 1 hambúrguer
(2, 3, 1),  -- 1 queijo
(2, 4, 2),  -- 2 alface
(2, 5, 2),  -- 2 tomate
(2, 11, 1), -- 1 cebola
(2, 14, 1), -- 1 maionese
(2, 17, 1), -- 1 ketchup

-- X-salada
(3, 1, 1),  -- 1 pão
(3, 2, 1),  -- 1 salsicha
(3, 3, 1),  -- 1 queijo
(3, 4, 3),  -- 3 alface
(3, 5, 3),  -- 3 tomate
(3, 11, 1), -- 1 cebola
(3, 12, 5), -- 5 picles
(3, 14, 1), -- 1 maionese
(3, 15, 1), -- 1 mostarda
(3, 17, 1), -- 1 ketchup


-- Misto-quente
(4, 1, 1),  -- 1 pão
(4, 2, 1),  -- 1 salsicha
(4, 3, 1),  -- 1 queijo

-- Bauru
(5, 1, 2),  -- 2 pães
(5, 2, 1),  -- 1 salsicha
(5, 3, 1),  -- 1 queijo
(5, 11, 1), -- 1 cebola

-- X-egg
(6, 1, 1),  -- 1 pão
(6, 2, 1),  -- 1 salsicha
(6, 3, 1),  -- 1 queijo
(6, 6, 1),  -- 1 ovo

-- X-milho
(7, 1, 1),  -- 1 pão
(7, 2, 1),  -- 1 salsicha
(7, 3, 1),  -- 1 queijo
(7, 7, 50), -- 50g milho

-- X-calabresa
(8, 1, 1),  -- 1 pão
(8, 8, 100), -- 100g calabresa

-- X-bacon
(9, 1, 1),  -- 1 pão
(9, 2, 1),  -- 1 salsicha
(9, 9, 50), -- 50g bacon

-- X-frango
(10, 1, 1),  -- 1 pão
(10, 10, 100); -- 100g frango

"""


"""
SELECT 
    p.id_pedido, 
    l.nome AS lanche, 
    p.quantidade, 
    p.data_pedido,
    p.id_lanche  -- Specify that id_lanche comes from the Pedidos table
FROM Pedidos p
JOIN Lanches l ON p.id_lanche = l.id_lanche;

"""