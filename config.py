from datetime import datetime

# URLs para download
DEMONSTRACOES_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
OPERADORAS_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/"

# Configurações gerais
PASTA_DOWNLOAD = "downloads"  # Diretório base para armazenar os arquivos baixados
MAX_WORKERS = 4  # Número de downloads simultâneos

# Anos para filtrar os arquivos de demonstrações contábeis
ANO_ATUAL = datetime.now().year
ANOS = [ANO_ATUAL - 1, ANO_ATUAL - 2]

# Configuração para o banco de dados MySQL
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "teste_banco_dados_db"
DB_USER = "mysql"
DB_PASSWORD = "admin"
