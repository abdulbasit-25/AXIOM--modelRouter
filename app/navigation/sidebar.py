
"""Axiom's light-themed navigation."""

import streamlit as st

from app.config import BRAND_NAME, BRAND_WORDMARK, NAVIGATION, NAV_ICONS
from app.components.branding import brand_lockup


def render_sidebar() -> str:
    """Render the sidebar and return the selected destination."""

    st.markdown(
        """
        <style>
        /* ===== SIDEBAR PALETTE ===== */

        [data-testid="stSidebar"] {
            --mr-sidebar-bg: #F0F2F1;
            --mr-sidebar-border: var(--brand-neutral);
            --mr-sidebar-ink: var(--brand-primary);
            --mr-sidebar-muted: var(--brand-secondary);
            --mr-sidebar-accent: var(--brand-accent);
            background: var(--mr-sidebar-bg);
            border-right: 1px solid var(--mr-sidebar-border);
        }

        [data-testid="stSidebar"] > div:first-child {
            padding: 1.45rem 1rem 1rem;
        }

        /* Brand spacing */
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            gap: 0.55rem;
        }

        /* Section label */
        .mr-nav-heading {
            margin: 1.55rem 0 0.7rem;
            padding: 0 0.75rem;
            color: var(--mr-sidebar-muted);
            font-family: "Segoe UI", sans-serif;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1.6px;
            text-transform: uppercase;
        }

        /* ===== NAVIGATION ===== */

        [data-testid="stSidebar"] [role="radiogroup"] {
            gap: 5px;
        }

        [data-testid="stSidebar"] [role="radiogroup"] [data-testid="stRadioOption"] {
            position: relative;
            display: flex;
            align-items: center;
            min-height: 45px;
            padding: 0.58rem 0.8rem;
            border: 1px solid transparent;
            border-radius: 10px;
            background: transparent;
            transition: background 160ms ease,
                        border-color 160ms ease,
                        box-shadow 160ms ease,
                        transform 160ms ease;
        }

        [data-testid="stSidebar"] [role="radiogroup"]
        [data-testid="stRadioOption"] > div:last-child,
        [data-testid="stSidebar"] [role="radiogroup"]
        [data-testid="stRadioOption"] > div:last-child p {
            margin: 0;
            color: var(--mr-sidebar-ink);
            font-family: "Segoe UI", sans-serif;
            font-size: 13.5px;
            font-weight: 550;
            letter-spacing: 0.1px;
            line-height: 1.5;
        }

        [data-testid="stSidebar"] [role="radiogroup"]
        [data-testid="stRadioOption"] > div:last-child > div:first-child {
            display: none !important;
        }

        [data-testid="stSidebar"] [role="radiogroup"]
        [data-testid="stRadioOption"]:hover {
            background: var(--primary-soft);
            border-color: var(--mr-sidebar-border);
            transform: translateX(2px);
        }

        [data-testid="stSidebar"] [role="radiogroup"]
        [data-testid="stRadioOption"]:hover > div:last-child,
        [data-testid="stSidebar"] [role="radiogroup"]
        [data-testid="stRadioOption"]:hover > div:last-child p {
            color: var(--mr-sidebar-ink);
        }

        /* High-contrast active state uses the primary Axiom brand color. */
        [data-testid="stSidebar"] [role="radiogroup"]
        [data-testid="stRadioOption"][data-selected="true"] {
            background: var(--brand-primary);
            border-color: var(--brand-primary);
            box-shadow: 0 5px 14px rgba(44, 66, 63, 0.14);
        }

        [data-testid="stSidebar"] [role="radiogroup"]
        [data-testid="stRadioOption"][data-selected="true"] > div:last-child,
        [data-testid="stSidebar"] [role="radiogroup"]
        [data-testid="stRadioOption"][data-selected="true"] > div:last-child p {
            color: #FFFFFF !important;
            font-weight: 650;
        }

        [data-testid="stSidebar"] [role="radiogroup"]
        [data-testid="stRadioOption"][data-selected="true"]::before {
            content: "";
            position: absolute;
            left: -1px;
            top: 11px;
            bottom: 11px;
            width: 3px;
            border-radius: 0 3px 3px 0;
            background: var(--mr-sidebar-accent);
        }

        /* Keyboard accessibility */
        [data-testid="stSidebar"] [role="radiogroup"]
        [data-testid="stRadioOption"]:focus-within {
            outline: 2px solid var(--mr-sidebar-accent);
            outline-offset: 2px;
        }

        /* ===== DIVIDER ===== */

        .mr-divider {
            height: 1px;
            margin: 1.15rem 0;
            background: var(--mr-sidebar-border);
        }

        /* ===== SYSTEM PANEL ===== */

        .mr-system-panel {
            padding: 16px 14px 14px;
            border: 1px solid var(--mr-sidebar-border);
            border-radius: 12px;
            background: #FFFFFF;
            box-shadow: 0 4px 14px rgba(44, 66, 63, 0.045);
        }

        .mr-system-eyebrow {
            color: var(--mr-sidebar-muted);
            font-family: "Segoe UI", sans-serif;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1.4px;
        }

        .mr-system-title {
            margin-top: 12px;
            color: var(--mr-sidebar-ink);
            font-family: "Segoe UI", sans-serif;
            font-size: 14px;
            font-weight: 700;
            letter-spacing: -0.2px;
        }

        .mr-system-description {
            margin-top: 5px;
            color: var(--mr-sidebar-muted);
            font-family: "Segoe UI", sans-serif;
            font-size: 11px;
            font-weight: 400;
            line-height: 1.7;
        }

        .mr-system-caption {
            margin-top: 14px;
            padding-top: 10px;
            border-top: 1px solid var(--mr-sidebar-border);
            color: var(--mr-sidebar-muted);
            font-family: "Segoe UI", sans-serif;
            font-size: 9px;
            font-weight: 700;
            letter-spacing: 1px;
        }

        /* ===== FOOTER ===== */

        .mr-sidebar-footer {
            padding: 10px 0 0;
            color: var(--mr-sidebar-muted);
            font-family: "Segoe UI", sans-serif;
            font-size: 9px;
            font-weight: 600;
            letter-spacing: 1.2px;
            text-align: center;
        }

        /* Hide sidebar's default radio label */
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        brand_lockup()

        st.markdown(
            f"""
            <div class="mr-nav-heading">Workspace</div>
            """,
            unsafe_allow_html=True,
        )

        destination = st.radio(
            "Main navigation",
            options=NAVIGATION,
            format_func=lambda name: (
                f"{NAV_ICONS.get(name, '•')}   {name}"
            ),
            label_visibility="collapsed",
            key="active_destination",
        )

        st.markdown(
            f"""
            <div class="mr-divider"></div>

            <div class="mr-system-panel">
                <div class="mr-system-eyebrow">YOUR WORKSPACE</div>
                <div class="mr-system-title">{BRAND_NAME}</div>
                <div class="mr-system-description">
                    Intelligent model selection and AI-powered
                    tutoring, unified in one workspace.
                </div>
                <div class="mr-system-caption">
                    AI · ROUTING · INTELLIGENCE
                </div>
            </div>

            <div class="mr-sidebar-footer">
                {BRAND_WORDMARK} LEARNING WORKSPACE
            </div>
            """,
            unsafe_allow_html=True,
        )

    return destination