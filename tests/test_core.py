from src.data import load_data, FEATURE_COLUMNS
from src.model import build_model, score_frame
from src.rag import RunbookRetriever
from src.agent import investigate

def test_dataset():
    df = load_data()
    assert len(df) > 100
    assert set(FEATURE_COLUMNS).issubset(df.columns)

def test_model_scores_rows():
    df = load_data()
    model = build_model().fit(df[FEATURE_COLUMNS])
    result = score_frame(df,model=model)
    assert len(result) == len(df)
    assert result.anomaly_score.notna().all()

def test_runbook_retrieval():
    result = RunbookRetriever().search("checkout latency database timeout")
    assert result and "source" in result[0]

def test_investigation():
    result = investigate("Why is checkout latency high?","checkout",write_audit=False)
    assert result["service"] == "checkout"
    assert "metrics" in result and "Investigation summary" in result["answer"]
