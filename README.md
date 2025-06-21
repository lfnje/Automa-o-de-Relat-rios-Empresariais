# Automação de Relatórios Empresariais em Python

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📊 Visão Geral do Projeto

Este projeto Python oferece uma solução robusta e dinâmica para a automação da geração e envio de relatórios empresariais. Utilizando `pandas` para manipulação de dados e configurações definidas em arquivos YAML, ele permite gerar diversos tipos de relatórios a partir de fontes de dados Excel, realizar operações como junções (merges), agrupamentos e agregações, e enviá-los automaticamente por e-mail, inclusive consolidando múltiplos relatórios em um único anexo.

**Principais funcionalidades:**
- Carregamento e padronização dinâmicos de dados de arquivos Excel.
- Geração de relatórios customizáveis via definições YAML.
- Suporte a junções de DataFrames (`pd.merge`) e operações de agrupamento/agregação (`groupby().agg()`).
- Envio automatizado de relatórios por e-mail, com anexos dinâmicos.
- Opção para consolidar múltiplos relatórios em um único e-mail.
- Configurações centralizadas para fácil gerenciamento (credenciais, diretórios, destinatários).
- Logging detalhado para monitoramento e depuração.

## 🚀 Como Começar

Siga estes passos para configurar e executar o projeto em sua máquina local.

### Pré-requisitos

Certifique-se de ter o Python instalado (versão 3.8 ou superior).

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SeuUsuario/NomeDoSeuRepositorio.git](https://github.com/SeuUsuario/NomeDoSeuRepositorio.git)
    cd NomeDoSeuRepositorio
    ```
    (Lembre-se de substituir `SeuUsuario/NomeDoSeuRepositorio` pelo caminho real do seu repositório no GitHub.)

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    (Certifique-se de ter um arquivo `requirements.txt` com `pandas`, `PyYAML`, `openpyxl` - se não tiver, crie-o com `pip freeze > requirements.txt` após instalar essas libs.)

### Configuração Inicial

1.  **Crie os diretórios necessários:**
    O script possui uma função `ensure_directories_exist()` (em `utils.py`) que cria automaticamente as pastas `data`, `relatorios` e `logs` se elas não existirem.

2.  **Configure o arquivo `config.py`:**
    Este arquivo armazena as configurações globais do projeto. Edite-o com suas informações.

    ```python
    # Automação de Relatórios Empresariais/config.py

    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # --- Configurações de E-mail ---
    EMAIL_REMETENTE = "seu_email@gmail.com"  # Seu e-mail (Gmail é recomendado para SMTP_SSL)
    SENHA_APP = "SUA_SENHA_DE_APP_AQUI"      # Senha de aplicativo do Gmail (NÃO a senha da sua conta)
                                             # Veja como gerar: [https://support.google.com/accounts/answer/185833](https://support.google.com/accounts/answer/185833)

    EMAIL_DESTINATARIOS = ["destino1@exemplo.com", "destino2@exemplo.com"] # Lista de destinatários padrão

    EMAIL_ASSUNTO_PADRAO = "Relatório Automatizado - {{periodo_extenso}}" # Assunto padrão
    EMAIL_CORPO_PADRAO = """
    Prezados(as),

    Segue em anexo o relatório automatizado referente a {{periodo_extenso}}.
    Esperamos que seja útil para sua análise.

    Atenciosamente,
    Equipe de Automação
    """

    # --- Caminhos de Diretórios ---
    CAMINHO_DADOS = os.path.join(BASE_DIR, 'data')
    CAMINHO_RELATORIOS = os.path.join(BASE_DIR, 'relatorios')
    CAMINHO_LOGS = os.path.join(BASE_DIR, 'logs')
    CAMINHO_DEFINICOES_RELATORIOS = os.path.join(BASE_DIR, 'config_reports', 'report_definitions.yaml')

    # --- Configurações de Logging ---
    LOG_FILE = os.path.join(CAMINHO_LOGS, 'automacao_relatorios.log')
    LOG_LEVEL = 'INFO' # DEBUG, INFO, WARNING, ERROR, CRITICAL
    ```

    **Importante:** Para `SENHA_APP` do Gmail, você precisa gerar uma "senha de app". Não use a senha principal da sua conta Google. Pesquise por "gerar senha de app Gmail" para mais informações.

3.  **Prepare os dados de entrada:**
    Coloque seus arquivos de dados (e.g., `transacoes_AAAA_MM.xlsx`, `cadastros_AAAA_MM.xlsx`) na pasta `data/`. O script espera o formato `nome_do_arquivo_ANO_MES.xlsx`. Ex: `transacoes_2025_01.xlsx`.

4.  **Defina seus relatórios em `config_reports/report_definitions.yaml`:**
    Este é o coração da customização. Você define a estrutura de cada relatório, suas fontes de dados, junções, agrupamentos, agregações e as colunas de saída.

    Exemplo de `report_definitions.yaml`:
    ```yaml
    # Caminho: Automação de Relatórios Empresariais/config_reports/report_definitions.yaml

    vendas_por_cliente:
      descricao: "Relatório gerencial de vendas agrupado por cliente."
      fontes_dados:
        - nome: "transacoes"
        - nome: "cadastros"
      juncoes:
        - esquerdo: "transacoes"
          direito: "cadastros"
          on: "cliente"
          how: "left"
      processamento_relatorio:
        agrupar_por: ["cliente", "nome_completo"]
        agregacoes:
          valor_total:
            coluna_origem: "valor"
            funcao: "sum"
      colunas_saida:
        - "cliente"
        - "nome_completo"
        - "segmento"
        - "valor_total"

    detalhes_das_transacoes:
      descricao: "Relatório detalhado de todas as transações."
      fontes_dados:
        - nome: "transacoes"
      processamento_relatorio:
        # Nenhuma agregação ou agrupamento para um relatório detalhado
        # filtros: # Exemplo de filtro
        #   - coluna: "valor"
        #     operador: ">"
        #     valor: 500
      colunas_saida:
        - "cliente"
        - "data"
        - "valor"
        - "produto"
        - "quantidade"
    ```
    **Lembre-se:** A indentação em arquivos YAML é crucial. Use espaços (geralmente 2 ou 4) e seja consistente.

## 🏃 Como Executar

Após a configuração, execute o script principal:

```bash
python main.py

<p align="center">
  <em>“A tecnologia não só resolve problemas, como também cria oportunidades.”</em><br>
  <strong>Luiz Filipe Nogueira</strong>
</p>
