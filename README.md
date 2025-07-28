# README Directory Guide for `inhouse-ai-agent`

This project follows a modular monorepo structure with separate areas for backend, frontend, automation, and AI logic. Below is a README for each major directory and sub-directory.

---

## Root Directory

Contains:

* `.env`: Environment variables template
* `README.md`: Project overview
* `docker-compose.yml`: Multi-container orchestration
* `Dockerfile.*`: Docker configuration for backend/frontend
* `scripts/`: Utility scripts (startup, ingestion)
* `models/`: Local LLM and embedding models
* `chroma/`: Chroma vector DB config and data path
* `tests/`: Automated test suites

---








---

## `/frontend`

React-based UI for the system.

### `/frontend/public`

Static assets like logos, manifest files, favicon.

### `/frontend/src`

Main app logic and views.

* `App.jsx`: Root component
* `main.jsx`: React DOM render entrypoint

#### `/frontend/src/pages`

Main pages.

* `Login.jsx`: Login form UI
* `Register.jsx`: User signup form
* `Home.jsx`: Dashboard with chat and task panels

#### `/frontend/src/components`

Reusable components.

* `ChatInterface.jsx`: Main chat screen with bot
* `FileUploader.jsx`: Upload area for documents
* `Dashboard.jsx`: Widgets showing tasks, docs, and status

#### `/frontend/src/components/Auth`

Auth-specific UI components (e.g., input forms, reset flows).

#### `/frontend/src/api`

Axios wrappers for backend API endpoints (auth, chat, files, etc).

#### `/frontend/src/context`

React Context APIs (e.g., user session provider, chat context).

---

## `/chroma`

Chroma vector DB setup.

* `chroma_config.yaml`: Collection config, embedding dims, DB location
* `startup.sh`: Run local Chroma DB server

---

## `/models`

Pre-downloaded models stored locally to avoid external calls.

* `tinyllama.gguf`: Lightweight LLM (e.g., TinyLlama 1.1B)
* `whisper-tiny.onnx`: Lightweight transcription model
* `embed_model/`: Embedding model(s) for document indexing

---

## `/scripts`

Developer and admin scripts.

* `start_dev.sh`: Launch Chroma, FastAPI, React
* `seed_users.py`: Create initial admin/test users
* `ingest_docs.py`: Script to batch ingest documents

---

## `/tests`

Unit and integration test suites.

* `test_auth.py`: Auth endpoints and flows
* `test_rag.py`: Query + retrieval testing
* `test_ingest.py`: File parsing and chunking logic
* `test_automation.py`: Action and task validation

---

This README guide can be extended with specific examples and usage patterns per module as the project evolves.

