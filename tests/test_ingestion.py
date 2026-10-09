import pytest

from ingestion.load_data import load_dataset, DEFAULT_DATA_PATH


def test_load_dataset_shapes():
    ds = load_dataset(DEFAULT_DATA_PATH)
    assert len(ds.records) == 1000
    assert len(ds.outlets) == 30
    assert len(ds.categories) == 12
    assert len(ds.data_dictionary) == 18


def test_records_columns_present():
    ds = load_dataset(DEFAULT_DATA_PATH)
    expected = {
        "inspection_id", "outlet_id", "outlet_name", "location", "lga", "outlet_type",
        "inspection_date", "inspection_type", "inspection_category", "observation",
        "compliance_status", "severity", "recommended_action", "follow_up_status",
        "resolution_date", "inspector_name", "days_to_resolution", "record_source",
    }
    assert expected <= set(ds.records.columns)


def test_records_dtypes_cast_correctly():
    ds = load_dataset(DEFAULT_DATA_PATH)
    assert str(ds.records["inspection_date"].dtype).startswith("datetime64")
    assert str(ds.records["resolution_date"].dtype).startswith("datetime64")
    assert ds.records["days_to_resolution"].dtype.name == "Int64"
    assert ds.records["outlet_id"].dtype.name == "string"


def test_missing_file_raises_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_dataset("does/not/exist.xlsx")