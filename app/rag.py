# app/rag.py
import chromadb

client = chromadb.PersistentClient(path="store/chroma")
collection = client.get_collection(name="policies")

def search_policy(query: str, k: int = 5) -> list:
    res = collection.query(query_texts=[query], n_results=k)
    hits = []
    for i in range(len(res["ids"][0])):
        md = res["metadatas"][0][i]
        hits.append({
            "control_id": md["control_id"],
            "title": md["title"],
            "source": md["source"],
            "text": res["documents"][0][i],
            "score": res["distances"][0][i],   # NOTE: lower = closer
        })
    return hits

def get_control(control_id: str):
    res = collection.get(ids=[control_id])
    if not res["ids"]:
        return None
    return {"control_id": res["ids"][0], "text": res["documents"][0], **res["metadatas"][0]}