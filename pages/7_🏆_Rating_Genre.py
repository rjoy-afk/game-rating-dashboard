import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
from utils.helpers import render_sidebar
from utils.data_loader import load_clean_data
from utils.chart_style import setup_theme, style_chart, add_insight_box, TEXT_PRIMARY

st.set_page_config(page_title="Rating per Genre", page_icon="🏆", layout="wide")
render_sidebar()
setup_theme()

st.title("Story 5: Rating Rata-rata per Genre")
df_clean = load_clean_data()
genres_exploded = df_clean.explode('Genres_list')
genre_rating = genres_exploded.groupby('Genres_list').agg(Avg_Rating=('Rating', 'mean'), Count=('Title', 'count')).reset_index()
genre_rating = genre_rating[genre_rating['Count'] >= 20].sort_values('Avg_Rating', ascending=True)

fig, ax = plt.subplots(figsize=(14, 8))
n = len(genre_rating)
y_pos = range(n)
gradient = plt.cm.RdYlGn(np.linspace(0.15, 0.85, n))

for i, (_, row) in enumerate(zip(y_pos, genre_rating.iterrows())):
    _, row = row
    w = row['Avg_Rating'] - 2.5
    ax.barh(i, w, height=0.6, color=gradient[i], alpha=0.85, left=2.5, zorder=3)
    ax.barh(i, w, height=0.72, color=gradient[i], alpha=0.1, left=2.5, zorder=2)

ax.set_yticks(range(n))
ax.set_yticklabels(genre_rating['Genres_list'], fontsize=11, color=TEXT_PRIMARY)
ax.set_xlim(2.5, 4.7)
ax.set_xlabel('Rata-rata Rating', fontsize=11, labelpad=12)
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.2))

for i, (_, row) in enumerate(genre_rating.iterrows()):
    ax.text(row['Avg_Rating']+0.03, i, f"{row['Avg_Rating']:.2f} ({int(row['Count'])} game)", va='center', fontsize=10, color=TEXT_PRIMARY)

style_chart(ax, 'RATING RATA-RATA PER GENRE', 'Genre mana yang konsisten berkualitas? | Minimum 20 game per genre')

best = genre_rating.iloc[-1]
worst = genre_rating.iloc[0]
add_insight_box(fig, f"'{best['Genres_list']}' memiliki rata-rata rating tertinggi ({best['Avg_Rating']:.2f}), sementara '{worst['Genres_list']}' terendah ({worst['Avg_Rating']:.2f}).")

st.pyplot(fig)