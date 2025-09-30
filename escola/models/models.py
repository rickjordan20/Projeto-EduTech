from database.database import conectar

#MODELO DE CRUD PARA CURSO
class Curso:
    def listar():
        #Listar todos os cursos em um lista
        con = conectar()
        cur = con.cursor()

        cur.execute(" SELECT id,nome FROM cursos ORDER BY id ") #intrução sql
        #busca os dados da tabela curso

        rows = cur.fetchall() #retorna todos os dados da consulta SQL acima
        con.close()

        return rows
    
    def adicionar(nome:str):
        #insere um novo curso com o nome informado
        con = conectar()
        cur = con.cursor()

        cur.execute("INSERT INTO cursos(nome) VALUES(%s)",(nome,))
        # "%s" é um placeholder que protege SQL Injection e formata os dados

        con.commit()
        con.close()
    
    def atualizar(id_:int, nome: str):
        #atualiza o nome do curso com base no id
        con = conectar()
        cur = con.cursor()

        cur.execute("UPDATE cursos SET nome=%s WHERE id=%s",(nome,id_))

        con.commit()
        con.close()

    def deletar(id_:int):
        #remove um curso com base no id informado
        con = conectar()
        cur = con.cursor()

        cur.execute("DELET FROM cursos WHERE id=%s",(id_,))

        con.commit()
        con.close()

#MODELO DE CRUD PARA TURMA
class Turma:
    #representa a entidade Turma que pertence a um Curso
    def listar():
        #Listar todos os cursos em um lista
        con = conectar()
        cur = con.cursor()

        cur.execute(""" SELECT t.id, t.nome, COALESCE(c.nome,'') AS curso
                        FROM turmas t
                        LEFT JOIN cursos c ON c.id = t.id """) #instrução sql
        #busca os dados da tabela curso

        rows = cur.fetchall() #retorna todos os dados da consulta SQL acima
        con.close()

        return rows
    
    def adicionar(nome:str, curso_id:int | None):
        #insere um novo curso com o nome informado
        con = conectar()
        cur = con.cursor()

        cur.execute("INSERT INTO turmas(nome,curso_id) VALUES(%s,%s)",(nome,curso_id))
        # "%s" é um placeholder que protege SQL Injection e formata os dados

        con.commit()
        con.close()
    
    def atualizar(id_:int, nome: str, curso_id:int | None):
        #atualiza o nome do curso com base no id
        con = conectar()
        cur = con.cursor()

        cur.execute("UPDATE turmas SET nome=%s,curso_id=%s WHERE id=%s",(nome,curso_id,id_))

        con.commit()
        con.close()

    def deletar(id_:int):
        #remove um curso com base no id informado
        con = conectar()
        cur = con.cursor()

        cur.execute("DELET FROM turmas WHERE id=%s",(id_,))

        con.commit()
        con.close()

    def listar_alunos(turma_id):
        con = conectar()
        cur = con.cursor()
        
        cur.execute("SELECT id, nome FROM alunos WHERE turma_id=%s",(turma_id,))
        dados = cur.fetchall() # retorna o resultado da consulta no banco
        con.close() # fecha a conxao com o banco
        return dados
    
class Aluno:
    @staticmethod
    def listar():
        con = conectar()
        cur = con.cursor()
    
        cur.execute(
                    """SELECT a.id, a.nome, t.nome
                    FROM alunos a
                    LEFT JOIN turmas t ON a.turma_id = t.id
                    """)
        dados = cur.fetchall()
        con.close()
        return dados 
    
    @staticmethod
    def adicionar(nome, turma_id = None):
        con = conectar()
        cur = con.cursor()
    
        cur.execute(
                    "INSERT INTO alunos(nome,turma_id) VALUES(%s,%s)",(nome,turma_id))
        con.commit() #salva as alteracoes no banco
        con.close() #fecha a conexao com o banco
    
    @staticmethod
    def atualizar(id_,nome,turma_id=None):
        con = conectar()
        cur = con.cursor()
    
        cur.execute(
                    "UPDATE alunos SET nome=%s, turma_id=%s WHERE id=%s",(nome,turma_id,id_))
        con.commit() #salva as alteracoes no banco
        con.close() #fecha a conexao com o banco

    @staticmethod
    def deletar(id_):
        con = conectar()
        cur = con.cursor()
    
        cur.execute(
                    "DELETE FROM alunos WHERE id=%s",(id_,))
        con.commit() #salva as alteracoes no banco
        con.close() #fecha a conexao com o banco
