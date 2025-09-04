import tkinter as tk
from models.models import Curso

class CursosView(tk.Frame):
    def __init__(self, master, voltar_callback):
        # Inicializa a classe pai (Frame) com cor de fundo personalizada
        super().__init__(master, bg="#f0f8ff")
        self.pack(fill="both", expand=True)        # Expande o frame para ocupar toda a janela
        self.voltar_callback = voltar_callback    # Função de callback para retornar ao menu principal
        self.sel_id = None                        # Armazena o ID do aluno selecionado na lista


        # Título da tela
        tk.Label(self, text="Cursos", font=("Arial", 18, "bold"), bg="#f0f8ff").pack(pady=10)

        #Lista os cursos cadastrados
        self.lista = tk.Listbox(self,width=48,height=12)
        self.lista.pack(pady=6)
        #Evento de seleceção de intens da lista do curso
        self.lista.bind("<<ListboxSelect>>",self.on_select)

        #Campo de entrada para o nome o curso
        tk.Label(self, text="Nome: ",bg="#f0f8ff").pack()
        self.ent_nome = tk.Entry(self, width=40)
        self.ent_nome.pack(pady=4)

        # Botões de ação
        box = tk.Frame(self, bg="#e6ffe6").pack(pady=8)
        tk.Button(box, text="Adicionar", width=12, command=self.adicionar).grid(row=0,column=0,pady=4)
        tk.Button(box, text="Atualizar", width=12, command=self.atualizar).grid(row=0,column=1,pady=4)
        tk.Button(box, text="Deletar", width=12, command=self.deletar).grid(row=0,column=2,pady=4)
        tk.Button(box, text="Voltar", width=12, command=self.voltar).grid(row=0,column=3,pady=4)

        #Carrega os cursos ao iniciar a tela
        self.carregar()

    def carregar(self):
        #carrega os alunos na lista
        self.lista.delete(0,tk.END) #Limpa a lista
        for a in Curso.listar():
            self.lista.insert(tk.END, f"{a[0]} - {a[1]}")
        self.sel_id = None
        self.ent_nome.delete(0,tk.END) #limpa o campo

    def on_select(self,_):
        s = self.lista.curselection() # Obtem o indice selecionado
        if not s: return
        curso = Curso.listar()[s[0]]
        self.sel_id = curso[0]
        self.ent_nome.delete(0,tk.END) #limpa o campo nome
        self.ent_nome.insert(0,curso[1]) #preencher com o nome selecionado
    
    def adicionar(self):
        nome = self.ent_nome.get().strip() #Captura o nome digitado, remove os espaços

        if nome:
            Curso.adicionar(nome)
            self.carregar()
    
    def deletar(self):
        if self.sel_id:
            Curso.deletar(self.sel_id)
            self.carregar() 

    def atualizar(self):
        if self.sel_id:
            nome = self.ent_nome.get.strip()
            Curso.atualizar(self.sel_id,nome)
            self.carregar()
    
    def voltar(self):
        self.destroy()
        self.voltar_callback() #chama a função para retornar ao menu principal

        

        