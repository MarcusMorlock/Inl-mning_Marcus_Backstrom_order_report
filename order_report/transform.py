"""Transform data"""

import pandas as pd

import logging 

from pathlib import Path

from .validation import validate_order_df


def sales_by_category(df: pd.DataFrame, category: str) -> pd.DataFrame:

    validated_df = validate_order_df(df=df)

    grouped_df = (
            validated_df.groupby(
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

    validated_df = validate_order_df(df=df)
    
    returns_by_category = (
        validated_df.groupby(
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

    validated_df = validate_order_df(df=df)

    total_sales = round(
        validated_df["discounted_value"].sum(),
        2,
    )
    number_of_orders = validated_df["order_id"].nunique()
    number_of_returns = int(validated_df["returned"].sum())

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