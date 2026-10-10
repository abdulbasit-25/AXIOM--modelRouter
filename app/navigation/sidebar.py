"""Axiom's dark, minimal navigation."""

import streamlit as st

from app.components.branding import brand_lockup
from app.config import BRAND_NAME, BRAND_WORDMARK, NAVIGATION

EVENT = "AICON'26"

# Palette: C5C5C5  949B96  4C5B61  2C423F  829191
_SIDEBAR_CSS = """
<style>
@keyframes sb-rise { from {opacity:0; transform: translateX(-14px);} to {opacity:1; transform:none;} }
@keyframes sb-spin { to {transform: rotate(360deg);} }
@keyframes sb-blink { 0%,100% {opacity:1;} 50% {opacity:.3;} }

[data-testid="stSidebar"] { background: linear-gradient(180deg, #2C423F 0%, #263a37 100%); border-right: 1px solid rgba(197,197,197,.12); }
[data-testid="stSidebar"] > div:first-child { padding-top: 1.2rem; }
[data-testid="stSidebar"] * { color: #C5C5C5; }

.mr-nav-heading { margin: 1.6rem 0 .8rem; display: flex; align-items: center; gap: .8rem; font-size: .7rem; letter-spacing: .3em; text-transform: uppercase; color: #829191 !important; }
.mr-nav-heading::after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, rgba(130,145,145,.5), transparent); }

[data-testid="stSidebar"] [role="radiogroup"] { gap: .25rem; }
[data-testid="stSidebar"] [role="radiogroup"] > label { position: relative; padding: .7rem .9rem .7rem 1.1rem; border-radius: 14px; border: 1px solid transparent; cursor: pointer; animation: sb-rise .7s both; transition: background .35s, border-color .35s, transform .35s; }
[data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(1) { animation-delay: .05s; }
[data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(2) { animation-delay: .12s; }
[data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(3) { animation-delay: .19s; }
[data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(4) { animation-delay: .26s; }
[data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(5) { animation-delay: .33s; }
[data-testid="stSidebar"] [role="radiogroup"] > label > div:first-child { display: none; }
[data-testid="stSidebar"] [role="radiogroup"] > label p { margin: 0; font-size: .95rem; font-weight: 300; letter-spacing: .06em; color: #949B96; transition: color .35s, letter-spacing .35s; }
[data-testid="stSidebar"] [role="radiogroup"] > label::before { content: ""; position: absolute; left: 0; top: 50%; width: 2px; height: 0; border-radius: 2px; background: #C5C5C5; box-shadow: 0 0 12px #C5C5C5; transform: translateY(-50%); transition: height .4s cubic-bezier(.2,.8,.2,1); }
[data-testid="stSidebar"] [role="radiogroup"] > label:hover { background: rgba(76,91,97,.35); transform: translateX(4px); }
[data-testid="stSidebar"] [role="radiogroup"] > label:hover p { color: #C5C5C5; }
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) { background: linear-gradient(90deg, rgba(76,91,97,.55), rgba(76,91,97,.12)); border-color: rgba(197,197,197,.2); }
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked)::before { height: 56%; }
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) p { color: #C5C5C5; letter-spacing: .1em; }

.mr-divider { height: 1px; margin: 1.6rem 0 1.4rem; background: linear-gradient(90deg, rgba(197,197,197,.25), transparent); }

.mr-system-panel { position: relative; overflow: hidden; padding: 1.2rem 1.2rem 1.1rem; border-radius: 20px; border: 1px solid rgba(197,197,197,.14); background: linear-gradient(160deg, rgba(76,91,97,.4), rgba(44,66,63,.15)); }
.mr-system-panel::before { content: ""; position: absolute; right: -34px; top: -34px; width: 110px; height: 110px; border-radius: 50%; border: 1px dashed rgba(197,197,197,.35); animation: sb-spin 30s linear infinite; }
.mr-system-eyebrow { display: flex; align-items: center; gap: .5rem; font-size: .66rem; letter-spacing: .28em; text-transform: uppercase; color: #829191 !important; }
.mr-system-eyebrow::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: #C5C5C5; animation: sb-blink 1.8s infinite; }
.mr-system-title { margin: .7rem 0 .2rem; font-size: 1.5rem; font-weight: 200; letter-spacing: .12em; text-transform: uppercase; color: #C5C5C5 !important; }
.mr-system-description { font-size: .82rem; color: #949B96 !important; }
.mr-system-caption { margin-top: .9rem; font-size: .62rem; letter-spacing: .26em; color: #829191 !important; }

.mr-sidebar-footer { margin-top: 1.4rem; text-align: center; font-size: .62rem; letter-spacing: .3em; text-transform: uppercase; color: #4C5B61 !important; }
.mr-sidebar-footer span { color: #829191 !important; }

@media (prefers-reduced-motion: reduce) { [data-testid="stSidebar"] *, .mr-system-panel::before { animation: none !important; } }
</style>
"""


def _html(markup: str) -> str:
    """Strip indentation and blank lines so Markdown never treats the HTML as code."""
    return "\n".join(line.strip() for line in markup.strip().splitlines() if line.strip())


def render_sidebar() -> str:
    """Render the sidebar and return the selected destination."""

    st.markdown(_html(_SIDEBAR_CSS), unsafe_allow_html=True)

    with st.sidebar:
        brand_lockup()

        st.markdown('<div class="mr-nav-heading">Workspace</div>', unsafe_allow_html=True)

        destination = st.radio(
            "Main navigation",
            options=NAVIGATION,
            label_visibility="collapsed",
            key="active_destination",
        )

        st.markdown(
            _html(
                f"""
                <div class="mr-divider"></div>
                <div class="mr-system-panel">
                    <div class="mr-system-eyebrow">{EVENT} / Build with AI</div>
                    <div class="mr-system-title">{BRAND_NAME}</div>
                    <div class="mr-system-description">Smart routing for smarter learning.</div>
                    <div class="mr-system-caption">AI / ROUTING / INTELLIGENCE</div>
                </div>
                <div class="mr-sidebar-footer"><span>{BRAND_WORDMARK}</span> Learning Workspace</div>
                """
            ),
            unsafe_allow_html=True,
        )

    return destination