""""""

from pathlib import Path
import pandas as pd
import logging

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_csv_to_dataframe(file_path: str | Path) -> pd.DataFrame:

    path = Path(file_path)
    if not path.is_file():
        logger.error("File could not be found: %s", path)
        raise FileNotFoundError(f"File not found at: {path}")
    
    try:
        logger.info("Loading CSV file from %s", path)
        df = pd.read_csv(path)

        if df.empty:
            logger.warning("CSV file empty: %s", path)
            raise ValueError(f"CSV File Empty: {path}")

        logger.info("Loaded %d rows from %s", len(df), path.name)
        return df

    except pd.errors.EmptyDataError:
        logger.error("File do not contain CSV data: %s", path)
        raise ValueError(f"File does not contain CSV Data: {path}")

def save_from_dataframe_to_csv(df: pd.DataFrame, file_path: str | Path) -> None:

    path = Path(file_path)
    folder = path.parent

    if not folder.exists():
        logger.info("Creating directory: %s", folder)
        folder.mkdir(parents=True, exist_ok=True)

    try:
        logger.info("Saving dataframe to csv: %s", path)
        df.to_csv(path, index=False) 

    except (PermissionError, OSError) as e:
        logger.error("Could not save dataframe to csv at: %s: %s", path, e)
        raise RuntimeError(f"Could not save csv file to {path}") from e


# def load_csv_to_dataframe(*path_segments: str | Path) -> pd.DataFrame:
#     """Load csv from project map into dataframe using Pandas.

#     Example:
#         load_csv_to_dataframe("data", "orders.csv")
#         load_csv_to_dataframe("data", "raw", "orders.csv")
#     """

#     file_path = PROJECT_ROOT.joinpath(*path_segments)

#     # Check if file and folder is accurate and can be accessed
#     if not file_path.is_file():
#         relative_display = Path(*path_segments)
#         raise FileNotFoundError(f"Filen saknas på sökvägen: {relative_display}")

#     return pd.read_csv(file_path)

