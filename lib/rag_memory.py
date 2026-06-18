import chromadb

client=chromadb.PersistentClient(path="./memory")
collection=client.get_or_create_collection("elvis_memory")
doc_id=collection.count()

def add_text(text):
    global doc_id

    collection.add(
        documents=[text],
        ids=[str(doc_id)]
    )

    doc_id += 1

def retrieve_text(query, n_results=3):
    if collection.count() == 0:
        return ""

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count())
    )

    return "\n\n".join(results["documents"][0])
