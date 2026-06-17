import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import textwrap
from utils.helpers import render_sidebar
from utils.data_loader import load_clean_data
from utils.chart_style import setup_theme, style_chart, add_insight_box, BORDER, ACCENT_GOLD, TEXT_PRIMARY, TEXT_SECONDARY

st.set_page_config(page_title="Plays vs Rating", page_icon="🔗", layout="wide")
render_sidebar()
setup_theme()

st.title("Story 7: Korelasi - Plays vs Rating")
df_clean = load_clean_data()

fig, ax = plt.subplots(figsize=(14, 8))
scatter = ax.scatter(df_clean['Plays'], df_clean['Rating'], alpha=0.35, c=df_clean['Rating'], cmap='RdYlGn', s=35, edgecolors=BORDER, linewidth=0.3, zorder=3)

top5 = df_clean.nlargest(5, 'Plays')
ax.scatter(top5['Plays'], top5['Rating'], s=120, facecolors='none', edgecolors=ACCENT_GOLD, linewidth=2, zorder=4)
for _, row in top5.iterrows():
    ax.annotate(textwrap.fill(row['Title'], 20), (row['Plays'], row['Rating']), fontsize=8.5, color=TEXT_PRIMARY, alpha=0.9, xytext=(12, 8), textcoords='offset points', arrowprops=dict(arrowstyle='->', color=TEXT_SECONDARY, lw=0.8))

ax.set_xlabel('Jumlah Plays', fontsize=11, labelpad=12)
ax.set_ylabel('Rating', fontsize=11, labelpad=12)
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}K'))

cbar = plt.colorbar(scatter, ax=ax, orientation='horizontal', pad=0.12, shrink=0.5, aspect=30)
cbar.set_label('Rating (warna titik)', color=TEXT_SECONDARY, fontsize=10)
cbar.ax.xaxis.set_tick_params(color=TEXT_SECONDARY)
plt.setp(plt.getp(cbar.ax.axes, 'xticklabels'), color=TEXT_SECONDARY)
cbar.outline.set_edgecolor(BORDER)

style_chart(ax, 'HUBUNGAN ANTARA JUMLAH PLAYS DAN RATING', 'Apakah game populer selalu berkualitas tinggi?')
ax.grid(axis='both', color='#21262D', linewidth=0.5, zorder=1)

corr = df_clean['Plays'].corr(df_clean['Rating'])
strength = 'lemah' if abs(corr) < 0.3 else ('sedang' if abs(corr) < 0.7 else 'kuat')
add_insight_box(fig, f"Korelasi Pearson = {corr:.3f} (korelasi {strength}). Game yang banyak dimainkan TIDAK selalu memiliki rating tinggi.")

st.pyplot(fig)