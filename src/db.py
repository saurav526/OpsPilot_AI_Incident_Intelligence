import os, sqlite3, json
from pathlib import Path
from datetime import datetime, timezone

def _connect():
    path = Path(os.getenv("OPS_PILOT_DB", "opspilot_audit.db"))
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path); conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with _connect() as c:
        c.execute("CREATE TABLE IF NOT EXISTS audit_log (id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT NOT NULL, question TEXT NOT NULL, service TEXT, answer TEXT NOT NULL, evidence_json TEXT NOT NULL)")

def log_interaction(question, service, answer, evidence):
    init_db()
    with _connect() as c:
        c.execute("INSERT INTO audit_log(created_at,question,service,answer,evidence_json) VALUES(?,?,?,?,?)",
          (datetime.now(timezone.utc).isoformat(), question, service, answer, json.dumps(evidence, default=str)))

def recent_interactions(limit=20):
    init_db()
    with _connect() as c:
        rows = c.execute("SELECT id,created_at,question,service,answer,evidence_json FROM audit_log ORDER BY id DESC LIMIT ?", (max(1,min(int(limit),200)),)).fetchall()
    return [dict(r) for r in rows]
