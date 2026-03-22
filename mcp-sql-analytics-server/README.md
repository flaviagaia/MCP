# mcp-sql-analytics-server

## PT-BR

Servidor MCP read-only para analytics SQL sobre uma base SQLite fictícia. O projeto expõe catálogo de tabelas, descrição de schema, métricas prontas e execução limitada de consultas `SELECT`.

### O que este projeto demonstra

- uso de MCP para acesso seguro a dados estruturados
- ferramentas analíticas read-only
- camada de proteção contra SQL destrutivo
- interface pensada para clientes MCP e assistentes de IA

### Ferramentas expostas

- `list_tables()`: lista tabelas disponíveis
- `describe_table(table_name)`: descreve colunas de uma tabela
- `run_readonly_query(query)`: executa apenas `SELECT`
- `run_metric(metric_name)`: executa métricas analíticas prontas

### Resource exposto

- `analytics://schema`: catálogo textual do schema analítico

### Métricas prontas

- `revenue_by_segment`
- `top_products`
- `pending_orders`
- `recent_paid_orders`

### Segurança

O servidor bloqueia operações destrutivas e aceita apenas consultas read-only. Isso o torna mais adequado para uso em cenários de analytics assistido.

### Estrutura

- `src/database.py`: schema e seed do banco SQLite
- `src/server.py`: servidor MCP com tools e resource
- `tests/test_server.py`: testes básicos do fluxo analítico

### Como executar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
python3 src/server.py
```

---

## EN

Read-only MCP server for SQL analytics over a fictional SQLite database. The project exposes table cataloging, schema description, predefined metrics, and limited `SELECT` query execution.

### What this project demonstrates

- MCP for secure access to structured analytics data
- read-only analytical tools
- a safety layer against destructive SQL
- an interface designed for MCP clients and AI assistants

### Exposed tools

- `list_tables()`: list available tables
- `describe_table(table_name)`: describe table columns
- `run_readonly_query(query)`: execute `SELECT` only
- `run_metric(metric_name)`: execute predefined analytics metrics

### Exposed resource

- `analytics://schema`: textual analytics schema catalog

### Predefined metrics

- `revenue_by_segment`
- `top_products`
- `pending_orders`
- `recent_paid_orders`

### Safety

The server blocks destructive operations and only accepts read-only queries. This makes it more suitable for analytics-assisted scenarios.

### Structure

- `src/database.py`: SQLite schema and seed
- `src/server.py`: MCP server with tools and resource
- `tests/test_server.py`: basic analytics flow tests

### Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
python3 src/server.py
```
