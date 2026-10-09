import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("Missing GROQ_API_KEY in .env")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
)

MODEL = "openai/gpt-oss-20b"

SYSTEM_PROMPT = (
    "You are a compliance analyst assistant. You will be given pre-computed "
    "risk scores and metrics for retail fuel outlets as structured data. "
    "Explain what the numbers mean in plain, professional language. "
    "Rules you must follow strictly:\n"
    "1. Never invent, estimate, or guess any number, outlet, or finding that "
    "is not explicitly present in the data you are given.\n"
    "2. Only refer to outlets, categories, and figures that appear in the "
    "provided data.\n"
    "3. If the data doesn't support a conclusion, say so rather than "
    "speculating.\n"
    "4. Keep the tone factual and neutral, not alarmist."
)


def _ask(data_as_text: str, instruction: str) -> str:
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"{instruction}\n\n{data_as_text}"},
            ],
            temperature=0.2,
        )
    except Exception as exc:
        return f"AI explanation unavailable right now ({exc})."
    return response.choices[0].message.content


def explain_risk_table(risk_table) -> str:
    data_as_text = risk_table.round(2).to_csv()
    instruction = (
        "Here is the current outlet risk-scoring table (columns: "
        "non_compliance_rate, severity_score, overdue_rate, recency_score, "
        "risk_score). Summarize the three highest-risk outlets and explain, "
        "in plain language, why each one scored the way it did."
    )
    return _ask(data_as_text, instruction)


def explain_recurring_issues(recurring_df) -> str:
    data_as_text = recurring_df.to_csv(index=False)
    instruction = (
        "Here is a table of outlet/category combinations that failed "
        "inspection two or more times (columns: outlet_id, outlet_name, "
        "inspection_category, occurrences). Summarize the most notable "
        "recurring problems and which outlets they affect."
    )
    return _ask(data_as_text, instruction)


if __name__ == "__main__":
    from ingestion.load_data import load_dataset
    from risk.risk_scoring import compute_risk_scores
    from trends.recurring_issues import recurring_non_compliance

    ds = load_dataset()
    risk_table = compute_risk_scores(ds.records)
    recurring = recurring_non_compliance(ds.records)

    print("=== Risk explanation ===")
    print(explain_risk_table(risk_table))
    print("\n=== Recurring issues explanation ===")
    print(explain_recurring_issues(recurring))