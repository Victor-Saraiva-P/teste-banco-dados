import logging
import os
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup

from config import MAX_WORKERS


def obter_sopa(url: str) -> BeautifulSoup:
    resposta = requests.get(url)
    resposta.raise_for_status()
    return BeautifulSoup(resposta.text, "html.parser")


def obter_links_arquivos(url: str, extensao_arquivo: str) -> list:
    sopa = obter_sopa(url)
    links = []
    for a in sopa.find_all("a", href=True):
        href = a["href"]
        if href.lower().endswith(extensao_arquivo):
            url_completa = url.rstrip("/") + "/" + href
            links.append(url_completa)
    return links


def baixar_arquivo(url: str, pasta_destino: str) -> str:
    nome_arquivo_local = os.path.join(pasta_destino, url.split("/")[-1])
    logging.info(f"Baixando {url} para {nome_arquivo_local}")
    resposta = requests.get(url, stream=True)
    resposta.raise_for_status()
    with open(nome_arquivo_local, 'wb') as f:
        for bloco in resposta.iter_content(chunk_size=8192):
            if bloco:
                f.write(bloco)

    # Se for um arquivo ZIP, extrai seu conteúdo e remove o arquivo ZIP
    if nome_arquivo_local.lower().endswith(".zip"):
        logging.info(f"Extraindo o conteúdo de {nome_arquivo_local}")
        try:
            with zipfile.ZipFile(nome_arquivo_local, 'r') as zip_ref:
                zip_ref.extractall(pasta_destino)
            os.remove(nome_arquivo_local)
            logging.info(f"Extração concluída e arquivo zip removido: {nome_arquivo_local}")
            return pasta_destino
        except zipfile.BadZipFile as erro:
            logging.error(f"Erro ao extrair {nome_arquivo_local}: {erro}")
            raise
    return nome_arquivo_local


def baixar_arquivos_concorrentes(urls: list, pasta_destino: str):
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futuros = {executor.submit(baixar_arquivo, url, pasta_destino): url for url in urls}
        for futuro in as_completed(futuros):
            url = futuros[futuro]
            try:
                resultado = futuro.result()
                logging.info(f"Download concluído: {resultado}")
            except Exception as erro:
                logging.error(f"Erro ao baixar {url}: {erro}")


def baixar_demonstracoes(url_base: str, pasta_destino: str, anos: list):
    """
    Itera sobre os anos definidos, constrói a URL específica para cada ano e baixa os arquivos ZIP
    (extraindo seu conteúdo) para a pasta correspondente.
    """
    for ano in anos:
        url_ano = f"{url_base.rstrip('/')}/{ano}/"
        logging.info(f"Buscando arquivos para o ano {ano} na URL: {url_ano}")
        links_zip = obter_links_arquivos(url_ano, ".zip")
        logging.info(f"Foram encontrados {len(links_zip)} arquivos ZIP para o ano {ano}.")

        if links_zip:
            # Cria uma subpasta para o ano, se não existir
            pasta_ano = os.path.join(pasta_destino, str(ano))
            if not os.path.exists(pasta_ano):
                os.makedirs(pasta_ano)
            baixar_arquivos_concorrentes(links_zip, pasta_ano)
        else:
            logging.warning(f"Nenhum arquivo ZIP encontrado para o ano {ano}.")


def baixar_operadoras_csv(url_base: str, pasta_destino: str):
    logging.info(f"Buscando arquivos CSV na URL: {url_base}")
    links_csv = obter_links_arquivos(url_base, ".csv")
    logging.info(f"Foram encontrados {len(links_csv)} arquivos CSV.")

    if links_csv:
        baixar_arquivos_concorrentes(links_csv, pasta_destino)
    else:
        logging.warning("Nenhum arquivo CSV encontrado.")
