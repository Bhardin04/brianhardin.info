---
title: "SQL Patterns Every Revenue Analyst Should Know"
slug: "sql-patterns-every-revenue-analyst-should-know"
excerpt: "You don't need to be a database engineer to write SQL that answers real business questions about revenue. Here are the patterns that matter most."
tags: ["SQL", "Revenue Operations", "Analytics", "Tutorial"]
published: true
featured: false
created_at: "2025-11-24"
published_at: "2025-11-24"
author: "Brian Hardin"
meta_description: "Essential SQL patterns for revenue analysts including window functions for MRR, cohort analysis, revenue waterfalls, and performance optimization."
---

Most revenue analysts I work with know basic SQL—`SELECT`, `WHERE`, `JOIN`, `GROUP BY`. That covers 70% of questions. But the interesting revenue questions require different patterns: cohort analysis, time-series calculations, cumulative metrics, change-over-time comparisons.

You don't need to be a database engineer. But mastering a few SQL patterns unlocks significantly more analytical capability. These are the patterns I use most frequently for revenue analysis.

## Window Functions for MRR Calculations

Monthly Recurring Revenue (MRR) analysis is the foundation of SaaS revenue operations. You need to track MRR over time, by customer, by product, by cohort. Window functions make this straightforward.

### Basic MRR by Customer Over Time

```sql
WITH monthly_revenue AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', invoice_date) AS month,
        SUM(amount) AS mrr
    FROM subscriptions
    WHERE status = 'active'
    GROUP BY customer_id, DATE_TRUNC('month', invoice_date)
)
SELECT
    month,
    customer_id,
    mrr,
    LAG(mrr) OVER (PARTITION BY customer_id ORDER BY month) AS prior_month_mrr,
    mrr - LAG(mrr) OVER (PARTITION BY customer_id ORDER BY month) AS mrr_change
FROM monthly_revenue
ORDER BY customer_id, month;
```

The `LAG()` function looks back to the previous row within each customer's time series. This gives you month-over-month change without complex self-joins.

### MRR Movement Categories

Understanding *why* MRR changed matters as much as knowing that it changed. Categorize movements into New, Expansion, Contraction, Churn, and Reactivation.

```sql
WITH monthly_mrr AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', invoice_date) AS month,
        SUM(amount) AS mrr
    FROM subscriptions
    WHERE status IN ('active', 'cancelled')
    GROUP BY customer_id, DATE_TRUNC('month', invoice_date)
),
mrr_with_prior AS (
    SELECT
        month,
        customer_id,
        mrr,
        LAG(mrr) OVER (PARTITION BY customer_id ORDER BY month) AS prior_mrr,
        LAG(month) OVER (PARTITION BY customer_id ORDER BY month) AS prior_month
    FROM monthly_mrr
)
SELECT
    month,
    customer_id,
    CASE
        WHEN prior_mrr IS NULL THEN 'New'
        WHEN prior_mrr > 0 AND mrr = 0 THEN 'Churn'
        WHEN prior_mrr = 0 AND mrr > 0 THEN 'Reactivation'
        WHEN mrr > prior_mrr THEN 'Expansion'
        WHEN mrr < prior_mrr THEN 'Contraction'
        ELSE 'Flat'
    END AS movement_type,
    mrr,
    prior_mrr,
    mrr - COALESCE(prior_mrr, 0) AS net_change
FROM mrr_with_prior
WHERE month >= '2024-01-01'
ORDER BY month, customer_id;
```

This categorization becomes the foundation for cohort analysis, churn analysis, and revenue waterfall reports.

## Cohort Analysis

Cohort analysis answers questions like "How does revenue from customers acquired in Q1 2024 compare to Q1 2023 cohorts?" or "What's the retention rate for enterprise vs. SMB customers?"

### Basic Retention Cohort

