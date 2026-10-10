"""Shared dark, minimal styling and markup helpers for the Axiom pages.

UI only. Import from the Calibration Studio and Production AI Tutor pages.
Suggested location: app/styles/page_base.py
"""

from html import escape

import streamlit as st

PAGE_BASE_CSS = """
<style>
:root {
  --mist: #D4D7D3; --mist-hover: #E5E7E3;
  --sage: #A3ADA5; --steel: #899B9A;
  --slate: #46565D; --forest: #263A36;
  --slate-hover: #566970; --forest-hover: #344B45;
  --field: rgba(24,38,35,.7);
  --line: rgba(212,215,211,.22);
  --focus-ring: #A3ADA5;
  --ease: cubic-bezier(.2,.8,.2,1);
}
.stApp { background: radial-gradient(1100px 650px at 85% -10%, rgba(137,155,154,.2), transparent 60%), radial-gradient(900px 600px at -10% 45%, rgba(70,86,93,.35), transparent 60%), var(--forest); color: var(--mist); }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1120px; padding-top: 2rem; }

@keyframes px-rise { from {opacity:0; transform: translateY(24px); filter: blur(6px);} to {opacity:1; transform:none; filter:none;} }
@keyframes px-float { 0%,100% {transform: translate(0,0);} 50% {transform: translate(30px,-24px);} }
@keyframes px-spin { to {transform: rotate(360deg);} }
@keyframes px-line { from {transform: scaleX(0);} to {transform: scaleX(1);} }
@keyframes px-down { from {transform: scaleY(0);} to {transform: scaleY(1);} }
@keyframes px-blink { 0%,100% {opacity:1;} 50% {opacity:.25;} }

/* Hero */
.px-hero { position: relative; overflow: hidden; border-radius: 28px; padding: 2.8rem 3rem; border: 1px solid rgba(212,215,211,.26); background: linear-gradient(145deg, #405653, #2C423F); box-shadow: 0 30px 70px rgba(0,0,0,.35), inset 0 1px 0 rgba(212,215,211,.2); }
.px-hero::before { content:""; position:absolute; inset:0; background-image: linear-gradient(rgba(212,215,211,.07) 1px, transparent 1px), linear-gradient(90deg, rgba(212,215,211,.07) 1px, transparent 1px); background-size: 56px 56px; -webkit-mask-image: radial-gradient(ellipse at 85% 30%, #000 15%, transparent 70%); mask-image: radial-gradient(ellipse at 85% 30%, #000 15%, transparent 70%); }
.px-orb { position:absolute; right:-70px; top:-90px; width:300px; height:300px; border-radius:50%; background: var(--steel); filter: blur(70px); opacity:.4; animation: px-float 14s ease-in-out infinite; }
.px-kicker { position: relative; display: inline-flex; align-items: center; gap: .6rem; padding: .38rem .95rem; border-radius: 999px; font-size: .72rem; letter-spacing: .2em; text-transform: uppercase; color: var(--mist); border: 1px solid rgba(212,215,211,.45); background: rgba(24,38,35,.7); animation: px-rise .9s both; }
.px-kicker i { width: 7px; height: 7px; border-radius: 50%; background: var(--mist); animation: px-blink 1.6s infinite; }
.stMarkdown h1.px-title { position: relative; margin: 1rem 0 .4rem; padding: 0; font-size: clamp(2.2rem, 6vw, 4rem); font-weight: 200; letter-spacing: .1em; line-height: 1.05; text-transform: uppercase; color: var(--mist) !important; animation: px-rise 1s .1s both; }
.stMarkdown p.px-lead { position: relative; max-width: 36rem; margin: 0; font-size: 1.08rem; line-height: 1.8; color: var(--sage) !important; animation: px-rise 1s .2s both; }
.stMarkdown p.px-note { position: relative; max-width: 44rem; margin: 1.1rem 0 0; padding-left: 1rem; border-left: 2px solid var(--steel); font-size: .82rem; line-height: 1.7; color: var(--sage) !important; }

/* Section labels */
.px-label { margin: 3rem 0 1.2rem; display: flex; align-items: center; gap: 1rem; font-size: .75rem; font-weight: 600; letter-spacing: .3em; text-transform: uppercase; color: var(--steel); }
.px-label em { font-style: normal; color: var(--mist); }
.px-label::after { content:""; flex:1; height:1px; background: linear-gradient(90deg, rgba(137,155,154,.55), transparent); transform-origin: left; animation: px-line 1.4s .2s both; }
.px-sub { margin: -.6rem 0 1.2rem; font-size: .88rem; line-height: 1.7; color: var(--sage); }

/* Cards, tiles, pills */
.px-info { height: 100%; padding: 1.3rem 1.4rem; border-radius: 20px; border: 1px solid var(--line); background: linear-gradient(160deg, #405653, #2C423F); box-shadow: 0 12px 28px rgba(0,0,0,.2); animation: px-rise .9s both; }
.px-info small { display: block; margin-bottom: .6rem; font-size: .7rem; font-weight: 600; letter-spacing: .24em; text-transform: uppercase; color: var(--steel); }
.px-info p { margin: 0; font-size: .95rem; line-height: 1.7; color: var(--mist); }
.px-tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1rem; margin-top: 1.4rem; }
.px-tile { position: relative; overflow: hidden; padding: 1.4rem 1.4rem 1.3rem; border-radius: 20px; border: 1px solid var(--line); background: linear-gradient(160deg, #405653, #2C423F); box-shadow: 0 12px 28px rgba(0,0,0,.2); animation: px-rise .9s both; transition: transform .45s var(--ease), border-color .45s, box-shadow .45s; }
.px-tile::before { content:""; position:absolute; left:0; top:0; height:2px; width:100%; background: linear-gradient(90deg, var(--mist), transparent); transform-origin: left; animation: px-line 1.4s .4s both; }
.px-tile:hover { transform: translateY(-6px); border-color: rgba(212,215,211,.45); box-shadow: 0 22px 44px rgba(0,0,0,.3); }
.px-tile small { display: block; font-size: .7rem; font-weight: 600; letter-spacing: .24em; text-transform: uppercase; color: var(--sage); }
.px-tile b { display: block; margin: .9rem 0 .35rem; font-size: clamp(1.4rem, 2.4vw, 1.9rem); font-weight: 300; color: var(--mist); word-break: break-word; }
.px-tile span { font-size: .8rem; color: var(--sage); }
.px-pills { display: flex; flex-wrap: wrap; gap: .5rem; }
.px-pill { display: inline-block; padding: .3rem .85rem; border-radius: 999px; font-size: .68rem; font-weight: 600; letter-spacing: .18em; text-transform: uppercase; color: var(--mist); border: 1px solid rgba(212,215,211,.4); background: rgba(24,38,35,.55); }
.px-panel-head { margin: 0 0 1rem; font-size: .75rem; font-weight: 600; letter-spacing: .28em; text-transform: uppercase; color: var(--steel); }

/* Routing path */
.px-path { list-style: none; margin: 0; padding: 0; }
.px-path li { position: relative; padding: 0 0 1.35rem 2.2rem; font-size: .92rem; line-height: 1.5; color: var(--mist); animation: px-rise .8s both; }
.px-path li:last-child { padding-bottom: 0; }
.px-path li::before { content:""; position:absolute; left: 6px; top: 9px; width: 9px; height: 9px; border-radius: 50%; background: var(--forest); border: 1px solid var(--mist); }
.px-path li::after { content:""; position:absolute; left: 10px; top: 22px; bottom: -4px; width: 1px; background: linear-gradient(180deg, var(--steel), rgba(137,155,154,.15)); transform-origin: top; animation: px-down .8s both; }
.px-path li:last-child::after { display: none; }
.px-path li:last-child::before { background: var(--mist); box-shadow: 0 0 12px var(--mist); }
.px-path.idle li { color: var(--sage); }
.px-path.idle li::before { border-color: rgba(212,215,211,.4); }

/* Empty state */
.px-empty { padding: 2rem 1rem; text-align: center; animation: px-rise .9s both; }
.px-empty-ring { position: relative; width: 64px; height: 64px; margin: 0 auto 1.2rem; border-radius: 50%; border: 1px dashed rgba(212,215,211,.5); animation: px-spin 24s linear infinite; }
.px-empty-ring::before { content:""; position:absolute; inset: 14px; border-radius: 50%; border: 1px solid rgba(137,155,154,.7); }
.px-empty-ring::after { content:""; position:absolute; top:-4px; left:50%; width:8px; height:8px; margin-left:-4px; border-radius:50%; background: var(--mist); box-shadow: 0 0 14px var(--mist); }
.px-empty h3 { margin: 0 0 .4rem; padding: 0; font-size: 1.25rem; font-weight: 300; letter-spacing: .06em; color: var(--mist); }
.px-empty p { margin: 0 auto; max-width: 26rem; font-size: .9rem; color: var(--sage); }

/* Widgets: every state keeps light text on a dark surface */
[data-testid="stWidgetLabel"] p { font-size: .72rem; font-weight: 600; letter-spacing: .22em; text-transform: uppercase; color: var(--sage); }
[data-baseweb="textarea"], [data-baseweb="base-input"] { background: var(--field) !important; border-radius: 14px !important; border: 1px solid rgba(212,215,211,.28) !important; transition: border-color .3s, box-shadow .3s; }
[data-baseweb="textarea"]:focus-within, [data-baseweb="base-input"]:focus-within { border-color: var(--mist) !important; box-shadow: 0 0 0 1px var(--mist); }
.stTextArea textarea, .stTextInput input { background: transparent !important; color: var(--mist) !important; -webkit-text-fill-color: var(--mist); caret-color: var(--mist); font-size: .98rem; line-height: 1.7; }
.stTextArea textarea::placeholder, .stTextInput input::placeholder { color: var(--sage); -webkit-text-fill-color: var(--sage); opacity: 1; }
[data-baseweb="select"] > div { background: var(--field); border: 1px solid rgba(212,215,211,.28); border-radius: 14px; color: var(--mist); transition: border-color .3s, background .3s; }
[data-baseweb="select"] > div:hover { border-color: var(--mist); background: var(--forest-hover); }
[data-baseweb="select"] span, [data-baseweb="select"] div { color: var(--mist); }
[data-baseweb="select"] svg { fill: var(--mist); color: var(--mist); }
[data-baseweb="popover"] > div, [data-baseweb="menu"], [data-baseweb="popover"] ul { background: #263A36 !important; border: 1px solid rgba(212,215,211,.25); border-radius: 14px; }
[data-baseweb="menu"] li, [data-baseweb="popover"] li { background: transparent; color: var(--mist); }
[data-baseweb="menu"] li:hover, [data-baseweb="popover"] li:hover, [data-baseweb="menu"] li[aria-selected="true"] { background: rgba(86,105,112,.6) !important; color: var(--mist); }
[data-baseweb="menu"] li *, [data-baseweb="popover"] li * { color: var(--mist); }

[data-testid="stForm"] { padding: 1.6rem; border-radius: 22px; border: 1px solid var(--line); background: linear-gradient(160deg, rgba(64,86,83,.85), rgba(44,66,63,.85)); box-shadow: 0 14px 34px rgba(0,0,0,.2); }
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]) { border-radius: 22px; }
div[data-testid="stVerticalBlockBorderWrapper"][class*="st-emotion-cache"] { border-color: var(--line); }
[data-testid="stAlert"] { background: rgba(70,86,93,.38); border: 1px solid rgba(212,215,211,.28); border-radius: 16px; color: var(--mist); }
[data-testid="stAlert"] p, [data-testid="stAlert"] div, [data-testid="stAlert"] svg { color: var(--mist); fill: var(--mist); }
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p { color: var(--sage); }
[data-testid="stSpinner"] p, .stSpinner p { color: var(--sage); }
[data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 18px; overflow: hidden; }

.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button { border-radius: 999px; padding: .65rem 1.5rem; font-weight: 400; letter-spacing: .08em; border: 1px solid rgba(212,215,211,.4); background: transparent; color: var(--mist); transition: transform .3s var(--ease), box-shadow .3s, background .3s, color .3s, border-color .3s; }
.stButton > button p, .stFormSubmitButton > button p, .stDownloadButton > button p, .stButton > button span { color: inherit; }
.stButton > button:hover, .stFormSubmitButton > button:hover, .stDownloadButton > button:hover { transform: translateY(-3px); border-color: var(--mist); background: var(--forest-hover); color: var(--mist); box-shadow: 0 10px 26px rgba(0,0,0,.28); }
.stButton > button:active, .stFormSubmitButton > button:active, .stDownloadButton > button:active { transform: translateY(-1px) scale(.98); background: var(--slate-hover); color: var(--mist); }
.stButton > button:focus-visible, .stFormSubmitButton > button:focus-visible, .stDownloadButton > button:focus-visible { outline: 2px solid var(--focus-ring); outline-offset: 3px; color: var(--mist); }
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primaryFormSubmit"] { background: var(--mist); color: var(--forest); border-color: var(--mist); font-weight: 600; }
.stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primaryFormSubmit"]:hover { background: var(--mist-hover); border-color: var(--mist-hover); color: var(--forest); }
.stButton > button[kind="primary"]:active, .stFormSubmitButton > button[kind="primaryFormSubmit"]:active { background: var(--steel); border-color: var(--steel); color: var(--forest); }
.stButton > button[kind="primary"]:focus-visible, .stFormSubmitButton > button[kind="primaryFormSubmit"]:focus-visible { background: var(--mist-hover); color: var(--forest); }

@media (max-width: 760px) { .px-hero { padding: 2.2rem 1.4rem; } }
@media (prefers-reduced-motion: reduce) {
    .px-hero *, .px-kicker i, .px-tile, .px-tile::before, .px-info, .px-path li, .px-path li::after,
    .px-empty, .px-empty-ring, .px-label::after, .px-orb { animation: none !important; transition: none !important; }
}
</style>
"""


