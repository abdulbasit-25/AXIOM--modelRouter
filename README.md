# EduRoute Model Router

EduRoute is a Streamlit tutoring app integrated with a model-routing backend.
The tutor classifies questions, selects a model, checks the response, escalates
when verification fails, and shows request latency and estimated cost.

## Run locally

1. Create and activate a Python 3.10+ virtual environment.
2. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Optionally set `GROQ_API_KEY` in the environment or in a root `.env` file to
   enable live Groq responses. Without a key, the app uses a clearly labelled
   simulated response.
4. Start the app:

   ```powershell
   python -m streamlit run app/main.py
   ```

The **Fallback Demonstration** scenario intentionally exercises the router's
verification escalation path.

## Calibration and reporting

**Calibration Studio** submits an editable evaluation prompt to the router and
compares its selected tier with the expected tier you choose. Requests are real
router runs and are included in session telemetry.

**SDG Analytics** reports routed requests, recorded latency, model usage, token
cost estimates, and savings versus the configured frontier-model pricing proxy.
The dashboard and downloadable CSV cover the active Streamlit session only;
they are operational proxies, not measured learning, access, or employment
outcomes. Data is held in session memory and is not stored in a database.

## Verify

Run the engine and router checks:

```powershell
python tests/test_engine.py
python tests/test_router.py
```

Run the frontend-to-router integration check:

```powershell
python tests/test_app_integration.py
```
