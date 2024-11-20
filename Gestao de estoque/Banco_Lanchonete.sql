CREATE DATABASE Banco_Lanchonete;

USE Banco_Lanchonete;

CREATE TABLE Ingredientes (
	id_ingrediente INT AUTO_INCREMENT PRIMARY KEY,
	nome varchar(20) NOT NULL,
	categoria varchar(20),
	quantidade REAL,
	preco_quilo REAL NOT NULL,
	data_recebimento DATE NOT NULL,
	quantidade_minima REAL NOT NULL
);

CREATE TABLE Lanches (
    id_lanche INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) UNIQUE  
);

CREATE TABLE Receita (
	id_lanche INTEGER,
	id_ingrediente INTEGER,
	quantidade_ingrediente REAL,	
	FOREIGN KEY (id_lanche) REFERENCES Lanches(id_lanche),
	FOREIGN KEY (id_ingrediente) REFERENCES Ingredientes(id_ingrediente)  
);

CREATE TABLE Pedidos (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_lanche INT,
    quantidade INT NOT NULL,
    data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (id_lanche) REFERENCES Lanches(id_lanche)
);

