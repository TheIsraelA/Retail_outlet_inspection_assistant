import pandas as pd


def recurring_non_compliance(records: pd.DataFrame, min_occurrences: int = 2) -> pd.DataFrame:
    non_compliant = records[records["compliance_status"] == "Non-Compliant"]
    counts = (
        non_compliant.groupby(["outlet_id", "outlet_name", "inspection_category"])
        .size()
        .reset_index(name="occurrences")
    )
    recurring = counts[counts["occurrences"] >= min_occurrences]
    return recurring.sort_values("occurrences", ascending=False)


def monthly_compliance_trend(records: pd.DataFrame) -> pd.Series:
    records = records.copy()
    records["inspection_month"] = records["inspection_date"].dt.to_period("M")
    return (
        records.groupby("inspection_month")["compliance_status"]
        .apply(lambda s: (s == "Compliant").mean())
        .sort_index()
    )


if __name__ == "__main__":
    from ingestion.load_data import load_dataset

    ds = load_dataset()
    print("Top recurring issues (same outlet, same category, 2+ times):")
    print(recurring_non_compliance(ds.records).head(10))

    print("\nMonthly compliance trend:")
    print(monthly_compliance_trend(ds.records))