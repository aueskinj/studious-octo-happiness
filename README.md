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