"""Validating content"""

import pandas as pd
import logging


logger = logging.getLogger(__name__)


REQUIRED = frozenset({
    "order_id",
    "order_date",
    "customer_id",
    "region",
    "product_category",
    "quantity",
    "unit_price",
    "discount",
    "returned",
})

def validate_order_df(df: pd.DataFrame) -> pd.DataFrame:
        


    missing_columns = REQUIRED - set(df.columns) 

    if missing_columns:
        logger.error("Validation failed. Missing columns: %s", missing_columns)
        raise ValueError(f"Dataframe misses required columns: {missing_columns}")

    logger.info("Dataframe validated and contain required columns: %d", len(REQUIRED))

    return df