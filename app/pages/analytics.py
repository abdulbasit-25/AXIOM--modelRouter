"""Session-scoped analytics page."""

import csv
from html import escape
from io import StringIO

import streamlit as st

from app.services.router_service import get_router

_CSS = """
<style>
@property --p { syntax: '<number>'; inherits: false; initial-value: 0; }
:root {
  --mist: #D4D7D3; --mist-hover: #E5E7E3;
  --sage: #A3ADA5; --steel: #899B9A;
  --slate: #46565D; --forest: #263A36;
  --slate-hover: #566970; --forest-hover: #344B45;
  --focus-ring: #A3ADA5;
  --ease: cubic-bezier(.2,.8,.2,1);
}
.stApp { background: radial-gradient(1100px 650px at 85% -10%, rgba(137,155,154,.2), transparent 60%), radial-gradient(900px 600px at -10% 45%, rgba(70,86,93,.35), transparent 60%), var(--forest); color: var(--mist); }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1120px; padding-top: 2rem; }

@keyframes an-rise { from {opacity:0; transform: translateY(24px); filter: blur(6px);} to {opacity:1; transform:none; filter:none;} }
@keyframes an-float { 0%,100% {transform: translate(0,0);} 50% {transform: translate(30px,-24px);} }
@keyframes an-spin { to {transform: rotate(360deg);} }
@keyframes an-line { from {transform: scaleX(0);} to {transform: scaleX(1);} }
@keyframes an-fill { from {transform: scaleX(0);} to {transform: scaleX(1);} }
@keyframes an-gauge { from {--p: 0;} }
@keyframes an-blink { 0%,100% {opacity:1;} 50% {opacity:.25;} }

/* Hero */
.an-hero { position: relative; overflow: hidden; border-radius: 28px; padding: 2.8rem 3rem; border: 1px solid rgba(212,215,211,.26); background: linear-gradient(145deg, #1c2c2a 0%, #233834 55%, #2a403c 100%); box-shadow: 0 30px 70px rgba(0,0,0,.4), inset 0 1px 0 rgba(212,215,211,.22), inset 0 0 80px rgba(16,26,24,.5); }
.an-hero::before { content:""; position:absolute; inset:0; background-image: linear-gradient(rgba(212,215,211,.07) 1px, transparent 1px), linear-gradient(90deg, rgba(212,215,211,.07) 1px, transparent 1px); background-size: 56px 56px; -webkit-mask-image: radial-gradient(ellipse at 85% 30%, #000 15%, transparent 70%); mask-image: radial-gradient(ellipse at 85% 30%, #000 15%, transparent 70%); }
.an-orb { position:absolute; right:-70px; top:-90px; width:300px; height:300px; border-radius:50%; background: var(--steel); filter: blur(70px); opacity:.4; animation: an-float 14s ease-in-out infinite; }
.an-live { position: relative; display: inline-flex; align-items: center; gap: .6rem; padding: .38rem .95rem; border-radius: 999px; font-size: .72rem; letter-spacing: .2em; text-transform: uppercase; color: var(--mist); border: 1px solid rgba(212,215,211,.45); background: rgba(24,38,35,.7); animation: an-rise .9s both; }
.an-live i { width: 7px; height: 7px; border-radius: 50%; background: var(--mist); animation: an-blink 1.6s infinite; }
.stMarkdown h1.an-title { position: relative; margin: 1rem 0 .4rem; padding: 0; font-size: clamp(2.2rem, 6vw, 4rem); font-weight: 200; letter-spacing: .1em; line-height: 1.05; text-transform: uppercase; color: var(--mist) !important; animation: an-rise 1s .1s both; }
.stMarkdown p.an-lead { position: relative; max-width: 34rem; margin: 0; font-size: 1.08rem; line-height: 1.8; color: var(--sage) !important; animation: an-rise 1s .2s both; }

.an-note { margin: 1.1rem 0 0; padding-left: 1rem; border-left: 2px solid var(--steel); font-size: .82rem; line-height: 1.7; color: var(--white); }

/* Labels */
.an-label { margin: 3rem 0 1.2rem; display: flex; align-items: center; gap: 1rem; font-size: .75rem; font-weight: 600; letter-spacing: .3em; text-transform: uppercase; color: var(--steel); }
.an-label::after { content:""; flex:1; height:1px; background: linear-gradient(90deg, rgba(137,155,154,.55), transparent); transform-origin: left; animation: an-line 1.4s .2s both; }
.an-sub { margin: -.6rem 0 1.2rem; font-size: .85rem; color: var(--sage); }

/* Metric tiles */
.an-tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1rem; margin-top: 1.4rem; }
.an-tile { position: relative; overflow: hidden; padding: 1.4rem 1.4rem 1.3rem; border-radius: 20px; border: 1px solid rgba(212,215,211,.22); background: linear-gradient(160deg, #2b413d, #1f312e); box-shadow: 0 14px 30px rgba(0,0,0,.3); animation: an-rise .9s both; transition: transform .45s var(--ease), border-color .45s, box-shadow .45s; }
.an-tile::before { content:""; position:absolute; left:0; top:0; height:2px; width:100%; background: linear-gradient(90deg, var(--mist), transparent); transform-origin: left; animation: an-line 1.4s .4s both; }
.an-tile:nth-child(1)::before { background: linear-gradient(90deg, #E5E7E3, transparent); }
.an-tile:nth-child(2)::before { background: linear-gradient(90deg, #899B9A, transparent); }
.an-tile:nth-child(3)::before { background: linear-gradient(90deg, #A3ADA5, transparent); }
.an-tile:nth-child(4)::before { background: linear-gradient(90deg, #D4D7D3, #899B9A 60%, transparent); }
.an-tile:hover { transform: translateY(-6px); border-color: rgba(212,215,211,.45); box-shadow: 0 22px 44px rgba(0,0,0,.3); }
.an-tile small { display: block; font-size: .7rem; font-weight: 600; letter-spacing: .24em; text-transform: uppercase; color: var(--sage); }
.an-tile b { display: block; margin: .9rem 0 .35rem; font-size: clamp(1.4rem, 2.4vw, 1.9rem); font-weight: 300; letter-spacing: .02em; color: var(--mist); word-break: break-word; }
.an-tile span { font-size: .8rem; color: var(--sage); }

/* Panels */
.an-panel { position: relative; height: 100%; padding: 1.6rem 1.6rem 1.5rem; border-radius: 22px; border: 1px solid rgba(212,215,211,.22); background: linear-gradient(160deg, #2b413d, #1f312e); box-shadow: 0 16px 36px rgba(0,0,0,.3); animation: an-rise .9s both; }
.an-panel h4 { margin: 0 0 1.3rem; font-size: .75rem; font-weight: 600; letter-spacing: .28em; text-transform: uppercase; color: var(--steel); }

.an-bar { margin-bottom: 1rem; }
.an-bar-top { display: flex; justify-content: space-between; gap: 1rem; font-size: .9rem; color: var(--mist); }
.an-bar-top em { font-style: normal; color: var(--sage); }
.an-track { height: 9px; margin-top: .55rem; border-radius: 9px; background: rgba(16,26,24,.65); border: 1px solid rgba(212,215,211,.12); overflow: hidden; }
.an-fill { height: 100%; border-radius: 9px; background: linear-gradient(90deg, #6f8281, #D4D7D3); box-shadow: 0 0 14px rgba(212,215,211,.35); transform-origin: left; animation: an-fill 1.2s var(--ease) both; }

.an-gauges { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
.an-gauge-wrap { text-align: center; }
.an-gauge { --p: 0; position: relative; width: 112px; height: 112px; margin: 0 auto .7rem; border-radius: 50%; background: conic-gradient(var(--c, var(--mist)) calc(var(--p) * 1%), rgba(212,215,211,.12) 0); box-shadow: 0 0 26px color-mix(in srgb, var(--c, #D4D7D3) 22%, transparent); animation: an-gauge 1.4s var(--ease) both; display: grid; place-items: center; }
.an-gauge::before { content:""; position:absolute; inset: 9px; border-radius: 50%; background: #212f2c; }
.an-gauge strong { position: relative; font-size: 1.15rem; font-weight: 300; color: var(--mist); }
.an-gauge-wrap small { font-size: .68rem; font-weight: 600; letter-spacing: .2em; text-transform: uppercase; color: var(--sage); }
.an-tokens { display: flex; justify-content: space-between; align-items: baseline; gap: 1rem; margin-top: 1.4rem; padding-top: 1.1rem; border-top: 1px solid rgba(212,215,211,.16); font-size: .8rem; letter-spacing: .12em; text-transform: uppercase; color: var(--sage); }
.an-tokens b { font-size: 1.15rem; font-weight: 300; letter-spacing: .02em; text-transform: none; color: var(--mist); }

/* Empty state */
.an-empty { position: relative; overflow: hidden; margin-top: 1.6rem; padding: 3.4rem 2rem; text-align: center; border-radius: 26px; border: 1px dashed rgba(212,215,211,.35); background: rgba(70,86,93,.28); animation: an-rise .9s both; }
.an-empty-ring { position: relative; width: 84px; height: 84px; margin: 0 auto 1.6rem; border-radius: 50%; border: 1px dashed rgba(212,215,211,.5); animation: an-spin 24s linear infinite; }
.an-empty-ring::before { content:""; position:absolute; inset: 18px; border-radius: 50%; border: 1px solid rgba(137,155,154,.7); }
.an-empty-ring::after { content:""; position:absolute; top:-4px; left:50%; width:8px; height:8px; margin-left:-4px; border-radius:50%; background: var(--mist); box-shadow: 0 0 14px var(--mist); }
.an-empty h3 { margin: 0 0 .5rem; padding: 0; font-size: 1.5rem; font-weight: 300; letter-spacing: .06em; color: var(--mist); }
.an-empty p { margin: 0 auto; max-width: 28rem; color: var(--sage); }

/* Dataframe and download */
[data-testid="stDataFrame"] { border: 1px solid rgba(212,215,211,.22); border-radius: 18px; overflow: hidden; }
.stDownloadButton > button { border-radius: 999px; padding: .65rem 1.5rem; font-weight: 400; letter-spacing: .08em; border: 1px solid rgba(212,215,211,.4); background: transparent; color: var(--mist); transition: transform .3s var(--ease), box-shadow .3s, background .3s, color .3s, border-color .3s; }
.stDownloadButton > button p, .stDownloadButton > button span { color: inherit; }
.stDownloadButton > button:hover { transform: translateY(-3px); border-color: var(--mist); background: var(--forest-hover); color: var(--mist); box-shadow: 0 10px 26px rgba(0,0,0,.28); }
.stDownloadButton > button:active { transform: translateY(-1px) scale(.98); background: var(--slate-hover); color: var(--mist); }
.stDownloadButton > button:focus-visible { outline: 2px solid var(--focus-ring); outline-offset: 3px; color: var(--mist); }

@media (max-width: 760px) { .an-hero { padding: 2.2rem 1.4rem; } .an-gauges { grid-template-columns: 1fr 1fr; } }
@media (prefers-reduced-motion: reduce) {
    .an-hero *, .an-live i, .an-tile, .an-tile::before, .an-panel, .an-fill, .an-gauge, .an-empty,
    .an-empty-ring, .an-label::after, .an-orb { animation: none !important; transition: none !important; }
}
</style>
"""


