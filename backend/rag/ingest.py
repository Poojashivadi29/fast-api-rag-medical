import json, os, nltk
from nltk.tokenize import sent_tokenize
from backend.rag.embeddings import Embeddings
from backend.rag.vector_store import FaissStore
import numpy as np
nltk.download("punkt", quiet=True)

def chunk_text(text, max_words=120, overlap=20):
    sents = sent_tokenize(text)
    chunks = []
    current = []
    cur_len = 0
    for s in sents:
        words = s.split()
        if cur_len + len(words) > max_words and current:
            chunks.append(" ".join(current))
            tail = " ".join(" ".join(current).split()[-overlap:])
            current = [tail] if overlap > 0 else []
            cur_len = len(tail.split()) if overlap>0 else 0
        current.append(s)
        cur_len += len(words)
    if current:
        chunks.append(" ".join(current))
    return chunks

def ingest(input_json="data/clinic_info.json", store_dir="backend/rag", model_name_local="all-MiniLM-L6-v2"):
    with open(input_json, "r", encoding="utf-8") as f:
        docs = json.load(f)
    texts = []
    metas = []
    for doc in docs:
        doc_id = doc.get("id")
        title = doc.get("title","")
        text = doc.get("text","")
        chunks = chunk_text(text)
        for i,c in enumerate(chunks):
            texts.append(c)
            metas.append({"doc_id": doc_id, "title": title, "chunk_id": i, "text": c})
    emb = Embeddings(model_name_local=model_name_local)
    vectors = emb.embed_texts(texts)
    dim = vectors.shape[1]
    os.makedirs(store_dir, exist_ok=True)
    store = FaissStore(dim=dim, index_path=f"{store_dir}/faiss.index", meta_path=f"{store_dir}/meta.json")
    store.add(vectors, metas)
    store.save()
    print(f"Ingested {len(texts)} chunks to {store_dir}")

if __name__ == "__main__":
    ingest()
