import pandas as pd
import numpy as np
import os
import datetime

# --- Configurações que podem ser alteradas pelo usuário ---
# Usando input para obter o ano e mês
ano_str = input("Digite o ano para os dados (ex: 2025): ")
mes_str = input("Digite o mês para os dados (ex: 06): ")

try:
    ano = int(ano_str)
    mes = int(mes_str)
    # Validação básica de mês
    if not (1 <= mes <= 12):
        raise ValueError("Mês inválido. Digite um número entre 1 e 12.")
except ValueError as e:
    print(f"Erro na entrada de ano/mês: {e}. Usando 2025-06 como padrão.")
    ano = 2025
    mes = 6

num_transacoes = int(input("Quantas transações deseja gerar? (ex: 1000): ") or 1000) # Valor padrão se vazio
num_clientes = int(input("Quantos clientes deseja gerar? (ex: 100): ") or 100) # Valor padrão se vazio

# --- Geração dos caminhos de arquivo baseados na entrada ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Garantir que o diretório 'data' existe
os.makedirs(DATA_DIR, exist_ok=True)

# Formatando o nome do arquivo com o ano e mês fornecidos
nome_arquivo_transacoes = f'transacoes_{ano:04d}_{mes:02d}.xlsx'
nome_arquivo_cadastros = f'cadastros_{ano:04d}_{mes:02d}.xlsx'

print(f"\nGerando dados para {mes:02d}/{ano:04d}...")
print(f"Gerando {num_transacoes} transações...")
print(f"Gerando {num_clientes} cadastros de clientes...")

# --- Geração de dados de transações ---
# Calcular o último dia do mês para as datas de venda
ultimo_dia_mes = (datetime.date(ano, mes, 1).replace(month=mes % 12 + 1, year=ano + mes // 12) - datetime.timedelta(days=1)).day

data_transacoes = {
    'ID Cliente': [f'CLI{i:03d}' for i in np.random.randint(1, num_clientes + 1, size=num_transacoes)],
    'Valor Venda': [round(x * 100 + 50, 2) for x in np.random.rand(num_transacoes)],
    'Data Venda': [datetime.date(ano, mes, np.random.randint(1, ultimo_dia_mes + 1)) for _ in range(num_transacoes)], # Data aleatória no mês/ano
    'Produto': [f'PROD{i:03d}' for i in np.random.randint(1, 21, size=num_transacoes)],
    'Quantidade': np.random.randint(1, 10, size=num_transacoes)
}
df_transacoes = pd.DataFrame(data_transacoes)
df_transacoes_path = os.path.join(DATA_DIR, nome_arquivo_transacoes)
df_transacoes.to_excel(df_transacoes_path, index=False)
print(f"Arquivo de transações salvo em: {df_transacoes_path}")

# --- Geração de dados de cadastros ---
print("\nGerando dados de cadastros...")
data_cadastros = {
    'Customer ID': [f'CLI{i:03d}' for i in range(1, num_clientes + 1)],
    'Nome Completo': [
        f'Cliente Teste {i}' if i % 2 == 0 else f'Empresa ABC {i}' for i in range(1, num_clientes + 1)
    ],
    'Segmento': [
        'Grande Empresa' if i % 3 == 0 else ('Pequena Empresa' if i % 3 == 1 else 'Média Empresa')
        for i in range(1, num_clientes + 1)
    ]
}
df_cadastros = pd.DataFrame(data_cadastros)
df_cadastros_path = os.path.join(DATA_DIR, nome_arquivo_cadastros)
df_cadastros.to_excel(df_cadastros_path, index=False)
print(f"Arquivo de cadastros salvo em: {df_cadastros_path}")

print("\nGeração de dados de teste concluída.")
