---
title: "Data Pipeline Architecture for Revenue Reporting"
slug: "data-pipeline-architecture-for-revenue-reporting"
excerpt: "If your revenue reports take three days to produce, you don't have a reporting problem — you have a data architecture problem."
tags: ["Data Engineering", "Revenue Operations", "Architecture", "Python"]
published: true
featured: false
created_at: "2025-10-27"
published_at: "2025-10-27"
author: "Brian Hardin"
meta_description: "How to design data pipeline architecture for revenue reporting, from source system extraction to dashboard delivery."
---

Three years ago, our month-end revenue close took 72 hours of manual work. Accountants pulling data from six systems, copying into Excel, running macros that broke every month, and praying the formulas were right.

Today, the same reports generate automatically every night. Month-end close takes 4 hours, and most of that is review.

The difference isn't better accountants. It's better data architecture.

## The Revenue Data Problem

Revenue reporting is uniquely complex because it requires combining data from systems that were never designed to talk to each other:

- **NetSuite** — General ledger, revenue schedules, deferred revenue
- **Salesforce** — Opportunity data, contract terms, customer attributes
- **Stripe/payment processor** — Cash collections, payment methods, failed charges
- **Contract management system** — Start dates, end dates, auto-renewal terms
- **Usage tracking** — Consumption data for usage-based pricing
- **Spreadsheets** — The manual adjustments that finance swears they'll eliminate (they won't)

Each system has its own primary keys, update frequencies, data quality issues, and quirks. Your pipeline has to handle all of it.

## Architecture Principles

Before we get into code, understand these principles:

**1. Separate extraction from transformation**

Pull raw data from source systems unchanged. Don't transform during extraction. Store the raw data. Transform separately. This lets you reprocess without hitting source systems again.

**2. Make pipelines idempotent**

Running the same pipeline twice with the same input should produce the same output. Delete and reload, don't append. Use unique keys to prevent duplicates.

**3. Track lineage**

Every row in your reporting layer should trace back to source system records. Store source IDs, extraction timestamps, and pipeline run IDs.

**4. Fail loudly**

Don't silently skip errors. Don't substitute default values for missing data. Fail the pipeline and send alerts. Bad data is worse than no data.

**5. Version your transformations**

Revenue rules change (ASC 606, contract modifications, pricing changes). Keep old transformation logic versioned so you can reproduce historical reports.

## The Three-Layer Architecture

I use a three-layer architecture for revenue pipelines:

**Layer 1: Raw (Bronze)**
Exact copy of source system data, stored as-is. Immutable once written.

**Layer 2: Standardized (Silver)**
Cleaned, typed, deduplicated data with consistent schemas. Business logic applied.

**Layer 3: Reporting (Gold)**
Pre-aggregated, denormalized tables optimized for specific reports.

```
Source Systems
     ↓
[Extraction Jobs] → Layer 1: Raw
     ↓
[Standardization Jobs] → Layer 2: Standardized
     ↓
[Aggregation Jobs] → Layer 3: Reporting
     ↓
Dashboards & Reports
```

## Layer 1: Extraction Pattern

Here's a real extraction job for NetSuite revenue schedules:

