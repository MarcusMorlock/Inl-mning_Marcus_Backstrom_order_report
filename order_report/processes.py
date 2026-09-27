
import pandas as pd

from .validation import validate_order_df

def overview_order_report_dataframe (df: pd.DataFrame) -> pd.DataFrame:

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
    
    validated_df["unit_price"] = validated_df["unit_price"].fillna(
        validated_df["unit_price"].median()
    )

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