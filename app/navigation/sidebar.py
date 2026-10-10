"""Axiom's dark, minimal navigation."""

import streamlit as st

from app.components.branding import brand_lockup
from app.config import BRAND_NAME, BRAND_WORDMARK, NAVIGATION

EVENT = "AICON'26"

# Same palette as the pages: mist / sage / steel on forest, slate for surfaces.
# Every hover, active and focus state changes background and text together.
_SIDEBAR_CSS = """
<style>
[data-testid="stSidebar"] {
    --sb-mist: #D4D7D3; --sb-mist-hover: #E5E7E3;
    --sb-sage: #A3ADA5; --sb-steel: #899B9A;
    --sb-slate: #46565D; --sb-slate-hover: #566970;
    --sb-forest: #263A36; --sb-forest-hover: #344B45;
    --sb-ease: cubic-bezier(.2,.8,.2,1);
    color: var(--sb-mist);
}
@keyframes sb-rise { from {opacity:0; transform: translateX(-16px);} to {opacity:1; transform:none;} }
@keyframes sb-spin { to {transform: rotate(360deg);} }
@keyframes sb-blink { 0%,100% {opacity:1;} 50% {opacity:.3;} }
@keyframes sb-sweep { to {background-position: 220% 0;} }
@keyframes sb-glow { 0%,100% {opacity:.55;} 50% {opacity:.9;} }

/* Surface */
[data-testid="stSidebar"] { background: linear-gradient(180deg, #2a403c 0%, #1f302d 100%); border-right: 1px solid rgba(212,215,211,.14); }
[data-testid="stSidebar"] > div:first-child { position: relative; padding-top: 1.2rem; background: transparent; overflow-x: hidden; }
[data-testid="stSidebar"] > div:first-child::before { content: ""; position: absolute; left: -60px; top: -80px; width: 260px; height: 260px; border-radius: 50%; background: var(--sb-steel); filter: blur(80px); opacity: .5; pointer-events: none; animation: sb-glow 8s ease-in-out infinite; }
[data-testid="stSidebar"] > div:first-child > * { position: relative; }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { color: var(--sb-mist); }
[data-testid="stSidebar"] ::-webkit-scrollbar { width: 6px; }
[data-testid="stSidebar"] ::-webkit-scrollbar-thumb { background: rgba(137,155,154,.45); border-radius: 6px; }
[data-testid="stSidebar"] ::-webkit-scrollbar-track { background: transparent; }

/* Collapse button */
[data-testid="stSidebarCollapseButton"] button, [data-testid="stSidebarCollapsedControl"] button { background: transparent; border: 1px solid rgba(212,215,211,.25); border-radius: 12px; transition: background .3s, border-color .3s; }
[data-testid="stSidebarCollapseButton"] button:hover, [data-testid="stSidebarCollapsedControl"] button:hover { background: var(--sb-forest-hover); border-color: rgba(212,215,211,.55); }
[data-testid="stSidebarCollapseButton"] svg, [data-testid="stSidebarCollapsedControl"] svg { color: var(--sb-mist); fill: var(--sb-mist); }

/* Section heading */
.mr-nav-heading { margin: 1.8rem 0 .9rem; display: flex; align-items: center; gap: .8rem; font-size: .7rem; font-weight: 600; letter-spacing: .3em; text-transform: uppercase; color: var(--sb-steel) !important; }
.mr-nav-heading::after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, rgba(137,155,154,.55), transparent); order: 1; }
.mr-nav-heading em { order: 2; font-style: normal; font-size: .66rem; letter-spacing: .2em; color: var(--sb-sage); }

/* Navigation items */
[data-testid="stSidebar"] [role="radiogroup"] { gap: .35rem; counter-reset: nav; }
[data-testid="stSidebar"] [role="radiogroup"] > label { position: relative; counter-increment: nav; padding: .85rem 2.4rem .85rem 1.15rem; border-radius: 16px; border: 1px solid transparent; background: transparent; cursor: pointer; animation: sb-rise .75s var(--sb-ease) both; transition: background .35s var(--sb-ease), border-color .35s var(--sb-ease), transform .35s var(--sb-ease), box-shadow .35s; }
/*DELAYS*/
[data-testid="stSidebar"] [role="radiogroup"] > label > div:first-child { display: none; }
[data-testid="stSidebar"] [role="radiogroup"] > label p { margin: 0; display: flex; align-items: baseline; gap: 1rem; font-size: 1rem; font-weight: 300; letter-spacing: .05em; color: var(--sb-sage); transition: color .35s, letter-spacing .35s, transform .35s var(--sb-ease); }
[data-testid="stSidebar"] [role="radiogroup"] > label p::before { content: counter(nav, decimal-leading-zero); font-size: .66rem; font-weight: 600; letter-spacing: .2em; color: var(--sb-steel); transition: color .35s; }

/* Accent bar on the left edge */
[data-testid="stSidebar"] [role="radiogroup"] > label::before { content: ""; position: absolute; left: 0; top: 50%; width: 3px; height: 0; border-radius: 3px; background: var(--sb-mist); box-shadow: 0 0 14px rgba(212,215,211,.85); transform: translateY(-50%); transition: height .4s var(--sb-ease); }
/* Chevron on the right edge */
[data-testid="stSidebar"] [role="radiogroup"] > label::after { content: ""; position: absolute; right: 1.1rem; top: 50%; width: 7px; height: 7px; border-top: 1.5px solid var(--sb-mist); border-right: 1.5px solid var(--sb-mist); transform: translate(-8px, -50%) rotate(45deg); opacity: 0; transition: opacity .35s, transform .4s var(--sb-ease); }

/* Hover: darker surface, brighter text */
[data-testid="stSidebar"] [role="radiogroup"] > label:hover { background: var(--sb-forest-hover); border-color: rgba(212,215,211,.2); transform: translateX(4px); }
[data-testid="stSidebar"] [role="radiogroup"] > label:hover p { color: var(--sb-mist); }
[data-testid="stSidebar"] [role="radiogroup"] > label:hover p::before { color: var(--sb-mist); }
[data-testid="stSidebar"] [role="radiogroup"] > label:hover::after { opacity: 1; transform: translate(0, -50%) rotate(45deg); }

/* Selected */
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) { background: linear-gradient(90deg, rgba(86,105,112,.8), rgba(86,105,112,.14)); border-color: rgba(212,215,211,.32); box-shadow: 0 10px 26px rgba(0,0,0,.25); }
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked)::before { height: 60%; }
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked)::after { opacity: 1; transform: translate(0, -50%) rotate(45deg); }
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) p { color: var(--sb-mist-hover); font-weight: 400; letter-spacing: .08em; }
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) p::before { color: var(--sb-mist); }

/* Keyboard focus and pressed */
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:focus-visible) { outline: 2px solid var(--sb-sage); outline-offset: 2px; }
[data-testid="stSidebar"] [role="radiogroup"] > label:active { transform: translateX(2px) scale(.985); background: var(--sb-slate-hover); }

.mr-divider { height: 1px; margin: 1.8rem 0 1.5rem; background: linear-gradient(90deg, rgba(212,215,211,.3), transparent); }

/* Event panel: a slow light sweeps around the border */
.mr-system-panel { position: relative; overflow: hidden; padding: 1.35rem 1.3rem 1.2rem; border-radius: 22px; border: 1px solid rgba(212,215,211,.16); background: #263A36; transition: transform .45s var(--sb-ease), box-shadow .45s; }
.mr-system-panel::before { content: ""; position: absolute; left: 50%; top: 50%; width: 360px; height: 360px; margin: -180px 0 0 -180px; border-radius: 50%; background: conic-gradient(from 0deg, transparent 0 72%, rgba(212,215,211,.55) 86%, transparent 100%); animation: sb-spin 10s linear infinite; pointer-events: none; }
.mr-system-panel::after { content: ""; position: absolute; inset: 1px; border-radius: 21px; background: linear-gradient(160deg, #344B45, #243733); pointer-events: none; }
.mr-system-panel > * { position: relative; z-index: 1; }
.mr-system-panel:hover { transform: translateY(-4px); box-shadow: 0 20px 40px rgba(0,0,0,.35); }
.mr-system-eyebrow { display: flex; align-items: center; gap: .55rem; font-size: .66rem; font-weight: 600; letter-spacing: .26em; text-transform: uppercase; color: var(--sb-sage) !important; }
.mr-system-eyebrow::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: var(--sb-mist); animation: sb-blink 1.8s infinite; }
.mr-system-title { margin: .85rem 0 .3rem; font-size: 1.7rem; font-weight: 200; letter-spacing: .14em; text-transform: uppercase; background: linear-gradient(100deg, #D4D7D3 25%, #E5E7E3 45%, #D4D7D3 65%, #E5E7E3 85%); background-size: 220% 100%; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; color: transparent !important; animation: sb-sweep 8s linear infinite; }
.mr-system-description { font-size: .84rem; line-height: 1.6; color: var(--sb-mist) !important; }
.mr-system-caption { margin-top: 1rem; padding-top: .9rem; border-top: 1px solid rgba(212,215,211,.16); font-size: .62rem; font-weight: 600; letter-spacing: .26em; color: var(--sb-steel) !important; }

.mr-sidebar-footer { margin-top: 1.5rem; text-align: center; font-size: .62rem; letter-spacing: .3em; text-transform: uppercase; color: var(--sb-sage) !important; }
.mr-sidebar-footer span { font-weight: 600; color: var(--sb-mist) !important; }

@media (prefers-reduced-motion: reduce) {
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] *::before, [data-testid="stSidebar"] *::after { animation: none !important; transition: none !important; }
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

        st.markdown(
            f'<div class="mr-nav-heading">Workspace<em>{len(NAVIGATION):02d}</em></div>',
            unsafe_allow_html=True,
        )

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