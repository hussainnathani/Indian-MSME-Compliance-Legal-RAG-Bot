# Indian MSME Compliance & Legal RAG Bot

AI-powered legal and compliance assistant for Indian MSMEs, built to help business owners understand complex GST, tax, and policy-related documents through plain-English questions and citation-backed answers.

## Authors
**Hussain & Yash**

---

## Overview

Indian MSMEs often struggle to navigate dense legal and compliance documents such as GST rules, tax requirements, MSME registration norms, and state-specific industrial subsidy policies. This project solves that problem by building an AI-powered legal assistant that searches real compliance documents and returns clear, summarized, and source-grounded answers.

Instead of relying on generic LLM memory, the system uses a **Retrieval-Augmented Generation (RAG)** pipeline. It retrieves the most relevant chunks from uploaded legal PDFs or curated policy data and then uses an LLM to generate an answer strictly based on that context.

---

## Features

- Ask legal and compliance questions in plain English
- Upload custom compliance PDFs for instant ingestion
- Seed a curated legal knowledge base
- Retrieve answers grounded only in provided documents
- Display source citations for transparency and trust
- Use local embeddings to avoid embedding API rate limits and reduce cost
- Modular RAG pipeline built with LangChain
- Dockerized setup for easy deployment
- Modern Streamlit chat UI with premium styling

---

## Tech Stack

### Frontend
- **Streamlit**
- Custom CSS for glassmorphism-style UI
- Chat interface with source cards and quick suggestions

### Backend
- **FastAPI**
- **Python**
- **LangChain** for document ingestion, chunking, and RAG orchestration

### Database
- **Supabase**
- **PostgreSQL**
- **pgvector** for vector similarity search

### AI Models
- **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **LLM:** `gemini-1.5-flash`

### Deployment / DevOps
- **Docker**

---

## Architecture

### 1. Document Ingestion
Users can upload PDFs or seed a pre-curated legal knowledge base. Using **LangChain**, the system extracts text from PDFs and splits large documents into smaller chunks for efficient retrieval.

### 2. Embedding Generation
Each chunk is converted into vector embeddings using the local HuggingFace model:

`sentence-transformers/all-MiniLM-L6-v2`

This keeps the embedding pipeline free from third-party embedding API costs and limits.

### 3. Storage and Retrieval
Chunks and embeddings are stored in Supabase using PostgreSQL + pgvector. When a user asks a question, the query is embedded and matched against stored vectors to retrieve the most relevant chunks.

### 4. Answer Generation
The top retrieved chunks are passed to Gemini Flash with strict instructions to answer only from the retrieved legal context and provide citations.

### 5. Containerized Deployment
The entire application can be containerized using **Docker**, making setup, local development, and deployment more consistent across environments.

---

