"""Axiom's dark, minimal navigation."""

import streamlit as st

from app.components.branding import brand_lockup
from app.config import BRAND_NAME, BRAND_WORDMARK, NAVIGATION

EVENT = "AICON'26"

# Palette: C5C5C5 mist | 949B96 sage | 4C5B61 slate | 2C423F forest | 829191 steel
# Every text/background pair below is dark-on-light or light-on-dark. Never light-on-light.
_SIDEBAR_CSS = """
<style>
[data-testid="stSidebar"] {
    --sb-mist: #C5C5C5; --sb-sage: #949B96; --sb-slate: #4C5B61; --sb-forest: #2C423F; --sb-steel: #829191;
    --sb-ease: cubic-bezier(.2,.8,.2,1);
}
@keyframes sb-rise { from {opacity:0; transform: translateX(-14px);} to {opacity:1; transform:none;} }
@keyframes sb-spin { to {transform: rotate(360deg);} }
@keyframes sb-blink { 0%,100% {opacity:1;} 50% {opacity:.3;} }
@keyframes sb-sweep { to {background-position: 200% 0;} }

/* Surface */
[data-testid="stSidebar"] { background: linear-gradient(180deg, #2C423F 0%, #263a37 100%); border-right: 1px solid rgba(197,197,197,.12); }
[data-testid="stSidebar"] > div:first-child { padding-top: 1.2rem; background: transparent; }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label, [data-testid="stSidebar"] div { color: var(--sb-mist); }
[data-testid="stSidebar"] ::-webkit-scrollbar { width: 6px; }
[data-testid="stSidebar"] ::-webkit-scrollbar-thumb { background: rgba(130,145,145,.45); border-radius: 6px; }
[data-testid="stSidebar"] ::-webkit-scrollbar-track { background: transparent; }

/* Collapse button */
[data-testid="stSidebarCollapseButton"] button, [data-testid="stSidebarCollapsedControl"] button { background: transparent; border: 1px solid rgba(197,197,197,.2); border-radius: 12px; transition: background .3s, border-color .3s; }
[data-testid="stSidebarCollapseButton"] button:hover, [data-testid="stSidebarCollapsedControl"] button:hover { background: rgba(76,91,97,.55); border-color: rgba(197,197,197,.45); }
[data-testid="stSidebarCollapseButton"] svg, [data-testid="stSidebarCollapsedControl"] svg { color: var(--sb-mist); fill: var(--sb-mist); }

/* Section heading */
.mr-nav-heading { margin: 1.6rem 0 .8rem; display: flex; align-items: center; gap: .8rem; font-size: .7rem; letter-spacing: .3em; text-transform: uppercase; color: var(--sb-mist) !important; }
.mr-nav-heading::after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, rgba(130,145,145,.5), transparent); }

/* Navigation items */
[data-testid="stSidebar"] [role="radiogroup"] { gap: .25rem; counter-reset: nav; }
[data-testid="stSidebar"] [role="radiogroup"] > label { position: relative; counter-increment: nav; padding: .75rem .9rem .75rem 1.1rem; border-radius: 14px; border: 1px solid transparent; background: transparent; cursor: pointer; animation: sb-rise .7s both; transition: background .35s var(--sb-ease), border-color .35s var(--sb-ease), transform .35s var(--sb-ease); }
/*DELAYS*/
[data-testid="stSidebar"] [role="radiogroup"] > label > div:first-child { display: none; }
[data-testid="stSidebar"] [role="radiogroup"] > label p { margin: 0; display: flex; align-items: baseline; gap: .9rem; font-size: .95rem; font-weight: 400; letter-spacing: .06em; color: var(--sb-mist); transition: color .35s, letter-spacing .35s; }
[data-testid="stSidebar"] [role="radiogroup"] > label p::before { content: counter(nav, decimal-leading-zero); font-size: .66rem; letter-spacing: .2em; color: var(--sb-mist); transition: color .35s; }
[data-testid="stSidebar"] [role="radiogroup"] > label::before { content: ""; position: absolute; left: 0; top: 50%; width: 2px; height: 0; border-radius: 2px; background: var(--sb-mist); box-shadow: 0 0 12px rgba(197,197,197,.8); transform: translateY(-50%); transition: height .4s var(--sb-ease); }

/* Hover: background and text change together, always light text on a dark surface */
[data-testid="stSidebar"] [role="radiogroup"] > label:hover { background: rgba(76,91,97,.55); border-color: rgba(197,197,197,.18); transform: translateX(4px); }
[data-testid="stSidebar"] [role="radiogroup"] > label:hover p { color: var(--sb-mist); }
[data-testid="stSidebar"] [role="radiogroup"] > label:hover p::before { color: var(--sb-mist); }

/* Selected */
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) { background: linear-gradient(90deg, rgba(76,91,97,.7), rgba(76,91,97,.18)); border-color: rgba(197,197,197,.28); }
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked)::before { height: 58%; }
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) p { color: var(--sb-mist); letter-spacing: .1em; }
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) p::before { color: var(--sb-mist); }

/* Keyboard focus */
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:focus-visible) { outline: 2px solid var(--sb-steel); outline-offset: 2px; }

/* Pressed */
[data-testid="stSidebar"] [role="radiogroup"] > label:active { transform: translateX(2px) scale(.985); }

.mr-divider { height: 1px; margin: 1.6rem 0 1.4rem; background: linear-gradient(90deg, rgba(197,197,197,.25), transparent); }

/* Panel */
.mr-system-panel { position: relative; overflow: hidden; padding: 1.25rem 1.25rem 1.1rem; border-radius: 20px; border: 1px solid rgba(197,197,197,.14); background: linear-gradient(160deg, rgba(76,91,97,.45), rgba(44,66,63,.15)); transition: border-color .4s, transform .4s var(--sb-ease); }
.mr-system-panel:hover { border-color: rgba(197,197,197,.35); transform: translateY(-3px); }
.mr-system-panel::before { content: ""; position: absolute; right: -34px; top: -34px; width: 110px; height: 110px; border-radius: 50%; border: 1px dashed rgba(197,197,197,.35); animation: sb-spin 30s linear infinite; pointer-events: none; }
.mr-system-eyebrow { display: flex; align-items: center; gap: .5rem; font-size: .66rem; letter-spacing: .28em; text-transform: uppercase; color: var(--sb-mist) !important; }
.mr-system-eyebrow::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: var(--sb-mist); animation: sb-blink 1.8s infinite; }
.mr-system-title { margin: .75rem 0 .2rem; font-size: 1.55rem; font-weight: 200; letter-spacing: .12em; text-transform: uppercase; background: linear-gradient(100deg, #C5C5C5 30%, #FFFFFF 50%, #E4E4E4 70%, #C5C5C5 90%); background-size: 220% 100%; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; color: transparent !important; animation: sb-sweep 8s linear infinite; }
.mr-system-description { font-size: .82rem; font-weight: 500; color: var(--sb-mist) !important; }
.mr-system-caption { margin-top: .9rem; font-size: .62rem; letter-spacing: .26em; color: var(--sb-mist) !important; }

.mr-sidebar-footer { margin-top: 1.4rem; text-align: center; font-size: .62rem; letter-spacing: .3em; text-transform: uppercase; color: var(--sb-mist) !important; }
.mr-sidebar-footer span { color: var(--sb-mist) !important; }

@media (prefers-reduced-motion: reduce) {
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] *::before { animation: none !important; transition: none !important; }
}
</style>
"""


def _html(markup: str) -> str:
    """Strip indentation and blank lines so Markdown never treats the HTML as code."""
    return "\n".join(line.strip() for line in markup.strip().splitlines() if line.strip())


def _sidebar_css() -> str:
    """Return the sidebar stylesheet with staggered entrance delays for every nav item."""
    delays = "\n".join(
        f'[data-testid="stSidebar"] [role="radiogroup"] > label:nth-child({i}) '
        f"{{ animation-delay: {0.05 + (i - 1) * 0.07:.2f}s; }}"
        for i in range(1, len(NAVIGATION) + 1)
    )
    return _html(_SIDEBAR_CSS.replace("/*DELAYS*/", delays))


def render_sidebar() -> str:
    """Render the sidebar and return the selected destination."""

    st.markdown(_sidebar_css(), unsafe_allow_html=True)

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