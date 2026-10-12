from pathlib import Path
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from src.data import FEATURE_COLUMNS, ROOT, load_data

MODEL_PATH = ROOT / "models" / "isolation_forest.joblib"

def build_model(contamination=0.06, random_state=42):
    return Pipeline([("scaler", StandardScaler()), ("detector", IsolationForest(
        n_estimators=250, contamination=contamination, random_state=random_state, n_jobs=-1))])

def train_model(df=None, output_path=None):
    df = df if df is not None else load_data()
    model = build_model().fit(df[FEATURE_COLUMNS])
    path = Path(output_path) if output_path else MODEL_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    return model, path

def score_frame(df, model=None, model_path=None):
    if model is None:
        path = Path(model_path) if model_path else MODEL_PATH
        if path.exists(): model = joblib.load(path)
        else: model, _ = train_model(df)
    result = df.copy()
    result["anomaly_score"] = -model.score_samples(result[FEATURE_COLUMNS])
    result["anomaly_flag"] = model.predict(result[FEATURE_COLUMNS]) == -1
    return result.sort_values("anomaly_score", ascending=False).reset_index(drop=True)
