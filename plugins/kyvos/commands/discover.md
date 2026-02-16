---
name: discover
description: >
  Unsupervised discovery engine that scans data for interesting, non-obvious patterns analysts wouldn't think to look for.
  Combines semantic model understanding with targeted data sampling to surface hidden insights with dynamic visualizations.
  Trigger: /discover or phrases like "surprise me", "show me something interesting", "what am I missing", "find hidden patterns".
---

# /discover — Unsupervised Data Discovery Engine

Scan data for interesting, non-obvious patterns that analysts wouldn't think to look for. Combine semantic model metadata with targeted data sampling to surface hidden insights and present them with compelling visualizations.

---

## When to Trigger

Activate this skill when the user says any of the following (or similar):

- `/discover`
- "Show me something interesting in [data/model]"
- "What am I missing in [area] last [period]?"
- "Find patterns I wouldn't think to look for"
- "Surprise me with insights from [model/data]"
- "What's hidden in my data?"
- "Discover something unexpected"

---

## Input Parameters

### Required
- A natural language request or the `/discover` command

### Optional (extract from user message if present)
| Parameter | Description | Examples |
|-----------|-------------|----------|
| **Focus area** | Specific metric, dimension, or business domain | "focus on customer segments", "only product performance" |
| **Time range** | Date boundaries for analysis | "last 90 days", "Q4", "last month" |
| **Scope constraints** | Specific filters to narrow exploration | "only Mumbai stores", "just electronics category" |
| **Semantic model** | Specific model to explore | "Quick Commerce data", "sales model" | 

If semantic model is not clear ask clearly.
If no parameters are specified dont assume any limitations in terms of these and consider a broader scope, for instance time range for last 6 months.
---

## Execution Flow

### Phase 1: Input Parsing & Intent Understanding

Parse the user's natural language input and extract:

1. **Target semantic model(s)** — from keywords in the query
2. **Focus area** — specific metrics, dimensions, or time range
3. **Business context keywords** — what domain the user cares about

**Example parsing:**
- "surprise me with Q4 sales insights" → Model: Sales model, Focus: Q4 timeframe, Context: sales performance
- "what am I missing in customer behavior?" → Model: best match, Focus: customer dimensions, Context: behavior patterns

### Phase 2: Semantic Model Exploration

Use the Kyvos MCP tools to understand available data:

**Step 2a — Identify relevant models:**
```
Tool: kyvos_list_semantic_models
```
- Read model names, `business_context`, and `querying_context`
- Select the model(s) that best match the user's query
- If user didn't specify, pick the most relevant model based on keywords

**Step 2b — Understand model structure:**
```
Tool: kyvos_list_semantic_model_columns (for selected model)
```
- Parse all column metadata: names, descriptions, data types
- Classify columns into:
  - **Measures** (numeric metrics that can be aggregated)
  - **Dimensions** (categorical fields to slice by)
  - **Time dimensions** (date/time fields for trend analysis)
- Build a mental map of the model's analytical surface area

**Step 2c — Identify analysis candidates:**
Based on metadata, shortlist:
- Numeric metrics worth analyzing for patterns (revenue, profit, counts, rates)
- Categorical dimensions to slice by (segments, categories, regions)
- Time dimensions for trend detection
- Column pairs that might have interesting correlations

### Phase 3: Data Depth Gauging

Run targeted sample queries to understand data characteristics BEFORE pattern detection. This prevents wasted queries and enables adaptive analysis.

**Step 3a — Temporal coverage check:**
```
Tool: kyvos_sql_generation_prompt → kyvos_execute_query
```
```sql
SELECT MIN(`date`), MAX(`date`), COUNT(DISTINCT `date`)
FROM `folder`.`model`
WHERE <user's optional time filters>
```
- Determine: How much history exists? What's the grain (daily/weekly/monthly)?

