INSERT_ALUNO = """
INSERT INTO alunos (nome, responsavel, telefone, celular, email, materia, valor_aula, observacoes)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

SELECT_ALUNOS = "SELECT * FROM alunos"