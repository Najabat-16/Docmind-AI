[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Gemini API](https://img.shields.io/badge/Powered%20by-Google%20Gemini-orange)](https://ai.google.dev)

# DocMind AI — AI-Powered Document Q&A System (RAG-Based)

**A Retrieval-Augmented Generation (RAG) system that lets you ask questions about your own PDF documents.**

## Features
- **PDF Processing**: Automatically extracts and chunks text from PDF files
- **Semantic Search**: Uses Gemini embeddings to find contextually relevant document sections
- **Grounded Answers**: Generates responses using only retrieved content (reduces hallucination)
- **Interactive UI**: Chat-based interface built with Streamlit
- **Source Attribution**: Shows which documents were used to answer each question

## Architecture
- **Embedding Model**: Google Gemini (`gemini-embedding-001`)
- **Vector Database**: ChromaDB (local, persistent storage)
- **Generation Model**: Google Gemini (`gemini-2.0-flash`)
- **Frontend**: Streamlit

## Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API key (free at https://aistudio.google.com/apikey)

### Installation
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/docmind-ai.git
cd docmind-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Setup
1. Create a `.env` file and add your API key: AQ.Ab8RN6Ip-qaDNpQUpbXqXTsxB2172iAZ4T2OOaGq4Y9HZXXSDw

2. Add your PDF files to the `data/` folder

3. Index the documents:
```bash
python ingest.py
```

4. Launch the chat interface:
```bash
streamlit run app.py
```

## How It Works

### Ingestion (`ingest.py`)
1. Reads PDFs from `data/` folder
2. Chunks text into 500-word segments with 50-word overlap
3. Embeds each chunk using Gemini's embedding model
4. Stores embeddings + metadata in ChromaDB vector database

### Retrieval & Generation (`app.py`)
1. User asks a question via Streamlit chat interface
2. Question is embedded using same model
3. ChromaDB performs cosine similarity search to find top-4 most relevant chunks
4. Retrieved chunks + question sent to Gemini for generation
5. Gemini generates grounded answer (instructed to use only provided context)
6. Answer + source documents displayed to user

## Project Structure
Ask questions about your own PDF documents and get grounded, AI-generated answers.
Built using Google Gemini (embeddings + generation) and ChromaDB (vector database).

docmind-ai/
├── rag_utils.py       # Shared helper functions (embedding, chunking, ChromaDB)
├── ingest.py          # One-time script to process PDFs and build vector database
├── app.py             # Streamlit chat interface
├── requirements.txt   # Python dependencies
├── .env.example       # Template for environment variables
├── .gitignore         # Git configuration
├── data/              # Folder for your PDF files
└── README.md          # This file

## Technical Details

### Vector Search
Uses cosine similarity to find semantically similar document chunks. The Gemini embedding model converts text into 768-dimensional vectors.

### Grounding
The LLM is explicitly instructed: "Answer using ONLY the context provided below." This grounds responses in actual document content, reducing hallucination.

### Chunking Strategy
- Chunk size: 500 words
- Overlap: 50 words (preserves context across boundaries)
- Prevents loss of information at chunk boundaries

## Performance
- Average retrieval latency: ~100-200ms (depends on ChromaDB size)
- Embedding API calls: Batched in groups of 20 for efficiency
- Storage: Minimal (vector embeddings are compressed, metadata-only)

## Limitations & Future Work
- ChromaDB is local; for production, use a cloud vector DB (Pinecone, Weaviate)
- Currently supports PDF input; could extend to Word, text, web pages
- No multi-user support (session-based)
- No chat history persistence across app restarts

## Use Cases
- Study assistant (ask questions about course notes)
- Document analysis (Q&A over research papers, reports)
- Knowledge base (company docs, manuals, FAQs)

## Author
**Rana Muhammad Najabat Ali**
- Email: alinajabat84@gmail.com
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- LinkedIn: [Your Profile]

## License
MIT License - feel free to use and modify this project

## Acknowledgments
- Google Gemini API for embeddings and generation
- ChromaDB for vector storage
- Streamlit for UI framework

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
