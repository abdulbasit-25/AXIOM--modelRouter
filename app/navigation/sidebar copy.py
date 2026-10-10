
"""Custom desktop sidebar navigation."""

import streamlit as st

from app.config import NAVIGATION, NAV_ICONS
from app.components.branding import brand_lockup


def render_sidebar() -> str:
    """Render the styled sidebar and return its active destination."""

    st.markdown(
        """
        <style>
        /* Sidebar foundation */
        [data-testid="stSidebar"] {
            background: #171c1d;
            border-right: 1px solid #2c423f;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding: 1.5rem 1rem 1rem;
        }

        /* Workspace heading */
        .mr-section-label {
            display: flex;
            align-items: center;
            gap: 9px;
            margin: 2rem 0 0.85rem;
            padding-left: 0.65rem;
            color: #949b96;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 2px;
        }

        .mr-section-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #829191;
        }

        /* Navigation */
        [data-testid="stSidebar"] [role="radiogroup"] {
            gap: 5px;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            position: relative;
            display: flex;
            align-items: center;
            min-height: 44px;
            padding: 0.55rem 0.75rem;
            border: 1px solid transparent;
            border-radius: 8px;
            background: transparent;
            transition: background 150ms ease,
                        border-color 150ms ease;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: #222b2c;
            border-color: #4c5b61;
        }

        /* Hide radio circles but preserve functionality */
        [data-testid="stSidebar"] [role="radiogroup"]
        label > div:first-child {
            display: none;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label p {
            color: #949b96;
            font-size: 13px;
            font-weight: 500;
        }

        /* Active destination */
        [data-testid="stSidebar"] [role="radiogroup"]
        label:has(input:checked) {
            background: #2c423f;
            border-color: #4c5b61;
        }

        [data-testid="stSidebar"] [role="radiogroup"]
        label:has(input:checked) p {
            color: #c5c5c5;
            font-weight: 650;
        }

        [data-testid="stSidebar"] [role="radiogroup"]
        label:has(input:checked)::before {
            content: "";
            position: absolute;
            left: -1px;
            top: 10px;
            bottom: 10px;
            width: 3px;
            border-radius: 0 3px 3px 0;
            background: #829191;
        }

        /* Divider */
        .mr-divider {
            height: 1px;
            margin: 1.25rem 0;
            background: #2c423f;
        }

        /* System status card */
        .mr-status-card {
            padding: 14px;
            border: 1px solid #4c5b61;
            border-radius: 10px;
            background: #202728;
        }

        .mr-status-heading {
            color: #829191;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1.5px;
        }

        .mr-status-title {
            margin-top: 14px;
            color: #c5c5c5;
            font-size: 13px;
            font-weight: 600;
        }

        .mr-status-description {
            margin-top: 6px;
            color: #949b96;
            font-size: 11px;
            line-height: 1.7;
        }

        .mr-status-footer {
            margin-top: 14px;
            padding-top: 10px;
            border-top: 1px solid #4c5b61;
            color: #829191;
            font-size: 10px;
        }

        /* Bottom branding */
        .mr-sidebar-footer {
            margin-top: 1.5rem;
            color: #829191;
            font-size: 9px;
            font-weight: 600;
            letter-spacing: 1.5px;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        brand_lockup()

        st.markdown(
            """
            <div class="mr-section-label">
                <span class="mr-section-dot"></span>
                WORKSPACE
            </div>
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

            <div class="mr-status-card">
                <div class="mr-status-heading">SYSTEM OVERVIEW</div>
                <div class="mr-status-title">Model Router</div>
                <div class="mr-status-description">
                    Intelligent model routing for AI-powered tutoring
                    and query processing.
                </div>
                <div class="mr-status-footer">
                    AI WORKSPACE &nbsp; / &nbsp; MODEL ROUTER
                </div>
            </div>

            <div class="mr-sidebar-footer">
                BUILT FOR INTELLIGENCE
            </div>
            """,
            unsafe_allow_html=True,
        )

    return destination