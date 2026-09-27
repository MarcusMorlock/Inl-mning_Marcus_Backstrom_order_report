"""Transform data"""

import pandas as pd

import logging 

from pathlib import Path



def sales_by_category(df: pd.DataFrame, category: str) -> pd.DataFrame:

    df_copy = df.copy()

    grouped_df = (
            df_copy.groupby(
                category,
                as_index=False,
            ).agg(
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
    

    return grouped_df


def returns_by_category(df: pd.DataFrame, category: str) -> pd.DataFrame:

    df_copy = df.copy()
    
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
        returns_by_category["returns"] / returns_by_category["order_count"]
    ).round(3)

    returns_by_category = (
        returns_by_category
        .sort_values(
            "return_rate",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    return returns_by_category

def overview(df: pd.DataFrame) -> pd.DataFrame:

    df_copy = df.copy()

    total_sales = round(
        df_copy["discounted_value"].sum(),
        2,
    )
    number_of_orders = df_copy["order_id"].nunique()
    number_of_returns = int(df_copy["returned"].sum())

    overview = pd.DataFrame(
        {
            "metric": [
                "total_sales",
                "order_count",
                "return_count",
            ],
            "value": [
                total_sales,
                number_of_orders,
                number_of_returns,
            ],
        }
    )

    return overview