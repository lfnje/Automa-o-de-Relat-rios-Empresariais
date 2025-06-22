# Caminho: Automação de Relatórios Empresariais/utils.py

import os
import logging
import yaml # NOVO IMPORT

# Importa as variáveis em maiúsculas (ALL_CAPS) do config.py
from config import LOG_FILE, LOG_LEVEL, LOG_FORMAT, CAMINHO_DADOS, CAMINHO_RELATORIOS, CAMINHO_DEFINICOES_RELATORIOS

logger = logging.getLogger(__name__)

def setup_logging():
    """Configura o sistema de logging para a automação."""
    log_dir = os.path.dirname(LOG_FILE)
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logger

def ensure_directories_exist():
    """Garante que os diretórios necessários para dados e relatórios existam."""
    logger.info("Verificando/criando diretórios necessários...")
    os.makedirs(CAMINHO_DADOS, exist_ok=True)
    os.makedirs(CAMINHO_RELATORIOS, exist_ok=True)
    # Também pode ser útil criar a pasta do YAML aqui, se ela não for garantida de outra forma
    os.makedirs(os.path.dirname(CAMINHO_DEFINICOES_RELATORIOS), exist_ok=True)
    logger.info("Diretórios verificados/criados com sucesso.")

# --- NOVA FUNÇÃO PARA CARREGAR DEFINIÇÕES DE RELATÓRIOS ---
def carregar_definicoes_relatorios() -> dict:
    """Carrega as definições de relatórios do arquivo YAML."""
    if not os.path.exists(CAMINHO_DEFINICOES_RELATORIOS):
        logger.error(f"Arquivo de definições de relatórios não encontrado: {CAMINHO_DEFINICOES_RELATORIOS}")
        raise FileNotFoundError(f"Arquivo de definições de relatórios não encontrado: {CAMINHO_DEFINICOES_RELATORIOS}")
    
    try:
        with open(CAMINHO_DEFINICOES_RELATORIOS, 'r', encoding='utf-8') as file:
            definicoes = yaml.safe_load(file)
        logger.info(f"Definições de relatórios carregadas com sucesso de: {CAMINHO_DEFINICOES_RELATORIOS}")
        return definicoes
    except yaml.YAMLError as e:
        logger.critical(f"Erro ao analisar o arquivo YAML de definições de relatórios: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.critical(f"Erro inesperado ao carregar definições de relatórios: {e}", exc_info=True)
        raise
    