import mysql.connector
import logging
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def criar_tabelas():
    """
    Conecta ao MySQL, limpa as tabelas existentes e recria todas as tabelas.
    """
    logging.info("Conectando ao banco de dados MySQL...")
    conn = None

    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            charset='utf8mb4'
        )

        cursor = conn.cursor()

        # Removendo tabelas existentes
        logging.info("Removendo tabelas existentes...")
        cursor.execute("DROP TABLE IF EXISTS demonstracoes_contabeis")
        cursor.execute("DROP TABLE IF EXISTS operadoras")

        # Criando as tabelas novamente
        logging.info("Recriando tabelas...")
        query1 = """-- MySQL
        CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
            id INT AUTO_INCREMENT PRIMARY KEY,
            data DATE,
            reg_ans INT,
            cd_conta_contabil INT,
            descricao TEXT
        )"""

        query2 = """-- MySQL
        CREATE TABLE IF NOT EXISTS operadoras (
            id INT AUTO_INCREMENT PRIMARY KEY,
            registro_ans INT,
            cnpj INT,
            razao_social TEXT
        )"""
        cursor.execute(query1)
        cursor.execute(query2)

        conn.commit()
        logging.info("Tabelas criadas com sucesso.")

    except Exception as erro:
        logging.error(f"Erro ao criar tabelas: {erro}")
        import traceback
        logging.debug(traceback.format_exc())

    finally:
        if conn:
            conn.close()
