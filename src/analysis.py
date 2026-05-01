def compute_metrics(df):
    df['Lost_Revenue'] = df['price'] * df['Stockout_count']

    brand_strategy = df.groupby('brand').agg({
        'Lost_Revenue': 'sum',
        'Stockout_rate': 'mean',
        'price': 'mean',
        'name': 'count'
    }).reset_index()

    return brand_strategy