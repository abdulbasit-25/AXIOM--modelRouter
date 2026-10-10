"""Shared CSS design tokens used by the application theme."""

BRAND_COLORS = {
    "primary": "#2C423F",
    "secondary": "#4C5B61",
    "accent": "#829191",
    "muted": "#949B96",
    "neutral": "#C5C5C5",
}

CSS_VARIABLES = f"""
    :root {{
        --brand-primary: {BRAND_COLORS["primary"]};
        --brand-secondary: {BRAND_COLORS["secondary"]};
        --brand-accent: {BRAND_COLORS["accent"]};
        --brand-muted: {BRAND_COLORS["muted"]};
        --brand-neutral: {BRAND_COLORS["neutral"]};
        --bg: #f6f4ef;
        --surface: #ffffff;
        --sidebar: #F0F2F1;
        --border: var(--brand-neutral);
        --border-strong: var(--brand-muted);
        --primary: var(--brand-primary);
        --primary-strong: var(--brand-primary);
        --primary-soft: #E8ECEB;
        --accent: var(--brand-accent);
        --gold: var(--brand-accent);
        --text: var(--brand-primary);
        --text-2: var(--brand-secondary);
        --text-3: var(--brand-secondary);
        --warn-bg: #F0F2F1;
        --warn-text: var(--brand-secondary);
        --warn-border: var(--brand-neutral);
        --r-md: 1rem;
        --r-lg: 1.4rem;
        --r-pill: 999px;
        --shadow-sm: 0 1px 2px rgba(24, 34, 38, 0.04), 0 4px 12px rgba(24, 34, 38, 0.04);
        --shadow-md: 0 2px 4px rgba(24, 34, 38, 0.05), 0 14px 30px rgba(24, 34, 38, 0.09);
        --ease: cubic-bezier(0.2, 0.7, 0.2, 1);
    }}
"""
