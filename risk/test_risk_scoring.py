from ingestion.load_data import load_dataset
from risk.risk_scoring import compute_risk_scores


def _load_records():
    return load_dataset().records


def test_risk_scores_cover_every_outlet():
    records = _load_records()
    result = compute_risk_scores(records)
    assert len(result) == records["outlet_id"].nunique()


def test_risk_scores_are_bounded():
    result = compute_risk_scores(_load_records())
    assert result["risk_score"].between(0, 100).all()


def test_risk_scores_are_sorted_descending():
    result = compute_risk_scores(_load_records())
    assert list(result["risk_score"]) == sorted(result["risk_score"], reverse=True)


def test_worst_offender_ranks_in_top_half():
    result = compute_risk_scores(_load_records())
    worst_by_rate = result["non_compliance_rate"].idxmax()
    rank = result.index.get_loc(worst_by_rate)
    assert rank < len(result) // 2