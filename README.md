![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
# Teste de banco de dados

Este projeto é um sistema de processamento de dados que extrai, armazena e analisa dados financeiros de operadoras de planos de saúde do Brasil. Utilizando a base de dados abertos da ANS (Agência Nacional de Saúde Suplementar), o sistema permite identificar as operadoras com maiores despesas em categorias específicas por períodos de tempo.
## Stack Utilizada

- **Linguagem:** Python 3
- **Banco de Dados:** MySQL
- **Bibliotecas principais:**
  - `requests` e `beautifulsoup4` – Para download e extração dos dados
  - `pandas` – Processamento e análise de dados
  - `mysql-connector-python` – Conexão com o banco de dados
  - `sqlalchemy` – ORM para consultas ao banco de dados
## Funcionalidades

- **Download Automático de Dados:** Baixa automaticamente as demonstrações contábeis e dados de operadoras diretamente do site da ANS.
- **Extração de Arquivos:** Extrai arquivos ZIP baixados e processa os CSVs contidos.
- **Configuração de Banco de Dados:** Cria e configura automaticamente o esquema do banco de dados.
- **Carregamento de Dados:** Importa os dados dos CSVs para as tabelas do MySQL.
- **Análise Financeira:** Realiza análises sobre as despesas das operadoras:
  - Top 10 operadoras com maiores despesas em uma categoria específica no último trimestre
  - Top 10 operadoras com maiores despesas em uma categoria específica no último ano
  ## Estrutura do Projeto

```
teste-banco-dados/
├── app/
│   ├── analysis/                # Módulos de análise de dados
│   │   └── analise.py           # Funções para análises financeiras
│   ├── data/                    # Processamento de dados
│   │   ├── cleaner.py           # Limpeza de diretórios
│   │   ├── downloader.py        # Download de arquivos
│   │   └── load_data.py         # Carregamento de dados para o banco
│   ├── database/                # Configuração de banco de dados
│   │   ├── db_setup.py          # Criação de tabelas
│   │   ├── sql_util.py          # Utilidades para SQL
│   │   └── scripts_sql/         # Consultas SQL
│   └── config.py                # Configurações gerais
├── main.py                      # Ponto de entrada da aplicação
└── requirements.txt             # Dependências Python
```
## Como Executar

1. **Clone o Repositório:**

```bash
git clone https://github.com/Victor-Saraiva-P/teste-api
```

2. **Configure o Ambiente Python:**

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
```

3. **Suba o ambiente com Docker (MySQL):**

Certifique-se de que você tem o Docker instalado. Em seguida, execute:

```bash
docker-compose up -d
```

Isso iniciará um contêiner com o MySQL configurado.


4. **Execute a Aplicação:**

```bash
python main.py
```

O sistema irá:

- Criar as tabelas necessárias
- Baixar os dados da ANS
- Processar e carregar os dados no banco
- Executar as análises

## Resultados

Ao final do processamento, o programa exibirá:

- Top 10 operadoras com maiores despesas na categoria configurada no último trimestre
- Top 10 operadoras com maiores despesas na categoria configurada no último ano

## Parâmetros Configuráveis

No arquivo `config.py`, é possível modificar:

- Período de análise (trimestre/ano)
- Categoria financeira analisada
- Configurações de conexão com o banco de dados
- Anos a serem considerados nos downloads

## 👨‍💻 Autor

Desenvolvido por **[Victor Saraiva](https://github.com/Victor-Saraiva-P)**
