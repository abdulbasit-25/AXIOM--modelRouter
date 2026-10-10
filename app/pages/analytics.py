"""SDG 4/8 Institutional Impact Analytics page."""

import csv
from html import escape
from io import StringIO
import logging

import streamlit as st

from app.services.router_service import get_router
from app.pages import page_base as ui

logger = logging.getLogger(__name__)

_ANALYTICS_CSS = """
<style>
.sdg-hero-card {
    position: relative;
    overflow: hidden;
    padding: 2.2rem 2.4rem;
    border-radius: 26px;
    border: 1px solid rgba(212,215,211,0.28);
    background: linear-gradient(145deg, #1f302d, #263A36);
    box-shadow: 0 20px 50px rgba(0,0,0,0.35);
    margin-bottom: 1.5rem;
}
.sdg-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.35rem 0.85rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #D4D7D3;
    border: 1px solid rgba(212,215,211,0.4);
    background: rgba(24,38,35,0.7);
    margin-bottom: 0.8rem;
}
.sdg-multiplier-card {
    position: relative;
    overflow: hidden;
    padding: 2rem;
    border-radius: 22px;
    border: 1.5px solid #D4D7D3;
    background: linear-gradient(135deg, #344B45, #263A36);
    box-shadow: 0 16px 40px rgba(0,0,0,0.3);
    text-align: center;
    margin: 1.5rem 0;
}
.sdg-mult-value {
    font-size: clamp(2.8rem, 5vw, 4.2rem);
    font-weight: 200;
    color: #D4D7D3;
    line-height: 1.1;
    margin: 0.4rem 0;
}
.sdg-bar-panel {
    padding: 1.6rem;
    border-radius: 22px;
    border: 1px solid rgba(212,215,211,0.22);
    background: linear-gradient(160deg, #2b413d, #1f312e);
    box-shadow: 0 14px 34px rgba(0,0,0,0.25);
    margin: 1rem 0;
}
.sdg-bar-panel h4 {
    margin: 0 0 1.2rem;
    font-size: 0.76rem;
    font-weight: 600;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #899B9A;
}
</style>
"""


