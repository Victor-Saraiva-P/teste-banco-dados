import os
import logging
import shutil


def limpar_pasta_download(pasta: str):
    """
    Remove a pasta de downloads se existir e a recria.
    """
    if os.path.exists(pasta):
        shutil.rmtree(pasta)
        logging.info(f"Pasta '{pasta}' limpa com sucesso.")
    os.makedirs(pasta)
    logging.info(f"Pasta '{pasta}' criada.")
