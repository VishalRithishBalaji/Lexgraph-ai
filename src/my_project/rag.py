from pypdf import PdfReader
import chromadb
from chromadb.utils import embedding_functions

# Persistent ChromaDB
client = chromadb.PersistentClient(path="vector_db")

embedding_fn = (
    embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
)

collection = client.get_or_create_collection(
    name="case_documents",
    embedding_function=embedding_fn
)

def clear_collection():
    try:
        client.delete_collection("case_documents")
    except Exception:
        pass

    return client.get_or_create_collection(
        name="case_documents",
        embedding_function=embedding_fn
    )

def ingest_pdf(pdf_path):
    global collection

    collection = clear_collection()
    reader = PdfReader(pdf_path)
    full_text = ""
    chunk_size = 800

    for page_num, page in enumerate(reader.pages):
        page_text = page.extract_text()

        if not page_text:
            continue

        full_text += f"\n\n[PAGE {page_num + 1}]\n"
        full_text += page_text

        # Create chunks per page
        chunks = []
        for i in range(0, len(page_text), chunk_size):
            chunks.append(page_text[i:i + chunk_size])

        for idx, chunk in enumerate(chunks):
            collection.add(
                ids=[f"page_{page_num+1}_chunk_{idx}"],
                documents=[chunk],
                metadatas=[
                    {
                        "page": page_num + 1
                    }
                ]
            )

    return full_text

def retrieve_context(query, k=5):
    results = collection.query(
        query_texts=[query],
        n_results=k
    )

    contexts = []
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    for doc, meta in zip(documents, metadatas):
        page = meta.get("page", "Unknown")

        contexts.append(
            f"""
SOURCE PAGE: {page}

{doc}
"""
        )

    return "\n\n".join(contexts)