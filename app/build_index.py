# app/build_index.py
import os, glob, re
import chromadb

chunks = []
for path in glob.glob("data/policies/*.md"):
    doc = open(path, encoding="utf-8").read()
    source = os.path.basename(path)
    for block in re.split(r"\n(?=## )", doc):
        m = re.match(r"## ([A-Z]+-\d+)\s*[-\u2014]\s*(.+)", block)
        if not m:
            continue
        chunks.append({
            "control_id": m.group(1),
            "title": m.group(2).strip(),
            "source": source,
            "text": block.strip(),
        })

client = chromadb.PersistentClient(path="store/chroma")
collection = client.get_or_create_collection(name="policies")

collection.upsert(
    ids=[c["control_id"] for c in chunks],
    documents=[c["text"] for c in chunks],
    metadatas=[{"control_id": c["control_id"],
                "title": c["title"],
                "source": c["source"]} for c in chunks],
)

print("Indexed", collection.count(), "controls into store/chroma")
