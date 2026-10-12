from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "incidents.csv"
FEATURE_COLUMNS = ["latency_ms", "error_rate_pct", "cpu_pct", "memory_pct", "requests_per_min", "db_connections_pct"]

def load_data(path=None):
    df = pd.read_csv(Path(path) if path else DATA_PATH, parse_dates=["timestamp"])
    required = {"timestamp", "service", "severity", "incident_type", *FEATURE_COLUMNS}
    missing = required - set(df.columns)
    if missing: raise ValueError(f"Missing columns: {sorted(missing)}")
    if df.empty: raise ValueError("Dataset is empty")
    for col in FEATURE_COLUMNS: df[col] = pd.to_numeric(df[col], errors="coerce")
    df[FEATURE_COLUMNS] = df[FEATURE_COLUMNS].fillna(df[FEATURE_COLUMNS].median())
    return df.sort_values("timestamp").reset_index(drop=True)

def summary(df):
    return {"rows": int(len(df)), "services": int(df.service.nunique()),
            "start": str(df.timestamp.min()), "end": str(df.timestamp.max()),
            "mean_latency_ms": round(float(df.latency_ms.mean()), 2),
            "mean_error_rate_pct": round(float(df.error_rate_pct.mean()), 3),
            "severity_counts": {str(k): int(v) for k,v in df.severity.value_counts().items()}}
