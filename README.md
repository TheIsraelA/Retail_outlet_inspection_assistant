# Retail Outlet Inspection Intelligence Assistant

An end-to-end data pipeline and dashboard that turns raw retail fuel outlet
inspection records into compliance metrics, risk scores, trend analysis, and
plain-language AI explanations — built to help a compliance team prioritise
which outlets need attention first.

## What it does

- Loads and validates raw inspection records (schema checks, dtype casting)
- Computes compliance metrics: overall and per-outlet compliance rate,
  severity mix of failures, resolution times
- Scores every outlet 0–100 on risk, combining non-compliance rate, failure
  severity, overdue follow-ups, and recency into one weighted number
- Flags recurring issues — the same outlet failing the same category of
  inspection more than once
- Tracks month-over-month compliance trend across the whole dataset
- Uses an LLM (via Groq's free API tier) to turn the computed numbers into a plain-language summary — the model never invents figures, it only narrates numbers Python has already calculated.
- Ties all of the above together in an interactive Streamlit dashboard

## Tech stack

Python, pandas, pytest, Streamlit, Groq API (OpenAI-SDK-compatible), python-dotenv



## Design decisions worth calling out

**AI explains, Python computes.** The AI layer never does arithmetic or invents an outlet, number, or finding — it only receives pre-computed tables and is instructed to describe what's already there. This keeps the numbers trustworthy regardless of which model is behind the API.

**Groq instead of OpenAI.** The project started on OpenAI's API but moved to Groq, which offers an OpenAI-SDK-compatible endpoint with a genuinely free tier. Only three lines changed (`base_url`, the API key's env var name, and
the model string) — the rest of the integration code didn't need to know which provider was behind it.

**Every module is tested in isolation.** The AI calls are mocked in tests (`unittest.mock.patch`) so the test suite runs free, fast, and without a network connection — a real API key is only needed to actually run the app.

## Setup

1. Clone the repo and create a virtual environment:
2. Install dependencies:
3. Copy `.env.example` to `.env` and fill in your own Groq API key (free at console.groq.com):



## Running it
Run the full test suite: python -m pytest -v
Launch the dashboard: python -m streamlit run app.py


## Possible future improvements

- Swap the synthetic dataset for a real/larger one to stress-test the risk
  thresholds
- Add outlet-level drill-down pages in the dashboard
- Cache AI explanations per outlet so repeat views don't re-call the API