```sql
WITH first_purchase AS (
    SELECT
        customer_id,
        MIN(DATE_TRUNC('month', purchase_date)) AS cohort_month
    FROM orders
    GROUP BY customer_id
),
customer_activity AS (
    SELECT
        o.customer_id,
        DATE_TRUNC('month', o.purchase_date) AS activity_month,
        SUM(o.amount) AS revenue
    FROM orders o
    GROUP BY o.customer_id, DATE_TRUNC('month', o.purchase_date)
)
SELECT
    fp.cohort_month,
    ca.activity_month,
    EXTRACT(YEAR FROM AGE(ca.activity_month, fp.cohort_month)) * 12 +
    EXTRACT(MONTH FROM AGE(ca.activity_month, fp.cohort_month)) AS months_since_first,
    COUNT(DISTINCT ca.customer_id) AS active_customers,
    SUM(ca.revenue) AS cohort_revenue,
    -- Calculate as percentage of cohort size
    ROUND(
        COUNT(DISTINCT ca.customer_id)::NUMERIC /
        FIRST_VALUE(COUNT(DISTINCT ca.customer_id)) OVER (
            PARTITION BY fp.cohort_month
            ORDER BY ca.activity_month
        ) * 100,
        2
    ) AS retention_pct
FROM first_purchase fp
JOIN customer_activity ca ON fp.customer_id = ca.customer_id
GROUP BY fp.cohort_month, ca.activity_month
ORDER BY fp.cohort_month, ca.activity_month;
```

This query groups customers by acquisition month (cohort), then tracks how many remain active in subsequent months. The retention percentage shows what portion of each cohort is still generating revenue over time.

### Revenue Cohort with Cumulative Value

```sql
WITH first_purchase AS (
    SELECT
        customer_id,
        MIN(DATE_TRUNC('month', purchase_date)) AS cohort_month
    FROM orders
    GROUP BY customer_id
),
customer_revenue AS (
    SELECT
        o.customer_id,
        fp.cohort_month,
        DATE_TRUNC('month', o.purchase_date) AS activity_month,
        SUM(o.amount) AS monthly_revenue
    FROM orders o
    JOIN first_purchase fp ON o.customer_id = fp.customer_id
    GROUP BY o.customer_id, fp.cohort_month, DATE_TRUNC('month', o.purchase_date)
)
SELECT
    cohort_month,
    activity_month,
    EXTRACT(YEAR FROM AGE(activity_month, cohort_month)) * 12 +
    EXTRACT(MONTH FROM AGE(activity_month, cohort_month)) AS months_since_first,
    COUNT(DISTINCT customer_id) AS active_customers,
    SUM(monthly_revenue) AS revenue,
    SUM(SUM(monthly_revenue)) OVER (
        PARTITION BY cohort_month, customer_id
        ORDER BY activity_month
    ) AS cumulative_ltv
FROM customer_revenue
GROUP BY cohort_month, activity_month
ORDER BY cohort_month, activity_month;
```

This adds cumulative lifetime value (LTV) tracking for each cohort, showing total revenue generated per customer over time.

## Revenue Waterfall Analysis

Revenue waterfalls show how you get from one period's revenue to the next, breaking down the components of change. Essential for board reporting and revenue planning.

