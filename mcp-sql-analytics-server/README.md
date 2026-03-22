# mcp-sql-analytics-server

## PT-BR

Servidor MCP read-only para analytics SQL sobre uma base SQLite fictícia. O projeto expõe catálogo de tabelas, descrição de schema, métricas prontas e execução limitada de consultas `SELECT`.

### O que este projeto demonstra

- uso de MCP para acesso seguro a dados estruturados
- ferramentas analíticas read-only
- camada de proteção contra SQL destrutivo
- interface pensada para clientes MCP e assistentes de IA

### Caso de Uso

Este projeto representa um cenário em que um cliente MCP ou assistente de IA precisa consultar dados estruturados de negócio sem receber acesso irrestrito ao banco.

Em vez de expor o banco inteiro diretamente ao modelo, o servidor MCP atua como uma camada controlada de acesso. Isso permite:

- listar tabelas disponíveis;
- descrever o schema antes da consulta;
- usar métricas prontas para perguntas comuns;
- restringir consultas a operações seguras de leitura.

### Arquitetura Técnica

O pipeline do projeto é composto por quatro blocos:

1. `SQLite` como banco fictício de analytics
2. camada de seed e schema em `database.py`
3. servidor MCP com `FastMCP` em `server.py`
4. tools e resources expostos para consumo por clientes MCP

Fluxo resumido:

1. o banco é populado com dados fictícios de clientes, produtos, pedidos e itens;
2. o servidor MCP expõe ferramentas para descoberta e consulta;
3. um cliente MCP chama uma tool, como `run_metric("revenue_by_segment")`;
4. o servidor executa SQL read-only e devolve uma resposta estruturada.

### Bibliotecas e Frameworks Utilizados

- `mcp` com `FastMCP`
  Usado para implementar o servidor MCP e expor `tools`, `resources` e `prompts` de forma padronizada.
- `sqlite3`
  Usado como banco de dados local leve, sem dependência de infraestrutura externa.
- `unittest`
  Usado para validar o comportamento do schema, das métricas e das restrições de segurança.
- `Pathlib`
  Usado para manipulação de caminhos de forma portável e limpa.

### Por Que Essas Escolhas

**Por que MCP**

Porque o objetivo aqui não é só “consultar SQL”, mas mostrar como disponibilizar capacidades analíticas para um ecossistema de clientes e agentes compatíveis com `Model Context Protocol`.

**Por que SQLite**

Porque é simples de executar, portátil e ideal para demonstração local. Ele permite mostrar o padrão arquitetural sem exigir provisionamento de Postgres, credenciais ou serviços externos.

**Por que tools separadas**

Separei a interface em `list_tables`, `describe_table`, `run_readonly_query` e `run_metric` porque isso cria uma experiência mais segura e mais previsível para o cliente:

- descoberta do schema;
- entendimento da estrutura;
- execução livre, mas controlada;
- execução orientada por métricas prontas.

**Por que métricas prontas**

Porque muitos casos de uso corporativos têm perguntas recorrentes, como:

- receita por segmento;
- top produtos;
- pedidos pendentes;
- pedidos recentes.

Ter essas métricas prontas reduz erro, acelera resposta e melhora a governança da camada analítica.

### Estratégia de Segurança

O projeto foi desenhado como `read-only` por padrão.

A tool `run_readonly_query()` aceita apenas consultas `SELECT` e bloqueia instruções destrutivas como:

- `DELETE`
- `UPDATE`
- `INSERT`
- `DROP`
- `ALTER`
- `CREATE`
- `ATTACH`
- `PRAGMA`

Essa escolha é importante porque mostra uma preocupação prática com segurança de uso por agentes.

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

### O Que Pode Ser Adaptado Para Produção

Este projeto foi intencionalmente construído em cima de SQLite para demonstração, mas a mesma ideia pode ser adaptada para:

- Postgres
- MySQL
- Snowflake
- BigQuery
- outros bancos ou warehouses

Na prática, os pontos principais de adaptação seriam:

1. trocar a camada de conexão e execução SQL;
2. enriquecer as regras de segurança;
3. adicionar autenticação e autorização por ferramenta;
4. incluir logging e auditoria de consultas.

---

## EN

Read-only MCP server for SQL analytics over a fictional SQLite database. The project exposes table cataloging, schema description, predefined metrics, and limited `SELECT` query execution.

### What this project demonstrates

- MCP for secure access to structured analytics data
- read-only analytical tools
- a safety layer against destructive SQL
- an interface designed for MCP clients and AI assistants

### Use Case

This project represents a scenario where an MCP client or AI assistant needs to query structured business data without receiving unrestricted database access.

Instead of exposing the whole database directly to the model, the MCP server acts as a controlled access layer. This makes it possible to:

- list available tables;
- describe the schema before querying;
- use predefined metrics for common questions;
- restrict execution to safe read-only operations.

### Technical Architecture

The project pipeline is composed of four blocks:

1. `SQLite` as a fictional analytics database
2. schema and seed layer in `database.py`
3. MCP server built with `FastMCP` in `server.py`
4. tools and resources exposed to MCP clients

High-level flow:

1. the database is seeded with fictional customer, product, order, and order-item data;
2. the MCP server exposes discovery and query tools;
3. an MCP client calls a tool such as `run_metric("revenue_by_segment")`;
4. the server executes read-only SQL and returns a structured result.

### Libraries and Frameworks Used

- `mcp` with `FastMCP`
  Used to implement the MCP server and expose standardized `tools`, `resources`, and `prompts`.
- `sqlite3`
  Used as a lightweight local database with no external infrastructure dependency.
- `unittest`
  Used to validate schema behavior, predefined metrics, and safety restrictions.
- `pathlib`
  Used for clean and portable path handling.

### Why These Choices

**Why MCP**

Because the goal is not only to “query SQL”, but to show how analytical capabilities can be exposed to an ecosystem of MCP-compatible clients and agents.

**Why SQLite**

Because it is simple, portable, and ideal for local demos. It lets the project demonstrate the architectural pattern without requiring Postgres provisioning, credentials, or external services.

**Why separate tools**

I split the interface into `list_tables`, `describe_table`, `run_readonly_query`, and `run_metric` to create a safer and more predictable client experience:

- schema discovery;
- schema understanding;
- free but controlled query execution;
- metric-oriented execution for common analytics cases.

**Why predefined metrics**

Because many business analytics use cases revolve around recurring questions such as:

- revenue by segment;
- top products;
- pending orders;
- recent orders.

Predefined metrics reduce error, improve speed, and strengthen governance over the analytics layer.

### Safety Strategy

The project was intentionally designed as `read-only`.

The `run_readonly_query()` tool accepts only `SELECT` statements and blocks destructive instructions such as:

- `DELETE`
- `UPDATE`
- `INSERT`
- `DROP`
- `ALTER`
- `CREATE`
- `ATTACH`
- `PRAGMA`

This is an important design choice because it demonstrates practical concern for agent-safe usage.

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

### What Can Be Adapted For Production

This project intentionally uses SQLite for demonstration purposes, but the same idea can be adapted to:

- Postgres
- MySQL
- Snowflake
- BigQuery
- other databases or warehouses

In practice, the main adaptation points would be:

1. replacing the SQL connection/execution layer;
2. strengthening the security rules;
3. adding authentication and authorization per tool;
4. including query logging and auditability.
