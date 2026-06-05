#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 08:20:47 2026

@author: tercio
"""

import pandas as pd
import numpy as np
import os
import re

pasta = "data"

# ================================
# Encontrar sujeitos na pasta
# ================================

sujeitos = set()

for arquivo in os.listdir(pasta):
    
    match = re.search(r"suj(\d+)", arquivo)
    
    if match:
        sujeitos.add(match.group(1))

sujeitos = np.array(sorted(int(s) for s in sujeitos))


# ================================
# Ler planilha control.xlsx
# ================================

control = pd.read_excel("control.xlsx", index_col=0)

control.index = control.index.astype(int)

control = control.reindex(sujeitos)

control = control[["Fator_Lesao","Fator_ETCC"]]


# ================================
# Condições experimentais
# ================================

maos = ['MD', 'ME']
momentos = ['pre', 'pos']




# ================================
# Ler nomes das colunas de referência
# ================================

ref_colunas = pd.read_excel("ref. colunas.xlsx", header=0)

todas_colunas = ref_colunas.columns.tolist()

# índices desejados:
# 0 a 12 e depois 33 a 34
#indices_colunas = list(range(0, 13)) + list(range(33, 35))

#colunas_novas = [todas_colunas[i] for i in indices_colunas]
colunas_novas = todas_colunas

# ================================
# Estruturas de armazenamento
# ================================

dados_completos = {
    
    col: pd.DataFrame(index=sujeitos,
                      columns=['ME_pre','MD_pre','ME_pos','MD_pos'])
    
    for col in colunas_novas
}


contagem_linhas = pd.DataFrame(index=sujeitos,
                               columns=['ME_pre','MD_pre','ME_pos','MD_pos'])

contagem_linhas_filtradas = pd.DataFrame(index=sujeitos,
                               columns=['ME_pre','MD_pre','ME_pos','MD_pos'])


# ================================
# Função para processar arquivos
# ================================

def processar_arquivo(caminho):
    
    try:
        
        if not os.path.exists(caminho):
            return None, 0, 0
        
        with open(caminho,'r') as f:
            linhas_totais = sum(1 for _ in f) - 10
        
        if linhas_totais <= 0:
            return None, 0, 0
        
        df = pd.read_csv(caminho,
                         sep='\t',
                         header=None,
                         skiprows=10)
        
        
        df = df.astype(str)
        
        
        df = df.applymap(lambda x: float(x.replace(',','.')))
        
        
        df = df.values
        
        
        mask = df[:,0] >= 150
        
        df_filtrado = df[mask]
        
        linhas_filtradas = df_filtrado.shape[0]
        
        
        if linhas_filtradas > 0:
            
            medias = pd.DataFrame(df_filtrado).mean()
            
            return medias, linhas_totais, linhas_filtradas
        
        else:
            
            return None, linhas_totais, 0
    
    
    except Exception as e:
        
        print(f"Erro em {caminho}: {e}")
        
        return None, 0, 0



# ================================
# Loop principal
# ================================

for suj in sujeitos:
    
    for mao in maos:
        
        for momento in momentos:
            
            
            arquivo = os.path.join(pasta,
                                   f"suj{suj}{mao}{momento}")
            
            
            medias, n_tot, n_fil = processar_arquivo(arquivo)
            
            
            coluna = f"{mao}_{momento}"
            
            
            contagem_linhas.at[suj,coluna] = n_tot
            
            contagem_linhas_filtradas.at[suj,coluna] = n_fil
            
            
            if medias is not None:
                
                for i,col in enumerate(colunas_novas):
                    
                    if i < len(medias):
                        
                        dados_completos[col].at[suj,coluna] = medias[i]



# ================================
# Criar arquivo Excel
# ================================

with pd.ExcelWriter("resultados_raw.xlsx",
                    engine="openpyxl") as writer:
    
    
    # planilhas individuais
    for col in colunas_novas:
        
        df_saida = pd.concat([control,
                              dados_completos[col]],
                             axis=1)
        
        
        df_saida = df_saida[
            ['Fator_Lesao',
             'Fator_ETCC',
             'ME_pre',
             'MD_pre',
             'ME_pos',
             'MD_pos']
        ]
        
        
        df_saida.to_excel(writer,
                          sheet_name=col[:31])
    
    
    # todos dados juntos
    todos = pd.concat(dados_completos,
                      axis=1)
    
    
    todos = pd.concat([control,
                       todos],
                      axis=1)
    
    
    todos.to_excel(writer,
                   sheet_name="TODOS_DADOS")
    
    
    # contagens
    contagem_linhas.to_excel(writer,
                             sheet_name="LINHAS_TOTAIS")
    
    
    contagem_linhas_filtradas.to_excel(writer,
                                       sheet_name="LINHAS_FILTRADAS")
    
    
    # estatísticas
    contagem_linhas.describe().to_excel(writer,
                                        sheet_name="ESTAT_TOTAIS")
    
    
    contagem_linhas_filtradas.describe().to_excel(writer,
                                                  sheet_name="ESTAT_FILTRADAS")
    
    

import matplotlib.pyplot as plt

# criar pastas para salvar os gráficos
os.makedirs("graficos_lesao", exist_ok=True)
os.makedirs("graficos_etcc", exist_ok=True)


def plotar_fator(df, fator, nome_variavel, pasta_saida):

    grupos = df[fator].dropna().unique()

    condicoes = ['ME_pre','MD_pre','ME_pos','MD_pos']

    x = np.arange(len(condicoes))

    largura = 0.8 / len(grupos)

    plt.figure(figsize=(7,5))

    for i, g in enumerate(grupos):

        dados = df[df[fator] == g][condicoes]

        medias = dados.mean()
        erro = dados.sem()

        pos = x + (i - len(grupos)/2) * largura + largura/2

        plt.bar(pos,
                medias,
                width=largura,
                yerr=erro,
                capsize=4,
                label=str(g))

    plt.xticks(x, condicoes)

    plt.ylabel("Média")

    plt.title(nome_variavel)

    plt.legend(title=fator)

    plt.tight_layout()

    plt.savefig(f"{pasta_saida}/{nome_variavel}.png", dpi=300)

    plt.close()


# ======================================
# gerar gráficos
# ======================================

for col in colunas_novas:

    df_plot = pd.concat([control, dados_completos[col]], axis=1)

    df_plot = df_plot[['Fator_Lesao',
                       'Fator_ETCC',
                       'ME_pre',
                       'MD_pre',
                       'ME_pos',
                       'MD_pos']]

    df_plot[['ME_pre','MD_pre','ME_pos','MD_pos']] = df_plot[
        ['ME_pre','MD_pre','ME_pos','MD_pos']
    ].astype(float)


    # gráfico por fator lesão
    plotar_fator(df_plot,
                 "Fator_Lesao",
                 col,
                 "graficos_lesao")


    # gráfico por fator ETCC
    plotar_fator(df_plot,
                 "Fator_ETCC",
                 col,
                 "graficos_etcc")
    
# ======================================
# FUNÇÃO REMOÇÃO DE OUTLIER (IQR)
# ======================================

def remover_outliers(df, fator):

    condicoes = ['ME_pre','MD_pre','ME_pos','MD_pos']

    df_clean = df.copy()

    for grupo in df[fator].dropna().unique():

        mask = df[fator] == grupo

        dados = df.loc[mask, condicoes]

        Q1 = dados.quantile(0.25)
        Q3 = dados.quantile(0.75)

        IQR = Q3 - Q1

        limite_inf = Q1 - 1.5*IQR
        limite_sup = Q3 + 1.5*IQR

        for c in condicoes:

            out = (dados[c] < limite_inf[c]) | (dados[c] > limite_sup[c])

            df_clean.loc[mask & out, c] = np.nan

    return df_clean

# ======================================
# criar pastas novos gráficos
# ======================================

os.makedirs("graficos_sem_outlier_lesao", exist_ok=True)
os.makedirs("graficos_sem_outlier_etcc", exist_ok=True)


writer_lesao = pd.ExcelWriter("resultados_sem_outlier_lesao.xlsx", engine="openpyxl")
writer_etcc = pd.ExcelWriter("resultados_sem_outlier_etcc.xlsx", engine="openpyxl")


for col in colunas_novas:

    df_plot = pd.concat([control, dados_completos[col]], axis=1)

    df_plot = df_plot[['Fator_Lesao','Fator_ETCC',
                       'ME_pre','MD_pre','ME_pos','MD_pos']]

    df_plot[['ME_pre','MD_pre','ME_pos','MD_pos']] = df_plot[
        ['ME_pre','MD_pre','ME_pos','MD_pos']
    ].astype(float)


    # ==============================
    # remover outliers por LESÃO
    # ==============================

    df_lesao = remover_outliers(df_plot, "Fator_Lesao")

    df_lesao.to_excel(writer_lesao, sheet_name=col[:31])

    plotar_fator(df_lesao,
                 "Fator_Lesao",
                 col,
                 "graficos_sem_outlier_lesao")


    # ==============================
    # remover outliers por ETCC
    # ==============================

    df_etcc = remover_outliers(df_plot, "Fator_ETCC")

    df_etcc.to_excel(writer_etcc, sheet_name=col[:31])

    plotar_fator(df_etcc,
                 "Fator_ETCC",
                 col,
                 "graficos_sem_outlier_etcc")


writer_lesao.close()
writer_etcc.close()