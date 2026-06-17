import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import textwrap
from utils.helpers import render_sidebar
from utils.data_loader import load_clean_data
from utils.chart_style import setup_theme, style_chart, add_insight_box, TEXT_PRIMARY

st.set_page_config(page_title="Top Developer", page_icon="🏢", layout="wide")
render_sidebar()
setup_theme()

st.title("Story 8: Developer/Studio Paling Produktif")
df_clean = load_clean_data()
teams_exploded = df_clean.explode('Team_list')
team_counts = teams_exploded['Team_list'].value_counts().head(12)

fig, ax = plt.subplots(figsize=(14, 8))
palette = plt.cm.cool(np.linspace(0.2, 0.85, len(team_counts)))[::-1]
n = len(team_counts)
y_pos = list(range(n-1, -1, -1))

for i, (y, (name, count)) in enumerate(zip(y_pos, team_counts.items())):
    ax.barh(y, count, height=0.69, color=palette[i], alpha=0.12, zorder=2)
    ax.barh(y, count, height=0.57, color=palette[i], alpha=0.85, zorder=3)

labels = [textwrap.fill(name, 28) for name in team_counts.index]
ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=10.5, color=TEXT_PRIMARY, va='center')
ax.set_xlabel('Jumlah Game Dirilis', fontsize=11, labelpad=12)

max_c = team_counts.max()
for i, (y, (name, count)) in enumerate(zip(y_pos, team_counts.items())):
    ax.text(count + max_c*0.02, y, f"{count} game", fontsize=11, fontweight='bold', color=palette[i], va='center')

ax.set_xlim(0, max_c * 1.2)
style_chart(ax, 'TOP 12 DEVELOPER / STUDIO PALING PRODUKTIF', 'Studio dengan jumlah game terbanyak di dataset')
add_insight_box(fig, f"'{team_counts.index[0]}' memimpin dengan {team_counts.values[0]} game dirilis.")

st.pyplot(fig)