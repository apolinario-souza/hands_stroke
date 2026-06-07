"""
Gráfico de médias marginais estimadas (estilo emmeans)
lesion x hand — para todas as abas do data.xlsx
Salva em figures/ com DPI 6000
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy import stats

FILE_PATH = 'data.xlsx'
OUT_DIR   = 'figures'
os.makedirs(OUT_DIR, exist_ok=True)

# ── Paleta e estilos por grupo de lesão ─────────────────────────────────────
LESION_STYLE = {
    'LS': {'color': '#2166AC', 'marker': 'o', 'label': 'LS'},
    'RS': {'color': '#D6604D', 'marker': 'o', 'label': 'RS'},
    'NS': {'color': '#777777', 'marker': 'o', 'label': 'NS'},
}

HAND_LABELS = {'LH': 'LH', 'RH': 'RH'}

def calc_emmeans(df):
    """
    Calcula médias marginais e IC 95% por (lesion, hand)
    usando o erro padrão da média por célula.
    """
    rows = []
    for (lesion, hand), grp in df.groupby(['lesion', 'hand']):
        vals = grp['valor'].dropna()
        n    = len(vals)
        if n < 2:
            continue
        mean = vals.mean()
        se   = vals.sem()
        t_crit = stats.t.ppf(0.975, df=n-1)
        rows.append({
            'lesion': lesion,
            'hand':   hand,
            'mean':   mean,
            'lower':  mean - t_crit * se,
            'upper':  mean + t_crit * se,
        })
    return pd.DataFrame(rows)


def spine_only(ax):
    """Remove grade, borda superior e direita."""
    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.8)
    ax.spines['bottom'].set_linewidth(0.8)


def plot_sheet(sheet_name, df, out_dir):
    em = calc_emmeans(df)
    if em.empty:
        print(f"  [PULADO] {sheet_name} — sem dados suficientes")
        return

    hand_order   = ['LH', 'RH']
    hand_x       = {h: i for i, h in enumerate(hand_order)}
    lesion_order = [l for l in ['LS', 'RS', 'NS'] if l in em['lesion'].unique()]

    fig, ax = plt.subplots(figsize=(5.5, 4.5))

    for lesion in lesion_order:
        sub = em[em['lesion'] == lesion].copy()
        sub = sub[sub['hand'].isin(hand_order)]
        sub['x'] = sub['hand'].map(hand_x)
        sub = sub.sort_values('x')

        style = LESION_STYLE.get(lesion, {'color': '#333333', 'marker': 'o', 'label': lesion})

        # Linha de conexão
        ax.plot(sub['x'], sub['mean'],
                color=style['color'], linewidth=1.4, zorder=2)

        # Barras de erro
        ax.errorbar(sub['x'], sub['mean'],
                    yerr=[sub['mean'] - sub['lower'], sub['upper'] - sub['mean']],
                    fmt='none',
                    color=style['color'],
                    capsize=4, capthick=1.2, linewidth=1.2, zorder=3)

        # Pontos
        ax.scatter(sub['x'], sub['mean'],
                   color=style['color'], marker=style['marker'],
                   s=60, zorder=4, label=style['label'])

    # Eixos
    ax.set_xticks([0, 1])
    ax.set_xticklabels([HAND_LABELS.get(h, h) for h in hand_order], fontsize=11)
    #ax.set_xlabel('Mão', fontsize=12, labelpad=6)
    #ax.set_ylabel('Média estimada', fontsize=12, labelpad=6)
    ax.tick_params(axis='both', labelsize=10)

   
    # Legenda
    ax.legend(title='', title_fontsize=10, fontsize=10,
              frameon=False, loc='upper right',
              bbox_to_anchor=(1.28, 1.0))

    spine_only(ax)

    plt.tight_layout(rect=[0, 0, 1, 0.88])

    out_path = os.path.join(out_dir, f'{sheet_name}.png')
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"  Salvo: {out_path}")


# ── Main ─────────────────────────────────────────────────────────────────────
xl = pd.read_excel(FILE_PATH, sheet_name=None)

print(f"Gerando gráficos para {len(xl)} abas...\n")

for sheet_name, df in xl.items():
    if not {'lesion', 'valor', 'hand'}.issubset(df.columns):
        print(f"  [PULADO] {sheet_name} — colunas ausentes")
        continue
    print(f"  Processando: {sheet_name}")
    plot_sheet(sheet_name, df, OUT_DIR)

print(f"\nPronto! Figuras salvas em: {os.path.abspath(OUT_DIR)}/")