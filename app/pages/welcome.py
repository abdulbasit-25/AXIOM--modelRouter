"""Welcome page."""

import streamlit as st

from app.components import feature_card, page_footer, page_header, section_heading, steps_markup
from app.config import (
    BRAND_DESCRIPTION,
    BRAND_NAME,
    BRAND_SHORT_DESCRIPTION,
    BRAND_TAGLINE,
    BRAND_WORDMARK,
    GETTING_STARTED,
)
from app.navigation.router import set_destination

HACKATHON_NAME = "AICON'26 - Build with AI Hackathon"

_WELCOME_CSS = """
<style>
@keyframes ax-gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
@keyframes ax-pulse { 0% {box-shadow: 0 0 0 0 rgba(52,211,153,.7);} 70% {box-shadow: 0 0 0 10px rgba(52,211,153,0);} 100% {box-shadow: 0 0 0 0 rgba(52,211,153,0);} }
@keyframes ax-float { 0%,100% {transform: translateY(0);} 50% {transform: translateY(-8px);} }
@keyframes ax-flow { 0% {background-position: 0 0;} 100% {background-position: 200% 0;} }

.ax-hero {
    position: relative; overflow: hidden; border-radius: 22px; padding: 2.4rem 2.2rem;
    background: linear-gradient(120deg, #0f172a, #312e81, #6d28d9, #0e7490, #0f172a);
    background-size: 300% 300%; animation: ax-gradient 14s ease infinite;
    color: #fff; box-shadow: 0 18px 50px rgba(79,70,229,.35);
}
.ax-hero::after {
    content: ""; position: absolute; inset: 0; pointer-events: none;
    background: radial-gradient(circle at 85% 15%, rgba(255,255,255,.18), transparent 45%);
}
.ax-event-badge {
    display: inline-flex; align-items: center; gap: .55rem; padding: .4rem .95rem; border-radius: 999px;
    background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.28);
    font-size: .8rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase;
}
.ax-dot { width: 9px; height: 9px; border-radius: 50%; background: #34d399; animation: ax-pulse 1.8s infinite; }
.ax-hero h1 { color: #fff; font-size: clamp(2rem, 4.6vw, 3.4rem); line-height: 1.08; margin: 1rem 0 .7rem; font-weight: 800; }
.ax-hero h1 span { background: linear-gradient(90deg, #67e8f9, #c4b5fd, #f9a8d4); -webkit-background-clip: text; background-clip: text; color: transparent; }
.ax-hero p { color: rgba(255,255,255,.86); font-size: 1.05rem; max-width: 46rem; margin: 0; }
.ax-chips { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1.3rem; }
.ax-chip { padding: .3rem .8rem; border-radius: 999px; font-size: .8rem; background: rgba(255,255,255,.14); border: 1px solid rgba(255,255,255,.22); }

.ax-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: .8rem; margin: 1.1rem 0 .4rem; }
.ax-stat { text-align: center; padding: 1rem .6rem; border-radius: 16px; border: 1px solid rgba(124,58,237,.25); background: rgba(124,58,237,.07); }
.ax-stat b { display: block; font-size: 1.7rem; background: linear-gradient(90deg, #7c3aed, #0891b2); -webkit-background-clip: text; background-clip: text; color: transparent; }
.ax-stat small { opacity: .75; font-size: .78rem; text-transform: uppercase; letter-spacing: .06em; }

.ax-pipeline { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 1rem; position: relative; }
.ax-node { position: relative; padding: 1.1rem 1.1rem 1.2rem; border-radius: 18px; border: 1px solid rgba(124,58,237,.28);
    background: linear-gradient(160deg, rgba(124,58,237,.10), rgba(8,145,178,.07)); transition: transform .25s, box-shadow .25s; }
.ax-node:hover { transform: translateY(-5px); box-shadow: 0 12px 28px rgba(124,58,237,.25); }
.ax-node .n { display: inline-flex; width: 2rem; height: 2rem; align-items: center; justify-content: center; border-radius: 50%;
    background: linear-gradient(135deg, #7c3aed, #0891b2); color: #fff; font-weight: 800; margin-bottom: .5rem; }
.ax-node h4 { margin: 0 0 .25rem; font-size: 1.02rem; }
.ax-node p { margin: 0; font-size: .87rem; opacity: .8; }
.ax-flowbar { height: 4px; border-radius: 4px; margin: 1rem 0 0; background: linear-gradient(90deg, #7c3aed, #0891b2, #ec4899, #7c3aed); background-size: 200% 100%; animation: ax-flow 4s linear infinite; }

.ax-judge { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1rem; }
.ax-judge-card { padding: 1.15rem; border-radius: 18px; border: 1px solid rgba(8,145,178,.3); background: rgba(8,145,178,.07); }
.ax-judge-card .ic { font-size: 1.6rem; display: inline-block; animation: ax-float 4s ease-in-out infinite; }
.ax-judge-card h4 { margin: .35rem 0 .25rem; }
.ax-judge-card p { margin: 0; font-size: .87rem; opacity: .82; }

.ax-demo { border-radius: 20px; padding: 1.4rem 1.6rem; border: 1px dashed rgba(236,72,153,.55); background: rgba(236,72,153,.06); }
.ax-demo ol { margin: .5rem 0 0 1.1rem; padding: 0; }
.ax-demo li { margin: .35rem 0; }
.ax-sdg { display: flex; gap: 1rem; align-items: center; padding: 1.1rem 1.3rem; border-radius: 18px; background: linear-gradient(90deg, rgba(196,18,48,.12), rgba(124,58,237,.08)); border: 1px solid rgba(196,18,48,.3); }
.ax-sdg .badge { flex: none; width: 3.4rem; height: 3.4rem; border-radius: 12px; background: #c5192d; color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.15rem; }
.ax-sdg p { margin: 0; }
</style>
"""