**Step 3b — Dimension cardinality check:**
For each key dimension (pick 2-3 most interesting):
```sql
SELECT `dimension_column`, COUNT(*) as records
FROM `folder`.`model`
WHERE <time_range and filters>
GROUP BY `dimension_column`
ORDER BY records DESC
LIMIT 20
```
- Determine: How many unique values? What's the distribution?

**Step 3c — Metric range check:**
For each key numeric metric (pick 2-3):
```sql
SELECT
  COUNT(*) as total_records,
  MIN(`metric`) as min_val,
  MAX(`metric`) as max_val,
  AVG(`metric`) as avg_val
FROM `folder`.`model`
WHERE <time_range and filters>
```
- Determine: What's the range? Are there likely outliers?

**Step 3d — Temporal pattern preview:**
```sql
SELECT
  DATE_FORMAT(`date`, 'yyyy-MM') as period,
  SUM(`metric1`), SUM(`metric2`)
FROM `folder`.`model`
WHERE <time_range and filters>
GROUP BY DATE_FORMAT(`date`, 'yyyy-MM')
ORDER BY period
```
- Quick look: Growing? Seasonal? Stable? Declining?

**Step 3e — Adjust strategy based on gauging results:**

| Data Characteristic | Strategy Adjustment |
|---|---|
| Sparse data (few records) | Focus on segment analysis, skip time-series |
| High cardinality dimensions | Look for long-tail / hidden segment patterns |
| Clear seasonality in preview | Include temporal pattern detection |
| Wide metric ranges | Check for outlier-driven distortions, Simpson's paradox |
| Many dimensions available | Prioritize cross-dimensional analysis |

### Phase 4: Pattern Detection (Adaptive)

Based on Phase 3 results, run **3-5 of the following pattern detectors** (not all — pick the ones most likely to yield insights given the data characteristics):

---

#### Pattern A: Counterintuitive Relationships
*Look for metrics that move opposite to expectations.*

```sql
SELECT `segment`,
       SUM(`metric_a`) as total_a,
       SUM(`metric_b`) as total_b
FROM `folder`.`model`
WHERE <filters>
GROUP BY `segment`
ORDER BY total_a DESC
```
- Flag segments where metric_a is high but metric_b is surprisingly low (or vice versa)
- Example: High revenue segment with low profit, or high volume with declining satisfaction

---

#### Pattern B: Hidden High-Value Segments
*Find small-volume segments with outsized impact.*

```sql
SELECT `dimension`,
       COUNT(*) as volume,
       SUM(`revenue_metric`) as total_value,
       SUM(`revenue_metric`) / COUNT(*) as value_per_unit
FROM `folder`.`model`
WHERE <filters>
GROUP BY `dimension`
HAVING COUNT(*) > 0
ORDER BY value_per_unit DESC
LIMIT 15
```
- Flag segments where volume is below average but value_per_unit is well above average
- These are the "small but mighty" segments analysts overlook

---

#### Pattern C: Emerging Trends (Consistent Directional Movement)
*Detect metrics moving consistently in one direction over recent periods.*

```sql
SELECT
  DATE_FORMAT(`date`, 'yyyy-MM') as month,
  SUM(`metric`) as value
FROM `folder`.`model`
WHERE <filters for last 6+ months>
GROUP BY DATE_FORMAT(`date`, 'yyyy-MM')
ORDER BY month
```
- After retrieval, analyze in-context: Are the last 3-4 periods consistently rising or falling?
- Flag any metric with 3+ consecutive periods of >5% directional change

---

#### Pattern D: Simpson's Paradox
*Check if aggregate trends contradict segment-level trends.*

**Query 1 — Overall trend:**
```sql
SELECT DATE_FORMAT(`date`, 'yyyy-MM') as period, SUM(`metric`)
FROM `folder`.`model`
WHERE <filters>
GROUP BY period
ORDER BY period
```

