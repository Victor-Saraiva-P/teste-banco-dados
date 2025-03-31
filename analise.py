import logging

import pandas as pd
from sqlalchemy import create_engine

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, FIM_TRIMESTRE, INICIO_TRIMESTRE, ANO_ANALISE


def top_dez_operadoras_trimestre():
    logging.info("Iniciando análise das operadoras...")

    logging.info(f"Período analisado: {INICIO_TRIMESTRE} a {FIM_TRIMESTRE}")

    # Cria o engine do SQLAlchemy para conexão com MySQL
    engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    # Descrição desejada (com normalização para ignorar variações de espaços/maiúsculas)
    desired_description = "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR"

    # Consulta para obter as 10 operadoras com maiores despesas calculadas como (vl_saldo_inicial - vl_saldo_final)
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
    df_top10 = pd.read_sql(query_top10, engine, params=(desired_description, INICIO_TRIMESTRE, FIM_TRIMESTRE))

    if df_top10.empty:
        logging.warning(
            "A consulta não retornou resultados. Verifique se os filtros (descrição e período) correspondem aos dados disponíveis.")
    else:
        logging.info("Análise por operadora concluída. Resultados:")
        logging.info(df_top10)

    print(
        "Top 10 operadoras com maiores despesas em 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR' no último trimestre de 2024:")
    print(df_top10)


def top_dez_operadoras_ultimo_ano():
    logging.info("Iniciando análise das operadoras para o último ano configurado...")

    start_date = f"{ANO_ANALISE}-01-01"
    end_date = f"{ANO_ANALISE}-12-31"
    logging.info(f"Período analisado: {start_date} a {end_date}")

    engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    desired_description = "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR"

    query_top10 = """
        SELECT 
            o.Razao_Social, 
            SUM(d.vl_saldo_inicial) AS total_saldo_inicial,
            SUM(d.vl_saldo_final) AS total_saldo_final,
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
    df_top10 = pd.read_sql(query_top10, engine, params=(desired_description, start_date, end_date))
    engine.dispose()

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)

    print(f"Top 10 operadoras com maiores despesas em '{desired_description}' no ano {ANO_ANALISE}:")
    print(df_top10.to_string(index=False))




if __name__ == "__main__":
    top_dez_operadoras_ultimo_ano()
    print("--------------------------------------------------------")
    top_dez_operadoras_trimestre()
