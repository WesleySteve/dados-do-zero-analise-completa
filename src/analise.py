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
df_viagens.columns

# %%
# definindo novos nomes para os campos
novos_nomes = {
    "Identificador do processo de viagem": "identificador_processo_viagem",
    "Número da Proposta (PCDP)": "numero_proposta_(PCDP)",
    "Situação": "situacao",
    "Viagem Urgente": "viagem_urgente",
    "Justificativa Urgência Viagem": "justificativa_urgencia_viagem",
    "Código do órgão superior": "codigo_orgao_superior",
    "Nome do órgão superior": "nome_orgao_superior",
    "Código órgão solicitante": "codigo_orgao_solicitante",
    "Nome órgão solicitante": "nome_orgao_solicitante",
    "CPF viajante": "cpf_viajante",
    "Nome": "nome",
    "Cargo": "cargo",
    "Função": "funcao",
    "Descrição Função": "descricao_funcao",
    "Período - Data de início": "periodo_data_inicio",
    "Período - Data de fim": "periodo_data_fim",
    "Destinos": "destinos",
    "Motivo": "motivo",
    "Valor diárias": "valor_diarias",
    "Valor passagens": "valor_passagens",
    "Valor devolução": "valor_devolucao",
    "Valor outros gastos": "valor_outros_gastos",
}

# %%
df_viagens = df_viagens.rename(columns=novos_nomes)

# %%
df_viagens.info()

# %%
# transformando valores objects em float

df_viagens["valor_diarias"] = (
    df_viagens["valor_diarias"].str.replace(",", ".").astype(float)
)

df_viagens["valor_passagens"] = (
    df_viagens["valor_passagens"].str.replace(",", ".").astype(float)
)

df_viagens["valor_devolucao"] = (
    df_viagens["valor_devolucao"].str.replace(",", ".").astype(float)
)

df_viagens["valor_outros_gastos"] = (
    df_viagens["valor_outros_gastos"].str.replace(",", ".").astype(float)
)

# %%
df_viagens.info()

# %%
# soma das colunas de gastos

df_viagens["despesas"] = (
    df_viagens["valor_diarias"]
    + df_viagens["valor_passagens"]
    + df_viagens["valor_devolucao"]
    + df_viagens["valor_outros_gastos"]
)

# %%
df_viagens.head()

# %%
# tratando nulos
df_viagens["cargo"] = df_viagens["cargo"].fillna("NAO INFORMADO")

# %%
# tratando datas
df_viagens["periodo_data_inicio"] = pd.to_datetime(
    df_viagens["periodo_data_inicio"], format="%d/%m/%Y"
)
df_viagens["periodo_data_fim"] = pd.to_datetime(
    df_viagens["periodo_data_fim"], format="%d/%m/%Y"
)

# %%
df_viagens.info()

# %%
# mes_viagem
df_viagens["mes_viagem"] = df_viagens["periodo_data_inicio"].dt.month_name()

# %%
# dias_viagem
df_viagens["dias_viagem"] = (
    df_viagens["periodo_data_fim"] - df_viagens["periodo_data_inicio"]
).dt.days

# %%
df_viagens.head()

# %%

(
    df_viagens.groupby("cargo")
    .agg(  # coluna usada da tabela principal, agregação
        despesa_nedia=("despesas", "mean"),
        duracao_media=("dias_viagem", "mean"),
        despesas_totais=("despesas", "sum"),
        destino_mais_frequentes=("destinos", pd.Series.mode),  # moda
        nro_viagens=("nome", "count"),
    )
    .reset_index()
)

# %%
# novas colunas base no cargo
df_viagens_consolidado = (
    df_viagens.groupby("cargo")
    .agg(
        despesa_nedia=("despesas", "mean"),
        duracao_media=("dias_viagem", "mean"),
        despesas_totais=("despesas", "sum"),
        destino_mais_frequentes=("destinos", pd.Series.mode),  # moda
        nro_viagens=("nome", "count"),
    )
    .reset_index()
)

# %%
df_cargos = df_viagens["cargo"].value_counts(normalize=True).reset_index()
df_cargos

# %%
df_cargos.loc[df_cargos["proportion"] > 0.01, "cargo"]

# %%
cargos_relevantes = df_cargos.loc[df_cargos["proportion"] > 0.01, "cargo"]

# %%
filtro = df_viagens_consolidado["cargo"].isin(cargos_relevantes)

# %%
df_final = df_viagens_consolidado[filtro].sort_values(by="nro_viagens", ascending=False)

# %%
df_final.head()

# %%
# ------- GRAFICO ----------- #
# %%
df_final = df_final.sort_values(by="nro_viagens", ascending=False)

# %%
df_final.plot(x="cargo", y="nro_viagens", kind="bar")

# %%
import matplotlib.pyplot as plt

# %%
fig, ax = plt.subplots(figsize=(16, 6))

ax.barh(df_final["cargo"], df_final["nro_viagens"])
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
