"""Axiom's dark, minimal navigation."""

import streamlit as st

from app.components.branding import brand_lockup
from app.config import BRAND_NAME, BRAND_WORDMARK, NAVIGATION

EVENT = "AICON'26"
DEVELOPER_NAME = "Abdul Basit"
PORTFOLIO_URL = "https://abdulbasit-archer.vercel.app/"
WHATSAPP_URL = "https://wa.me/923415878569?text=Hi%20Abdul%2C%20I%20found%20you%20through%20AICON%2726."

# Same palette and fonts as the pages: mist / sage / steel on forest, slate for surfaces.
# Every hover, active and focus state changes background and text together.
_SIDEBAR_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;700&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');

[data-testid="stSidebar"] {
    --sb-mist: #D4D7D3; --sb-mist-hover: #E5E7E3;
    --sb-sage: #A3ADA5; --sb-steel: #899B9A;
    --sb-slate: #46565D; --sb-slate-hover: #566970;
    --sb-forest: #263A36; --sb-forest-hover: #344B45;
    --sb-ease: cubic-bezier(.2,.8,.2,1);
    --sb-display: 'Space Grotesk', 'Inter', system-ui, sans-serif;
    --sb-body: 'Inter', system-ui, sans-serif;
    --sb-mono: 'JetBrains Mono', ui-monospace, monospace;
    color: var(--sb-mist);
    font-family: var(--sb-body);
}
@keyframes sb-rise { from {opacity:0; transform: translateX(-18px); filter: blur(4px);} to {opacity:1; transform:none; filter:none;} }
@keyframes sb-spin { to {transform: rotate(360deg);} }
@keyframes sb-blink { 0%,100% {opacity:1;} 50% {opacity:.3;} }
@keyframes sb-sweep { to {background-position: 220% 0;} }
@keyframes sb-glow { 0%,100% {opacity:.5;} 50% {opacity:.9;} }
@keyframes sb-drift { 0%,100% {transform: translate(0,0);} 50% {transform: translate(26px,18px);} }
@keyframes sb-pulse { 0% {box-shadow: 0 0 0 0 rgba(143,209,158,.55);} 70% {box-shadow: 0 0 0 8px rgba(143,209,158,0);} 100% {box-shadow: 0 0 0 0 rgba(143,209,158,0);} }
@keyframes sb-shine { from {transform: translateX(-120%) skewX(-18deg);} to {transform: translateX(260%) skewX(-18deg);} }

