"""About page."""

from html import escape

import streamlit as st

from app.components import page_footer
from app.config import BRAND_DESCRIPTION, BRAND_EXPANSION, BRAND_NAME, BRAND_TAGLINE

EVENT = "AICON'26"
EVENT_LONG = "Build with AI Hackathon"

# Palette: C5C5C5  949B96  4C5B61  2C423F  829191
_CSS = """
<style>
:root { --mist:#C5C5C5; --sage:#949B96; --slate:#4C5B61; --forest:#2C423F; --steel:#829191; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1120px; padding-top: 2rem; }
@keyframes ab-rise { from {opacity:0; transform: translateY(26px); filter: blur(6px);} to {opacity:1; transform:none; filter:none;} }
@keyframes ab-spin { to {transform: rotate(360deg);} }
@keyframes ab-float { 0%,100% {transform: translate(0,0);} 50% {transform: translate(30px,-24px);} }
@keyframes ab-shine { to {background-position: 220% 0;} }
@keyframes ab-line { from {transform: scaleX(0);} to {transform: scaleX(1);} }
@keyframes ab-grow { from {transform: scaleY(0);} to {transform: scaleY(1);} }

.ab-hero { position: relative; overflow: hidden; border-radius: 28px; padding: 3rem 3rem 2.8rem; border: 1px solid rgba(197,197,197,.2); background: linear-gradient(145deg, #405653, #2C423F); }
.ab-hero::before { content:""; position:absolute; inset:0; background-image: linear-gradient(rgba(197,197,197,.06) 1px, transparent 1px), linear-gradient(90deg, rgba(197,197,197,.06) 1px, transparent 1px); background-size: 56px 56px; -webkit-mask-image: radial-gradient(ellipse at 80% 30%, #000 15%, transparent 70%); mask-image: radial-gradient(ellipse at 80% 30%, #000 15%, transparent 70%); }
.ab-orb { position:absolute; right:-70px; top:-90px; width:320px; height:320px; border-radius:50%; background: var(--steel); filter: blur(70px); opacity:.5; animation: ab-float 14s ease-in-out infinite; }
.ab-kicker { position: relative; font-size: .74rem; letter-spacing: .32em; text-transform: uppercase; color: var(--mist); animation: ab-rise .9s both; }
.ab-title { position: relative; margin: .9rem 0 .6rem; font-size: clamp(2.6rem, 7vw, 5rem); font-weight: 200; letter-spacing: .1em; line-height: 1.05; text-transform: uppercase;
    background: linear-gradient(100deg, #C5C5C5 20%, #FFFFFF 40%, #C5C5C5 60%, #FFFFFF 80%); background-size: 220% 100%; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; color: transparent; animation: ab-rise 1s .1s both, ab-shine 7s linear infinite; }
.stMarkdown h1.ab-title { color: transparent !important; -webkit-text-fill-color: transparent !important; }
.ab-lead { position: relative; max-width: 34rem; margin: 0; font-size: 1.1rem; font-weight: 400; color: var(--mist); animation: ab-rise 1s .25s both; }

.ab-label { margin: 3.4rem 0 1.3rem; display: flex; align-items: center; gap: 1rem; font-size: .75rem; font-weight: 700; letter-spacing: .3em; text-transform: uppercase; color: var(--slate); }
.ab-label::after { content:""; flex:1; height:1px; background: linear-gradient(90deg, rgba(130,145,145,.5), transparent); transform-origin: left; animation: ab-line 1.4s .2s both; }

.ab-pills { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1rem; }
.ab-pill { padding: 1.2rem 1.3rem; border-radius: 18px; border: 1px solid rgba(197,197,197,.2); background: linear-gradient(150deg, #405653, #2C423F); animation: ab-rise .9s both; transition: transform .45s cubic-bezier(.2,.8,.2,1), border-color .45s; }
.ab-pill:hover { transform: translateY(-6px); border-color: rgba(197,197,197,.4); }
.ab-pill small { display:block; font-size:.7rem; letter-spacing:.24em; color: var(--mist); margin-bottom:.5rem; }
.ab-pill span { font-size: 1.12rem; font-weight: 300; color: var(--mist); }

.ab-team { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.2rem; }
.ab-member { position: relative; overflow: hidden; border-radius: 26px; padding: 2.4rem 1.6rem 2rem; text-align: center; border: 1px solid rgba(197,197,197,.2); background: linear-gradient(170deg, #405653, #2C423F);
    animation: ab-rise .95s both; transition: transform .55s cubic-bezier(.2,.8,.2,1), border-color .5s, box-shadow .5s; }
.ab-member:nth-child(1) { animation-delay: .1s; } .ab-member:nth-child(2) { animation-delay: .25s; } .ab-member:nth-child(3) { animation-delay: .4s; }
.ab-member:hover { transform: translateY(-10px); border-color: rgba(197,197,197,.42); box-shadow: 0 28px 56px rgba(0,0,0,.3); }
.ab-member::before { content:""; position:absolute; left:50%; top: 4.4rem; width: 360px; height: 360px; margin: -180px 0 0 -180px; border-radius:50%; background: radial-gradient(circle, rgba(197,197,197,.22), transparent 62%); opacity:0; transition: opacity .6s; }
.ab-member:hover::before { opacity:1; }
.ab-idx { position:absolute; top:1rem; left:1.3rem; font-size:.7rem; letter-spacing:.24em; color: var(--mist); }
.ab-avatar { position: relative; width: 112px; height: 112px; margin: 0 auto 1.5rem; display:flex; align-items:center; justify-content:center; }
.ab-avatar::before { content:""; position:absolute; inset:0; border-radius:50%; border:1px dashed rgba(197,197,197,.4); animation: ab-spin 26s linear infinite; }
.ab-avatar::after { content:""; position:absolute; top:-4px; left:50%; width:8px; height:8px; margin-left:-4px; border-radius:50%; background: var(--mist); box-shadow: 0 0 14px var(--mist); transform-origin: 4px 60px; animation: ab-spin 9s linear infinite; }
.ab-core { width: 84px; height: 84px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size: 1.6rem; font-weight: 200; letter-spacing:.08em; color: var(--mist); background: radial-gradient(circle at 30% 25%, rgba(130,145,145,.55), rgba(44,66,63,.9)); border: 1px solid rgba(197,197,197,.35); transition: background .5s, color .5s, transform .5s; }
.ab-member:hover .ab-core { background: var(--mist); color: var(--forest); transform: scale(1.06); }
.stMarkdown h3.ab-name { position: relative; margin: 0; font-size: 1.3rem; font-weight: 500; color: var(--mist) !important; }
.ab-roles { position: relative; display:flex; flex-wrap:wrap; justify-content:center; gap:.45rem; margin-top: 1rem; }
.ab-role { padding: .28rem .8rem; border-radius: 999px; font-size: .68rem; font-weight: 600; letter-spacing: .2em; text-transform: uppercase; color: var(--mist); border: 1px solid rgba(197,197,197,.45); transition: color .4s, border-color .4s; }
.ab-member:hover .ab-role { color: var(--mist); border-color: rgba(197,197,197,.6); }

.ab-flow { position: relative; display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; }
.ab-flow::before { content:""; position:absolute; left: 0; right: 0; top: 17px; height:1px; background: linear-gradient(90deg, var(--steel), rgba(130,145,145,.1)); transform-origin: left; animation: ab-line 1.6s .3s both; }
.ab-node { position: relative; padding-top: 3rem; animation: ab-rise .9s both; }
.ab-node:nth-child(1){animation-delay:.1s}.ab-node:nth-child(2){animation-delay:.2s}.ab-node:nth-child(3){animation-delay:.3s}.ab-node:nth-child(4){animation-delay:.4s}.ab-node:nth-child(5){animation-delay:.5s}
.ab-dot { position:absolute; top:6px; left:0; width:24px; height:24px; border-radius:50%; background: var(--forest); border: 1px solid var(--mist); display:flex; align-items:center; justify-content:center; font-size:.62rem; letter-spacing:.05em; color: var(--mist); transition: background .4s, color .4s, transform .4s; }
.ab-node:hover .ab-dot { background: var(--mist); color: var(--forest); transform: scale(1.25); }
.ab-node h4 { margin: 0 0 .3rem; font-size: 1.12rem; font-weight: 600; color: var(--slate) !important; }
.ab-node p { margin: 0; font-size: .85rem; color: var(--slate); }

.ab-event { position: relative; margin-top: 3.4rem; padding: 2.4rem 2rem; text-align: center; border-radius: 26px; border: 1px solid rgba(197,197,197,.2); background: linear-gradient(180deg, #405653, #2C423F); }
.ab-event b { display:block; font-size: clamp(2rem, 5vw, 3.4rem); font-weight: 200; letter-spacing: .12em; color: var(--mist); }
.ab-event span { font-size: .8rem; font-weight: 600; letter-spacing: .4em; text-transform: uppercase; color: var(--mist); }
@media (max-width: 820px) { .ab-flow { grid-template-columns: 1fr; } .ab-flow::before { display:none; } .ab-hero { padding: 2.2rem 1.4rem; } }
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
                <div class="ab-kicker">About &nbsp;/&nbsp; {escape(BRAND_EXPANSION)}</div>
                <h1 class="ab-title">{escape(BRAND_NAME)}</h1>
                <p class="ab-lead">{escape(BRAND_TAGLINE)}</p>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    _label("Inside the engine")
    pills = "".join(
        f'<div class="ab-pill" style="animation-delay:{0.1 + i * 0.12:.2f}s"><small>{i + 1:02d}</small><span>{escape(text)}</span></div>'
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
        f'<div class="ab-node"><div class="ab-dot">{i + 1}</div><h4>{escape(title)}</h4><p>{escape(text)}</p></div>'
        for i, (title, text) in enumerate(FLOW)
    )
    st.markdown(f'<div class="ab-flow">{nodes}</div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="ab-event"><b>{EVENT}</b><span>{EVENT_LONG}</span></div>',
        unsafe_allow_html=True,
    )

    st.write("")
    page_footer()