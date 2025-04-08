import tkinter as tk
from tkinter import ttk, messagebox
from database.models import DatabaseManager

class AlunosWindow:
    def __init__(self, root):
        self.root = root
        self.db = DatabaseManager()
        self.setup_ui()
        self.carregar_alunos()  # Carrega automaticamente ao iniciar
    
    def setup_ui(self):
        # Configuração principal
        self.root.title("Sistema de Aulas Particulares")
        self.root.geometry("800x600")
        
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview (lista de alunos)
        self.tree = ttk.Treeview(
            self.main_frame, 
            columns=('Nome', 'Telefone', 'Matéria', 'Valor'),
            show='headings'
        )
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Telefone', text='Telefone')
        self.tree.heading('Matéria', text='Matéria')
        self.tree.heading('Valor', text='Valor (R$)')
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Frame de botões
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            btn_frame, 
            text="Carregar Alunos", 
            command=self.carregar_alunos
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Adicionar Aluno",
            command=self.adicionar_aluno
        ).pack(side=tk.LEFT, padx=5)
    
    def carregar_alunos(self):
        # Limpa a lista atual
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Busca no banco de dados
        cursor = self.db.get_cursor()
        try:
            cursor.execute("SELECT nome, telefone, materia, valor_aula FROM alunos")
            for aluno in cursor.fetchall():
                self.tree.insert('', tk.END, values=aluno)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar alunos: {str(e)}")
        finally:
            cursor.close()
    
    def adicionar_aluno(self):
        # Janela de cadastro (implementar depois)
        messagebox.showinfo("Info", "Funcionalidade em desenvolvimento")