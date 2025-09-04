import tkinter as tk                      # Importa o módulo principal do Tkinter para interfaces gráficas
from tkinter import ttk                   # Importa ttk (widgets mais modernos do Tkinter)
from models.models import Aluno, Turma     # Importa as classes Aluno e Turma do módulo models


# Classe responsável pela tela de gerenciamento de Alunos
class AlunosView(tk.Frame):
    def __init__(self, master, voltar_callback):
        # Inicializa a classe pai (Frame) com cor de fundo personalizada
        super().__init__(master, bg="#f0f8ff")
        self.pack(fill="both", expand=True)        # Expande o frame para ocupar toda a janela
        self.voltar_callback = voltar_callback    # Função de callback para retornar ao menu principal
        self.sel_id = None                        # Armazena o ID do aluno selecionado na lista


        # Título da tela
        tk.Label(self, text="Alunos", font=("Arial", 18, "bold"), bg="#f0f8ff").pack(pady=10)


        # Lista para exibir os alunos cadastrados
        self.lista = tk.Listbox(self, width=54, height=12)
        self.lista.pack(pady=6)
        self.lista.bind("<<ListboxSelect>>", self.on_select)  # Evento de seleção na lista (pega o clique)


        # Formulário para entrada de dados
        form = tk.Frame(self,bg="#f0f8ff").pack(pady=6)

        #Campos de entrada para o nome aluno
        tk.Label(form, text="Nome", bg="#f0f8ff").grid(row=0,column=0)
        self.ent_nome = tk.Entry(form,width=42)

        #Campos de seleção de turma (combobox)
        tk.Label(form, text="Turma", bg="#f0f8ff").grid(row=0,column=0)
        self.cb_turmas = ttk.Combobox(form, width=42).grid(row=3, column=0, pady=4)

        # Botões de ação
        box = tk.Frame(self, bg="#f0f8ff").pack(pady=8)
        tk.Button(box, text="Adicionar", width=12, command=self.adicionar).grid(row=0,column=0,pady=4)
        tk.Button(box, text="Atualizar", width=12, command=self.atualizar).grid(row=0,column=1,pady=4)
        tk.Button(box, text="Deletar", width=12, command=self.deletar).grid(row=0,column=2,pady=4)
        tk.Button(box, text="Voltar", width=12, command=self.voltar).grid(row=0,column=3,pady=4)

        # Carrega os dados inicias (turmas e alunos)
        self.carregar_turmas()
        self.carregar()

    def carregar_turmas(self):
        #carrega as turmas em um combobox
        self.cb_turmas['values'] = [f"{t[0]} - {t[1]}" for t in Turma.listar()]
    
    def carregar(self):
        #carrega os alunos na lista
        self.lista.delete(0,tk.END) #Limpa a lista
        for a in Aluno.listar():
            self.lista.insert(tk.END, f"{a[0]} - {a[1]} | Turma: {a[2]}")
        self.sel_id = None
        self.ent_nome.delete(0,tk.END) #limpa o campo
        self.cb_turmas.set("")

    def on_select(self, _):
        #evento de seleção na lista de alunos
        s = self.lista.curselection() # Pega o indice selecionado
        if not s: return 
        aluno = Aluno.listar()[s[0]]
        self.sel_id = aluno[0]
        self.ent_nome.delete(0,tk.END) # limpa o campo nome
        self.ent_nome.insert(0,aluno[1]) #preenche o campo nome
        turma_nome = aluno[2] or "" #Nome da turma associada
        #Marca a turma correpondente ao combobox
        for i, v in enumerate(self.cb_turmas['values']):
            if v.split(" - ",1)[1]  == turma_nome:
                self.cb_turmas.currrent(i)
                break
        
    def adicionar(self):
        #adiciona um novo aluno
        nome = self.ent_nome.get().strip() # Captura o nome digitado
        turma_sel = self.cb_turmas.get() # Captura a turma selecionada 
        turma_id = int(turma_id.split("-")[0] if turma_sel else None) #pega o id da turma
        
        if nome: #so adiciona se o nome não estiver vazio
            Aluno.adicionar(nome,turma_id)
            self.carregar()
    
    def atualizar(self):
        if self.sel_id:   #só atualiza se um aluno estiver selecionado
            nome = self.ent_nome.get().strip() #captura o nome digitado
            turma_sel = self.cb_turmas.get() #captura a turma selecionada
            turma_id = int(turma_id.split("-")[0] if turma_sel else None)
            Aluno.atualizar(self,nome,turma_id)
            self.carregar()
    
    def deletar(self):
        #Deleta um aluno
        if self.sel_id: #Só deleta se houver aluno selecionado
            Aluno.deletar(self.sel_id)
            self.carregar()
    
    def voltar(self):
        #volta para a tela anterior
        self.destroy()  #Destroi a tela atual
        self.voltar_callback() #executa a função retorno


        




        

        
   
