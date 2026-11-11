# %%
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


    def calcular(self, df_anp, eixos, distancia_km, regiao = None, estado = None):
        if eixos not in self.consumo_km_por_litro:
            raise ValueError("Necessidade de informacao de 3, 5 ou 7 eixos.")
        if distancia_km <= 0:
            raise ValueError("A distância deve ser maior que zero.")

        #Utiliza dados de combustivel da ANP
        if regiao is None and estado is None:
            df_anp_br = (
                df_anp.groupby("Produto")["Valor de Venda"]
                .mean()
            )
            diesel_s10 = df_anp_br.iloc[0]
        elif regiao is not None:
            df_anp_reg = (
                df_anp.groupby("Regiao - Sigla")["Valor de Venda"]
                .mean()
            )
            diesel_s10 = df_anp_est.loc[regiao]
        elif estado is not None:
            df_anp_est = (
                df_anp.groupby("Estado - Sigla")["Valor de Venda"]
                .mean()
            )
            diesel_s10 = df_anp_est.loc[estado]
    

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

        return {
            "preco_combustivel": round(float(diesel_s10),2),
            "custos_por_km": custos,
            "custo_medio_por_km": custo_por_km,
            "preco_medio_por_km": preco_por_km,
            "margem_media_por_km": margem_por_km,
            "custo_estimado": custo_por_km * distancia_km,
            "frete_estimado": preco_por_km * distancia_km,
            "margem_estimada": margem_por_km * distancia_km
        }


