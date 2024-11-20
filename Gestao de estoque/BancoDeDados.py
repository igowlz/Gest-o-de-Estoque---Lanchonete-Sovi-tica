import mysql.connector

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
            comando = "SELECT id_pedido, id_lanche, quantidade, data_pedido FROM Pedidos"
            try:
                self.cursor.execute(comando)
                pedidos = self.cursor.fetchall()
                return pedidos
            except mysql.connector.Error as err:
                print(f"Erro ao buscar pedidos: {err}")
                return None
        return None

    def adicionar_pedido(self, lanche, quantidade):
        if self.cursor:
            comando = "INSERT INTO Pedidos (id_lanche, quantidade, data_pedido) VALUES (%s, %s, NOW())"
            try:
                id_lanche = self.buscar_id_lanche(lanche)
                if id_lanche:
                    self.cursor.execute(comando, (id_lanche, quantidade))
                    self.conexao.commit()
                    print(f"Pedido de {lanche} realizado com sucesso!")
                else:
                    print(f"Lanche {lanche} não encontrado.")
            except mysql.connector.Error as err:
                print(f"Erro ao adicionar pedido: {err}")

    def buscar_id_lanche(self, nome_lanche):
        if self.cursor:
            comando = "SELECT id_lanche FROM Lanches WHERE nome = %s"
            try:
                self.cursor.execute(comando, (nome_lanche,))
                resultado = self.cursor.fetchone()
                return resultado['id_lanche'] if resultado else None # Access using key now
            except mysql.connector.Error as err:
                print(f"Erro ao buscar ID do lanche: {err}")
                return None
    def executar_comando(self, comando, params=None):
        if self.cursor:
            try:
                self.cursor.execute(comando, params)
                resultados = self.cursor.fetchall()
                return resultados
            except mysql.connector.Error as err:
                print(f"Erro ao executar comando: {err}")
                return None