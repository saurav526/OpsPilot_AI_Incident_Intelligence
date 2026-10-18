# OpsPilot AI: Incident Intelligence & Resolution Copilot
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-Isolation%20Forest-F7931E?logo=scikitlearn&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Audit%20Log-003B57?logo=sqlite&logoColor=white)
![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)

An AI copilot that helps on-call engineers investigate incidents. It ranks unusual
metric patterns with anomaly detection, retrieves relevant runbook guidance, and
composes evidence-backed, **read-only** recommendations. It runs on synthetic
telemetry and never executes production actions.

![Dashboard screenshot](docs/dashboard.png)

## Features

- **Anomaly detection**: StandardScaler + Isolation Forest to surface unusual metric combinations
- **Runbook retrieval**: TF-IDF / cosine similarity over a markdown knowledge base
- **Investigation agent**: combines metrics, anomalies, and runbooks into a recommended set of checks
- **Optional LLM**: Groq-powered answers, with a deterministic local fallback when no key is set
- **REST API**: FastAPI with request validation and interactive docs at `/docs`
- **Dashboard**: Streamlit UI for exploring metrics, anomalies, and investigations
- **Audit trail**: every investigation logged to SQLite

## How it works

```
Question + service
      │
      ▼
 Metrics summary ──► Anomaly scores (Isolation Forest)
      │                       │
      └────────┬──────────────┘
               ▼
     Runbook retrieval (TF-IDF)
               ▼
   Agent composes evidence + read-only next steps
               ▼
        Response + SQLite audit log
```

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
## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
