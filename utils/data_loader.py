import pandas as pd
import streamlit as st
from utils.preprocessing import clean_data

@st.cache_data
def load_raw_data():
    return pd.read_csv('games.csv')

@st.cache_data
def load_clean_data():
    df = load_raw_data()
    return clean_data(df)