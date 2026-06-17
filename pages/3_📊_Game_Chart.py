import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import textwrap

# Mengambil fungsi dari folder utils
from utils.helpers import render_sidebar
from utils.data_loader import load_clean_data
from utils.chart_style import (
    setup_theme, style_chart, add_insight_box,
    BG_DARK, BG_CARD, BORDER, TEXT_PRIMARY, TEXT_SECONDARY,
    ACCENT_GOLD, ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE
)

st.set_page_config(page_title="Game Chart", page_icon="📊", layout="wide")

# 1. Render Identitas di Sidebar
render_sidebar()

# 2. Tambahkan Dropdown Menu di Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 🗂️ Navigasi Sub Menu")
menu_options = [
    "a. Top 10 Game dengan Rating Tertinggi",
    "b. Top 10 Game Paling Banyak Dimainkan",
    "c. Genre Game Terpopuler",
    "d. Tren Jumlah Rilis Game per Tahun",
    "e. Rating Rata-rata per Genre",
    "f. Top 10 Game Paling Banyak Di-Wishlist",
    "g. Korelasi - Plays vs Rating",
    "h. Developer/Studio Paling Produktif",
    "i. Kesimpulan"
]
selected_menu = st.sidebar.selectbox("Pilih Chart:", menu_options)

# Load data & Set Theme Matplotlib
df_clean = load_clean_data()
setup_theme()

st.title("📊 Game Chart & Analysis")
st.markdown("Gunakan **dropdown di sidebar sebelah kiri** untuk menavigasi antar cerita data (Story) dan Kesimpulan.")
st.markdown("---")

# ==========================================
# LOGIKA ROUTING BERDASARKAN DROPDOWN
# ==========================================

if selected_menu == "a. Top 10 Game dengan Rating Tertinggi":
    st.subheader("Story 1: Top 10 Game dengan Rating Tertinggi")
    st.write("> *Game apa yang dinilai paling tinggi oleh para pemain?*")
    
    df_dedup = df_clean.sort_values(['Base_Title', 'Rating', 'Plays'], ascending=[True, False, False]).drop_duplicates(subset='Base_Title', keep='first')
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

elif selected_menu == "b. Top 10 Game Paling Banyak Dimainkan":
    st.subheader("Story 2: Top 10 Game Paling Banyak Dimainkan")
    st.write("> *Game mana yang paling banyak dimainkan?*")
    
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
    add_insight_box(fig, f"'{top_played.iloc[0]['Title']}' paling banyak dimainkan dengan rating {top_played.iloc[0]['Rating']}.")
    st.pyplot(fig)

elif selected_menu == "c. Genre Game Terpopuler":
    st.subheader("Story 3: Genre Game Terpopuler")
    
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

    style_chart(ax, 'GENRE GAME TERPOPULER', 'Frekuensi genre di seluruh dataset')
    ax.grid(axis='y', color='#21262D', linewidth=0.5, zorder=1)
    ax.grid(axis='x', visible=False)
    add_insight_box(fig, f"Genre '{genre_counts.index[0]}' mendominasi dengan {genre_counts.values[0]} game.")
    st.pyplot(fig)

elif selected_menu == "d. Tren Jumlah Rilis Game per Tahun":
    st.subheader("Story 4: Tren Jumlah Rilis Game per Tahun")
    
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

    style_chart(ax1, 'TREN JUMLAH RILIS GAME & RATA-RATA RATING PER TAHUN')
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', facecolor=BG_CARD, edgecolor=BORDER, labelcolor=TEXT_PRIMARY, fontsize=10)

    peak = yearly.loc[yearly['Jumlah_Game'].idxmax()]
    add_insight_box(fig, f"Tahun {int(peak['Year'])} adalah tahun paling produktif dengan {int(peak['Jumlah_Game'])} game dirilis.")
    st.pyplot(fig)

elif selected_menu == "e. Rating Rata-rata per Genre":
    st.subheader("Story 5: Rating Rata-rata per Genre")
    
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

    style_chart(ax, 'RATING RATA-RATA PER GENRE', 'Minimum 20 game per genre')
    best = genre_rating.iloc[-1]
    add_insight_box(fig, f"'{best['Genres_list']}' memiliki rata-rata rating tertinggi ({best['Avg_Rating']:.2f}).")
    st.pyplot(fig)

elif selected_menu == "f. Top 10 Game Paling Banyak Di-Wishlist":
    st.subheader("Story 6: Top 10 Game Paling Banyak Di-Wishlist")
    
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
    style_chart(ax, 'TOP 10 GAME PALING BANYAK DI-WISHLIST')
    add_insight_box(fig, f"'{top_wishlist.iloc[0]['Title']}' menjadi game paling banyak di-wishlist ({top_wishlist.iloc[0]['Wishlist']/1000:.1f}K).")
    st.pyplot(fig)

elif selected_menu == "g. Korelasi - Plays vs Rating":
    st.subheader("Story 7: Korelasi - Plays vs Rating")
    
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

elif selected_menu == "h. Developer/Studio Paling Produktif":
    st.subheader("Story 8: Developer/Studio Paling Produktif")
    
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
    style_chart(ax, 'TOP 12 DEVELOPER / STUDIO PALING PRODUKTIF')
    add_insight_box(fig, f"'{team_counts.index[0]}' memimpin dengan {team_counts.values[0]} game dirilis.")
    st.pyplot(fig)

elif selected_menu == "i. Kesimpulan":
    st.subheader("📝 Kesimpulan Analisis")
    st.markdown("""
    Dari 8 cerita data yang kita eksplorasi, berikut adalah temuan utamanya:
    
    1. **Rating tertinggi** tidak selalu dimiliki oleh game yang paling populer.
    2. **Genre RPG dan Adventure** mendominasi baik dari segi jumlah maupun kualitas.
    3. **Korelasi antara popularitas dan rating** cenderung lemah — banyak dimainkan bukan berarti berkualitas tinggi.
    4. **Wishlist tinggi** menandakan hype besar dari komunitas, namun belum tentu rating tinggi setelah dimainkan.
    5. **Tren produksi game** meningkat pesat sejak era 2010-an seiring mudahnya akses alat developer.
    6. Beberapa **studio besar** secara konsisten merilis banyak game dalam dataset ini.
    7. **Game klasik** seperti *Chrono Trigger (1995)* masih masuk Top 10 rating, membuktikan kualitas lintas generasi.

    Dataset ini membuktikan bahwa industri game sangat dinamis, dan setiap metrik (rating, plays, wishlist) menceritakan cerita yang berbeda tentang standar kesuksesan sebuah karya game.
    """)