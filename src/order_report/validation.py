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

    return df