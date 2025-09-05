# Responsável por criar a janela raiz, configurar layout e navegar
# entre as telas (views) de Cursos, Alunos e Turmas.


import tkinter as tk                    # Importa o Tkinter básico
from tkinter import ttk                 # Importa widgets temáticos (ttk)
from database.database import criar_tabelas  # Função para garantir as tabelas
from views.cursos import CursosView     # View de gerenciamento de Cursos
from views.alunos import AlunosView     # View de gerenciamento de Alunos
from views.turmas import TurmasView     # View de gerenciamento de Turmas




class App(tk.Tk):
    """Janela principal da aplicação."""
    def __init__(self):
        super().__init__()                                  # Inicializa tk.Tk
        self.title("EduTec - Sistema Escolar")              # Título da janela
        self.geometry("600x460")                            # Tamanho padrão
        self.configure(bg="#e0f7fa")                        # Cor de fundo


        criar_tabelas()                                     # Garante as tabelas do BD
        self.menu()                                         # Exibe o menu principal


    def limpar(self):
        """Remove todos os widgets atuais da janela para trocar de tela."""
        for w in self.winfo_children():
            w.destroy()


    def menu(self):
        """Desenha o menu principal com botões de navegação."""
        self.limpar()
        tk.Label(self, text="🏫 Menu Principal", font=("Arial", 18, "bold"),
                 bg="#e0f7fa").pack(pady=20)


        ttk.Button(self, text="Gerenciar Cursos",
                   command=self.abrir_cursos).pack(pady=10, ipadx=10, ipady=5)
        ttk.Button(self, text="Gerenciar Alunos",
                   command=self.abrir_alunos).pack(pady=10, ipadx=10, ipady=5)
        ttk.Button(self, text="Gerenciar Turmas",
                   command=self.abrir_turmas).pack(pady=10, ipadx=10, ipady=5)
        ttk.Button(self, text="Sair",
                   command=self.destroy).pack(pady=20, ipadx=10, ipady=5)


    def abrir_cursos(self):
        """Navega para a tela de Cursos."""
        self.limpar()
        CursosView(self, self.menu)


    def abrir_alunos(self):
        """Navega para a tela de Alunos."""
        self.limpar()
        AlunosView(self, self.menu)


    def abrir_turmas(self):
        """Navega para a tela de Turmas."""
        self.limpar()
        TurmasView(self, self.menu)




if __name__ == "__main__":
    App().mainloop()                      # Inicia o loop de eventos do Tkinter
