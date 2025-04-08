import sqlite3
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_name='aulas.db'):
        self.db_path = Path(__file__).parent.parent / db_name
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                responsavel TEXT NOT NULL,
                telefone TEXT,
                celular TEXT NOT NULL,
                email TEXT,
                materia TEXT,
                valor_aula REAL,
                observacoes TEXT
                )
            ''')
            self.conn.commit()
        finally:
            cursor.close()
    
    def get_cursor(self):
        return self.conn.cursor()
    
    def close(self):
        if self.conn:
            self.conn.close()