/* Surface */
[data-testid="stSidebar"] { background: linear-gradient(180deg, #2c423e 0%, #1c2c29 100%); border-right: 1px solid rgba(212,215,211,.14); }
[data-testid="stSidebar"] > div:first-child { position: relative; padding-top: 1.2rem; background: transparent; overflow-x: hidden; }
[data-testid="stSidebar"] > div:first-child::before { content: ""; position: absolute; left: -60px; top: -80px; width: 260px; height: 260px; border-radius: 50%; background: var(--sb-steel); filter: blur(80px); opacity: .5; pointer-events: none; animation: sb-glow 8s ease-in-out infinite, sb-drift 18s ease-in-out infinite; }
[data-testid="stSidebar"] > div:first-child::after { content: ""; position: absolute; inset: 0; pointer-events: none; opacity: .05; mix-blend-mode: overlay; background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>"); }
[data-testid="stSidebar"] > div:first-child > * { position: relative; z-index: 1; }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { color: var(--sb-mist); font-family: var(--sb-body); }
[data-testid="stSidebar"] ::-webkit-scrollbar { width: 6px; }
[data-testid="stSidebar"] ::-webkit-scrollbar-thumb { background: rgba(137,155,154,.45); border-radius: 6px; }
[data-testid="stSidebar"] ::-webkit-scrollbar-track { background: transparent; }

/* Collapse button */
[data-testid="stSidebarCollapseButton"] button, [data-testid="stSidebarCollapsedControl"] button { background: transparent; border: 1px solid rgba(212,215,211,.25); border-radius: 12px; transition: background .3s, border-color .3s, transform .3s var(--sb-ease); }
[data-testid="stSidebarCollapseButton"] button:hover, [data-testid="stSidebarCollapsedControl"] button:hover { background: var(--sb-forest-hover); border-color: rgba(212,215,211,.55); transform: scale(1.06); }
[data-testid="stSidebarCollapseButton"] svg, [data-testid="stSidebarCollapsedControl"] svg { color: var(--sb-mist); fill: var(--sb-mist); }

/* Section heading */
.mr-nav-heading { margin: 1.8rem 0 .9rem; display: flex; align-items: center; gap: .8rem; font-family: var(--sb-mono); font-size: .68rem; font-weight: 500; letter-spacing: .28em; text-transform: uppercase; color: var(--sb-steel) !important; }
.mr-nav-heading::after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, rgba(137,155,154,.55), transparent); order: 1; }
.mr-nav-heading em { order: 2; font-style: normal; padding: .12rem .45rem; border: 1px solid rgba(212,215,211,.28); border-radius: 6px; font-size: .62rem; letter-spacing: .12em; color: var(--sb-mist) !important; }

/* Navigation items */
[data-testid="stSidebar"] [role="radiogroup"] { gap: .35rem; counter-reset: nav; }
[data-testid="stSidebar"] [role="radiogroup"] > label { position: relative; overflow: hidden; counter-increment: nav; padding: .85rem 2.4rem .85rem 1.15rem; border-radius: 16px; border: 1px solid transparent; background: transparent; cursor: pointer; animation: sb-rise .8s var(--sb-ease) both; transition: background .35s var(--sb-ease), border-color .35s var(--sb-ease), transform .35s var(--sb-ease), box-shadow .35s; }
/*DELAYS*/
[data-testid="stSidebar"] [role="radiogroup"] > label > div:first-child { display: none; }
[data-testid="stSidebar"] [role="radiogroup"] > label p { margin: 0; display: flex; align-items: baseline; gap: 1rem; font-family: var(--sb-display); font-size: 1.02rem; font-weight: 400; letter-spacing: .03em; color: var(--sb-sage); transition: color .35s, letter-spacing .35s, transform .35s var(--sb-ease); }
[data-testid="stSidebar"] [role="radiogroup"] > label p::before { content: counter(nav, decimal-leading-zero); font-family: var(--sb-mono); font-size: .66rem; font-weight: 500; letter-spacing: .14em; color: var(--sb-steel); transition: color .35s; }

/* Light sweep across the item on hover */
[data-testid="stSidebar"] [role="radiogroup"] > label > div:last-child { position: relative; z-index: 1; }

/* Accent bar on the left edge */
[data-testid="stSidebar"] [role="radiogroup"] > label::before { content: ""; position: absolute; left: 0; top: 50%; width: 3px; height: 0; border-radius: 3px; background: var(--sb-mist); box-shadow: 0 0 14px rgba(212,215,211,.85); transform: translateY(-50%); transition: height .4s var(--sb-ease); }
/* Chevron on the right edge */
[data-testid="stSidebar"] [role="radiogroup"] > label::after { content: ""; position: absolute; right: 1.1rem; top: 50%; width: 7px; height: 7px; border-top: 1.5px solid var(--sb-mist); border-right: 1.5px solid var(--sb-mist); transform: translate(-8px, -50%) rotate(45deg); opacity: 0; transition: opacity .35s, transform .4s var(--sb-ease); }

/* Hover: darker surface, brighter text */
[data-testid="stSidebar"] [role="radiogroup"] > label:hover { background: var(--sb-forest-hover); border-color: rgba(212,215,211,.2); transform: translateX(5px); }
[data-testid="stSidebar"] [role="radiogroup"] > label:hover p { color: var(--sb-mist-hover); letter-spacing: .05em; }
[data-testid="stSidebar"] [role="radiogroup"] > label:hover p::before { color: var(--sb-mist); }
[data-testid="stSidebar"] [role="radiogroup"] > label:hover::after { opacity: 1; transform: translate(0, -50%) rotate(45deg); }

/* Selected */
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) { background: linear-gradient(90deg, rgba(86,105,112,.85), rgba(86,105,112,.14)); border-color: rgba(212,215,211,.34); box-shadow: 0 10px 26px rgba(0,0,0,.28), inset 0 1px 0 rgba(212,215,211,.12); }
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked)::before { height: 62%; }
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked)::after { opacity: 1; transform: translate(0, -50%) rotate(45deg); }
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) p { color: var(--sb-mist-hover); font-weight: 500; letter-spacing: .06em; }
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
.mr-system-eyebrow { display: flex; align-items: center; gap: .55rem; font-family: var(--sb-mono); font-size: .62rem; font-weight: 500; letter-spacing: .2em; text-transform: uppercase; color: var(--sb-sage) !important; }
.mr-system-eyebrow::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: #8FD19E; animation: sb-pulse 2s infinite; }
.mr-system-title { margin: .85rem 0 .3rem; font-family: var(--sb-display); font-size: 1.75rem; font-weight: 300; letter-spacing: .12em; text-transform: uppercase; background: linear-gradient(100deg, #D4D7D3 25%, #F2F4F1 45%, #D4D7D3 65%, #F2F4F1 85%); background-size: 220% 100%; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; color: transparent !important; animation: sb-sweep 8s linear infinite; }
.mr-system-description { font-size: .84rem; font-weight: 300; line-height: 1.6; color: var(--sb-mist) !important; }
.mr-system-caption { margin-top: 1rem; padding-top: .9rem; border-top: 1px solid rgba(212,215,211,.16); font-family: var(--sb-mono); font-size: .6rem; font-weight: 500; letter-spacing: .22em; color: var(--sb-steel) !important; }

/* Developer chip */
.mr-dev { margin-top: 1rem; padding: .95rem 1rem; border-radius: 18px; border: 1px solid rgba(212,215,211,.16); background: rgba(27,43,40,.55); transition: border-color .4s, transform .4s var(--sb-ease); }
.mr-dev:hover { border-color: rgba(212,215,211,.4); transform: translateY(-2px); }
.mr-dev-top { display: flex; align-items: center; gap: .8rem; }
.mr-dev-avatar { flex: none; width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: var(--sb-display); font-size: .85rem; font-weight: 500; letter-spacing: .06em; color: var(--sb-mist) !important; background: radial-gradient(circle at 30% 25%, rgba(137,155,154,.6), rgba(27,43,40,.97)); border: 1px solid rgba(212,215,211,.4); }
.mr-dev-name { font-family: var(--sb-display); font-size: .95rem; font-weight: 500; line-height: 1.2; color: var(--sb-mist-hover) !important; }
.mr-dev-role { font-family: var(--sb-mono); font-size: .58rem; font-weight: 500; letter-spacing: .16em; text-transform: uppercase; color: var(--sb-steel) !important; }
.mr-dev-links { display: grid; grid-template-columns: 1fr 1fr; gap: .5rem; margin-top: .85rem; }
[data-testid="stSidebar"] a.mr-dev-btn { position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center; gap: .35rem; padding: .5rem .4rem; border-radius: 999px; font-family: var(--sb-mono); font-size: .62rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; text-decoration: none !important; color: var(--sb-mist) !important; border: 1px solid rgba(212,215,211,.35); background: transparent; transition: background .3s, color .3s, border-color .3s, transform .3s var(--sb-ease); }
[data-testid="stSidebar"] a.mr-dev-btn::after { content: ""; position: absolute; top: 0; bottom: 0; left: 0; width: 40%; background: linear-gradient(90deg, transparent, rgba(255,255,255,.4), transparent); transform: translateX(-120%) skewX(-18deg); }
[data-testid="stSidebar"] a.mr-dev-btn:hover { background: var(--sb-mist); color: var(--sb-forest) !important; border-color: var(--sb-mist); transform: translateY(-2px); }
[data-testid="stSidebar"] a.mr-dev-btn:hover::after { animation: sb-shine .8s var(--sb-ease); }
[data-testid="stSidebar"] a.mr-dev-btn.wa { color: #0E2A1A !important; background: #8FD19E; border-color: #8FD19E; }
[data-testid="stSidebar"] a.mr-dev-btn.wa:hover { background: #A9E0B5; border-color: #A9E0B5; color: #0E2A1A !important; }
[data-testid="stSidebar"] a.mr-dev-btn:focus-visible { outline: 2px solid var(--sb-sage); outline-offset: 2px; }

.mr-sidebar-footer { margin-top: 1.5rem; text-align: center; font-family: var(--sb-mono); font-size: .6rem; letter-spacing: .28em; text-transform: uppercase; color: var(--sb-sage) !important; }
.mr-sidebar-footer span { font-weight: 700; color: var(--sb-mist) !important; }

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
                <div class="mr-dev">
                    <div class="mr-dev-top">
                        <div class="mr-dev-avatar" aria-hidden="true">AB</div>
                        <div>
                            <div class="mr-dev-name">{DEVELOPER_NAME}</div>
                            <div class="mr-dev-role">Developer</div>
                        </div>
                    </div>
                    <div class="mr-dev-links">
                        <a class="mr-dev-btn" href="{PORTFOLIO_URL}" target="_blank" rel="noopener noreferrer">Portfolio &#8599;</a>
                        <a class="mr-dev-btn wa" href="{WHATSAPP_URL}" target="_blank" rel="noopener noreferrer">WhatsApp &#8599;</a>
                    </div>
                </div>
                <div class="mr-sidebar-footer"><span>{BRAND_WORDMARK}</span> Learning Workspace</div>
                """
            ),
            unsafe_allow_html=True,
        )

    return destination