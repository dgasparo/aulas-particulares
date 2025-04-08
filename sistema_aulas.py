# Sistema de Gestão de Aulas Particulares v1.0
# Desenvolvido por Daniel
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class SistemaAulas:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Aulas Particulares")
        self.root.geometry("1000x600")
        
        self.criar_banco_dados()
        self.criar_interface()
    
    def criar_banco_dados(self):
        """Cria o banco de dados SQLite e as tabelas necessárias"""
        self.conn = sqlite3.connect('aulas.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT,
            email TEXT,
            materia TEXT,
            frequencia TEXT,
            valor_aula REAL,
            observacoes TEXT
        )''')
        
        # Tabelas para atividades e pagamentos (serão implementadas depois)
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER,
            data TEXT,
            tipo TEXT,
            descricao TEXT,
            comentarios TEXT,
            status TEXT,
            FOREIGN KEY (aluno_id) REFERENCES alunos (id)
        )''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS pagamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER,
            data TEXT,
            valor REAL,
            status TEXT,
            forma_pagamento TEXT,
            observacoes TEXT,
            FOREIGN KEY (aluno_id) REFERENCES alunos (id)
        )''')
        
        self.conn.commit()
    
    def criar_interface(self):
        """Cria a interface principal com abas"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        
        # Aba Alunos
        self.aba_alunos = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_alunos, text="Alunos")
        
        # Configura o evento para quando a aba for alterada
        self.notebook.bind("<<NotebookTabChanged>>", self.ao_mudar_aba)
        
        self.criar_aba_alunos()
        
        # (As outras abas serão implementadas depois)
    
    def ao_mudar_aba(self, event):
        """Atualiza automaticamente a lista quando a aba Alunos é selecionada"""
        if self.notebook.tab(self.notebook.select(), "text") == "Alunos":
            self.carregar_alunos()
    
    def criar_aba_alunos(self):
        """Cria todos os elementos da aba de alunos"""
        # Frame do formulário de cadastro
        frame_cadastro = ttk.LabelFrame(self.aba_alunos, text="Cadastrar Novo Aluno")
        frame_cadastro.pack(pady=10, padx=10, fill='x')
        
        # Campos do formulário
        tk.Label(frame_cadastro, text="Nome:").grid(row=0, column=0, sticky='e')
        self.entry_nome = tk.Entry(frame_cadastro, width=40)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_cadastro, text="Telefone:").grid(row=1, column=0, sticky='e')
        self.entry_telefone = tk.Entry(frame_cadastro)
        self.entry_telefone.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame_cadastro, text="E-mail:").grid(row=2, column=0, sticky='e')
        self.entry_email = tk.Entry(frame_cadastro)
        self.entry_email.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(frame_cadastro, text="Matéria:").grid(row=3, column=0, sticky='e')
        self.entry_materia = tk.Entry(frame_cadastro)
        self.entry_materia.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(frame_cadastro, text="Valor Aula (R$):").grid(row=4, column=0, sticky='e')
        self.entry_valor = tk.Entry(frame_cadastro)
        self.entry_valor.grid(row=4, column=1, padx=5, pady=5)
        
        # Botão Salvar
        tk.Button(frame_cadastro, text="Salvar Aluno", command=self.salvar_aluno).grid(row=5, column=1, pady=10, sticky='e')
        
        # Lista de alunos (Treeview)
        frame_lista = ttk.LabelFrame(self.aba_alunos, text="Alunos Cadastrados")
        frame_lista.pack(pady=10, padx=10, fill='both', expand=True)
        
        colunas = ('Nome', 'Telefone', 'Matéria', 'Valor Aula')
        self.tree_alunos = ttk.Treeview(frame_lista, columns=colunas, show='headings')
        
        for col in colunas:
            self.tree_alunos.heading(col, text=col)
        
        self.tree_alunos.pack(fill='both', expand=True)
        
        # Carrega os alunos imediatamente ao abrir a aba
        self.carregar_alunos()
    
    def salvar_aluno(self):
        """Salva um novo aluno no banco de dados"""
        nome = self.entry_nome.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()
        materia = self.entry_materia.get()
        valor = self.entry_valor.get()
        
        if not nome:
            messagebox.showerror("Erro", "O nome do aluno é obrigatório!")
            return
        
        try:
            self.cursor.execute(
                "INSERT INTO alunos (nome, telefone, email, materia, valor_aula) VALUES (?, ?, ?, ?, ?)",
                (nome, telefone, email, materia, float(valor) if valor else 0.0))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
            self.limpar_campos()
            self.carregar_alunos()  # Atualiza a lista após salvar
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar: {str(e)}")
    
    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        self.entry_nome.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_materia.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)
    
    def carregar_alunos(self):
        """Carrega a lista de alunos do banco de dados"""
        # Limpa a treeview
        for item in self.tree_alunos.get_children():
            self.tree_alunos.delete(item)
        
        # Busca os alunos no banco
        self.cursor.execute("SELECT nome, telefone, materia, valor_aula FROM alunos")
        alunos = self.cursor.fetchall()
        
        # Adiciona na treeview
        for aluno in alunos:
            self.tree_alunos.insert('', tk.END, values=aluno)

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaAulas(root)
    root.mainloop()