def render() -> None:
    ui.inject()
    st.markdown(_ANALYTICS_CSS, unsafe_allow_html=True)

    telemetry = get_router().telemetry
    rows = telemetry.query_history
    summary = telemetry.get_session_summary()

    latencies = [row["latency_ms"] for row in rows if "latency_ms" in row]
    average_latency = sum(latencies) / len(latencies) if latencies else 0.0
    fallback_count = sum(bool(row.get("fallback_triggered")) for row in rows)
    multiplier = summary["edtech_multiplier"]

    # Hero Section
    st.markdown(
        f"""
        <div class="sdg-hero-card">
            <div class="sdg-tag">SDG 4 Quality Education · SDG 8 Economic Growth</div>
            <h1 class="px-title" style="margin:0.4rem 0 0.6rem; color:#D4D7D3;">Institutional Impact Analytics</h1>
            <p class="px-lead" style="margin:0; color:#A3ADA5;">
                Real-time financial telemetry measuring actual routing spend versus Frontier Model Baseline 
                ($2.50 input / $10.00 output per 1M tokens), computing institutional accessibility gains.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Top KPI Tiles
    ui.label("Institutional Efficiency KPIs", "Cumulative session-scoped impact metrics.", index="01")

    metrics = (
        ("Routed Questions", str(summary["total_queries"]), "Active session queries"),
        ("Average Latency", f"{average_latency:.0f} ms" if latencies else "—", "Wall-clock inference latency"),
        ("Axiom Total Spend", f"${summary['cumulative_spend']:.6f}", "Multi-architecture query cost"),
        ("Frontier Baseline Spend", f"${summary['cumulative_baseline_spend']:.6f}", "GPT-4o proxy comparison"),
    )
    st.markdown(ui.tiles(metrics), unsafe_allow_html=True)

    # Prominent EdTech Accessibility Multiplier Hero Card
    st.markdown(
        f"""
        <div class="sdg-multiplier-card">
            <span style="font-size:0.75rem; letter-spacing:0.25em; text-transform:uppercase; color:#A3ADA5; font-weight:700;">
                EdTech Accessibility Multiplier (SDG 4 & SDG 8)
            </span>
            <div class="sdg-mult-value">{multiplier:.1f}×</div>
            <p style="margin:0; color:#D4D7D3; font-size:1.05rem;">
                <b>{multiplier:.1f} times more students served</b> on the exact same institutional budget 
                compared to standard frontier-model deployments.
            </p>
            <div style="margin-top:0.6rem; font-size:0.8rem; color:#899B9A;">
                Net Dollars Saved: <b>${summary['cumulative_dollars_saved']:.6f}</b> · 
                Net Savings: <b>{summary['overall_savings_pct']:.1f}%</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not rows:
        st.markdown(
            ui.empty(
                "No Session Telemetry Yet",
                "Execute questions in the Production AI Tutor to generate real-time institutional telemetry.",
            ),
            unsafe_allow_html=True,
        )
        return

    # Comparative Spend Bar Chart (EduRoute Spend vs Frontier Baseline Spend)
    ui.label(
        "Comparative Spend & Volume Distribution",
        "Axiom EduRoute Spend vs Frontier Baseline Spend ($2.50 / $10.00 per 1M tokens).",
        index="02",
    )

    chart_col1, chart_col2 = st.columns(2, gap="medium")
    with chart_col1:
        with st.container(border=True):
            st.markdown('<div class="px-panel-head">Comparative Spend ($ USD)</div>', unsafe_allow_html=True)
            spend_data = {
                "Axiom Spend ($)": summary["cumulative_spend"],
                "Frontier Baseline ($)": summary["cumulative_baseline_spend"],
            }
            st.bar_chart(spend_data, height=220)
            st.caption(
                f"Axiom saved ${summary['cumulative_dollars_saved']:.6f} "
                f"({summary['overall_savings_pct']:.1f}%) across {summary['total_queries']} queries."
            )

    with chart_col2:
        with st.container(border=True):
            st.markdown('<div class="px-panel-head">Calls Per Model Architecture</div>', unsafe_allow_html=True)
            model_counts: dict[str, int] = {}
            for row in rows:
                for m in row.get("models", []):
                    model_counts[m] = model_counts.get(m, 0) + 1
            if model_counts:
                st.bar_chart(model_counts, height=220)
                st.caption(f"Fallback escalation frequency: {fallback_count} / {len(rows)} queries ({(fallback_count/len(rows))*100:.1f}%)")

    # Detailed Audit Trail & CSV Download
    st.write("")
    ui.label("Detailed Request Audit Log", "Chronological audit trail of all routed queries.", index="03")

    display_rows = [
        {
            "Timestamp (UTC)": row.get("timestamp", ""),
            "Tier": row.get("tier", 1),
            "Route": " -> ".join(row.get("models", [row.get("model", "")])),
            "Latency (ms)": row.get("latency_ms", 0.0),
            "Escalated": bool(row.get("fallback_triggered", False)),
            "Simulated": bool(row.get("mock_fallback", False)),
            "In Tokens": row.get("in_tokens", 0),
            "Out Tokens": row.get("out_tokens", 0),
            "Axiom Cost ($)": f"${row.get('actual_cost', 0.0):.6f}",
            "Baseline Cost ($)": f"${row.get('baseline_cost', 0.0):.6f}",
            "Dollars Saved ($)": f"${row.get('dollars_saved', 0.0):.6f}",
            "Savings (%)": f"{row.get('savings_pct', 0.0):.1f}%",
        }
        for row in reversed(rows)
    ]
    st.dataframe(display_rows, width="stretch", hide_index=True)

    csv_buf = StringIO()
    writer = csv.DictWriter(csv_buf, fieldnames=list(display_rows[0].keys()))
    writer.writeheader()
    writer.writerows(display_rows)

    st.download_button(
        "Download Institutional Audit Report (CSV)",
        data=csv_buf.getvalue(),
        file_name="axiom-institutional-sdg-report.csv",
        mime="text/csv",
        key="download_analytics_csv",
    )