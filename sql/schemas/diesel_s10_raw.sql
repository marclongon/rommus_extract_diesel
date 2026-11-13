CREATE SCHEMA IF NOT EXISTS `gen-lang-client-0722386172.rommus_staging_diesel_s10_raw`;
CREATE TABLE IF NOT EXISTS `gen-lang-client-0722386172.rommus_staging_diesel_s10_raw.diesel_s10` (
  captured_on             DATE,
  ingested_at             TIMESTAMP,
  legal_name              STRING,
  cnpj                    STRING,
  address                 STRING,
  address_complement      STRING,
  neighborhood            STRING,
  postal_code             STRING,
  region                  STRING,
  state                   STRING,
  municipality_name       STRING,
  product                 STRING,
  sell_value              NUMERIC,
  purchase_value          NUMERIC,
  measurement_unit        STRING,
  brand                   STRING,
  source_id               STRING,
  source_type             STRING,
  PRIMARY KEY (
    captured_on,
    state,
    municipality_name,
    product,
    brand
  ) NOT ENFORCED
)
PARTITION BY captured_on