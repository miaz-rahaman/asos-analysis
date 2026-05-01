import pandas as pd
def clean_data(df):
    df = df.copy()

    df.loc[:, 'price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df.dropna(subset=['price']).copy()

    df.loc[:, 'description'] = df['description'].astype(str)

    return df