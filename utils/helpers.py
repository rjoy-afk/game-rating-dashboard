import streamlit as st
import os

def render_sidebar():
    st.sidebar.markdown("### 🎓 Profil Mahasiswa")
    
    # Membungkus profil dalam elemen div HTML agar terlihat seperti 'Card'
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
    
    # Memberikan jarak kosong (spacer) agar logo terdorong ke bagian bawah
    st.sidebar.markdown("<br>" * 3, unsafe_allow_html=True)
    
    # ==========================================
    # BAGIAN PENAMBAHAN 2 GAMBAR / LOGO
    # ==========================================
    logo1_path = "assets/logo1.png"  # Ganti dengan nama file gambar pertama
    logo2_path = "assets/logo2.png"  # Ganti dengan nama file gambar kedua
    
    # Membagi sidebar menjadi 2 kolom dengan lebar seimbang
    col_img1, col_img2 = st.sidebar.columns(2)
    
    # Menampilkan gambar pertama di kolom kiri
    with col_img1:
        if os.path.exists(logo1_path):
            st.image(logo1_path, use_container_width=True)
        else:
            st.markdown("<p style='font-size: 10px; color: gray; text-align: center;'>[logo1.png]</p>", unsafe_allow_html=True)
            
    # Menampilkan gambar kedua di kolom kanan
    with col_img2:
        if os.path.exists(logo2_path):
            st.image(logo2_path, use_container_width=True)
        else:
            st.markdown("<p style='font-size: 10px; color: gray; text-align: center;'>[logo2.png]</p>", unsafe_allow_html=True)