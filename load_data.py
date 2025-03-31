import mysql.connector
import logging
import glob
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def carregar_dados():
    """
    Carrega os dados dos CSVs para as tabelas demonstracoes_contabeis e operadoras
    usando o comando LOAD DATA LOCAL INFILE.
    """
    logging.info("Carregando dados para as tabelas...")
    conn = None

    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            charset='utf8mb4',
            allow_local_infile=True
        )
        cursor = conn.cursor()

        # --- Carregar dados para demonstracoes_contabeis ---
        # Procura todos os arquivos CSV recursivamente na pasta de demonstracoes
        lista_csv_demonstracoes = glob.glob("downloads/demonstracoes_contabeis/**/*.csv", recursive=True)
        if not lista_csv_demonstracoes:
            logging.warning("Nenhum arquivo CSV encontrado para demonstracoes_contabeis.")
        else:
            for caminho in lista_csv_demonstracoes:
                logging.info(f"Carregando dados do arquivo: {caminho}")
                query_load_demonstracoes = f"""
                LOAD DATA LOCAL INFILE '{caminho.replace('\\', '/')}' 
                INTO TABLE demonstracoes_contabeis
                CHARACTER SET utf8mb4
                FIELDS TERMINATED BY ';' -- Ajuste aqui se o delimitador for diferente
                OPTIONALLY ENCLOSED BY '"' -- Ajuste se os valores estiverem entre aspas
                LINES TERMINATED BY '\\n'
                IGNORE 1 LINES
                (data, reg_ans, cd_conta_contabil, descricao);
                """

                cursor.execute(query_load_demonstracoes)
                conn.commit()
            logging.info("Dados carregados para demonstracoes_contabeis com sucesso.")

        # --- Carregar dados para operadoras ---
        # Supondo que exista apenas um CSV para operadoras (ajuste se houver mais)
        caminho_csv_operadoras = "downloads/operadoras/Relatorio_cadop.csv"
        logging.info(f"Carregando dados do arquivo: {caminho_csv_operadoras}")
        query_load_operadoras = f"""
                        LOAD DATA LOCAL INFILE '{caminho_csv_operadoras.replace('\\', '/')}' 
                        INTO TABLE operadoras
                        CHARACTER SET utf8mb4
                        FIELDS TERMINATED BY ';' -- Ajuste aqui se o delimitador for diferente
                        OPTIONALLY ENCLOSED BY '"' -- Ajuste se os valores estiverem entre aspas
                        LINES TERMINATED BY '\\n'
                        IGNORE 1 LINES
                        (registro_ans, cnpj, razao_social);
                        """
        cursor.execute(query_load_operadoras)
        conn.commit()
        logging.info("Dados carregados para operadoras com sucesso.")

    except Exception as erro:
        logging.error(f"Erro ao carregar dados: {erro}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    carregar_dados()
