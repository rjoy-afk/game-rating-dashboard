import streamlit as st
import os

def render_sidebar():
    st.sidebar.markdown("### 🎓 Profil Mahasiswa")
    
    profil_html = """
    <div style='background-color: #161B22; padding: 15px; border-radius: 10px; border: 1px solid #30363D; margin-bottom: 20px;'>
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
    st.sidebar.markdown("<br>" * 3, unsafe_allow_html=True)
    
    # ==========================================
    # PERBAIKAN PATH GAMBAR (ABSOLUTE PATH)
    # ==========================================
    # 1. Ambil path absolut dari folder tempat file helpers.py ini berada (folder utils)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Mundur satu level ke root folder, lalu masuk ke folder assets
    root_dir = os.path.dirname(current_dir)
    
    # 3. Rangkai path file secara absolut sesuai nama file di explorer Anda
    logo1_path = os.path.join(root_dir, "assets", "logo_uin.png")
    logo2_path = os.path.join(root_dir, "assets", "logo_mti.png")
    
    # Tampilkan ke dalam 2 kolom
    col_img1, col_img2 = st.sidebar.columns(2)
    
    with col_img1:
        if os.path.exists(logo1_path):
            st.image(logo1_path, use_container_width=True)
        else:
            st.error("Gagal load logo_uin.png")
            
    with col_img2:
        if os.path.exists(logo2_path):
            st.image(logo2_path, use_container_width=True)
        else:
            st.error("Gagal load logo_mti.png")