"""About page."""

from html import escape

import streamlit as st

from app.components import page_footer
from app.config import BRAND_EXPANSION, BRAND_NAME, BRAND_TAGLINE

EVENT = "AICON'26"
EVENT_LONG = "Build with AI Hackathon"
PORTFOLIO_URL = "https://abdulbasit-archer.vercel.app/"
WHATSAPP_URL = "https://wa.me/923415878569?text=Hi%20Abdul%2C%20I%20found%20you%20through%20AICON%2726."

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;700&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');

@property --ang { syntax: '<angle>'; initial-value: 0deg; inherits: false; }

:root {
  --mist: #D4D7D3; --mist-hover: #E5E7E3;
  --sage: #A3ADA5; --steel: #899B9A;
  --slate: #46565D; --forest: #263A36; --deep: #1B2B28;
  --focus-ring: #A3ADA5;
  --ease: cubic-bezier(.2,.8,.2,1);
  --display: 'Space Grotesk', 'Inter', system-ui, sans-serif;
  --body: 'Inter', system-ui, sans-serif;
  --mono: 'JetBrains Mono', ui-monospace, monospace;
}

.stApp, .stApp p, .stApp li, .stApp span, .stApp div { font-family: var(--body); }
.stApp {
  background:
    radial-gradient(1100px 650px at 85% -10%, rgba(137,155,154,.22), transparent 60%),
    radial-gradient(900px 600px at -10% 45%, rgba(70,86,93,.38), transparent 60%),
    radial-gradient(700px 500px at 60% 110%, rgba(137,155,154,.14), transparent 60%),
    var(--forest);
  color: var(--mist);
}
/* film grain */
.stApp::after { content:""; position: fixed; inset: 0; pointer-events: none; z-index: 0; opacity: .05; mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>"); }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1120px; padding-top: 2rem; position: relative; z-index: 1; }

@keyframes ab-rise { from {opacity:0; transform: translateY(28px); filter: blur(8px);} to {opacity:1; transform:none; filter:none;} }
@keyframes ab-spin { to {transform: rotate(360deg);} }
@keyframes ab-orbit { to {--ang: 360deg;} }
@keyframes ab-float { 0%,100% {transform: translate(0,0) scale(1);} 50% {transform: translate(36px,-28px) scale(1.08);} }
@keyframes ab-shine { to {background-position: 220% 0;} }
@keyframes ab-line { from {transform: scaleX(0);} to {transform: scaleX(1);} }
@keyframes ab-caret { 0%,100% {opacity:1;} 50% {opacity:0;} }
@keyframes ab-pulse { 0% {box-shadow: 0 0 0 0 rgba(143,209,158,.6);} 70% {box-shadow: 0 0 0 9px rgba(143,209,158,0);} 100% {box-shadow: 0 0 0 0 rgba(143,209,158,0);} }
@keyframes ab-marquee { to {transform: translateX(-50%);} }
@keyframes ab-sweep { from {transform: translateX(-120%) skewX(-18deg);} to {transform: translateX(260%) skewX(-18deg);} }

/* ---------- Hero ---------- */
.ab-hero { position: relative; overflow: hidden; border-radius: 30px; padding: 3.4rem 3rem 3.1rem; border: 1px solid rgba(212,215,211,.26); background: linear-gradient(145deg, #405653, #2C423F); box-shadow: 0 30px 70px rgba(0,0,0,.35), inset 0 1px 0 rgba(212,215,211,.22); }
.ab-hero::before { content:""; position:absolute; inset:0; background-image: linear-gradient(rgba(212,215,211,.07) 1px, transparent 1px), linear-gradient(90deg, rgba(212,215,211,.07) 1px, transparent 1px); background-size: 56px 56px; -webkit-mask-image: radial-gradient(ellipse at 80% 30%, #000 15%, transparent 70%); mask-image: radial-gradient(ellipse at 80% 30%, #000 15%, transparent 70%); }
.ab-orb { position:absolute; right:-70px; top:-90px; width:340px; height:340px; border-radius:50%; background: var(--steel); filter: blur(72px); opacity:.45; animation: ab-float 14s ease-in-out infinite; }
.ab-orb.two { right:auto; left:-110px; top:auto; bottom:-150px; width:260px; height:260px; opacity:.22; animation-duration: 18s; animation-direction: reverse; }
.ab-kicker { position: relative; font-family: var(--mono); font-size: .74rem; font-weight: 500; letter-spacing: .3em; text-transform: uppercase; color: var(--sage); animation: ab-rise .9s both; }
.ab-kicker::before { content:"// "; color: var(--steel); }
.ab-title { position: relative; margin: .9rem 0 .2rem; font-family: var(--display); font-size: clamp(2.6rem, 7vw, 5rem); font-weight: 300; letter-spacing: .08em; line-height: 1.05; text-transform: uppercase;
    background: linear-gradient(100deg, #D4D7D3 20%, #F2F4F1 40%, #D4D7D3 60%, #F2F4F1 80%); background-size: 220% 100%; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; color: transparent; animation: ab-rise 1s .1s both, ab-shine 7s linear infinite; }
.stMarkdown h1.ab-title { color: transparent !important; -webkit-text-fill-color: transparent !important; padding: 0; }
.ab-exp { position: relative; display: flex; align-items: center; gap: 1.1rem; margin: .5rem 0 1.4rem; animation: ab-rise .9s .2s both; }
.ab-exp::before { content:""; flex: none; width: 64px; height: 1px; background: linear-gradient(90deg, var(--mist), rgba(212,215,211,.2)); transform-origin: left; animation: ab-line 1.3s .5s both; }
.stMarkdown .ab-exp span { font-family: var(--mono); font-size: clamp(.72rem, 1.1vw, .9rem); letter-spacing: .26em; line-height: 1.8; text-transform: uppercase; color: var(--sage) !important; }
.ab-exp span::after { content:""; display:inline-block; width:7px; height:1em; margin-left:.7rem; vertical-align:-.15em; background: var(--mist); animation: ab-caret 1.1s steps(1) infinite; }
.stMarkdown p.ab-lead { position: relative; max-width: 34rem; margin: 0; font-size: 1.12rem; font-weight: 300; line-height: 1.8; color: var(--mist) !important; animation: ab-rise 1s .3s both; }

/* ---------- Section labels ---------- */
.ab-label { margin: 3.6rem 0 1.4rem; display: flex; align-items: center; gap: 1rem; font-family: var(--mono); font-size: .74rem; font-weight: 500; letter-spacing: .28em; text-transform: uppercase; color: var(--steel); }
.ab-label b { font-weight: 500; color: var(--mist); padding: .2rem .55rem; border: 1px solid rgba(212,215,211,.3); border-radius: 6px; letter-spacing: .1em; }
.ab-label::after { content:""; flex:1; height:1px; background: linear-gradient(90deg, rgba(137,155,154,.55), transparent); transform-origin: left; animation: ab-line 1.4s .2s both; }

/* ---------- Developer ---------- */
.ab-dev-wrap { position: relative; padding: 1.5px; border-radius: 32px; animation: ab-rise 1s both;
  background: conic-gradient(from var(--ang), rgba(212,215,211,.08), rgba(163,173,165,.9), rgba(137,155,154,.15) 40%, rgba(212,215,211,.08) 60%, rgba(229,231,227,.8), rgba(212,215,211,.08));
  animation: ab-rise 1s both, ab-orbit 9s linear infinite; box-shadow: 0 30px 70px rgba(0,0,0,.35); }
.ab-dev { position: relative; overflow: hidden; display: grid; grid-template-columns: 240px 1fr; gap: 2.6rem; align-items: center; padding: 2.8rem 2.8rem 2.4rem; border-radius: 31px; background: linear-gradient(160deg, #3F5552, #263A36 80%); }
.ab-dev::before { content:""; position:absolute; left:-90px; bottom:-130px; width:380px; height:380px; border-radius:50%; background: radial-gradient(circle, rgba(137,155,154,.3), transparent 65%); pointer-events:none; }
.ab-dev::after { content:""; position:absolute; inset:0; background-image: linear-gradient(rgba(212,215,211,.05) 1px, transparent 1px), linear-gradient(90deg, rgba(212,215,211,.05) 1px, transparent 1px); background-size: 44px 44px; -webkit-mask-image: radial-gradient(ellipse at 100% 0%, #000 0%, transparent 65%); mask-image: radial-gradient(ellipse at 100% 0%, #000 0%, transparent 65%); pointer-events:none; }
.ab-dev-side { position: relative; z-index: 1; text-align: center; }
.ab-avatar { position: relative; width: 176px; height: 176px; margin: 0 auto 1.3rem; display:flex; align-items:center; justify-content:center; }
.ab-avatar::before { content:""; position:absolute; inset:0; border-radius:50%; border:1px dashed rgba(212,215,211,.45); animation: ab-spin 26s linear infinite; }
.ab-avatar::after { content:""; position:absolute; top:-4px; left:50%; width:8px; height:8px; margin-left:-4px; border-radius:50%; background: var(--mist); box-shadow: 0 0 16px var(--mist); transform-origin: 4px 92px; animation: ab-spin 9s linear infinite; }
.ab-ring { position:absolute; inset:12px; border-radius:50%; border: 1px solid rgba(212,215,211,.2); }
.ab-core { position: relative; width: 128px; height: 128px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-family: var(--display); font-size: 2.6rem; font-weight: 300; letter-spacing:.06em; color: var(--mist); background: radial-gradient(circle at 30% 25%, rgba(137,155,154,.6), rgba(27,43,40,.97)); border: 1px solid rgba(212,215,211,.42); box-shadow: 0 14px 34px rgba(0,0,0,.35), inset 0 1px 0 rgba(212,215,211,.25); transition: background .5s, color .5s, transform .6s var(--ease); }
.ab-dev:hover .ab-core { background: var(--mist); color: var(--forest); transform: scale(1.06) rotate(-4deg); }
.ab-status { display: inline-flex; align-items: center; gap: .55rem; padding: .38rem .9rem; border-radius: 999px; font-family: var(--mono); font-size: .66rem; font-weight: 500; letter-spacing: .16em; text-transform: uppercase; color: var(--mist); border: 1px solid rgba(212,215,211,.35); background: rgba(27,43,40,.6); }
.ab-status i { width: 8px; height: 8px; border-radius: 50%; background: #8FD19E; animation: ab-pulse 2s infinite; }
.ab-dev-main { position: relative; z-index: 1; min-width: 0; }
.ab-term { display: inline-block; margin-bottom: 1.1rem; padding: .45rem .9rem; border-radius: 10px; font-family: var(--mono); font-size: .76rem; color: var(--sage); background: rgba(27,43,40,.7); border: 1px solid rgba(212,215,211,.2); }
.ab-term b { color: #8FD19E; font-weight: 500; }
.ab-term::after { content:""; display:inline-block; width:7px; height:.95em; margin-left:.4rem; vertical-align:-.12em; background: var(--mist); animation: ab-caret 1.1s steps(1) infinite; }
.stMarkdown h3.ab-name { margin: 0; padding: 0; font-family: var(--display); font-size: clamp(2rem, 4vw, 3rem); font-weight: 500; letter-spacing: -.01em; line-height: 1.05; color: var(--mist-hover) !important; }
.ab-name em { font-style: normal; font-family: var(--mono); font-weight: 500; color: var(--steel); letter-spacing: .2em; font-size: .3em; margin-left: .9rem; padding: .25rem .6rem; border: 1px solid rgba(137,155,154,.5); border-radius: 6px; vertical-align: .9em; }
.ab-title-line { margin: .7rem 0 0; font-family: var(--mono); font-size: .76rem; font-weight: 500; letter-spacing: .2em; text-transform: uppercase; color: var(--sage); }
.stMarkdown .ab-bio { margin: 1.2rem 0 0; max-width: 40rem; font-size: 1.02rem; font-weight: 300; line-height: 1.85; color: var(--mist) !important; }
.ab-meta { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin: 1.6rem 0 0; }
.ab-meta div { padding: .9rem 1rem; border-radius: 14px; font-size: .9rem; color: var(--mist); background: rgba(27,43,40,.45); border: 1px solid rgba(212,215,211,.15); transition: border-color .4s, transform .4s var(--ease); }
.ab-meta div:hover { border-color: rgba(212,215,211,.45); transform: translateY(-3px); }
.ab-meta small { display: block; margin-bottom: .35rem; font-family: var(--mono); font-size: .62rem; font-weight: 500; letter-spacing: .22em; text-transform: uppercase; color: var(--steel); }
.ab-marquee { position: relative; overflow: hidden; margin-top: 1.6rem; padding: .3rem 0; -webkit-mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent); mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent); }
.ab-track { display: flex; width: max-content; gap: .6rem; animation: ab-marquee 34s linear infinite; }
.ab-marquee:hover .ab-track { animation-play-state: paused; }
.ab-chip { flex: none; padding: .38rem .95rem; border-radius: 999px; font-family: var(--mono); font-size: .7rem; font-weight: 500; letter-spacing: .08em; color: var(--sage); border: 1px solid rgba(212,215,211,.35); background: rgba(27,43,40,.35); transition: color .35s, border-color .35s, background .35s; }
.ab-chip:hover { color: var(--forest); background: var(--mist); border-color: var(--mist); }
.ab-links { display: flex; flex-wrap: wrap; gap: .8rem; margin-top: 1.8rem; }
.stMarkdown a.ab-btn { position: relative; overflow: hidden; display: inline-flex; align-items: center; gap: .6rem; padding: .85rem 1.5rem; border-radius: 999px; font-family: var(--mono); font-size: .76rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; text-decoration: none !important; color: var(--forest) !important; background: var(--mist); border: 1px solid var(--mist); transition: background .35s, transform .35s var(--ease), box-shadow .35s; }
.stMarkdown a.ab-btn::after { content:""; position:absolute; top:0; bottom:0; left:0; width:40%; background: linear-gradient(90deg, transparent, rgba(255,255,255,.55), transparent); transform: translateX(-120%) skewX(-18deg); }
.stMarkdown a.ab-btn:hover { background: var(--mist-hover); transform: translateY(-3px); box-shadow: 0 16px 32px rgba(0,0,0,.35); }
.stMarkdown a.ab-btn:hover::after { animation: ab-sweep .9s var(--ease); }
.stMarkdown a.ab-btn span { display:inline-block; transition: transform .35s var(--ease); }
.stMarkdown a.ab-btn:hover span { transform: translate(3px,-3px); }
.stMarkdown a.ab-btn.ghost { color: var(--mist) !important; background: transparent; border-color: rgba(212,215,211,.45); }
.stMarkdown a.ab-btn.ghost:hover { background: rgba(212,215,211,.1); }
.stMarkdown a.ab-btn.wa { color: #0E2A1A !important; background: #8FD19E; border-color: #8FD19E; }
.stMarkdown a.ab-btn.wa:hover { background: #A9E0B5; box-shadow: 0 16px 32px rgba(143,209,158,.28); }

/* ---------- Contact CTA ---------- */
.ab-cta { position: relative; overflow: hidden; margin-top: 3.6rem; display: grid; grid-template-columns: 1.3fr 1fr; gap: 2rem; align-items: center; padding: 2.6rem 2.8rem; border-radius: 28px; border: 1px solid rgba(212,215,211,.26); background: linear-gradient(145deg, #405653, #2C423F); box-shadow: 0 24px 56px rgba(0,0,0,.28), inset 0 1px 0 rgba(212,215,211,.2); animation: ab-rise 1s both; }
.ab-cta::before { content:""; position:absolute; right:-80px; top:-100px; width:300px; height:300px; border-radius:50%; background: var(--steel); filter: blur(70px); opacity:.35; animation: ab-float 16s ease-in-out infinite; }
.ab-cta > * { position: relative; }
.stMarkdown .ab-cta h3 { margin: 0; padding: 0; font-family: var(--display); font-size: clamp(1.6rem, 3.2vw, 2.4rem); font-weight: 500; line-height: 1.15; color: var(--mist-hover) !important; }
.stMarkdown .ab-cta p { margin: .8rem 0 0; font-size: 1rem; font-weight: 300; line-height: 1.8; color: var(--mist) !important; }
.ab-cta-side { display: grid; gap: .9rem; justify-items: start; }
.ab-phone { font-family: var(--mono); font-size: 1.05rem; letter-spacing: .08em; color: var(--mist); }
.ab-phone small { display:block; margin-bottom:.3rem; font-size:.62rem; letter-spacing:.24em; text-transform:uppercase; color: var(--steel); }
.stMarkdown a.ab-btn:focus-visible { outline: 2px solid var(--focus-ring); outline-offset: 3px; }

/* ---------- About the project ---------- */
.ab-about { display: grid; grid-template-columns: 1.4fr 1fr; gap: 1.2rem; }
.ab-panel { position: relative; overflow: hidden; padding: 1.9rem 1.9rem 1.7rem; border-radius: 24px; border: 1px solid rgba(212,215,211,.22); background: linear-gradient(150deg, #405653, #2C423F); box-shadow: 0 12px 28px rgba(0,0,0,.18); animation: ab-rise .9s both; transition: transform .5s var(--ease), border-color .5s, box-shadow .5s; }
.ab-panel:hover { transform: translateY(-5px); border-color: rgba(212,215,211,.45); box-shadow: 0 22px 44px rgba(0,0,0,.3); }
.stMarkdown .ab-panel p { margin: 0 0 1rem; font-size: 1.02rem; font-weight: 300; line-height: 1.85; color: var(--mist) !important; }
.stMarkdown .ab-panel p:last-child { margin-bottom: 0; }
.ab-panel h4 { margin: 0 0 1.1rem; padding: 0; font-family: var(--mono); font-size: .72rem; font-weight: 500; letter-spacing: .24em; text-transform: uppercase; color: var(--sage) !important; }
.ab-points { margin: 0; padding: 0; list-style: none; display: grid; gap: .95rem; }
.ab-points li { position: relative; padding-left: 1.5rem; font-size: .95rem; font-weight: 300; line-height: 1.6; color: var(--mist); }
.ab-points li::before { content:""; position:absolute; left:0; top:.55em; width:7px; height:7px; border-radius:50%; background: var(--steel); box-shadow: 0 0 10px rgba(137,155,154,.7); }

/* ---------- Capabilities ---------- */
.ab-pills { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1rem; }
.ab-pill { position: relative; overflow: hidden; padding: 1.35rem 1.4rem; border-radius: 20px; border: 1px solid rgba(212,215,211,.22); background: linear-gradient(150deg, #405653, #2C423F); box-shadow: 0 12px 28px rgba(0,0,0,.18); animation: ab-rise .9s both; transition: transform .45s var(--ease), border-color .45s, box-shadow .45s; }
.ab-pill::after { content:""; position:absolute; left:0; right:0; bottom:0; height:2px; background: linear-gradient(90deg, var(--steel), var(--mist)); transform: scaleX(0); transform-origin: left; transition: transform .6s var(--ease); }
.ab-pill:hover { transform: translateY(-7px); border-color: rgba(212,215,211,.45); box-shadow: 0 22px 44px rgba(0,0,0,.3); }
.ab-pill:hover::after { transform: scaleX(1); }
.ab-pill small { display:block; font-family: var(--mono); font-size:.7rem; letter-spacing:.22em; color: var(--sage); margin-bottom:.7rem; }
.ab-pill span { font-family: var(--display); font-size: 1.15rem; font-weight: 400; color: var(--mist); }

/* ---------- Flow ---------- */
.ab-flow { position: relative; display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; }
.ab-flow::before { content:""; position:absolute; left: 0; right: 0; top: 17px; height:1px; background: linear-gradient(90deg, var(--steel), rgba(137,155,154,.12)); transform-origin: left; animation: ab-line 1.6s .3s both; }
.ab-node { position: relative; padding-top: 3rem; animation: ab-rise .9s both; }
.ab-node:nth-child(1){animation-delay:.1s}.ab-node:nth-child(2){animation-delay:.2s}.ab-node:nth-child(3){animation-delay:.3s}.ab-node:nth-child(4){animation-delay:.4s}.ab-node:nth-child(5){animation-delay:.5s}
.ab-dot { position:absolute; top:6px; left:0; width:24px; height:24px; border-radius:50%; background: var(--forest); border: 1px solid var(--mist); display:flex; align-items:center; justify-content:center; font-family: var(--mono); font-size:.62rem; color: var(--mist); transition: background .4s, color .4s, transform .4s var(--ease), box-shadow .4s; }
.ab-node:hover .ab-dot { background: var(--mist); color: var(--forest); transform: scale(1.3); box-shadow: 0 0 18px rgba(212,215,211,.6); }
.stMarkdown .ab-node h4 { margin: 0 0 .3rem; padding: 0; font-family: var(--display); font-size: 1.15rem; font-weight: 500; color: var(--mist) !important; }
.ab-node p { margin: 0; font-size: .86rem; font-weight: 300; color: var(--sage); }

/* ---------- Event ---------- */
.ab-event { position: relative; overflow: hidden; margin-top: 3.6rem; padding: 2.8rem 2rem; text-align: center; border-radius: 28px; border: 1px solid rgba(212,215,211,.24); background: linear-gradient(180deg, #405653, #2C423F); box-shadow: 0 20px 50px rgba(0,0,0,.25); }
.ab-event::before { content:""; position:absolute; left:50%; top:-60%; width: 520px; height: 520px; margin-left:-260px; border-radius:50%; background: radial-gradient(circle, rgba(137,155,154,.3), transparent 65%); }
.ab-event b { position: relative; display:block; font-family: var(--display); font-size: clamp(2rem, 5vw, 3.6rem); font-weight: 300; letter-spacing: .12em; color: var(--mist); }
.ab-event span { position: relative; font-family: var(--mono); font-size: .78rem; font-weight: 500; letter-spacing: .36em; text-transform: uppercase; color: var(--sage); }

@media (max-width: 820px) {
    .ab-flow { grid-template-columns: 1fr; }
    .ab-flow::before { display: none; }
    .ab-about { grid-template-columns: 1fr; }
    .ab-cta { grid-template-columns: 1fr; padding: 2rem 1.4rem; text-align: center; }
    .ab-cta-side { justify-items: center; }
    .ab-dev { grid-template-columns: 1fr; padding: 2rem 1.4rem; gap: 1.6rem; text-align: center; }
    .ab-links { justify-content: center; }
    .stMarkdown .ab-bio { margin-left: auto; margin-right: auto; }
    .ab-name em { display: none; }
    .ab-hero { padding: 2.2rem 1.4rem; }
    .ab-exp::before { width: 28px; }
    .stMarkdown .ab-exp span { letter-spacing: .16em; }
}
@media (prefers-reduced-motion: reduce) {
    .ab-hero *, .ab-exp, .ab-exp::before, .ab-exp span::after, .ab-pill, .ab-panel, .ab-dev-wrap, .ab-node, .ab-flow::before,
    .ab-label::after, .ab-avatar::before, .ab-avatar::after, .ab-orb, .ab-status i, .ab-track, .ab-term::after { animation: none !important; transition: none !important; }
}
</style>
"""

DEVELOPER = {
    "name": "Abdul Basit",
    "alias": "ARCHER",
    "initials": "AB",
    "headline": "Full-Stack Developer · AI Specialist",
    "whoami": "abdul-basit // full-stack · ai · iot",
    "bio": (
        "Full-stack React developer and generative-AI specialist who builds intelligent, "
        "ethical and visually polished digital products. Works across the MERN stack, "
        "LLM integration and prompt engineering, and extends into IoT with Arduino and "
        "ESP32 systems. Built this project's routing and cost-telemetry engine for AICON'26."
    ),
    "location": "Islamabad, Pakistan",
    "availability": "Freelance · Full-time · Remote",
    "role": "Design & development",
    "status": "Open to work",
    "skills": (
        "React",
        "Next.js",
        "MERN Stack",
        "Python",
        "Streamlit",
        "LLM Integration",
        "OpenAI API",
        "Groq",
        "Prompt Engineering",
        "Arduino / ESP32",
    ),
    "phone": "+92 341 5878569",
    "links": (
        ("Portfolio", PORTFOLIO_URL, ""),
        ("WhatsApp", WHATSAPP_URL, "wa"),
    ),
}

ABOUT_PARAGRAPHS = (
    "Not every prompt needs the biggest model. This app inspects each request, "
    "decides how demanding it is, and sends it to the smallest Groq model that can "
    "answer it well, so quality stays high while cost and latency stay low.",
    "Every answer is checked before it reaches you. If the check fails, the request "
    "escalates to a stronger tier automatically, and each session reports its tokens "
    "and estimated spend so the trade-offs stay visible.",
)

ABOUT_POINTS = (
    "Transparent: the tier and model behind every answer are shown.",
    "Resilient: a labeled local mock keeps the app usable without a live API.",
    "Accountable: tokens and estimated cost are tracked per session.",
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


def _label(index: str, text: str) -> None:
    st.markdown(
        f'<div class="ab-label"><b>{escape(index)}</b>{escape(text)}</div>',
        unsafe_allow_html=True,
    )


def _hero() -> None:
    st.markdown(
        _html(
            f"""
            <div class="ab-hero">
                <div class="ab-orb"></div>
                <div class="ab-orb two"></div>
                <div class="ab-kicker">About</div>
                <h1 class="ab-title">{escape(BRAND_NAME)}</h1>
                <div class="ab-exp"><span>{escape(BRAND_EXPANSION)}</span></div>
                <p class="ab-lead">{escape(BRAND_TAGLINE)}</p>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


def _developer() -> None:
    d = DEVELOPER
    _label("01", "The developer")
    chip_list = [f'<span class="ab-chip">{escape(s)}</span>' for s in d["skills"]]
    chips = "".join(chip_list * 2)  # duplicated for a seamless marquee loop
    links = "".join(
        f'<a class="ab-btn {style}" href="{escape(url, quote=True)}" '
        f'target="_blank" rel="noopener noreferrer">{escape(text)} <span aria-hidden="true">↗</span></a>'
        for text, url, style in d["links"]
    )
    st.markdown(
        _html(
            f"""
            <div class="ab-dev-wrap">
            <article class="ab-dev">
                <div class="ab-dev-side">
                    <div class="ab-avatar" aria-hidden="true"><div class="ab-ring"></div><div class="ab-core">{escape(d["initials"])}</div></div>
                    <span class="ab-status"><i></i>{escape(d["status"])}</span>
                </div>
                <div class="ab-dev-main">
                    <div class="ab-term"><b>$</b> whoami &rarr; {escape(d["whoami"])}</div>
                    <h3 class="ab-name">{escape(d["name"])}<em>{escape(d["alias"])}</em></h3>
                    <div class="ab-title-line">{escape(d["headline"])}</div>
                    <p class="ab-bio">{escape(d["bio"])}</p>
                    <div class="ab-meta">
                        <div><small>Based in</small>{escape(d["location"])}</div>
                        <div><small>Availability</small>{escape(d["availability"])}</div>
                        <div><small>Role here</small>{escape(d["role"])}</div>
                    </div>
                    <div class="ab-marquee"><div class="ab-track">{chips}</div></div>
                    <div class="ab-links">{links}</div>
                </div>
            </article>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


def _about_project() -> None:
    _label("02", "About the project")
    paragraphs = "".join(f"<p>{escape(p)}</p>" for p in ABOUT_PARAGRAPHS)
    points = "".join(f"<li>{escape(p)}</li>" for p in ABOUT_POINTS)
    st.markdown(
        _html(
            f"""
            <div class="ab-about">
                <div class="ab-panel">{paragraphs}</div>
                <div class="ab-panel"><h4>Principles</h4><ul class="ab-points">{points}</ul></div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


def _capabilities() -> None:
    _label("03", "Inside the engine")
    pills = "".join(
        f'<div class="ab-pill" style="animation-delay:{0.1 + i * 0.12:.2f}s">'
        f"<small>{i + 1:02d}</small><span>{escape(text)}</span></div>"
        for i, text in enumerate(CAPABILITIES)
    )
    st.markdown(f'<div class="ab-pills">{pills}</div>', unsafe_allow_html=True)


def _flow() -> None:
    _label("04", "How it flows")
    nodes = "".join(
        f'<div class="ab-node"><div class="ab-dot">{i + 1}</div>'
        f"<h4>{escape(title)}</h4><p>{escape(text)}</p></div>"
        for i, (title, text) in enumerate(FLOW)
    )
    st.markdown(f'<div class="ab-flow">{nodes}</div>', unsafe_allow_html=True)


def _contact() -> None:
    d = DEVELOPER
    links = "".join(
        f'<a class="ab-btn {style}" href="{escape(url, quote=True)}" '
        f'target="_blank" rel="noopener noreferrer">{escape(text)} <span aria-hidden="true">↗</span></a>'
        for text, url, style in d["links"]
    )
    st.markdown(
        _html(
            f"""
            <div class="ab-cta">
                <div>
                    <h3>Have an idea? Let's build it.</h3>
                    <p>Open to freelance projects, full-time roles and remote collaboration. Message on WhatsApp or browse the portfolio.</p>
                </div>
                <div class="ab-cta-side">
                    <div class="ab-phone"><small>WhatsApp</small>{escape(d["phone"])}</div>
                    <div class="ab-links" style="margin-top:0">{links}</div>
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


def render() -> None:
    st.markdown(_html(_CSS), unsafe_allow_html=True)
    _hero()
    _developer()
    _about_project()
    _capabilities()
    _flow()
    _contact()

    st.markdown(
        f'<div class="ab-event"><b>{escape(EVENT)}</b><span>{escape(EVENT_LONG)}</span></div>',
        unsafe_allow_html=True,
    )

    st.write("")
    page_footer()