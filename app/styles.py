"""Shared visual styling for the EduRoute Streamlit app.

Design notes
------------
* Tokens live on :root so colours, radii and shadows are changed in one place.
* Layout is responsive at two breakpoints: <= 1000px (tablet) and <= 820px
  (phone / small tablet). At <= 820px the sidebar is replaced by a sticky top
  bar with a Menu (hamburger) button that opens a navigation sheet.
* Streamlit containers created with ``st.container(key="x")`` expose a
  ``.st-key-x`` class, which is how the layout hooks below target them.
"""

APP_CSS = """
<style>
    /* 1. Tokens */
    :root {
        --bg: #f6f4ef;
        --surface: #ffffff;
        --sidebar: #edf1ef;
        --border: #e1dfd8;
        --border-strong: #cdcac0;
        --primary: #2c4a44;
        --primary-strong: #1b322d;
        --primary-soft: #e1eee9;
        --accent: #3f7a6d;
        --gold: #c79a2e;
        --text: #182226;
        --text-2: #41525a;
        --text-3: #566469;
        --warn-bg: #f8f0da;
        --warn-text: #5c4813;
        --warn-border: #e8d8a6;
        --r-md: 1rem;
        --r-lg: 1.4rem;
        --r-pill: 999px;
        --shadow-sm: 0 1px 2px rgba(24, 34, 38, 0.04), 0 4px 12px rgba(24, 34, 38, 0.04);
        --shadow-md: 0 2px 4px rgba(24, 34, 38, 0.05), 0 14px 30px rgba(24, 34, 38, 0.09);
        --ease: cubic-bezier(0.2, 0.7, 0.2, 1);
    }

    /* 2. App shell */
    html, body, .stApp {
        font-family: Inter, "Segoe UI", system-ui, -apple-system, sans-serif;
        -webkit-font-smoothing: antialiased;
    }

    .stApp {
        color-scheme: light;
        color: var(--text);
        background:
            radial-gradient(1100px 480px at 88% -8%, rgba(63, 122, 109, 0.12), transparent 60%),
            radial-gradient(800px 400px at -5% 12%, rgba(199, 154, 46, 0.07), transparent 60%),
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
        color: var(--accent) !important;
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
    .brand-shell { display: flex; align-items: center; gap: 0.8rem; padding: 0.1rem 0 0.9rem; }

    .brand-mark, .mini-brand-mark, .team-mark {
        display: grid;
        place-items: center;
        flex: 0 0 auto;
        border-radius: 0.8rem;
        background: linear-gradient(145deg, var(--primary) 0%, var(--accent) 140%);
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

    .brand-tagline { font-size: 0.78rem; color: var(--text-2) !important; margin-top: 0.15rem; }

    .sidebar-section-label, .sidebar-meta, .panel-heading, .insight-label,
    .metric-label, .plan-kicker, .about-kicker {
        color: var(--text-2) !important;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .sidebar-section-label, .sidebar-meta { margin: 0.4rem 0 0.7rem; }

    [data-testid="stSidebar"] [data-testid="stRadio"] > label { display: none; }

    [data-testid="stSidebar"] [role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
    }

    [data-testid="stSidebar"] label[data-baseweb="radio"] {
        width: 100%;
        margin: 0;
        padding: 0.75rem 0.95rem;
        border: 1px solid transparent;
        border-radius: var(--r-md);
        background: transparent;
        cursor: pointer;
        transition: background 0.18s var(--ease), border-color 0.18s var(--ease), transform 0.18s var(--ease);
    }

    [data-testid="stSidebar"] label[data-baseweb="radio"] > div:first-child { display: none; }

    [data-testid="stSidebar"] label[data-baseweb="radio"] p {
        color: var(--text) !important;
        font-weight: 600;
        font-size: 0.95rem;
    }

    [data-testid="stSidebar"] label[data-baseweb="radio"]:hover {
        background: rgba(255, 255, 255, 0.75);
        border-color: var(--border);
        transform: translateX(2px);
    }

    [data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) {
        background: var(--primary);
        border-color: var(--primary);
        box-shadow: var(--shadow-sm);
    }

    [data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) p,
    [data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) div {
        color: #ffffff !important;
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
        box-shadow: 0 0 0 4px rgba(199, 154, 46, 0.18);
    }

    /* 5. Cards and panels */
    .insight-card, .status-card, .plan-card, .metric-card, .feature-card,
    .about-section, .overview-panel, .welcome-visual, .page-footer {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--r-lg);
        box-shadow: var(--shadow-sm);
    }

    .insight-card, .status-card, .plan-card, .feature-card,
    .overview-panel, .about-section, .metric-card, .welcome-visual { padding: 1.3rem 1.35rem; }

    .status-card { background: var(--sidebar); }
    .about-section { margin-top: 1rem; }
    .overview-panel { margin-top: 0.8rem; }

    .insight-card p, .status-card p, .plan-card p, .feature-card p,
    .overview-panel p, .about-section p, .metric-note, .step-list,
    .step-list li, .team-copy, .hero-copy p, .result-placeholder, .route-note {
        color: var(--text-3) !important;
        font-size: 0.96rem;
        line-height: 1.7;
        margin: 0;
    }

    .insight-label, .metric-label, .plan-kicker, .about-kicker { margin-bottom: 0.7rem; }

    .plan-card h4 { margin: 0 0 0.6rem; font-size: 1.15rem; }

    .plan-badge, .planning-pill {
        display: inline-flex;
        align-items: center;
        border-radius: var(--r-pill);
        background: #edf3ef;
        border: 1px solid #cfe1d8;
        color: var(--primary) !important;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 0.34rem 0.7rem;
    }

    .plan-badge { margin-top: 1rem; }

    .planning-banner {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        padding: 0.95rem 1.1rem;
        background: var(--warn-bg);
        border: 1px solid var(--warn-border);
        border-radius: var(--r-md);
        font-size: 0.95rem;
        line-height: 1.5;
        margin: 0.8rem 0 1.6rem;
    }

    .planning-banner span { color: var(--warn-text) !important; }

    .metric-card { min-height: 130px; }

    .metric-value {
        color: #8a969a !important;
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
        border: 1px solid #c9ddd5;
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
        background: linear-gradient(160deg, #ffffff 0%, #f3f6f4 100%);
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
        background: rgba(44, 74, 68, 0.08);
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
    .visual-card.primary { background: var(--primary-soft); border-color: rgba(44, 74, 68, 0.22); color: var(--primary); }
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
        box-shadow: 0 0 0 4px rgba(63, 122, 109, 0.14);
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
        box-shadow: 0 0 0 3px rgba(63, 122, 109, 0.18);
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
        background: repeating-linear-gradient(135deg, transparent 0 10px, rgba(44, 74, 68, 0.025) 10px 20px);
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
        .page-footer, .planning-banner { flex-direction: column; align-items: flex-start; }
        .feature-card { min-height: 0; }
    }

    @media (max-width: 520px) {
        .page-intro { font-size: 1rem; }

        .insight-card, .status-card, .plan-card, .feature-card,
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