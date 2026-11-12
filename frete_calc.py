from dataclasses import dataclass

@dataclass
class Frete:
    consumo_km_por_litro = {
        3: 3.2,
        5: 2.7,
        7: 2.0,
    }

    outros_custos_por_km = {
        3: {
            "Manutenção": 0.35,
            "Pneus": 0.22,
            "Motorista": 0.90,
            "Custos fixos": 0.95,
            "Margem": 0.20
        },
        5: {
            "Manutenção": 0.45,
            "Pneus": 0.32,
            "Motorista": 1.00,
            "Custos fixos": 1.15,
            "Margem": 0.20
        },
        7: {
            "Manutenção": 0.60,
            "Pneus": 0.42,
            "Motorista": 1.15,
            "Custos fixos": 1.55,
            "Margem": 0.20
        },
    }    


    def calcular(self, df_anp, eixos, distancia_km, visao = "br", local = None):
        if eixos not in self.consumo_km_por_litro:
            raise ValueError("Necessidade de informacao de 3, 5 ou 7 eixos.")
        if distancia_km <= 0:
            raise ValueError("A distância deve ser maior que zero.")      

        df_anp_hist, diesel_s10 = resumo_diesel_s10(df_anp, visao = visao, local = local)
        custo_combustivel_km = (
            diesel_s10 / self.consumo_km_por_litro[eixos]
        )

        custos = self.outros_custos_por_km[eixos].copy()
        custos["Combustível Km"] = round(float(custo_combustivel_km),2)
        margem = custos["Margem"]

        total_sem_margem = sum(
            valor for item, valor in custos.items()
            if item != "Margem"
        )
        
        custo_por_km = total_sem_margem
        preco_por_km = custo_por_km  / (1-margem)
        margem_por_km = preco_por_km * margem

        return df_anp_hist, {
            "preco_combustivel": diesel_s10,
            "custos_por_km": custos,
            "custo_medio_por_km": custo_por_km,
            "preco_medio_por_km": preco_por_km,
            "margem_media_por_km": margem_por_km,
            "custo_estimado": custo_por_km * distancia_km,
            "frete_estimado": preco_por_km * distancia_km,
            "margem_estimada": margem_por_km * distancia_km,
        }

def resumo_diesel_s10(df_anp, visao = "br", local = None):
    visoes = ["br", "regiao", "estado"]
    regioes = ["N", "NE", "CO", "SE", "S"]
    estados = ["AC", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT",
    "PA", "PB", "PE", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE",
    "SP", "AL", "TO", "AP", "PI"]

    import pandas as pd
    pd.set_option("display.multi_sparse", False)

    if visao not in visoes:
        raise ValueError("O local informado nao e valido")
    else:
        if visao == "br":
            df_anp_hist = (
                    df_anp.groupby(["anomes", "Produto"])["Valor de Venda"]
                    .mean()
                    .reset_index()
                    .sort_index(ascending = True)
            )
            diesel_s10 = df_anp_hist.iloc[-1]["Valor de Venda"]
        elif visao == "regiao":
            if local in regioes:
                df_anp_hist = (
                        df_anp.groupby(["anomes", "Regiao - Sigla"])["Valor de Venda"]
                        .mean()
                        .reset_index()
                        .sort_index(ascending = True)
                )
                df_anp_hist = df_anp_hist[df_anp_hist["Regiao - Sigla"] == local]
                diesel_s10 = df_anp_hist.iloc[-1]["Valor de Venda"]
            else:
                raise ValueError("O local informado nao e valido")
        elif visao == "estado":
            if local in estados:
                df_anp_hist = (
                        df_anp.groupby(["anomes", "Estado - Sigla"])["Valor de Venda"]
                        .mean()
                        .reset_index()
                        .sort_index(ascending = True)
                )
                df_anp_hist = df_anp_hist[df_anp_hist["Estado - Sigla"] == local]
                diesel_s10 = df_anp_hist.iloc[-1]["Valor de Venda"]
            else:
                raise ValueError("O local informado nao e valido")

        diesel_s10 = round(float(diesel_s10),2)
        
    return df_anp_hist, diesel_s10