```sql
WITH period_revenue AS (
    SELECT
        customer_id,
        '2024-12-01'::DATE AS current_period,
        '2024-11-01'::DATE AS prior_period,
        SUM(CASE WHEN DATE_TRUNC('month', invoice_date) = '2024-12-01' THEN amount ELSE 0 END) AS current_mrr,
        SUM(CASE WHEN DATE_TRUNC('month', invoice_date) = '2024-11-01' THEN amount ELSE 0 END) AS prior_mrr
    FROM subscriptions
    WHERE DATE_TRUNC('month', invoice_date) IN ('2024-11-01', '2024-12-01')
    GROUP BY customer_id
),
categorized AS (
    SELECT
        customer_id,
        current_mrr,
        prior_mrr,
        CASE
            WHEN prior_mrr = 0 AND current_mrr > 0 THEN 'new'
            WHEN prior_mrr > 0 AND current_mrr = 0 THEN 'churn'
            WHEN current_mrr > prior_mrr THEN 'expansion'
            WHEN current_mrr < prior_mrr THEN 'contraction'
            ELSE 'flat'
        END AS category,
        current_mrr - prior_mrr AS net_change
    FROM period_revenue
)
SELECT
    category,
    COUNT(DISTINCT customer_id) AS customer_count,
    SUM(prior_mrr) AS prior_period_mrr,
    SUM(current_mrr) AS current_period_mrr,
    SUM(net_change) AS net_mrr_change,
    ROUND(SUM(net_change) / NULLIF(SUM(prior_mrr), 0) * 100, 2) AS pct_change
FROM categorized
GROUP BY category
ORDER BY
    CASE category
        WHEN 'new' THEN 1
        WHEN 'expansion' THEN 2
        WHEN 'contraction' THEN 3
        WHEN 'churn' THEN 4
        WHEN 'flat' THEN 5
    END;
```

This produces a waterfall showing starting MRR, additions from new customers, expansion from existing customers, contraction, churn, and ending MRR. Visualize this in a waterfall chart and you have executive-ready reporting.

## Running Totals and Cumulative Metrics

Revenue recognition often requires calculating cumulative totals—remaining contract value, recognized vs. deferred revenue, cumulative bookings.

### Cumulative Revenue Recognition

```sql
WITH contract_schedule AS (
    SELECT
        contract_id,
        customer_id,
        start_date,
        end_date,
        total_value,
        -- Generate a row for each month in the contract period
        generate_series(
            DATE_TRUNC('month', start_date),
            DATE_TRUNC('month', end_date),
            '1 month'::INTERVAL
        ) AS recognition_month
    FROM contracts
),
monthly_recognition AS (
    SELECT
        contract_id,
        customer_id,
        recognition_month,
        total_value / NULLIF(
            EXTRACT(MONTH FROM AGE(end_date, start_date)) + 1,
            0
        ) AS monthly_amount
    FROM contract_schedule
)
SELECT
    recognition_month,
    contract_id,
    monthly_amount,
    SUM(monthly_amount) OVER (
        PARTITION BY contract_id
        ORDER BY recognition_month
    ) AS cumulative_recognized,
    total_value - SUM(monthly_amount) OVER (
        PARTITION BY contract_id
        ORDER BY recognition_month
    ) AS remaining_deferred
FROM monthly_recognition
ORDER BY contract_id, recognition_month;
```

The `generate_series()` function is PostgreSQL-specific but incredibly useful for time-series analysis. It creates a row for each month in a date range, allowing you to allocate contract value over time.

## Performance Optimization for Large Datasets

When you're querying millions of rows, query performance matters. A few patterns make a big difference.

### Use Materialized Views for Complex Aggregations

If you're repeatedly calculating the same metrics (like MRR movement categories), materialize them.

```sql
CREATE MATERIALIZED VIEW mrr_monthly_summary AS
WITH monthly_mrr AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', invoice_date) AS month,
        SUM(amount) AS mrr
    FROM subscriptions
    WHERE status IN ('active', 'cancelled')
    GROUP BY customer_id, DATE_TRUNC('month', invoice_date)
),
mrr_with_prior AS (
    SELECT
        month,
        customer_id,
        mrr,
        LAG(mrr) OVER (PARTITION BY customer_id ORDER BY month) AS prior_mrr
    FROM monthly_mrr
)
SELECT
    month,
    customer_id,
    mrr,
    prior_mrr,
    CASE
        WHEN prior_mrr IS NULL THEN 'new'
        WHEN prior_mrr > 0 AND mrr = 0 THEN 'churn'
        WHEN mrr > prior_mrr THEN 'expansion'
        WHEN mrr < prior_mrr THEN 'contraction'
        ELSE 'flat'
    END AS movement_type,
    mrr - COALESCE(prior_mrr, 0) AS net_change
FROM mrr_with_prior;

-- Refresh nightly
CREATE INDEX idx_mrr_summary_month ON mrr_monthly_summary(month);
CREATE INDEX idx_mrr_summary_customer ON mrr_monthly_summary(customer_id);
```

