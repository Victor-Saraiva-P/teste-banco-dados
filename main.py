import logging
import os

from analise import top_dez_operadoras
from cleaner import limpar_pasta_download
from config import DEMONSTRACOES_URL, OPERADORAS_URL, PASTA_DOWNLOAD, ANOS
from db_setup import criar_tabelas
from downloader import baixar_demonstracoes, baixar_operadoras_csv
from load_data import carregar_dados


def main():
    # Configurações de logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Criação das tabelas no banco de dados
    logging.info("Criando as tabelas no banco de dados...")
    criar_tabelas()

    # Limpa a pasta de downloads a cada execução
    limpar_pasta_download(PASTA_DOWNLOAD)

    # Pasta de demonstrações contábeis
    pasta_demonstracoes = os.path.join(PASTA_DOWNLOAD, "demonstracoes_contabeis")
    os.makedirs(pasta_demonstracoes, exist_ok=True)

    logging.info("Iniciando o download dos arquivos de demonstrações contábeis...")

    # Baixar as demonstrações contábeis
    baixar_demonstracoes(DEMONSTRACOES_URL, pasta_demonstracoes, ANOS)

    # Pasta de operadoras
    pasta_operadoras = os.path.join(PASTA_DOWNLOAD, "operadoras")
    os.makedirs(pasta_operadoras, exist_ok=True)

    logging.info("Iniciando o download dos arquivos de operadoras...")

    # Baixar os arquivos CSV das operadoras
    baixar_operadoras_csv(OPERADORAS_URL, pasta_operadoras)

    # Carrega os dados dos CSVs para as tabelas no banco de dados
    carregar_dados()

    # Executa a análise após carregar os dados
    top_dez_operadoras()

if __name__ == "__main__":
    main()
