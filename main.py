import os
import logging

from cleaner import limpar_pasta_download
from downloader import baixar_demonstracoes, baixar_operadoras_csv
from config import DEMONSTRACOES_URL, OPERADORAS_URL, PASTA_DOWNLOAD, ANOS



def main():
    # Configurações de logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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


if __name__ == "__main__":
    main()
