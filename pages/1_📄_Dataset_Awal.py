import streamlit as st
from utils.helpers import render_sidebar
from utils.data_loader import load_raw_data

st.set_page_config(page_title="Dataset Awal", page_icon="📄", layout="wide")
render_sidebar()

st.title("📄 Dataset Awal (Mentah)")
df = load_raw_data()
st.write(f"Total Baris: {df.shape[0]} | Total Kolom: {df.shape[1]}")
st.dataframe(df.head(100)) # Menampilkan 100 data pertama agar ringan