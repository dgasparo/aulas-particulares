INSERT_ALUNO = """
INSERT INTO alunos (nome, telefone, email, materia, valor_aula)
VALUES (?, ?, ?, ?, ?)
"""

SELECT_ALUNOS = "SELECT * FROM alunos"