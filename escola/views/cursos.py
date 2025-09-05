import tkinter as tk                   # Importa o Tkinter para criação da interface gráfica
from models.models import Curso         # Importa a classe Curso do módulo models




# Classe responsável pela tela de gerenciamento de Cursos
class CursosView(tk.Frame):
    def __init__(self, master, voltar_callback):
        # Inicializa a classe pai (Frame) com cor de fundo personalizada
        super().__init__(master, bg="#e6ffe6")
        self.pack(fill="both", expand=True)        # Expande o frame para ocupar toda a área da janela
        self.voltar_callback = voltar_callback    # Função de callback para voltar ao menu principal
        self.sel_id = None                        # Armazena o ID do curso selecionado na lista


        # Título da tela
        tk.Label(self, text="Cursos", font=("Arial", 18, "bold"), bg="#e6ffe6").pack(pady=10)


        # Lista de cursos cadastrados
        self.lista = tk.Listbox(self, width=48, height=12)
        self.lista.pack(pady=6)
        self.lista.bind("<<ListboxSelect>>", self.on_select)  # Evento de seleção de item na lista


        # Campo de entrada para o nome do curso
        tk.Label(self, text="Nome:", bg="#e6ffe6").pack()
        self.ent_nome = tk.Entry(self, width=40)
        self.ent_nome.pack(pady=4)


        # Botões de ação
        box = tk.Frame(self, bg="#e6ffe6"); box.pack(pady=8)
        tk.Button(box, text="Adicionar", width=12, command=self.adicionar).grid(row=0, column=0, padx=4)
        tk.Button(box, text="Atualizar", width=12, command=self.atualizar).grid(row=0, column=1, padx=4)
        tk.Button(box, text="Deletar",   width=12, command=self.deletar).grid(row=0, column=2, padx=4)
        tk.Button(box, text="Voltar",    width=12, command=self.voltar).grid(row=0, column=3, padx=4)


        # Carrega os cursos ao iniciar a tela
        self.carregar()


    # Carrega os cursos cadastrados no banco e atualiza a lista
    def carregar(self):
        self.lista.delete(0, tk.END)         # Limpa a lista antes de recarregar
        for c in Curso.listar():             # Percorre os cursos retornados do banco
            self.lista.insert(tk.END, f"{c[0]} - {c[1]}")  # Mostra ID e nome do curso
        self.sel_id = None                   # Reseta o curso selecionado
        self.ent_nome.delete(0, tk.END)      # Limpa o campo de texto


    # Evento disparado ao selecionar um curso na lista
    def on_select(self, _):
        s = self.lista.curselection()        # Obtém o índice selecionado
        if not s: return                     # Se nada for selecionado, não faz nada
        curso = Curso.listar()[s[0]]         # Recupera o curso da lista pelo índice
        self.sel_id = curso[0]               # Salva o ID do curso selecionado
        self.ent_nome.delete(0, tk.END)      # Limpa o campo de nome
        self.ent_nome.insert(0, curso[1])    # Preenche com o nome do curso selecionado


    # Adiciona um novo curso
    def adicionar(self):
        nome = self.ent_nome.get().strip()   # Captura o nome digitado, removendo espaços extras
        if nome:                             # Só adiciona se houver nome
            Curso.adicionar(nome)
            self.carregar()                  # Atualiza a lista


    # Atualiza o curso selecionado
    def atualizar(self):
        if self.sel_id:                      # Só atualiza se houver um curso selecionado
            nome = self.ent_nome.get().strip()
            Curso.atualizar(self.sel_id, nome)
            self.carregar()


    # Deleta o curso selecionado
    def deletar(self):
        if self.sel_id:                      # Só deleta se houver curso selecionado
            Curso.deletar(self.sel_id)
            self.carregar()


    # Volta para a tela anterior
    def voltar(self):
        self.destroy()           # Fecha a tela atual
        self.voltar_callback()   # Chama a função para retornar ao menu principal
