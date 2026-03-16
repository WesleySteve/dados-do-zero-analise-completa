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
