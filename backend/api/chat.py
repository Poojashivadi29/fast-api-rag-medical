from fastapi import APIRouter, HTTPException
from backend.models import AgentQueryRequest, AgentQueryResponse, RetrievedPassage
from backend.agent.scheduling_agent import decide_intent, generate_answer
router = APIRouter(prefix="/api", tags=["agent"])

EMB = None
RAG_STORE = None
try:
    EMB = Embeddings()
    sample = EMB.embed_texts(["hello"])
    dim = sample.shape[1]
    store = FaissStore(dim=dim, index_path="backend/rag/faiss.index", meta_path="backend/rag/meta.json")
    if store.load():
        RAG_STORE = store
except Exception:
    RAG_STORE = None
import os

router = APIRouter(prefix="/api", tags=["agent"])

# Lazy/import-safe initialization of RAG components. Some systems (Windows) may not have
# faiss/sentence-transformers available; import errors should not prevent the API from
# starting for non-RAG functionality.
EMB = None
RAG_STORE = None
try:
    # Import inside try so missing heavy deps don't crash app startup
    from backend.rag.embeddings import Embeddings
    from backend.rag.vector_store import FaissStore

    EMB = Embeddings()
    sample = EMB.embed_texts(["hello"])
    dim = sample.shape[1]
    store = FaissStore(dim=dim, index_path="backend/rag/faiss.index", meta_path="backend/rag/meta.json")
    if store.load():
        RAG_STORE = store
except Exception:
    EMB = None
    RAG_STORE = None

def retrieve_passages(query: str, top_k: int = 3):
    if RAG_STORE and EMB:
        qv = EMB.embed_texts([query])
        hits = RAG_STORE.search(qv, top_k=top_k)[0]
        return [{"id": h["doc_id"], "title": h["title"], "text": h["text"], "score": h["_score"]} for h in hits]
    else:
        return []

@router.post("/agent/query", response_model=AgentQueryResponse)
def agent_query(req: AgentQueryRequest):
    intent = decide_intent(req.user_query)
    passages = retrieve_passages(req.user_query, top_k=3)
    first_slot = None
    if intent == "book" and req.provider_id:
        from backend.api.calendly_integration import availability
        avail_resp = availability(provider_id=req.provider_id, days=7, timezone=req.timezone or os.getenv("APP_TZ","Asia/Kolkata"))
        if avail_resp.slots:
            first_slot = {"start": avail_resp.slots[0].start.isoformat(), "end": avail_resp.slots[0].end.isoformat(), "timezone": avail_resp.timezone}
    answer, suggested = generate_answer(req.user_query, passages, intent, provider_id=req.provider_id, first_slot=first_slot)
    return AgentQueryResponse(
        answer=answer,
        passages=[RetrievedPassage(**p) for p in passages],
        suggested_booking=suggested
    )
