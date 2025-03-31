LOAD DATA LOCAL INFILE '%s'
    INTO TABLE operadoras
    CHARACTER SET utf8mb4
    FIELDS TERMINATED BY ';'
    OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES
    (registro_ans, cnpj, razao_social);