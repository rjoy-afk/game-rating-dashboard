import streamlit as st
import base64
import os

def render_sidebar():
    # ==========================================
    # 1. GAMBAR DI PALING ATAS SIDEBAR (CSS HACK)
    # ==========================================
    # Path gambar (sesuaikan dengan games_transparent.png jika ada)
    img_path = "Assets/games.png" 
    
    if os.path.exists(img_path):
        # Membaca file gambar dan mengubahnya ke Base64
        with open(img_path, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()

        # Menyuntikkan CSS untuk menaruh gambar di blok navigasi teratas
        st.markdown(
            f"""
            <style>
            [data-testid="stSidebarNav"]::before {{
                content: "";
                display: block;
                background-image: url("data:image/png;base64,{encoded_string}");
                background-size: contain;
                background-repeat: no-repeat;
                background-position: center;
                height: 120px; /* Anda bisa menyesuaikan tinggi gambar di sini */
                margin-bottom: 20px;
                margin-top: 10px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    # ==========================================
    # 2. PROFIL MAHASISWA
    # ==========================================
    st.sidebar.markdown("### 🎓 Profil Mahasiswa")
    
    profil_html = """
    <div style='background-color: #161B22; padding: 15px; border-radius: 10px; border: 1px solid #30363D; margin-bottom: 10px;'>
        <div style='margin-bottom: 10px;'>
            <b style='color: #E6EDF3; font-size: 1.05em;'>1. Wandy Hanyudha</b><br>
            <span style='color: #8B949E; font-size: 0.9em;'>NIM: 2250420010</span>
        </div>
        <div style='margin-bottom: 15px;'>
            <b style='color: #E6EDF3; font-size: 1.05em;'>2. Rizal Wiedha Verika</b><br>
            <span style='color: #8B949E; font-size: 0.9em;'>NIM: 2250420012</span>
        </div>
        <hr style='border: 0; border-top: 1px solid #30363D; margin: 10px 0;'>
        <div style='color: #E6EDF3; font-size: 0.9em; line-height: 1.4;'>
            <b>Program Studi:</b><br>
            Magister Teknologi Informasi<br>
            <i style='color: #8B949E;'>UIN Syarif Hidayatullah Jakarta</i>
        </div>
    </div>
    """
    st.sidebar.markdown(profil_html, unsafe_allow_html=True)
    
    # ==========================================
    # 3. LOGO BAWAH (UIN & MTI)
    # ==========================================
    col_img1, col_img2 = st.sidebar.columns(2)
    
    with col_img1:
        try:
            st.image("Assets/logo_uin.png", use_container_width=True)
        except Exception:
            pass 
            
    with col_img2:
        try:
            st.image("Assets/logo_mti.png", use_container_width=True)
        except Exception:
            pass