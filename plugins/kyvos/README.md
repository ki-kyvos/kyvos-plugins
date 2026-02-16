# Kyvos Plugin

A specialized plugin for [Cowork](https://claude.com/product/cowork) that connects directly to Kyvos semantic models. Query your business data using natural language, create visualizations, build dashboards, and validate analyses—all powered by Kyvos's semantic layer.


## What It Does

This plugin transforms Claude into a data analyst that works directly with your Kyvos semantic models. It understands your business context, queries the right data, and delivers insights without requiring you to write SQL or navigate complex data structures.

### Key Capabilities

- **Natural language to SQL**: Ask questions in plain English, get accurate results from Kyvos
- **Semantic model integration**: Works with your cubes, measures, and dimensions as defined in Kyvos
- **End-to-end analysis**: From data query to visualization to validation
- **Business-ready outputs**: Generates quality charts and interactive dashboards

### Requirements

**Required:**
- Kyvos MCP server connection (provides access to your semantic models)


## Commands

| Command | Description |
|---------|-------------|
| `/get-data` | Query Kyvos semantic models using natural language |
| `/analyze` | Answer data questions from quick lookups to comprehensive analyses |
| `/create-viz` | Generate quality visualizations |
| `/build-dashboard` | Build interactive HTML dashboards with charts and filters |
| `/validate` | QA an analysis before sharing—methodology, accuracy, and bias checks |
| `/discover` | Unsupervised discovery engine that scans data for interesting, non-obvious patterns analysts wouldn't think to look for |

## How It Works

### Kyvos Integration Workflow

When you ask a data question, the plugin:

1. **Discovers available models** from your Kyvos connection
2. **Selects the relevant semantic model** based on your question
3. **Retrieves generation instructions** specific to that model (including business context, SQL syntax, and query rules)
4. **Generates optimized SQL** following Kyvos requirements
5. **Executes the query** and returns results
6. **Presents insights** with context and visualizations

This workflow ensures queries are correct, efficient, and aligned with your business definitions.

## Command Details

### `/get-data` - Query Semantic Models

Query your Kyvos semantic models using natural language. The plugin handles model discovery, SQL generation according to Kyvos specifications, and query execution.

**Usage:**
```
/get-data What were the top 10 products by total sales last quarter?
/get-data Show me monthly revenue trends for 2024
/get-data Which regions had the highest growth rate year-over-year?
```

**What makes it special:**
- Always calls `kyvos_sql_generation_prompt` before generating queries to get Kyvos-specific instructions
- Follows Kyvos syntax requirements and limitations exactly
- Respects business logic and calculation rules defined in your semantic models

### `/analyze` - Comprehensive Data Analysis

Answer any data question, from simple lookups to formal reports. Integrates with Kyvos to query semantic models and deliver insights with proper validation.

**Usage:**
```
/analyze How many new users signed up in December?
/analyze What's driving the drop in conversion rate?
/analyze Prepare a quarterly business review of our subscription metrics
```

**Analysis levels:**
- **Quick answer**: Single metric with context
- **Full analysis**: Multi-dimensional exploration with trends and comparisons
- **Formal report**: Comprehensive investigation with methodology, caveats, and recommendations

### `/create-viz` - Publication-Quality Visualizations

Create professional data visualizations. Generates charts from query results or uploaded data with best practices for clarity and design.

**Usage:**
```
/create-viz Show monthly revenue for the last 12 months as a line chart
/create-viz Create a horizontal bar chart ranking products by NPS score
/create-viz Query orders table and create a heatmap of volume by day and hour
```

**Features:**
- Smart chart type selection based on data relationships
- Professional styling with colorblind-friendly palettes
- Formatted numbers (currency, percentages, abbreviated large numbers)
- Clean, publication-ready output

### `/build-dashboard` - Interactive HTML Dashboards

Build self-contained interactive dashboards that open directly in a browser. No server or dependencies required—everything embedded in a single HTML file.

**Usage:**
```
/build-dashboard Monthly sales dashboard with revenue trend, top products, and regional breakdown
/build-dashboard Support ticket dashboard showing volume by priority and response times
/build-dashboard Executive overview with MRR, churn, new customers, and NPS
```

**Dashboard components:**
- KPI cards with headline metrics
- Interactive Chart.js visualizations
- Filterable data tables
- Dropdown filters that update all components
- Professional styling with responsive layout

### `/validate` - Pre-Share Quality Assurance

Review an analysis for accuracy, methodology, and potential biases before sharing with stakeholders. Generates a confidence assessment and improvement suggestions.

**Usage:**
```
/validate Review this quarterly revenue analysis before I send it to the exec team
/validate Check my churn analysis—Q4 has a shorter measurement window than Q3
/validate Does this SQL query logic look correct for our conversion funnel?
```

**Validation checks:**
- Methodology and assumptions review
- Common analytical errors (survivorship bias, Simpson's paradox, double-counting)
- Calculation spot-checks and aggregation logic
- Visualization accuracy and clarity
- Three-level confidence assessment: Ready to share | Share with caveats | Needs revision

### `/discover` - Unsupervised Data Discovery Engine

Scan your Kyvos semantic models for interesting, non-obvious patterns that analysts wouldn't think to look for. The plugin combines semantic model understanding with targeted data sampling to surface hidden insights and present them with dynamic visualizations.

**Usage:**
```
/discover surprise me with insights from Quick Commerce data
/discover what am I missing in customer behavior last quarter?
/discover show me something interesting in sales data
/discover find hidden patterns in product performance
```

**What makes it special:**
- Intelligently explores your semantic models without requiring you to know what to ask
- Runs adaptive pattern detection (counterintuitive relationships, hidden segments, Simpson's paradox, concentration risks, emerging trends, and more)
- Validates findings to filter out noise and data quality issues
- Generates interactive React dashboards with matched visualizations for each insight
- Delivers quality over quantity: 2-3 solid, surprising insights instead of overwhelming you with trivial findings

## Example Workflows

### Quick Data Lookup

```
You: /get-data What was our total revenue last month?

Claude: [Discovers Kyvos models] → [Selects Sales cube] → [Gets generation rules]
       → [Generates and executes query] → "$2.4M in January 2025, up 12% from December"
```

### Comprehensive Analysis

```
You: /analyze Why did our conversion rate drop in Q4?

Claude: [Queries conversion funnel data] → [Breaks down by segment and channel]
       → [Identifies pattern: mobile web conversion declined 8pp]
       → [Creates trend visualization] → [Validates methodology]
       → "The Q4 drop was driven entirely by mobile web users..."
```

### Dashboard Creation

```
You: /build-dashboard Create an executive sales dashboard

Claude: [Queries revenue, pipeline, and win rate data from Kyvos]
       → [Generates HTML with embedded data and Chart.js]
       → [Includes filters for region and time period]
       → [Opens dashboard in browser]
```

### Pre-Presentation Validation

```
You: /validate [shares analysis document]

Claude: [Reviews methodology] → [Spot-checks calculations]
       → [Flags potential issue: "Churn denominator excludes trial users—
          this could overstate conversion rate by ~5pp"]
       → [Assessment: "Share with noted caveat"]
```

## Connecting Kyvos

This plugin requires a Kyvos MCP server connection. Configure your Kyvos connection in Claude Code settings or `.mcp.json`:

```json
{
  "mcpServers": {
    "kyvos-mcp": {
      "type":"http",
      "url":"<your-kyvos-mcp-server-url>"
    }
  }
}
```

Once connected, the plugin can access all your Kyvos semantic models and their business context.

## Tips for Best Results

**For queries:**
- Be specific about time ranges and segments when possible
- If you know the cube name, mention it to speed up model selection
- The plugin respects all business rules defined in your Kyvos models

**For analysis:**
- Complex questions may be broken into multiple queries—this is intentional for accuracy
- All results are validated before presentation
- Ask follow-up questions to drill deeper into findings

**For visualizations:**
- Request "interactive" for hover tooltips and zoom capabilities
- Specify "presentation" for larger fonts and higher contrast
- Charts are saved as PNG files in your working directory

**For dashboards:**
- Dashboards are point-in-time snapshots (data embedded at creation time)
- Share the HTML file with anyone—no special software needed
- Request specific color schemes to match your brand

**For validation:**
- Run `/validate` before any high-stakes presentation
- Even quick analyses benefit from a methodology check
- Validation output can be shared alongside your analysis to build stakeholder confidence

## Skills

The plugin includes six specialized skills that provide domain expertise for different aspects of data analysis:

| Skill | Description |
|-------|-------------|
| `sql-queries` | Natural language to SQL query generation for Kyvos semantic models |
| `anomaly-detector` | Statistical anomaly and outlier detection across multiple methods |
| `data-visualization` | Chart selection, visualization patterns, and design principles |
| `statistical-analysis` | Descriptive statistics, trend analysis, hypothesis testing, and interpretation |
| `interactive-dashboard-builder` | HTML/JavaScript dashboard construction with Chart.js and professional styling |
| `data-context-extractor` | Meta-skill for building domain-specific analytical capabilities from Kyvos cubes |

### sql-queries

Converts natural language questions into accurate Kyvos SQL queries. Discovers available semantic models, retrieves generation instructions, and generates SQL that respects model-specific constraints and business rules. Always calls `kyvos_sql_generation_prompt` before generating queries to ensure accuracy.

### anomaly-detector

Identifies statistical anomalies and outliers using multiple methods: Z-score (normally distributed data), IQR (robust to outliers), percentile filtering (extreme values), moving average deviation (time-series), and frequency analysis (categorical data). Never automatically removes anomalies—investigates and recommends appropriate handling.

### data-visualization

Creates publication-quality charts with Python (matplotlib, seaborn, plotly). Recommends chart types based on data relationships, applies design best practices (colorblind-friendly palettes, clear typography, accurate axes), and includes code patterns for common visualization needs. Emphasizes accessibility and honest data representation.

### statistical-analysis

Applies statistical methods for descriptive stats, trend analysis, and hypothesis testing. Focuses on practical interpretation: when to use mean vs. median, how to detect seasonality, understanding p-values and effect sizes. Includes critical thinking framework for avoiding common pitfalls (correlation vs. causation, Simpson's paradox, survivorship bias).

### interactive-dashboard-builder

Builds self-contained HTML dashboards with Chart.js visualizations, KPI cards, interactive filters, and sortable tables. All data embedded as JSON—no server required. Dashboards work offline and can be shared as a single HTML file.

### data-context-extractor

Meta-skill that extracts business context from Kyvos cubes to build domain-specific analytical capabilities. 

**Bootstrap mode** creates new domain skills by interviewing experts and documenting business logic. 
**Iteration mode** refines existing skills by adding missing context. Bridges the gap between technical schema and business terminology.
