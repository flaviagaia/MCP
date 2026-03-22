import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.database import seed_database  # noqa: E402
from src.server import describe_table, list_tables, run_metric, run_readonly_query  # noqa: E402


class SQLAnalyticsServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        seed_database()

    def test_list_tables(self):
        tables = list_tables()
        self.assertEqual(len(tables), 4)

    def test_describe_table(self):
        description = describe_table("orders")
        self.assertEqual(description["table"], "orders")
        self.assertTrue(any(column["name"] == "total_amount" for column in description["columns"]))

    def test_predefined_metric(self):
        result = run_metric("pending_orders")
        self.assertEqual(result["row_count"], 1)
        self.assertEqual(result["rows"][0]["pending_orders"], 2)

    def test_readonly_query_blocks_unsafe_sql(self):
        result = run_readonly_query("DELETE FROM orders")
        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
