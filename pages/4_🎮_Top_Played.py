import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import textwrap
from utils.helpers import render_sidebar
from utils.data_loader import load_clean_data
from utils.chart_style import setup_theme, style_chart, add_insight_box, BG_DARK, TEXT_PRIMARY, TEXT_SECONDARY

st.set_page_config(page_title="Top 10 Played", page_icon="🎮", layout="wide")
render_sidebar()
setup_theme()

st.title("Story 2: Top 10 Game Paling Banyak Dimainkan")
df_clean = load_clean_data()
top_played = df_clean.nlargest(10, 'Plays')[['Title', 'Plays', 'Rating', 'Year']].reset_index(drop=True)

fig, ax = plt.subplots(figsize=(14, 9))
palette = ['#58A6FF', '#539BF5', '#4E90EA', '#4985DF', '#447AD4', '#3F6FC9', '#3A64BE', '#3559B3', '#304EA8', '#2B439D']
n = len(top_played)
y_pos = list(range(n-1, -1, -1))

for i, (y, (_, row)) in enumerate(zip(y_pos, top_played.iterrows())):
    ax.barh(y, row['Plays'], height=0.69, color=palette[i], alpha=0.1, zorder=2)
    ax.barh(y, row['Plays'], height=0.57, color=palette[i], alpha=0.85, zorder=3)

labels = [f"{textwrap.fill(r['Title'], 26)}\n({int(r['Year'])})" for _, r in top_played.iterrows()]
ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=10.5, color=TEXT_PRIMARY, linespacing=1.1, va='center')
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}K'))
ax.set_xlabel('Jumlah Plays', fontsize=11, labelpad=12)

max_p = top_played['Plays'].max()
for i, (y, (_, row)) in enumerate(zip(y_pos, top_played.iterrows())):
    ax.text(row['Plays'] + max_p*0.02, y+0.1, f"{row['Plays']/1000:.1f}K", fontsize=13, fontweight='bold', color=palette[i], va='center')
    ax.text(row['Plays'] + max_p*0.02, y-0.17, f"Rating: {row['Rating']:.1f}", fontsize=9, color=TEXT_SECONDARY, va='center')
    ax.text(max_p*0.01, y, f"#{i+1}", fontsize=12, fontweight='bold', color=BG_DARK, va='center', zorder=5, alpha=0.5)

ax.set_xlim(0, max_p * 1.22)
style_chart(ax, 'TOP 10 GAME PALING BANYAK DIMAINKAN', 'Berdasarkan total plays | Dataset: 1,512 games (1980-2023)')
add_insight_box(fig, f"'{top_played.iloc[0]['Title']}' paling banyak dimainkan ({top_played.iloc[0]['Plays']/1000:.0f}K plays) dengan rating {top_played.iloc[0]['Rating']}. Game populer tidak selalu memiliki rating tertinggi.")

st.pyplot(fig)