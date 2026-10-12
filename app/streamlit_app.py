import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
import plotly.express as px
import streamlit as st
from src.data import load_data, summary
from src.model import score_frame
from src.agent import investigate
from src.db import recent_interactions

st.set_page_config(page_title="OpsPilot AI", page_icon="🛰️", layout="wide")
st.title("🛰️ OpsPilot AI")
st.caption("Enterprise Incident Intelligence & Resolution Copilot · synthetic demo data")
df = load_data()
with st.sidebar:
    st.header("Settings")
    services = ["All services"] + sorted(df.service.unique().tolist())
    selected = st.selectbox("Service filter",services,index=1 if "checkout" in services else 0)
    st.info("Read-only demo. No production actions are executed.")
    st.caption("Optional LLM: set GROQ_API_KEY in .env. Local fallback works without it.")
s = summary(df)
cols = st.columns(4)
cols[0].metric("Telemetry rows",f"{s['rows']:,}")
cols[1].metric("Services",s["services"])
cols[2].metric("Mean latency",f"{s['mean_latency_ms']:.0f} ms")
cols[3].metric("Mean error rate",f"{s['mean_error_rate_pct']:.2f}%")
filtered = df if selected == "All services" else df[df.service == selected]
t1,t2,t3 = st.tabs(["📈 Telemetry","🚨 Anomalies","🧠 Incident copilot"])
with t1:
    a,b = st.columns(2)
    with a: st.plotly_chart(px.line(filtered,x="timestamp",y="latency_ms",color="service",title="Latency over time (ms)"),use_container_width=True)
    with b: st.plotly_chart(px.line(filtered,x="timestamp",y="error_rate_pct",color="service",title="Error rate over time (%)"),use_container_width=True)
    st.dataframe(filtered.sort_values("timestamp",ascending=False).head(30),use_container_width=True)
with t2:
    scored = score_frame(df)
    if selected != "All services": scored = scored[scored.service == selected]
    st.caption("Higher score = more unusual metric combination, not confirmed root cause.")
    st.dataframe(scored.head(25),use_container_width=True)
    st.plotly_chart(px.scatter(scored,x="latency_ms",y="error_rate_pct",color="anomaly_flag",size="anomaly_score",hover_data=["service","timestamp","cpu_pct"],title="Latency vs error rate"),use_container_width=True)
with t3:
    with st.form("investigate"):
        question = st.text_area("Incident question","Why is checkout latency high, and what should I check first?")
        service_options = sorted(df.service.unique().tolist())
        idx = service_options.index(selected) if selected in service_options else 0
        service = st.selectbox("Service",service_options,index=idx)
        go = st.form_submit_button("Investigate",type="primary")
    if go:
        with st.spinner("Gathering metrics and runbook evidence..."):
            result = investigate(question,service)
        st.markdown(result["answer"])
        with st.expander("Structured evidence"): st.json({"metrics":result["metrics"],"anomalies":result["anomalies"],"runbooks":result["runbooks"]})
with st.expander("Recent audit log"):
    for row in recent_interactions(20):
        st.markdown(f"**{row['created_at']} · {row['service'] or 'unknown'}**")
        st.write(row["question"])
        st.caption(row["answer"][:350])
        st.divider()
