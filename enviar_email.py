# Caminho: Automação de Relatórios Empresariais/enviar_email.py

import smtplib
from email.message import EmailMessage
import os
import logging
from config import (
    EMAIL_REMETENTE, SENHA_APP, EMAIL_DESTINATARIOS,
    EMAIL_ASSUNTO_PADRAO, EMAIL_CORPO_PADRAO
)
import datetime

logger = logging.getLogger(__name__)

def enviar_email_relatorio(
    caminho_arquivo: str,
    definicao_email: dict,
    destinatarios_globais: list = None,
    data_referencia_relatorio: datetime.date = None
) -> None:
    """
    Envia o relatório gerado por e-mail com anexo, com assunto e corpo dinâmicos.
    Esta função é projetada para enviar um ÚNICO anexo por e-mail.
    
    Parâmetros:
        caminho_arquivo (str): O caminho completo para o arquivo do relatório a ser anexado.
        definicao_email (dict): Dicionário com configurações de e-mail específicas para este relatório (assunto, corpo, destinatarios).
        destinatarios_globais (list, optional): Lista de e-mails de destinatários globais (do config.py). Usado se 'destinatarios' não estiver em definicao_email.
        data_referencia_relatorio (datetime.date, optional): Data de referência para substituição de placeholders no assunto/corpo.
    """
    if not os.path.exists(caminho_arquivo):
        logger.error(f"Erro: Arquivo para anexar não encontrado: {caminho_arquivo}", exc_info=True)
        raise FileNotFoundError(f"Arquivo de relatório não encontrado: {caminho_arquivo}")

    try:
        # Prioriza destinatários definidos no YAML do relatório, senão usa os globais do config.py
        destinatarios_finais = definicao_email.get('destinatarios')
        if not destinatarios_finais:
            destinatarios_finais = destinatarios_globais if destinatarios_globais is not None else EMAIL_DESTINATARIOS
        
        if not destinatarios_finais:
            logger.warning("Nenhum destinatário definido para o e-mail (nem no YAML, nem globalmente). Pulando envio.")
            return

        logger.info(f"Iniciando envio do e-mail para {', '.join(destinatarios_finais)}...")

        # --- Substituição de Placeholders no Assunto e Corpo ---
        data_para_placeholders = data_referencia_relatorio if data_referencia_relatorio else datetime.date.today()

        mes_ano_str = data_para_placeholders.strftime('%Y_%m')
        periodo_extenso = data_para_placeholders.strftime('%B de %Y')
        dia_mes_ano = data_para_placeholders.strftime('%d/%m/%Y')

        assunto_template = definicao_email.get('assunto', EMAIL_ASSUNTO_PADRAO)
        corpo_template = definicao_email.get('corpo', EMAIL_CORPO_PADRAO)

        assunto_final = assunto_template.replace('{{mes_ano}}', mes_ano_str).replace('{{periodo_extenso}}', periodo_extenso).replace('{{dia_mes_ano}}', dia_mes_ano)
        corpo_final = corpo_template.replace('{{mes_ano}}', mes_ano_str).replace('{{periodo_extenso}}', periodo_extenso).replace('{{dia_mes_ano}}', dia_mes_ano)
        
        corpo_final = corpo_final.replace('[Seu Nome ou Equipe de Automação]', 'Equipe de Automação')
        corpo_final = corpo_final.replace('[Destinatários]', ', '.join(destinatarios_finais))


        msg = EmailMessage()
        msg['Subject'] = assunto_final
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = ', '.join(destinatarios_finais)
        msg.set_content(corpo_final)

        nome_arquivo = os.path.basename(caminho_arquivo)
        with open(caminho_arquivo, 'rb') as f:
            conteudo = f.read()
        msg.add_attachment(conteudo, maintype='application', subtype='octet-stream', filename=nome_arquivo)
        logger.info(f"Arquivo '{nome_arquivo}' anexado ao e-mail.")

        logger.info("Conectando ao servidor SMTP do Gmail...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_REMETENTE, SENHA_APP)
            logger.info("Login SMTP bem-sucedido.")
            smtp.send_message(msg)
        logger.info("E-mail enviado com sucesso!")

    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"Erro de autenticação SMTP. Verifique seu EMAIL_REMETENTE e SENHA_APP. Detalhes: {e}", exc_info=True)
        raise
    except smtplib.SMTPServerDisconnected as e:
        logger.error(f"Erro de conexão com o servidor SMTP. Servidor desconectado inesperadamente. Detalhes: {e}", exc_info=True)
        raise
    except smtplib.SMTPException as e:
        logger.error(f"Erro SMTP geral ao enviar e-mail: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao enviar e-mail: {e}", exc_info=True)
        raise

