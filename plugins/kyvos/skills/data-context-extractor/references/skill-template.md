# Generated Skill Template

Use this template when generating a new data analysis skill. Replace all `[PLACEHOLDER]` values.

---

```markdown
---
name: [company]-data-analyst
description: "[COMPANY] data analysis skill. Provides context for querying Kyvos cubes including entity definitions, metric calculations, and common query patterns. Use when analyzing [COMPANY] data for: (1) [PRIMARY_USE_CASE_1], (2) [PRIMARY_USE_CASE_2], (3) [PRIMARY_USE_CASE_3], or any data questions requiring [COMPANY]-specific context."
---

# [COMPANY] Data Analysis

## Query Generation Rules

**CRITICAL**: Always call `kyvos_sql_generation_prompt` before generating any queries. This tool provides the exact syntax, dialect, and rules required by the Kyvos MCP server.

Do not assume any specific SQL dialect (e.g., Spark SQL) unless explicitly instructed by the prompt.

---

## Entity Disambiguation

When users mention these terms, clarify which entity they mean:

[EXAMPLE FORMAT - customize based on discovery:]

**"User" can mean:**
- **Account**: An individual login/profile ([PRIMARY_CUBE]: [ID_FIELD])
- **Organization**: A billing entity that can have multiple accounts ([ORG_CUBE]: [ORG_ID])
- **[OTHER_TYPE]**: [DEFINITION] ([CUBE]: [ID])

**Relationships:**
- [ENTITY_1] → [ENTITY_2]: [RELATIONSHIP_TYPE] (join on [JOIN_KEY])

---

## Business Terminology

| Term | Definition | Notes |
|------|------------|-------|
| [TERM_1] | [DEFINITION] | [CONTEXT/GOTCHA] |
| [TERM_2] | [DEFINITION] | [CONTEXT/GOTCHA] |
| [ACRONYM] | [FULL_NAME] - [EXPLANATION] | |

---

## Standard Filters

Always apply these filters unless explicitly told otherwise:

```sql
-- Exclude test/internal data
WHERE [TEST_FLAG_COLUMN] = 'FALSE'
  AND [INTERNAL_FLAG_COLUMN] = 'FALSE'

-- Exclude invalid/fraud
  AND [STATUS_COLUMN] != '[EXCLUDED_STATUS]'

-- [OTHER STANDARD EXCLUSIONS]
```

**When to override:**
- [SCENARIO_1]: Include [NORMALLY_EXCLUDED] when [CONDITION]

---

## Key Metrics

### [METRIC_1_NAME]
- **Definition**: [PLAIN_ENGLISH_EXPLANATION]
- **Formula**: `[EXACT_CALCULATION]`
- **Source**: `[CUBE_NAME].[COLUMN_NAME]`
- **Time grain**: [DAILY/WEEKLY/MONTHLY]
- **Caveats**: [EDGE_CASES_OR_GOTCHAS]

### [METRIC_2_NAME]
[REPEAT FORMAT]

---

## Knowledge Base Navigation

Use these reference files for detailed domain documentation:

| Domain | Reference File | Use For |
|--------|----------------|---------|
| [DOMAIN_1] | `references/domains/[domain1].md` | [BRIEF_DESCRIPTION] |
| [DOMAIN_2] | `references/domains/[domain2].md` | [BRIEF_DESCRIPTION] |

---

## Common Query Patterns

### [PATTERN_1_NAME]
```sql
[SAMPLE_QUERY]
```

### [PATTERN_2_NAME]
```sql
[SAMPLE_QUERY]
```

---

## Troubleshooting

### Common Mistakes
- **[MISTAKE_1]**: [EXPLANATION] → [CORRECT_APPROACH]
- **[MISTAKE_2]**: [EXPLANATION] → [CORRECT_APPROACH]

### Access Issues
- If you encounter permission errors on `[CUBE]`: [WORKAROUND]
- For PII-restricted columns: [ALTERNATIVE_APPROACH]

### Performance Tips
- Filter by `[PARTITION_COLUMN]` first to reduce data scanned
- For large cubes, use `LIMIT` during exploration
- Prefer `[AGGREGATED_CUBE]` over `[RAW_CUBE]` when possible
```

---

## Customization Notes

When generating a skill:

1. **Fill all placeholders** - Don't leave any `[PLACEHOLDER]` text
2. **Remove unused sections** - If they don't have dashboards, remove that section
3. **Add specificity** - Generic advice is less useful than specific column names and values
4. **Include real examples** - Sample queries should use actual cube/column names
5. **Keep it scannable** - Use tables and code blocks liberally
