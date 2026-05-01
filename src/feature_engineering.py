import pandas as pd

import re

def get_brand(text):
    if not isinstance(text, str):
        return "Unknown"

    match = re.search(r'by ([A-Za-z& ]+)', text)
    
    if match:
        brand = match.group(1).strip()

        # Remove trailing unwanted words (like slogans)
        brand = re.sub(r'(If|Ready|Throw|Low|In|With|For).*', '', brand).strip()

        return brand

    return "Unknown"


def extract_brand(df):
    df['brand'] = df['description'].apply(get_brand)
    return df

def clean_brands(df):
    df = df.copy()

    # Remove very short or invalid brands
    df = df[df['brand'].str.len() > 2]

    # Remove weird patterns
    df = df[~df['brand'].str.contains(r'^[^a-zA-Z]+$', regex=True)]

    return df
    
def normalize_and_filter_brands(df, min_count=5):
    df = df.copy()

    brand_map = {

        'New' : 'New Look',
        'Vero': 'Vero Moda',
        'Native': 'Native Youth',
        'Carhartt': 'Carhartt WIP',
        'River': 'River Island',
        'Miss': 'Miss Selfridge',
        'TopshopWelcome': 'Topshop'
    }


    # Normalize brand names
    df.loc[:, 'brand'] = df['brand'].map(brand_map).fillna(df['brand'])

    # Filter low-frequency brands
    brand_counts = df['brand'].value_counts()
    valid_brands = brand_counts[brand_counts > 5].index

    df = df[df['brand'].isin(valid_brands)].copy()

    return df

def add_stockout_features(df):
    def get_num_outof_stock(size_str):
        if not isinstance(size_str, str):
            return 0, 0.0

        sizes = size_str.split(',')
        total = len(sizes)
        out_of_stock_count = size_str.count('Out of stock')

        return out_of_stock_count, out_of_stock_count / total

    df[['Stockout_count', 'Stockout_rate']] = df['size'].apply(
        lambda x: pd.Series(get_num_outof_stock(x))
    )

    return df