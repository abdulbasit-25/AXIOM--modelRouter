"""About page."""

from html import escape

import streamlit as st

from app.components import page_footer
from app.config import BRAND_EXPANSION, BRAND_NAME, BRAND_TAGLINE

EVENT = "AICON'26"
EVENT_LONG = "Build with AI Hackathon"

_CSS = """
<style>
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

@keyframes ab-rise { from {opacity:0; transform: translateY(26px); filter: blur(6px);} to {opacity:1; transform:none; filter:none;} }
@keyframes ab-spin { to {transform: rotate(360deg);} }
@keyframes ab-float { 0%,100% {transform: translate(0,0);} 50% {transform: translate(30px,-24px);} }
@keyframes ab-shine { to {background-position: 220% 0;} }
@keyframes ab-line { from {transform: scaleX(0);} to {transform: scaleX(1);} }
@keyframes ab-caret { 0%,100% {opacity:1;} 50% {opacity:0;} }

/* Hero */
.ab-hero { position: relative; overflow: hidden; border-radius: 28px; padding: 3.2rem 3rem 3rem; border: 1px solid rgba(212,215,211,.26); background: linear-gradient(145deg, #405653, #2C423F); box-shadow: 0 30px 70px rgba(0,0,0,.35), inset 0 1px 0 rgba(212,215,211,.2); }
.ab-hero::before { content:""; position:absolute; inset:0; background-image: linear-gradient(rgba(212,215,211,.07) 1px, transparent 1px), linear-gradient(90deg, rgba(212,215,211,.07) 1px, transparent 1px); background-size: 56px 56px; -webkit-mask-image: radial-gradient(ellipse at 80% 30%, #000 15%, transparent 70%); mask-image: radial-gradient(ellipse at 80% 30%, #000 15%, transparent 70%); }
.ab-orb { position:absolute; right:-70px; top:-90px; width:320px; height:320px; border-radius:50%; background: var(--steel); filter: blur(70px); opacity:.42; animation: ab-float 14s ease-in-out infinite; }
.ab-kicker { position: relative; font-size: .74rem; font-weight: 600; letter-spacing: .34em; text-transform: uppercase; color: var(--sage); animation: ab-rise .9s both; }
.ab-title { position: relative; margin: .9rem 0 .2rem; font-size: clamp(2.6rem, 7vw, 5rem); font-weight: 200; letter-spacing: .1em; line-height: 1.05; text-transform: uppercase;
    background: linear-gradient(100deg, #D4D7D3 20%, #E5E7E3 40%, #D4D7D3 60%, #E5E7E3 80%); background-size: 220% 100%; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; color: transparent; animation: ab-rise 1s .1s both, ab-shine 7s linear infinite; }
.stMarkdown h1.ab-title { color: transparent !important; -webkit-text-fill-color: transparent !important; padding: 0; }
.ab-exp { position: relative; display: flex; align-items: center; gap: 1.1rem; margin: .5rem 0 1.4rem; animation: ab-rise .9s .2s both; }
.ab-exp::before { content:""; flex: none; width: 64px; height: 1px; background: linear-gradient(90deg, var(--mist), rgba(212,215,211,.2)); transform-origin: left; animation: ab-line 1.3s .5s both; }
.stMarkdown .ab-exp span { font-size: clamp(.76rem, 1.2vw, .95rem); letter-spacing: .32em; line-height: 1.8; text-transform: uppercase; color: var(--sage) !important; }
.ab-exp span::after { content:""; display:inline-block; width:7px; height:1em; margin-left:.7rem; vertical-align:-.15em; background: var(--mist); animation: ab-caret 1.1s steps(1) infinite; }
.stMarkdown p.ab-lead { position: relative; max-width: 34rem; margin: 0; font-size: 1.1rem; font-weight: 400; line-height: 1.8; color: var(--mist) !important; animation: ab-rise 1s .3s both; }

/* Labels */
.ab-label { margin: 3.4rem 0 1.3rem; display: flex; align-items: center; gap: 1rem; font-size: .75rem; font-weight: 600; letter-spacing: .3em; text-transform: uppercase; color: var(--steel); }
.ab-label::after { content:""; flex:1; height:1px; background: linear-gradient(90deg, rgba(137,155,154,.55), transparent); transform-origin: left; animation: ab-line 1.4s .2s both; }

/* Capabilities */
.ab-pills { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1rem; }
.ab-pill { padding: 1.25rem 1.3rem; border-radius: 18px; border: 1px solid rgba(212,215,211,.22); background: linear-gradient(150deg, #405653, #2C423F); box-shadow: 0 12px 28px rgba(0,0,0,.18); animation: ab-rise .9s both; transition: transform .45s var(--ease), border-color .45s, box-shadow .45s; }
.ab-pill:hover { transform: translateY(-6px); border-color: rgba(212,215,211,.45); box-shadow: 0 20px 40px rgba(0,0,0,.28); }
.ab-pill small { display:block; font-size:.7rem; letter-spacing:.24em; color: var(--sage); margin-bottom:.6rem; }
.ab-pill span { font-size: 1.12rem; font-weight: 300; color: var(--mist); }

/* Team */
.ab-team { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.2rem; }
.ab-member { position: relative; overflow: hidden; border-radius: 26px; padding: 2.4rem 1.6rem 2rem; text-align: center; border: 1px solid rgba(212,215,211,.22); background: linear-gradient(170deg, #405653, #2C423F); box-shadow: 0 14px 34px rgba(0,0,0,.2);
    animation: ab-rise .95s both; transition: transform .55s var(--ease), border-color .5s, box-shadow .5s; }
.ab-member:nth-child(1) { animation-delay: .1s; } .ab-member:nth-child(2) { animation-delay: .25s; } .ab-member:nth-child(3) { animation-delay: .4s; }
.ab-member:hover { transform: translateY(-10px); border-color: rgba(212,215,211,.45); box-shadow: 0 28px 56px rgba(0,0,0,.32); }
.ab-member::before { content:""; position:absolute; left:50%; top: 4.4rem; width: 360px; height: 360px; margin: -180px 0 0 -180px; border-radius:50%; background: radial-gradient(circle, rgba(212,215,211,.22), transparent 62%); opacity:0; transition: opacity .6s; }
.ab-member:hover::before { opacity:1; }
.ab-idx { position:absolute; top:1rem; left:1.3rem; font-size:.7rem; letter-spacing:.24em; color: var(--sage); }
.ab-avatar { position: relative; width: 112px; height: 112px; margin: 0 auto 1.5rem; display:flex; align-items:center; justify-content:center; }
.ab-avatar::before { content:""; position:absolute; inset:0; border-radius:50%; border:1px dashed rgba(212,215,211,.45); animation: ab-spin 26s linear infinite; }
.ab-avatar::after { content:""; position:absolute; top:-4px; left:50%; width:8px; height:8px; margin-left:-4px; border-radius:50%; background: var(--mist); box-shadow: 0 0 14px var(--mist); transform-origin: 4px 60px; animation: ab-spin 9s linear infinite; }
.ab-core { width: 84px; height: 84px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size: 1.6rem; font-weight: 300; letter-spacing:.08em; color: var(--mist); background: radial-gradient(circle at 30% 25%, rgba(137,155,154,.55), rgba(38,58,54,.95)); border: 1px solid rgba(212,215,211,.4); transition: background .5s, color .5s, transform .5s var(--ease); }
.ab-member:hover .ab-core { background: var(--mist); color: var(--forest); transform: scale(1.06); }
.stMarkdown h3.ab-name { position: relative; margin: 0; padding: 0; font-size: 1.3rem; font-weight: 400; color: var(--mist) !important; }
.ab-roles { position: relative; display:flex; flex-wrap:wrap; justify-content:center; gap:.45rem; margin-top: 1rem; }
.ab-role { padding: .28rem .8rem; border-radius: 999px; font-size: .68rem; font-weight: 600; letter-spacing: .2em; text-transform: uppercase; color: var(--sage); border: 1px solid rgba(212,215,211,.4); transition: color .4s, border-color .4s, background .4s; }
.ab-member:hover .ab-role { color: var(--mist); border-color: rgba(212,215,211,.7); background: rgba(38,58,54,.55); }

/* Flow */
.ab-flow { position: relative; display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; }
.ab-flow::before { content:""; position:absolute; left: 0; right: 0; top: 17px; height:1px; background: linear-gradient(90deg, var(--steel), rgba(137,155,154,.12)); transform-origin: left; animation: ab-line 1.6s .3s both; }
.ab-node { position: relative; padding-top: 3rem; animation: ab-rise .9s both; }
.ab-node:nth-child(1){animation-delay:.1s}.ab-node:nth-child(2){animation-delay:.2s}.ab-node:nth-child(3){animation-delay:.3s}.ab-node:nth-child(4){animation-delay:.4s}.ab-node:nth-child(5){animation-delay:.5s}
.ab-dot { position:absolute; top:6px; left:0; width:24px; height:24px; border-radius:50%; background: var(--forest); border: 1px solid var(--mist); display:flex; align-items:center; justify-content:center; font-size:.62rem; letter-spacing:.05em; color: var(--mist); transition: background .4s, color .4s, transform .4s var(--ease); }
.ab-node:hover .ab-dot { background: var(--mist); color: var(--forest); transform: scale(1.25); }
.stMarkdown .ab-node h4 { margin: 0 0 .3rem; padding: 0; font-size: 1.12rem; font-weight: 400; color: var(--mist) !important; }
.ab-node p { margin: 0; font-size: .86rem; color: var(--sage); }

/* Event */
.ab-event { position: relative; margin-top: 3.4rem; padding: 2.6rem 2rem; text-align: center; border-radius: 26px; border: 1px solid rgba(212,215,211,.24); background: linear-gradient(180deg, #405653, #2C423F); box-shadow: 0 20px 50px rgba(0,0,0,.25); }
.ab-event b { display:block; font-size: clamp(2rem, 5vw, 3.4rem); font-weight: 200; letter-spacing: .12em; color: var(--mist); }
.ab-event span { font-size: .8rem; font-weight: 600; letter-spacing: .4em; text-transform: uppercase; color: var(--sage); }

@media (max-width: 820px) {
    .ab-flow { grid-template-columns: 1fr; }
    .ab-flow::before { display: none; }
    .ab-hero { padding: 2.2rem 1.4rem; }
    .ab-exp::before { width: 28px; }
    .stMarkdown .ab-exp span { letter-spacing: .2em; }
}
@media (prefers-reduced-motion: reduce) {
    .ab-hero *, .ab-exp, .ab-exp::before, .ab-exp span::after, .ab-pill, .ab-member, .ab-node, .ab-flow::before,
    .ab-label::after, .ab-avatar::before, .ab-avatar::after, .ab-orb { animation: none !important; transition: none !important; }
}
</style>
"""