**Query 2 — Same metric by segment:**
```sql
SELECT DATE_FORMAT(`date`, 'yyyy-MM') as period,
       `segment_dimension`,
       SUM(`metric`)
FROM `folder`.`model`
WHERE <filters>
GROUP BY period, `segment_dimension`
ORDER BY period, `segment_dimension`
```
- Compare: Does the overall trend go UP while most/all segments go DOWN (or vice versa)?
- This is one of the most powerful "surprise" findings

---

#### Pattern E: Temporal Anomalies
*Detect unusual spikes or drops in specific time periods.*

```sql
SELECT
  DATE_FORMAT(`date`, 'yyyy-MM') as period,
  SUM(`metric`) as value
FROM `folder`.`model`
WHERE <filters>
GROUP BY DATE_FORMAT(`date`, 'yyyy-MM')
ORDER BY period
```
- After retrieval, calculate: Which periods deviate more than 1.5x from the mean?
- Flag as anomalies worth investigating

---

#### Pattern F: Concentration Risk
*Identify dangerous over-reliance on a few entities.*

```sql
SELECT `dimension`,
       SUM(`metric`) as total,
       SUM(`metric`) * 100.0 / (SELECT SUM(`metric`) FROM `folder`.`model` WHERE <filters>) as pct_of_total
FROM `folder`.`model`
WHERE <filters>
GROUP BY `dimension`
ORDER BY total DESC
LIMIT 10
```
- Flag when top 3 entities account for >60% of total (Pareto concentration)
- Business risk: losing one entity = massive impact

---

#### Pattern G: Weekend/Weekday or Time-of-Day Patterns
*Detect behavioral differences across time slices.*

```sql
SELECT `time_slice_dimension`,
       SUM(`metric`) as total,
       AVG(`metric`) as average
FROM `folder`.`model`
WHERE <filters>
GROUP BY `time_slice_dimension`
ORDER BY `time_slice_dimension`
```
- Compare weekend vs weekday, or morning vs evening
- Flag differences >20% as significant behavioral patterns

---

### Phase 5: Ranking & Filtering

After running pattern detectors, score each finding by:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Statistical Strength** | 30% | Effect size — how big is the difference/change? |
| **Business Impact** | 30% | Revenue/customer/margin implications |
| **Novelty** | 25% | Is this genuinely surprising? Not obvious from model descriptions? |
| **Actionability** | 15% | Can the user do something about it? |

**Keep:** Top 3-5 insights (quality over quantity)

