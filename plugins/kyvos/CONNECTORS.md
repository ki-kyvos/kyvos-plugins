## Connectors
 
## How tool references work
 
Plugins are **tool-agnostic** — they describe workflows in terms of categories rather than specific products. The `.mcp.json` pre-configures Kyvos MCP servers.
 
## Connectors for this plugin
 
| Included servers | Description |
|-----------------|-------------|
| Kyvos (mcp-remote via SSE) | Query Kyvos semantic models, list tables/columns, generate and execute Spark SQL |
 
## Kyvos MCP Server Tools
 
The Kyvos MCP server exposes the following tools:
 
| Tool | Description |
|------|-------------|
| `kyvos_list_semantic_models` | List all tables/semantic models available in Kyvos |
| `kyvos_list_semantic_model_columns` | List all columns for a given table and folder |
| `kyvos_sql_generation_prompt` | Get the SQL generation prompt for a table (must call before executing SQL) |
| `kyvos_execute_query` | Execute a Spark SQL query on Kyvos |