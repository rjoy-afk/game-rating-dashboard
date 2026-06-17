import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from utils.helpers import render_sidebar
from utils.data_loader import load_clean_data
from utils.chart_style import setup_theme, style_chart, add_insight_box, TEXT_PRIMARY

st.set_page_config(page_title="Genre Terpopuler", page_icon="📚", layout="wide")
render_sidebar()
setup_theme()

st.title("Story 3: Genre Game Terpopuler")
df_clean = load_clean_data()
genres_exploded = df_clean.explode('Genres_list')
genre_counts = genres_exploded['Genres_list'].value_counts().head(12)

fig, ax = plt.subplots(figsize=(14, 7))
palette = plt.cm.viridis(np.linspace(0.3, 0.9, len(genre_counts)))

bars = ax.bar(range(len(genre_counts)), genre_counts.values, color=palette, width=0.7, edgecolor='none', zorder=3, alpha=0.85)
for bar, c in zip(bars, palette):
    ax.bar(bar.get_x() + bar.get_width()/2, bar.get_height(), width=bar.get_width()+0.1, color=c, alpha=0.1, zorder=2)

ax.set_xticks(range(len(genre_counts)))
ax.set_xticklabels(genre_counts.index, rotation=40, ha='right', fontsize=10.5, color=TEXT_PRIMARY)
ax.set_ylabel('Jumlah Game', fontsize=11, labelpad=10)

for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8, f'{int(bar.get_height())}', ha='center', va='bottom', fontweight='bold', fontsize=10, color=TEXT_PRIMARY)

style_chart(ax, 'GENRE GAME TERPOPULER', 'Frekuensi genre di seluruh dataset | Satu game bisa memiliki beberapa genre')
ax.grid(axis='y', color='#21262D', linewidth=0.5, zorder=1)
ax.grid(axis='x', visible=False)

add_insight_box(fig, f"Genre '{genre_counts.index[0]}' mendominasi dengan {genre_counts.values[0]} game, diikuti '{genre_counts.index[1]}' ({genre_counts.values[1]}) dan '{genre_counts.index[2]}' ({genre_counts.values[2]}).")

st.pyplot(fig)