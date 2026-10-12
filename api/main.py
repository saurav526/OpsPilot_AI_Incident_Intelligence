from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from src.data import load_data, summary
from src.model import score_frame
from src.agent import investigate
from src.db import recent_interactions

app = FastAPI(title="OpsPilot AI API", version="1.0.0", description="Synthetic-data incident intelligence demo. Recommendations only.")

class InvestigateRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    service: str | None = Field(default=None, max_length=100)
    top_k: int = Field(default=3, ge=1, le=5)

@app.get("/health")
def health(): return {"status":"ok","service":"opspilot-api"}

@app.get("/metrics/summary")
def metrics_summary(): return summary(load_data())

@app.get("/anomalies")
def anomalies(limit: int = Query(default=10, ge=1, le=100)):
    df = score_frame(load_data()).head(limit).copy()
    df["timestamp"] = df.timestamp.astype(str)
    return df.to_dict(orient="records")

@app.post("/investigate")
def investigate_incident(payload: InvestigateRequest):
    try: return investigate(payload.question,payload.service,payload.top_k)
    except Exception as exc: raise HTTPException(status_code=500, detail=f"Investigation failed: {type(exc).__name__}: {exc}")

@app.get("/audit/recent")
def audit_recent(limit: int = Query(default=20, ge=1, le=200)): return recent_interactions(limit)
