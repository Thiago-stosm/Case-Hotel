"""O arquivo executa uma leitura dos dados da tabela do Excel e as exibe no console"""
import pandas as pd

# Carrega a planilha
df = pd.read_excel("C:\\Users\\LENOVO\\Documents\\_Case Hotel (1).xlsx", sheet_name="Base de Dados")

# Mostra as primeiras linhas
print(df.head())

# Mostra os nomes das colunas
print(df.columns)

# Verifica tipos de dados
print(df.dtypes)
