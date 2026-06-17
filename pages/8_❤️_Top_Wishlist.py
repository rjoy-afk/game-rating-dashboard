import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import textwrap
from utils.helpers import render_sidebar
from utils.data_loader import load_clean_data
from utils.chart_style import setup_theme, style_chart, add_insight_box, BG_DARK, TEXT_PRIMARY, TEXT_SECONDARY

st.set_page_config(page_title="Top Wishlist", page_icon="❤️", layout="wide")
render_sidebar()
setup_theme()

st.title("Story 6: Top 10 Game Paling Banyak Di-Wishlist")
df_clean = load_clean_data()
df_wish_dedup = df_clean.sort_values(['Base_Title', 'Wishlist'], ascending=[True, False]).drop_duplicates(subset='Base_Title', keep='first')
top_wishlist = df_wish_dedup.nlargest(10, 'Wishlist')[['Title', 'Wishlist', 'Plays', 'Rating', 'Year']].reset_index(drop=True)

fig, ax = plt.subplots(figsize=(14, 9))
palette = plt.cm.magma(np.linspace(0.3, 0.85, 10))[::-1]
n = len(top_wishlist)
y_pos = list(range(n-1, -1, -1))

for i, (y, (_, row)) in enumerate(zip(y_pos, top_wishlist.iterrows())):
    ax.barh(y, row['Wishlist'], height=0.69, color=palette[i], alpha=0.12, zorder=2)
    ax.barh(y, row['Wishlist'], height=0.57, color=palette[i], alpha=0.85, zorder=3)

labels = [f"{textwrap.fill(r['Title'], 26)}\n({int(r['Year'])})" for _, r in top_wishlist.iterrows()]
ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=10.5, color=TEXT_PRIMARY, linespacing=1.1, va='center')
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}K'))
ax.set_xlabel('Jumlah Wishlist', fontsize=11, labelpad=12)

max_w = top_wishlist['Wishlist'].max()
for i, (y, (_, row)) in enumerate(zip(y_pos, top_wishlist.iterrows())):
    ax.text(row['Wishlist'] + max_w*0.02, y+0.1, f"{row['Wishlist']/1000:.1f}K", fontsize=13, fontweight='bold', color=palette[i], va='center')
    ax.text(row['Wishlist'] + max_w*0.02, y-0.17, f"Rating: {row['Rating']:.1f} | {row['Plays']/1000:.1f}K plays", fontsize=9, color=TEXT_SECONDARY, va='center')
    ax.text(max_w*0.01, y, f"#{i+1}", fontsize=12, fontweight='bold', color=BG_DARK, va='center', zorder=5, alpha=0.5)

ax.set_xlim(0, max_w * 1.25)
style_chart(ax, 'TOP 10 GAME PALING BANYAK DI-WISHLIST', 'Game yang paling ditunggu-tunggu oleh para gamer')
add_insight_box(fig, f"'{top_wishlist.iloc[0]['Title']}' menjadi game paling banyak di-wishlist ({top_wishlist.iloc[0]['Wishlist']/1000:.1f}K).")

st.pyplot(fig)