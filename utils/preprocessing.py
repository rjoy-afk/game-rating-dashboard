import pandas as pd
import numpy as np
import ast
import re

def convert_k(value):
    if isinstance(value, str):
        value = value.strip()
        if value.upper().endswith('K'):
            return int(float(value[:-1]) * 1000)
        else:
            try:
                return int(float(value.replace(',', '')))
            except ValueError:
                return np.nan
    return value

def base_title(t):
    t = re.sub(r'\s*[-:]\s*(The Final Cut|Special Edition|Game of the Year Edition|GOTY|'
               r'HD Edition|Remastered|Definitive Edition|Director\'s Cut|'
               r'Subsistence|Complete Edition|Enhanced Edition|Anniversary Edition).*$',
               '', t, flags=re.IGNORECASE)
    t = re.sub(r'\s*:\s*.+$', '', t)
    return t.strip()

def clean_data(df):
    cols_to_convert = ['Plays', 'Playing', 'Backlogs', 'Wishlist', 'Times Listed', 'Number of Reviews']
    for col in cols_to_convert:
        if col in df.columns:
            df[col] = df[col].apply(convert_k)

    if 'Release Date' in df.columns:
        df['Release Date'] = pd.to_datetime(df['Release Date'], format='mixed', errors='coerce')
        df['Year'] = df['Release Date'].dt.year

    if 'Genres' in df.columns:
        df['Genres_list'] = df['Genres'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])

    if 'Team' in df.columns:
        df['Team_list'] = df['Team'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])

    df_clean = df.dropna(subset=['Rating']).copy()

    if 'Title' in df_clean.columns:
        df_clean['Base_Title'] = df_clean['Title'].apply(base_title)
        df_clean = df_clean.sort_values('Plays', ascending=False)
        df_clean = df_clean.drop_duplicates(subset='Base_Title', keep='first')

    return df_clean