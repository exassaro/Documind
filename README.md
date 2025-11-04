# DocuMind

**Bridging AI reasoning and document understanding.**

> DocuMind enables anyone to interact with their files conversationally — **without needing cloud APIs or external dependencies**.

---

<!-- Badges (replace with real links) -->

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](#license)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](#)

## 📸 Preview

Dark, fluid, futuristic interface with glowing purple accents — built for effortless AI interaction.

![UI Preview](./assets/preview.png)

*Available: dark mode UI, inline document previews, conversational sidebar.*

---

## ✨ Key Features

* **Local-first RAG** — keep all PDFs on your machine. No cloud upload required.
* **Interactive Chat UI** — dropdown to select datasets, drag & drop PDFs, and a conversational pane with context-aware replies.
* **Privacy-first** — data/ folder ignored from git by default; easy to configure local-only storage.
* **Embeddings + Vector DB** — plug-and-play with FAISS / Chroma / Milvus (optional).
* **Modular** — swap retriever, LLM backend, or embedding model without rewriting the UI.

---

## 🧭 Quick Demo (interactive elements)

> The README shows interactive-like controls using HTML details/summary blocks and code playground links. Replace the placeholders with real URLs or GIFs.

<details>
<summary>🎛️ Demo controls — open to interact</summary>

* **Select data**: a dropdown appears in the UI to pick `data/project-a` or `data/manuals`.
* **Drag & drop**: drop PDFs into the `Upload` zone to index them instantly.
* **Chat**: type questions, reference a document, and get grounded answers with citations.

</details>

---

## 🚀 Quickstart

> These steps assume you have Python 3.8+ and Git installed.

```bash
# 1. clone the repo
git clone https://github.com/your-username/documind.git
cd documind

# 2. create venv & install
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate     # Windows
pip install -r requirements.txt

# 3. prepare data
# Put your PDFs inside the `data/` folder (this folder is ignored by git).

# 4. run the app
python -m src.app
```

Open your browser at `http://localhost:8000` (or the port printed on startup).

---

## 🧩 Features — In-UI Interactions

### Select dataset (dropdown)

The top-left UI contains a dataset selector. It lists all subfolders under `data/` and lets you switch retrieval context without re-indexing.

### Drag & drop PDF upload

Drop one or many PDF files onto the upload card. Files are stored in `data/<dataset>/raw/` and queued for indexing.

### Interactive chat

* The chat accepts **document references** using `@doc-name:page` (e.g. `@invoice-2024:3`).
* Use the `Source` toggle to show/hide inline citations and page links.

---

## 🔧 Configuration

Create a `.env` file at project root (the repo includes `.env.example`).

```env
# .env
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTOR_DB=faiss
HOST=0.0.0.0
PORT=8000
```

---

## 🔒 Security & Privacy

* **Local-only by default** — no remote APIs are required. If you enable an external LLM/backend, configure credentials in `.env` and never commit the file.
* Add `data/` and `.env` to `.gitignore` (project already includes this):

```
# .gitignore (example)
data/
.env
```

If `data/` was already tracked by Git, remove it from history with:

```bash
git rm -r --cached data/
git commit -m "Stop tracking data/"
```

> For absolute removal (history rewrite) use `git filter-repo` or `bfg` — be careful and backup first.

---

## 🧪 Indexing & Retriever

By default DocuMind provides a simple pipeline:

1. Extract text from PDFs (PyPDF2 / pdfplumber fallback).
2. Chunk text and create embeddings.
3. Store embeddings in a local vector store.

You can swap components by editing `src/pipeline.py`.

```py
# example: change embedding model
from embeddings import EmbeddingClient
client = EmbeddingClient(model="sentence-transformers/all-MiniLM-L6-v2")
```

---

## 📦 Example `requirements.txt`

```
fastapi
uvicorn
langchain
sentence-transformers
faiss-cpu
PyPDF2
python-dotenv
chromadb
tqdm
pandas
```

*Adjust the list to match your environment; use `pip freeze > requirements.txt` to pin versions.*

---

## 🧰 Developer Notes

* UI components live in `src/ui/` and are built with a lightweight framework (Vanilla + Tailwind or React — your choice).
* Backend endpoints: `POST /index`, `POST /upload`, `GET /datasets`, `POST /chat`.

---

## ♿ Accessibility

* Keyboard navigation for the chat input and dataset dropdown.
* ARIA labels for the upload zone and actionable buttons.

---

## ❓ FAQ

**Q — How do I add a new dataset?**

A — Create a new subfolder inside `data/`, add PDFs, then click `Re-scan datasets` in the UI or call `POST /index?dataset=your-dataset`.

**Q — My PDFs are already in the repo — how do I remove them from git?**

A — Add `data/` to `.gitignore` and run:

```bash
git rm -r --cached data/
git commit -m "Remove data from repo"
```

---

## 🤝 Contributing

We love contributions!

1. Fork the repo
2. Create a feature branch `git checkout -b feat/my-feature`
3. Open a PR. Include screenshots or a short GIF for UI changes.

---

## 📜 License

This project is MIT-licensed. See `LICENSE` for details.

---

## 🙋‍♂️ Need more?

If you want, I can:

* Generate a demo GIF for the README (placeholder used currently).
* Create a polished `requirements.txt` with exact version pins.
* Add a `docs/` folder with screenshots and a quick walkthrough.

---

*End of README — built for interactive-style guidance and local-first privacy.*
