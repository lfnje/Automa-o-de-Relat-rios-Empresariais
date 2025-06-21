# 🚀 Solução de Automação de Relatórios Empresariais em Python 📊

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.co/badge/License-MIT-green.svg)

## Prezado(a) Diretor(a) / Gestor(a),

Tenho o prazer de apresentar nossa solução desenvolvida em Python para a automação completa da geração e distribuição de relatórios empresariais. Este projeto representa um avanço significativo em nossa capacidade de fornecer informações estratégicas de forma rápida, precisa e eficiente.

Com base em um desenvolvimento focado na robustez e flexibilidade, esta ferramenta elimina a necessidade de processos manuais demorados e suscetíveis a erros. Ela otimiza o fluxo de trabalho, garantindo que os relatórios cheguem às mãos certas, no momento certo, impulsionando a tomada de decisões baseada em dados.

**Esta solução oferece valor estratégico através de:**
- **Otimização Operacional:** Automatiza a extração, transformação e carregamento de dados (ETL) de planilhas Excel, liberando sua equipe para tarefas de maior valor agregado.
- **Inteligência de Negócios Aprimorada:** Gera relatórios customizáveis e precisos, configurados via arquivos YAML intuitivos, que podem incluir desde análises de vendas por cliente até detalhes de transações.
- **Eficiência na Distribuição:** Garante que os relatórios cheguem automaticamente aos stakeholders relevantes via e-mail, com a capacidade aprimorada de consolidar múltiplos anexos em uma única mensagem, simplificando a gestão da informação.
- **Redução de Riscos:** Minimiza erros humanos através de um processo padronizado e automatizado, com logs detalhados para auditoria e monitoramento de desempenho.
- **Escalabilidade e Flexibilidade:** A arquitetura modular permite fácil adaptação a novas fontes de dados, requisitos de relatórios ou formatos de saída, assegurando a longevidade do investimento.

## 🚀 Implementação e Execução

Para integrar esta solução em nosso ambiente e iniciar a geração automatizada de relatórios, os passos são simples e diretos.

### Pré-requisitos Técnicos

A solução exige a presença do **Python (versão 3.8 ou superior)** em seu ambiente de execução.

### Instalação (Para a Equipe Técnica)

1.  **Obtenção do Código:**
    ```bash
    git clone [https://github.com/SeuUsuario/NomeDoSeuRepositorio.git](https://github.com/SeuUsuario/NomeDoSeuRepositorio.git)
    cd NomeDoSeuRepositorio
    ```
    *(Por favor, substitua `SeuUsuario/NomeDoSeuRepositorio` pelo caminho real do nosso repositório no GitHub.)*

2.  **Ambiente Controlado:**
    Recomenda-se a criação e ativação de um ambiente virtual para gerenciar as dependências do projeto de forma isolada:
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instalação das Dependências:**
    Todas as bibliotecas necessárias podem ser instaladas via `pip`:
    ```bash
    pip install -r requirements.txt
    ```
    *(Caso o `requirements.txt` precise ser gerado, utilize `pip freeze > requirements.txt` após instalar `pandas`, `PyYAML`, `openpyxl` e outras bibliotecas utilizadas.)*

### Configuração Inicial (Para o Administrador da Solução)

1.  **Estrutura de Diretórios:**
    A solução é auto-suficiente na criação da estrutura de pastas. A função `ensure_directories_exist()` (localizada em `utils.py`) garante a criação automática das pastas `data`, `relatorios` e `logs` conforme necessário.

2.  **Configuração do `config.py`:**
    Este arquivo centraliza todas as configurações essenciais para o funcionamento da automação. Edite `Automação de Relatórios Empresariais/config.py` com as informações pertinentes à nossa operação:

    ```python
    # Automação de Relatórios Empresariais/config.py

    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # --- Credenciais e Destinatários de E-mail ---
    EMAIL_REMETENTE = "seu_email_corporativo@dominio.com"  # O e-mail de onde os relatórios serão enviados
    SENHA_APP = "SUA_SENHA_DE_APP_AQUI"                    # Importante: Para Gmail, utilize uma "senha de app" gerada pelo Google.
                                                           # Isso garante a segurança de nossa conta principal.
                                                           # Para outros provedores, utilize a senha de acesso SMTP fornecida.

    EMAIL_DESTINATARIOS = ["analista1@dominio.com", "gestor@dominio.com"] # Lista de e-mails para o envio padrão consolidado

    EMAIL_ASSUNTO_PADRAO = "Relatórios Gerenciais Consolidados - {{periodo_extenso}}" # Assunto padrão para os e-mails
    EMAIL_CORPO_PADRAO = """
    Prezados(as) Colegas,

    Seguem em anexo os relatórios gerenciais consolidados para o período de **{{periodo_extenso}}**.
    Estas informações são cruciais para nossa análise e planejamento estratégico.

    Atenciosamente,
    Equipe de Automação de Dados
    """

    # --- Definição dos Caminhos de Dados e Saída ---
    CAMINHO_DADOS = os.path.join(BASE_DIR, 'data')
    CAMINHO_RELATORIOS = os.path.join(BASE_DIR, 'relatorios')
    CAMINHO_LOGS = os.path.join(BASE_DIR, 'logs')
    CAMINHO_DEFINICOES_RELATORIOS = os.path.join(BASE_DIR, 'config_reports', 'report_definitions.yaml')

    # --- Nível de Detalhe do Registro (Logging) ---
    LOG_FILE = os.path.join(CAMINHO_LOGS, 'automacao_relatorios.log')
    LOG_LEVEL = 'INFO' # Recomendado para ambientes de produção. Altere para 'DEBUG' para depuração.
    ```

3.  **Provisão de Dados de Entrada:**
    Os arquivos de dados (ex: `transacoes_AAAA_MM.xlsx`, `cadastros_AAAA_MM.xlsx`) devem ser alocados na pasta `data/`. A solução foi desenhada para carregar arquivos seguindo o padrão de nomeação `nome_do_arquivo_ANO_MES.xlsx`.

4.  **Definição dos Relatórios em `config_reports/report_definitions.yaml`:**
    Este arquivo é a base para a criação dos relatórios. Cada seção define um relatório específico, incluindo suas fontes de dados, regras de junção, agrupamento, agregação e as colunas a serem apresentadas. A clareza e precisão na indentação YAML são vitais para o correto processamento.

    Exemplo da estrutura (para referência):
    ```yaml
    # Exemplo: Automação de Relatórios Empresariais/config_reports/report_definitions.yaml

    # Exemplo de Relatório: Vendas Consolidado por Cliente
    vendas_por_cliente:
      descricao: "Relatório gerencial de vendas consolidado por cliente."
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

    # Exemplo de Relatório: Detalhes Operacionais das Transações
    detalhes_das_transacoes:
      descricao: "Relatório detalhado de todas as transações, para auditoria e análise individual."
      fontes_dados:
        - nome: "transacoes"
      colunas_saida:
        - "cliente"
        - "data"
        - "valor"
        - "produto"
        - "quantidade"
    ```

## 🏃 Como Operar a Solução

Com todas as configurações em vigor, basta executar o script principal:

```bash
python main.py

<p align="center">
  <em>“A tecnologia não só resolve problemas, como também cria oportunidades.”</em><br>
  <strong>Luiz Filipe Nogueira</strong>
</p>
