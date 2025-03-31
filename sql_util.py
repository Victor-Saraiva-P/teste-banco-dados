import os


def ler_sql_arquivo(nome_arquivo):
    """
    Lê um arquivo SQL e retorna seu conteúdo como string.
    """
    pasta_sql = os.path.join(os.path.dirname(__file__), "scripts_sql")
    caminho_arquivo = os.path.join(pasta_sql, nome_arquivo)

    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        return arquivo.read()
