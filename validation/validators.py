"""
Validation layer for the Retail Outlet Inspection dataset.
"""

from dataclasses import dataclass, field

import pandas as pd

from config.schema import (
    INSPECTION_RECORDS_COLUMNS,
    OUTLET_DIRECTORY_COLUMNS,
    CATEGORY_REFERENCE_COLUMNS,
    COMPLIANCE_STATUS_VALUES,
    SEVERITY_VALUES,
    FOLLOW_UP_STATUS_VALUES,
    INSPECTION_TYPE_VALUES,
)
from ingestion.load_data import InspectionDataset


@dataclass
class ValidationReport:
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)

    @property
    def is_valid(self):
        return len(self.errors) == 0

    def summary(self):
        lines = [f"Errors: {len(self.errors)}", f"Warnings: {len(self.warnings)}"]
        lines += [f"  ERROR: {e}" for e in self.errors]
        return "\n".join(lines)


def validate_dataset(dataset: InspectionDataset) -> ValidationReport:
    report = ValidationReport()
    records, outlets, categories = dataset.records, dataset.outlets, dataset.categories

    #  Schema: are all expected columns present? 
    missing = INSPECTION_RECORDS_COLUMNS - set(records.columns)
    if missing:
        report.errors.append(f"INSPECTION_RECORDS missing columns: {sorted(missing)}")

    # Controlled values: does every value fall inside the allowed set? 
    bad_compliance = set(records["compliance_status"].dropna()) - COMPLIANCE_STATUS_VALUES
    if bad_compliance:
        report.errors.append(f"Invalid compliance_status values: {sorted(bad_compliance)}")

    bad_severity = set(records["severity"].dropna()) - SEVERITY_VALUES
    if bad_severity:
        report.errors.append(f"Invalid severity values: {sorted(bad_severity)}")

    # Uniqueness: no duplicate inspection_id 
    if records["inspection_id"].duplicated().any():
        report.errors.append("Duplicate inspection_id values found")

    # Referential integrity: every outlet_id must exist in OUTLET_DIRECTORY 
    unknown_outlets = set(records["outlet_id"]) - set(outlets["outlet_id"])
    if unknown_outlets:
        report.errors.append(f"Records reference unknown outlet_id(s): {sorted(unknown_outlets)}")

    # Business rule: Compliant records must have severity 'Not Applicable'
    compliant = records[records["compliance_status"] == "Compliant"]
    if (compliant["severity"] != "Not Applicable").any():
        report.errors.append("Some Compliant records have a real severity value")

    # Business rule: Open/Overdue records must NOT have a resolution_date 
    open_or_overdue = records[records["follow_up_status"].isin(["Open", "Overdue"])]
    if open_or_overdue["resolution_date"].notna().any():
        report.errors.append("Some Open/Overdue records have a resolution_date set")

    # Business rule: Resolved records MUST have a resolution_date
    resolved = records[records["follow_up_status"] == "Resolved"]
    if resolved["resolution_date"].isna().any():
        report.errors.append("Some Resolved records are missing a resolution_date")

    return report


if __name__ == "__main__":
    from ingestion.load_data import load_dataset

    ds = load_dataset()
    rpt = validate_dataset(ds)
    print(rpt.summary())