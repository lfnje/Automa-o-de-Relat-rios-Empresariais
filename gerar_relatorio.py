# Caminho: Automação de Relatórios Empresariais/gerar_relatorio.py

import pandas as pd
import logging
import os
from config import CAMINHO_RELATORIOS

logger = logging.getLogger(__name__)

# Adaptação: gerar_relatorio AGORA RECEBE O DICIONÁRIO DE DATAFRAMES E A DEFINIÇÃO DO RELATÓRIO
def gerar_relatorio(dataframes: dict[str, pd.DataFrame], definicao_relatorio: dict, caminho_saida_relatorio: str) -> str:
    """
    Gera um relatório dinamicamente com base nas definições fornecidas no YAML.
    """
    nome_relatorio_yaml = definicao_relatorio.get('descricao', 'Relatório não especificado')
    logger.info(f"Iniciando a geração do relatório: {nome_relatorio_yaml}")

    try:
        # 1. Obter a fonte de dados principal
        # Certifique-se de que 'fontes_dados' e o primeiro elemento existem
        fontes_dados_config = definicao_relatorio.get('fontes_dados')
        if not fontes_dados_config or not isinstance(fontes_dados_config, list) or not fontes_dados_config[0].get('nome'):
            raise ValueError("A definição 'fontes_dados' no YAML está ausente ou malformada.")
            
        fonte_principal_nome = fontes_dados_config[0].get('nome') # Pega a primeira fonte como principal
        if not fonte_principal_nome or fonte_principal_nome not in dataframes:
            raise ValueError(f"Fonte de dados principal '{fonte_principal_nome}' não definida ou não carregada.")
        
        df_relatorio = dataframes[fonte_principal_nome].copy()

        if df_relatorio.empty:
            logger.warning(f"O DataFrame da fonte principal '{fonte_principal_nome}' está vazio. Retornando DataFrame vazio.")
            # Dependendo da sua necessidade, você pode levantar um erro aqui ou retornar um DF vazio e deixar o chamador decidir.
            return pd.DataFrame() # Retorna um DataFrame vazio se a fonte principal estiver vazia

        # 2. Realizar Junções (Merge), se definidas
        if 'juncoes' in definicao_relatorio:
            for juncao in definicao_relatorio['juncoes']:
                df_direita_nome = juncao.get('direito')
                on_coluna = juncao.get('on')
                how_tipo = juncao.get('how', 'left') # Default para left merge

                if not df_direita_nome or df_direita_nome not in dataframes:
                    logger.warning(f"DataFrame '{df_direita_nome}' para junção não encontrado ou nome inválido. Pulando esta junção.")
                    continue
                
                df_direita = dataframes[df_direita_nome]

                # Selecionar colunas específicas para junção do dataframe direito, se especificado
                colunas_direita_para_incluir = [on_coluna] # Sempre incluir a coluna de junção
                # Adiciona outras colunas do df_direita que serão usadas na saída ou agregação, se não forem a chave de junção
                for col_saida in definicao_relatorio.get('colunas_saida', []):
                    if col_saida in df_direita.columns and col_saida != on_coluna:
                        colunas_direita_para_incluir.append(col_saida)
                
                # Certificar-se que as colunas existem antes de selecionar
                colunas_direita_validas = list(set([col for col in colunas_direita_para_incluir if col in df_direita.columns]))
                
                if not colunas_direita_validas: # Se nem a coluna 'on' não existe no df_direita
                    logger.warning(f"Nenhuma coluna válida para junção de '{df_direita_nome}'. Junção pulada.")
                    continue

                try:
                    df_relatorio = df_relatorio.merge(
                        df_direita[colunas_direita_validas], # Seleciona apenas as colunas necessárias para o merge
                        on=on_coluna,
                        how=how_tipo
                    )
                    logger.debug(f"Junção de '{fonte_principal_nome}' com '{df_direita_nome}' na coluna '{on_coluna}' concluída.")
                except pd.errors.MergeError as e:
                    logger.warning(f"Erro ao mesclar dados: {e}. Junção entre '{fonte_principal_nome}' e '{df_direita_nome}' pulada.", exc_info=True)
                except Exception as e:
                    logger.warning(f"Erro inesperado durante a junção: {e}. Junção entre '{fonte_principal_nome}' e '{df_direita_nome}' pode estar incompleta.", exc_info=True)

        # 3. Processamento de Relatório (Agrupar e Agregações)
        processamento = definicao_relatorio.get('processamento_relatorio')
        if processamento:
            agrupar_por = processamento.get('agrupar_por')
            agregacoes_yaml = processamento.get('agregacoes')

            if agrupar_por and agregacoes_yaml:
                # Converter as agregações do YAML para o formato aceito pelo .agg() do Pandas
                pandas_aggs = {}
                for nome_nova_coluna, def_agg in agregacoes_yaml.items():
                    coluna_origem = def_agg.get('coluna_origem')
                    funcao_agg = def_agg.get('funcao')
                    if coluna_origem and funcao_agg:
                        pandas_aggs[nome_nova_coluna] = (coluna_origem, funcao_agg)
                    else:
                        logger.warning(f"Agregação malformada para '{nome_nova_coluna}'. Pulando.")

                if pandas_aggs:
                    # Garantir que as colunas de agrupamento existam e são válidas
                    valid_group_cols = [col for col in agrupar_por if col in df_relatorio.columns]
                    missing_group_cols = [col for col in agrupar_por if col not in df_relatorio.columns]

                    if missing_group_cols:
                        logger.warning(f"Colunas de agrupamento ausentes no DataFrame após junções: {missing_group_cols}. Agrupamento pode ser incompleto ou falhar.")
                    
                    if not valid_group_cols:
                        logger.warning("Nenhuma coluna de agrupamento válida encontrada. Agrupamento ignorado.")
                        # Se não há colunas para agrupar, somar tudo se houver agregações
                        df_relatorio = df_relatorio.agg(**pandas_aggs).to_frame().T # Soma total, Transpõe para manter formato de DF
                    else:
                        df_relatorio = df_relatorio.groupby(valid_group_cols, as_index=False).agg(**pandas_aggs)
                        logger.debug(f"Agrupamento e agregações realizadas por: {valid_group_cols}.")
                else:
                    logger.warning("Nenhuma agregação válida definida para o relatório.")
            elif agrupar_por:
                logger.warning("Agrupamento definido, mas nenhuma agregação. Relatório pode não ter as métricas esperadas.")


        # 4. Cálculos Adicionais (complexo, aqui apenas um placeholder para futura expansão)
        # if 'calculos_adicionais' in definicao_relatorio:
        #     for calc in definicao_relatorio['calculos_adicionais']:
        #         logger.warning(f"Cálculos adicionais não implementados ainda: {calc.get('nome_nova_coluna')}")


        # 5. Seleção e Ordem das Colunas de Saída
        colunas_saida = definicao_relatorio.get('colunas_saida')
        if colunas_saida:
            # Filtrar e ordenar as colunas que realmente existem no DataFrame final
            final_cols = [col for col in colunas_saida if col in df_relatorio.columns]
            if len(final_cols) < len(colunas_saida):
                missing_cols = set(colunas_saida) - set(final_cols)
                logger.warning(f"Algumas colunas de saída especificadas não foram encontradas no relatório final: {missing_cols}. Elas serão ignoradas.")
            
            if not final_cols: # Se nenhuma coluna de saída válida foi encontrada
                logger.warning("Nenhuma coluna de saída válida para o relatório. Verifique a definição no YAML. Retornando DataFrame vazio.")
                return pd.DataFrame()
            
            df_relatorio = df_relatorio[final_cols]
            logger.debug("Colunas de saída selecionadas e ordenadas.")
        else:
            logger.warning("Nenhuma coluna de saída especificada. Todas as colunas disponíveis serão incluídas.")

        # Opcional: Ordenar o relatório final
        if 'ordenar_por' in definicao_relatorio:
            sort_config = definicao_relatorio['ordenar_por']
            sort_cols = sort_config.get('colunas', []) # Pode ser uma lista de colunas para ordenar
            sort_ascending = sort_config.get('ascendente', True)

            # Garante que as colunas de ordenação existem no DataFrame final
            existing_sort_cols = [col for col in sort_cols if col in df_relatorio.columns]
            if existing_sort_cols:
                df_relatorio = df_relatorio.sort_values(by=existing_sort_cols, ascending=sort_ascending)
                logger.debug(f"Relatório ordenado por: {existing_sort_cols}.")
            else:
                logger.warning(f"Colunas para ordenação '{sort_cols}' não encontradas no relatório final. Ordenação ignorada.")


        # 6. Salvar o Relatório
        os.makedirs(CAMINHO_RELATORIOS, exist_ok=True)
        df_relatorio.to_excel(caminho_saida_relatorio, index=False)
        logger.info(f"Relatório salvo com sucesso em: {caminho_saida_relatorio}")

        return caminho_saida_relatorio

    except ValueError as e:
        logger.error(f"Erro de dados ao gerar o relatório '{nome_relatorio_yaml}': {e}", exc_info=True)
        # return None # Poderia retornar None para indicar falha, mas raise é mais robusto para erros críticos
        raise
    except KeyError as e:
        logger.error(f"Erro: Coluna essencial faltando ou erro de definição no YAML para '{nome_relatorio_yaml}': {e}", exc_info=True)
        # return None
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao gerar ou salvar o relatório '{nome_relatorio_yaml}': {e}", exc_info=True)
        # return None
        raise
    