CREATE SCHEMA IF NOT EXISTS `rommus.consultas`;
CREATE TABLE IF NOT EXISTS `rommus.consultas.diesel_s10` (
    anomes                INT64,
    regiao_sigla          STRING,
    estado_sigla          STRING,
    municipio             STRING,
    produto               STRING,
    data_coleta           DATE,
    valor_venda           NUMERIC,
    bandeira              STRING,
  PRIMARY KEY (
    data_coleta,
    estado_sigla,
    municipio,
    produto,
    bandeira
  ) NOT ENFORCED
)
PARTITION BY data_coleta