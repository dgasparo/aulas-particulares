import tkinter as tk
from gui.alunos_window import AlunosWindow

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.app = AlunosWindow(self.root)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def on_close(self):
        """Executado quando a janela é fechada"""
        if hasattr(self.app, 'db'):
            self.app.db.close()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()