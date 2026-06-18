import streamlit as st

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
    st.sidebar.markdown("<br>" * 1, unsafe_allow_html=True)
    
    # Menampilkan Logo
    col_img1, col_img2 = st.sidebar.columns(2)
    
    with col_img1:
        try:
            st.image("Assets/logo_uin.png", use_container_width=True)
        except Exception:
            pass # Menyembunyikan pesan error jika sewaktu-waktu gagal load
            
    with col_img2:
        try:
            st.image("Assets/logo_mti.png", use_container_width=True)
        except Exception:
            pass