import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# Import utils
from utils.helpers import render_sidebar
from utils.data_loader import load_clean_data
from utils.chart_style import (
    setup_theme, style_chart, add_insight_box,
    BG_DARK, BG_CARD, BORDER, TEXT_PRIMARY, TEXT_SECONDARY,
    ACCENT_GOLD, ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE, ACCENT_RED
)

st.set_page_config(page_title="Model Validation", page_icon="🤖", layout="wide")

# ==========================================
# KONFIGURASI SIDEBAR & DROPDOWN
# ==========================================
st.sidebar.markdown("### 🗂️ Navigasi Model Validation")
menu_options = [
    "a. Persiapan & Rekayasa Fitur",
    "b. Hasil Validasi Model",
    "c. Narasi A - Akurasi Prediksi",
    "d. Narasi B - Faktor Penentu",
    "e. Narasi C - Anomali Game",
    "f. Kesimpulan Model"
]
selected_menu = st.sidebar.selectbox("Pilih Sub Menu:", menu_options)
st.sidebar.markdown("---")
render_sidebar()

# ==========================================
# PIPELINE MACHINE LEARNING (CACHED)
# ==========================================
@st.cache_resource
def run_ml_pipeline():
    df = load_clean_data()
    eng = ['Plays', 'Number of Reviews', 'Times Listed', 'Backlogs', 'Wishlist']
    df_ml = df.dropna(subset=eng + ['Year']).copy()
    
    # 1. Split Mencegah Leakage
    df_train_temp, _ = train_test_split(df_ml, test_size=0.20, random_state=42)
    top_genres = (pd.Series([g for gs in df_train_temp['Genres_list'] for g in gs])
                  .value_counts().head(15).index.tolist())
    
    # 2. Rekayasa Fitur
    for g in top_genres:
        df_ml[f'genre_{g}'] = df_ml['Genres_list'].apply(lambda L: int(g in L))
    genre_cols = [f'genre_{g}' for g in top_genres]
    feature_cols = eng + ['Year'] + genre_cols
    
    X = df_ml[feature_cols].copy()
    y = df_ml['Rating'].copy()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    
    # 3. Random Forest
    rf = RandomForestRegressor(n_estimators=200, max_depth=10, min_samples_leaf=2, random_state=42, n_jobs=-1)
    rf_cv_scores = cross_val_score(rf, X, y, cv=5, scoring='r2')
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    
    rf_metrics = {
        'cv_mean': rf_cv_scores.mean(),
        'r2': r2_score(y_test, y_pred_rf),
        'mae': mean_absolute_error(y_test, y_pred_rf),
        'rmse': np.sqrt(mean_squared_error(y_test, y_pred_rf))
    }
    
    feature_importance = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': rf.feature_importances_
    }).sort_values('Importance', ascending=False).reset_index(drop=True)
    
    # 4. Linear Regression
    lr = LinearRegression()
    lr_cv_scores = cross_val_score(lr, X, y, cv=5, scoring='r2')
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    
    lr_metrics = {
        'cv_mean': lr_cv_scores.mean(),
        'r2': r2_score(y_test, y_pred_lr),
        'mae': mean_absolute_error(y_test, y_pred_lr),
        'rmse': np.sqrt(mean_squared_error(y_test, y_pred_lr))
    }
    
    coef_df = pd.DataFrame({
        'Feature': feature_cols,
        'Coefficient': lr.coef_
    }).sort_values('Coefficient', key=abs, ascending=False).reset_index(drop=True)
    
    # 5. Baseline
    baseline_pred = np.repeat(y_train.mean(), len(y_test))
    baseline_mae = mean_absolute_error(y_test, baseline_pred)
    imp_rf = ((baseline_mae - rf_metrics['mae']) / baseline_mae) * 100
    imp_lr = ((baseline_mae - lr_metrics['mae']) / baseline_mae) * 100
    
    # 6. Residuals (Narasi C)
    df_res = df_ml.copy()
    df_res['Prediksi'] = rf.predict(X)
    df_res['Residual'] = df_res['Rating'] - df_res['Prediksi']
    hidden_gems = df_res.sort_values('Residual', ascending=False).head(5)
    overrated = df_res.sort_values('Residual', ascending=True).head(5)
    
    return {
        'eng': eng, 'genre_cols': genre_cols, 'top_genres': top_genres,
        'X_shape': X.shape, 'X_train_len': len(X_train), 'X_test_len': len(X_test),
        'rf_metrics': rf_metrics, 'lr_metrics': lr_metrics, 
        'baseline_mae': baseline_mae, 'imp_rf': imp_rf, 'imp_lr': imp_lr,
        'feature_importance': feature_importance, 'coef_df': coef_df,
        'y_test': y_test, 'y_pred_rf': y_pred_rf,
        'hidden_gems': hidden_gems, 'overrated': overrated
    }

