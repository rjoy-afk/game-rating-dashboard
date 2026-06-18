import streamlit as st
from utils.helpers import render_sidebar

st.set_page_config(
    page_title="Data Storytelling: Video Games",
    page_icon="🎮",
    layout="wide"
)

render_sidebar()

st.title("🎮 Data Storytelling: Video Games Dataset (1980-2023)")
st.write("""
Selamat datang di Dashboard Data Storytelling Video Games!  
Dataset ini berisi **1.512 game** dengan informasi rating, jumlah pemain, genre, developer, dan lainnya. 
Silakan navigasikan menu di sebelah kiri untuk melihat dataset awal, hasil pembersihan data, serta 8 visualisasi cerita data.
""")