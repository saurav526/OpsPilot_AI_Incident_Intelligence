from src.data import load_data, FEATURE_COLUMNS
from src.model import train_model, score_frame

if __name__ == "__main__":
    df = load_data()
    model, path = train_model(df)
    scored = score_frame(df, model=model)
    flagged = int(scored.anomaly_flag.sum())
    print("OpsPilot lightweight smoke evaluation")
    print(f"Rows: {len(df)} | features: {len(FEATURE_COLUMNS)} | model: {path}")
    print(f"Flagged: {flagged} ({flagged/len(df):.1%})")
    print(f"Mean anomaly score: {scored.anomaly_score.mean():.4f}")
    print(scored[scored.anomaly_flag].groupby("service").size().sort_values(ascending=False).to_string())
    print("Synthetic data without ground-truth labels: this is not a model-quality claim.")
