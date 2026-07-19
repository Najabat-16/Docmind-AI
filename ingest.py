"""
ingest.py
Run this file FIRST, whenever you add new PDFs to the data/ folder.
It reads every PDF in data/, splits it into chunks, turns those chunks
into embeddings, and stores everything in the ChromaDB vector database.

Run it from the terminal like this:
    python ingest.py
"""

import os
import glob
from rag_utils import get_client, extract_text_from_pdf, chunk_text, embed_texts, get_collection

DATA_FOLDER = "./data"


def main():
    client = get_client()
    collection = get_collection()

    pdf_files = glob.glob(os.path.join(DATA_FOLDER, "*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {DATA_FOLDER}/")
        print("Add some PDF files to the 'data' folder and run this script again.")
        return

    print(f"Found {len(pdf_files)} PDF file(s). Starting ingestion...\n")

    doc_id_counter = 0

    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        print(f"Processing: {filename}")

        text = extract_text_from_pdf(pdf_path)
        if not text.strip():
            print(f"  No readable text found in {filename}, skipping.")
            continue

        chunks = chunk_text(text, chunk_size=500, overlap=50)
        print(f"  Split into {len(chunks)} chunk(s).")

        # Send chunks to the embedding API in small batches
        batch_size = 20
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            embeddings = embed_texts(client, batch, task_type="RETRIEVAL_DOCUMENT")

            ids = [f"{filename}_{doc_id_counter + j}" for j in range(len(batch))]
            metadatas = [{"source": filename} for _ in batch]

            collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=batch,
                metadatas=metadatas,
            )
            doc_id_counter += len(batch)

        print(f"  Done with {filename}.\n")

    print(f"Ingestion complete. Total chunks stored: {doc_id_counter}")
    print("You can now run: streamlit run app.py")


if __name__ == "__main__":
    main()
