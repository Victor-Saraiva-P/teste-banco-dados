import logging

import pandas as pd
from sqlalchemy import create_engine

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, FIM_TRIMESTRE, INICIO_TRIMESTRE, ANO_ANALISE, \
    CATEGORIA_ANALISE


def top_dez_operadoras_trimestre():
    engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


    query_top10 = """
        SELECT 
            o.Razao_Social, 
            SUM(d.vl_saldo_inicial - d.vl_saldo_final) AS total_despesa
        FROM demonstracoes_contabeis d
        JOIN operadoras o ON d.reg_ans = o.Registro_ANS
        WHERE REGEXP_REPLACE(UPPER(d.descricao), '[[:space:]]+', '') =
              REGEXP_REPLACE(UPPER(%s), '[[:space:]]+', '')
          AND d.data BETWEEN %s AND %s
        GROUP BY o.Razao_Social
        ORDER BY total_despesa DESC
        LIMIT 10;
    """
    df_top10 = pd.read_sql(query_top10, engine, params=(CATEGORIA_ANALISE, INICIO_TRIMESTRE, FIM_TRIMESTRE))
    engine.dispose()

    logging.info("Análise do último trimestre concluída.")
    return df_top10


def top_dez_operadoras_ultimo_ano():
    start_date = f"{ANO_ANALISE}-01-01"
    end_date = f"{ANO_ANALISE}-12-31"

    engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    query_top10 = """
        SELECT 
            o.Razao_Social, 
            SUM(d.vl_saldo_inicial - d.vl_saldo_final) AS total_despesa
        FROM demonstracoes_contabeis d
        JOIN operadoras o ON d.reg_ans = o.Registro_ANS
        WHERE REGEXP_REPLACE(UPPER(d.descricao), '[[:space:]]+', '') =
              REGEXP_REPLACE(UPPER(%s), '[[:space:]]+', '')
          AND d.data BETWEEN %s AND %s
        GROUP BY o.Razao_Social
        ORDER BY total_despesa DESC
        LIMIT 10;
    """
    df_top10 = pd.read_sql(query_top10, engine, params=(CATEGORIA_ANALISE, start_date, end_date))
    engine.dispose()

    logging.info("Análise do último ano concluída.")
    return df_top10


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    top_dez_operadoras_ultimo_ano()
    top_dez_operadoras_trimestre()
