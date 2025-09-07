# 🧠 Auto Doc Gen — Evidence-Grounded Technical Documentation from Any GitHub Repo

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Status](https://img.shields.io/badge/status-active-success)

> Paste a GitHub URL → get a Word-ready, **evidence-cited** handover document.  
> Local app with retrieval-augmented generation (RAG), a **judge** for factuality/citations, Mermaid→image rendering, and one-click DOCX export.

---

## ✨ Features

- **One-click docs from a repo**  
  Clone, analyze, and generate an ordered handover: **Objective & Scope → Installation & Setup → Technologies Used → System Architecture → API Key**.

- **Evidence-grounded writing**  
  Dual **FAISS** indexes (Text + Code) and **section-aware retrieval** keep claims tied to real repo content.

- **Inline citations**  
  Substantive statements cite `file:line–line` (e.g., `[app/imports.py:12–28]`). If evidence is missing, we insert **[Information not available in repository]**.

- **Quality gate (“LLM-as-judge”)**  
  A second model verifies **factuality**, **citations**, and **missing-but-expected** items; verdicts saved as JSON for audit.

- **Word-friendly diagrams**
  The app **automatically creates a Mermaid system architecture diagram**, and all Mermaid blocks are rendered to **PNG** so diagrams show up correctly in DOCX.

- **Local-first**  
  Everything runs on your machine; only embeddings/LLM calls use your configured provider key.

---

## 🏗️ System Architecture

```mermaid
flowchart LR
  subgraph Ingestion_And_Indexing
    GH[GitHub Repo] --> CL[Clone Repo]
    CL --> PC[Parse and Chunk]
    PC --> EMB[Create Embeddings]
  end

  EMB --> R[Retrieve Context]

  subgraph Agent
    R --> W[Write]
    W --> J[Judge]
    J -- pass --> S[Save]
    J -- fail --> V[Revise]
    V --> J
  end

  S --> E[End]
  Agent --> D[Generate DOCX]
```

---


## 🧩 How It Works (High Level)

1. **Ingest** — Clone the repo; collect README/docs and source code.
2. **Chunk**
   - **Text** via paragraph/heading splits
   - **Code** via **AST** (functions/classes) → precise `file:line` spans
3. **Index** — Build **two FAISS stores** (Text **and** Code) with embeddings.
4. **Generate per section** — Retrieve most relevant chunks → LLM writes **grounded** prose with inline citations.
5. **Judge** — Second LLM checks factuality, citations, and missing items; JSON verdicts saved to `app/debug/`.
6. **Assemble** — Electron merges Markdown, renders Mermaid to **PNG**, adds a **cover page** (repo title), imposes your **section order**, then converts HTML → **DOCX**.

**Artifacts saved**

- `app/docs/` — final Markdown per section
- `app/docs_index/` — FAISS stores (text_index/, code_index/)
- `app/debug/` — judge JSONs per section

---

## 📁 Project Structure

```
<your-repo>/
├─ app/
│  ├─ app.py
│  ├─ imports.py
│  ├─ chunking.py
│  ├─ graph.py
│  ├─ save_to_vector_db.py
│  ├─ sections.yaml
│  ├─ .env                  # your API keys (not committed)
├─ requirements.txt
```

---

## 🧷 Citations & Judge

- **Inline citations**:  
  `... reads env vars [app/imports.py:12–28].`
- **Missing evidence**:  
  `[Information not available in repository]` (no guessing).
- **Judge JSON (per section)**:
  ```json
  {
    "factual": true,
    "cites_ok": true,
    "hallucinated": false,
    "missing_but_expected": ["Specific environment variables..."],
    "score": 0.9,
    "notes": "..."
  }
  ```

Use these for quality gates (CI) or quick manual edits.

---



## 🛠 Tech Stack

**UI**  
Streamlit

**Python Pipeline**  
LangChain / LangGraph, FAISS, GitPython, Tiktoken, (optional) `python-docx`

**Models**  
Your provider’s embeddings + LLM (configured in `app/.env`)

---

## 🗺️ Roadmap

- **Human-in-the-Loop review** UI (approve/revise sections)
- **Interactive Docs (RAG chat)** over the indexed repo
- **Multilingual output** (bilingual DOCX/PDF)
- **Delta docs** (incremental re-runs on diffs)
- **CI integration** with quality gates (fail on low judge score)
- **Richer sections** (Testing, Data model, Security, Ops)
- **Env-var detector** to auto-build `.env.example`
- **Offline/On-prem mode** (local embeddings/LLM)
- **More diagrams** (sequence/ER diagrams)

---


> Our system differs by mining the **entire repository** with **RAG + judge**, packaging a **Word-ready** handover with rendered diagrams.

---

## 🤝 Contributing

1. Fork → create a feature branch → commit → open PR.
2. Follow PEP 8 (Python) / standard JS style.
3. Include/update docs and, if possible, a small test repo URL for validation.

---

## 📝 License

This project is released under the **MIT License**. See [LICENSE](LICENSE).

---

> **TL;DR**: Paste a GitHub URL → get a structured, evidence-cited **DOCX** handover. Local, reproducible, and audit-friendly.