```python
# extract_netsuite_revenue.py
from datetime import datetime, timedelta
import json
from pathlib import Path
from netsuite_client import NetSuiteClient
from storage import S3Storage


def extract_revenue_schedules(start_date: str, end_date: str, run_id: str):
    """
    Extract revenue schedules from NetSuite.
    Stores raw JSON in S3 with metadata.
    """

    ns = NetSuiteClient.from_env()
    storage = S3Storage(bucket="revenue-data-raw")

    # SuiteQL query for revenue schedules
    query = f"""
        SELECT
            rs.id,
            rs.revenuerecognitionrule,
            rs.revrecstartdate,
            rs.revrecenddate,
            rs.totalamount,
            rs.recognizedamount,
            rs.deferredamount,
            rs.transaction,
            rs.item,
            rs.postingperiod
        FROM
            revenueplan rs
        WHERE
            rs.revrecstartdate BETWEEN '{start_date}' AND '{end_date}'
    """

    print(f"Extracting revenue schedules from {start_date} to {end_date}")

    # Paginated extraction
    all_records = []
    offset = 0
    limit = 1000

    while True:
        paginated_query = f"{query} OFFSET {offset} LIMIT {limit}"

        try:
            response = ns.post("/services/rest/query/v1/suiteql", {"q": paginated_query})
        except Exception as e:
            print(f"Extraction failed at offset {offset}: {e}")
            raise

        records = response.get("items", [])

        if not records:
            break

        all_records.extend(records)
        print(f"Extracted {len(all_records)} records so far...")

        if len(records) < limit:
            break

        offset += limit

    # Store raw data with metadata
    extraction_metadata = {
        "source_system": "netsuite",
        "object_type": "revenue_schedule",
        "extraction_timestamp": datetime.utcnow().isoformat(),
        "run_id": run_id,
        "record_count": len(all_records),
        "start_date": start_date,
        "end_date": end_date,
        "query": query
    }

    # Write to S3 in raw layer
    date_partition = datetime.utcnow().strftime("%Y/%m/%d")
    raw_data_path = f"raw/netsuite/revenue_schedules/{date_partition}/{run_id}.json"
    metadata_path = f"raw/netsuite/revenue_schedules/{date_partition}/{run_id}_metadata.json"

    storage.write_json(raw_data_path, all_records)
    storage.write_json(metadata_path, extraction_metadata)

    print(f"Extraction complete: {len(all_records)} records stored at {raw_data_path}")

    return {
        "success": True,
        "records_extracted": len(all_records),
        "storage_path": raw_data_path
    }


if __name__ == "__main__":
    import sys

    # Run for previous day by default
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
    run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    result = extract_revenue_schedules(
        start_date=yesterday,
        end_date=yesterday,
        run_id=run_id
    )

    print(json.dumps(result, indent=2))
```

**Key elements:**

- Pagination handling (NetSuite limits results)
- Raw JSON storage (no transformation)
- Metadata tracking (when, what, how many)
- Date partitioning (for efficient querying later)
- Unique run IDs (enables reprocessing)

## Layer 2: Standardization Pattern

Layer 2 transforms raw data into clean, typed, validated data:

```python
# standardize_revenue.py
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, validator
from typing import Optional
import pandas as pd


class RevenueScheduleStandard(BaseModel):
    """
    Standardized revenue schedule model.
    Enforces types, validates data, normalizes formats.
    """
    source_system: str = "netsuite"
    source_record_id: str
    recognition_rule: str
    start_date: datetime
    end_date: datetime
    total_amount: Decimal
    recognized_amount: Decimal
    deferred_amount: Decimal
    transaction_id: str
    item_id: str
    posting_period: str
    extracted_at: datetime
    standardized_at: datetime
    run_id: str

    @validator('total_amount', 'recognized_amount', 'deferred_amount')
    def validate_amounts(cls, v):
        if v < 0:
            raise ValueError("Revenue amounts cannot be negative")
        return v

    @validator('end_date')
    def validate_date_range(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError("End date must be after start date")
        return v

    def to_dict(self):
        """Convert to dictionary with proper serialization."""
        return {
            **self.dict(),
            'total_amount': float(self.total_amount),
            'recognized_amount': float(self.recognized_amount),
            'deferred_amount': float(self.deferred_amount),
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'extracted_at': self.extracted_at.isoformat(),
            'standardized_at': self.standardized_at.isoformat()
        }


def standardize_revenue_schedules(raw_data_path: str, run_id: str):
    """
    Transform raw NetSuite revenue data into standardized format.
    """
    storage = S3Storage(bucket="revenue-data-raw")
    standardized_storage = S3Storage(bucket="revenue-data-standardized")

    # Read raw data
    raw_records = storage.read_json(raw_data_path)
    raw_metadata = storage.read_json(raw_data_path.replace('.json', '_metadata.json'))

    standardized_records = []
    errors = []

    for record in raw_records:
        try:
            # Map NetSuite fields to standardized model
            std_record = RevenueScheduleStandard(
                source_record_id=str(record['id']),
                recognition_rule=record['revenuerecognitionrule'],
                start_date=datetime.fromisoformat(record['revrecstartdate']),
                end_date=datetime.fromisoformat(record['revrecenddate']),
                total_amount=Decimal(str(record['totalamount'])),
                recognized_amount=Decimal(str(record['recognizedamount'])),
                deferred_amount=Decimal(str(record['deferredamount'])),
                transaction_id=str(record['transaction']),
                item_id=str(record['item']),
                posting_period=record['postingperiod'],
                extracted_at=datetime.fromisoformat(raw_metadata['extraction_timestamp']),
                standardized_at=datetime.utcnow(),
                run_id=run_id
            )

            standardized_records.append(std_record.to_dict())

        except Exception as e:
            errors.append({
                "source_record_id": record.get('id', 'unknown'),
                "error": str(e),
                "record": record
            })

    # Fail if error rate is too high
    error_rate = len(errors) / len(raw_records) if raw_records else 0
    if error_rate > 0.05:  # More than 5% errors
        raise Exception(
            f"Standardization error rate too high: {error_rate:.1%} "
            f"({len(errors)}/{len(raw_records)} records failed)"
        )

    # Write standardized data
    date_partition = datetime.utcnow().strftime("%Y/%m/%d")
    std_data_path = f"standardized/revenue_schedules/{date_partition}/{run_id}.json"
    error_path = f"standardized/revenue_schedules/{date_partition}/{run_id}_errors.json"

    standardized_storage.write_json(std_data_path, standardized_records)

    if errors:
        standardized_storage.write_json(error_path, errors)
        print(f"Warning: {len(errors)} records failed validation (see {error_path})")

    print(f"Standardized {len(standardized_records)} records to {std_data_path}")

    return {
        "success": True,
        "records_standardized": len(standardized_records),
        "errors": len(errors),
        "storage_path": std_data_path
    }
```

