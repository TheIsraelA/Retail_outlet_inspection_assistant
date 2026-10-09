import pandas as pd

from metrics.compliance_metrics import non_compliance_rate_by

SEVERITY_WEIGHTS = {
    "Not Applicable": 0,
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Critical": 4,
}
MAX_SEVERITY_WEIGHT = max(SEVERITY_WEIGHTS.values())


def _avg_severity_score_by_outlet(records: pd.DataFrame) -> pd.Series:
    non_compliant = records[records["compliance_status"] == "Non-Compliant"].copy()
    non_compliant["severity_weight"] = non_compliant["severity"].map(SEVERITY_WEIGHTS)
    return non_compliant.groupby("outlet_id")["severity_weight"].mean() / MAX_SEVERITY_WEIGHT

    
def _overdue_rate_by_outlet(records: pd.DataFrame) -> pd.Series:
    return records.groupby("outlet_id")["follow_up_status"].apply(lambda s: (s == "Overdue").mean())


def _recency_score_by_outlet(records: pd.DataFrame) -> pd.Series:
    non_compliant = records[records["compliance_status"] == "Non-Compliant"]
    latest_overall = records["inspection_date"].max()
    days_since_last_issue = non_compliant.groupby("outlet_id")["inspection_date"].apply(
        lambda dates: (latest_overall - dates.max()).days
    )
    max_days = days_since_last_issue.max()
    return 1 - (days_since_last_issue / max_days)


def compute_risk_scores(records: pd.DataFrame) -> pd.DataFrame:
    components = pd.DataFrame({
        "non_compliance_rate": non_compliance_rate_by(records, "outlet_id"),
        "severity_score": _avg_severity_score_by_outlet(records),
        "overdue_rate": _overdue_rate_by_outlet(records),
        "recency_score": _recency_score_by_outlet(records),
    }).fillna(0)

    components["risk_score"] = (
        0.35 * components["non_compliance_rate"]
        + 0.35 * components["severity_score"]
        + 0.20 * components["overdue_rate"]
        + 0.10 * components["recency_score"]
    ) * 100

    return components.sort_values("risk_score", ascending=False)


if __name__ == "__main__":
    from ingestion.load_data import load_dataset

    ds = load_dataset()
    print(compute_risk_scores(ds.records).round(2).head(10))