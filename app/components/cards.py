"""Feature and information cards."""

from collections.abc import Sequence
from html import escape

import streamlit as st

# Palette: C5C5C5  949B96  4C5B61  2C423F  829191
_STYLE = (
    "<style>"
    "@keyframes cd-rise{from{opacity:0;transform:translateY(22px);filter:blur(5px)}to{opacity:1;transform:none;filter:none}}"
    ".feature-card,.team-card,.about-section{position:relative;overflow:hidden;border-radius:22px;"
    "border:1px solid rgba(197,197,197,.14);background:linear-gradient(160deg,rgba(76,91,97,.38),rgba(44,66,63,.15));"
    "color:#C5C5C5;animation:cd-rise .9s both;"
    "transition:transform .5s cubic-bezier(.2,.8,.2,1),border-color .5s,box-shadow .5s}"
    ".feature-card::before,.team-card::before{content:'';position:absolute;width:220px;height:220px;right:-90px;top:-90px;"
    "border-radius:50%;background:radial-gradient(circle,rgba(197,197,197,.32),transparent 70%);opacity:0;transition:opacity .5s}"
    ".feature-card:hover,.team-card:hover{transform:translateY(-8px);border-color:rgba(197,197,197,.4);box-shadow:0 24px 50px rgba(0,0,0,.28)}"
    ".feature-card:hover::before,.team-card:hover::before{opacity:1}"
    ".feature-card{padding:1.7rem 1.5rem 1.5rem;min-height:190px}"
    ".feature-icon,.team-avatar{display:flex;align-items:center;justify-content:center;width:2.6rem;height:2.6rem;border-radius:50%;"
    "border:1px solid rgba(197,197,197,.35);color:#C5C5C5;font-weight:300;letter-spacing:.05em;transition:background .4s,color .4s}"
    ".feature-card:hover .feature-icon,.team-card:hover .team-avatar{background:#C5C5C5;color:#2C423F}"
    ".feature-title{margin:1.8rem 0 .3rem;font-size:1.35rem;font-weight:300;color:#C5C5C5}"
    ".feature-card p{margin:0;color:#949B96;font-size:.95rem}"
    ".team-card{padding:1.6rem 1.4rem;text-align:center}"
    ".team-avatar{width:4rem;height:4rem;margin:0 auto 1rem;font-size:1.15rem}"
    ".team-name{margin:0;font-size:1.15rem;font-weight:300;color:#C5C5C5}"
    ".team-role{margin-top:.3rem;font-size:.72rem;letter-spacing:.24em;text-transform:uppercase;color:#829191}"
    ".about-section{padding:1.8rem 1.8rem 1.6rem;margin-bottom:1rem}"
    ".about-section p{color:#949B96;margin:.6rem 0 0}"
    ".about-kicker{display:flex;align-items:center;gap:1rem;font-size:.75rem;letter-spacing:.3em;text-transform:uppercase;color:#829191}"
    ".about-kicker::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(130,145,145,.5),transparent)}"
    ".step-list{list-style:none;counter-reset:s;margin:1rem 0 0;padding:0}"
    ".step-list li{counter-increment:s;display:flex;gap:1rem;align-items:baseline;padding:.8rem 0;border-top:1px solid rgba(197,197,197,.14);"
    "color:#949B96;transition:padding-left .4s,border-color .4s}"
    ".step-list li::before{content:counter(s,decimal-leading-zero);font-size:.75rem;letter-spacing:.2em;color:#829191}"
    ".step-list li:hover{padding-left:.6rem;border-color:rgba(197,197,197,.4)}"
    ".step-list strong{font-weight:400;color:#C5C5C5}"
    ".team-placeholder{display:flex;align-items:center;gap:1rem;margin-top:1rem;padding:1rem 1.2rem;border-radius:16px;"
    "border:1px dashed rgba(197,197,197,.3)}"
    ".team-mark{display:flex;align-items:center;justify-content:center;width:2.4rem;height:2.4rem;border-radius:50%;"
    "border:1px solid rgba(197,197,197,.35);color:#C5C5C5}"
    ".team-copy{color:#949B96;font-size:.92rem}"
    "</style>"
)


def feature_card(title: str, body: str) -> None:
    """Render a feature card; the icon is the title's first letter."""
    st.markdown(
        _STYLE
        + (
            '<div class="feature-card">'
            f'<div class="feature-icon" aria-hidden="true">{escape(title[0])}</div>'
            f'<div class="feature-title">{escape(title)}</div>'
            f"<p>{escape(body)}</p>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def team_member_card(name: str, role: str, initials: str) -> None:
    """Render a team member card."""
    st.markdown(
        _STYLE
        + (
            '<article class="team-card">'
            f'<div class="team-avatar" aria-hidden="true">{escape(initials)}</div>'
            f'<h3 class="team-name">{escape(name)}</h3>'
            f'<div class="team-role">{escape(role)}</div>'
            "</article>"
        ),
        unsafe_allow_html=True,
    )


def steps_markup(steps: Sequence[tuple[str, str]]) -> str:
    items = "".join(
        f"<li><strong>{escape(title)}</strong> {escape(text)}</li>" for title, text in steps
    )
    return f'<ol class="step-list">{items}</ol>'


def info_section(
    kicker: str,
    body: str = "",
    steps: Sequence[tuple[str, str]] = (),
    placeholder: str | None = None,
) -> None:
    """Render a titled information section."""
    parts = [f'<div class="about-kicker">{escape(kicker)}</div>']
    if body:
        parts.append(f"<p>{escape(body)}</p>")
    if steps:
        parts.append(steps_markup(steps))
    if placeholder:
        parts.append(
            '<div class="team-placeholder"><div class="team-mark" aria-hidden="true">T</div>'
            f'<div class="team-copy">{escape(placeholder)}</div></div>'
        )
    st.markdown(
        f'{_STYLE}<div class="about-section">{"".join(parts)}</div>',
        unsafe_allow_html=True,
    )