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
    # KODE PELACAK ISI FOLDER (DEBUGGING)
    # ==========================================
    assets_dir = "assets"
    
    if os.path.exists(assets_dir):
        # Membaca file apa saja yang benar-benar ada di server
        files_in_server = os.listdir(assets_dir)
        st.sidebar.warning(f"File yang terbaca oleh server: {files_in_server}")
        
        # Mencoba load gambar berdasarkan nama persis yang Anda sebutkan
        col_img1, col_img2 = st.sidebar.columns(2)
        with col_img1:
            try:
                st.image(f"assets/logo_uin.png", use_container_width=True)
            except Exception:
                st.error("logo_uin.png gagal")
        with col_img2:
            try:
                st.image(f"assets/logo_mti.png", use_container_width=True)
            except Exception:
                st.error("logo_mti.png gagal")
                
    else:
        st.sidebar.error("Folder 'assets' sama sekali tidak ditemukan oleh server Streamlit.")