def html(markup: str) -> str:
    """Strip indentation and blank lines so Markdown never treats the HTML as code."""
    return "\n".join(line.strip() for line in markup.strip().splitlines() if line.strip())


def inject() -> None:
    """Inject the shared page stylesheet."""
    st.markdown(html(PAGE_BASE_CSS), unsafe_allow_html=True)


def hero(kicker: str, title: str, lead: str, note: str = "") -> None:
    """Render the page hero."""
    note_markup = f'<p class="px-note">{escape(note)}</p>' if note else ""
    st.markdown(
        html(
            f"""
            <div class="px-hero">
                <div class="px-orb"></div>
                <div class="px-kicker"><i></i>{escape(kicker)}</div>
                <h1 class="px-title">{escape(title)}</h1>
                <p class="px-lead">{escape(lead)}</p>
                {note_markup}
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


def label(text: str, sub: str = "", index: str = "") -> None:
    """Render a section label with an optional index and sub line."""
    prefix = f"<em>{escape(index)}</em>" if index else ""
    st.markdown(f'<div class="px-label">{prefix}{escape(text)}</div>', unsafe_allow_html=True)
    if sub:
        st.markdown(f'<div class="px-sub">{escape(sub)}</div>', unsafe_allow_html=True)


def info_card(heading: str, body: str) -> str:
    """Return markup for a small information card."""
    return f'<div class="px-info"><small>{escape(heading)}</small><p>{escape(body)}</p></div>'


def tile(index: int, heading: str, value: str, note: str) -> str:
    """Return markup for one metric tile."""
    return (
        f'<div class="px-tile" style="animation-delay:{0.1 + index * 0.1:.2f}s">'
        f"<small>{escape(heading)}</small><b>{escape(value)}</b><span>{escape(note)}</span></div>"
    )


def tiles(items) -> str:
    """Return markup for a responsive grid of metric tiles."""
    return '<div class="px-tiles">' + "".join(tile(i, *item) for i, item in enumerate(items)) + "</div>"


def pill(text: str) -> str:
    """Return markup for a small pill."""
    return f'<span class="px-pill">{escape(text)}</span>'


def path(stages, idle: bool = False) -> str:
    """Return markup for a vertical routing path."""
    items = "".join(
        f'<li style="animation-delay:{0.08 + i * 0.12:.2f}s">{escape(str(stage))}</li>'
        for i, stage in enumerate(stages)
    )
    return f'<ul class="px-path{" idle" if idle else ""}">{items}</ul>'


def empty(title: str, text: str) -> str:
    """Return markup for an empty state."""
    return (
        '<div class="px-empty"><div class="px-empty-ring" aria-hidden="true"></div>'
        f"<h3>{escape(title)}</h3><p>{escape(text)}</p></div>"
    )
