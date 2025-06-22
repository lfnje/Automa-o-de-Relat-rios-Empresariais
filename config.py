# Caminho: Automação de Relatórios Empresariais/config.py

import os
from logging import INFO
import datetime

# --- Caminhos de Arquivos ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CAMINHO_DADOS = os.path.join(BASE_DIR, 'data') # Pasta onde os arquivos de entrada estão
CAMINHO_RELATORIOS = os.path.join(BASE_DIR, 'relatorios') # Pasta onde os relatórios serão salvos

# Caminho para o arquivo de definições de relatórios (NOVO)
CAMINHO_DEFINICOES_RELATORIOS = os.path.join(BASE_DIR, 'config_reports', 'report_definitions.yaml') 

# --- Mapeamento de Colunas Flexíveis (manter e personalizar) ---
# ATENÇÃO: Ajuste estes aliases para os NOMES REAIS (e em minúsculas, recomendado) das colunas nas SUAS planilhas!
COLUNAS_TRANSACOES = {
    'cliente': ['cliente', 'ID Cliente', 'Cód. Cliente', 'Nome do Cliente', 'Customer ID'],
    'valor': ['valor', 'Valor Venda', 'Total Venda', 'Preço Total', 'Sales Value'],
    'data': ['data', 'Data Venda', 'Sale Date', 'Transaction Date']
}

COLUNAS_CADASTROS = {
    'cliente': ['cliente', 'ID Cliente', 'Cód. Cliente', 'Nome do Cliente', 'Customer ID'],
    'nome_completo': ['Nome', 'Nome Completo', 'Full Name'],
    'segmento': ['Segmento', 'Classificacao Cliente', 'Customer Segment']
}

# --- Configurações de E-mail (globais - podem ser sobrescritas no YAML do relatório) ---
# É ALTAMENTE RECOMENDADO carregar estas variáveis de ambiente para maior segurança.
# Se não usar variáveis de ambiente, coloque suas credenciais AQUI para TESTE, mas remova para PROD.
EMAIL_REMETENTE = os.getenv('EMAIL_REMETENTE', 'lfesperanca17@gmail.com') # <--- **COLOQUE SEU E-MAIL DE REMETENTE AQUI**
SENHA_APP = os.getenv('SENHA_APP', 'ryrhsmhcinhbkecz') # <--- **COLOQUE SUA SENHA DE APP DO GOOGLE AQUI**
EMAIL_DESTINATARIOS = [
    'lfnjecorporativo@gmail.com', # <--- **COLOQUE OS E-MAILS REAIS DOS DESTINATÁRIOS AQUI**
    'lfnjeesperanca@gmail.com'
]
EMAIL_ASSUNTO_PADRAO = "Relatório Gerencial Mensal de Vendas"
EMAIL_CORPO_PADRAO = """
Prezados(as),

Segue em anexo o relatório gerencial de vendas atualizado, com os dados mais recentes.

Atenciosamente,

Equipe de Automação de Relatórios
"""

# --- Configurações de Logging ---
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'automacao_relatorios.log')
LOG_LEVEL = INFO
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
