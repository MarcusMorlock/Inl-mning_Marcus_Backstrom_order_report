import pandas as pd


def validate_order_df(df: pd.DataFrame) -> pd.DataFrame:
        
    required = {
        "order_id",
        "order_date",
        "customer_id",
        "region",
        "product_category",
        "quantity",
        "unit_price",
        "discount",
        "returned",
    }
    if not required.issubset(df.columns):
        raise Exception("Fel data")
    
    return df