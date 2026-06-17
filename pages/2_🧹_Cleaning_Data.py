import streamlit as st
from utils.helpers import render_sidebar
from utils.data_loader import load_clean_data

st.set_page_config(page_title="Cleaning Data", page_icon="🧹", layout="wide")
render_sidebar()

st.title("🧹 Dataset Hasil Cleaning")
df_clean = load_clean_data()
st.write(f"Data setelah cleaning: {len(df_clean)} game")
st.write(f"Rentang tahun: {int(df_clean['Year'].min())} - {int(df_clean['Year'].max())}")
st.dataframe(df_clean[['Title', 'Rating', 'Plays', 'Wishlist', 'Year', 'Genres']].head(100))