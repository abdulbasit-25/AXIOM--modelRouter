# Axiom Rebrand Audit

## Scope and outcome

The active Streamlit application is branded **Axiom — AI eXcellence in Optimized Mentoring**, with the tagline **“Intelligence, routed with purpose.”** The rebrand covers the app metadata, welcome and About content, navigation, shared branding components, palette, page footer, analytics export name, logo assets, developer README, and this audit. Existing destinations, router behavior, model identifiers, and session-state keying are retained.

## Implemented changes

- Added `app/assets/axiom-logo.svg` and `app/assets/axiom-mark.svg` for the sidebar/mobile brand and browser icon.
- Centralized name, expansion, tagline, description, asset paths, page title, and icon in `app/config.py`.
- Centralized the official five-color palette in `app/styles/tokens.py` and updated the shared app styling and sidebar to use it.
- Updated shared branding, navigation labels, the welcome page, About page, app menu/caption, and footer with Axiom identity and accurate prototype messaging.
- Renamed analytics CSV downloads to `axiom-session-report.csv`.
- Updated `README.md` with setup, launch, tests, routing overview, project structure, and known limitations.
- Updated `ENGINE_SPECS_HANDOFF.md` and the engine package description to reflect the current project identity and module organization.
- Extended app integration checks to cover the new branding, SVG assets, and page metadata.

## Validation performed

Using the configured Python 3.13.14 virtual environment:

- `python tests/test_app_integration.py` — passed (all six application integration checks).
- `python tests/test_router.py` — passed (all four routing/fallback scenarios).
- `python -c "... runpy ... tests/test_engine.py ..."` with the Groq client patched off — passed (pricing, mock generation, telemetry, and end-to-end checks).
- `python -m compileall -q app core engine tests` — passed.
- Confirmed both configured SVG asset paths exist; app integration checks additionally validate these paths and the configured page icon.

No live provider API request or production deployment was exercised as part of this audit.

## Current limitations

- The application is a working local prototype, not a persistent multi-user reporting service. Its telemetry is in-memory/session-scoped and is lost when that session ends.
- Cost, baseline, savings, and student-impact values are estimates based on configured rates and proxies; they are not provider invoices, measured educational outcomes, or independently audited savings.
- Calibration checks router tier agreement, not response accuracy or educational effectiveness.
- Response verification uses lightweight heuristics; it is not a comprehensive correctness or safety evaluation.
- Provider availability, quotas, model access, and token limits depend on the configured Groq account. Without a usable provider client, responses use an explicitly labeled local mock path.
- Streamlit's page title, icon, and About menu are configured. Separate Open Graph/social metadata is not implemented.
- No production hosting, persistent database, centralized secret management, or monitoring integration is included.

## Historical references retained

- `AUDIT.md` is a dated historical audit of the earlier EduRoute incarnation. It is retained as a historical record and was not rewritten or treated as current Axiom product documentation.
- `HANDOFF_PERSON_3.md` is an earlier handoff artifact and may contain obsolete naming or paths. It was not rewritten because it records historical handoff context.
- `app/navigation/sidebar copy.py` is an unused copy containing earlier Model Router UI content. The active navigation imports `app/navigation/sidebar.py`; the stray copy was left untouched rather than removed as unrelated cleanup.
- Model identifiers and the Groq API environment variable remain unchanged because these are backend integration configuration, not user-facing brand identity.

## Audit conclusion

The active application surfaces and README now present a consistent Axiom identity without implying that session telemetry is persistent or that a live provider is always available. The brand assets and local test suite validate in the configured development environment. The backend remains a prototype integration with the limitations listed above.
