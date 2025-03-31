LOAD DATA LOCAL INFILE '%s'
    INTO TABLE demonstracoes_contabeis
    CHARACTER SET utf8mb4
    FIELDS TERMINATED BY ';'
    OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES
    (data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final);