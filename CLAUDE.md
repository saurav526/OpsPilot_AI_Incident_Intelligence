# OpsPilot AI — Incident Intelligence & Resolution Copilot

Portfolio project: anomaly detection, runbook retrieval, a tool-using incident
assistant, FastAPI REST API, Streamlit dashboard, SQLite audit log.
Uses synthetic telemetry. No production actions are ever executed.

## Commands
- Setup: `pip install -r requirements.txt` (Python 3.11, use a .venv)
- Train: `python scripts/train.py`
- Evaluate: `python scripts/evaluate.py`
- Test: `pytest -q`
- Dashboard: `streamlit run app/streamlit_app.py` (http://localhost:8501)
- API: `uvicorn api.main:app --reload` (docs at http://127.0.0.1:8000/docs)

## Architecture
- `src/data.py` – data loading and summary
- `src/model.py` – StandardScaler + Isolation Forest
- `src/rag.py` – TF-IDF / cosine-similarity runbook retrieval (knowledge_base/)
- `src/agent.py` – metrics + anomaly + retrieval tools; optional Groq generation, deterministic local fallback
- `src/db.py` – SQLite audit log
- `api/main.py` – routes: /health, /metrics/summary, /anomalies, /investigate, /audit/recent
- `app/streamlit_app.py` – dashboard
- `data/`, `reports/`, `knowledge_base/` – telemetry, outputs, runbooks

## Conventions
- Keep the agent read-only: recommend checks, never perform write actions.
- The app must work with no GROQ_API_KEY (local fallback).
- Never read, print, or commit `.env`. Config goes through `.env.example`.
- Anomaly scores prioritise investigation; do not claim they prove root cause.
- Add or update tests in `tests/` for any change in `src/` or `api/`.

## Known limitations
Synthetic data, lexical retrieval, simple routing, no authentication.
Hardening ideas: auth, rate limits, secret management, drift monitoring,
model versioning, human approval gates before any write action.
