import tkinter as tk
from tkinter import ttk
from models.models import Turma, Curso, Aluno


class TurmasView(tk.Frame):
    def __init__(self, master, voltar_callback):
        super().__init__(master, bg="#fffbe6")
        self.pack(fill="both", expand=True)
        self.voltar_callback = voltar_callback
        self.sel_id = None


        tk.Label(self, text="Turmas", font=("Arial", 18, "bold"), bg="#fffbe6").pack(pady=10)


        cont = tk.Frame(self, bg="#fffbe6"); cont.pack(fill="both", expand=True, padx=10, pady=8)


        # CRUD
        crud = tk.Frame(cont, bg="#fffbe6"); crud.pack(side=tk.LEFT, fill="both", expand=True, padx=10)
        tk.Label(crud, text="Nome:", bg="#fffbe6").pack(anchor="w")
        self.ent_nome = tk.Entry(crud, width=30); self.ent_nome.pack(pady=4, fill="x")


        tk.Label(crud, text="Curso:", bg="#fffbe6").pack(anchor="w")
        self.cb_cursos = ttk.Combobox(crud, state="readonly"); self.cb_cursos.pack(pady=4, fill="x")


        self.lista = tk.Listbox(crud, width=42, height=12); self.lista.pack(pady=8, fill="both", expand=True)
        self.lista.bind("<<ListboxSelect>>", self.on_select)


        box = tk.Frame(crud, bg="#fffbe6"); box.pack(pady=6)
        tk.Button(box, text="Adicionar", width=12, command=self.adicionar).grid(row=0, column=0, padx=4)
        tk.Button(box, text="Atualizar", width=12, command=self.atualizar).grid(row=0, column=1, padx=4)
        tk.Button(box, text="Deletar",   width=12, command=self.deletar).grid(row=0, column=2, padx=4)
        tk.Button(box, text="Voltar",    width=12, command=self.voltar).grid(row=0, column=3, padx=4)


        # Alunos por Turma
        painel = tk.Frame(cont, bg="#fffbe6"); painel.pack(side=tk.RIGHT, fill="both", expand=True, padx=10)
        tk.Label(painel, text="Alunos da Turma", font=("Arial", 14), bg="#fffbe6").pack(pady=6)
        self.lista_alunos = tk.Listbox(painel, width=42, height=10); self.lista_alunos.pack(pady=4, fill="both", expand=True)


        tk.Label(painel, text="Associar Aluno:", bg="#fffbe6").pack(anchor="w")
        self.cb_alunos = ttk.Combobox(painel, state="readonly"); self.cb_alunos.pack(pady=4, fill="x")
        tk.Button(painel, text="Associar", command=self.associar).pack(pady=6)


        self.carregar_cursos()
        self.carregar_alunos_combo()
        self.carregar()


    # --- helpers de carga ---
    def carregar_cursos(self):
        self.cb_cursos['values'] = [f"{c[0]} - {c[1]}" for c in Curso.listar()]


    def carregar_alunos_combo(self):
        self.cb_alunos['values'] = [f"{a[0]} - {a[1]}" for a in Aluno.listar()]


    def carregar(self):
        self.lista.delete(0, tk.END)
        for t in Turma.listar():
            self.lista.insert(tk.END, f"{t[0]} - {t[1]} (Curso: {t[2]})")
        self.sel_id = None
        self.ent_nome.delete(0, tk.END)
        self.cb_cursos.set("")
        self.lista_alunos.delete(0, tk.END)


    # --- CRUD ---
    def on_select(self, _):
        s = self.lista.curselection()
        if not s: return
        turma = Turma.listar()[s[0]]
        self.sel_id = turma[0]
        self.ent_nome.delete(0, tk.END); self.ent_nome.insert(0, turma[1])


        curso_nome = turma[2] or ""
        for i, v in enumerate(self.cb_cursos['values']):
            if v.split(" - ", 1)[1] == curso_nome:
                self.cb_cursos.current(i); break


        self.listar_alunos_turma()


    def adicionar(self):
        nome = self.ent_nome.get().strip()
        curso_sel = self.cb_cursos.get()
        if nome and curso_sel:
            curso_id = int(curso_sel.split(" - ")[0])
            Turma.adicionar(nome, curso_id)
            self.carregar()


    def atualizar(self):
        if self.sel_id:
            nome = self.ent_nome.get().strip()
            curso_sel = self.cb_cursos.get()
            if nome and curso_sel:
                curso_id = int(curso_sel.split(" - ")[0])
                Turma.atualizar(self.sel_id, nome, curso_id)
                self.carregar()


    def deletar(self):
        if self.sel_id:
            Turma.deletar(self.sel_id)
            self.carregar()


    # --- alunos por turma ---
    def listar_alunos_turma(self):
        self.lista_alunos.delete(0, tk.END)
        if not self.sel_id: return
        for a in Turma.listar_alunos(self.sel_id):
            self.lista_alunos.insert(tk.END, f"{a[0]} - {a[1]}")


    def associar(self):
        if self.sel_id:
            aluno_sel = self.cb_alunos.get()
            if aluno_sel:
                aluno_id = int(aluno_sel.split(" - ")[0])
                # pegar o nome atual do aluno
                nome = None
                for a in Aluno.listar():
                    if a[0] == aluno_id:
                        nome = a[1]; break
                if nome is not None:
                    Aluno.atualizar(aluno_id, nome, self.sel_id)
                    self.listar_alunos_turma()
                    self.carregar_alunos_combo()


    def voltar(self):
        self.destroy()
        self.voltar_callback()



