import sqlite3

# Nome do arquivo do banco de dados SQLite
DB_NAME = "escola.db"  # será criado automaticamente se não existir

def conectar():
    """Conecta (ou cria) o banco de dados SQLite."""
    return sqlite3.connect(DB_NAME)


def criar_banco():
    """Cria o arquivo do banco de dados (caso não exista)."""
    conn = conectar()
    conn.close()  # apenas garante a criação do arquivo


def criar_tabelas():
    """Cria as tabelas (cursos, turmas, alunos) se não existirem."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turmas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            curso_id INTEGER,
            FOREIGN KEY (curso_id) REFERENCES cursos(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turma_id INTEGER,
            FOREIGN KEY (turma_id) REFERENCES turmas(id)
        )
    """)

    conn.commit()
    conn.close()


# Exemplo de uso:
if __name__ == "__main__":
    criar_banco()
    criar_tabelas()
    print("Banco de dados e tabelas criados com sucesso!")
