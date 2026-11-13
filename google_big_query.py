import google.auth
from google.cloud import bigquery
from pathlib import Path

credenciais, projeto = google.auth.default()
print("Projeto:", projeto)

client = bigquery.Client(project=projeto, credentials=credenciais)

# Cria tabela no Bigquery
sql_raw_path = Path("sql/schemas/diesel_s10_raw.sql")
sql_raw = sql_raw_path.read_text(encoding="utf-8")
query_job = client.query(sql_raw)
query_job.result()

sql_raw_staging_path = Path("sql/schemas/diesel_s10_raw_staging.sql")
sql_raw_staging = sql_raw_staging_path.read_text(encoding="utf-8")
query_job = client.query(sql_raw_staging)
query_job.result()

def validar_duplicidades():

    sql_val_path = Path(
        "sql/validations/diesel_s10_val.sql"
    )

    sql_val = sql_val_path.read_text(encoding="utf-8")
    resultado = client.query(sql_val).result()

    duplicidades = list(resultado)

    if duplicidades:

        print("Validacao: Foram encontradas duplicidades a serem tratadas")

        # for linha in duplicidades:
        #     print(dict(linha.items()))

        # raise ValueError(
        #     "Validacao: Carga interrompida - existem registros duplicados."
        # )

    else:
        print("Validacao: Nenhum registro duplicado.")

def carregar_bigquery(df):

    staging_table = "gen-lang-client-0722386172.rommus_staging_diesel_s10_raw_staging.diesel_s10"

    # 1. Carregar dados na staging
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE"
    )

    job = client.load_table_from_dataframe(
        df,
        staging_table,
        job_config=job_config
    )

    job.result()

    print("Dados carregados na staging.")

    # 2. Validar duplicidades
    validar_duplicidades()

    # 3. Executar MERGE
    sql_path = Path(
        "sql/transformations/diesel_s10_merge.sql"
    )

    sql = sql_path.read_text(encoding="utf-8")

    client.query(sql).result()

    print("Tabela definitiva atualizada com sucesso!")
