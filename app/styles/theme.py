"""Shared visual styling for the Axiom Streamlit app.

Design notes
------------
* Tokens live on :root so colours, radii and shadows are changed in one place.
* Layout is responsive at two breakpoints: <= 1000px (tablet) and <= 820px
  (phone / small tablet). At <= 820px the sidebar is replaced by a sticky top
  bar with a Menu (hamburger) button that opens a navigation sheet.
* Streamlit containers created with ``st.container(key="x")`` expose a
  ``.st-key-x`` class, which is how the layout hooks below target them.
"""

from app.styles.tokens import CSS_VARIABLES


APP_CSS = (
    "<style>"
    + CSS_VARIABLES
    + """
    /* 2. App shell */
    html, body, .stApp {
        font-family: Inter, "Segoe UI", system-ui, -apple-system, sans-serif;
        -webkit-font-smoothing: antialiased;
    }

    .stApp {
        color-scheme: light;
        color: var(--text);
        background:
            radial-gradient(1000px 430px at 88% -8%, rgba(130, 145, 145, 0.10), transparent 62%),
            var(--bg) !important;
    }

    [data-testid="stMainBlockContainer"],
    .main .block-container {
        max-width: 1200px;
        padding: 3rem 2rem 3rem;
        animation: rise 0.4s var(--ease) both;
    }

    [data-testid="stHeader"] { background: transparent; }
    footer { visibility: hidden; }

    [data-testid="stSidebar"] {
        background: var(--sidebar);
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] .block-container,
    [data-testid="stSidebarUserContent"] { padding-top: 1.6rem; }

    hr, [data-testid="stHorizontalRule"] { border-color: var(--border) !important; }

    @keyframes rise {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: none; }
    }

    /* 3. Typography */
    h1, h2, h3, h4,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: var(--text) !important;
        letter-spacing: -0.035em;
        margin-top: 0;
    }

    h1 {
        font-size: clamp(2rem, 1.35rem + 2.6vw, 3rem) !important;
        line-height: 1.08 !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
        padding: 0 !important;
    }

    h3 { font-size: 1.35rem; line-height: 1.3; }
    h4 { font-size: 1.1rem; line-height: 1.4; }

    label, .stMarkdown p, .stMarkdown li { color: var(--text); }

    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p,
    .stCaption { color: var(--text-3) !important; }

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        color: var(--brand-secondary) !important;
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.7rem;
    }

    .eyebrow::before {
        content: "";
        width: 1.4rem;
        height: 2px;
        border-radius: 2px;
        background: var(--accent);
    }

    .page-intro {
        color: var(--text-2) !important;
        font-size: 1.05rem;
        line-height: 1.7;
        max-width: 68ch;
        margin: 0.4rem 0 1.8rem;
    }

    .section-heading { margin-top: 2.4rem !important; margin-bottom: 0.2rem !important; }

    /* 4. Brand and sidebar */
    .brand-shell {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        padding: 0.35rem 0.1rem 1.25rem;
        margin-bottom: 1.05rem;
        border-bottom: 1px solid var(--border);
    }

    .brand-mark, .mini-brand-mark, .team-mark {
        display: grid;
        place-items: center;
        flex: 0 0 auto;
        border-radius: 0.8rem;
        background: var(--brand-primary);
        color: #ffffff;
        font-weight: 700;
        box-shadow: var(--shadow-sm);
    }

    .brand-mark { width: 2.7rem; height: 2.7rem; font-size: 1.15rem; }
    .mini-brand-mark { width: 2.1rem; height: 2.1rem; font-size: 1rem; border-radius: 0.7rem; }
    .team-mark { width: 2.5rem; height: 2.5rem; font-size: 1rem; }

    .brand-name {
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: -0.04em;
        line-height: 1.1;
        color: var(--text) !important;
    }

    .brand-tagline { font-size: 0.78rem; color: var(--text-2) !important; margin-top: 0.22rem; }

    [data-testid="stSidebar"] .brand-mark {
        width: 2.9rem;
        height: 2.9rem;
        border-radius: 0.95rem;
        box-shadow: 0 5px 14px rgba(44, 66, 63, 0.14);
    }

    .mr-workspace-label, .sidebar-meta, .panel-heading, .insight-label,
    .metric-label, .about-kicker {
        color: var(--text-2) !important;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .mr-workspace-label {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin: 0.25rem 0 0.7rem;
        padding-left: 0.25rem;
    }

    .mr-label-dot {
        width: 0.42rem;
        height: 0.42rem;
        border-radius: 50%;
        background: var(--accent);
        box-shadow: 0 0 0 3px rgba(130, 145, 145, 0.18);
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] > label { display: none; }

    [data-testid="stSidebar"] [role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
    }

    [data-testid="stSidebar"] [data-testid="stRadioOption"] {
        width: 100%;
        margin: 0;
        min-height: 2.9rem;
        padding: 0.68rem 0.85rem;
        border: 1px solid transparent;
        border-radius: 0.85rem;
        background: transparent;
        cursor: pointer;
        transition: background 0.18s var(--ease), border-color 0.18s var(--ease), color 0.18s var(--ease), transform 0.18s var(--ease), box-shadow 0.18s var(--ease);
    }

    [data-testid="stSidebar"] [data-testid="stRadioOption"] > span:first-child { display: none; }

    [data-testid="stSidebar"] [data-testid="stRadioOption"] > div:last-child {
        display: flex;
        align-items: center;
        width: 100%;
        color: var(--text) !important;
        font-weight: 600;
        font-size: 0.9rem;
        line-height: 1.35;
        margin: 0;
    }

    [data-testid="stSidebar"] [data-testid="stRadioOption"]:hover {
        background: rgba(255, 255, 255, 0.82);
        border-color: var(--border);
        transform: translateX(3px);
    }

    [data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected="true"] {
        background: var(--brand-primary);
        border-color: transparent;
        box-shadow: 0 5px 14px rgba(44, 66, 63, 0.14);
    }

    [data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected="true"] > div:last-child,
    [data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected="true"] > div:last-child * {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadioOption"]:focus-within {
        outline: 3px solid rgba(130, 145, 145, 0.42);
        outline-offset: 2px;
    }

    .mr-sidebar-spacer { height: 1.2rem; }

    .mr-sidebar-divider {
        height: 1px;
        margin: 0.15rem 0 1.1rem;
        background: var(--border);
    }

    .mr-engine-card {
        padding: 1rem 1.05rem 0.9rem;
        border: 1px solid rgba(130, 145, 145, 0.3);
        border-radius: 1rem;
        background: rgba(255, 255, 255, 0.86);
        box-shadow: var(--shadow-sm);
    }

    .mr-engine-header, .mr-engine-footer {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .mr-engine-header { margin-bottom: 0.8rem; }

    .mr-engine-indicator {
        width: 0.48rem;
        height: 0.48rem;
        border-radius: 50%;
        background: var(--brand-primary);
        box-shadow: 0 0 0 3px rgba(130, 145, 145, 0.18);
    }

    .mr-engine-title {
        color: var(--text-2);
        font-size: 0.65rem;
        font-weight: 750;
        letter-spacing: 0.11em;
    }

    .mr-engine-live {
        margin-left: auto;
        padding: 0.18rem 0.45rem;
        border: 1px solid rgba(130, 145, 145, 0.34);
        border-radius: var(--r-pill);
        background: rgba(130, 145, 145, 0.12);
        color: var(--brand-primary);
        font-size: 0.6rem;
        font-weight: 750;
        letter-spacing: 0.08em;
    }

    .mr-engine-name {
        color: var(--text);
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }

    .mr-engine-description {
        margin-top: 0.28rem;
        color: var(--text-2);
        font-size: 0.76rem;
        line-height: 1.5;
    }

    .mr-engine-footer {
        justify-content: space-between;
        margin-top: 0.85rem;
        padding-top: 0.7rem;
        border-top: 1px solid var(--border);
        color: var(--text-3);
        font-size: 0.7rem;
    }

    .mr-engine-ready { color: var(--brand-primary); font-weight: 700; }

    .mr-sidebar-footer {
        display: flex;
        justify-content: space-between;
        gap: 0.5rem;
        margin-top: 0.9rem;
        color: var(--text-3);
        font-size: 0.58rem;
        font-weight: 700;
        letter-spacing: 0.1em;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        border-radius: var(--r-pill);
        border: 1px solid var(--warn-border);
        background: var(--warn-bg);
        color: var(--warn-text);
        font-size: 0.76rem;
        font-weight: 700;
        padding: 0.45rem 0.8rem;
    }

    .status-dot {
        width: 0.55rem;
        height: 0.55rem;
        border-radius: 50%;
        background: var(--gold);
        box-shadow: 0 0 0 4px rgba(130, 145, 145, 0.2);
    }

    /* 5. Cards and panels */
    .insight-card, .status-card, .metric-card, .feature-card,
    .about-section, .overview-panel, .welcome-visual, .page-footer {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--r-lg);
        box-shadow: var(--shadow-sm);
    }

    .insight-card, .status-card, .feature-card,
    .overview-panel, .about-section, .metric-card, .welcome-visual { padding: 1.3rem 1.35rem; }

    .status-card { background: var(--sidebar); }
    .about-section { margin-top: 1rem; }
    .overview-panel { margin-top: 0.8rem; }

    .insight-card p, .status-card p, .feature-card p,
    .overview-panel p, .about-section p, .metric-note, .step-list,
    .step-list li, .team-copy, .hero-copy p, .result-placeholder, .route-note {
        color: var(--text-3) !important;
        font-size: 0.96rem;
        line-height: 1.7;
        margin: 0;
    }

    .insight-label, .metric-label, .about-kicker { margin-bottom: 0.7rem; }

    .metric-card { min-height: 130px; }

    .metric-value {
        color: var(--brand-secondary) !important;
        font-size: 1.9rem;
        font-weight: 700;
        line-height: 1.2;
        letter-spacing: -0.05em;
    }

    .metric-note { margin-top: 0.55rem; font-size: 0.88rem; }

    .chip {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.35rem 0.75rem;
        border-radius: var(--r-pill);
        background: var(--primary-soft);
        border: 1px solid var(--brand-neutral);
        color: var(--primary) !important;
        font-size: 0.78rem;
        font-weight: 700;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid var(--border);
        border-radius: var(--r-lg);
        background: var(--surface);
        box-shadow: var(--shadow-sm);
        padding: 0.35rem;
    }

    /* 6. Welcome page */
    .mini-brand { display: flex; align-items: center; gap: 0.7rem; margin-bottom: 1.1rem; }
    .mini-brand-text, .feature-title { color: var(--text) !important; }
    .mini-brand-text { font-weight: 700; letter-spacing: -0.03em; }

    .hero-copy { padding: 0.4rem 0 0.8rem; }

    .hero-text {
        color: var(--text) !important;
        font-size: clamp(1.9rem, 1.2rem + 2.6vw, 3rem);
        font-weight: 700;
        line-height: 1.1;
        letter-spacing: -0.05em;
        max-width: 560px;
        margin-bottom: 0.9rem;
    }

    .hero-copy p { font-size: 1.04rem; max-width: 620px; }

    .welcome-visual {
        min-height: 290px;
        display: flex;
        align-items: center;
        background: var(--sidebar);
    }

    .visual-window {
        width: 100%;
        min-height: 220px;
        padding: 1rem;
        border-radius: 1.2rem;
        background: #ffffff;
        border: 1px solid var(--border);
        position: relative;
        overflow: hidden;
    }

    .visual-badge {
        display: inline-flex;
        border-radius: var(--r-pill);
        background: rgba(44, 66, 63, 0.08);
        border: 1px solid var(--border);
        color: var(--text-2);
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 0.36rem 0.7rem;
    }

    .visual-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.8rem;
        margin-top: 1rem;
    }

    .visual-card {
        min-height: 72px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 0.9rem;
        background: #ffffff;
        border: 1px solid var(--border);
        color: var(--text);
        font-weight: 600;
        letter-spacing: -0.02em;
        animation: float 6s ease-in-out infinite;
    }

    .visual-card:nth-child(2) { animation-delay: -1.5s; }
    .visual-card:nth-child(3) { animation-delay: -3s; }
    .visual-card:nth-child(4) { animation-delay: -4.5s; }
    .visual-card.primary { background: var(--primary-soft); border-color: rgba(44, 66, 63, 0.22); color: var(--primary); }
    .visual-card.muted { background: var(--sidebar); }

    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50%      { transform: translateY(-4px); }
    }

    .feature-card {
        min-height: 13rem;
        display: flex;
        flex-direction: column;
        margin-bottom: 0.6rem;
        transition: transform 0.2s var(--ease), box-shadow 0.2s var(--ease), border-color 0.2s var(--ease);
    }

    .feature-card:hover { transform: translateY(-3px); border-color: var(--accent); box-shadow: var(--shadow-md); }

    .feature-icon {
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 0.8rem;
        background: var(--primary-soft);
        color: var(--primary);
        display: grid;
        place-items: center;
        font-weight: 700;
        margin-bottom: 0.9rem;
    }

    .feature-title {
        font-size: 1.15rem;
        font-weight: 700;
        line-height: 1.35;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }

    .step-list { padding-left: 0; margin: 0.4rem 0 0; list-style: none; counter-reset: step; }

    .step-list li {
        position: relative;
        counter-increment: step;
        padding: 0.15rem 0 0.15rem 2.5rem;
        margin-bottom: 0.9rem;
        min-height: 1.9rem;
    }

    .step-list li::before {
        content: counter(step);
        position: absolute;
        left: 0;
        top: 0.05rem;
        width: 1.8rem;
        height: 1.8rem;
        display: grid;
        place-items: center;
        border-radius: 50%;
        background: var(--primary-soft);
        color: var(--primary);
        font-size: 0.8rem;
        font-weight: 700;
    }

    .step-list li strong { color: var(--text) !important; }

    .team-placeholder {
        display: flex;
        align-items: center;
        gap: 0.9rem;
        background: var(--sidebar);
        border: 1px dashed var(--border-strong);
        border-radius: var(--r-md);
        padding: 1rem 1.1rem;
    }

    .team-copy { font-weight: 500; }

    .st-key-team_grid [data-testid="stHorizontalBlock"] {
        align-items: stretch;
        gap: 1rem;
    }

    .team-card {
        position: relative;
        display: flex;
        height: 100%;
        min-height: 12rem;
        flex-direction: column;
        align-items: flex-start;
        justify-content: center;
        overflow: hidden;
        padding: 1.5rem;
        border: 1px solid var(--border);
        border-radius: var(--r-lg);
        background:
            radial-gradient(circle at 100% 0%, rgba(130, 145, 145, 0.14), transparent 42%),
            var(--surface);
        box-shadow: var(--shadow-sm);
        transition: transform 180ms var(--ease), box-shadow 180ms var(--ease),
                    border-color 180ms var(--ease);
    }

    .team-card::after {
        position: absolute;
        right: -1.7rem;
        bottom: -2.2rem;
        width: 6rem;
        height: 6rem;
        border: 1px solid rgba(130, 145, 145, 0.2);
        border-radius: 50%;
        content: "";
        transition: transform 220ms var(--ease);
    }

    .team-card:hover {
        transform: translateY(-5px);
        border-color: var(--brand-accent);
        box-shadow: var(--shadow-md);
    }

    .team-card:hover::after { transform: scale(1.28); }

    .team-avatar {
        display: grid;
        width: 3.25rem;
        height: 3.25rem;
        place-items: center;
        margin-bottom: 1.2rem;
        border: 1px solid rgba(130, 145, 145, 0.34);
        border-radius: 1rem;
        background: linear-gradient(145deg, var(--primary-soft), #ffffff);
        color: var(--brand-primary);
        font-size: 1rem;
        font-weight: 750;
        letter-spacing: 0.04em;
        box-shadow: 0 5px 14px rgba(44, 66, 63, 0.08);
        transition: transform 180ms var(--ease);
    }

    .team-card:hover .team-avatar { transform: rotate(-4deg) scale(1.04); }

    .team-name {
        margin: 0 0 0.5rem !important;
        color: var(--text) !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
        line-height: 1.35 !important;
    }

    .team-role {
        display: inline-flex;
        align-items: center;
        min-height: 1.8rem;
        padding: 0.3rem 0.7rem;
        border: 1px solid var(--border);
        border-radius: var(--r-pill);
        background: var(--sidebar);
        color: var(--text-2);
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 0.025em;
    }

    @media (prefers-reduced-motion: reduce) {
        .team-card, .team-avatar, .team-card::after { transition: none; }
    }

    .page-footer {
        margin-top: 2.2rem;
        padding: 1rem 1.2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }

    .footer-brand { display: flex; align-items: center; gap: 0.7rem; }
    .footer-tagline { font-size: 0.78rem; color: var(--text-2) !important; margin-top: 0.14rem; }
    .footer-links { display: flex; flex-wrap: wrap; gap: 0.5rem; }

    /* 7. Buttons */
    .stButton > button, .stDownloadButton > button {
        border: 1px solid var(--border-strong);
        border-radius: var(--r-pill);
        background: var(--surface);
        color: var(--text) !important;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        min-height: 2.9rem;
        box-shadow: none;
        transition: border-color 0.18s var(--ease), transform 0.18s var(--ease),
                    background 0.18s var(--ease), box-shadow 0.18s var(--ease);
    }

    .stButton > button p, .stDownloadButton > button p { color: inherit !important; font-weight: 600; }

    .stButton > button:hover { border-color: var(--primary); transform: translateY(-1px); box-shadow: var(--shadow-sm); }
    .stButton > button:active { transform: translateY(0); }

    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        border-color: var(--primary);
        background: var(--primary);
        color: #ffffff !important;
        box-shadow: var(--shadow-sm);
    }

    .stButton > button[kind="primary"] p,
    .stButton > button[data-testid="stBaseButton-primary"] p { color: #ffffff !important; }

    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover {
        background: var(--primary-strong);
        border-color: var(--primary-strong);
        box-shadow: var(--shadow-md);
    }

    /* Scenario picker: buttons become selectable cards */
    .st-key-scenario_grid .stButton > button {
        border-radius: var(--r-md);
        min-height: 5.4rem;
        padding: 1rem 1.15rem;
        justify-content: flex-start;
        align-items: flex-start;
        text-align: left;
        white-space: normal;
    }

    .st-key-scenario_grid .stButton > button > div,
    .st-key-scenario_grid .stButton > button [data-testid="stMarkdownContainer"] {
        width: 100%;
        text-align: left;
    }

    .st-key-scenario_grid .stButton > button p {
        text-align: left;
        line-height: 1.5;
        font-weight: 500;
        color: var(--text-3) !important;
    }

    .st-key-scenario_grid .stButton > button p strong { color: var(--text); font-weight: 700; font-size: 1rem; }

    .st-key-scenario_grid .stButton > button[kind="primary"],
    .st-key-scenario_grid .stButton > button[data-testid="stBaseButton-primary"] {
        background: var(--primary-soft);
        border: 1.5px solid var(--primary);
        box-shadow: 0 0 0 4px rgba(130, 145, 145, 0.24);
    }

    .st-key-scenario_grid .stButton > button[kind="primary"] p,
    .st-key-scenario_grid .stButton > button[data-testid="stBaseButton-primary"] p { color: var(--text-2) !important; }

    .st-key-scenario_grid .stButton > button[kind="primary"] p strong,
    .st-key-scenario_grid .stButton > button[data-testid="stBaseButton-primary"] p strong { color: var(--primary-strong) !important; }

    /* 8. Inputs */
    .stTextInput > div > div, .stTextArea > div > div,
    .stSelectbox > div > div, .stNumberInput > div > div {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: var(--r-md);
    }

    [data-testid="stTextArea"] textarea, [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input {
        background: #ffffff !important;
        color: var(--text) !important;
        border-radius: var(--r-md);
        line-height: 1.6;
        font-size: 1rem;
    }

    [data-testid="stTextArea"] textarea { min-height: 140px; }

    [data-testid="stTextArea"] textarea::placeholder,
    [data-testid="stTextInput"] input::placeholder { color: var(--text-3) !important; }

    [data-testid="stTextArea"] > div > div:focus-within {
        border-color: var(--accent);
        box-shadow: 0 0 0 3px rgba(130, 145, 145, 0.3);
    }

    button:focus-visible, [role="radio"]:focus-visible {
        outline: 2px solid var(--accent) !important;
        outline-offset: 2px !important;
    }

    .composer-meta { display: flex; justify-content: flex-end; align-items: center; min-height: 2.9rem; }

    [data-testid="stAlert"], .stAlert {
        border-radius: var(--r-md);
        border: 1px solid var(--warn-border);
        background: var(--warn-bg) !important;
        color: var(--warn-text) !important;
    }

    [data-testid="stAlert"] p, [data-testid="stAlert"] div, [data-testid="stAlert"] strong { color: var(--warn-text) !important; }

    /* 9. Empty state and routing timeline */
    .empty-state {
        display: grid;
        justify-items: center;
        align-content: center;
        gap: 0.5rem;
        min-height: 170px;
        text-align: center;
        padding: 1.1rem 0.8rem;
        border: 1.5px dashed var(--border-strong);
        border-radius: var(--r-md);
        background: repeating-linear-gradient(135deg, transparent 0 10px, rgba(44, 66, 63, 0.025) 10px 20px);
    }

    .empty-icon {
        display: grid;
        place-items: center;
        width: 3rem;
        height: 3rem;
        border-radius: 50%;
        background: var(--sidebar);
        border: 1px solid var(--border);
        color: var(--text);
        font-size: 1.3rem;
    }

    .empty-title { color: var(--text) !important; font-size: 1rem; font-weight: 700; }
    .panel-heading { margin-bottom: 0.9rem; }

    .route { display: flex; flex-direction: column; margin-top: 0.2rem; }
    .route-step { position: relative; display: flex; align-items: flex-start; gap: 0.85rem; padding-bottom: 1.05rem; }
    .route-step:not(.is-live) { opacity: 0.7; }

    .route-step:not(:last-child)::before {
        content: "";
        position: absolute;
        left: 0.94rem;
        top: 2rem;
        bottom: 0.1rem;
        width: 2px;
        background: var(--border);
    }

    .route-node {
        flex: 0 0 1.9rem;
        height: 1.9rem;
        display: grid;
        place-items: center;
        border-radius: 50%;
        background: var(--sidebar);
        border: 1px solid var(--border-strong);
        color: var(--text-2);
        font-size: 0.8rem;
        font-weight: 700;
    }

    .route-step.is-live .route-node { background: var(--primary); border-color: var(--primary); color: #ffffff; }
    .route-title { color: var(--text) !important; font-size: 0.95rem; font-weight: 700; line-height: 1.9rem; }
    .route-hint { color: var(--text-3) !important; font-size: 0.84rem; line-height: 1.5; margin-top: -0.2rem; }
    .route-note { font-size: 0.82rem; margin-top: 0.3rem; }

    /* 10. Mobile top bar + hamburger (hidden on desktop) */
    .st-key-mobile_nav { display: none; }

    .mobile-brand {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-weight: 700;
        font-size: 1.15rem;
        letter-spacing: -0.03em;
        color: var(--text);
    }

    .mobile-brand-name {
        color: var(--brand-primary);
        font-size: 0.95rem;
        font-weight: 750;
        letter-spacing: 0.12em;
    }

    div[role="dialog"] { border-radius: var(--r-lg); background: var(--bg); }
    div[role="dialog"] .stButton > button { justify-content: flex-start; min-height: 3.1rem; }

    /* 11. Responsive */
    @media (max-width: 1000px) {
        .st-key-features [data-testid="stHorizontalBlock"] { flex-wrap: wrap; gap: 1rem; }

        .st-key-features [data-testid="stColumn"],
        .st-key-features [data-testid="column"] {
            flex: 1 1 calc(50% - 1rem) !important;
            min-width: calc(50% - 1rem) !important;
        }
    }

    @media (max-width: 820px) {
        [data-testid="stSidebar"],
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="stExpandSidebarButton"],
        [data-testid="collapsedControl"],
        [data-testid="stHeader"] { display: none !important; }

        [data-testid="stMainBlockContainer"],
        .main .block-container { padding: 0.9rem 1rem 2.5rem; }

        .st-key-mobile_nav {
            display: flex !important;
            flex-direction: row !important;
            align-items: center;
            justify-content: space-between;
            gap: 0.75rem;
            position: sticky;
            top: 0;
            z-index: 100;
            margin: 0 -1rem 1.2rem;
            padding: 0.6rem 1rem;
            background: rgba(246, 244, 239, 0.92);
            -webkit-backdrop-filter: blur(10px);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--border);
        }

        .st-key-mobile_nav > * { width: auto !important; flex: 0 0 auto; }

        .st-key-mobile_nav .stButton > button {
            min-height: 2.75rem;
            padding: 0.45rem 1rem;
            background: var(--primary);
            border-color: var(--primary);
            color: #ffffff !important;
        }

        .st-key-mobile_nav .stButton > button p { color: #ffffff !important; }

        [data-testid="stMain"] [data-testid="stHorizontalBlock"] { flex-wrap: wrap; gap: 1rem; }

        [data-testid="stMain"] [data-testid="stColumn"],
        [data-testid="stMain"] [data-testid="column"] {
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }

        .st-key-composer_actions [data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: 0.75rem; }

        .st-key-composer_actions [data-testid="stColumn"],
        .st-key-composer_actions [data-testid="column"] { flex: 1 1 auto !important; min-width: 0 !important; }

        .st-key-composer_actions [data-testid="stColumn"]:first-child,
        .st-key-composer_actions [data-testid="column"]:first-child { flex: 0 0 auto !important; }

        .welcome-visual { min-height: 0; }
        .page-footer { flex-direction: column; align-items: flex-start; }
        .feature-card { min-height: 0; }
    }

    @media (max-width: 520px) {
        .page-intro { font-size: 1rem; }

        .insight-card, .status-card, .feature-card,
        .overview-panel, .about-section, .metric-card, .welcome-visual { padding: 1.1rem; }

        .stButton > button { width: 100%; }
        .st-key-mobile_nav .stButton > button,
        .st-key-composer_actions .stButton > button { width: auto; }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
            scroll-behavior: auto !important;
        }
    }
    
</style>
"""
)


def apply_theme() -> None:
    """Install the shared application CSS in the current Streamlit run."""
    import streamlit as st

    st.markdown(APP_CSS, unsafe_allow_html=True)