import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.data import load_data
from src.model import train_model, score_frame

if __name__ == "__main__":
    df = load_data()
    model, path = train_model(df)
    scored = score_frame(df, model=model)
    print(f"Loaded {len(df)} rows across {df.service.nunique()} services.")
    print(f"Saved model: {path}")
    print(scored[["timestamp","service","latency_ms","error_rate_pct","cpu_pct","anomaly_score","anomaly_flag"]].head(10).to_string(index=False))
