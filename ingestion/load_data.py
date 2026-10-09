""" loads the Retail Outlet Inspection workbook into typed pandas DataFrames. 
"""

from dataclasses import dataclass
from pathlib import Path
import pandas as pd

from config.schema import (
    SHEET_INSPECTION_RECORDS,
    SHEET_OUTLET_DIRECTORY, 
    SHEET_CATEGORY_REFERENCE,
    SHEET_DATA_DICTIONARY,
)

DEFAULT_DATA_PATH = (
    Path(__file__).resolve().parents[1] / "data" / "raw" / "retail_outlet_inspection_dataset.xlsx"
)

_RECORDS_STRINGS_COLUMNS = [
    "inspection_id", "outlet_id", "outlet_name", "location", "lga",
    "outlet_type", "inspection_type", "inspection_category", "observation",
    "compliance_status", "severity", "recommended_action", "follow_up_status",
    "inspector_name", "record_source",
]


@dataclass
class InspectionDataset:
    records: pd.DataFrame
    outlets: pd.DataFrame
    categories: pd.DataFrame
    data_dictionary: pd.DataFrame
    source_path: Path

def load_dataset(path: str | Path = DEFAULT_DATA_PATH) -> InspectionDataset:

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}")

    xl = pd.ExcelFile(path)

    records = xl.parse(SHEET_INSPECTION_RECORDS)
    outlets = xl.parse(SHEET_OUTLET_DIRECTORY)
    categories = xl.parse(SHEET_CATEGORY_REFERENCE)
    data_dictionary = xl.parse(SHEET_DATA_DICTIONARY)

    records = _cast_records(records)
    outlets = _cast_outlets(outlets)
    
    return InspectionDataset(
        records=records,
        outlets=outlets,
        categories=categories,
        data_dictionary=data_dictionary,
        source_path=path,
    )

def _cast_records(records: pd.DataFrame) -> pd.DataFrame:
    records = records.copy()
    records["inspection_date"] = pd.to_datetime(records["inspection_date"], errors="coerce")
    records["resolution_date"] = pd.to_datetime(records["resolution_date"], errors="coerce")
    records["days_to_resolution"] = records["days_to_resolution"].astype("Int64")
    for col in _RECORDS_STRINGS_COLUMNS:
        records[col] = records[col].astype("string")
    return records

def _cast_outlets(outlets: pd.DataFrame) -> pd.DataFrame:
    outlets = outlets.copy()
    for col in ["outlet_id", "outlet_name", "location", "lga", "outlet_type", "operational_status"]:
        outlets[col] = outlets[col].astype(str)
    return outlets

if __name__ == "__main__":
    dataset = load_dataset()
    print(
        f"Loaded {len(dataset.records)} inspection records, {len(dataset.outlets)} outlets, "
        f"{len(dataset.categories)} categories, and {len(dataset.data_dictionary)} data dictionary entries from {dataset.source_path}" 
    )
