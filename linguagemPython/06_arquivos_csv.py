import csv
from pathlib import Path

ROOT_PATH = Path(__file__).parent


# Escrevendo de arquivo .csv:
try:
    with open(ROOT_PATH / 'usuarios.csv', 'w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["id", "Nome"])
        escritor.writerow(["1", "Maria"])
        escritor.writerow(["2", "João"])
except IOError as exc:
    print(f'Erro ao criar o arquivo {exc}')



# Lende os arquivos .csv
try:
    with open(ROOT_PATH / 'usuarios.csv', 'r', newline='', encoding='utf-8') as arquivo:
        leitor = csv.reader(arquivo)
        for row in leitor:
            print(row)

except IOError as exc:
    print(f'Erro ao criar o arquivo {exc}')
