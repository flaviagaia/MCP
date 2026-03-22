from __future__ import annotations

import sqlite3
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .database import DB_PATH, get_connection, seed_database


mcp = FastMCP("mcp-sql-analytics-server")

TABLE_DESCRIPTIONS = {
    "customers": "Customer master data, including name, segment, and city.",
    "products": "Product catalog with category and unit price.",
    "orders": "Order header table with status, date, and total amount.",
    "order_items": "Order line details with product, quantity, and line revenue.",
}

PREDEFINED_QUERIES = {
    "revenue_by_segment": """
        SELECT c.segment, ROUND(SUM(o.total_amount), 2) AS revenue
        FROM orders o
        JOIN customers c ON c.id = o.customer_id
        WHERE o.status = 'paid'
        GROUP BY c.segment
        ORDER BY revenue DESC
    """,
    "top_products": """
        SELECT p.name, ROUND(SUM(oi.line_total), 2) AS revenue
        FROM order_items oi
        JOIN products p ON p.id = oi.product_id
        JOIN orders o ON o.id = oi.order_id
        WHERE o.status != 'cancelled'
        GROUP BY p.name
        ORDER BY revenue DESC
        LIMIT 5
    """,
    "pending_orders": """
        SELECT COUNT(*) AS pending_orders
        FROM orders
        WHERE status = 'pending'
    """,
    "recent_paid_orders": """
        SELECT o.id, c.name, o.order_date, o.total_amount
        FROM orders o
        JOIN customers c ON c.id = o.customer_id
        WHERE o.status = 'paid'
        ORDER BY o.order_date DESC
        LIMIT 5
    """,
}


def _run_select(query: str) -> dict:
    normalized = query.strip().lower()
    if not normalized.startswith("select"):
        return {"error": "Only SELECT queries are allowed."}

    blocked = ["insert ", "update ", "delete ", "drop ", "alter ", "create ", "attach ", "pragma "]
    if any(token in normalized for token in blocked):
        return {"error": "Unsafe SQL detected. Only read-only SELECT statements are allowed."}

    connection = get_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query)
    rows = [dict(row) for row in cursor.fetchall()]
    connection.close()
    return {"rows": rows, "row_count": len(rows)}


@mcp.resource("analytics://schema")
def schema_catalog() -> str:
    lines = ["Available analytics tables:"]
    for table_name, description in TABLE_DESCRIPTIONS.items():
        lines.append(f"- {table_name}: {description}")
    return "\n".join(lines)


@mcp.tool()
def list_tables() -> list[dict]:
    """List available tables in the analytics database."""
    return [{"table": table, "description": description} for table, description in TABLE_DESCRIPTIONS.items()]


@mcp.tool()
def describe_table(table_name: str) -> dict:
    """Describe a table and its columns."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    rows = cursor.fetchall()
    connection.close()

    if not rows:
        return {"error": f"Table '{table_name}' not found."}

    return {
        "table": table_name,
        "description": TABLE_DESCRIPTIONS.get(table_name, ""),
        "columns": [
            {
                "cid": row[0],
                "name": row[1],
                "type": row[2],
                "notnull": row[3],
                "default_value": row[4],
                "pk": row[5],
            }
            for row in rows
        ],
    }


@mcp.tool()
def run_readonly_query(query: str) -> dict:
    """Run a read-only SELECT query against the analytics database."""
    return _run_select(query)


@mcp.tool()
def run_metric(metric_name: str) -> dict:
    """Run one of the predefined analytics metrics."""
    sql = PREDEFINED_QUERIES.get(metric_name)
    if not sql:
        return {"error": f"Metric '{metric_name}' not found.", "available_metrics": sorted(PREDEFINED_QUERIES)}
    return {"metric": metric_name, **_run_select(sql)}


@mcp.prompt()
def analytics_question(question: str) -> str:
    return (
        "Use the analytics tools to answer the user's question.\n"
        f"Question: {question}\n"
        "Prefer predefined metrics when appropriate. Use read-only SQL only."
    )


def main():
    if not Path(DB_PATH).exists():
        seed_database()
    mcp.run()


if __name__ == "__main__":
    main()
