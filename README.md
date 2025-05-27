### PI05 - Pumpkim Intelligence

O projeto "Pumpkim Intelligence", válido pelo Projeto Integrador 5 do curso de Big Data para Negócios, tem como objetivo realizar a Gestão de Estoque dos produtos comercializados pela empresa Pumpkim Saudável, um restaurante com a temática de comida saudável e produtos naturais.


Para usar este processo, basta fazer o seguinte:

##### Banco de Dados

1 - Criará um banco de dados postgresql;
2 - Executará os comandos SQL que estão na pasta scr/SQL Statements, sendo a ordem de tabelas e depois index;


##### Stage

1 - Instalar as bibliotecas necessárias com pip install:
Streamlit, segno, streamlit_router, psycopg2, dotenv;
2 - na pasta stage/code, criará um arquivo .env com as informações de conexão com o seu banco de dados criado (será chamado no login.py).
3 - Dentro do terminal da pasta stage/code, execute o comando "py -m streamlit run main.py" (Desconsidere as aspas);


_Obs: O projeto está sendo desenvolvido e se encontra em fase de testes_