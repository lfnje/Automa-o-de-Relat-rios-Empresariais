# 🚀 Automação de Relatórios Empresariais em Python 

---

## 🎯 Sobre Esta Solução

Este projeto representa uma **solução estratégica e robusta para a automação de relatórios empresariais**, desenvolvida em Python. Meu principal objetivo com esta ferramenta é **otimizar e agilizar o processo de coleta, transformação e distribuição de dados**, fornecendo insights cruciais para a tomada de decisões de forma consistente e eficiente.
Como Analista e Desenvolvedor de Sistemas em formação, apliquei neste projeto, conhecimentos aprofundados em engenharia de dados e automação, focando em entregar um sistema que não apenas gere relatórios, mas que o faça de maneira **inteligente, escalável e com mínima intervenção manual**.

---

## 💻 Tecnologias Utilizadas

A robustez e flexibilidade desta solução são garantidas pela escolha criteriosa das seguintes tecnologias:

* **Python (3.8+):** A linguagem base para toda a lógica de automação e processamento.
* **Pandas:** Essencial para a **manipulação eficiente de grandes volumes de dados**, permitindo operações complexas como junções (`merge`), agrupamentos (`groupby`) e agregações (`sum`, `mean`, etc.).
* **PyYAML:** Habilita a **configuração dinâmica dos relatórios** através de arquivos YAML. Isso significa que podemos criar e modificar relatórios facilmente, sem alterar o código principal.
* **`smtplib` e `email` (Módulos Nativos do Python):** Utilizados para garantir a **entrega segura e eficaz dos relatórios por e-mail**, com suporte avançado para múltiplos anexos em uma única mensagem.
* **`openpyxl`:** Fundamental para a **interação com arquivos Excel (.xlsx)**, tanto para leitura dos dados de entrada quanto para a gravação dos relatórios gerados.

---

## ✨ Funcionalidades Estratégicas

Desenvolvemos um conjunto de funcionalidades chave para garantir o máximo valor e eficiência:

* **Processamento de Dados Automatizado:** O sistema é capaz de carregar e padronizar dados de diversas fontes Excel de forma dinâmica, preparando-os para análise sem intervenção manual.
* **Geração de Relatórios Configurável (via YAML):** A flexibilidade é um pilar. Podemos definir novos relatórios, suas fontes de dados, regras de junção, agrupamentos e colunas de saída diretamente em arquivos YAML, tornando a solução altamente adaptável às necessidades de negócio.
* **Consolidação de Relatórios em um Único E-mail:** Um avanço significativo! Múltiplos relatórios podem ser gerados e enviados em um único e-mail, organizando a comunicação e garantindo que os destinatários recebam todas as informações relevantes de uma só vez.
* **Envio de E-mail Seguro e Personalizado:** As configurações de e-mail (remetente, destinatários, assunto, corpo) são centralizadas e suportam substituições dinâmicas de data, garantindo comunicação profissional e relevante.
* **Gerenciamento Automático de Diretórios:** A solução cuida da criação e organização das pastas de dados, relatórios e logs, garantindo um ambiente de trabalho limpo e funcional.
* **Logging Detalhado:** Todas as operações são registradas em logs completos, o que facilita o monitoramento, a auditoria e a rápida identificação de qualquer anomalia.

---

## 🚀 Como Implementar e Operar

Para sua equipe técnica ou para iniciar a operação desta solução:

### Configuração de Ambiente

1.  **Clone o Repositório:** Obtenha a base do código da solução.
    ```bash
    git clone [https://github.com/lfnje/Automa-o-de-Relat-rios-Empresariais.git](https://github.com/lfnje/Automa-o-de-Relat-rios-Empresariais.git)
    cd Automa-o-de-Relat-rios-Empresariais
    ```
    *(Por favor, atualize `SeuUsuario/NomeDoSeuRepositorio` com o caminho real do nosso projeto.)*

2.  **Ambiente Virtual:** (Recomendado) Crie e ative um ambiente virtual para isolar as dependências do projeto.
    ```bash
    python -m venv venv
    # No Windows: .\venv\Scripts\activate
    # No macOS/Linux: source venv/bin/activate
    ```

3.  **Instale as Dependências:** As bibliotecas necessárias estão listadas em `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
    
---
### Estrutura da Solução

<p align="center">
  <img src="img/Estrutura de Solução.png" alt="Estrutura de Solução para Automação" style="width:75%; max-width:600px;">
</p>

---

### Ajustes Essenciais

1.  **`config.py`:** Edite este arquivo para definir as credenciais de e-mail (utilize uma **Senha de Aplicativo** para maior segurança com o Gmail), os destinatários padrão e os caminhos dos diretórios.
2.  **`data/`:** Posicione seus arquivos Excel de dados (`transacoes_AAAA_MM.xlsx`, `cadastros_AAAA_MM.xlsx`, etc.) nesta pasta, seguindo o padrão `nome_ANO_MES.xlsx`.
3.  **`config_reports/report_definitions.yaml`:** Personalize as definições de cada relatório aqui. Você pode criar novos relatórios, ajustar colunas, agrupamentos e filtros de acordo com as necessidades específicas de negócio.

### Próximos Passos: Tudo Pronto para a Ação!

Com as configurações ajustadas e seus dados organizados, a solução está configurada e pronta para iniciar suas operações. Agora, você pode prosseguir para a seção de "Execução" para ver a automação em funcionamento e começar a gerar seus relatórios de forma eficiente.

### Execução

Após a configuração, a operação é simples:

```bash
python main.py
```

Esta solução pode ser facilmente executada a partir do seu terminal integrado ou de qualquer outro ambiente onde o Python esteja configurado, proporcionando flexibilidade na implementação.

---

## 📜 Licença

Este projeto possui todos os direitos reservados, sendo proibida a reprodução, modificação ou distribuição de seu código e conteúdo sem a prévia autorização por escrito de [Luiz Filipe Nogueira]. Para qualquer uso ou esclarecimento, por favor, entre em contato. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🤝 Colaboração e Suporte

Incentivamos a colaboração e o feedback para a melhoria contínua desta solução. Para sugestões, reportar um comportamento inesperado ou propor novas funcionalidades, por favor, **não hesite em entrar em contato através das redes abaixo:**

* **LinkedIn:** [linkedin.com/in/luizfilipenogueira](https://www.linkedin.com/in/luizfilipenogueira/)
* **Email:** [lfnjecorporativo@gmail.com](mailto:lfnjecorporativo@gmail.com)
* **Instagram:** [instagram.com/_lfnje/](https://www.instagram.com/_lfnje/)

---

<p align="center">
  <em>“A tecnologia não só resolve problemas, como também cria oportunidades.”</em><br>
  <strong>Luiz Filipe Nogueira</strong>
</p>
