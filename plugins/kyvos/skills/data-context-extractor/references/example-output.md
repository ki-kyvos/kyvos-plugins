# Example: Generated Skill

This is an example of what a generated skill looks like after the bootstrap process. This example is for a fictional e-commerce company called "ShopCo" using Kyvos.

---

## Example SKILL.md

```markdown
---
name: shopco-data-analyst
description: "ShopCo data analysis skill for Kyvos. Provides context for querying e-commerce data including customer, order, and product analytics. Use when analyzing ShopCo data for: (1) Revenue and order metrics, (2) Customer behavior and retention, (3) Product performance, or any data questions requiring ShopCo-specific context."
---

# ShopCo Data Analysis

## Query Generation Rules

**CRITICAL**: Always call `kyvos_sql_generation_prompt` before generating any queries. This tool provides the exact syntax, dialect, and rules required by the Kyvos MCP server.

---

## Entity Disambiguation

**"Customer" can mean:**
- **User**: A login account that can browse and save items (`ShopCo_Core`.`Users`: user_id)
- **Customer**: A user who has made at least one purchase (`ShopCo_Core`.`Customers`: customer_id)
- **Account**: A billing entity, can have multiple users in B2B (`ShopCo_Core`.`Accounts`: account_id)

---

## Business Terminology

| Term | Definition | Notes |
|------|------------|-------|
| GMV | Gross Merchandise Value - total order value before returns/discounts | Use for top-line reporting |
| NMV | Net Merchandise Value - GMV minus returns and discounts | Use for actual revenue |
| AOV | Average Order Value - NMV / order count | Exclude $0 orders |
| LTV | Lifetime Value - total NMV per customer since first order | Rolling calc, updates daily |
| CAC | Customer Acquisition Cost - marketing spend / new customers | By cohort month |

---

## Standard Filters

Always apply these filters unless explicitly told otherwise:

```sql
-- Exclude Test Data
WHERE order_status != 'TEST'
  AND customer_type != 'INTERNAL'

-- Exclude Employee Orders
  AND is_employee_order = 'FALSE'
```

---

## Knowledge Base Navigation

| Domain | Reference File | Use For |
|--------|----------------|---------|
| Revenue Operations | `references/domains/revenue.md` | GMV, NMV, Order volume, Discounts |
| Customer Retention | `references/domains/retention.md` | LTV, Churn, Cohorts, Repeat rates |
| Product Performance | `references/domains/product.md` | Inventory, Category mix, Returns analysis |

---

## Common Query Patterns

### Monthly GMV Trend
```sql
SELECT
    year_month,
    SUM(order_total_gross) as gmv
FROM `ShopCo_Core`.`Orders`
WHERE order_status NOT IN ('TEST', 'CANCELLED')
GROUP BY year_month
ORDER BY year_month
```

---

## Example references/domains/revenue.md

```markdown
# Revenue Operations

This document covers the Revenue Operations business subject, mapping financial concepts to Kyvos cubes and columns.

---

## Business Context

**Purpose**: Tracks top-line (GMV) and bottom-line (NMV) revenue performance across channels and regions.
**Key Stakeholders**: Finance, Sales Leadership, Executive Team

### Key Concepts & Definitions

| Concept | Definition | Kyvos Mapping |
|---------|------------|---------------|
| **Gross Revenue (GMV)** | Total value of orders placed, pre-discount/return | `Orders.order_total_gross` |
| **Net Revenue (NMV)** | Realized revenue after deductions | `Orders.net_revenue` |
| **Discount Rate** | Percentage of GMV given as discount | `discount_amount / order_total_gross` |

---

## Underlying Data Sources

This domain is primarily served by the following Kyvos cubes:

### Orders
**Location**: `ShopCo_Core`.`Orders`
**Grain**: Order ID (One row per order)

**Key Columns for this Domain**:

| Column | Type | Business Meaning | Column Context (Valid Values, Caveats) |
|--------|------|------------------|----------------------------------------|
| **order_total_gross** | Measure | Pre-discount order value | Includes tax in NA, excludes in EU. |
| **discount_amount** | Measure | Total discounts applied | Null if no discount. |
| **return_amount** | Measure | Value of returned items | Updates asynchronously (up to 90 days lag). |
| **order_status** | Dimension | Lifecycle state of order | Valid: 'PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED'. Filter 'TEST' out. |
| **channel** | Dimension | Sales channel | 'WEB', 'APP', 'POS'. 'POS' data delayed 24h. |

---

## Standard Filters & Logic

For Revenue analysis, always apply:

1. **Valid Orders Only**: `WHERE order_status != 'CANCELLED'` (Cancelled orders don't count for revenue)
2. **Exclude Fraud**: `WHERE fraud_flag = 'FALSE'`

---

## Common Analytical Patterns

### Monthly Revenue by Channel
**Use Case**: Executive dashboarding

```sql
SELECT
    DATE_TRUNC('month', order_date) as month,
    channel,
    SUM(order_total_gross) as gmv,
    SUM(order_total_gross - discount_amount - return_amount) as net_revenue
FROM `ShopCo_Core`.`Orders`
WHERE order_status NOT IN ('TEST', 'CANCELLED')
GROUP BY 1, 2
ORDER BY 1 DESC, 3 DESC
```
```
