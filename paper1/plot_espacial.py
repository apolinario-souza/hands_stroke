import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

# =============================================================================
# LEITURA DOS DADOS
# =============================================================================

xl = pd.ExcelFile("data_figura_espacial.xlsx")

df_final_cm    = pd.read_excel(xl, sheet_name="P_final_cm")
df_final_graus = pd.read_excel(xl, sheet_name="P_final_graus")
df_1sub_cm     = pd.read_excel(xl, sheet_name="Posicao_1sub_cm")
df_1sub_graus  = pd.read_excel(xl, sheet_name="Posicao_1sub_graus")

# =============================================================================
# CÁLCULO X, Y
# =============================================================================

def to_xy(df_cm, df_graus):
    df = df_cm.copy().rename(columns={"valor": "r"})
    df["angulo"] = df_graus["valor"]
    df["x"] = df["r"] * np.cos(np.radians(df["angulo"]))
    df["y"] = df["r"] * np.sin(np.radians(df["angulo"]))
    return df[["sujeito", "Fator_Lesao", "lado", "x", "y"]]

df_final = to_xy(df_final_cm, df_final_graus)
df_1sub  = to_xy(df_1sub_cm,  df_1sub_graus)

# =============================================================================
# REFERÊNCIAS
# =============================================================================

alvo_x = 19.0 * np.cos(np.radians(45))  # ≈ 13.44
alvo_y = 19.0 * np.sin(np.radians(45))  # ≈ 13.44

# 3 grupos → 3 painéis
grupos = [
    ("sem_lesao", "NS"),
    ("Lesao_E",   "LS"),
    ("Lesao_D",   "RS"),
]

# mãos diferenciadas por cor
maos = {
    "ME": dict(color="#b45c20", label="LH"),
    "MD": dict(color="#b42078", label="RH"),
}

alpha_pts = 0.75
s_final   = 50   # círculo ●
s_1sub    = 35   # x

# =============================================================================
# FIGURA: 1 linha × 3 colunas
# =============================================================================

fig, axes = plt.subplots(1, 3, figsize=(17, 6))

for ax, (grupo_key, grupo_title) in zip(axes, grupos):

    
    # trajetória ideal
    ax.plot([0, alvo_x], [0, alvo_y],
            color="black", lw=1.2, ls="--", alpha=0.35, zorder=1)

    # origem
    ax.scatter(0, 0, s=130, color="black", zorder=7, marker="o")
    ax.annotate("home\n(0,0)", xy=(0, 0),
                xytext=(0.7, -1.1), fontsize=8, ha="center", color="black")

    # alvo
    ax.add_patch(plt.Circle((alvo_x, alvo_y), radius=0.5,
                             color="gold", ec="black", lw=1.5, zorder=6))
    ax.annotate(f"target\n({alvo_x:.1f}, {alvo_y:.1f})",
                xy=(alvo_x, alvo_y),
                xytext=(alvo_x + 1.0, alvo_y - 1.3),
                fontsize=8, ha="left", color="darkorange",
                arrowprops=dict(arrowstyle="-", color="darkorange", lw=0.8))

    # pontos por mão
    for mao, estilo in maos.items():
        cor = estilo["color"]

        # posição final → círculo ●
        fin = df_final[(df_final["Fator_Lesao"]==grupo_key) &
                       (df_final["lado"]==mao)].dropna(subset=["x","y"])
        ax.scatter(fin["x"], fin["y"],
                   c=cor, marker="o", s=s_final,
                   alpha=alpha_pts, zorder=5,
                   edgecolors="white", linewidths=0.5)

        # 1º submovimento → x
        sub = df_1sub[(df_1sub["Fator_Lesao"]==grupo_key) &
                      (df_1sub["lado"]==mao)].dropna(subset=["x","y"])
        ax.scatter(sub["x"], sub["y"],
                   c=cor, marker="x", s=s_1sub,
                   alpha=alpha_pts, zorder=5,
                   linewidths=1.2)

    #ax.set_xlim(xmin, xmax)
    #ax.set_ylim(ymin, ymax)
    ax.set_xlim(-1, 20)
    ax.set_ylim(-1, 18)
    ax.set_title(grupo_title, fontsize=13, fontweight="bold", pad=10)
    
    ax.set_xlabel("x (cm)", fontsize=11)
    ax.set_aspect("equal", adjustable="box")
    
    ax.spines[["top","right"]].set_visible(False)

axes[0].set_ylabel("y (cm)", fontsize=11)

# =============================================================================
# LEGENDA
# =============================================================================

legend_maos = [
    mpatches.Patch(color=v["color"], label=v["label"])
    for v in maos.values()
]

legend_tipo = [
    Line2D([0],[0], marker="o", color="gray", ls="none",
           markersize=7, label="Endpoint position"),
    Line2D([0],[0], marker="x", color="gray", ls="none",
           markersize=7, markeredgewidth=1.5, label="Position at the end of the 1st submovement"),
    
]

fig.legend(handles=legend_maos + legend_tipo,
           loc="lower center", ncol=6,
           fontsize=10, frameon=True,
           bbox_to_anchor=(0.5, -0.05))


plt.tight_layout()
plt.savefig("figura_espacial.png", dpi=300, bbox_inches="tight")
print("Figura salva.")
