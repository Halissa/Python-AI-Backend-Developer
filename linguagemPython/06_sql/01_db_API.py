import sqlite3
from pathlib import Path

# Definindo que o nosso db será criado dentro da pasta atual
ROOT_PATH = Path(__file__).parent

# Criando uma conexão com db dentro da pasta atual
conexao = sqlite3.connect(ROOT_PATH / "meu_banco.db")

# Recuperando o cursor
cursor = conexao.cursor()

# ___ Executando comandos a partir do cursos ___

"""
# --> Criando uma tabela
cursor.execute(
    "CREATE TABLE clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(100), email VARCHAR(150))"
)


# --> Inserindo dados na tabela
data = ("Suzana", "suzana@gmail.com")
cursor.execute("INSERT INTO clientes (nome, email) VALUES (?, ?)", data)
conexao.commit()


# --> Atualizar registro
data = ("Suzana Souza", "suzi@gmail.com", 2)
cursor.execute("UPDATE clientes SET nome=?, email=? WHERE id=?;", data)
conexao.commit()


# --> Excluindo um registro
data = (1,)
cursor.execute("DELETE FROM clientes WHERE id=?;", data)
conexao.commit()


# --> Inserindo registros em massa
dados = [
    ("Ana", "ana@gmail.com"),
    ("Pedro", "pedro@gmail.com"),
    ("Gustavo", "gustavo@gmail.com"),
    ("Isabela", "isabela@gmail.com"),
    ("Maria", "maria@gmail.com"),
    ("Nessa", "nessa@gmail.com"),
]

cursor.executemany("INSERT INTO clientes (nome, email) VALUES (?, ?)", dados)
conexao.commit()


# --> Procurando dados
id_sql = 2
cursor.execute("SELECT * FROM clientes WHERE id=?", (id_sql,))
cliente = cursor.fetchone()
print(cliente)


# --> Exibindo toda a tabela:
clientes = cursor.execute("SELECT * FROM clientes;")
for cliente in clientes:
    print(cliente)
"""


# --> Retornando dados como dicionario usando Row factory
id_sql = 6

cursor.row_factory = sqlite3.Row
cursor.execute("SELECT * FROM clientes WHERE id=?", (id_sql,))

cliente = cursor.fetchone()

print(dict(cliente))
print(cliente["nome"], cliente["email"])


# __ Exemplo de funções para executar os comandos __
def criar_tabela(conexao, cursor):
    cursor.execute(
        "CREATE TABLE clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(100), email VARCHAR(150))"
    )


def inserir_registro(conexao, cursor, nome, email):
    data = (nome, email)
    cursor.execute("INSERT INTO clientes (nome, email) VALUES (?, ?)", data)
    conexao.commit()


def atualizar_registro(conexao, cursor, nome, email, id):
    data = (nome, email, id)
    cursor.execute("UPDATE clientes SET nome=?, email=? WHERE id=?;", data)
    conexao.commit()


def excluir_registro(conexao, cursor, id):
    data = (id,)
    cursor.execute("DELETE FROM clientes WHERE id=?;", data)
    conexao.commit()


def inserir_em_massa(conexao, cursor, dados):
    cursor.executemany("INSERT INTO clientes (nome, email) VALUES (?, ?)", dados)
    conexao.commit()


def recuperar_cliente(conexao, cursor, id):
    cursor.execute("SELECT * FROM clientes WHERE id=?", (id,))
    return cursor.fetchone()


def listar_clientes(cursor):
    return cursor.execute("SELECT * FROM clientes;")
