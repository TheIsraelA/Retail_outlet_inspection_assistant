from unittest.mock import patch, MagicMock

import pandas as pd

from ai.explain import explain_risk_table


def test_explain_risk_table_returns_mocked_content():
    fake_risk_table = pd.DataFrame(
        {"risk_score": [55.0]}, index=pd.Index(["OUT001"], name="outlet_id")
    )
    fake_response = MagicMock()
    fake_response.choices[0].message.content = "Mocked explanation text."

    with patch("ai.explain.client.chat.completions.create", return_value=fake_response) as mock_create:
        result = explain_risk_table(fake_risk_table)

    assert result == "Mocked explanation text."
    mock_create.assert_called_once()


def test_explain_risk_table_handles_api_failure_gracefully():
    fake_risk_table = pd.DataFrame(
        {"risk_score": [10.0]}, index=pd.Index(["OUT001"], name="outlet_id")
    )
    with patch("ai.explain.client.chat.completions.create", side_effect=Exception("network down")):
        result = explain_risk_table(fake_risk_table)

    assert "unavailable" in result.lower()