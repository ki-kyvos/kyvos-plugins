---
description: "Query a Kyvos semantic model using natural language"
argument-hint: "<your question about the data>"
---

# /get-data

> Requires: ~~semantic layer (Kyvos MCP server)

Query your Kyvos semantic models using natural language. This command handles the full workflow: discovering available models, selecting the right table, getting generation instructions, and executing the query.

## Workflow

1. **Discover models**: Call `kyvos_list_semantic_models` to see all available semantic models
2. **Select the right model**: Based on the user's question, identify the most relevant table
3. **Get columns**: Call `kyvos_list_semantic_model_columns` with the selected table and folder
4. **Get generation prompt**: Call `kyvos_sql_generation_prompt` with the table and folder to get specific generation instructions
5. **Generate Query**: Write the query strictly following the instructions from step 4
6. **Execute**: Call `kyvos_execute_query` with the generated query
7. **Present results**: Format the results clearly with insights

## Important Notes

- **Always** call `kyvos_sql_generation_prompt` BEFORE generating the query.
- Do not assume any specific SQL dialect (e.g., Spark SQL) unless the prompt explicitly says so.
- Follow the prompt's instructions for syntax, functions, and limitations.
- If the user's question is ambiguous, ask for clarification before querying.

## Usage

```
/get-data What were the top 10 products by total sales last quarter?
/get-data Show me monthly revenue trends for 2024
/get-data Which regions had the highest growth rate year-over-year?
```