def _html(markup: str) -> str:
    """Strip indentation and blank lines so Markdown never treats the HTML as code."""
    return "\n".join(line.strip() for line in markup.strip().splitlines() if line.strip())


def _label(text: str, sub: str = "") -> None:
    st.markdown(f'<div class="an-label">{escape(text)}</div>', unsafe_allow_html=True)
    if sub:
        st.markdown(f'<div class="an-sub">{escape(sub)}</div>', unsafe_allow_html=True)


def _tile(index: int, label: str, value: str, note: str) -> str:
    return (
        f'<div class="an-tile" style="animation-delay:{0.1 + index * 0.1:.2f}s">'
        f"<small>{escape(label)}</small><b>{escape(value)}</b><span>{escape(note)}</span></div>"
    )


def _gauge(percent: float, label: str, color: str = "#D4D7D3") -> str:
    shown = max(0.0, min(100.0, percent))
    return (
        '<div class="an-gauge-wrap">'
        f'<div class="an-gauge" style="--p:{shown:.1f};--c:{color}"><strong>{percent:.1f}%</strong></div>'
        f"<small>{escape(label)}</small></div>"
    )


def render() -> None:
    st.markdown(_html(_CSS), unsafe_allow_html=True)

    telemetry = get_router().telemetry
    rows = telemetry.query_history
    summary = telemetry.get_session_summary()
    latencies = [row["latency_ms"] for row in rows if "latency_ms" in row]
    average_latency = sum(latencies) / len(latencies) if latencies else 0.0
    fallback_count = sum(bool(row.get("fallback_triggered")) for row in rows)

    metrics = (
        ("Routed questions", str(summary["total_queries"]), "Current Streamlit session"),
        ("Average latency", f"{average_latency:.0f} ms" if latencies else "—", "Recorded model-call latency"),
        ("Estimated spend", f"${summary['cumulative_spend']:.6f}", "Based on configured token pricing"),
        ("Estimated savings", f"${summary['cumulative_dollars_saved']:.6f}", "Versus configured baseline proxy"),
    )
    tiles = "".join(_tile(i, *metric) for i, metric in enumerate(metrics))

    st.markdown(
        _html(
            f"""
            <div class="an-hero">
                <div class="an-orb"></div>
                <div class="an-live"><i></i>Live session</div>
                <h1 class="an-title">SDG Analytics</h1>
                <p class="an-lead">See what the router is doing in this session.</p>
                <p class="an-lead" style="color: #FFFFFF; font-size: 11px; line-height: 1.8; margin: 0; opacity: 0.9;">
    Session-scoped operational proxies only. Query counts do not measure learning outcomes or access; savings compare estimated token cost with the configured frontier-model proxy.
</p>
            </div>
            <div class="an-tiles">{tiles}</div>
            """
        ),
        unsafe_allow_html=True,
    )

    if not rows:
        st.markdown(
            _html(
                """
                <div class="an-empty">
                    <div class="an-empty-ring" aria-hidden="true"></div>
                    <h3>No session data yet</h3>
                    <p>Run a tutor question or calibration evaluation to populate live analytics.</p>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )
        return

    model_counts: dict[str, int] = {}
    for row in rows:
        for model in row.get("models", []):
            model_counts[model] = model_counts.get(model, 0) + 1
    peak = max(model_counts.values()) if model_counts else 1

    bars = "".join(
        _html(
            f"""
            <div class="an-bar">
                <div class="an-bar-top"><span>{escape(model)}</span><em>{count}</em></div>
                <div class="an-track"><div class="an-fill" style="width:{count / peak * 100:.1f}%;animation-delay:{0.2 + i * 0.12:.2f}s"></div></div>
            </div>
            """
        )
        for i, (model, count) in enumerate(sorted(model_counts.items(), key=lambda item: -item[1]))
    )

    fallback_rate = fallback_count / len(rows) * 100
    savings_pct = summary["overall_savings_pct"]
    tokens_in = f"{summary['total_input_tokens']:,}"
    tokens_out = f"{summary['total_output_tokens']:,}"

    _label("Model usage", "Counts include each model call; escalated requests count both models.")
    chart_column, breakdown_column = st.columns(2, gap="medium")
    with chart_column:
        st.markdown(
            f'<div class="an-panel"><h4>Calls per model</h4>{bars}</div>',
            unsafe_allow_html=True,
        )
    with breakdown_column:
        st.markdown(
            _html(
                f"""
                <div class="an-panel">
                    <h4>Routing and efficiency</h4>
                    <div class="an-gauges">
                        {_gauge(fallback_rate, "Fallback rate", "#899B9A")}
                        {_gauge(savings_pct, "Savings vs baseline", "#E5E7E3")}
                    </div>
                    <div class="an-tokens"><span>Input / output tokens</span><b>{tokens_in} / {tokens_out}</b></div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    _label("Request history", "Detailed estimates are local to this active Streamlit session.")
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
    st.write("")
    st.download_button(
        "Download session report (CSV)",
        data=output.getvalue(),
        file_name="axiom-session-report.csv",
        mime="text/csv",
    )