import pandas as pd
from streamlit import cache_data
@cache_data
def load_data(): return pd.read_csv('data/games.csv')