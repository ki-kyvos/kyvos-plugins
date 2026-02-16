---
name: sql-queries
description: Answer natural language questions by generating and executing queries on Kyvos semantic models. Relies on Kyvos MCP for metadata and generation instructions.
---

# SQL Queries Skill

## Overview

This skill enables natural language querying of Kyvos semantic models. It uses the Kyvos MCP server to retrieve the necessary context and instructions to generate accurate queries without requiring pre-existing knowledge of the schema or SQL dialect.

## Workflow

### Step 1: Model Discovery and Selection

Identify the correct data source for the user's question.

1. **List Models**: Call `kyvos_list_semantic_models` to see available semantic models.
2. **Select Model**: Choose the table/folder that best matches the query intent.

### Step 2: Metadata Retrieval

Gather the necessary context to build the query.

1. **Get Columns**: Call `kyvos_list_semantic_model_columns` for the selected model.
2. **Get Generation Prompt**: Call `kyvos_sql_generation_prompt`.
   - **Critical**: This tool returns the specific instructions, required syntax, and context for generating the query.

### Step 3: Query Generation

Construct the query based *only* on the provided prompt.

- **Input**: User's natural language question + Metadata + Generation Prompt.
- **Action**: Generate the query string.
- **Rule**: Strictly follow the instructions and syntax rules provided by `kyvos_sql_generation_prompt`. Do not apply external SQL rules or assumptions.

### Step 4: Execution and Results

Run the query and present the data.

1. **Execute**: Call `kyvos_execute_query` with the generated query.
2. **Analyze**: Review the returned data.
3. **Present**: Answer the user's original question using the query results.

## Best Practices

- **Always use the Prompt**: Never generate a query without first calling `kyvos_sql_generation_prompt`.
- **Strict Adherence**: The MCP server knows the exact dialect and limitations. Follow its prompt exactly.
- **Iterative Refinement**: If execution fails, use the error message and the generation prompt to correct the query.

## Common Use Cases

1. **Ad-hoc Analysis**: Answer specific business questions on the fly (e.g., "What were sales last week?").
2. **Trend Analysis**: Show performance over time (e.g., "Show monthly revenue for 2024").
3. **Comparisons**: Compare metrics across dimensions (e.g., "Compare sales by region").
4. **Top/Bottom Analysis**: Identify best or worst performers (e.g., "Top 10 products by profit").