TEAM = (
    ("Muhammad Arslan Jaffer", ("Backend",), "MJ"),
    ("Abdul Basit", ("Frontend",), "AB"),
    ("Fatima Asim", ("Classifier", "Testing"), "FA"),
)

CAPABILITIES = (
    "Rule-based classifier",
    "Tiered Groq routing",
    "Heuristic verification",
    "Session cost telemetry",
)

FLOW = (
    ("Classify", "Rule-based complexity tier."),
    ("Select", "Tier mapped to a Groq model."),
    ("Generate", "Live response, or a labeled local mock."),
    ("Verify", "Heuristic checks, escalate on failure."),
    ("Review", "Tokens and estimated cost per session."),
)


def _html(markup: str) -> str:
    """Strip indentation and blank lines so Markdown never treats the HTML as code."""
    return "\n".join(line.strip() for line in markup.strip().splitlines() if line.strip())


def _label(text: str) -> None:
    st.markdown(f'<div class="ab-label">{escape(text)}</div>', unsafe_allow_html=True)


def render() -> None:
    st.markdown(_html(_CSS), unsafe_allow_html=True)

    st.markdown(
        _html(
            f"""
            <div class="ab-hero">
                <div class="ab-orb"></div>
                <div class="ab-kicker">About</div>
                <h1 class="ab-title">{escape(BRAND_NAME)}</h1>
                <div class="ab-exp"><span>{escape(BRAND_EXPANSION)}</span></div>
                <p class="ab-lead">{escape(BRAND_TAGLINE)}</p>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    _label("Inside the engine")
    pills = "".join(
        f'<div class="ab-pill" style="animation-delay:{0.1 + i * 0.12:.2f}s">'
        f"<small>{i + 1:02d}</small><span>{escape(text)}</span></div>"
        for i, text in enumerate(CAPABILITIES)
    )
    st.markdown(f'<div class="ab-pills">{pills}</div>', unsafe_allow_html=True)

    _label("The team")
    members = "".join(
        _html(
            f"""
            <article class="ab-member">
                <div class="ab-idx">{i + 1:02d}</div>
                <div class="ab-avatar" aria-hidden="true"><div class="ab-core">{escape(initials)}</div></div>
                <h3 class="ab-name">{escape(name)}</h3>
                <div class="ab-roles">{"".join(f'<span class="ab-role">{escape(r)}</span>' for r in roles)}</div>
            </article>
            """
        )
        for i, (name, roles, initials) in enumerate(TEAM)
    )
    st.markdown(f'<div class="ab-team">{members}</div>', unsafe_allow_html=True)

    _label("How it flows")
    nodes = "".join(
        f'<div class="ab-node"><div class="ab-dot">{i + 1}</div>'
        f"<h4>{escape(title)}</h4><p>{escape(text)}</p></div>"
        for i, (title, text) in enumerate(FLOW)
    )
    st.markdown(f'<div class="ab-flow">{nodes}</div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="ab-event"><b>{EVENT}</b><span>{EVENT_LONG}</span></div>',
        unsafe_allow_html=True,
    )

    st.write("")
    page_footer()