**Key elements:**

- Pydantic models enforce types and validation
- Failed records logged but don't stop pipeline (unless error rate is high)
- Decimal type for money (never use float for currency)
- Timestamps track data lineage
- Errors stored for review

## Layer 3: Aggregation for Reporting

Layer 3 creates denormalized, pre-aggregated tables for specific reports:

```python
# aggregate_monthly_revenue.py
import pandas as pd
from datetime import datetime


def aggregate_monthly_revenue(standardized_data_path: str, run_id: str):
    """
    Create monthly revenue report aggregations.
    Combines revenue schedules with contract and customer data.
    """

    storage = S3Storage(bucket="revenue-data-standardized")
    reporting_storage = S3Storage(bucket="revenue-data-reporting")

    # Load standardized data
    revenue_schedules = pd.DataFrame(storage.read_json(standardized_data_path))
    contracts = pd.DataFrame(storage.read_json("standardized/contracts/latest.json"))
    customers = pd.DataFrame(storage.read_json("standardized/customers/latest.json"))

    # Join datasets
    df = revenue_schedules.merge(
        contracts[['transaction_id', 'contract_id', 'contract_type', 'auto_renew']],
        on='transaction_id',
        how='left'
    ).merge(
        customers[['customer_id', 'customer_name', 'segment', 'region']],
        left_on='contract_id',  # Assumes contract has customer_id
        right_on='customer_id',
        how='left'
    )

    # Calculate monthly metrics
    df['month'] = pd.to_datetime(df['start_date']).dt.to_period('M')

    monthly_revenue = df.groupby(['month', 'segment', 'region']).agg({
        'total_amount': 'sum',
        'recognized_amount': 'sum',
        'deferred_amount': 'sum',
        'contract_id': 'nunique'  # Distinct contracts
    }).reset_index()

    monthly_revenue.columns = [
        'month', 'segment', 'region',
        'total_revenue', 'recognized_revenue', 'deferred_revenue',
        'contract_count'
    ]

    # Add calculated fields
    monthly_revenue['recognition_rate'] = (
        monthly_revenue['recognized_revenue'] / monthly_revenue['total_revenue']
    )

    # Convert month period to string for JSON serialization
    monthly_revenue['month'] = monthly_revenue['month'].astype(str)

    # Write to reporting layer
    report_path = f"reporting/monthly_revenue/{run_id}.json"
    reporting_storage.write_json(report_path, monthly_revenue.to_dict('records'))

    # Also write to "latest" for dashboards
    reporting_storage.write_json("reporting/monthly_revenue/latest.json",
                                monthly_revenue.to_dict('records'))

    print(f"Generated monthly revenue report: {len(monthly_revenue)} rows")

    return {
        "success": True,
        "report_rows": len(monthly_revenue),
        "storage_path": report_path
    }
```

