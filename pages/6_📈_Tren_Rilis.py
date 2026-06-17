import streamlit as st
import matplotlib.pyplot as plt
from utils.helpers import render_sidebar
from utils.data_loader import load_clean_data
from utils.chart_style import setup_theme, style_chart, add_insight_box, ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE, BG_CARD, BORDER, TEXT_PRIMARY

st.set_page_config(page_title="Tren Rilis Game", page_icon="📈", layout="wide")
render_sidebar()
setup_theme()

st.title("Story 4: Tren Jumlah Rilis Game per Tahun")
df_clean = load_clean_data()
yearly = df_clean.groupby('Year').agg(Jumlah_Game=('Title', 'count'), Rata_Rata_Rating=('Rating', 'mean')).reset_index()
yearly = yearly[yearly['Year'] >= 1990]

fig, ax1 = plt.subplots(figsize=(16, 7))
bar_colors = [ACCENT_BLUE if y < 2020 else ACCENT_GREEN for y in yearly['Year']]
ax1.bar(yearly['Year'], yearly['Jumlah_Game'], color=bar_colors, alpha=0.7, width=0.8, zorder=3, label='Jumlah Game')
ax1.set_xlabel('Tahun', fontsize=11, labelpad=10)
ax1.set_ylabel('Jumlah Game Dirilis', fontsize=11, color=ACCENT_BLUE, labelpad=10)

ax2 = ax1.twinx()
ax2.plot(yearly['Year'], yearly['Rata_Rata_Rating'], color=ACCENT_ORANGE, linewidth=2.5, marker='o', markersize=4, label='Rata-rata Rating', zorder=4)
ax2.set_ylabel('Rata-rata Rating', fontsize=11, color=ACCENT_ORANGE, labelpad=10)
ax2.set_ylim(2.5, 5.0)
ax2.tick_params(axis='y', colors=ACCENT_ORANGE)
for spine in ['right', 'left', 'top', 'bottom']:
    ax2.spines[spine].set_visible(False)

style_chart(ax1, 'TREN JUMLAH RILIS GAME & RATA-RATA RATING PER TAHUN', 'Apakah industri game semakin produktif? | Data dari 1990-2023')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', facecolor=BG_CARD, edgecolor=BORDER, labelcolor=TEXT_PRIMARY, fontsize=10)

peak = yearly.loc[yearly['Jumlah_Game'].idxmax()]
add_insight_box(fig, f"Tahun {int(peak['Year'])} adalah tahun paling produktif dengan {int(peak['Jumlah_Game'])} game dirilis.")

st.pyplot(fig)