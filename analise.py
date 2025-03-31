import logging

import pandas as pd
from sqlalchemy import create_engine

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, FIM_TRIMESTRE, INICIO_TRIMESTRE


def top_dez_operadoras():
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


if __name__ == "__main__":
    top_dez_operadoras()
