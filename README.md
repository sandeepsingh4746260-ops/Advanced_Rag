# Advanced RAG Medical Q&A Assistant

An advanced Retrieval-Augmented Generation (RAG) project built in a Jupyter Notebook. It answers questions using a supplied medical/community-health PDF and combines semantic retrieval, keyword search, re-ranking, query rewriting, and answer checking.

> **Important:** This is an educational project, not a medical device or a substitute for a qualified healthcare professional. The assistant is designed to provide general information from the source document, not diagnose or prescribe treatment.

## Features

- **PDF ingestion:** Loads `text_medical.pdf` and splits it into overlapping text chunks.
- **Local embeddings:** Uses Ollama's `embeddinggemma` embedding model to represent text as vectors.
- **Vector search:** Stores and retrieves semantically relevant chunks with ChromaDB.
- **Keyword search:** Uses BM25 to find exact terms and keywords that vector search may miss.
- **Hybrid retrieval:** Combines candidate passages from vector and keyword search.
- **Re-ranking:** Uses `cross-encoder/ms-marco-MiniLM-L-6-v2` to rank retrieved passages by relevance.
- **Query rewriting and multi-query search:** Expands a user's question into clearer search queries to improve retrieval.
- **LangGraph workflow:** Organizes the assistant into nodes for routing, retrieval, context augmentation, answer generation, and answer checking/refinement.
- **Conversation memory:** Uses LangGraph checkpointing and SQLite-backed storage so follow-up questions can use prior conversation context.
- **Web search support:** The notebook includes Tavily-related configuration/dependencies for web retrieval where enabled in the workflow.
- **Source-aware answers:** Uses retrieved document context and page references where available, and adds a general-information safety note to health answers.

## Architecture

```text
User question
     |
     v
Question router
     |----------------------> Direct chat response
     |
     v
Query rewriting
     |
     v
Multi-query generation
     |
     v
Hybrid retrieval
(Vector search / ChromaDB + BM25 keyword search + optional web search)
     |
     v
Cross-encoder re-ranking
     |
     v
Context augmentation
     |
     v
LLM answer generation
     |
     v
Answer checking / self-correction
     |
     v
Final response with source context
```

## Tech Stack

- Python
- Jupyter Notebook
- LangChain
- LangGraph
- ChromaDB
- Ollama (`embeddinggemma`)
- Groq API for chat models
- BM25 (`rank_bm25`)
- Sentence Transformers cross-encoder
- PyPDF
- SQLite / LangGraph checkpointing
- Tavily search integration (when enabled)
- `python-dotenv` for environment configuration

## Project Files

Suggested repository layout:

```text
Advanced_RAG/
├── advanced_rag.ipynb
├── text_medical.pdf
├── medical_questions.json       # optional question/answer dataset, if you choose to include it
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

Do **not** commit `.env`, API keys, SQLite database files, WAL/SHM files, virtual environments, or generated ChromaDB folders. The notebook can recreate its vector store from the PDF when needed.

## Prerequisites

1. Python 3.10 or a compatible version supported by the installed packages.
2. Visual Studio Code with the **Python** and **Jupyter** extensions, or Jupyter Notebook.
3. [Ollama](https://ollama.com/) installed and running locally.
4. A Groq API key for the chat models.
5. A Tavily API key if web search is enabled in the notebook.
6. The source PDF, `text_medical.pdf`, in the notebook's working directory.

Pull the embedding model with Ollama:

```bash
ollama pull embeddinggemma
```

Make sure the Ollama service is running before executing the embedding and retrieval cells.

## Installation

Create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Install the dependencies used by the notebook:

```bash
pip install langchain-community langchain-text-splitters langchain-ollama langchain-groq langgraph langgraph-checkpoint-sqlite chromadb pypdf python-dotenv rank_bm25 sentence-transformers tavily-python
```

If the project already has a `requirements.txt`, you can also install from it after checking that its package names are valid:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a local `.env` file in the project folder:

```dotenv
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

Use only the keys you need for the enabled notebook features. Never commit `.env` to GitHub. If a real API key has ever been committed, uploaded, or shared, revoke it and generate a replacement.

The notebook uses Groq-hosted chat models. Model identifiers can change over time, so check the current available model names in the Groq console and update the notebook configuration if necessary.

## Run the Notebook

1. Put `advanced_rag.ipynb` and `text_medical.pdf` in the same folder.
2. Start Ollama and confirm that `embeddinggemma` is available.
3. Create the `.env` file with the required API keys.
4. Open the notebook in VS Code and select the `.venv` Python kernel.
5. Run the cells from top to bottom.
6. Wait for the PDF to be chunked, embedded, and indexed on the first run.
7. Ask questions in the notebook's chat loop. Type `exit` to stop.

The first run may take longer because it downloads models and creates the vector database. Later runs can reuse the persisted ChromaDB index if the folder remains available.

## Example Questions

- `What is the difference between a symptom and a sign?`
- `Why is sanitation important for preventing diarrhea?`
- `What are some danger signs that require immediate medical help?`
- `What does the source say about antibiotics and viral infections?`
- `Can you explain that in simpler words?`

Answers depend on the supplied PDF, the retrieved passages, and the model's generation. Verify health information with a qualified professional, especially for urgent symptoms or treatment decisions.

## Configuration Notes

The notebook's settings include values such as:

- `PDF_FILE`: source PDF filename
- `OLLAMA_URL`: local Ollama endpoint, commonly `http://localhost:11434`
- `CHROMA_FOLDER`: local persistent vector-store directory
- Number of generated queries and retrieved chunks
- Re-ranking and answer-refinement limits
- Chat model identifiers

Adjust these settings in the notebook rather than hard-coding secrets.

## Limitations

- Retrieval quality depends on the PDF content, chunk size/overlap, embeddings, retrieval settings, and re-ranking.
- The BM25 index may be built in memory each run, while the Chroma vector store persists on disk.
- The first run can require substantial time and disk space for model downloads and embeddings.
- API rate limits, model availability, network access, and local Ollama status can affect execution.
- Generated answers can still be incomplete or incorrect. Retrieval and self-correction reduce some errors but do not guarantee correctness.
- This project should not be used for diagnosis, emergency triage, or independent treatment decisions.

## Future Improvements

- Add an evaluation set and measure retrieval quality (Recall@k / MRR) and answer quality.
- Add citations with page-level evidence for every health-related claim.
- Add a small UI (for example, Streamlit) if a user-facing interface is needed.
- Add structured logging, exception handling, and automated tests.
- Use versioned configuration and pinned dependency versions for reproducible setup.

## Author

Add your name, GitHub profile, and contact details here before publishing.
