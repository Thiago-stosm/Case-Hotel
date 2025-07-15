# -*- coding: utf-8 -*-
"""
Script para migrar dados de um arquivo Excel para uma tabela em um banco de dados MySQL.
- Carrega os dados do Excel.
- Limpa e prepara os dados (renomeia colunas, ajusta tipos).
- Conecta ao MySQL e insere os dados na tabela.
"""

import os
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus  # Para tratar senhas com caracteres especiais


def migrar_excel_para_mysql():
    """
    Função principal que executa todo o processo de migração.
    """
    # --- 1. CONFIGURAÇÕES ---
    # Altere os valores abaixo com suas informações.

    # Configurações do Banco de Dados
    db_user = "root"
    # Sua senha pode ter caracteres especiais. O 'quote_plus' cuidará disso.
    db_password = "MySQL_@0756"
    db_host = "localhost"
    db_port = "3306"
    db_name = "reservas"
    db_table_name = "reservas_hoteis"

    # Configuração do Arquivo Excel
    excel_file_name = "_Case Hotel (1).xlsx"
    # Assumimos que o cabeçalho está na primeira linha do Excel (índice 0).
    # Se estiver em outra linha, ajuste este número.
    excel_header_row = 0

    # --- 2. CARREGAR DADOS DO EXCEL ---
    print(">>> Iniciando Etapa 2: Carregar dados do Excel...")
    try:
        # Pega o caminho do diretório onde este script está salvo
        script_dir = os.path.dirname(os.path.abspath(__file__))
        excel_path = os.path.join(script_dir, excel_file_name)

        print(f"Carregando arquivo: {excel_path}")
        # Para ler a SEGUNDA aba do arquivo, usamos o índice 1 (sheet_name=1)
        df = pd.read_excel(excel_path, sheet_name=1, header=excel_header_row)
        print("✔ Arquivo Excel carregado com sucesso!")

    except FileNotFoundError:
        print(f"ERRO: O arquivo '{excel_file_name}' não foi encontrado na pasta '{script_dir}'.")
        print("Por favor, verifique se o nome do arquivo está correto e se ele está na mesma pasta do script.")
        return  # Encerra a função se o arquivo não for encontrado

    except Exception as e:
        print(f"ERRO inesperado ao ler o arquivo Excel: {e}")
        return

    # --- 3. PREPARAR O DATAFRAME ---
    print("\n>>> Iniciando Etapa 3: Preparar os dados...")
    try:
        # Renomeia colunas para corresponder à tabela do banco de dados
        colunas_para_renomear = {
            'país': 'pais'  # Remove o acento
        }
        df.rename(columns=colunas_para_renomear, inplace=True)

        # Trata a coluna 'agencia_turismo': preenche valores vazios (NaN) com 0 e converte para inteiro.
        if 'agencia_turismo' in df.columns:
            df['agencia_turismo'] = df['agencia_turismo'].fillna(0).astype(int)

        print("✔ Dados preparados para o banco de dados.")
        # Mostra as colunas para verificação final
        print("Colunas que serão inseridas:", df.columns.tolist())

    except Exception as e:
        print(f"ERRO ao preparar os dados do DataFrame: {e}")
        return

    # --- 4. CONECTAR AO MYSQL E INSERIR DADOS ---
    print("\n>>> Iniciando Etapa 4: Conectar ao MySQL e inserir dados...")
    try:
        # Codifica a senha para evitar erros com caracteres especiais (como @, #, $)
        encoded_password = quote_plus(db_password)

        # Cria a string de conexão segura
        connection_string = f"mysql+mysqlconnector://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"

        # Cria o "motor" de conexão do SQLAlchemy
        engine = create_engine(connection_string)

        print("Conectando ao banco de dados...")
        # Insere os dados do DataFrame na tabela do MySQL
        df.to_sql(
            name=db_table_name,
            con=engine,
            if_exists='append',  # Adiciona os dados aos existentes. Use 'replace' para substituir.
            index=False  # Não insere o índice do DataFrame como uma coluna.
        )
        print("----------------------------------------------------------------")
        print(f"SUCESSO! {len(df)} linhas foram inseridas na tabela '{db_table_name}'.")
        print("----------------------------------------------------------------")

    except Exception as e:
        print(f"ERRO durante a conexão ou inserção no MySQL: {e}")


# Esta é uma boa prática em Python para garantir que o script só será executado
# quando você rodar este arquivo diretamente.
if __name__ == "__main__":
    migrar_excel_para_mysql()