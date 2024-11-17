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
            self.cursor = self.conexao.cursor()
            print("Conexão bem-sucedida!")
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao banco de dados: {err}")
            self.conexao = None
            self.cursor = None

    def buscar_ingredientes(self):
        if self.cursor:
            comando = "SELECT nome_ingrediente, quantidade FROM Ingredientes"
            try:
                self.cursor.execute(comando)
                ingredientes = self.cursor.fetchall()
                return ingredientes
            except mysql.connector.Error as err:
                print(f"Erro ao buscar ingredientes: {err}")
                return None
        return None

    def adicionar_ingrediente(self, nome_ingrediente, quantidade):
        if self.cursor:
            comando = "INSERT INTO Ingredientes (nome_ingrediente, quantidade) VALUES (%s, %s)"
            try:
                self.cursor.execute(comando, (nome_ingrediente, quantidade))
                self.conexao.commit()
                print(f"Ingresso do ingrediente {nome_ingrediente} realizado!")
            except mysql.connector.Error as err:
                print(f"Erro ao adicionar ingrediente: {err}")
