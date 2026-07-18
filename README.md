# sec-rag

A production-ready Retrieval-Augmented Generation (RAG) system for parsing, indexing, and querying SEC filings (Form 10-K, 10-Q, 8-K, etc.) using clean architecture design principles.

---

## Architecture Overview

This project is built using **Clean Architecture** patterns to ensure testability, maintainability, and domain independence. 

```mermaid
graph TD
    Client[React Frontend] --> API[FastAPI Routing & Schemas]
    API --> Services[Business Services Layer]
    Services --> DBRepo[SQLAlchemy Postgres Repository]
    Services --> VecRepo[Qdrant Vector Repository]
    DBRepo --> PostgreSQL[(PostgreSQL)]
    VecRepo --> Qdrant[(Qdrant Store)]
```

### Key Architectural Guidelines
1. **Thin API layer**: Routes in `api/` are thin; they only perform request validation, authentication checks, and delegate execution to services.
2. **Decoupled Business Logic**: Core business operations (parsing, chunking, embedding, retrieval, reranking, generation, validation, evaluation) reside strictly inside standalone `services`.
3. **Repository Abstraction**: Data access logic is isolated in repositories (PostgreSQL for tabular data, Qdrant for vector data). Database libraries are hidden behind interfaces (`BaseDocumentRepository`, `BaseVectorRepository`) for easy replacement.
4. **Data Validation**: Inputs and outputs are strictly typed and validated using **Pydantic v2** models and **SQLAlchemy 2.x** mapping styles.

---

## Directory Structure

```
sec-rag/
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── api/              # API Routing Layer
│   │   │   └── v1/
│   │   │       ├── endpoints/# Thin routes (auth, documents, query)
│   │   │       └── router.py # Root route mappings
│   │   ├── core/             # App configs, logger setups, and JWT security
│   │   ├── db/               # SQLAlchemy Session generators and migrations
│   │   ├── models/           # SQLAlchemy 2.0 DB Models (User, Document, Chunks)
│   │   ├── repositories/     # Interfaces and DB repositories (Postgres, Qdrant)
│   │   ├── schemas/          # Pydantic v2 Validation Schemas
│   │   ├── services/         # 8 business logic services (parsing, chunking, etc.)
│   │   └── main.py           # Application initializer
│   ├── scripts/              # CLI execution scripts (e.g. batch embedder)
│   ├── tests/                # Unit and Integration test directories
│   ├── Dockerfile            # Multi-stage production Docker build
│   └── requirements.txt      # Python dependencies
│
├── frontend/                 # Vite + React + TypeScript App
│   ├── src/
│   │   ├── components/       # Shared UI components
│   │   ├── pages/            # Page layouts
│   │   ├── hooks/            # Custom React hooks
│   │   ├── lib/              # Client utility libraries
│   │   └── App.tsx           # Premium mockup dashboard UI
│   ├── package.json          # Node scripts and dependencies
│   └── vite.config.ts        # Vite proxy and compiler configuration
│
├── data/                     # Raw, XBRL, and processed SEC records
│   ├── raw_filings/
│   ├── xbrl/
│   └── processed/
│
├── docker-compose.yml        # Multi-container local execution setup
└── README.md                 # Project reference manual
```

---

## Setup & Running Guide

### Prerequisites
- [Docker & Docker Compose](https://www.docker.com/)
- [Python 3.11+](https://www.python.org/)
- [Node.js 18+](https://nodejs.org/)

---

### Docker Quickstart (Recommended)

1. Clone the repository and navigate to the project directory:
   ```bash
   cd sec-fillings-rag
   ```

2. Copy the backend environment sample to `.env`:
   ```bash
   cp backend/.env.example backend/.env
   ```

3. Spin up all containers (FastAPI backend, React frontend, PostgreSQL database, and Qdrant search server):
   ```bash
   docker compose up --build
   ```

4. Verify service ports:
   - **Frontend Console**: [http://localhost:5173](http://localhost:5173)
   - **FastAPI API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Qdrant Vector Dashboard**: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

---

### Running Locally (Manual Setup)

#### 1. Databases (Docker Containerized)
If running python and node locally, you can start only the databases:
```bash
docker compose up -d postgres qdrant
```

#### 2. Backend API Local Run
1. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```
2. Install python dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Create database configurations file under `backend/.env` matching your local environment variables.
4. Launch FastAPI server:
   ```bash
   uvicorn backend.app.main:app --reload
   ```

#### 3. Frontend Local Run
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Launch development server:
   ```bash
   npm run dev
   ```

---

## Environment Variables

| Variable | Description | Example / Default |
| :--- | :--- | :--- |
| `JWT_SECRET` | Security key for signing JWT tokens | `openssl rand -hex 32` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://postgres:postgres@localhost:5432/secrag` |
| `QDRANT_URL` | Qdrant vector database URL | `http://localhost:6333` |
| `QDRANT_API_KEY` | Optional security key for Qdrant | `your-qdrant-key` |
| `OPENAI_API_KEY` | OpenAI API key for Embeddings/LLM | `sk-...` |
| `GROQ_API_KEY` | Groq model endpoint token | `gsk_...` |
| `HF_TOKEN` | HuggingFace Inference API access key | `hf_...` |

---

## Future Roadmap

1. **Step 1: Document Parsing Engine**
   - Integrate structured layout extraction (e.g. Unstructured, LlamaParse) to process PDF tables and text.
2. **Step 2: Advanced Semantic Chunking**
   - Implement hierarchical section headers and table segmentation algorithms.
3. **Step 3: Vector Store Population**
   - Hook up embedding batch runs with metadata filters in Qdrant.
4. **Step 4: Reranking & Synthesis Evaluation**
   - Add Cross-Encoder models and RAGAS telemetry tracers to benchmark query grounding and latency.
