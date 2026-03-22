from __future__ import annotations

from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .document_store import DocumentStore


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_ROOT / "docs"
STORE = DocumentStore(DOCS_DIR)

mcp = FastMCP("mcp-docs-assistant")


@mcp.resource("docs://catalog")
def docs_catalog() -> str:
    items = STORE.list_documents()
    if not items:
        return "No documents available."

    lines = ["Available documentation:"]
    for item in items:
        lines.append(
            f"- {item['doc_id']}: {item['title']} [{item['category']}] tags={', '.join(item['tags'])}"
        )
    return "\n".join(lines)


@mcp.tool()
def list_docs() -> list[dict]:
    """List all available documents with metadata."""
    return STORE.list_documents()


@mcp.tool()
def search_docs(query: str, top_k: int = 3) -> list[dict]:
    """Search documentation using BM25 over local markdown files."""
    return STORE.search(query=query, top_k=top_k)


@mcp.tool()
def get_doc(doc_id: str) -> dict:
    """Fetch a full documentation entry by document id."""
    record = STORE.get_document(doc_id)
    if not record:
        return {"error": f"Document '{doc_id}' not found."}
    return record


@mcp.prompt()
def docs_question(question: str) -> str:
    return (
        "Use the available documentation tools to answer the user's question.\n"
        f"Question: {question}\n"
        "First search for relevant documents, then retrieve the most relevant one if necessary."
    )


def main():
    mcp.run()


if __name__ == "__main__":
    main()