**Key elements:**

- Joins across datasets (revenue, contracts, customers)
- Pre-aggregated metrics (sum, count, calculated fields)
- Both versioned and "latest" outputs
- Optimized for dashboard queries

## Orchestration Pattern

Tie it all together with a pipeline orchestrator:

```python
# revenue_pipeline.py
from datetime import datetime, timedelta
import logging


class RevenuePipeline:
    """
    Orchestrates end-to-end revenue reporting pipeline.
    """

    def __init__(self, run_date: str = None):
        self.run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        self.run_date = run_date or (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
        self.logger = logging.getLogger(__name__)

    def run(self):
        """Execute full pipeline."""

        self.logger.info(f"Starting revenue pipeline run {self.run_id} for {self.run_date}")

        try:
            # Step 1: Extract from all sources
            self.logger.info("Step 1: Extracting data from source systems...")
            extract_result = extract_revenue_schedules(
                start_date=self.run_date,
                end_date=self.run_date,
                run_id=self.run_id
            )
            self.logger.info(f"Extracted {extract_result['records_extracted']} revenue schedules")

            # Step 2: Standardize
            self.logger.info("Step 2: Standardizing data...")
            standardize_result = standardize_revenue_schedules(
                raw_data_path=extract_result['storage_path'],
                run_id=self.run_id
            )
            self.logger.info(f"Standardized {standardize_result['records_standardized']} records")

            # Step 3: Aggregate for reporting
            self.logger.info("Step 3: Generating reports...")
            report_result = aggregate_monthly_revenue(
                standardized_data_path=standardize_result['storage_path'],
                run_id=self.run_id
            )
            self.logger.info(f"Generated report with {report_result['report_rows']} rows")

            # Step 4: Data quality checks
            self.logger.info("Step 4: Running data quality checks...")
            quality_result = run_quality_checks(self.run_id)

            if not quality_result['passed']:
                raise Exception(f"Data quality checks failed: {quality_result['failures']}")

            self.logger.info("Pipeline completed successfully")

            return {
                "success": True,
                "run_id": self.run_id,
                "run_date": self.run_date,
                "steps": {
                    "extract": extract_result,
                    "standardize": standardize_result,
                    "report": report_result,
                    "quality": quality_result
                }
            }

        except Exception as e:
            self.logger.error(f"Pipeline failed: {e}")
            self.send_failure_alert(str(e))
            raise

    def send_failure_alert(self, error_message: str):
        """Send alert when pipeline fails."""
        # Send to Slack, PagerDuty, email, etc.
        pass


def run_quality_checks(run_id: str) -> dict:
    """
    Data quality checks for revenue data.
    """
    checks = []

    # Check 1: Total revenue matches between layers
    raw_total = get_raw_revenue_total(run_id)
    standardized_total = get_standardized_revenue_total(run_id)

    if abs(raw_total - standardized_total) > 0.01:  # Allow for rounding
        checks.append({
            "check": "revenue_total_consistency",
            "passed": False,
            "message": f"Revenue totals don't match: raw={raw_total}, std={standardized_total}"
        })
    else:
        checks.append({
            "check": "revenue_total_consistency",
            "passed": True
        })

    # Check 2: No duplicate source records
    duplicates = find_duplicate_source_records(run_id)
    if duplicates:
        checks.append({
            "check": "no_duplicates",
            "passed": False,
            "message": f"Found {len(duplicates)} duplicate records"
        })
    else:
        checks.append({
            "check": "no_duplicates",
            "passed": True
        })

    # Check 3: All records have required fields
    missing_fields = check_required_fields(run_id)
    if missing_fields:
        checks.append({
            "check": "required_fields",
            "passed": False,
            "message": f"Missing required fields: {missing_fields}"
        })
    else:
        checks.append({
            "check": "required_fields",
            "passed": True
        })

    all_passed = all(check['passed'] for check in checks)
    failures = [c['message'] for c in checks if not c['passed']]

    return {
        "passed": all_passed,
        "checks": checks,
        "failures": failures
    }
```

