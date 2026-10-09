import pandas as pd

from ingestion.load_data import load_dataset, DEFAULT_DATA_PATH
from validation.validators import validate_dataset


def _load():
    return load_dataset(DEFAULT_DATA_PATH)


def test_real_dataset_passes_validation():
    ds = _load()
    report = validate_dataset(ds)
    assert report.is_valid, report.summary()


def test_catches_compliant_with_real_severity():
    ds = _load()
    ds.records.loc[0, "compliance_status"] = "Compliant"
    ds.records.loc[0, "severity"] = "High"
    report = validate_dataset(ds)
    assert not report.is_valid
    assert any("Compliant records have a real severity" in e for e in report.errors)


def test_catches_orphan_outlet_id():
    ds = _load()
    ds.records.loc[0, "outlet_id"] = "OUT999"
    report = validate_dataset(ds)
    assert not report.is_valid
    assert any("unknown outlet_id" in e for e in report.errors)


def test_catches_duplicate_inspection_id():
    ds = _load()
    ds.records.loc[1, "inspection_id"] = ds.records.loc[0, "inspection_id"]
    report = validate_dataset(ds)
    assert not report.is_valid
    assert any("Duplicate inspection_id" in e for e in report.errors)


def test_catches_open_record_with_resolution_date():
    ds = _load()
    open_idx = ds.records[ds.records["follow_up_status"] == "Open"].index[0]
    ds.records.loc[open_idx, "resolution_date"] = ds.records.loc[open_idx, "inspection_date"] + pd.Timedelta(days=3)
    report = validate_dataset(ds)
    assert not report.is_valid
    assert any("Open/Overdue records have a resolution_date" in e for e in report.errors)


def test_catches_resolved_record_missing_resolution_date():
    ds = _load()
    resolved_idx = ds.records[ds.records["follow_up_status"] == "Resolved"].index[0]
    ds.records.loc[resolved_idx, "resolution_date"] = pd.NaT
    report = validate_dataset(ds)
    assert not report.is_valid
    assert any("missing a resolution_date" in e for e in report.errors)