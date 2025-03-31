import logging

import pandas as pd
from sqlalchemy import create_engine

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, FIM_TRIMESTRE, INICIO_TRIMESTRE, ANO_ANALISE, \
    CATEGORIA_ANALISE
from sql_util import ler_sql_arquivo


def top_dez_operadoras_trimestre():
    engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    query_top10 = ler_sql_arquivo("top_10_despesas.sql")
    df_top10 = pd.read_sql(query_top10, engine, params=(CATEGORIA_ANALISE, INICIO_TRIMESTRE, FIM_TRIMESTRE))
    engine.dispose()

    logging.info("Análise do último trimestre concluída.")
    return df_top10


def top_dez_operadoras_ultimo_ano():
    start_date = f"{ANO_ANALISE}-01-01"
    end_date = f"{ANO_ANALISE}-12-31"

    engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    query_top10 = ler_sql_arquivo("top_10_despesas.sql")
    df_top10 = pd.read_sql(query_top10, engine, params=(CATEGORIA_ANALISE, start_date, end_date))
    engine.dispose()

    logging.info("Análise do último ano concluída.")
    return df_top10

if __name__ == "__main__":
    # Configurações de logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Executa a análise após carregar os dados
    logging.info("Iniciando análise dos dados do csv")

    top_semestre = top_dez_operadoras_trimestre()
    print(f"Quais as 10 operadoras com maiores despesas em '{CATEGORIA_ANALISE}' no último trimestre?")
    print(f"Top 10 operadoras com maiores despesas em '{CATEGORIA_ANALISE}' no último trimestre de 2024:")
    print(top_semestre)

    print(
        "------------------------------------------------------------------------------------------------------------------")

    top_ano = top_dez_operadoras_ultimo_ano()
    print(f"Quais as 10 operadoras com maiores despesas nessa categoria no último ano?")
    print(f"Top 10 operadoras com maiores despesas em '{CATEGORIA_ANALISE}' no ano {ANO_ANALISE}:")
    print(top_ano)
