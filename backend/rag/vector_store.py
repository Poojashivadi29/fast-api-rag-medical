import faiss, numpy as np, json, os
from typing import List, Dict, Any

class FaissStore:
    def __init__(self, dim: int, index_path="backend/rag/faiss.index", meta_path="backend/rag/meta.json"):
        self.dim = dim
        self.index_path = index_path
        self.meta_path = meta_path
        self.index = faiss.IndexFlatIP(dim)
        self.metadata: List[Dict[str,Any]] = []
        os.makedirs(os.path.dirname(self.index_path) or ".", exist_ok=True)

    def add(self, vectors: np.ndarray, metadatas: List[Dict[str,Any]]):
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms==0] = 1.0
        vecs = vectors / norms
        self.index.add(vecs)
        self.metadata.extend(metadatas)

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    def load(self):
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.meta_path, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)
            return True
        return False

    def search(self, vectors: np.ndarray, top_k: int = 5):
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms==0] = 1.0
        vecs = vectors / norms
        distances, indices = self.index.search(vecs, top_k)
        results = []
        for row_scores, row_idx in zip(distances, indices):
            hits = []
            for score, idx in zip(row_scores.tolist(), row_idx.tolist()):
                if idx < 0 or idx >= len(self.metadata):
                    continue
                meta = dict(self.metadata[idx])
                meta["_score"] = float(score)
                meta["_index"] = int(idx)
                hits.append(meta)
            results.append(hits)
        return results

    def ntotal(self):
        return int(self.index.ntotal)
