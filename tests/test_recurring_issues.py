from ingestion.load_data import load_dataset
from trends.recurring_issues import recurring_non_compliance, monthly_compliance_trend


def _load_records():
    return load_dataset().records


def test_recurring_non_compliance_respects_threshold():
    result = recurring_non_compliance(_load_records(), min_occurrences=2)
    assert (result["occurrences"] >= 2).all()


def test_recurring_non_compliance_has_expected_columns():
    result = recurring_non_compliance(_load_records())
    expected = {"outlet_id", "outlet_name", "inspection_category", "occurrences"}
    assert expected <= set(result.columns)


def test_monthly_compliance_trend_is_bounded():
    trend = monthly_compliance_trend(_load_records())
    assert trend.between(0, 1).all()


def test_monthly_compliance_trend_is_chronological():
    trend = monthly_compliance_trend(_load_records())
    assert list(trend.index) == sorted(trend.index)