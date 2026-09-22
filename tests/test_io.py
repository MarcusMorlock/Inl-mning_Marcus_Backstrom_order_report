"""Testing Loading and Saving Functions"""
import pytest
import logging

import pandas as pd


from pathlib import Path

from order_report import load_csv_to_dataframe

# test_log_file = tmp_path / "test_run.log"

def test_load_csv_to_dataframe(tmp_path: str | Path) -> None:
    csv_path = tmp_path / "order_report.csv"

    csv_path.write_text(
        """order_id,order_date,customer_id,region,product_category,quantity,unit_price,discount,returned
        \nO0001,2026-01-04,C018,South,Electronics,2.0,799.0,0.0,true
        \nO0002,2026-03-17,C028,North,Electronics,1.0,499.0,0.05,false""",
        encoding="utf-8"
    )

    expected = pd.DataFrame(
        {
            "order_id": ["O0001","O0002"],
            "order_date": ["2026-01-04","2026-03-17"],
            "customer_id": ["C018","C028"],
            "region": ["South","North"],
            "product_category": ["Electronics","Electronics"],
            "quantity" : [2.0, 1.0],
            "unit_price" : [799.0, 499.0],
            "discount" : [0,0,0.05],
            "returned" : [True, False]
        }
    )

    result = load_csv_to_dataframe(csv_path)

    pd.testing.assert_frame_equal(result, expected)
