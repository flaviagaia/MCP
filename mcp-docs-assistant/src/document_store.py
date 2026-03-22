from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import frontmatter
from rank_bm25 import BM25Okapi


@dataclass
class DocumentRecord:
    doc_id: str
    title: str
    category: str
    tags: list[str]
    content: str
    path: Path


class DocumentStore:
    def __init__(self, docs_dir: Path):
        self.docs_dir = docs_dir
        self.documents = self._load_documents()
        self._bm25 = BM25Okapi([self._tokenize(doc.content) for doc in self.documents]) if self.documents else None

    def _load_documents(self) -> list[DocumentRecord]:
        records: list[DocumentRecord] = []
        for path in sorted(self.docs_dir.glob("*.md")):
            post = frontmatter.load(path)
            records.append(
                DocumentRecord(
                    doc_id=post.metadata["doc_id"],
                    title=post.metadata["title"],
                    category=post.metadata.get("category", "General"),
                    tags=list(post.metadata.get("tags", [])),
                    content=post.content.strip(),
                    path=path,
                )
            )
        return records

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return text.lower().replace("\n", " ").split()

    def list_documents(self) -> list[dict]:
        return [
            {
                "doc_id": doc.doc_id,
                "title": doc.title,
                "category": doc.category,
                "tags": doc.tags,
            }
            for doc in self.documents
        ]

    def get_document(self, doc_id: str) -> dict | None:
        for doc in self.documents:
            if doc.doc_id == doc_id:
                return {
                    "doc_id": doc.doc_id,
                    "title": doc.title,
                    "category": doc.category,
                    "tags": doc.tags,
                    "content": doc.content,
                }
        return None

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        if not self.documents or not self._bm25:
            return []

        scores = self._bm25.get_scores(self._tokenize(query))
        ranked = sorted(zip(self.documents, scores), key=lambda item: item[1], reverse=True)[:top_k]
        return [
            {
                "doc_id": doc.doc_id,
                "title": doc.title,
                "category": doc.category,
                "tags": doc.tags,
                "score": round(float(score), 4),
                "snippet": doc.content[:240],
            }
            for doc, score in ranked
            if score > 0
        ]
