---
name: data-context-extractor
description: >
  Orchestrate the extraction of deep semantic context and business logic from Kyvos cubes to build domain-specific analytical skills.

  BOOTSTRAP MODE - Triggers: "Create a data context skill", "Set up analysis for our Kyvos cubes",
  "Help me create a skill for our Kyvos environment", "Generate a Kyvos data skill"
  → Performs schema introspection, profiles semantic models, and interviews domain experts to construct a knowledge base.

  ITERATION MODE - Triggers: "Add context about [domain]", "The skill needs more info about [metrics]",
  "Update the Kyvos skill with [cube/measure/dimension info]", "Improve the [domain] reference"
  → Refines existing domain models by targeting specific semantic gaps or business logic changes.

  Use when establishing a bridge between raw Kyvos semantic models and high-level business questions.
---

# Data Context Extractor

A meta-skill designed to profile Kyvos semantic models, extract company specific business knowledge, and synthesize domain-specific analytical capabilities. It treats the Kyvos cube not just as a table, but as a semantic layer requiring both **Business Context** and **Column Context** to be fully leveraged.

## Core Philosophy

Kyvos cubes are powerful, denormalized semantic structures that flatten complex joins into a single, queryable entity. While the **Kyvos MCP Server** handles the technical SQL generation (dialect, syntax, aggregation rules), this skill focuses on two layers of meaning:

1.  **Business Context (The "Why")**: Mapping technical objects to real-world business domains (e.g., P&L, Churn, Inventory).
2.  **Column Context (The "What")**: Precise definitions, valid values, and usage rules for specific measures and dimensions.

---

## How It Works

This skill has two modes:

1. **Bootstrap Mode**: Use when: User wants to create a new data context skill for their Kyvos cubes.
2. **Iteration Mode**: Improve an existing skill by adding domain-specific reference files


## Bootstrap Mode

**Objective**: Initialize a comprehensive knowledge base for a set of high-value semantic models.

### Phase 1: Semantic Model Discovery & Technical Profiling

Leverage the MCP tools to map the technical landscape before engaging stakeholders.

1. **Catalog Enumeration**: Call `kyvos_list_semantic_models` to identify available semantic domains.
2. **Target Selection**: Consult with the user to identify the "Core Business Cubes" (e.g., the 20% of cubes that answer 80% of questions).
3. **Schema Analysis**: Call `kyvos_list_semantic_model_columns` to retrieve the flat structure (measures and dimensions).
4. **Prompt Intelligence**: Call `kyvos_sql_generation_prompt` for the target cubes.
   - *Expert Note*: This prompt contains the "ground truth" for SQL generation. Analyze it to understand the cube's specific constraints (e.g., "This cube is pre-aggregated at the Monthly level").


### Phase 2: Semantic Enrichment (The Expert Interview)

Engage the domain expert to layer meaning on top of the technical schema.

**1. Domain & Scope Definition**
> "I've analyzed the `[Cube_Name]` schema. It appears to cover `[Subject]`. To structure the domain knowledge correctly:
> - What is the primary **Business Domain** this cube serves? (e.g., 'Global Supply Chain', 'Executive Finance')
> - What are the **Strategic KPIs** driven by this model?"

**2. Column Context & Dictionary (Crucial)**
> "Let's define the key columns found in the schema:
> - **Ambiguity Check**: I see `[Order Date]` and `[Ship Date]`. Which one drives revenue recognition?
> - **Status Codes**: For the `[Status]` dimension, what do values like 'X' or '99' actually mean?
> - **Measure Logic**: Is `[Sales_Amount]` pre-tax or post-tax? Does it include returns?"

**3. Dimensionality & Hierarchies**
> "The schema lists `[Dim_A]` and `[Dim_B]`.
> - In practice, what are the primary **Drill-Down Paths** analysts use?
> - Are there 'Virtual Hierarchies' that aren't explicitly defined but logically exist (e.g., Product Category -> SKU)?"

**4. The "Knowledge" Layer**
> "Every dataset has unwritten rules.
> - Are there **Standard Exclusions**? (e.g., 'Exclude internal test accounts', 'Ignore transactions before 2020')
> - Are there **Data Quality** caveats we should document? (e.g., 'Region X reporting is delayed by 2 days')"

**5. Analytical Patterns**
> "How is this data typically consumed?
> - **Trend Analysis**: Is this mostly for MoM/YoY comparisons?
> - **Cohort Analysis**: Do we track entities over time?
> - **Snapshotting**: Is this a point-in-time view?"

### Phase 3: Domain Knowledge Modeling

Synthesize the findings into a structured "Domain Knowledge Graph" (represented as files).

**Structure**:
```
[company]-kyvos-analyst/
├── SKILL.md
└── references/
    ├── domains/             # Domain-Centric Documentation
    │   ├── [business_domain_1].md  # e.g., "revenue_operations.md"
    │   ├── [business_domain_2].md  # e.g., "customer_experience.md"
    │   └── [business_domain_3].md
    └── common-patterns.md   # Cross-domain analytical patterns
```

**Templates**:
- **SKILL.md**: Use `references/skill-template.md`
- **Domain Reference**: Use `references/domain-template.md` (Focus on mapping Business Concepts → Cube Objects)

### Phase 4: Validation & Delivery

**Step 1: Semantic Verification**
> "I have modeled the `[Domain]` context. Let's validate it against a real-world scenario. Ask me a complex business question, and I will demonstrate how I map it to the Kyvos schema using the new reference files."

**Step 2: Refinement**
Adjust the domain mappings based on the test results.

**Step 3: Packaging**
Deliver the finalized skill package.

---

## Iteration Mode

**Objective**: User has an existing Kyvos skill but needs to add more context.

1. **Gap Analysis**: Analyze the failure point (e.g., "The model failed to calculate 'Net Churn' correctly").
2. **Targeted Introspection**: Re-examine the specific columns or prompt instructions involved.
3. **Logic Injection**: Update the specific `[domain].md` file with the missing business logic or concept mapping.
4. **Re-alignment**: Ensure the new logic doesn't conflict with existing patterns.

---

## Reference File Standards

### Domain Documentation (`domains/[subject].md`)
Create a **Business-to-Technical Map** that captures both high-level context and low-level column details:

- **Business Concept**: The term users say (e.g., "Gross Churn").
- **Technical Implementation**: The specific Kyvos measure/dimension + filter combination.
- **Column Context**:
    - **Definition**: Precise meaning of the column.
    - **Valid Values**: Enumeration of important categorical values.
    - **Caveats**: Null handling, data quality notes.
- **Grain Implications**: Does this concept only exist at a certain level of aggregation?
- **Cross-Cube Logic**: If the domain spans multiple cubes, explain the join/relationship logic (conceptually).

### Query Patterns
Focus on **Intent-Based Patterns**:
- "Period-over-Period Growth"
- "Contribution to Total (Part-to-Whole)"
- "Ranking & Top-N"
- "Cohort Retention"

---

## Quality Assurance Checklist

- [ ] **Business-First**: Does the documentation start with business terms?
- [ ] **Column-Precise**: Are key columns defined with specific context (not just generic names)?
- [ ] **Prompt-Aligned**: Does the skill explicitly defer SQL generation rules to the MCP prompt?
- [ ] **Context-Rich**: Are "Tribal Knowledge" filters and caveats clearly documented?
- [ ] **Actionable**: Can a user read the domain file and immediately understand *what* questions they can ask?
