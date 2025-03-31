import mysql.connector
import logging
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def criar_tabelas():
    """
    Conecta ao MySQL e executa as queries de criacao das tabelas.
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

        query1 = """-- MySQL
        CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            operador VARCHAR(255), 
            categoria VARCHAR(255), 
            despesa DECIMAL(12,2), 
            data_operacao DATE, 
            outros_campos TEXT
        )"""

        query2 = """-- MySQL
        CREATE TABLE IF NOT EXISTS operadoras (
            id INT AUTO_INCREMENT PRIMARY KEY,
            codigo VARCHAR(50),
            nome VARCHAR(255),
            endereco TEXT
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
