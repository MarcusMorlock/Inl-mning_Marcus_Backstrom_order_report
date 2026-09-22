"""Testing Loading and Saving Functions"""
import pytest
import logging

import pandas as pd


from pathlib import Path
from unittest.mock import patch

from order_report import load_csv_to_dataframe, save_from_dataframe_to_csv

#Test load_csv_to_dataframe

def test_load_csv_success(tmp_path: str | Path) -> None:
    csv_path = tmp_path / "order_report.csv"

    csv_path.write_text(
    "order_id,order_date,customer_id,region,product_category,quantity,unit_price,discount,returned\n"
    "O0001,2026-01-04,C018,South,Electronics,2.0,799.0,0.0,true\n"
    "O0002,2026-03-17,C028,North,Electronics,1.0,499.0,0.05,false",
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
            "discount" : [0.0,0.05],
            "returned" : [True, False]
        }
    )

    result = load_csv_to_dataframe(csv_path)

    pd.testing.assert_frame_equal(result, expected)


def test_load_csv_file_found_raises_error() -> None:
    with pytest.raises(FileNotFoundError, match="File not found at:"
                       ): load_csv_to_dataframe("empty")

def test_load_csv_empty_dataframe(tmp_path) -> None:
    csv_path = tmp_path / "empty_rows.csv"
    csv_path.write_text("order_id,order_date\n", encoding="utf-8")

    with pytest.raises(ValueError, match="CSV File Empty:"):
        load_csv_to_dataframe(csv_path)

def test_load_csv_zero_bytes(tmp_path) -> None:
    csv_path = tmp_path / "zero_bytes.csv"
    csv_path.touch()

    with pytest.raises(ValueError, match="File does not contain CSV Data:"):
        load_csv_to_dataframe(csv_path)

#Test save_from_dataframe_to_csv

def test_save_from_dataframe_to_csv(tmp_path) -> None:

    csv_path = tmp_path / "save_test.csv"

    data = pd.DataFrame(
        {
            "test_str": ["test","Test"],
            "test_int": [1, 5]
        }
    )

    save_from_dataframe_to_csv(data, csv_path)

    assert csv_path.exists()

def test_save_from_dataframe_to_csv_folder_creation(tmp_path) -> None:

    folder = tmp_path / "subfolder"
    file_path = folder / "save_test.csv"

    data = pd.DataFrame(
            {
                "test_str": ["test","Test"],
                "test_int": [1, 5]
            }
        )

    assert not folder.exists()

    save_from_dataframe_to_csv(data, file_path=file_path)

    assert file_path.exists()

def test_save_from_dataframe_raises_runtime_error_on_os_error(tmp_path) -> None:
    df = pd.DataFrame({"a": [1, 2]})
    file_path = tmp_path / "test.csv"

    with patch.object(pd.DataFrame, "to_csv", side_effect=PermissionError("Permission denied")):
        with pytest.raises(RuntimeError, match="Could not save csv file to"):
            save_from_dataframe_to_csv(df, file_path)