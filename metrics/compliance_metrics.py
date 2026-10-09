import pandas as pd


def overall_compliance_rate(records: pd.DataFrame) -> float:
    return (records["compliance_status"] == "Compliant").mean()


def compliance_rate_by(records: pd.DataFrame, group_col: str) -> pd.Series:
    return (
        records.groupby(group_col)["compliance_status"]
        .apply(lambda s: (s == "Compliant").mean())
        .sort_values()
    )


def non_compliance_rate_by(records: pd.DataFrame, group_col: str) -> pd.Series:
    return (
        records.groupby(group_col)["compliance_status"]
        .apply(lambda s: (s == "Non-Compliant").mean())
        .sort_values(ascending=False)
    )


def severity_mix(records: pd.DataFrame) -> pd.Series:
    non_compliant = records[records["compliance_status"] == "Non-Compliant"]
    return non_compliant["severity"].value_counts(normalize=True)


def follow_up_status_counts(records: pd.DataFrame) -> pd.Series:
    return records["follow_up_status"].value_counts()


def avg_days_to_resolution(records: pd.DataFrame) -> float:
    resolved = records[records["follow_up_status"] == "Resolved"]
    return resolved["days_to_resolution"].mean()


if __name__ == "__main__":
    from ingestion.load_data import load_dataset

    ds = load_dataset()
    print("Overall compliance rate:", overall_compliance_rate(ds.records))
    print("\nBy outlet (worst 5):")
    print(non_compliance_rate_by(ds.records, "outlet_id").head())
    print("\nSeverity mix:")
    print(severity_mix(ds.records))