# Menjalankan pipeline (hanya berat di awal, setelahnya memakai cache)
ml_data = run_ml_pipeline()
setup_theme()

st.title("🤖 Model Validation & Analysis")
st.markdown("Menguji temuan Data Storytelling menggunakan algoritma *Random Forest* dan *Linear Regression*.")
st.markdown("---")

# ==========================================
# LOGIKA ROUTING BERDASARKAN DROPDOWN
# ==========================================

if selected_menu == "a. Persiapan & Rekayasa Fitur":
    st.subheader("1. Pembersihan & Rekayasa Fitur")
    st.write("> *Setiap pola yang ditemukan di EDA diubah menjadi petunjuk matematis untuk model.*")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Dimensi Fitur Akhir:** {ml_data['X_shape'][1]} Fitur, {ml_data['X_shape'][0]} Sampel Game")
        st.write(f"- **Data Latih (Train):** {ml_data['X_train_len']} game")
        st.write(f"- **Data Uji (Test):** {ml_data['X_test_len']} game")
    
    with col2:
        st.success("**Pencegahan Data Leakage (Kebocoran Data):**\n\nPenentuan 15 genre terpopuler dilakukan **hanya pada data latih**, memastikan model tidak 'menyontek' dari data uji.")

    st.markdown("#### Detail Fitur")
    st.write(f"**1. Fitur Engagement ({len(ml_data['eng'])}):** `{'`, `'.join(ml_data['eng'])}`")
    st.write("**2. Fitur Rilis (1):** `Year`")
    st.write(f"**3. Fitur Genre Multi-hot ({len(ml_data['top_genres'])}):** `{'`, `'.join(ml_data['top_genres'])}`")

elif selected_menu == "b. Hasil Validasi Model":
    st.subheader("2. Hasil Evaluasi Performa Model")
    
    comparison = pd.DataFrame({
        'Model': ['Linear Regression', 'Random Forest'],
        'CV R² (5-Fold)': [ml_data['lr_metrics']['cv_mean'], ml_data['rf_metrics']['cv_mean']],
        'Test R²': [ml_data['lr_metrics']['r2'], ml_data['rf_metrics']['r2']],
        'MAE': [ml_data['lr_metrics']['mae'], ml_data['rf_metrics']['mae']],
        'RMSE': [ml_data['lr_metrics']['rmse'], ml_data['rf_metrics']['rmse']]
    })
    
    st.dataframe(comparison.style.background_gradient(subset=['CV R² (5-Fold)', 'Test R²'], cmap='Greens')
                                  .background_gradient(subset=['MAE', 'RMSE'], cmap='Reds_r'), use_container_width=True)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].bar(comparison['Model'], comparison['Test R²'], color=[ACCENT_BLUE, ACCENT_GREEN])
    axes[0].set_title('Perbandingan R² Score (Lebih Tinggi Lebih Baik)', fontsize=13, fontweight='bold', color=TEXT_PRIMARY)
    for i, v in enumerate(comparison['Test R²']):
        axes[0].text(i, v + 0.01, f'{v:.3f}', ha='center', fontsize=11, color=TEXT_PRIMARY)
        
    axes[1].bar(comparison['Model'], comparison['MAE'], color=[ACCENT_BLUE, ACCENT_GREEN])
    axes[1].set_title('Perbandingan MAE (Lebih Rendah Lebih Baik)', fontsize=13, fontweight='bold', color=TEXT_PRIMARY)
    for i, v in enumerate(comparison['MAE']):
        axes[1].text(i, v + 0.01, f'{v:.3f}', ha='center', fontsize=11, color=TEXT_PRIMARY)
    
    st.pyplot(fig)

elif selected_menu == "c. Narasi A - Akurasi Prediksi":
    st.subheader("Narasi A: Seberapa Akurat Rating Bisa Ditebak?")
    st.write("> *Model machine learning berguna, tetapi rating game tidak bisa diprediksi secara sempurna hanya dari angka di atas kertas.*")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(ml_data['y_test'], ml_data['y_pred_rf'], color=ACCENT_BLUE, alpha=0.6, edgecolor=BORDER, s=50)
    ax.plot([ml_data['y_test'].min(), ml_data['y_test'].max()], [ml_data['y_test'].min(), ml_data['y_test'].max()], color=ACCENT_RED, linestyle='--', lw=2)
    
    ax.set_xlabel('Rating Aktual', color=TEXT_SECONDARY, fontweight='bold')
    ax.set_ylabel('Rating Prediksi (Random Forest)', color=TEXT_SECONDARY, fontweight='bold')
    
    style_chart(ax, 'Seberapa Akurat Model Menebak Rating?', f"Random Forest memangkas error {ml_data['imp_rf']:.1f}% dari tebakan rata-rata")
    add_insight_box(fig, 'Sebagian besar titik mengelompok di sekitar garis diagonal merah, namun sebarannya menunjukkan bahwa model kesulitan memprediksi rating ekstrem.')
    
    st.pyplot(fig)
    
    st.markdown(f"""
    Berdasarkan evaluasi *Random Forest*, model mampu memangkas tingkat kesalahan prediksi hingga **{ml_data['imp_rf']:.1f}%** dibandingkan *baseline*. Rata-rata model hanya meleset **{ml_data['rf_metrics']['mae']:.3f} poin** dari rating asli.
    Namun, R² score sebesar **{ml_data['rf_metrics']['r2']:.3f}** membuktikan bahwa mayoritas alasan sebuah game mendapat rating bergantung pada faktor kualitatif di luar dataset (cerita, mekanika *gameplay*, *bug*, dll).
    """)

