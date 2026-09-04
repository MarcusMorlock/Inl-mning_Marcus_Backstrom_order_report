import pandas as pd
import logging

logger = logging.getLogger(__name__)

def validate_order_df(df: pd.DataFrame) -> pd.DataFrame:
        
    _required = {
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

    missing_columns = _required - set(df.columns) 

    if missing_columns:
        logger.error("Validation failed. Missing columns: %s", missing_columns)
        raise ValueError(f"Dataframe misses required columns: {missing_columns}")

    logger.info("Dataframe validated and contain required columns: %d", len(_required))

    return df