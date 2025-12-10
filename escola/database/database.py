import mysql.connector

#Dados do servidor MySQL
HOST = "localhost"
USER = "root"
PASSWORD = "980507@Rick"
DB_NAME = "escola_db" #nome do banco de dados

def conectar(usando_banco=True):
    """Conectar ao Mysql 
    -usando_banco=True -> conectar direto ao schema DB_NAME
    -usando_banco=False -> conectar sem definir um banco"""
    if usando_banco:
        return mysql.connector.connect(
            host = HOST,
            user = USER,
            port = "3306",
            password = PASSWORD,
            database = DB_NAME
        )
    else:
        return mysql.connector.connect(
            host = HOST,
            user = USER,
            port="3306",
            password = PASSWORD
        ) 

def criar_banco():
    #Criar banco caso não exista
    conn = conectar(usando_banco=False) #Cria uma instância de conexão com o banco
    cursor = conn.cursor() # Aponta para o Banco de Dadosa
    cursor.execute(""" CREATE DATABASE 
                   IF NOT EXISTS {DB_NAME}""")
    conn.commit() # salva as alterações no banco
    conn.close() # fecha a conexão com o banco


def criar_tabelas():
    #cria as tabelas (curso, turma, aluno) 
    # se não existirem do BD
    conn = conectar() # abre a conexão com o banco
    cursor = conn.cursor() # cria um cursor que aponta pro BD e executa intruções SQL
    
    cursor.execute(""" 
                    CREATE TABLE IF NOT EXISTS cursos(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        nome VARCHAR(100) NOT NULL
                    )
                 """)

    cursor.execute(""" 
                    CREATE TABLE IF NOT EXISTS turmas(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        nome VARCHAR(100) NOT NULL,
                        curso_id INT,
                        FOREIGN KEY(curso_id) REFERENCES cursos(id)
                    )
                 """)
    
    cursor.execute(""" 
                    CREATE TABLE IF NOT EXISTS alunos(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        nome VARCHAR(100) NOT NULL,
                        turma_id INT,
                        FOREIGN KEY(turma_id) REFERENCES turmas(id)
                    )
                 """)
    
    conn.commit() #salva(confirmar) as alterações no banco
    conn.close() #fechar a conexão com o banco