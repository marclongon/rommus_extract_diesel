import pandas as pd
from decimal import Decimal

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
    df_anp["Data da Coleta"] = df_anp["Data da Coleta"].dt.date

    df_anp["Valor de Venda"] = (
        df_anp["Valor de Venda"]
        .astype("string")
        .str.replace(",", ".", regex=False)
        .map(lambda valor: Decimal(valor) if valor and valor.strip() else None)
    )

    df_anp["Valor de Compra"] = (
        df_anp["Valor de Venda"]
        .astype("string")
        .str.replace(",", ".", regex=False)
        .map(lambda valor: Decimal(valor) if valor and valor.strip() else None)
    )

    df_anp["address"] = (
        df_anp["Nome da Rua"].astype("string").fillna("").str.strip() + ", " + 
        df_anp["Numero Rua"].astype("string").fillna("").str.strip()
    ).str.strip()
    df_anp.drop(columns=["Nome da Rua", "Numero Rua"], inplace=True)

    df_anp["ingested_at"] = pd.Timestamp.now(tz="UTC")
    df_anp["source_id"] = "anp"
    df_anp["source_type"] = "official"
    
    df_anp.reset_index()

    df_anp = df_anp.rename(columns={
                    "Revenda": "legal_name",
                    "Regiao - Sigla": "region",
                    "Estado - Sigla": "state",
                    "Municipio": "municipality_name",
                    "Produto": "product",
                    "Data da Coleta": "captured_on",
                    "Valor de Venda": "sell_value",
                    "Bandeira": "brand",
                    "CNPJ da Revenda": "cnpj",
                    "Endereco": "address",
                    "Complemento": "address_complement",
                    "Bairro": "neighborhood",
                    "Cep": "postal_code",
                    "Valor de Compra": "purchase_value",
                    "Unidade de Medida": "measurement_unit"
    })

    df_anp = df_anp[["captured_on", "ingested_at", "legal_name", "cnpj", 
                     "address", "address_complement", "neighborhood", 
                     "postal_code", "region", "state", "municipality_name", 
                     "product", "sell_value", "purchase_value", "measurement_unit", 
                     "brand", "source_id", "source_type"
    ]]

    print(f"\n{df_anp.info()}")

    return df_anp