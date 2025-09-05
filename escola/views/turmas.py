import tkinter as tk                      # Importa o módulo base do Tkinter (widgets clássicos e gerenciamento de janelas)
from tkinter import ttk                   # Importa ttk (conjunto de widgets com temas/estilo moderno)
from models.models import Turma, Curso, Aluno  # Importa as classes do modelo (acesso a dados/regras de negócio)


class TurmasView(tk.Frame):               # Define a view de Turmas como um Frame do Tkinter
    def __init__(self, master, voltar_callback):
        super().__init__(master, bg="#fffbe6")   # Inicializa o Frame com cor de fundo
        self.pack(fill="both", expand=True)      # Posiciona o Frame ocupando toda a área disponível
        self.voltar_callback = voltar_callback   # Função de retorno para a tela anterior/menus
        self.sel_id = None                       # Armazena o ID da turma atualmente selecionada (ou None)

        # Título da tela
        tk.Label(self, text="Turmas", font=("Arial", 18, "bold"), bg="#fffbe6").pack(pady=10)  # Label de cabeçalho

        # Container principal que abriga as duas colunas (CRUD à esquerda e painel de alunos à direita)
        cont = tk.Frame(self, bg="#fffbe6"); cont.pack(fill="both", expand=True, padx=10, pady=8)  # Frame container

        # CRUD
        crud = tk.Frame(cont, bg="#fffbe6"); crud.pack(side=tk.LEFT, fill="both", expand=True, padx=10)  # Coluna esquerda
        tk.Label(crud, text="Nome:", bg="#fffbe6").pack(anchor="w")                                      # Rótulo do campo Nome
        self.ent_nome = tk.Entry(crud, width=30); self.ent_nome.pack(pady=4, fill="x")                   # Campo de entrada do nome

        tk.Label(crud, text="Curso:", bg="#fffbe6").pack(anchor="w")                                      # Rótulo do combobox de Curso
        self.cb_cursos = ttk.Combobox(crud, state="readonly"); self.cb_cursos.pack(pady=4, fill="x")     # Combobox de cursos (somente leitura)

        self.lista = tk.Listbox(crud, width=42, height=12); self.lista.pack(pady=8, fill="both", expand=True)  # Lista de turmas
        self.lista.bind("<<ListboxSelect>>", self.on_select)                                                   # Evento ao selecionar item

        box = tk.Frame(crud, bg="#fffbe6"); box.pack(pady=6)  # Frame para organizar os botões em grade
        tk.Button(box, text="Adicionar", width=12, command=self.adicionar).grid(row=0, column=0, padx=4)  # Botão Adicionar
        tk.Button(box, text="Atualizar", width=12, command=self.atualizar).grid(row=0, column=1, padx=4)  # Botão Atualizar
        tk.Button(box, text="Deletar",   width=12, command=self.deletar).grid(row=0, column=2, padx=4)    # Botão Deletar
        tk.Button(box, text="Voltar",    width=12, command=self.voltar).grid(row=0, column=3, padx=4)     # Botão Voltar

        # Alunos por Turma
        painel = tk.Frame(cont, bg="#fffbe6"); painel.pack(side=tk.RIGHT, fill="both", expand=True, padx=10)  # Coluna direita
        tk.Label(painel, text="Alunos da Turma", font=("Arial", 14), bg="#fffbe6").pack(pady=6)               # Título do painel
        self.lista_alunos = tk.Listbox(painel, width=42, height=10); self.lista_alunos.pack(pady=4, fill="both", expand=True)  # Lista de alunos ligados à turma

        tk.Label(painel, text="Associar Aluno:", bg="#fffbe6").pack(anchor="w")             # Rótulo do combobox de alunos
        self.cb_alunos = ttk.Combobox(painel, state="readonly"); self.cb_alunos.pack(pady=4, fill="x")  # Combobox para escolher aluno
        tk.Button(painel, text="Associar", command=self.associar).pack(pady=6)              # Botão para associar aluno selecionado à turma

        self.carregar_cursos()          # Preenche o combobox de cursos
        self.carregar_alunos_combo()    # Preenche o combobox de alunos
        self.carregar()                 # Carrega/atualiza a lista de turmas e reseta campos

    # --- helpers de carga ---
    def carregar_cursos(self):
        self.cb_cursos['values'] = [f"{c[0]} - {c[1]}" for c in Curso.listar()]  # Monta lista "id - nome" de cursos

    def carregar_alunos_combo(self):
        self.cb_alunos['values'] = [f"{a[0]} - {a[1]}" for a in Aluno.listar()]  # Monta lista "id - nome" de alunos

    def carregar(self):
        self.lista.delete(0, tk.END)                                 # Limpa a Listbox de turmas
        for t in Turma.listar():                                     # Itera sobre as turmas vindas do modelo
            self.lista.insert(tk.END, f"{t[0]} - {t[1]} (Curso: {t[2]})")  # Insere "id - nome (Curso: nomeCurso)"
        self.sel_id = None                                           # Limpa seleção atual
        self.ent_nome.delete(0, tk.END)                              # Limpa campo de nome
        self.cb_cursos.set("")                                       # Limpa seleção do combobox de curso
        self.lista_alunos.delete(0, tk.END)                          # Limpa a lista de alunos da turma

    # --- CRUD ---
    def on_select(self, _):
        s = self.lista.curselection()             # Obtém tupla de índices selecionados na Listbox
        if not s: return                           # Se nada selecionado, sai
        turma = Turma.listar()[s[0]]              # Recupera os dados da turma correspondente ao índice
        self.sel_id = turma[0]                    # Salva o ID da turma selecionada
        self.ent_nome.delete(0, tk.END); self.ent_nome.insert(0, turma[1])  # Preenche o campo Nome com o valor atual

        curso_nome = turma[2] or ""               # Nome do curso associado (pode ser None → substitui por "")
        for i, v in enumerate(self.cb_cursos['values']):         # Percorre os valores do combobox de cursos
            if v.split(" - ", 1)[1] == curso_nome:               # Compara a parte do nome (depois do " - ")
                self.cb_cursos.current(i); break                 # Seleciona o curso correspondente e interrompe

        self.listar_alunos_turma()                # Atualiza a lista de alunos pertencentes à turma selecionada

    def adicionar(self):
        nome = self.ent_nome.get().strip()        # Lê o nome digitado (sem espaços extras nas extremidades)
        curso_sel = self.cb_cursos.get()          # Lê a string selecionada no combobox (ex.: "3 - Informática")
        if nome and curso_sel:                    # Valida se há nome e curso escolhido
            curso_id = int(curso_sel.split(" - ")[0])  # Extrai o ID numérico do curso (antes do " - ")
            Turma.adicionar(nome, curso_id)            # Chama o modelo para inserir a nova turma
            self.carregar()                             # Recarrega a interface (lista/limpeza de campos)

    def atualizar(self):
        if self.sel_id:                           # Só atualiza se houver turma selecionada
            nome = self.ent_nome.get().strip()    # Lê o nome atualizado
            curso_sel = self.cb_cursos.get()      # Lê o curso selecionado
            if nome and curso_sel:                # Validação simples
                curso_id = int(curso_sel.split(" - ")[0])  # Extrai ID do curso
                Turma.atualizar(self.sel_id, nome, curso_id)  # Atualiza no modelo
                self.carregar()                                # Recarrega a interface

    def deletar(self):
        if self.sel_id:                           # Só deleta se houver turma selecionada
            Turma.deletar(self.sel_id)            # Solicita a exclusão pelo ID
            self.carregar()                       # Recarrega a interface após deletar

    # --- alunos por turma ---
    def listar_alunos_turma(self):
        self.lista_alunos.delete(0, tk.END)       # Limpa lista de alunos
        if not self.sel_id: return                # Se não há turma selecionada, sai
        for a in Turma.listar_alunos(self.sel_id):                      # Obtém alunos associados à turma
            self.lista_alunos.insert(tk.END, f"{a[0]} - {a[1]}")        # Insere "id - nome" de cada aluno

    def associar(self):
        if self.sel_id:                           # Só associa se houver turma selecionada
            aluno_sel = self.cb_alunos.get()      # Lê o aluno selecionado (ex.: "5 - Maria")
            if aluno_sel:
                aluno_id = int(aluno_sel.split(" - ")[0])  # Extrai o ID do aluno
                # pegar o nome atual do aluno
                nome = None                                        # Variável para armazenar o nome encontrado
                for a in Aluno.listar():                           # Percorre todos os alunos (do modelo)
                    if a[0] == aluno_id:                           # Se o ID bate
                        nome = a[1]; break                          # Guarda o nome e interrompe
                if nome is not None:                               # Se encontrou o aluno
                    Aluno.atualizar(aluno_id, nome, self.sel_id)   # Atualiza o aluno associando-o à turma atual
                    self.listar_alunos_turma()                     # Atualiza a lista de alunos da turma
                    self.carregar_alunos_combo()                   # Recarrega o combobox (se necessário refletir mudanças)

    def voltar(self):
        self.destroy()                              # Destroi/fecha este Frame (tela atual)
        self.voltar_callback()                      # Chama a função que retorna à tela anterior/menu
