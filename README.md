# OpsPilot AI — Incident Intelligence & Resolution Copilot

A runnable portfolio project demonstrating data science, anomaly detection, runbook retrieval, a tool-using incident assistant, REST API, Streamlit dashboard, and SQLite audit logging. Uses synthetic telemetry; no production actions are executed.

## Quick start (Windows PowerShell)
Install Python 3.11, unzip this folder, open it in VS Code, then run:
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts\train.py
streamlit run app\streamlit_app.py
```
Open `http://localhost:8501`.

For the API, open a second terminal from the project root:
```powershell
.\.venv\Scripts\Activate.ps1
uvicorn api.main:app --reload
```
Open `http://127.0.0.1:8000/docs`.

macOS/Linux: use `python3 -m venv .venv` and `source .venv/bin/activate`, then the same pip/train/streamlit commands. API command: `uvicorn api.main:app --reload`.

## Optional LLM
Copy `.env.example` to `.env`, add `GROQ_API_KEY`, and optionally set `GROQ_MODEL`. Without a key, a deterministic local answer generator works. Never commit `.env`.

## Test/evaluate
```bash
python scripts/evaluate.py
pytest -q
```

## API
- `GET /health`
- `GET /metrics/summary`
- `GET /anomalies?limit=10`
- `POST /investigate` with `{"question":"Why is checkout latency high?","service":"checkout"}`
- `GET /audit/recent?limit=20`

## Architecture
- `src/data.py`: data loading and summary
- `src/model.py`: StandardScaler + Isolation Forest
- `src/rag.py`: TF-IDF/cosine runbook retrieval
- `src/agent.py`: metrics + anomaly + retrieval tool workflow; optional Groq generation
- `src/db.py`: SQLite audit log
- `api/main.py`: FastAPI routes
- `app/streamlit_app.py`: dashboard
- `scripts/train.py`, `scripts/evaluate.py`: model training and smoke evaluation
- `tests/test_core.py`: core tests

## Interview talking points
Problem: incident context is scattered across telemetry and runbooks. Data science ranks unusual metric combinations; retrieval supplies operational guidance; the agent composes evidence and recommended read-only checks. API validation, audit logging, tests, and local fallback make the demo reproducible.

Limitations: synthetic data, lexical retrieval, simple routing, no authentication, and no production observability. Anomaly scores prioritize investigation but do not prove root cause.

## Production hardening
Add authentication/authorization, rate limits, secret management, structured monitoring, a labeled evaluation set, drift monitoring, model versioning, and human approval gates before any write action.
