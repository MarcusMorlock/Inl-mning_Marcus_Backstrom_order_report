
import pandas as pd

import logging

from .validation import validate_order_df

def overview_order_report_dataframe (df: pd.DataFrame, fill_na: bool = True) -> pd.DataFrame:
    """
        If fill_na is true unit_price and quantity and discount will be filled any NA in code.

    """
    logger = logging.getLogger(__name__)

    validated_df = validate_order_df(df=df)

    str_cols = ["region", "product_category"]

    for col in str_cols:
        validated_df[col] = (
            validated_df[col].fillna("Unknown").astype(str).str.strip().str.title()
        )

    num_cols = ["quantity", "unit_price", "discount"]

    for col in num_cols:
        validated_df[col] = pd.to_numeric(
            validated_df[col], errors="coerce"
        )

    if fill_na:
        logger.info("Fill unit_price NA with median.")
        validated_df["unit_price"] = validated_df["unit_price"].fillna(
            validated_df["unit_price"].median()
        )
        # As unit_price is filled with median this is not a report able to be used for any legal usage as it´s falsified information.
        logger.warning("unit_price HAVE BEEN FILLED WITH MEDIAN CANNOT BE USED FOR LEGAL USAGE.")

    if fill_na:
        logger.info("Fill quantity NA with 1, fill discount NA with 0")
        validated_df = validated_df.fillna({"quantity": 1, "discount": 0})


    validated_df["returned"] = (
        validated_df["returned"]
        .fillna("false")
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "yes", "1", "ja"])
    )

    validated_df["order_value"] = (
        validated_df["quantity"] * validated_df["unit_price"]
    )

    validated_df["discounted_value"] = (
        validated_df["order_value"] * (1 - validated_df["discount"])
    )

    return validated_df