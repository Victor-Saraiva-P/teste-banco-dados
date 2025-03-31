SELECT o.Razao_Social,
       SUM(d.vl_saldo_inicial - d.vl_saldo_final) AS total_despesa
FROM demonstracoes_contabeis d
         JOIN operadoras o ON d.reg_ans = o.Registro_ANS
WHERE REGEXP_REPLACE(UPPER(d.descricao), '[[:space:]]+', '') =
      REGEXP_REPLACE(UPPER(%s), '[[:space:]]+', '')
          AND d.data BETWEEN %s AND %s
GROUP BY o.Razao_Social
ORDER BY total_despesa DESC
LIMIT 10;