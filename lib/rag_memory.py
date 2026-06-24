import chromadb
import document_handler

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

def chunk_text(text, chunk_size=8192):
    # Have to split the text into chunks to avoid hitting the token limit of the model probably using recurssion
    pass
    

def handle_document(file_path):
    pdf_file = document_handler.convert_docx_to_pdf(file_path)
    text = document_handler.extract_text_from_pdf(pdf_file)
    