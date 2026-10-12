import os
from dotenv import load_dotenv
from src.data import load_data
from src.model import score_frame
from src.rag import RunbookRetriever
from src.db import log_interaction

load_dotenv()

def _latest_metrics(df, service):
    subset = df[df.service.str.lower() == service.lower()] if service else df
    if subset.empty: return {"error": f"No telemetry found for service '{service}'."}
    r = subset.sort_values("timestamp").iloc[-1]
    return {"service": str(r.service), "timestamp": str(r.timestamp),
      **{k: round(float(r[k]), 3) for k in ["latency_ms","error_rate_pct","cpu_pct","memory_pct","requests_per_min","db_connections_pct"]}}

def _local_answer(metrics, anomalies, runbooks):
    if "error" in metrics: return metrics["error"]
    text = (f"## Investigation summary\n\nLatest **{metrics['service']}** telemetry at {metrics['timestamp']}: "
      f"latency **{metrics['latency_ms']} ms**, errors **{metrics['error_rate_pct']}%**, CPU **{metrics['cpu_pct']}%**, "
      f"memory **{metrics['memory_pct']}%**, DB connections **{metrics['db_connections_pct']}%**.\n\n")
    if anomalies:
        a = anomalies[0]
        text += f"Top anomaly candidate: latency {a['latency_ms']} ms, error rate {a['error_rate_pct']}%, anomaly score {a['anomaly_score']:.4f}.\n\n"
    text += "## Suggested next checks\n- Compare symptoms with recent deployments and configuration changes.\n- Inspect logs and distributed traces around the timestamp.\n- Check database pool utilization and slow queries if latency/connection usage is elevated.\n- Compare upstream and downstream dependency latency.\n"
    if runbooks:
        text += "\n## Retrieved runbook evidence\n"
        for r in runbooks:
            text += f"\n**{r['source']}** (score {r['score']}):\n\n{r['text'][:600]}\n"
    return text + "\n**Caution:** Anomaly scores prioritize investigation; they do not prove root cause. Validate with logs, traces, and an operator."

def _groq_answer(question, metrics, anomalies, runbooks):
    if not os.getenv("GROQ_API_KEY"): return None
    try:
        from groq import Groq
        context = {"metrics":metrics,"anomalies":anomalies[:3],"runbooks":[{"source":r["source"],"text":r["text"][:1000]} for r in runbooks]}
        response = Groq(api_key=os.getenv("GROQ_API_KEY")).chat.completions.create(
          model=os.getenv("GROQ_MODEL","llama-3.3-70b-versatile"), temperature=0.2,
          messages=[
            {"role":"system","content":"You are an incident triage assistant. Use only provided evidence. Separate facts from hypotheses, cite runbook filenames, recommend safe read-only checks, and never claim anomaly scores prove root cause. Never execute or suggest automatic production changes."},
            {"role":"user","content":f"Question: {question}\nEvidence: {context}"}
          ])
        return response.choices[0].message.content
    except Exception:
        return None

def investigate(question, service=None, top_k=3, write_audit=True):
    df = load_data()
    if not service: service = str(df.service.iloc[0])
    metrics = _latest_metrics(df, service)
    if "error" in metrics:
        result = {"question":question,"service":service,"answer":metrics["error"],"metrics":metrics,"anomalies":[],"runbooks":[]}
        if write_audit: log_interaction(question,service,result["answer"],result)
        return result
    scored = score_frame(df)
    anomalies = scored[scored.service.str.lower() == metrics["service"].lower()].head(3).to_dict("records")
    for a in anomalies:
        a["timestamp"] = str(a["timestamp"])
        for k,v in list(a.items()):
            if hasattr(v,"item"): a[k] = v.item()
    runbooks = RunbookRetriever().search(f"{service} {question} latency errors CPU memory database", top_k)
    answer = _groq_answer(question,metrics,anomalies,runbooks) or _local_answer(metrics,anomalies,runbooks)
    result = {"question":question,"service":metrics["service"],"answer":answer,"metrics":metrics,"anomalies":anomalies,"runbooks":runbooks}
    if write_audit: log_interaction(question,metrics["service"],answer,{"metrics":metrics,"anomalies":anomalies,"runbooks":runbooks})
    return result
