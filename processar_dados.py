# Caminho: Automação de Relatórios Empresariais/processar_dados.py

import pandas as pd
import logging
from config import COLUNAS_TRANSACOES, COLUNAS_CADASTROS

logger = logging.getLogger(__name__)

def _padronizar_e_validar_colunas(df: pd.DataFrame, esperado: dict, nome_df: str) -> pd.DataFrame:
    """
    Padroniza nomes de colunas, valida a presença de colunas essenciais,
    e converte tipos de dados, se necessário.
    """
    df_padronizado = df.copy()

    # Recomendação: Converta nomes das colunas do DataFrame para minúsculas
    # e coloque os aliases no config.py em minúsculas para robustez case-insensitive.
    df_padronizado.columns = df_padronizado.columns.str.lower()

    for coluna_logica, aliases in esperado.items():
        encontrada = False
        aliases_para_comparar = [alias.lower() for alias in aliases] # Garante que estamos comparando minúsculas com minúsculas

        for alias in aliases_para_comparar:
            if alias in df_padronizado.columns:
                if alias != coluna_logica:
                    df_padronizado = df_padronizado.rename(columns={alias: coluna_logica})
                encontrada = True
                logger.debug(f"Coluna '{coluna_logica}' mapeada para '{alias}' em {nome_df}.")
                break
        if not encontrada:
            raise KeyError(f"Coluna essencial '{coluna_logica}' (aliases: {aliases}) não encontrada no arquivo de {nome_df}.")

    # Exemplo de conversão de tipo:
    if 'valor' in esperado and 'valor' in df_padronizado.columns:
        try:
            df_padronizado['valor'] = pd.to_numeric(df_padronizado['valor'], errors='coerce')
            df_padronizado.dropna(subset=['valor'], inplace=True)
            logger.debug(f"Coluna 'valor' convertida para numérica em {nome_df}.")
        except Exception as e:
            logger.error(f"Erro ao converter tipo da coluna 'valor' em {nome_df}: {e}", exc_info=True)
            raise

    # Convertendo a coluna 'data' para datetime, se presente e essencial
    if 'data' in esperado and 'data' in df_padronizado.columns:
        try:
            df_padronizado['data'] = pd.to_datetime(df_padronizado['data'], errors='coerce')
            df_padronizado.dropna(subset=['data'], inplace=True)
            logger.debug(f"Coluna 'data' convertida para datetime em {nome_df}.")
        except Exception as e:
            logger.error(f"Erro ao converter tipo da coluna 'data' em {nome_df}: {e}", exc_info=True)
            raise

    return df_padronizado

def carregar_dados(caminhos_arquivos: dict) -> dict[str, pd.DataFrame]:
    """
    Carrega, padroniza e valida os dados de arquivos Excel baseados nos caminhos fornecidos.
    Retorna um dicionário de DataFrames.
    """
    dataframes = {}
    logger.info("Iniciando carregamento dos dados de entrada...")

    mapeamento_colunas = {
        "transacoes": COLUNAS_TRANSACOES,
        "cadastros": COLUNAS_CADASTROS,
    }

    for nome_fonte, caminho_arquivo in caminhos_arquivos.items():
        try:
            logger.info(f"Carregando {nome_fonte} de: {caminho_arquivo}")
            df = pd.read_excel(caminho_arquivo)

            if df.empty:
                logger.warning(f"O DataFrame de {nome_fonte} está vazio.")
                dataframes[nome_fonte] = pd.DataFrame()
                continue

            colunas_esperadas = mapeamento_colunas.get(nome_fonte)
            if colunas_esperadas:
                df_padronizado = _padronizar_e_validar_colunas(df, colunas_esperadas, nome_fonte)
                dataframes[nome_fonte] = df_padronizado
                logger.info(f"Dados de {nome_fonte} carregados e padronizados com sucesso.")
            else:
                logger.warning(f"Mapeamento de colunas não encontrado para {nome_fonte}. Carregando DataFrame sem padronização.")
                dataframes[nome_fonte] = df
            
        except FileNotFoundError as e:
            logger.error(f"Erro: Arquivo não encontrado para {nome_fonte} - {e.filename}.", exc_info=True)
            raise
        except pd.errors.EmptyDataError as e:
            logger.error(f"Erro: Arquivo de dados de {nome_fonte} vazio - {e.filename}.", exc_info=True)
            raise
        except KeyError as e:
            logger.error(f"Erro de estrutura de dados em {nome_fonte}: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao carregar os dados de {nome_fonte}: {e}", exc_info=True)
            raise
    
    # Esta verificação é importante, pois 'transacoes' é a base da maioria dos relatórios
    if dataframes.get("transacoes", pd.DataFrame()).empty:
        raise ValueError("O DataFrame de transações está vazio após o carregamento e padronização. Não é possível gerar o relatório principal.")
    
    logger.info("Todos os dados de entrada carregados, padronizados e validados com sucesso!")
    return dataframes