def _html(markup: str) -> str:
    """Strip leading indentation so Markdown never treats the HTML as a code block."""
    return "\n".join(line.strip() for line in markup.strip().splitlines() if line.strip())


def render() -> None:
    st.markdown(_html(_WELCOME_CSS), unsafe_allow_html=True)

    page_header(
        f"{BRAND_WORDMARK} · {HACKATHON_NAME.upper()}",
        BRAND_TAGLINE,
        f"{BRAND_SHORT_DESCRIPTION} {BRAND_DESCRIPTION}",
    )

    # ------------------------------------------------------------------ Hero
    st.markdown(
        _html(
            f"""
            <div class="ax-hero">
                <div class="ax-event-badge"><span class="ax-dot"></span>Live at {HACKATHON_NAME}</div>
                <h1>{BRAND_NAME}: <span>the right AI for every question.</span></h1>
                <p>{BRAND_DESCRIPTION} Every student question is classified, routed to the best-fit model, verified, and escalated only when needed, so learning gets smarter while costs stay low.</p>
                <div class="ax-chips">
                    <span class="ax-chip">Smart model routing</span>
                    <span class="ax-chip">Answer verification</span>
                    <span class="ax-chip">Auto-escalation</span>
                    <span class="ax-chip">Live cost telemetry</span>
                    <span class="ax-chip">Built for SDG 4</span>
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    cta_left, cta_mid, cta_right = st.columns(3, gap="small")
    with cta_left:
        if st.button("Launch the AI Tutor", type="primary", width="stretch", key="cta_tutor"):
            set_destination("Production AI Tutor")
    with cta_mid:
        if st.button("See routing in Calibration Studio", width="stretch", key="cta_calibration"):
            set_destination("Calibration Studio")
    with cta_right:
        if st.button(f"About {BRAND_NAME}", width="stretch", key="cta_about"):
            set_destination("About")

    # ----------------------------------------------------------------- Stats
    st.markdown(
        _html(
            """
            <div class="ax-stats">
                <div class="ax-stat"><b>4</b><small>Pipeline stages</small></div>
                <div class="ax-stat"><b>3</b><small>Live workspaces</small></div>
                <div class="ax-stat"><b>Per-query</b><small>Cost telemetry</small></div>
                <div class="ax-stat"><b>SDG 4</b><small>Quality education</small></div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------------- How it works
    section_heading(
        "How it works",
        "One question travels through four stages in seconds, and you can inspect every decision.",
    )
    st.markdown(
        _html(
            """
            <div class="ax-pipeline">
                <div class="ax-node"><div class="n">1</div><h4>Classify</h4><p>The question classifier estimates complexity and subject: vocabulary, curriculum, or STEM.</p></div>
                <div class="ax-node"><div class="n">2</div><h4>Route</h4><p>The model router picks the most cost-efficient model that can handle the question well.</p></div>
                <div class="ax-node"><div class="n">3</div><h4>Verify</h4><p>The response verifier checks the answer quality before a student ever sees it.</p></div>
                <div class="ax-node"><div class="n">4</div><h4>Escalate</h4><p>Weak answers are automatically retried on a stronger tier, with every step logged.</p></div>
            </div>
            <div class="ax-flowbar"></div>
            """
        ),
        unsafe_allow_html=True,
    )
    st.caption(
        "If Groq is not configured or available, the app clearly labels its local mock response, so demos never fail silently."
    )

    # -------------------------------------------------------------- Features
    section_heading("Explore the workspaces", "Tutor, evaluate, and measure, all in one prototype.")
    features = (
        ("Production AI Tutor", "Ask an educational question and watch routing, verification, fallback, and cost metrics update live."),
        ("Calibration Studio", "Compare expected question complexity with the tier the router actually selected, and spot miscalibration."),
        ("SDG Analytics", "See session-level education-support activity and cost-efficiency indicators from recorded session data."),
    )
    with st.container(key="features"):
        for column, (heading, body) in zip(st.columns(3, gap="medium"), features):
            with column:
                feature_card(heading, body)
                if st.button(f"Open {heading}", key=f"feature_{heading}", width="stretch"):
                    set_destination(heading)

    # ----------------------------------------------------------- Hackathon
    section_heading(
        f"Built for {HACKATHON_NAME}",
        "Why Axiom is a strong fit for a build-with-AI challenge.",
    )
    st.markdown(
        _html(
            """
            <div class="ax-judge">
                <div class="ax-judge-card"><span class="ic">💡</span><h4>Innovation</h4><p>Instead of one big model for everything, Axiom matches each question to the right model tier.</p></div>
                <div class="ax-judge-card"><span class="ic">🌍</span><h4>Impact</h4><p>Cheaper, verified AI tutoring makes quality learning support easier to scale to more students.</p></div>
                <div class="ax-judge-card"><span class="ic">⚙️</span><h4>Technical depth</h4><p>Classifier, router, verifier, escalation, and cost telemetry work together as one integrated engine.</p></div>
                <div class="ax-judge-card"><span class="ic">🎬</span><h4>Demo-ready</h4><p>Every routing decision is visible on screen, so judges can see the AI think in real time.</p></div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    st.markdown("&nbsp;", unsafe_allow_html=True)
    st.markdown(
        _html(
            """
            <div class="ax-sdg">
                <div class="badge">SDG 4</div>
                <p><b>Quality Education.</b> Axiom is designed around the idea that AI tutoring should be accurate, accountable, and affordable, because the best support is the support that can actually reach every learner.</p>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------ Demo path
    section_heading("60-second demo path", "A quick script for judges and first-time visitors.")
    st.markdown(
        _html(
            """
            <div class="ax-demo">
                <b>Try this flow:</b>
                <ol>
                    <li>Open the <b>Production AI Tutor</b> and ask a simple vocabulary question, then a harder STEM one.</li>
                    <li>Compare the selected model, verification result, and cost for each answer.</li>
                    <li>Jump to <b>Calibration Studio</b> to see how expected complexity matches the routing tier.</li>
                    <li>Finish in <b>SDG Analytics</b> to review the session's cost-efficiency and education-support activity.</li>
                </ol>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------ Getting started
    section_heading("Getting started", "These steps help a first-time user understand the current prototype flow.")
    st.markdown(f'<div class="overview-panel">{steps_markup(GETTING_STARTED)}</div>', unsafe_allow_html=True)

    final_left, final_right = st.columns([2, 1], gap="medium")
    with final_left:
        st.markdown(f"**Ready to see {BRAND_NAME} in action at {HACKATHON_NAME}?**")
    with final_right:
        if st.button("Start the demo", type="primary", width="stretch", key="cta_final"):
            set_destination("Production AI Tutor")

    page_footer()