import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import textwrap
from utils.helpers import render_sidebar
from utils.data_loader import load_clean_data
from utils.chart_style import setup_theme, style_chart, add_insight_box, BG_DARK, TEXT_PRIMARY, TEXT_SECONDARY

st.set_page_config(page_title="Top 10 Rating", page_icon="⭐", layout="wide")
render_sidebar()
setup_theme()

st.title("Story 1: Top 10 Game dengan Rating Tertinggi")
st.write("> *Game apa yang dinilai paling tinggi oleh para pemain?*")

df_clean = load_clean_data()
df_dedup = df_clean.sort_values(['Base_Title', 'Rating', 'Plays'], ascending=[True, False, False])
df_dedup = df_dedup.drop_duplicates(subset='Base_Title', keep='first')
top_rated = (df_dedup[df_dedup['Plays'] >= 500].sort_values(['Rating', 'Plays'], ascending=[False, False]).head(10).reset_index(drop=True))

fig, ax = plt.subplots(figsize=(14, 9))
colors = ['#FFD700', '#FFC107', '#FFB300', '#FFA000', '#FF8F00', '#FF7043', '#EF6C00', '#E65100', '#D84315', '#BF360C']
n = len(top_rated)
y_pos = list(range(n-1, -1, -1))
x_min = 3.0

for i, (y, (_, row)) in enumerate(zip(y_pos, top_rated.iterrows())):
    w = row['Rating'] - x_min
    ax.barh(y, w, height=0.67, color=colors[i], alpha=0.1, left=x_min, zorder=2)
    ax.barh(y, w, height=0.55, color=colors[i], alpha=0.85, left=x_min, zorder=3)

labels = [f"{textwrap.fill(r['Title'], 26)}\n({int(r['Year'])})" for _, r in top_rated.iterrows()]
ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=10.5, color=TEXT_PRIMARY, linespacing=1.1, va='center')
ax.set_xlim(x_min, 5.2)
ax.set_xlabel('Rating', fontsize=11, labelpad=12)
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.2))

for i, (y, (_, row)) in enumerate(zip(y_pos, top_rated.iterrows())):
    ax.text(row['Rating']+0.04, y+0.1, f"{row['Rating']:.1f}", fontsize=14, fontweight='bold', color=colors[i], va='center')
    ax.text(row['Rating']+0.04, y-0.17, f"{row['Plays']/1000:.1f}K plays", fontsize=9, color=TEXT_SECONDARY, va='center')
    ax.text(x_min+0.05, y, f"#{i+1}", fontsize=12, fontweight='bold', color=BG_DARK, va='center', zorder=5, alpha=0.5)

style_chart(ax, 'TOP 10 GAME DENGAN RATING TERTINGGI', 'Berdasarkan rating pengguna (min. 500 plays) | Dataset: 1,512 games (1980-2023)')
add_insight_box(fig, f"9 dari 10 game teratas berbagi rating 4.6. Yang membedakan adalah jumlah plays. '{top_rated.iloc[0]['Title']}' memimpin dengan {top_rated.iloc[0]['Plays']/1000:.1f}K plays.")

st.pyplot(fig)