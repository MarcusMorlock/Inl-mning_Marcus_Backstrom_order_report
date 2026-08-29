from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# def load_csv_to_dataframe(file_name: str, file_folder:str) -> pd.DataFrame:

#     folder = PROJECT_ROOT / file_folder

#     path = folder / file_name

#     load_data = pd.read_csv(path)

#     return load_data

def load_csv_to_dataframe(file_name: str, file_folder:str) -> pd.DataFrame:

    clean_folder_path = file_folder.strip("/\\")

    folder_path = PROJECT_ROOT / clean_folder_path 

    if not folder_path.is_dir():
        raise FileNotFoundError(f"Folder {clean_folder_path} could not be found.")

    file_path = folder_path / file_name

    if not file_path.is_file():
        relative_path = f"{clean_folder_path}/{file_name}" if clean_folder_path else file_name
        raise FileNotFoundError(f"File {file_name} not found at {relative_path}")

    return pd.read_csv(file_path)
