import sqlite3 #bliblioteca nativa do Python para BD

DB_NAME = "escola.db" #nome do banco de dados

def conectar():
    #abre e retorna uma conexão em SQLite3 com o banco
    return sqlite3.connect(DB_NAME)

def criar_tabelas():
    #cria as tabelas (curso, turma, aluno) 
    # se não existirem do BD
    con = conectar() # abre a conexão com o banco
    cur = con.cursor() # cria um cursor que aponta pro BD e executa intruções SQL
    
    cur.execute(""" 
                    CREATE TABLE IF NOT EXISTS cursos(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL
                    )
                 """)

    cur.execute(""" 
                    CREATE TABLE IF NOT EXISTS turmas(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        curso_id INTEGER,
                        FOREIGN KEY(curso_id) REFERENCES cursos(id)
                    )
                 """)
    
    cur.execute(""" 
                    CREATE TABLE IF NOT EXISTS alunos(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        turma_id INTEGER,
                        FOREIGN KEY(turma_id) REFERENCES turmas(id)
                    )
                 """)
    
    con.commit() #salva(confirmar) as alterações no banco
    con.close() #fechar a conexão com o banco