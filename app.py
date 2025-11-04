import os
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, flash, session

# Ensure imports work when running the web app
from populate_database import load_documents, split_documents, add_to_chroma
from query_data import query_rag


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = "replace-this-with-a-random-secret"

    base_dir = Path(__file__).parent.resolve()
    data_dir = base_dir / "data"
    chroma_dir = base_dir / "chroma"

    # Create necessary directories
    data_dir.mkdir(parents=True, exist_ok=True)
    chroma_dir.mkdir(parents=True, exist_ok=True)

    # Align working directory so existing scripts' relative paths ("data", "chroma") match
    os.chdir(base_dir)

    @app.get("/")
    def index():
        messages = session.get("messages", [])
        # List available PDFs
        pdf_files = sorted([f.name for f in data_dir.glob("*.pdf")])
        selected_source = session.get("selected_source", "__all__")
        return render_template("index.html", messages=messages, pdf_files=pdf_files, selected_source=selected_source)

    @app.post("/upload")
    def upload():
        if "file" not in request.files:
            flash("No file part in the request.")
            return redirect(url_for("index"))

        file = request.files["file"]
        if file.filename == "":
            flash("No file selected.")
            return redirect(url_for("index"))

        # Save into ragchatbot/data (matches populate_database expectations)
        save_path = data_dir / file.filename
        file.save(save_path)

        # Populate/Update the vector DB with all PDFs in data
        documents = load_documents()
        chunks = split_documents(documents)
        add_to_chroma(chunks)

        flash(f"Uploaded and indexed: {file.filename}")
        return redirect(url_for("index"))

    @app.post("/ask")
    def ask():
        question = request.form.get("question", "").strip()
        selected_source = request.form.get("source", "__all__")
        session["selected_source"] = selected_source
        if not question:
            flash("Please enter a question.")
            return redirect(url_for("index"))

        # Initialize / read session chat history
        messages = session.get("messages", [])
        messages.append({"role": "user", "content": question})

        # Use existing RAG query function
        source_filter = None if selected_source == "__all__" else str((data_dir / selected_source).as_posix())
        answer_text = query_rag(question, source_filter=source_filter)

        # Get sources to attach to assistant message (optional)
        try:
            from langchain_chroma import Chroma
            from get_embedding_function import get_embedding_function

            db = Chroma(persist_directory="chroma", embedding_function=get_embedding_function())
            if source_filter:
                results = db.similarity_search_with_score(question, k=5, filter={"source": source_filter})
            else:
                results = db.similarity_search_with_score(question, k=5)
            sources = [doc.metadata.get("id", None) for doc, _score in results]
        except Exception:
            sources = None

        messages.append({"role": "assistant", "content": answer_text, "sources": sources})
        session["messages"] = messages

        return redirect(url_for("index"))

    @app.post("/clear")
    def clear_chat():
        session.pop("messages", None)
        flash("Chat cleared.")
        return redirect(url_for("index"))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)


