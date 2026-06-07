import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

# =============================================================================
# LEITURA DOS DADOS
# =============================================================================

xl = pd.ExcelFile("data_figura_temporal.xlsx")

def load(sheet):
    return pd.read_excel(xl, sheet_name=sheet).rename(columns={"valor": sheet})

key = ["sub", "lesion", "hand"]
df = (load("TR")
      .merge(load("TM"),   on=key, how="outer")
      .merge(load("TRPV"), on=key, how="outer")
      .merge(load("PV"),   on=key, how="outer")
      .merge(load("NC"),   on=key, how="outer"))

df = df.dropna(subset=["TR", "TM"])

df["t_trpv_abs"] = df["TR"] + df["TM"] * (df["TRPV"] / 100.0)
df["t_fim"]      = df["TR"] + df["TM"]
df["t_pv_abs"]   = df["TR"] + df["TM"] * (df["TRPV"] / 100.0) * 0.80

# =============================================================================
# CONFIGURAÇÃO
# =============================================================================

grupos = [
    ("NS", "NS"),
    ("LS", "LS"),
    ("RS", "RS"),
]

cores = {
    "RH": "#b45c20",
    "LH": "#b42078",
}

fig, axes = plt.subplots(1, 3, figsize=(18, 8), sharey=False)

for ax, (grupo_key, grupo_title) in zip(axes, grupos):

    d = df[df["lesion"] == grupo_key].copy()

    # lista de sujeitos únicos (ordem consistente)
    subs = sorted(d["sub"].unique())
    n_subs = len(subs)

    # cada sujeito ocupa 2 linhas: RH (y + 0.15) e LH (y - 0.15)
    # sujeitos espaçados de 0.6 em y
    gap_sub  = 0.6
    gap_mao  = 0.18   # distância entre RH e LH do mesmo sujeito

    ax.set_title(grupo_title, fontsize=13, fontweight="bold", pad=10)
    ax.set_xlabel("Time (ms)", fontsize=11)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(left=False, labelleft=False)
    ax.grid(axis="x", ls=":", alpha=0.4)

    for s_idx, sub in enumerate(subs):
        y_center = (n_subs - s_idx) * gap_sub   # de cima para baixo

        for mao, offset in [("RH", +gap_mao), ("LH", -gap_mao)]:
            yi  = y_center + offset
            cor = cores[mao]
            row = d[(d["sub"] == sub) & (d["hand"] == mao)]

            if row.empty:
                continue
            row = row.iloc[0]

            # barra TR
            ax.barh(yi, row["TR"], left=0,
                    height=0.10, color=cor, alpha=0.2, zorder=2)

            # barra TM
            ax.barh(yi, row["TM"], left=row["TR"],
                    height=0.10, color=cor, alpha=0.7, zorder=2)

            # "|" RTPV
            if not np.isnan(row.get("TRPV", np.nan)):
                ax.vlines(row["t_trpv_abs"], yi - 0.06, yi + 0.06,
                          color=cor, lw=2, zorder=4)

            # "x" correções (ND)
            if not np.isnan(row.get("NC", np.nan)) and not np.isnan(row["t_trpv_abs"]):
                nc_int  = max(1, int(round(row["NC"])))
                t_start = row["t_trpv_abs"]
                t_end   = row["t_fim"]
                if t_end > t_start:
                    t_corr = np.linspace(t_start, t_end, nc_int + 2)[1:-1]
                    ax.scatter(t_corr, [yi] * len(t_corr),
                               marker="x", s=22, color=cor,
                               linewidths=0.9, alpha=1, zorder=5)

            # "▲" PV
            if not np.isnan(row.get("PV", np.nan)) and not np.isnan(row.get("t_pv_abs", np.nan)):
                pv_norm = row["PV"] / 80.0
                ax.scatter(row["t_pv_abs"], yi,
                           s=pv_norm * 120, color=cor,
                           marker="^", alpha=0.7, zorder=6,
                           edgecolors="white", linewidths=0.4)

    ax.set_yticks([])
    # label do sujeito no centro entre RH e LH, dentro do painel
    for s_idx, sub in enumerate(subs):
        y_center = (n_subs - s_idx) * gap_sub
        ax.text(-25, y_center, f"S{sub}",
                fontsize=7.5, ha="right", va="center", color="gray")
    ax.set_xlim(-30, 1800)
    ax.set_ylim(gap_sub * 0.3, (n_subs + 0.5) * gap_sub)

# =============================================================================
# LEGENDA
# =============================================================================

legend_maos = [
    Line2D([0],[0], color=cores["RH"], lw=5, alpha=0.55, label="RH"),
    Line2D([0],[0], color=cores["LH"], lw=5, alpha=0.55, label="LH"),
]

legend_extra = [
    Line2D([0],[0], color="gray", lw=5, alpha=0.2,  label="RT"),
    Line2D([0],[0], color="gray", lw=5, alpha=0.55, label="MT"),
    Line2D([0],[0], color="gray", lw=1.5, marker="|", markersize=10,
           ls="none", label="RTPV"),
    Line2D([0],[0], color="gray", marker="x", markersize=7,
           ls="none", markeredgewidth=1.2, label="ND"),
    Line2D([0],[0], color="gray", marker="^", markersize=8,
           ls="none", alpha=0.8, label="PV"),
]

fig.legend(handles=legend_maos + legend_extra,
           loc="lower center", ncol=7,
           fontsize=9.5, frameon=True,
           bbox_to_anchor=(0.5, -0.04))

plt.tight_layout()
plt.savefig("figura_temporal.png", dpi=300, bbox_inches="tight")
print("Figura salva.")
