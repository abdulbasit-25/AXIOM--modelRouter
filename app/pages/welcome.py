"""Welcome page."""

from html import escape

import streamlit as st

from app.components import page_footer
from app.config import BRAND_EXPANSION, BRAND_NAME, BRAND_TAGLINE, BRAND_WORDMARK
from app.navigation.router import set_destination

EVENT = "AICON'26"
EVENT_LONG = "Build with AI Hackathon"

_CSS = """
<style>
:root {
  /* Text and light surfaces */
  --mist: #D4D7D3;
  --mist-hover: #E5E7E3;
  /* Muted accents */
  --sage: #A3ADA5;
  --steel: #899B9A;
  /* Structure */
  --slate: #46565D;
  --forest: #263A36;
  /* Interaction */
  --slate-hover: #566970;
  --forest-hover: #344B45;
  --border: rgba(212,215,211,.2);
  --focus-ring: #A3ADA5;
  --ease: cubic-bezier(.2,.8,.2,1);
}

.stApp { background: radial-gradient(1200px 700px at 80% -10%, rgba(137,155,154,.2), transparent 60%), radial-gradient(900px 600px at -10% 40%, rgba(70,86,93,.35), transparent 60%), var(--forest); color: var(--mist); }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1120px; padding-top: 2rem; }

@keyframes ax-rise { from {opacity:0; transform: translateY(28px); filter: blur(6px);} to {opacity:1; transform: none; filter: none;} }
@keyframes ax-float-a { 0%,100% {transform: translate(0,0) scale(1);} 50% {transform: translate(40px,-30px) scale(1.12);} }
@keyframes ax-float-b { 0%,100% {transform: translate(0,0) scale(1);} 50% {transform: translate(-50px,35px) scale(.92);} }
@keyframes ax-spin { to {transform: rotate(360deg);} }
@keyframes ax-marquee { to {transform: translateX(-50%);} }
@keyframes ax-shine { to {background-position: 220% 0;} }
@keyframes ax-blink { 0%,100% {opacity:1;} 50% {opacity:.25;} }
@keyframes ax-line { from {transform: scaleX(0);} to {transform: scaleX(1);} }
@keyframes ax-caret { 0%,100% {opacity:1;} 50% {opacity:0;} }

/* Hero */
.ax-hero { position: relative; min-height: 480px; border-radius: 28px; padding: 3.2rem 3rem; overflow: hidden; display: flex; flex-direction: column; justify-content: center;
    border: 1px solid rgba(212,215,211,.26); background: linear-gradient(145deg, #405653, #2C423F); box-shadow: 0 30px 70px rgba(0,0,0,.35), inset 0 1px 0 rgba(212,215,211,.2); }
.ax-grid { position: absolute; inset: 0; background-image: linear-gradient(rgba(212,215,211,.07) 1px, transparent 1px), linear-gradient(90deg, rgba(212,215,211,.07) 1px, transparent 1px); background-size: 56px 56px; -webkit-mask-image: radial-gradient(ellipse at 70% 40%, #000 20%, transparent 72%); mask-image: radial-gradient(ellipse at 70% 40%, #000 20%, transparent 72%); }
.ax-orb { position: absolute; border-radius: 50%; filter: blur(64px); opacity: .45; }
.ax-orb.a { width: 340px; height: 340px; right: -60px; top: -80px; background: var(--steel); animation: ax-float-a 14s ease-in-out infinite; }
.ax-orb.b { width: 280px; height: 280px; right: 22%; bottom: -120px; background: var(--slate); animation: ax-float-b 18s ease-in-out infinite; }
.ax-ring { position: absolute; right: 7%; top: 50%; width: 260px; height: 260px; margin-top: -130px; border-radius: 50%; border: 1px dashed rgba(212,215,211,.5); animation: ax-spin 40s linear infinite; }
.ax-ring::before { content:""; position:absolute; inset: 34px; border-radius: 50%; border: 1px solid rgba(137,155,154,.6); animation: ax-spin 24s linear infinite reverse; }
.ax-ring::after { content:""; position:absolute; top:-5px; left:50%; width:10px; height:10px; border-radius:50%; background: var(--mist); box-shadow: 0 0 18px var(--mist); }
.ax-badge { position: relative; align-self: flex-start; display: inline-flex; align-items: center; gap: .6rem; padding: .42rem 1rem; border-radius: 999px; font-size: .74rem; letter-spacing: .16em; text-transform: uppercase; color: var(--mist);
    border: 1px solid rgba(212,215,211,.45); background: rgba(24,38,35,.7); box-shadow: 0 8px 24px rgba(0,0,0,.25); animation: ax-rise .9s .05s both; }
.ax-badge i { width: 7px; height: 7px; border-radius: 50%; background: var(--mist); animation: ax-blink 1.6s infinite; }

/* Wordmark */
.ax-word { position: relative; margin: 1.4rem 0 .1rem; font-size: clamp(3.4rem, 9vw, 7rem); font-weight: 200; letter-spacing: .14em; line-height: 1; text-transform: uppercase;
    background: linear-gradient(100deg, #D4D7D3 20%, #E5E7E3 40%, #D4D7D3 60%, #E5E7E3 80%); background-size: 220% 100%; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; color: transparent; animation: ax-rise 1s .15s both, ax-shine 7s linear infinite; }
.stMarkdown h1.ax-word { color: transparent !important; -webkit-text-fill-color: transparent !important; padding: 0; }

/* Expansion: the full name, set as a quiet signature line */
.ax-exp { position: relative; display: flex; align-items: center; gap: 1.1rem; margin: .5rem 0 1.6rem; animation: ax-rise .9s .25s both; }
.ax-exp::before { content: ""; flex: none; width: 64px; height: 1px; background: linear-gradient(90deg, var(--mist), rgba(212,215,211,.2)); transform-origin: left; animation: ax-line 1.3s .6s both; }
.ax-exp span { font-size: clamp(.78rem, 1.2vw, .98rem); font-weight: 400; letter-spacing: .34em; line-height: 1.8; text-transform: uppercase; color: var(--sage); }
.ax-exp span::after { content: ""; display: inline-block; width: 7px; height: 1em; margin-left: .7rem; vertical-align: -.15em; background: var(--mist); animation: ax-caret 1.1s steps(1) infinite; }
.stMarkdown .ax-exp span { color: var(--sage) !important; }

.stMarkdown p.ax-tag { position: relative; margin: 0; max-width: 34rem; font-size: clamp(1.05rem, 1.4vw, 1.2rem); font-weight: 400; line-height: 1.85; letter-spacing: .012em; color: var(--mist) !important; text-wrap: pretty; -webkit-font-smoothing: antialiased; animation: ax-rise .85s .35s both; }

/* Marquee */
.ax-marquee { overflow: hidden; margin: 1.6rem 0 .6rem; border-top: 1px solid rgba(212,215,211,.14); border-bottom: 1px solid rgba(212,215,211,.14); padding: .9rem 0; -webkit-mask-image: linear-gradient(90deg, transparent, #000 12%, #000 88%, transparent); mask-image: linear-gradient(90deg, transparent, #000 12%, #000 88%, transparent); }
.ax-track { display: flex; width: max-content; gap: 3rem; animation: ax-marquee 28s linear infinite; }
.ax-track span { font-size: .85rem; letter-spacing: .32em; text-transform: uppercase; color: var(--steel); white-space: nowrap; }
.ax-track span::after { content: "/"; margin-left: 3rem; color: var(--slate-hover); }

/* Labels */
.ax-label { margin: 3.2rem 0 1.2rem; display: flex; align-items: center; gap: 1rem; font-size: .75rem; font-weight: 600; letter-spacing: .3em; text-transform: uppercase; color: var(--steel); }
.ax-label::after { content:""; flex: 1; height: 1px; background: linear-gradient(90deg, rgba(137,155,154,.55), transparent); transform-origin: left; animation: ax-line 1.4s .2s both; }

/* Flow */
.ax-steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; }
.ax-step { position: relative; padding: 1.4rem 1.2rem 1.6rem 0; border-top: 1px solid rgba(212,215,211,.2); animation: ax-rise .9s both; }
.ax-step:nth-child(1) { animation-delay: .1s; } .ax-step:nth-child(2) { animation-delay: .22s; } .ax-step:nth-child(3) { animation-delay: .34s; } .ax-step:nth-child(4) { animation-delay: .46s; }
.ax-step::before { content:""; position:absolute; top:-1px; left:0; width:0; height:1px; background: var(--mist); transition: width .6s ease; }
.ax-step:hover::before { width: 100%; }
.ax-step b { display:block; font-size: .8rem; font-weight: 600; letter-spacing: .2em; color: var(--steel); margin-bottom: .8rem; }
.ax-step h4 { margin: 0; font-size: 1.5rem; font-weight: 300; color: var(--sage) !important; transition: transform .4s var(--ease), letter-spacing .4s var(--ease), color .4s; }
.ax-step:hover h4 { transform: translateX(8px); letter-spacing: .04em; color: var(--mist) !important; }

/* Workspace cards */
.ax-card { position: relative; border-radius: 22px; padding: 1.8rem 1.6rem 1.5rem; min-height: 190px; overflow: hidden; border: 1px solid rgba(212,215,211,.22); background: linear-gradient(160deg, #405653, #2C423F); box-shadow: 0 14px 34px rgba(0,0,0,.2); transition: transform .5s var(--ease), border-color .5s, box-shadow .5s; animation: ax-rise .9s both; }
.ax-card::before { content:""; position:absolute; width: 220px; height: 220px; right:-90px; top:-90px; border-radius:50%; background: radial-gradient(circle, rgba(212,215,211,.35), transparent 70%); opacity:0; transition: opacity .5s; }
.ax-card:hover { transform: translateY(-8px); border-color: rgba(212,215,211,.45); box-shadow: 0 24px 50px rgba(0,0,0,.3); }
.ax-card:hover::before { opacity: 1; }
.ax-card small { color: var(--sage); letter-spacing: .24em; font-size: .72rem; }
.stMarkdown .ax-card h3 { margin: 2.6rem 0 .3rem; font-size: 1.5rem; font-weight: 300; color: var(--mist) !important; padding: 0; }
.ax-card p { margin: 0; color: var(--mist); font-size: .95rem; }

/* Event */
.ax-event { position: relative; margin-top: 3.4rem; padding: 3rem 2rem; text-align: center; border-radius: 28px; overflow: hidden; border: 1px solid rgba(212,215,211,.22); background: #2C423F; }
.ax-event::before { content:""; position:absolute; left:50%; top:50%; width: 620px; height: 620px; margin: -310px 0 0 -310px; border-radius:50%; background: conic-gradient(from 0deg, transparent 0 70%, rgba(212,215,211,.3) 85%, transparent 100%); animation: ax-spin 12s linear infinite; }
.ax-event::after { content:""; position:absolute; inset: 1px; border-radius: 27px; background: linear-gradient(180deg, #34504c, #2C423F); opacity: .94; }
.ax-event > * { position: relative; z-index: 1; }
.ax-event .big { font-size: clamp(2.4rem, 6vw, 4.4rem); font-weight: 200; letter-spacing: .12em; color: var(--mist); margin: 0; }
.ax-event .sub { margin: .5rem 0 0; font-size: .85rem; font-weight: 600; letter-spacing: .42em; text-transform: uppercase; color: var(--sage); }

/* Buttons: every state sets background AND text together */
.stButton > button { border-radius: 999px; padding: .65rem 1.4rem; font-weight: 400; letter-spacing: .08em; border: 1px solid rgba(212,215,211,.4); background: transparent; color: var(--mist); transition: transform .3s var(--ease), box-shadow .3s, background .3s, color .3s, border-color .3s; }
.stButton > button p, .stButton > button span { color: inherit; }
.stButton > button:hover { transform: translateY(-3px); border-color: var(--mist); background: var(--forest-hover); color: var(--mist); box-shadow: 0 10px 26px rgba(0,0,0,.28); }
.stButton > button:active { transform: translateY(-1px) scale(.98); background: var(--slate-hover); color: var(--mist); }
.stButton > button:focus-visible { outline: 2px solid var(--focus-ring); outline-offset: 3px; color: var(--mist); }
.stButton > button[kind="primary"] { background: var(--mist); color: var(--forest); border-color: var(--mist); font-weight: 600; }
.stButton > button[kind="primary"]:hover { background: var(--mist-hover); border-color: var(--mist-hover); color: var(--forest); }
.stButton > button[kind="primary"]:active { background: var(--steel); border-color: var(--steel); color: var(--forest); }
.stButton > button[kind="primary"]:focus-visible { background: var(--mist-hover); color: var(--forest); }

@media (max-width: 760px) {
    .ax-steps { grid-template-columns: 1fr 1fr; }
    .ax-hero { padding: 2.2rem 1.5rem; }
    .ax-ring { display: none; }
    .ax-exp::before { width: 28px; }
    .ax-exp span { letter-spacing: .2em; }
}
@media (prefers-reduced-motion: reduce) {
    .ax-hero *, .ax-exp, .ax-exp::before, .ax-exp span::after, .ax-card, .ax-step, .ax-track,
    .ax-event::before, .ax-label::after, .ax-word, .ax-badge i { animation: none !important; transition: none !important; }
}
</style>
"""