# --- NOVA FUNÇÃO PARA ENVIAR MÚLTIPLOS ANEXOS ---
def enviar_email_com_multiplos_anexos(
    caminhos_arquivos: list[str],
    assunto: str,
    corpo: str,
    destinatarios: list[str],
    data_referencia_relatorio: datetime.date = None
) -> None:
    """
    Envia um e-mail com múltiplos arquivos anexados.
    
    Parâmetros:
        caminhos_arquivos (list[str]): Uma lista de caminhos completos para os arquivos a serem anexados.
        assunto (str): O assunto do e-mail. Pode conter placeholders como {{periodo_extenso}}.
        corpo (str): O corpo do e-mail. Pode conter placeholders como {{periodo_extenso}}.
        destinatarios (list[str]): Uma lista de e-mails de destinatários.
        data_referencia_relatorio (datetime.date, optional): Data de referência para substituição de placeholders.
    """
    if not caminhos_arquivos:
        logger.warning("Nenhum arquivo especificado para anexar. Pulando envio de e-mail com múltiplos anexos.")
        return

    if not destinatarios:
        logger.warning("Nenhum destinatário definido para o e-mail com múltiplos anexos. Pulando envio.")
        return

    logger.info(f"Iniciando envio do e-mail com múltiplos anexos para {', '.join(destinatarios)}...")

    # --- Substituição de Placeholders no Assunto e Corpo ---
    data_para_placeholders = data_referencia_relatorio if data_referencia_relatorio else datetime.date.today()
    mes_ano_str = data_para_placeholders.strftime('%Y_%m')
    periodo_extenso = data_para_placeholders.strftime('%B de %Y')
    dia_mes_ano = data_para_placeholders.strftime('%d/%m/%Y')

    assunto_final = assunto.replace('{{mes_ano}}', mes_ano_str).replace('{{periodo_extenso}}', periodo_extenso).replace('{{dia_mes_ano}}', dia_mes_ano)
    corpo_final = corpo.replace('{{mes_ano}}', mes_ano_str).replace('{{periodo_extenso}}', periodo_extenso).replace('{{dia_mes_ano}}', dia_mes_ano)
    
    corpo_final = corpo_final.replace('[Seu Nome ou Equipe de Automação]', 'Equipe de Automação')
    corpo_final = corpo_final.replace('[Destinatários]', ', '.join(destinatarios))


    msg = EmailMessage()
    msg['Subject'] = assunto_final
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = ', '.join(destinatarios)
    msg.set_content(corpo_final)

    for caminho_arquivo in caminhos_arquivos:
        if not os.path.exists(caminho_arquivo):
            logger.warning(f"Arquivo para anexar não encontrado: {caminho_arquivo}. Ignorando este anexo.")
            continue
        
        nome_arquivo = os.path.basename(caminho_arquivo)
        try:
            with open(caminho_arquivo, 'rb') as f:
                conteudo = f.read()
            msg.add_attachment(conteudo, maintype='application', subtype='octet-stream', filename=nome_arquivo)
            logger.info(f"Arquivo '{nome_arquivo}' anexado ao e-mail com múltiplos anexos.")
        except Exception as e:
            logger.error(f"Erro ao anexar arquivo '{nome_arquivo}': {e}", exc_info=True)
            continue

    if not list(msg.iter_attachments()): # Verifica se algum anexo válido foi realmente adicionado
        logger.warning("Nenhum anexo válido foi adicionado ao e-mail. Pulando envio.")
        return

    try:
        logger.info("Conectando ao servidor SMTP do Gmail para múltiplos anexos...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_REMETENTE, SENHA_APP)
            logger.info("Login SMTP bem-sucedido para múltiplos anexos.")
            smtp.send_message(msg)
        logger.info("E-mail com múltiplos anexos enviado com sucesso!")

    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"Erro de autenticação SMTP ao enviar múltiplos anexos. Verifique suas credenciais. Detalhes: {e}", exc_info=True)
        raise
    except smtplib.SMTPServerDisconnected as e:
        logger.error(f"Erro de conexão com o servidor SMTP ao enviar múltiplos anexos. Servidor desconectado inesperadamente. Detalhes: {e}", exc_info=True)
        raise
    except smtplib.SMTPException as e:
        logger.error(f"Erro SMTP geral ao enviar e-mail com múltiplos anexos: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao enviar e-mail com múltiplos anexos: {e}", exc_info=True)
        raise
    