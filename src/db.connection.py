import pandas as pd
from sqlalchemy import create_engine
import os

# --- 1. CONFIGURAÇÕES ---
# Coloque aqui as informações de conexão com o seu banco de dados MySQL.
# É uma boa prática não deixar senhas diretamente no código em projetos reais,
# mas para este script de migração, faremos de forma direta.
db_user = "root"  # Ex: "root"
db_password = "MySQL_@0756"
db_host = "localhost"  # Geralmente é "localhost" ou "127.0.0.1"
db_port = "3306"  # Porta padrão do MySQL
db_name = "reservas"  # O nome do banco de dados que você criou

# --- 2. CARREGAR OS DADOS DO EXCEL ---
# Como o arquivo está no diretório do projeto, podemos criar o caminho para ele.
# Substitua 'nome_do_seu_arquivo.xlsx' pelo nome real do seu arquivo.
try:
    file_name = "_Case Hotel (1).xlsx"
    # Pega o caminho do diretório onde o script está sendo executado
    project_directory = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(project_directory, file_name)

    print(f"Tentando carregar o arquivo de: {excel_path}")
    df = pd.read_excel(excel_path)
    print("Arquivo Excel carregado com sucesso!")

except FileNotFoundError:
    print(f"ERRO: O arquivo '{file_name}' não foi encontrado no diretório do projeto.")
    exit()  # Encerra o script se o arquivo não for encontrado

# --- 3. PREPARAR O DATAFRAME PARA O MYSQL ---
# É crucial que os nomes das colunas no DataFrame sejam idênticos aos da tabela no MySQL.
# Vamos fazer alguns ajustes que identificamos na análise anterior.

# Dicionário para renomear as colunas (de 'nome_no_excel' para 'nome_no_mysql')
colunas_para_renomear = {
    'país': 'pais'  # Remove o acento para corresponder à coluna do MySQL
    # Adicione outras colunas aqui se os nomes forem diferentes.
}

df.rename(columns=colunas_para_renomear, inplace=True)

# O Pandas pode ler a coluna 'agencia_turismo' com valores vazios (NaN) como float.
# Se a coluna no MySQL for INT, precisamos converter e tratar os NaNs.
# Vamos preencher os valores vazios (NaN) com 0 e depois converter para inteiro.
# Se você quiser manter os valores vazios como NULL no banco, a abordagem é outra.
# Por simplicidade, vamos usar 0.
if 'agencia_turismo' in df.columns:
    df['agencia_turismo'] = df['agencia_turismo'].fillna(0).astype(int)

print("Colunas do DataFrame ajustadas para o padrão do MySQL.")
print("Colunas atuais:", df.columns.tolist())

# --- 4. CONECTAR AO BANCO DE DADOS E INSERIR OS DADOS ---
try:
    # A string de conexão informa ao SQLAlchemy como se conectar ao banco.
    # O formato é: "mysql+mysqlconnector://usuario:senha@host:porta/database"
    connection_string = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    # Cria o "motor" de conexão
    engine = create_engine(connection_string)

    print("Conexão com o MySQL estabelecida com sucesso!")

    # Agora, a "mágica" acontece. O método to_sql do pandas envia o DataFrame para o SQL.
    # - 'reservas_hoteis': Nome da tabela que você criou no MySQL.
    # - con=engine: A conexão que acabamos de criar.
    # - if_exists='append': Se a tabela já tiver dados, ele adiciona os novos no final.
    #   Outras opções: 'replace' (apaga a tabela e cria de novo) ou 'fail' (dá erro).
    # - index=False: Para não criar uma coluna "index" do pandas dentro da sua tabela SQL.
    df.to_sql('reservas_hoteis', con=engine, if_exists='append', index=False)

    print("----------------------------------------------------------")
    print(f"SUCESSO! Os dados foram inseridos na tabela 'reservas_hoteis'.")
    print(f"Total de {len(df)} linhas inseridas.")
    print("----------------------------------------------------------")

except Exception as e:
    print(f"Ocorreu um erro durante a conexão ou inserção no MySQL: {e}")