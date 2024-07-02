import sqlite3
from pathlib import Path

# Definindo que o nosso db será criado dentro da pasta atual
ROOT_PATH = Path(__file__).parent

# Criando uma conexão com db dentro da pasta atual
conexao = sqlite3.connect(ROOT_PATH / "meu_banco.db")

# Recuperando o cursor
cursor = conexao.cursor()

# Definindo o cursor como row factory
cursor.row_factory = sqlite3.Row

try:
    cursor.execute(
        "INSERT INTO clientes (nome, email) VALUES(?, ?)",
        ("Teste 1", "teste1@gmail.com"),
    )
    cursor.execute(
        "INSERT INTO clientes (id, nome, email) VALUES(?, ?, ?)",
        (2, "Teste 2", "teste2@gmail.com"),
    )
    conexao.commit()
except Exception as exc:
    print(f"Ops! um erro ocorreu {exc}")
    conexao.rollback()
