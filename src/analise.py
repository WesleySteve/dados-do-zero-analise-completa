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
