# Domain Reference File Template

Use this template when creating reference files for specific business domains (e.g., Profit and Loss, Customer Feedback).

---

```markdown
# [DOMAIN_NAME] (e.g., Profit and Loss)

This document covers the [DOMAIN_NAME] business subject, mapping business concepts to Kyvos cubes and columns.

---

## Business Context

**Purpose**: [What business questions does this domain answer? e.g., "Tracks monthly P&L across all regions"]
**Key Stakeholders**: [Who uses this data? e.g., Finance, Executive Team]

### Key Concepts & Definitions

| Concept | Definition | Kyvos Mapping (Cube.Column) |
|---------|------------|-----------------------------|
| [CONCEPT_1] | [BUSINESS_DEFINITION] | `[CUBE].[COLUMN]` |
| [CONCEPT_2] | [BUSINESS_DEFINITION] | `[CUBE].[COLUMN]` |

---

## Underlying Data Sources

This domain is primarily served by the following Kyvos cubes:

### [CUBE_NAME]
**Location**: `[folder].[semantic_model]`
**Grain**: [The lowest level of detail]

**Key Columns for this Domain**:

| Column | Type | Business Meaning | Column Context (Valid Values, Caveats) |
|--------|------|------------------|----------------------------------------|
| **[column_1]** | Measure | [DESCRIPTION] | [CONTEXT: e.g., "Pre-tax", "Includes returns"] |
| **[column_2]** | Dimension | [DESCRIPTION] | [CONTEXT: e.g., "Status '99' = Error", "Null = Unknown"] |

---

## Standard Filters & Logic

For [DOMAIN_NAME] analysis, always apply:

1. **[FILTER_NAME]**: `WHERE [COLUMN] = 'VALUE'` ([REASON])
2. **[LOGIC_NAME]**: [EXPLANATION]

---

## Common Analytical Patterns

### [PATTERN_1_NAME] (e.g., Monthly P&L Statement)
**Use Case**: [WHEN_TO_USE]

```sql
-- [Description]
SELECT
    [columns]
FROM [cube]
WHERE [standard_filters]
GROUP BY [grouping]
```

### [PATTERN_2_NAME]
**Use Case**: [WHEN_TO_USE]

```sql
[SAMPLE_QUERY]
```

---

## Common Gotchas

1. **[GOTCHA_1]**: [EXPLANATION]
   - Wrong: `[INCORRECT_APPROACH]`
   - Right: `[CORRECT_APPROACH]`

```

---

## Tips for Creating Domain Files

1. **Focus on the Business View**: Start with business concepts (e.g., "Churn"), then map to data.
2. **Define Column Context**: Don't just list columns; explain *what* is in them (valid values, null handling).
3. **Cross-Cube Context**: If a domain spans multiple cubes (e.g., Sales vs Targets), explain how they relate.
4. **Real Examples**: Use actual values and query snippets.