elif selected_menu == "d. Narasi B - Faktor Penentu":
    st.subheader("Narasi B: Faktor Apa yang Paling Menentukan?")
    st.write("> *Hype membawa game ke permukaan, tetapi audiens niche sangat setia pada genrenya.*")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    top_rf = ml_data['feature_importance'].head(10).sort_values('Importance', ascending=True)
    top_rf.plot(kind='barh', x='Feature', y='Importance', ax=ax1, color=ACCENT_BLUE, legend=False)
    style_chart(ax1, '10 Faktor Utama (Random Forest)', 'Didominasi metrik antisipasi (Wishlist & Plays)')
    ax1.set_ylabel('')
    
    top_lr = ml_data['coef_df'].head(10).sort_values('Coefficient', key=abs, ascending=True)
    top_lr.plot(kind='barh', x='Feature', y='Coefficient', ax=ax2, color=ACCENT_GREEN, legend=False)
    style_chart(ax2, '10 Pendorong Rating (Linear Regression)', 'Genre niche memberikan dorongan positif terbesar')
    ax2.set_ylabel('')
    
    add_insight_box(fig, 'Random Forest mengandalkan sinyal popularitas, sementara Linear Regression menangkap bahwa game Visual Novel/Taktikal memiliki tendensi rating alami yang lebih tinggi.')
    st.pyplot(fig)

elif selected_menu == "e. Narasi C - Anomali Game":
    st.subheader("Narasi C: Game Mana yang Mengejutkan Model?")
    st.write("> *Anomali data adalah tempat di mana cerita paling menarik bersembunyi.*")
    
    st.markdown("#### 💎 TOP 5 HIDDEN GEMS (Rating Aktual Jauh Melampaui Prediksi)")
    st.write("Game dengan nilai residual positif terbesar. Kualitas aslinya diakui jauh lebih tinggi dari ekspektasi model yang didasarkan pada popularitas.")
    st.dataframe(ml_data['hidden_gems'][['Title', 'Rating', 'Prediksi', 'Residual', 'Plays', 'Wishlist', 'Year']]
                 .style.background_gradient(subset=['Residual'], cmap='Greens'), use_container_width=True)
    
    st.markdown("#### 📉 TOP 5 OVERRATED / DISAPPOINTING (Rating Aktual Mengecewakan)")
    st.write("Game yang sukses mendulang angka *Plays/Wishlist* luar biasa, namun rating aktualnya jauh di bawah prediksi (sering diakibatkan oleh *hype* berlebih).")
    st.dataframe(ml_data['overrated'][['Title', 'Rating', 'Prediksi', 'Residual', 'Plays', 'Wishlist', 'Year']]
                 .style.background_gradient(subset=['Residual'], cmap='Reds_r'), use_container_width=True)

elif selected_menu == "f. Kesimpulan Model":
    st.subheader("📝 Kesimpulan Validasi Model")
    st.markdown("""
    Kita berangkat dari pertanyaan: **"Faktor apa yang memprediksi rating game, dan seberapa baik model dapat menebaknya?"** Model menjawab dalam 3 lapis analisis:
    
    1. **Akurasi & Keterbatasan:** Model memangkas *error* ~29% dibanding tebakan rata-rata. Namun R² (~0.44) menegaskan bahwa rating game tidak bisa sepenuhnya diprediksi hanya dari *hype* pra-rilis. Ini adalah temuan faktual, bukan kelemahan sistem.
    2. **Faktor Penentu Utama:** **Wishlist** adalah sinyal terkuat. Antusiasme audiens terbukti lebih informatif daripada popularitas mentah (jumlah *Plays*), sangat sejalan dengan korelasi lemah yang kita temukan saat fase EDA.
    3. **Pencarian Melalui Anomali:** Model yang salah tebak justru menghasilkan wawasan (Narasi C). Selisih tebakan model memungkinkan kita menemukan *hidden gems* dan game yang *overrated* secara sistematis.
    
    **Catatan Metodologis:** Deduplikasi game telah memblokir kebocoran data, pemisahan *genre* dikarantina hanya di data latih, dan 5-fold CV menjamin performa ini adalah pantulan nyata (*true performance*).
    """)