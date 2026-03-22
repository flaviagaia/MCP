import unittest
from pathlib import Path

from src.document_store import DocumentStore


class DocumentStoreTest(unittest.TestCase):
    def setUp(self):
        docs_dir = Path(__file__).resolve().parents[1] / "docs"
        self.store = DocumentStore(docs_dir)

    def test_list_documents(self):
        docs = self.store.list_documents()
        self.assertEqual(len(docs), 3)
        self.assertEqual(docs[0]["doc_id"], "incident-response-runbook")

    def test_get_document(self):
        doc = self.store.get_document("security-access-standard")
        self.assertIsNotNone(doc)
        self.assertIn("multi-factor authentication", doc["content"])

    def test_search_documents(self):
        results = self.store.search("How often should access be reviewed?", top_k=2)
        self.assertTrue(results)
        self.assertEqual(results[0]["doc_id"], "security-access-standard")


if __name__ == "__main__":
    unittest.main()
