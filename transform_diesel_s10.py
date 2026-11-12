import pandas as pd

def transform(df_anp):
    print(f"\n{df_anp.info()}\n")
    print(f"\n{df_anp.describe()}\n")
    print(f"\n{df_anp.nunique()}\n")

    # Criacao de anomes para id do mes
    df_anp["Data da Coleta"] = pd.to_datetime(
        df_anp["Data da Coleta"],
        dayfirst=True,
        errors="coerce"
    )
    df_anp["anomes"] = df_anp["Data da Coleta"].dt.strftime("%Y-%m")

    # Adequa valor ao padrao americano
    df_anp["Valor de Venda"] = pd.to_numeric(
        df_anp["Valor de Venda"].astype("string").str.replace(",", ".", regex=False),
        errors="coerce"
    )

    df_anp.reset_index()

    # Reducao de colunas para o necessario
    df_anp = df_anp[["anomes", "Regiao - Sigla", "Estado - Sigla", "Municipio", "Produto",
                    "Data da Coleta", "Valor de Venda", "Bandeira"]]

    df_anp = df_anp.rename(columns={
                    "anomes": "anomes", 
                    "Regiao - Sigla": "regiao_sigla",
                    "Estado - Sigla": "estado_sigla",
                    "Municipio": "municipio",
                    "Produto": "produto",
                    "Data da Coleta": "data_coleta",
                    "Valor de Venda": "valor_venda",
                    "Bandeira": "bandeira"
    })

    print(f"\n{df_anp.info()}")

    return df_anp