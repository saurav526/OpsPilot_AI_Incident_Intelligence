---
description: Start the FastAPI server and smoke-test the endpoints
---
Start `uvicorn api.main:app --reload` in the background, then check:
GET /health, GET /metrics/summary, GET /anomalies?limit=10, and
POST /investigate with {"question":"Why is checkout latency high?","service":"checkout"}.
Report status codes and anything unexpected, then stop the server.
