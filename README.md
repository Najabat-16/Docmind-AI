# DocMind AI — AI-Powered Document Q&A System (RAG-Based)

Ask questions about your own PDF documents and get grounded, AI-generated answers.
Built using Google Gemini (embeddings + generation) and ChromaDB (vector database).

## How it works
1. `ingest.py` reads your PDFs, splits them into chunks, converts each chunk into
   a vector embedding using Gemini, and stores them in a local ChromaDB database.
2. `app.py` runs a chat interface (Streamlit). When you ask a question, it embeds
   your question, finds the most relevant chunks from your documents, and asks
   Gemini to answer using only that retrieved content.

## Setup Instructions (Beginner Friendly)

### 1. Install Python
Check if Python is already installed by opening a terminal and running:
```
python3 --version
```
If it's not installed, download it from https://www.python.org/downloads/
(during installation on Windows, check the box "Add Python to PATH").

### 2. Open this folder in VS Code
Open VS Code → File → Open Folder → select the `docmind-ai` folder.

### 3. Create a virtual environment
In the VS Code terminal (Terminal → New Terminal), run:
```
python3 -m venv venv
```
Then activate it:
- On Mac/Linux: `source venv/bin/activate`
- On Windows: `venv\Scripts\activate`

You'll know it worked because you'll see `(venv)` at the start of your terminal line.

### 4. Install the required packages
```
pip install -r requirements.txt
```

### 5. Get a free Gemini API key
Go to https://aistudio.google.com/apikey and click "Create API Key" (free tier available).
Copy the key.

### 6. Create your .env file
Copy `.env.example` and rename the copy to `.env`. Open it and paste your key:
```
GEMINI_API_KEY=your_actual_key_here
```

### 7. Add your documents
Put a few PDF files into the `data/` folder (e.g. your course notes, a textbook chapter,
lecture slides exported as PDF).

### 8. Run ingestion
This reads your PDFs and builds the vector database:
```
python ingest.py
```
You should see it print progress for each file, ending with "Ingestion complete."

### 9. Launch the chat app
```
streamlit run app.py
```
This opens a browser window where you can start asking questions about your documents.

## Notes for your resume / interview prep
- **Chunking**: text is split into 500-word chunks with 50-word overlap so context
  isn't lost at chunk boundaries.
- **Embeddings**: Gemini's `gemini-embedding-001` model converts text into vectors.
- **Vector search**: ChromaDB finds the top-k most similar chunks using cosine similarity.
- **Grounding**: the LLM is instructed to answer only from retrieved context, reducing
  hallucination and keeping answers tied to your actual documents.

## Troubleshooting
- "GEMINI_API_KEY not found" → make sure your `.env` file exists (not just `.env.example`)
  and is in the same folder as the Python files.
- "No PDF files found" → make sure your PDFs are directly inside the `data/` folder.
- Model not found errors → check https://ai.google.dev/gemini-api/docs/models for the
  current model names and update `EMBEDDING_MODEL` / `GENERATION_MODEL` in `rag_utils.py`.