Query the materialized view instead of recalculating every time. Refresh it nightly (or hourly, depending on your needs).

### Partition Large Tables by Date

If your subscription or transaction table has millions of rows spanning years, partition by month or quarter.

```sql
-- PostgreSQL 10+ declarative partitioning
CREATE TABLE subscriptions (
    subscription_id BIGINT,
    customer_id BIGINT,
    invoice_date DATE,
    amount NUMERIC(10,2),
    status VARCHAR(50)
) PARTITION BY RANGE (invoice_date);

CREATE TABLE subscriptions_2024_q1 PARTITION OF subscriptions
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE subscriptions_2024_q2 PARTITION OF subscriptions
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Queries automatically use only relevant partitions
SELECT SUM(amount)
FROM subscriptions
WHERE invoice_date >= '2024-03-01' AND invoice_date < '2024-04-01';
```

When you query March 2024, Postgres only scans the Q1 partition, not the entire table. Dramatic performance improvement for time-range queries.

### Filter Early, Aggregate Late

Push filters down to the innermost query to reduce data volume before joins and aggregations.

```sql
-- Bad: filtering after joins and aggregation
SELECT *
FROM (
    SELECT
        c.customer_id,
        c.name,
        COUNT(s.subscription_id) AS sub_count,
        SUM(s.amount) AS total_revenue
    FROM customers c
    LEFT JOIN subscriptions s ON c.customer_id = s.customer_id
    GROUP BY c.customer_id, c.name
) AS summary
WHERE total_revenue > 10000;

-- Good: filter before join
WITH high_value_customers AS (
    SELECT customer_id
    FROM subscriptions
    WHERE invoice_date >= '2024-01-01'
    GROUP BY customer_id
    HAVING SUM(amount) > 10000
)
SELECT
    c.customer_id,
    c.name,
    COUNT(s.subscription_id) AS sub_count,
    SUM(s.amount) AS total_revenue
FROM customers c
JOIN high_value_customers hvc ON c.customer_id = hvc.customer_id
LEFT JOIN subscriptions s ON c.customer_id = s.customer_id
    AND s.invoice_date >= '2024-01-01'
GROUP BY c.customer_id, c.name;
```

The second version filters to high-value customers first, then joins. Far fewer rows to process.

## Practical Tips for Revenue Analysts

**Use CTEs for readability**: Common Table Expressions (`WITH` clauses) make complex queries maintainable. Break logic into named steps.

**Always include date ranges**: Revenue queries without date filters scan entire tables. Always filter to the period you need.

**Test with small date ranges first**: Debug your logic on a single month before running it on years of data.

**Use `EXPLAIN ANALYZE`**: When a query is slow, run `EXPLAIN ANALYZE` to see where time is spent. Look for sequential scans on large tables—those need indexes.

**Window functions > self-joins**: If you're joining a table to itself for time-series comparisons, window functions are cleaner and often faster.

**Comment your queries**: Revenue logic gets complex. Comment the business logic, especially edge cases and calculations.

```sql
-- Calculate Net Dollar Retention (NDR) for each cohort
-- NDR = (Starting MRR + Expansion - Contraction - Churn) / Starting MRR
-- Excludes new customer MRR to isolate expansion/retention performance
WITH cohort_mrr AS (
    -- ... query logic
)
```

## The Bottom Line

These SQL patterns handle 90% of revenue analysis questions. MRR movements, cohort retention, revenue waterfalls, cumulative metrics—they all build on window functions, CTEs, and thoughtful aggregation.

You don't need to memorize every SQL function. But mastering these patterns gives you the toolkit to answer business questions independently, without waiting for data engineering to write custom queries.

Start with these patterns. Adapt them to your specific data model. Build a library of queries that answer your recurring questions. That's how you go from running reports to driving revenue insights.