**Run it on a schedule:**

```bash
# Airflow DAG, cron job, or whatever scheduler you use
# Runs every night at 2 AM for previous day's data
0 2 * * * /usr/bin/python /opt/pipelines/revenue_pipeline.py
```

## Incremental vs Full Loads

**Full load:** Re-extract all data every run. Simple but slow.

**Incremental load:** Only extract changed records. Fast but complex.

For revenue reporting, I use a hybrid approach:

- **Incremental daily:** Extract only yesterday's transactions
- **Full weekly:** Re-extract last 90 days to catch updates to historical records
- **Full monthly:** Complete historical reload for month-end close

NetSuite updates historical records when accountants make adjustments. Incremental-only misses those changes.

## Handling Manual Adjustments

Finance will make manual adjustments. Always. Don't fight it.

Create a "manual adjustments" table that overlays onto your pipeline output:

```sql
-- Manual adjustments table
CREATE TABLE manual_revenue_adjustments (
    adjustment_id UUID PRIMARY KEY,
    month DATE,
    segment VARCHAR,
    adjustment_amount DECIMAL(15,2),
    reason TEXT,
    created_by VARCHAR,
    created_at TIMESTAMP,
    approved_by VARCHAR,
    approved_at TIMESTAMP
);

-- Final revenue report view
CREATE VIEW monthly_revenue_final AS
SELECT
    mr.month,
    mr.segment,
    mr.recognized_revenue + COALESCE(SUM(adj.adjustment_amount), 0) as recognized_revenue_final
FROM monthly_revenue mr
LEFT JOIN manual_revenue_adjustments adj
    ON mr.month = adj.month AND mr.segment = adj.segment
    WHERE adj.approved_at IS NOT NULL
GROUP BY mr.month, mr.segment, mr.recognized_revenue;
```

Finance gets an interface to add adjustments. The pipeline never touches them. Both systems coexist.

## Monitoring and Alerts

Know when your pipeline breaks:

```python
# alerts.py
def send_pipeline_metrics(run_id: str, metrics: dict):
    """Send metrics to monitoring system."""

    # CloudWatch, Datadog, etc.
    cloudwatch.put_metric_data(
        Namespace='RevenuePipeline',
        MetricData=[
            {
                'MetricName': 'RecordsProcessed',
                'Value': metrics['records_processed'],
                'Unit': 'Count'
            },
            {
                'MetricName': 'PipelineDuration',
                'Value': metrics['duration_seconds'],
                'Unit': 'Seconds'
            },
            {
                'MetricName': 'ErrorRate',
                'Value': metrics['error_rate'],
                'Unit': 'Percent'
            }
        ]
    )

    # Alert if error rate exceeds threshold
    if metrics['error_rate'] > 5.0:
        send_slack_alert(
            channel='#revenue-ops',
            message=f"⚠️ Revenue pipeline error rate: {metrics['error_rate']:.1f}%",
            run_id=run_id
        )
```

Set up alerts for:
- Pipeline failures
- High error rates (>5%)
- Data quality check failures
- Revenue totals outside expected range
- Missing expected source data
- Pipeline duration exceeding SLA

## The Results

After implementing this architecture:

- **Month-end close time:** 72 hours → 4 hours
- **Report accuracy:** Frequent manual errors → zero errors in 18 months
- **Data freshness:** 3 days → next morning
- **Time to new report:** 2 weeks → 2 hours
- **Team capacity:** 80% on data wrangling → 80% on analysis

The hardest part wasn't the code. It was getting finance to trust automated data over their Excel files.

We ran the pipeline in parallel with manual processes for three months. Every morning, they compared outputs. After three months of perfect matches, they stopped running the Excel process.

Now they ask for new reports that would have been impossible before.

Good data architecture doesn't just make reporting faster. It makes new analysis possible.
