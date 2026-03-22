# MCP

Repositório para projetos práticos com `Model Context Protocol (MCP)`.

## PT-BR

Este repositório reúne experimentos e mini-produtos construídos com MCP, com foco em casos de uso aplicados, integração com clientes compatíveis e desenho seguro de ferramentas.

## O que é MCP

`MCP` significa `Model Context Protocol`. Ele é um protocolo criado para padronizar a forma como modelos e assistentes de IA acessam contexto, ferramentas e recursos externos.

Na prática, o MCP permite que um cliente compatível converse com um servidor e descubra capacidades como:

- ferramentas (`tools`) para executar ações ou consultas;
- recursos (`resources`) para expor contexto estruturado;
- prompts reutilizáveis (`prompts`) para orientar o uso das ferramentas.

Em vez de criar integrações fechadas e específicas para cada aplicação, o MCP fornece uma interface mais padronizada para conectar modelos a sistemas reais.

## Onde MCP pode ser usado

O MCP é especialmente útil quando você quer conectar um assistente de IA a fontes de informação ou capacidades operacionais, por exemplo:

- documentação interna;
- bancos de dados e analytics;
- sistemas corporativos;
- pipelines de suporte;
- catálogos, runbooks, políticas e bases de conhecimento.

Ou seja, ele faz sentido quando o modelo precisa ir além do texto puro e acessar contexto controlado, confiável e reutilizável.

## Como pensar o uso de MCP

Uma forma simples de entender é:

1. o cliente ou assistente recebe uma pergunta;
2. ele descobre quais tools e resources estão disponíveis;
3. consulta o contexto necessário;
4. usa esse contexto para responder melhor ou executar uma tarefa de forma segura.

Isso ajuda a separar responsabilidades:

- o servidor MCP conhece os dados e as regras de acesso;
- o cliente MCP conhece a experiência do usuário;
- o modelo usa esse ecossistema para responder com mais contexto e menos improviso.

## Quando usar MCP

Vale a pena usar MCP quando você quer:

- padronizar integrações para IA;
- expor ferramentas de forma segura;
- permitir descoberta de capacidades por clientes compatíveis;
- manter a lógica de acesso perto da fonte de dados;
- reduzir acoplamento entre o modelo e sistemas internos.

Se o seu caso envolve IA com documentos, SQL, APIs internas ou workflows corporativos, MCP costuma ser uma boa escolha arquitetural.

## Como usar este repositório

Este repositório foi organizado como uma coleção de projetos independentes, cada um mostrando um padrão diferente de uso de MCP.

Se você está começando agora, a ordem mais simples é:

1. ler esta introdução;
2. abrir o `mcp-docs-assistant` para entender um caso read-only com documentação local;
3. depois abrir o `mcp-sql-analytics-server` para ver um caso de dados estruturados e analytics.

Cada projeto possui README próprio com contexto, arquitetura, ferramentas expostas e instruções de execução.

## Projetos

### `mcp-docs-assistant`

Servidor MCP read-only para busca e leitura de documentação local, com suporte a catálogo de documentos, busca BM25 e recuperação de conteúdo completo.

- pasta: [`mcp-docs-assistant`](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/MCP/mcp-docs-assistant)
- foco: documentação, governança e acesso seguro a conhecimento interno

### `mcp-sql-analytics-server`

Servidor MCP read-only para consultas analíticas em SQLite, com catálogo de tabelas, descrição de schema, métricas prontas e execução segura de `SELECT`.

- pasta: [`mcp-sql-analytics-server`](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/MCP/mcp-sql-analytics-server)
- foco: analytics, SQL, governança e acesso estruturado a dados

## Próximos projetos sugeridos

- `mcp-policy-guard`
- `mcp-github-ops-assistant`
- `mcp-multi-source-research`

---

## EN

This repository groups practical projects built with `Model Context Protocol (MCP)`, focusing on applied use cases, integration with compatible clients, and secure tool design.

## What MCP Is

`MCP` stands for `Model Context Protocol`. It is a protocol designed to standardize how models and AI assistants access context, tools, and external resources.

In practice, MCP allows a compatible client to talk to a server and discover capabilities such as:

- `tools` to perform actions or queries;
- `resources` to expose structured context;
- reusable `prompts` to guide tool usage.

Instead of building one-off integrations for each application, MCP provides a more standardized interface for connecting models to real systems.

## Where MCP Can Be Used

MCP is especially useful when you want to connect an AI assistant to information sources or operational capabilities such as:

- internal documentation;
- databases and analytics;
- enterprise systems;
- support workflows;
- catalogs, runbooks, policies, and knowledge bases.

In other words, it becomes valuable when the model needs more than plain text and must access controlled, reliable, reusable context.

## How to Think About MCP

A simple mental model is:

1. a client or assistant receives a question;
2. it discovers which tools and resources are available;
3. it retrieves the relevant context;
4. it uses that context to answer better or execute a task safely.

This separation is useful because:

- the MCP server knows the data and access rules;
- the MCP client owns the user experience;
- the model uses that ecosystem to answer with more grounding and less guesswork.

## When to Use MCP

MCP is a strong fit when you want to:

- standardize AI integrations;
- expose tools safely;
- allow compatible clients to discover capabilities;
- keep access logic close to the data source;
- reduce coupling between the model and internal systems.

If your use case involves AI over documents, SQL, internal APIs, or enterprise workflows, MCP is usually a very good architectural choice.

## How to Use This Repository

This repository is organized as a collection of independent projects, each one showing a different MCP usage pattern.

If you are new to MCP, the simplest path is:

1. read this introduction;
2. open `mcp-docs-assistant` to understand a read-only documentation use case;
3. then open `mcp-sql-analytics-server` to see a structured-data and analytics use case.

Each project has its own README with context, architecture, exposed tools, and run instructions.

## Projects

### `mcp-docs-assistant`

Read-only MCP server for searching and reading local documentation, with catalog exposure, BM25 search, and full document retrieval.

- folder: `mcp-docs-assistant`
- focus: documentation, governance, and secure access to internal knowledge

### `mcp-sql-analytics-server`

Read-only MCP server for analytics queries over SQLite, with table cataloging, schema description, predefined metrics, and safe `SELECT` execution.

- folder: `mcp-sql-analytics-server`
- focus: analytics, SQL, governance, and structured data access

## Suggested next projects

- `mcp-policy-guard`
- `mcp-github-ops-assistant`
- `mcp-multi-source-research`