def _html(markup: str) -> str:
    """Strip indentation and blank lines so Markdown never turns the HTML into a code block."""
    return "\n".join(line.strip() for line in markup.strip().splitlines() if line.strip())


def render() -> None:
    st.markdown(_html(_CSS), unsafe_allow_html=True)

    # Hero
    st.markdown(
        _html(
            f"""
            <div class="ax-hero">
                <div class="ax-grid"></div>
                <div class="ax-orb a"></div>
                <div class="ax-orb b"></div>
                <div class="ax-ring"></div>
                <div class="ax-badge"><i></i>{EVENT} &nbsp;/&nbsp; {EVENT_LONG}</div>
                <h1 class="ax-word">{escape(BRAND_WORDMARK)}</h1>
                <div class="ax-exp"><span>{escape(BRAND_EXPANSION)}</span></div>
                <p class="ax-tag">{escape(BRAND_TAGLINE)}</p>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    st.write("")
    cta_a, cta_b, _spacer = st.columns([1.1, 1, 2.2], gap="small")
    with cta_a:
        if st.button("Open the Tutor", type="primary", width="stretch", key="cta_tutor"):
            set_destination("Production AI Tutor")
    with cta_b:
        if st.button(f"About {BRAND_NAME}", width="stretch", key="cta_about"):
            set_destination("About")

    # Marquee
    words = ["Classify", "Route", "Verify", "Escalate", "Measure", "Learn"]
    items = "".join(f"<span>{w}</span>" for w in words * 2)
    st.markdown(
        f'<div class="ax-marquee"><div class="ax-track">{items}{items}</div></div>',
        unsafe_allow_html=True,
    )

    # Flow
    st.markdown('<div class="ax-label">The flow</div>', unsafe_allow_html=True)
    st.markdown(
        _html(
            """
            <div class="ax-steps">
                <div class="ax-step"><b>01</b><h4>Classify</h4></div>
                <div class="ax-step"><b>02</b><h4>Route</h4></div>
                <div class="ax-step"><b>03</b><h4>Verify</h4></div>
                <div class="ax-step"><b>04</b><h4>Escalate</h4></div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    # Workspaces
    st.markdown('<div class="ax-label">Workspaces</div>', unsafe_allow_html=True)
    spaces = (
        ("01", "Production AI Tutor", "Ask. Route. Verify."),
        ("02", "Calibration Studio", "Tune the router."),
        ("03", "SDG Analytics", "Measure the impact."),
    )
    for column, (num, name, line) in zip(st.columns(3, gap="medium"), spaces):
        with column:
            st.markdown(
                f'<div class="ax-card"><small>{num}</small><h3>{name}</h3><p>{line}</p></div>',
                unsafe_allow_html=True,
            )
            st.write("")
            if st.button("Enter", key=f"feature_{name}", width="stretch"):
                set_destination(name)

    # Event
    st.markdown(
        _html(
            f"""
            <div class="ax-event">
                <p class="big">{EVENT}</p>
                <p class="sub">{EVENT_LONG}</p>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    st.write("")
    page_footer()