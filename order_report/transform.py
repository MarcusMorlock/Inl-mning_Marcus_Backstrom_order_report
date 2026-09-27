"""Transform data, sort by."""

import pandas as pd

import logging 

from pathlib import Path
from order_report import save_from_dataframe_to_csv


def save_csv_sales_by_category(df: pd.DataFrame, output_path: str | Path, category: str) -> None:

    output_path = Path(output_path)

    df_copy = df.copy()

    grouped_df = (
            df_copy.groupby(
                category,
                as_index=False,
            )
            .agg(
                order_count=("order_id", "nunique"),
                total_sales=("discounted_value", "sum"),
                returns=("returned", "sum"),
            )
        )
    
    grouped_df["total_sales"] = (
            grouped_df["total_sales"].round(2)
        )
    
    grouped_df["return_rate"] = (
            grouped_df["returns"]
            / grouped_df["order_count"]
        ).round(3)
    
    grouped_df = (
            grouped_df
            .sort_values(
                "total_sales",
                ascending=False,
            )
            .reset_index(drop=True)
        )
    

    save_from_dataframe_to_csv(grouped_df, output_path)


def save_csv_returns_by_category(df: pd.DataFrame, output_path: str | Path, category: str) -> None:

    output_path = Path(output_path)

    df_copy = df.copy

    returns_by_category = (
        df_copy.groupby(
            category,
            as_index=False,
        )
        .agg(
            order_count=("order_id", "nunique"),
            returns=("returned", "sum"),
        )
    )

    returns_by_category["return_rate"] = (
        returns_by_category["returns"]
        / returns_by_category["order_count"]
    ).round(3)

    returns_by_category = (
        returns_by_category
        .sort_values(
            "return_rate",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    save_from_dataframe_to_csv(returns_by_category, output_path)

    return None