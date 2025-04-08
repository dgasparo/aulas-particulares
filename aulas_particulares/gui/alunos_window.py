import tkinter as tk
from tkinter import ttk, messagebox
from utils.masks import MaskedEntry
from database.models import DatabaseManager

class AlunosWindow:
    def __init__(self, root):
        self.root = root
        self.db = DatabaseManager()
        self.setup_ui()
        self.carregar_alunos()
    
    def setup_ui(self):
        # Configuração principal
        self.root.title("Sistema de Aulas Particulares")
        self.root.geometry("1000x700")
        
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Formulário de cadastro
        self.criar_formulario()
        
        # Treeview (lista de alunos)
        self.tree = ttk.Treeview(
            self.main_frame, 
            columns=('Nome da Criança', 'Responsável','Telefone Fixo', 'Celular','E-mail', 'Matéria', 'Valor','Observações'),
            show='headings'
        )
        self.tree.heading('Nome da Criança', text='Nome da Criança')
        self.tree.heading('Responsável', text='Responsável')
        self.tree.heading('Telefone Fixo', text='Telefone Fixo')
        self.tree.heading('Celular', text='Celular')
        self.tree.heading('E-mail', text="E-mail")
        self.tree.heading('Matéria', text='Matéria')
        self.tree.heading('Valor', text='Valor (R$)')
        self.tree.heading('Observações', text='Observações')
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Frame de botões
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            btn_frame, 
            text="Atualizar Lista", 
            command=self.carregar_alunos
        ).pack(side=tk.LEFT, padx=5)

    def criar_formulario(self):
        form_frame = ttk.LabelFrame(self.main_frame, text="Cadastro de Aluno")
        form_frame.pack(fill=tk.X, pady=10)

        # Campos do formulário
        ttk.Label(form_frame, text="Nome da Criança*:").grid(row=0, column=0, sticky='e', padx=5)
        self.entry_nome = ttk.Entry(form_frame, width=30)
        self.entry_nome.grid(row=0, column=1, pady=5, sticky='w')

        ttk.Label(form_frame, text="Responsável*:").grid(row=1, column=0, sticky='e', padx=5)
        self.entry_responsavel = ttk.Entry(form_frame, width=30)
        self.entry_responsavel.grid(row=1, column=1, pady=5, sticky='w')

        ttk.Label(form_frame, text="Telefone Fixo:").grid(row=2, column=0, sticky='e', padx=5)
        self.entry_telefone = MaskedEntry(form_frame, mask="(XX)XXXX-XXXX", width=15)
        self.entry_telefone.grid(row=2, column=1, pady=5, sticky='w')

        ttk.Label(form_frame, text="Celular*:").grid(row=3, column=0, sticky='e', padx=5)
        self.entry_celular = MaskedEntry(form_frame, mask="(XX)XXXXX-XXXX", width=15)
        self.entry_celular.grid(row=3, column=1, pady=5, sticky='w')

        ttk.Label(form_frame, text="E-mail:").grid(row=4, column=0, sticky='e', padx=5)
        self.entry_email = ttk.Entry(form_frame, width=30)
        self.entry_email.grid(row=4, column=1, pady=5, sticky='w')

        ttk.Label(form_frame, text="Matéria:").grid(row=5, column=0, sticky='e', padx=5)
        self.entry_materia = ttk.Entry(form_frame, width=20)
        self.entry_materia.grid(row=5, column=1, pady=5, sticky='w')

        ttk.Label(form_frame, text="Valor Aula (R$):").grid(row=6, column=0, sticky='e', padx=5)
        self.entry_valor = ttk.Entry(form_frame, width=10)
        self.entry_valor.grid(row=6, column=1, pady=5, sticky='w')

        ttk.Label(form_frame, text="Observações:").grid(row=7, column=0, sticky='ne', padx=5)
        self.text_obs = tk.Text(form_frame, width=30, height=3)
        self.text_obs.grid(row=7, column=1, pady=5, sticky='w')

        # Botão de salvar
        ttk.Button(
            form_frame, 
            text="Salvar Aluno", 
            command=self.salvar_aluno
        ).grid(row=8, column=1, pady=10, sticky='w')

    def salvar_aluno(self):
        """Salva um novo aluno no banco de dados"""
        # Coleta os dados do formulário
        dados = {
            'nome': self.entry_nome.get().strip(),
            'responsavel': self.entry_responsavel.get().strip(),
            'telefone': self.entry_telefone.get().strip(),
            'celular': self.entry_celular.get().strip(),
            'email': self.entry_email.get().strip(),
            'materia': self.entry_materia.get().strip(),
            'valor': self.entry_valor.get().strip(),
            'observacoes': self.text_obs.get("1.0", tk.END).strip()
        }

        # Validação dos campos obrigatórios
        if not dados['nome']:
            messagebox.showerror("Erro", "O nome da criança é obrigatório!")
            return
        if not dados['responsavel']:
            messagebox.showerror("Erro", "O nome do responsável é obrigatório!")
            return
        if len(dados['celular']) < 14:  # Verifica se o celular está completo
            messagebox.showerror("Erro", "O celular deve estar completo!")
            return

        try:
            # Converte o valor para float
            valor_aula = float(dados['valor']) if dados['valor'] else 0.0
            
            # Salva no banco de dados
            cursor = self.db.get_cursor()
            cursor.execute(
                "INSERT INTO alunos (nome, responsavel, telefone, celular, email, materia, valor_aula, observacoes) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    dados['nome'],
                    dados['responsavel'],
                    dados['telefone'],
                    dados['celular'],
                    dados['email'],
                    dados['materia'],
                    valor_aula,
                    dados['observacoes']
                )
            )
            self.db.conn.commit()
            
            messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
            self.limpar_campos()
            self.carregar_alunos()
            
        except ValueError:
            messagebox.showerror("Erro", "Valor da aula deve ser um número!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar aluno:\n{str(e)}")
        finally:
            if cursor:
                cursor.close()

    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        self.entry_nome.delete(0, tk.END)
        self.entry_responsavel.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_celular.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_materia.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)
        self.text_obs.delete("1.0", tk.END)

    def carregar_alunos(self):
        """Carrega a lista de alunos do banco de dados"""
        # Limpa a treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Busca os alunos no banco
        cursor = self.db.get_cursor()
        try:
            cursor.execute("SELECT nome, responsavel, telefone, celular, email, materia, valor_aula, observacoes FROM alunos")
            alunos = cursor.fetchall()
            
            # Adiciona na treeview
            for aluno in alunos:
                self.tree.insert('', tk.END, values=aluno)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar alunos:\n{str(e)}")
        finally:
            cursor.close()