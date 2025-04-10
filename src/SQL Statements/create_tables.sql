-- Tabela: Funcionario
DROP TABLE IF EXISTS tb_funcionario;
CREATE TABLE tb_funcionario (
    id_funcionario SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cpf CHAR(11) NOT NULL,
    data_Nascimento DATE NOT NULL,
    numero_telefone CHAR(11) NOT NULL,
    endereco VARCHAR(150) NOT NULL,
    sexo CHAR(1) NOT NULL,
    cargo VARCHAR(20) NOT NULL

);
 
-- Tabela: Cliente
DROP TABLE IF EXISTS tb_cliente;
CREATE TABLE tb_cliente (
    codigo_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    email VARCHAR(40) NOT NULL,
    cpf CHAR(11) NOT NULL,
    data_nascimento DATE NOT NULL,
    numero_telefone CHAR(11) NOT NULL,
    senha VARCHAR NOT NULL,
    sexo CHAR(1) NOT NULL
);
 
-- Tabela: Pedido
DROP TABLE IF EXISTS tb_pedido;
CREATE TABLE tb_pedido (
    codigo_de_pedido SERIAL PRIMARY KEY,
    codigo_cliente SMALLINT NOT NULL,
    data_realizacao DATE NOT NULL,
    FOREIGN KEY (codigo_cliente) REFERENCES tb_cliente(codigo_cliente)
);
 
-- Tabela: Movimento
DROP TABLE IF EXISTS tb_movimentacao;
CREATE TABLE tb_movimentacao (
    codigo_movimentacao SERIAL PRIMARY KEY,
    id_funcionario SMALLINT NOT NULL,
    codigo_de_pedido INTEGER NOT NULL,
    codigo_cliente SMALLINT NOT NULL,
    data_hora DATE NOT NULL,
	
    FOREIGN KEY (id_funcionario) REFERENCES tb_funcionario(id_funcionario),
    FOREIGN KEY (codigo_de_pedido) REFERENCES tb_pedido(codigo_de_pedido),
    FOREIGN KEY (codigo_cliente) REFERENCES tb_cliente(codigo_cliente)
);
 
-- Tabela: Produto
DROP TABLE IF EXISTS tb_produto;
CREATE TABLE tb_produto (
    codigo_do_produto SERIAL PRIMARY KEY,
    nome_produto VARCHAR(20) NOT NULL,
    categoria VARCHAR(15) NOT NULL
);
 
-- Tabela: Item
DROP TABLE IF EXISTS tb_item;
CREATE TABLE tb_item (
    codigo_item_produto SERIAL PRIMARY KEY,
    codigo_de_pedido INTEGER NOT NULL,
    codigo_do_produto SMALLINT NOT NULL,
    codigo_cliente SMALLINT NOT NULL,
    quantidade SMALLINT NOT NULL,

    FOREIGN KEY (codigo_de_pedido) REFERENCES tb_pedido(codigo_de_pedido),
    FOREIGN KEY (codigo_do_produto) REFERENCES tb_produto(codigo_do_produto),
    FOREIGN KEY (codigo_cliente) REFERENCES tb_cliente(codigo_cliente)
);
 
-- Tabela: Ingrediente
DROP TABLE IF EXISTS tb_ingrediente;
CREATE TABLE tb_ingrediente (
    codigo_de_ingrediente SERIAL PRIMARY KEY,
    nome_ingrediente VARCHAR NOT NULL
);
 
-- Tabela: Ingredientes de Produtos
DROP TABLE IF EXISTS tb_ingredientes_de_produtos;
CREATE TABLE tb_ingredientes_de_produtos (
    codigo_ingrediente_produto SERIAL PRIMARY KEY,
    codigo_do_produto SMALLINT NOT NULL,
    codigo_de_ingrediente SMALLINT NOT NULL,

    FOREIGN KEY (codigo_do_produto) REFERENCES tb_produto(codigo_do_produto),
    FOREIGN KEY (codigo_de_ingrediente) REFERENCES tb_ingrediente(codigo_de_ingrediente)
);