#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

arquivo = "resultados_sem_outlier_lesao.xlsx" # MUDAR

# ler todas as abas
sheets = pd.read_excel(arquivo, sheet_name=None)

resultado_long = {}

for nome_aba, df in sheets.items():
    
    # renomear coluna sujeito se necessário
    if "Unnamed: 0" in df.columns:
        df = df.rename(columns={"Unnamed: 0": "sujeito"})
    
    # transformar para long
    long = df.melt(
        id_vars=["sujeito","Fator_Lesao","Fator_ETCC"],
        value_vars=["ME_pre","MD_pre","ME_pos","MD_pos"],
        var_name="condicao",
        value_name="valor"
    )
    
    # separar lado e tempo
    long[["lado","tempo"]] = long["condicao"].str.split("_", expand=True)
    
    long = long.drop(columns="condicao")
    
    resultado_long[nome_aba] = long

# salvar novo arquivo com todas abas
with pd.ExcelWriter("resultados_long.xlsx") as writer:
    for nome_aba, df in resultado_long.items():
        df.to_excel(writer, sheet_name=nome_aba, index=False)