**Filter out:**
- Known/obvious patterns (already described in model's business_context)
- Trivial findings driven by a single outlier data point
- Data quality issues masquerading as insights (e.g., null values causing weird averages)

### Phase 6: Validation

For each candidate insight, do a quick sanity check:

1. **Temporal robustness** — Does the pattern hold if you shift the time window slightly? (Run a quick confirming query if needed)
2. **Outlier check** — Is the finding driven by one extreme value or a consistent pattern?
3. **Plausibility** — Can you construct a reasonable business explanation?

Drop any insight that fails validation. It's better to present 2 solid insights than 5 shaky ones.

### Phase 7: Visualization & Presentation

For each validated insight, create a matched visualization. Generate a **single interactive React/HTML artifact** that presents all insights as an insight dashboard.

#### Visualization Matching Guide

| Pattern Type | Best Visualization |
|---|---|
| Counterintuitive Relationships | Diverging bar chart or dual-axis chart with annotation |
| Hidden High-Value Segments | Bubble chart (size=volume, y=value per unit) |
| Emerging Trends | Line chart with trend arrow and % change annotation |
| Simpson's Paradox | Two charts: aggregate line + segmented lines (reveal) |
| Temporal Anomalies | Line chart with highlighted anomaly bands |
| Concentration Risk | Stacked bar or treemap showing % contribution |
| Time-of-Day/Week Patterns | Heatmap or grouped bar chart |

#### Insight Card Structure

Each insight in the dashboard should include:

1. **Catchy Title** — Hook that describes the finding (e.g., "🎯 Hidden Customer Goldmine")
2. **The Finding** — 2-3 sentence plain language description
3. **Visualization** — Appropriate chart type from the guide above
4. **The Evidence** — Key numbers supporting the finding
5. **Why It Matters** — Business implication and potential action
6. **Confidence Level** — Based on data volume and validation results (Low / Medium / High)

#### Output Format

**Primary output:** Interactive React artifact (`.jsx`) with:
- Dashboard header showing model name, time range, and scope
- Insight cards with embedded Recharts visualizations
- Each card is self-contained with finding + chart + evidence + action

**Use these libraries in the React artifact:**
- `recharts` for charts (LineChart, BarChart, ScatterChart, etc.)
- Tailwind CSS for layout and styling
- `lucide-react` for icons

---

## Important Rules

1. **Always use `kyvos_sql_generation_prompt` before `kyvos_execute_query`** — This is required by the MCP server for proper SQL generation
2. **Respect Spark SQL syntax** — All queries go through Kyvos semantic layer using Spark SQL
3. **Wrap column names in backticks** — e.g., `` `store name` ``
4. **Follow querying_context from model metadata** — If the model has specific aggregation rules, obey them
5. **Don't try to profile the entire dataset** — Use targeted samples, not full scans
6. **Limit total queries to ~8-12** — Be efficient; gauging (3-4 queries) + detection (4-6 queries) + validation (1-2 queries)
7. **Quality over quantity** — 2-3 solid, validated, surprising insights beat 7 mediocre ones
8. **Present findings in business language** — No technical jargon in insight titles or descriptions
9. **Always generate a visualization artifact** — The user expects to SEE the insights, not just read them
10. **If a query fails, adapt** — Skip that pattern detector and move to the next. Don't block on errors.

---

## Example Runs

### Example 1: Broad Query
```
User: "Surprise me with insights from Quick Commerce data"

Phase 1: Model → Quick Commerce Store Analysis, Focus → all, Time → last 90 days
Phase 2: Load model columns, identify measures (revenue, profit, waste cost), dimensions (city, category, store)
Phase 3: Gauge data — 90 days available, 15 stores, 8 categories, revenue range $500-$50K/day
Phase 4: Run patterns B (hidden segments), C (trends), F (concentration)
Phase 5: Top 3 insights selected
Phase 6: Validated across time windows
Phase 7: React dashboard with 3 insight cards + charts
```

### Example 2: Focused Query
```
User: "Find something surprising about product categories in Q4"

Phase 1: Model → best match, Focus → product category dimension, Time → Q4
Phase 2: Load columns, focus on category + financial metrics
Phase 3: Gauge category cardinality (8 categories), check Q4 date range
Phase 4: Run patterns A (counterintuitive), D (Simpson's paradox on categories), E (anomalies)
Phase 5: Top 2-3 insights about category-level surprises
Phase 7: Dashboard focused on category comparisons
```

### Example 3: Risk-Focused Query
```
User: "What patterns am I missing in the last 30 days?"

Phase 1: Model → most relevant, Focus → broad, Time → last 30 days
Phase 3: Gauge — only 30 days means limited trend data
Phase 4: Focus on F (concentration risk), B (hidden segments), G (time patterns)
          Skip C (emerging trends) — not enough periods
Phase 7: Dashboard with risk-oriented insights
```

---

## Error Handling

| Scenario | Action |
|---|---|
| No semantic models found | Inform user no models are available; suggest checking Kyvos connection |
| Model has very few columns | Reduce pattern detectors to 2-3; focus on what's available |
| Query returns empty results | Skip that pattern, try next. Note in output if many queries failed |
| All patterns return nothing interesting | Be honest: "The data appears stable with no surprising patterns in this time range. Try expanding the time window or focusing on a different area." |
| SQL errors | Log the error, skip that detector, continue with remaining patterns |

---


