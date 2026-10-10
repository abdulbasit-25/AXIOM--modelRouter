"""Session-scoped analytics page."""

import csv
from io import StringIO

import streamlit as st

from app.components import empty_state, metric_card, page_header, section_heading
from app.services.router_service import get_router


def render() -> None:
    page_header(
        "SDG Analytics",
        "See what the router is doing in this session.",
        "Live operational metrics from completed tutor and calibration requests, including query volume, latency, model usage, and estimated cost.",
    )
    telemetry = get_router().telemetry
    rows = telemetry.query_history
    summary = telemetry.get_session_summary()
    latencies = [row["latency_ms"] for row in rows if "latency_ms" in row]
    average_latency = sum(latencies) / len(latencies) if latencies else 0.0
    fallback_count = sum(bool(row.get("fallback_triggered")) for row in rows)

    st.caption(
        "Session-scoped operational proxies only. Query counts do not measure learning outcomes "
        "or access; savings compare estimated token cost with the configured frontier-model proxy."
    )
    metrics = (
        ("Routed questions", str(summary["total_queries"]), "Current Streamlit session"),
        ("Average latency", f"{average_latency:.0f} ms" if latencies else "—", "Recorded model-call latency"),
        ("Estimated spend", f"${summary['cumulative_spend']:.6f}", "Based on configured token pricing"),
        ("Estimated savings", f"${summary['cumulative_dollars_saved']:.6f}", "Versus configured baseline proxy"),
    )
    for column, (label, value, note) in zip(st.columns(4, gap="medium"), metrics):
        with column:
            metric_card(label, value, note)

    if not rows:
        empty_state(
            "No session data yet",
            "Run a tutor question or calibration evaluation to populate live analytics.",
            "◔",
        )
        return

    chart_column, breakdown_column = st.columns(2, gap="medium")
    with chart_column:
        section_heading("Model usage", "Counts include each model call; escalated requests count both models.")
        model_counts: dict[str, int] = {}
        for row in rows:
            for model in row.get("models", []):
                model_counts[model] = model_counts.get(model, 0) + 1
        st.bar_chart(model_counts)
    with breakdown_column:
        section_heading("Routing and efficiency")
        st.metric("Fallback rate", f"{fallback_count / len(rows) * 100:.1f}%")
        st.metric("Estimated savings vs baseline", f"{summary['overall_savings_pct']:.1f}%")
        st.metric(
            "Input / output tokens",
            f"{summary['total_input_tokens']:,} / {summary['total_output_tokens']:,}",
        )

    section_heading("Request history", "Detailed estimates are local to this active Streamlit session.")
    display_rows = [
        {
            "Timestamp (UTC)": row.get("timestamp", ""),
            "Tier": row.get("tier", ""),
            "Route": " -> ".join(row.get("models", [])),
            "Latency (ms)": row.get("latency_ms", ""),
            "Escalated": row.get("fallback_triggered", False),
            "Simulated": row.get("mock_fallback", False),
            "Input tokens": row["in_tokens"],
            "Output tokens": row["out_tokens"],
            "Estimated cost (USD)": row["actual_cost"],
            "Baseline proxy (USD)": row["baseline_cost"],
            "Estimated savings (USD)": row["dollars_saved"],
        }
        for row in reversed(rows)
    ]
    st.dataframe(display_rows, width="stretch", hide_index=True)

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=list(display_rows[0]))
    writer.writeheader()
    writer.writerows(display_rows)
    st.download_button(
        "Download session report (CSV)",
        data=output.getvalue(),
        file_name="axiom-session-report.csv",
        mime="text/csv",
    )
