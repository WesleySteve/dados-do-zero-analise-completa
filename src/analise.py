# %%
import os

import pandas as pd

# %%
# DEFINIÇAO DE DIRETORIOS

BASE_DIR = os.path.dirname(os.path.abspath("."))
DATA_DIR = os.path.join(BASE_DIR, "data")
VIAGENS_DIR = os.path.join(DATA_DIR, "viagens")
VIAGENS_DIR_2024 = os.path.join(VIAGENS_DIR, "viagens_2024")


# %%
# esse comando deixa visivel todos os campos das colunas
pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", "{:.2f}".format)

df_viagens = pd.read_csv(
    os.path.join(VIAGENS_DIR_2024, "2024_Viagem.csv"),
    sep=";",
    encoding="windows-1252",
)

df_viagens.head()

# %%
df_viagens.info()

# %%
# transformando valores objects em float

df_viagens["Valor diárias"] = (
    df_viagens["Valor diárias"].str.replace(",", ".").astype(float)
)

df_viagens["Valor passagens"] = (
    df_viagens["Valor passagens"].str.replace(",", ".").astype(float)
)

df_viagens["Valor devolução"] = (
    df_viagens["Valor devolução"].str.replace(",", ".").astype(float)
)

df_viagens["Valor outros gastos"] = (
    df_viagens["Valor outros gastos"].str.replace(",", ".").astype(float)
)

# %%
df_viagens.info()

# %%
# soma das colunas de gastos

df_viagens["Despesas"] = (
    df_viagens["Valor diárias"]
    + df_viagens["Valor passagens"]
    + df_viagens["Valor devolução"]
    + df_viagens["Valor outros gastos"]
)

# %%
df_viagens.head()

# %%
# tratando nulos
df_viagens["Cargo"] = df_viagens["Cargo"].fillna("NAO INFORMADO")

# %%
# tratando datas
df_viagens["Período - Data de início"] = pd.to_datetime(
    df_viagens["Período - Data de início"], format="%d/%m/%Y"
)
df_viagens["Período - Data de fim"] = pd.to_datetime(
    df_viagens["Período - Data de fim"], format="%d/%m/%Y"
)

# %%
df_viagens.info()

# %%
# mes_viagem
df_viagens["Mes_viagem"] = df_viagens["Período - Data de início"].dt.month_name()

# %%
# dias_viagem
df_viagens["Dias_viagem"] = (
    df_viagens["Período - Data de fim"] - df_viagens["Período - Data de início"]
).dt.days

# %%
df_viagens.head()

# %%

(
    df_viagens.groupby("Cargo")
    .agg(  # coluna usada da tabela principal, agregação
        despesa_nedia=("Despesas", "mean"),
        duracao_media=("Dias_viagem", "mean"),
        despesas_totais=("Despesas", "sum"),
        destino_mais_frequentes=("Destinos", pd.Series.mode),  # moda
        nro_viagens=("Nome", "count"),
    )
    .reset_index()
)

# %%
# novas colunas base no cargo
df_viagens_consolidado = (
    df_viagens.groupby("Cargo")
    .agg(
        despesa_nedia=("Despesas", "mean"),
        duracao_media=("Dias_viagem", "mean"),
        despesas_totais=("Despesas", "sum"),
        destino_mais_frequentes=("Destinos", pd.Series.mode),  # moda
        nro_viagens=("Nome", "count"),
    )
    .reset_index()
)

# %%
df_cargos = df_viagens["Cargo"].value_counts(normalize=True).reset_index()
df_cargos

# %%
df_cargos.loc[df_cargos["proportion"] > 0.01, "Cargo"]

# %%
cargos_relevantes = df_cargos.loc[df_cargos["proportion"] > 0.01, "Cargo"]

# %%
filtro = df_viagens_consolidado["Cargo"].isin(cargos_relevantes)

# %%
df_final = df_viagens_consolidado[filtro].sort_values(by="nro_viagens", ascending=False)

# %%
df_final.head()

# %%
# ------- GRAFICO ----------- #
# %%
df_final = df_final.sort_values(by="nro_viagens", ascending=False)

# %%
df_final.plot(x="Cargo", y="nro_viagens", kind="bar")

# %%
import matplotlib.pyplot as plt

# %%
fig, ax = plt.subplots(figsize=(16, 6))

ax.barh(df_final["Cargo"], df_final["nro_viagens"])
ax.invert_yaxis()

fig.suptitle("Viagens por cargo publico (2024)", fontsize=14)

plt.figtext(0.65, 0.90, "Fonte: Portal da Transparência", fontsize=9)

plt.grid(color="gray", linestyle="--", linewidth="0.3")
plt.yticks(fontsize=8)
plt.xlabel("Numero de viagens")

plt.show()

# %%
# definindo diretorio para salvar o arquivo final
OUTPUT_DIR = os.path.join(VIAGENS_DIR_2024, "output")

# %%
# SALVANDO ARQUIVO
df_viagens.to_csv(os.path.join(OUTPUT_DIR, "viagens_final.csv"), index=False)

# %%
