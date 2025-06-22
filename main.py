# Caminho: Automação de Relatórios Empresariais/main.py

import os
import logging
import datetime
import yaml # Embora não usado diretamente aqui, é bom manter para contexto se houver uso futuro

import config
from utils import setup_logging, ensure_directories_exist, carregar_definicoes_relatorios
from processar_dados import carregar_dados
from gerar_relatorio import gerar_relatorio
# Importar AMBAS as funções de envio de e-mail
from enviar_email import enviar_email_relatorio, enviar_email_com_multiplos_anexos

def main():
    # 1. Configurar logging
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Iniciando automação de relatórios empresariais...")

    # 2. Verificar/criar diretórios necessários
    ensure_directories_exist()

    try:
        # 3. Carregar definições de relatórios
        definicoes_relatorios = carregar_definicoes_relatorios()

        # --- Solicitar ano e mês para processamento ---
        ano_processamento_str = input("Digite o ano para processar os relatórios (ex: 2025): ")
        mes_processamento_str = input("Digite o mês para processar os relatórios (ex: 06): ")

        try:
            ano_processamento = int(ano_processamento_str)
            mes_processamento = int(mes_processamento_str)
            # Validar mês
            if not (1 <= mes_processamento <= 12):
                raise ValueError("Mês inválido. Digite um número entre 1 e 12.")
            data_referencia = datetime.date(ano_processamento, mes_processamento, 1)
        except ValueError as e:
            logger.error(f"Erro na entrada de ano/mês: {e}. Usando o mês e ano atuais como padrão.", exc_info=True)
            data_referencia = datetime.date.today()
            ano_processamento = data_referencia.year
            mes_processamento = data_referencia.month

        logger.info(f"Processando relatórios para o mês de {mes_processamento:02d}/{ano_processamento:04d}.")

        # 4. Definir caminhos dos arquivos de entrada dinamicamente
        caminhos_arquivos_entrada = {
            'transacoes': os.path.join(config.CAMINHO_DADOS, f'transacoes_{ano_processamento:04d}_{mes_processamento:02d}.xlsx'),
            'cadastros': os.path.join(config.CAMINHO_DADOS, f'cadastros_{ano_processamento:04d}_{mes_processamento:02d}.xlsx')
        }

        # Carregar todos os DataFrames de entrada uma única vez e padronizá-los
        dataframes_carregados = carregar_dados(caminhos_arquivos_entrada)

        # Lista para armazenar os caminhos dos relatórios que serão enviados em um único e-mail
        caminhos_relatorios_para_email_unico = []

        # Iterar sobre as definições de relatórios e executá-los
        for nome_relatorio, def_relatorio in definicoes_relatorios.items():
            logger.info(f"Executando relatório: {nome_relatorio}.")
            
            # Formatar o nome do arquivo de saída de forma consistente
            # Substitui espaços por underscores e converte para minúsculas
            nome_arquivo_base = f"{nome_relatorio.replace(' ', '_').lower()}_{ano_processamento:04d}_{mes_processamento:02d}.xlsx"
            caminho_saida_relatorio = os.path.join(config.CAMINHO_RELATORIOS, nome_arquivo_base)
            
            # CHAMA gerar_relatorio COM OS DATAFRAMES CARREGADOS E A DEFINIÇÃO COMPLETA DO RELATÓRIO
            caminho_relatorio_gerado = gerar_relatorio(
                dataframes=dataframes_carregados,
                definicao_relatorio=def_relatorio,
                caminho_saida_relatorio=caminho_saida_relatorio
            )

            # Adiciona o caminho do relatório gerado à lista para envio consolidado
            if caminho_relatorio_gerado and os.path.exists(caminho_relatorio_gerado):
                caminhos_relatorios_para_email_unico.append(caminho_relatorio_gerado)
                logger.info(f"Relatório '{nome_relatorio}' adicionado à lista para envio consolidado.")
            else:
                logger.error(f"Relatório '{nome_relatorio}' não foi gerado ou o caminho de retorno está incorreto/arquivo não existe. Não será incluído no e-mail.")
            
            # --- NOTA ---
            # Se você ainda quisesse a opção de enviar e-mails individuais para ALGUNS relatórios,
            # baseando-se numa flag no YAML (ex: enviar_individualmente: true), a lógica ficaria aqui:
            #
            # if def_relatorio.get('email', {}).get('enviar_individualmente', False):
            #     email_config_para_relatorio = {
            #         'destinatarios': def_relatorio.get('email', {}).get('destinatarios'),
            #         'assunto': def_relatorio.get('email', {}).get('assunto'),
            #         'corpo': def_relatorio.get('email', {}).get('corpo')
            #     }
            #     enviar_email_relatorio(
            #         caminho_arquivo=caminho_relatorio_gerado,
            #         definicao_email=email_config_para_relatorio,
            #         destinatarios_globais=config.EMAIL_DESTINATARIOS,
            #         data_referencia_relatorio=data_referencia 
            #     )
            # else:
            #     logger.info(f"Envio de e-mail individual desabilitado para o relatório '{nome_relatorio}'.")

        # --- FIM DO LOOP DE GERAÇÃO DE RELATÓRIOS ---

        # 5. Enviar um ÚNICO E-MAIL com TODOS os relatórios gerados como anexos
        if caminhos_relatorios_para_email_unico:
            logger.info(f"Iniciando envio do e-mail consolidado com {len(caminhos_relatorios_para_email_unico)} relatórios anexados.")
            
            # Você pode definir um assunto e corpo padrão para o e-mail consolidado
            # Ou, se quiser, pode pegar de uma nova seção no seu config.py ou report_definitions.yaml
            assunto_consolidado = f"Relatórios Gerenciais Consolidados - {data_referencia.strftime('%B de %Y')}"
            corpo_consolidado = f"""
Prezados(as),

Seguem em anexo os relatórios gerenciais consolidados para o período de **{data_referencia.strftime('%B de %Y')}**.

Os relatórios incluídos são:
{'- ' + '\\n- '.join([os.path.basename(p) for p in caminhos_relatorios_para_email_unico])}

Esperamos que sejam úteis para sua análise.

Atenciosamente,

Equipe de Automação de Relatórios
"""
            # Chamar a nova função que envia múltiplos anexos
            enviar_email_com_multiplos_anexos(
                caminhos_arquivos=caminhos_relatorios_para_email_unico,
                assunto=assunto_consolidado,
                corpo=corpo_consolidado,
                destinatarios=config.EMAIL_DESTINATARIOS, # Usa os destinatários globais do config.py
                data_referencia_relatorio=data_referencia
            )
        else:
            logger.warning("Nenhum relatório válido foi gerado para envio consolidado por e-mail.")


        logger.info("Automação de relatórios concluída com sucesso!")

    except FileNotFoundError as e:
        logger.critical(f"Erro: Arquivo não encontrado. Verifique se todos os caminhos estão corretos. Detalhes: {e}", exc_info=True)
    except KeyError as e:
        logger.critical(f"Erro de estrutura de dados: Coluna essencial não encontrada ou erro na definição do YAML. Detalhes: {e}", exc_info=True)
    except ValueError as e:
        logger.critical(f"Erro de dados ou configuração inválida: {e}", exc_info=True)
    except Exception as e:
        logger.critical(f"Ocorreu um erro crítico durante a execução da automação: {e}", exc_info=True)

if __name__ == "__main__":
    main()
