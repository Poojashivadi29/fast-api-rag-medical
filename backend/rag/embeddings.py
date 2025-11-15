import os

OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")
USE_OPENAI = bool(OPENAI_KEY)


class Embeddings:
    """Lazy-loading Embeddings wrapper.

    Heavy dependencies (numpy, sentence-transformers, openai) are imported only when
    actually needed so the module can be imported on systems where those packages
    aren't installed (e.g., Windows dev machines).
    """

    def __init__(self, model_name_local: str = "all-MiniLM-L6-v2"):
        self.use_openai = USE_OPENAI
        self.model_name_local = model_name_local
        self.local_model = None
        # Defer heavy imports to here so importing this module doesn't fail
        if self.use_openai:
            import openai

            openai.api_key = OPENAI_KEY
            self._openai = openai
        else:
            # sentence-transformers may not be installed; allow the caller to catch
            # import errors when attempting to construct this class.
            from sentence_transformers import SentenceTransformer

            self.local_model = SentenceTransformer(model_name_local)

    def embed_texts(self, texts):
        # Import numpy locally to avoid top-level dependency
        import numpy as np

        if self.use_openai:
            model = "text-embedding-3-small"
            embeddings = []
            batch = 16
            for i in range(0, len(texts), batch):
                b = texts[i : i + batch]
                resp = self._openai.Embeddings.create(input=b, model=model)
                batch_emb = [r["embedding"] for r in resp["data"]]
                embeddings.extend(batch_emb)
            return np.array(embeddings, dtype=np.float32)
        else:
            arr = self.local_model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
            return arr.astype("float32")
