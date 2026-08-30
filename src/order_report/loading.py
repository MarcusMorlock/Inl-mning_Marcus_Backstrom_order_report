""""""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_csv_to_dataframe(*path_segments: str | Path) -> pd.DataFrame:
    """Load csv from project map into dataframe using Pandas.

    Example:
        load_csv_to_dataframe("data", "orders.csv")
        load_csv_to_dataframe("data", "raw", "orders.csv")
    """

    file_path = PROJECT_ROOT.joinpath(*path_segments)

    # Check if file and folder is accurate and can be accessed
    if not file_path.is_file():
        relative_display = Path(*path_segments)
        raise FileNotFoundError(f"Filen saknas på sökvägen: {relative_display}")

    return pd.read_csv(file_path)

