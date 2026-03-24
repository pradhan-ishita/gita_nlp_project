def select_best_verses(df, top_k=5):
    """
    Basic fallback selector:
    returns top_k rows from already ranked dataframe
    """
    if df is None or len(df) == 0:
        return []

    return df.head(top_k).to_dict(orient="records")