import streamlit as st
import pandas as pd
import plotly.express as px

from ingestion.load_data import load_dataset
from metrics.compliance_metrics import overall_compliance_rate, non_compliance_rate_by, severity_mix
from risk.risk_scoring import compute_risk_scores
from trends.recurring_issues import recurring_non_compliance, monthly_compliance_trend
from ai.explain import explain_risk_table, explain_recurring_issues

st.set_page_config(page_title="Retail Outlet Inspection Intelligence", layout="wide")


@st.cache_data
def get_data():
    ds = load_dataset()
    return ds.records


records = get_data()

st.title("Retail Outlet Inspection Intelligence Assistant")
st.caption("Compliance, risk, and trend insights across retail fuel outlets")

col1, col2, col3 = st.columns(3)
col1.metric("Overall Compliance Rate", f"{overall_compliance_rate(records):.1%}")
col2.metric("Total Inspections", len(records))
col3.metric("Outlets Covered", records["outlet_id"].nunique())

st.divider()

st.header("Outlet Risk Scores")
risk_table = compute_risk_scores(records).sort_values("risk_score", ascending=False)
st.dataframe(risk_table.round(2), use_container_width=True, hide_index=False)

if st.button("Explain top risks with AI"):
    with st.spinner("Asking the AI to explain the risk table..."):
        explanation = explain_risk_table(risk_table)
    st.write(explanation)

st.divider()

st.header("Non-Compliance Rate by Outlet")
non_compliance_df = non_compliance_rate_by(records, "outlet_id").reset_index()
non_compliance_df.columns = ["outlet_id", "non_compliance_rate"]

bar_fig = px.bar(
    non_compliance_df,
    x="outlet_id",
    y="non_compliance_rate",
    color="non_compliance_rate",
    color_continuous_scale="YlOrRd",
    title="Non-Compliance Rate by Outlet",
    labels={"outlet_id": "Outlet ID", "non_compliance_rate": "Non-Compliance Rate"},
    hover_data={"outlet_id": True, "non_compliance_rate": ":.2%"},
)
bar_fig.update_layout(template="plotly_white", paper_bgcolor="black", plot_bgcolor="black")
st.plotly_chart(bar_fig, use_container_width=True, theme="streamlit")

st.divider()

st.header("Severity Mix of Non-Compliant Findings")
severity_df = severity_mix(records).reset_index()
severity_df.columns = ["severity", "share"]

pie_fig = px.pie(
    severity_df,
    names="severity",
    values="share",
    title="Severity Mix of Non-Compliant Findings",
    color="severity",
    color_discrete_sequence=px.colors.qualitative.Set2,
)
pie_fig.update_traces(textinfo="percent+label", hoverinfo="label+percent")
pie_fig.update_layout(template="plotly_white")
st.plotly_chart(pie_fig, use_container_width=True, theme="streamlit")

st.divider()

st.header("Recurring Issues (2+ occurrences)")
recurring = recurring_non_compliance(records)
st.dataframe(recurring, use_container_width=True)

if st.button("Explain recurring issues with AI"):
    with st.spinner("Asking the AI to explain recurring issues..."):
        explanation = explain_recurring_issues(recurring)
    st.write(explanation)

st.divider()

st.header("Monthly Compliance Trend")
trend = monthly_compliance_trend(records).reset_index()
trend.columns = ["month", "compliance_rate"]
trend["month"] = trend["month"].astype(str)

line_fig = px.line(
    trend,
    x="month",
    y="compliance_rate",
    markers=True,
    title="Monthly Compliance Trend",
    labels={"month": "Month", "compliance_rate": "Compliance Rate"},
    color_discrete_sequence=["#2EDEAF"],
)
line_fig.update_layout(template="plotly_white")
line_fig.update_yaxes(range=[0, 1.05], tickformat=".0%")
st.plotly_chart(line_fig, use_container_width=True, theme="streamlit")