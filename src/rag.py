from pathlib import Path
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.data import ROOT

KB_PATH = ROOT / "knowledge_base"

def load_documents(kb_path=None):
    docs = []
    for file in sorted((Path(kb_path) if kb_path else KB_PATH).glob("*.md")):
        text = file.read_text(encoding="utf-8")
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        chunk = ""
        for p in paragraphs:
            if chunk and len(chunk) + len(p) > 1000:
                docs.append({"source": file.name, "text": chunk.strip()}); chunk = ""
            chunk += p + "\n\n"
        if chunk.strip(): docs.append({"source": file.name, "text": chunk.strip()})
    return docs

class RunbookRetriever:
    def __init__(self, kb_path=None):
        self.documents = load_documents(kb_path)
        if not self.documents: raise ValueError("No Markdown runbooks found")
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2))
        self.matrix = self.vectorizer.fit_transform([d["text"] for d in self.documents])
    def search(self, query, top_k=3):
        scores = cosine_similarity(self.vectorizer.transform([query]), self.matrix).ravel()
        order = scores.argsort()[::-1][:max(1, top_k)]
        return [{**self.documents[i], "score": round(float(scores[i]), 4)}
                for i in order if scores[i] > 0]
