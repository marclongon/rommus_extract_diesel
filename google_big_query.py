import google.auth
from google.cloud import bigquery
from pathlib import Path

credenciais, projeto = google.auth.default()
print("Projeto:", projeto)

client = bigquery.Client(project=projeto, credentials=credenciais)

# Cria tabela no Bigquery
sql_path = Path("sql/schemas/diesel_s10.sql")
sql = sql_path.read_text(encoding="utf-8")

query_job = client.query(sql)
query_job.result()

def validar_duplicidades():

    sql_path = Path(
        "sql/validations/val_diesel_s10.sql"
    )

    sql = sql_path.read_text(encoding="utf-8")
    resultado = client.query(sql).result()

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

    staging_table = "rommus.staging.diesel_s10"

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
        "sql/transformations/merge_diesel_s10.sql"
    )

    sql = sql_path.read_text(encoding="utf-8")

    client.query(sql).result()

    print("Tabela definitiva atualizada com sucesso!")
