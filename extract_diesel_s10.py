import pandas as pd
from urllib.error import HTTPError

def extract():
    meses = pd.date_range(
        end=pd.Timestamp.today().replace(day=1),
        periods=13,
        freq="MS"
    )

    dfs = []

    for data in meses:  # meses criado com pd.date_range(...)
        ano = data.year
        mes = f"{data.month:02d}"

        print(f"\nConsultando {mes}/{ano}")

        urls = [
            f"https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsan/{ano}/{mes}-dados-abertos-precos-{ano}-{mes}-diesel-gnv.csv",
            f"https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsan/{ano}/{mes}-diesel-gnv.csv",
            f"https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsan/{ano}/precos-diesel-gnv-{mes}.csv",
            f"https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsan/{ano}/{mes}-dados-abertos-precos-diesel-gnv.csv",
            f"https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsan/{ano}/{mes}-dados-abertos-precos-diesel-gnv"
        ]

        for url in urls:
            try:
                df_mes = pd.read_csv(url, sep=";")  # remova sep=";" se o arquivo usar vírgula
                print(f"Quantidade de dados: {len(df_mes)}")
                print(f"Arquivo encontrado: {url}\n")
                dfs.append(df_mes)  # guarda o DataFrame
                break  # achou um arquivo; passa para o próximo mês
            except HTTPError as erro:
                if erro.code != 404:
                    print(f"Nenhum dos links foi encontrado para {mes}/{ano}\n")
                    # raise
        else:
            # raise FileNotFoundError(f"Nenhum dos links foi encontrado para {mes}/{ano}")
            print(f"Nenhum dos links foi encontrado para {mes}/{ano}\n")


    df_anp = pd.concat(dfs, ignore_index=True)
    df_anp = df_anp[df_anp["Produto"] == "DIESEL S10"]

    return df_anp