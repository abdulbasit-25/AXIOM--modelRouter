
"""Light-themed navigation for Model Router."""

import streamlit as st

from app.config import NAVIGATION, NAV_ICONS
from app.components.branding import brand_lockup


def render_sidebar() -> str:
    """Render the sidebar and return the selected destination."""

    st.markdown(
        """
        <style>
        /* ===== SIDEBAR PALETTE ===== */

        [data-testid="stSidebar"] {
            --mr-sidebar-bg: #EAF2EE;
            --mr-sidebar-border: #D3E1DA;
            --mr-sidebar-ink: #203A33;
            --mr-sidebar-muted: #5B7168;
            --mr-sidebar-accent: #17634F;
            background:
                radial-gradient(ellipse at 0% 0%, rgba(73, 137, 108, 0.10), transparent 44%),
                linear-gradient(180deg, #F1F6F3 0%, var(--mr-sidebar-bg) 58%, #E5EEE9 100%);
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
            color: #557267;
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
            background: #DDEBE4;
            border-color: #C6D9CE;
            transform: translateX(2px);
        }

        [data-testid="stSidebar"] [role="radiogroup"]
        [data-testid="stRadioOption"]:hover > div:last-child,
        [data-testid="stSidebar"] [role="radiogroup"]
        [data-testid="stRadioOption"]:hover > div:last-child p {
            color: #174B3D;
        }

        /* Evergreen active state with a small warm accent. */
        [data-testid="stSidebar"] [role="radiogroup"]
        [data-testid="stRadioOption"][data-selected="true"] {
            background: linear-gradient(110deg, #174B3D 0%, #21644F 100%);
            border-color: #174B3D;
            box-shadow: 0 5px 14px rgba(23, 75, 61, 0.18);
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
            background: #D4B56A;
        }

        /* Keyboard accessibility */
        [data-testid="stSidebar"] [role="radiogroup"]
        [data-testid="stRadioOption"]:focus-within {
            outline: 2px solid #43846A;
            outline-offset: 2px;
        }

        /* ===== DIVIDER ===== */

        .mr-divider {
            height: 1px;
            margin: 1.15rem 0;
            background: #CDDDD4;
        }

        /* ===== SYSTEM PANEL ===== */

        .mr-system-panel {
            padding: 16px 14px 14px;
            border: 1px solid #D0E0D7;
            border-radius: 12px;
            background:
                radial-gradient(190px 110px at 100% 0%, rgba(73, 137, 108, 0.10), transparent 75%),
                linear-gradient(145deg, #FFFFFF 0%, #F5F8F5 100%);
            box-shadow: 0 4px 14px rgba(32, 58, 51, 0.045);
        }

        .mr-system-eyebrow {
            color: #39735C;
            font-family: "Segoe UI", sans-serif;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1.4px;
        }

        .mr-system-title {
            margin-top: 12px;
            color: #203A33;
            font-family: "Segoe UI", sans-serif;
            font-size: 14px;
            font-weight: 700;
            letter-spacing: -0.2px;
        }

        .mr-system-description {
            margin-top: 5px;
            color: #5B7168;
            font-family: "Segoe UI", sans-serif;
            font-size: 11px;
            font-weight: 400;
            line-height: 1.7;
        }

        .mr-system-caption {
            margin-top: 14px;
            padding-top: 10px;
            border-top: 1px solid #DCE7E1;
            color: #39735C;
            font-family: "Segoe UI", sans-serif;
            font-size: 9px;
            font-weight: 700;
            letter-spacing: 1px;
        }

        /* ===== FOOTER ===== */

        .mr-sidebar-footer {
            padding: 10px 0 0;
            color: #688076;
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
            """
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
            """
            <div class="mr-divider"></div>

            <div class="mr-system-panel">
                <div class="mr-system-eyebrow">YOUR WORKSPACE</div>
                <div class="mr-system-title">Model Router</div>
                <div class="mr-system-description">
                    Intelligent model selection and AI-powered
                    tutoring, unified in one workspace.
                </div>
                <div class="mr-system-caption">
                    AI · ROUTING · INTELLIGENCE
                </div>
            </div>

            <div class="mr-sidebar-footer">
                MODEL ROUTER WORKSPACE
            </div>
            """,
            unsafe_allow_html=True,
        )

    return destination