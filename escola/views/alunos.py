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
        self.lista.bind("<<ListboxSelect>>", self.on_select)  # Evento de seleção na lista


        # Formulário para entrada de dados
        form = tk.Frame(self, bg="#f0f8ff"); form.pack(pady=6)


        # Campo de entrada para o nome do aluno
        tk.Label(form, text="Nome:", bg="#f0f8ff").grid(row=0, column=0, sticky="w")
        self.ent_nome = tk.Entry(form, width=42); self.ent_nome.grid(row=1, column=0, pady=4)


        # Campo de seleção de turmas (combobox)
        tk.Label(form, text="Turma:", bg="#f0f8ff").grid(row=2, column=0, sticky="w")
        self.cb_turmas = ttk.Combobox(form, state="readonly", width=40); self.cb_turmas.grid(row=3, column=0, pady=4)


        # Botões de ação
        box = tk.Frame(self, bg="#f0f8ff"); box.pack(pady=8)
        tk.Button(box, text="Adicionar", width=12, command=self.adicionar).grid(row=0, column=0, padx=4)
        tk.Button(box, text="Atualizar", width=12, command=self.atualizar).grid(row=0, column=1, padx=4)
        tk.Button(box, text="Deletar",   width=12, command=self.deletar).grid(row=0, column=2, padx=4)
        tk.Button(box, text="Voltar",    width=12, command=self.voltar).grid(row=0, column=3, padx=4)


        # Carrega os dados iniciais (turmas e alunos)
        self.carregar_turmas()
        self.carregar()


    # Carrega as turmas no combobox
    def carregar_turmas(self):
        self.cb_turmas['values'] = [f"{t[0]} - {t[1]}" for t in Turma.listar()]


    # Carrega os alunos na lista
    def carregar(self):
        self.lista.delete(0, tk.END)  # Limpa a lista
        for a in Aluno.listar():      # Adiciona cada aluno encontrado
            self.lista.insert(tk.END, f"{a[0]} - {a[1]} | Turma: {a[2]}")
        # Reseta os campos após atualização
        self.sel_id = None
        self.ent_nome.delete(0, tk.END)
        self.cb_turmas.set("")


    # Evento de seleção na lista de alunos
    def on_select(self, _):
        s = self.lista.curselection()   # Pega o índice selecionado
        if not s: return                # Se nada foi selecionado, não faz nada
        aluno = Aluno.listar()[s[0]]    # Recupera o aluno correspondente
        self.sel_id = aluno[0]          # Salva o ID do aluno
        self.ent_nome.delete(0, tk.END); self.ent_nome.insert(0, aluno[1])  # Preenche o campo nome
        turma_nome = aluno[2] or ""     # Nome da turma associada
        # Marca a turma correspondente no combobox
        for i, v in enumerate(self.cb_turmas['values']):
            if v.split(" - ", 1)[1] == turma_nome:
                self.cb_turmas.current(i); break


    # Adiciona um novo aluno
    def adicionar(self):
        nome = self.ent_nome.get().strip()  # Captura o nome digitado
        turma_sel = self.cb_turmas.get()    # Captura a turma selecionada
        turma_id = int(turma_sel.split(" - ")[0]) if turma_sel else None  # Extrai o ID da turma
        if nome:                            # Só adiciona se o nome não estiver vazio
            Aluno.adicionar(nome, turma_id)
            self.carregar()                 # Atualiza a lista


    # Atualiza os dados de um aluno existente
    def atualizar(self):
        if self.sel_id:                     # Só atualiza se um aluno estiver selecionado
            nome = self.ent_nome.get().strip()
            turma_sel = self.cb_turmas.get()
            turma_id = int(turma_sel.split(" - ")[0]) if turma_sel else None
            Aluno.atualizar(self.sel_id, nome, turma_id)
            self.carregar()


    # Deleta um aluno
    def deletar(self):
        if self.sel_id:                     # Só deleta se houver aluno selecionado
            Aluno.deletar(self.sel_id)
            self.carregar()


    # Volta para a tela anterior
    def voltar(self):
        self.destroy()            # Destroi a tela atual
        self.voltar_callback()    # Executa a função de retorno


