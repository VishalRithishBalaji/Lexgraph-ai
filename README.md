# ⚖️ LexGraph AI: Evidence-Grounded Multi-Agent Legal Intelligence Platform

## Overview

LexGraph AI is a multi-agent legal intelligence platform that analyzes court case documents using Retrieval-Augmented Generation (RAG), local Large Language Models (LLMs), and specialized AI agents.

The system automatically extracts evidence, generates legal arguments from both defense and prosecution perspectives, identifies contradictions, builds a knowledge graph, and produces a final judicial assessment.

All processing runs locally using Ollama and Qwen, making the system private, cost-effective, and suitable for legal document analysis.

---

## Features

### 📄 PDF Case Upload

* Upload legal case documents in PDF format.
* Automatic text extraction using PyPDF.

### 🧠 Retrieval-Augmented Generation (RAG)

* ChromaDB vector database.
* Semantic search over uploaded case documents.
* Evidence retrieval for agent reasoning.

### 🤖 Multi-Agent Courtroom Simulation

#### Investigator Agent

* Extracts evidence
* Builds timelines
* Identifies witness statements
* Finds contradictions

#### Defense Lawyer Agent

* Builds defense arguments
* Highlights reasonable doubt
* Challenges evidence

#### Prosecutor Agent

* Builds prosecution case
* Connects evidence and motive
* Evaluates witness credibility

#### Contradiction Analyst Agent

* Detects inconsistencies
* Finds unsupported claims
* Evaluates risk areas

#### Knowledge Graph Agent

* Extracts entities and relationships
* Produces graph-ready JSON

#### Judge Agent

* Reviews all reports
* Evaluates evidence strength
* Produces final verdict

### 🕸 Knowledge Graph Generation

* Entity extraction
* Relationship mapping
* Visual legal network generation

### 📑 Automated Report Generation

Generates:

* Evidence Report
* Defense Report
* Prosecution Report
* Contradiction Report
* Final Judgement Report

### 📄 PDF Export

Automatic conversion of generated reports into downloadable PDF files.

### 🖥 Interactive UI

Built using Gradio for a simple browser-based workflow.

---

## Architecture

```text
PDF Upload
    │
    ▼
PyPDF Extraction
    │
    ▼
ChromaDB Vector Store
    │
    ▼
Investigator Agent
    │
    ├─────────────┐
    ▼             ▼
Defense      Prosecution
    │             │
    └──────┬──────┘
           ▼
Contradiction Analyst
           ▼
Knowledge Graph Agent
           ▼
Judge Agent
           ▼
Final Verdict
           ▼
PDF Reports + Knowledge Graph
```

---

## Tech Stack

### AI & Agent Frameworks

* CrewAI
* Ollama
* Qwen 3:4B

### RAG Stack

* ChromaDB
* Sentence Transformers

### Document Processing

* PyPDF

### Visualization

* NetworkX
* Matplotlib

### Frontend

* Gradio

### Report Generation

* ReportLab

### Programming Language

* Python 3.12

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/lexgraph-ai.git
cd lexgraph-ai
```

### Create Environment

```bash
uv sync
```

### Install Ollama

```bash
ollama pull qwen3:4b
```

### Run Application

```bash
uv run python app.py
```

---

## Demo Workflow

### Step 1

Upload a court case PDF.

### Step 2

The system extracts text and stores document chunks inside ChromaDB.

### Step 3

Investigator Agent analyzes evidence.

### Step 4

Defense and Prosecutor agents independently construct legal arguments.

### Step 5

Contradiction Analyst identifies inconsistencies.

### Step 6

Knowledge Graph Agent extracts entities and relationships.

### Step 7

Judge Agent reviews all reports and generates the final judgement.

### Step 8

PDF reports and knowledge graph are exported.

---

## Generated Outputs

```text
reports/
├── evidence_report.md
├── defense_report.md
├── prosecution_report.md
├── contradiction_report.md
├── judgement.md

├── evidence_report.pdf
├── defense_report.pdf
├── prosecution_report.pdf
├── contradiction_report.pdf
├── judgement.pdf

├── knowledge_graph.json
└── knowledge_graph.png
```

---

## Future Work

### Planned Improvements

* Citation-aware reasoning
* Evidence confidence scoring
* Multi-document case analysis
* Legal precedent retrieval
* Neo4j graph database integration
* Interactive graph visualization
* Agent memory
* Explainable AI dashboards
* Legal benchmark evaluation

---

## Project Status

✅ Working Prototype

Current Features:

* PDF Upload
* ChromaDB RAG
* Multi-Agent Reasoning
* Knowledge Graph Generation
* PDF Export
* Local LLM Deployment

---

## Author

Vishal Rithish Balaji

B.Tech Artificial Intelligence Student

Built as a portfolio project exploring:

* Agentic AI Systems
* Multi-Agent Collaboration
* Retrieval-Augmented Generation
* Legal Document Intelligence
