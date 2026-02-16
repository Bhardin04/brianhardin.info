---
title: "Python for Finance Teams: Automating the Work Nobody Wants to Do"
slug: "python-for-finance-teams-automating-the-work-nobody-wants-to-do"
excerpt: "Your finance team spends 30% of their time on tasks a Python script could handle in seconds. Here's where to start and what to automate first."
tags: ["Python", "Automation", "Finance", "Tutorial"]
published: true
featured: false
created_at: "2025-10-06"
published_at: "2025-10-06"
author: "Brian Hardin"
meta_description: "How to use Python to automate common finance tasks like reconciliation, report generation, and data validation, with practical code examples."
---

# Python for Finance Teams: Automating the Work Nobody Wants to Do

I learned Python because I was tired of spending Friday afternoons manually reconciling Stripe payouts against our bank statements.

Every week, the same process: download CSV from Stripe, download CSV from the bank, open both in Excel, run VLOOKUP formulas, highlight discrepancies, send email to accounting. Two hours of my life I'd never get back.

Then I wrote a Python script that did the entire thing in 15 seconds.

That was five years ago. Since then, I've automated dozens of finance workflows using Python. Not because I'm a software engineer (I'm not), but because Python is the most accessible tool for turning repetitive work into automated processes.

Here's where to start and what to automate first.

## Why Python for Finance Work?

Finance teams already know Excel. Why learn something new?

Because **Excel breaks at scale**. Once you're dealing with files over 100,000 rows, multiple data sources, or repetitive monthly processes, Excel becomes the bottleneck.

Python handles:
- **Large datasets** that Excel can't open
- **Automated workflows** that run on schedule without human intervention
- **Data validation** that catches errors before they make it into reports
- **API integrations** that pull data directly from source systems
- **Reproducible processes** where the same input always produces the same output

The real advantage: **Python scripts don't get tired, don't make typos, and don't take vacation**.

## The 80/20 of Python for Finance

You don't need to master Python to automate 80% of your repetitive work. You need **three libraries** and **five patterns**.

### The Three Libraries

**1. pandas** — for working with tabular data (think Excel on steroids)
**2. openpyxl** — for reading and writing Excel files
**3. requests** — for pulling data from APIs

Install them once:

```bash
pip install pandas openpyxl requests
```

That's it. These three libraries cover 90% of finance automation use cases.

### The Five Patterns

1. **Read data from files** (CSV, Excel)
2. **Filter and transform data** (select rows, calculate columns)
3. **Merge datasets** (like VLOOKUP, but better)
4. **Validate data** (check for errors)
5. **Export results** (write to CSV or Excel)

Master these five patterns and you can automate most manual finance work.

## Use Case 1: Automating Invoice Reconciliation

**The Manual Process:**

Every month, your finance team downloads invoices from the billing system, matches them against revenue records in the ERP, and flags discrepancies for review.

**Time Required:** 4-6 hours/month

**The Automated Process:**

A Python script reads both datasets, matches records based on invoice ID, flags discrepancies, and generates a report.

**Time Required:** 30 seconds

### The Code

```python
import pandas as pd

# Read data from CSV files
billing_data = pd.read_csv('billing_invoices.csv')
erp_data = pd.read_csv('erp_revenue.csv')

# Standardize column names (common pain point)
billing_data.columns = billing_data.columns.str.strip().str.lower()
erp_data.columns = erp_data.columns.str.strip().str.lower()

# Merge datasets on invoice_id
merged = billing_data.merge(
    erp_data,
    on='invoice_id',
    how='outer',
    suffixes=('_billing', '_erp'),
    indicator=True
)

# Identify discrepancies
discrepancies = merged[
    (merged['_merge'] != 'both') |
    (merged['amount_billing'] != merged['amount_erp'])
]

# Export results
discrepancies.to_csv('invoice_discrepancies.csv', index=False)

print(f"Found {len(discrepancies)} discrepancies")
print("Report saved to invoice_discrepancies.csv")
```

### What This Does

1. **Reads two CSV files** — one from billing, one from ERP
2. **Cleans column names** (removes spaces, converts to lowercase) to avoid matching errors
3. **Merges datasets** using `invoice_id` as the key (like VLOOKUP, but handles duplicates better)
4. **Flags discrepancies** — invoices that exist in one system but not the other, or where amounts don't match
5. **Exports results** to a new CSV for review

**Time Saved:** 4-6 hours/month → 30 seconds

## Use Case 2: Generating Executive Reports from Multiple Sources

**The Manual Process:**

Every Monday morning, you pull revenue metrics from Salesforce, billing data from Stripe, and expense data from NetSuite. You copy-paste each into an Excel template, calculate growth rates, and email to leadership.

**Time Required:** 2 hours/week (100+ hours/year)

**The Automated Process:**

A Python script pulls data from each system's API, combines it, calculates metrics, and generates a formatted Excel report.

**Time Required:** Run once on Monday morning, 10 seconds

### The Code

```python
import pandas as pd
import requests
from datetime import datetime, timedelta

# Define time period (last 30 days)
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# Pull Salesforce data (simplified - actual implementation uses OAuth)
sf_response = requests.get(
    'https://your-instance.salesforce.com/services/data/v59.0/query',
    headers={'Authorization': f'Bearer {SALESFORCE_TOKEN}'},
    params={'q': 'SELECT Amount, CloseDate FROM Opportunity WHERE CloseDate >= ' + start_date.strftime('%Y-%m-%d')}
)
opportunities = pd.DataFrame(sf_response.json()['records'])

# Pull Stripe data
stripe_response = requests.get(
    'https://api.stripe.com/v1/charges',
    headers={'Authorization': f'Bearer {STRIPE_API_KEY}'},
    params={'created[gte]': int(start_date.timestamp())}
)
charges = pd.DataFrame(stripe_response.json()['data'])

# Calculate metrics
total_revenue = opportunities['Amount'].sum()
total_charges = charges['amount'].sum() / 100  # Stripe amounts are in cents
average_deal_size = opportunities['Amount'].mean()

# Build summary DataFrame
summary = pd.DataFrame({
    'Metric': ['Total Revenue (Closed/Won)', 'Total Charges (Stripe)', 'Average Deal Size', 'Deal Count'],
    'Value': [
        f'${total_revenue:,.2f}',
        f'${total_charges:,.2f}',
        f'${average_deal_size:,.2f}',
        len(opportunities)
    ]
})

# Export to Excel with formatting
with pd.ExcelWriter('weekly_revenue_report.xlsx', engine='openpyxl') as writer:
    summary.to_excel(writer, sheet_name='Summary', index=False)
    opportunities.to_excel(writer, sheet_name='Opportunities', index=False)
    charges.to_excel(writer, sheet_name='Charges', index=False)

print("Report generated: weekly_revenue_report.xlsx")
```

### What This Does

1. **Pulls data from multiple APIs** (Salesforce, Stripe)
2. **Calculates key metrics** (totals, averages, counts)
3. **Formats results** into a clean summary table
4. **Exports to Excel** with multiple sheets (summary + raw data)

**Time Saved:** 100+ hours/year

### Making It Better

Once this works, you can improve it:

- **Schedule it to run automatically** using cron (Mac/Linux) or Task Scheduler (Windows)
- **Email the report** using Python's `smtplib` library
- **Add charts** using `openpyxl` or `xlsxwriter`
- **Store credentials securely** using environment variables or a secrets manager

## Use Case 3: Data Validation Before Import

**The Manual Process:**

Your team receives customer data from Sales to import into the billing system. Before import, you manually check for:
- Missing required fields
- Invalid email formats
- Duplicate customer IDs
- Amounts that don't match contracts

If anything is wrong, you email Sales and ask them to fix it. This process repeats 3-4 times before the data is clean.

**Time Required:** 1-2 hours per import cycle, 2-3 cycles to get it right

**The Automated Process:**

A Python script validates the data in seconds and generates a report of all errors with specific line numbers and descriptions.

**Time Required:** 10 seconds

### The Code

```python
import pandas as pd
import re

def validate_customer_data(file_path):
    """Validate customer import file and return list of errors"""

    # Read data
    df = pd.read_csv(file_path)
    errors = []

    # Check for missing required fields
    required_fields = ['customer_id', 'customer_name', 'email', 'amount']
    for field in required_fields:
        missing = df[df[field].isna()]
        if len(missing) > 0:
            errors.append({
                'error_type': 'Missing Required Field',
                'field': field,
                'rows': missing.index.tolist(),
                'count': len(missing)
            })

    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    invalid_emails = df[~df['email'].str.match(email_pattern, na=False)]
    if len(invalid_emails) > 0:
        errors.append({
            'error_type': 'Invalid Email Format',
            'field': 'email',
            'rows': invalid_emails.index.tolist(),
            'count': len(invalid_emails)
        })

    # Check for duplicates
    duplicates = df[df.duplicated(subset=['customer_id'], keep=False)]
    if len(duplicates) > 0:
        errors.append({
            'error_type': 'Duplicate Customer ID',
            'field': 'customer_id',
            'rows': duplicates.index.tolist(),
            'count': len(duplicates)
        })

    # Check for negative amounts
    negative_amounts = df[df['amount'] < 0]
    if len(negative_amounts) > 0:
        errors.append({
            'error_type': 'Negative Amount',
            'field': 'amount',
            'rows': negative_amounts.index.tolist(),
            'count': len(negative_amounts)
        })

    return errors

# Run validation
errors = validate_customer_data('customer_import.csv')

if len(errors) == 0:
    print("✓ All validation checks passed. File is ready for import.")
else:
    print(f"✗ Found {len(errors)} validation errors:\n")
    for error in errors:
        print(f"  {error['error_type']}: {error['field']}")
        print(f"    Affected rows: {error['rows'][:10]}...")  # Show first 10 rows
        print(f"    Total count: {error['count']}\n")

    # Export errors to CSV for review
    errors_df = pd.DataFrame(errors)
    errors_df.to_csv('validation_errors.csv', index=False)
    print("Full error report saved to validation_errors.csv")
```

### What This Does

1. **Reads the import file**
2. **Checks for missing required fields** (customer_id, name, email, amount)
3. **Validates email format** using regex
4. **Detects duplicate customer IDs**
5. **Flags negative amounts** (usually an error)
6. **Generates detailed error report** with row numbers

**Time Saved:** Multiple hours per import cycle, eliminates back-and-forth with Sales

### Extending This Pattern

This validation pattern is reusable. Once you have it working, you can:

- Add more validation rules (phone numbers, ZIP codes, currency codes)
- Check against external data sources (does this customer exist in the CRM?)
- Validate data relationships (does the amount match the contract value?)
- Auto-fix common errors (standardize state names, strip whitespace)

## Getting Started: Your First Automation Project

If you're new to Python, here's how to pick your first project:

### Step 1: Identify a Painful, Repetitive Task

Look for tasks that:
- **Happen weekly or monthly** (high return on time invested)
- **Follow a clear process** (if you can write down the steps, you can automate it)
- **Involve structured data** (CSV files, Excel spreadsheets, database exports)

Good first projects:
- Reconciling two datasets
- Generating a report from multiple files
- Data validation before import
- Summarizing transaction logs

Bad first projects:
- Anything involving unstructured data (PDFs, scanned documents)
- Processes with lots of judgment calls
- Systems that don't have APIs or export capabilities

### Step 2: Learn the Basics (1-2 Weeks)

You don't need a computer science degree. You need:

1. **How to read a CSV or Excel file** (`pandas.read_csv()`, `pandas.read_excel()`)
2. **How to filter rows** (`df[df['column'] > 100]`)
3. **How to create new columns** (`df['new_col'] = df['col1'] + df['col2']`)
4. **How to merge datasets** (`pd.merge()`)
5. **How to export results** (`df.to_csv()`, `df.to_excel()`)

Resources:
- **Python for Data Analysis** by Wes McKinney (the pandas creator)
- **Automate the Boring Stuff with Python** by Al Sweigart (free online)
- **Kaggle Learn** (free interactive Python tutorials)

### Step 3: Build a Minimum Viable Script

Don't try to build the perfect solution on day one. Build the **smallest thing that works**:

1. Read one file
2. Do one transformation
3. Export the result

Once that works, add the next piece. Test after each change.

### Step 4: Handle Errors Gracefully

Real-world data is messy. Your script needs to handle:

- **Missing files** — what if the input file doesn't exist?
- **Missing columns** — what if someone renamed a column in the export?
- **Unexpected values** — what if there's a null where you expected a number?

Add error handling:

```python
try:
    df = pd.read_csv('data.csv')
except FileNotFoundError:
    print("Error: data.csv not found")
    exit()

if 'required_column' not in df.columns:
    print("Error: required_column missing from data")
    exit()
```

## Common Mistakes and How to Avoid Them

### Mistake 1: Not Saving Intermediate Results

When debugging, save intermediate steps so you can inspect what's happening:

```python
# Save checkpoint after merge
merged.to_csv('checkpoint_after_merge.csv', index=False)
```

### Mistake 2: Hardcoding File Paths

Don't do this:

```python
df = pd.read_csv('/Users/brian/Desktop/data.csv')
```

Use relative paths or command-line arguments:

```python
import sys
file_path = sys.argv[1]  # Pass filename as argument
df = pd.read_csv(file_path)
```

### Mistake 3: Not Documenting What the Script Does

Six months from now, you won't remember what this script does. Add comments:

```python
# Read billing data from Stripe export
# Expected columns: invoice_id, amount, customer_name, date
billing_data = pd.read_csv('billing.csv')
```

### Mistake 4: Ignoring Data Quality Issues

Your script will only be as good as your data. If your input data is messy, your output will be messy.

Always add validation steps:

```python
# Check for expected columns
expected_cols = ['invoice_id', 'amount', 'date']
missing_cols = [col for col in expected_cols if col not in df.columns]
if missing_cols:
    print(f"Error: Missing columns: {missing_cols}")
    exit()
```

## The 10x Automation Opportunities

Once you've automated a few tasks, you'll start seeing opportunities everywhere. Here are the highest-value targets:

### Month-End Close Automation
- Journal entry generation from transaction logs
- Account reconciliation reports
- Variance analysis (budget vs. actual)

### Revenue Recognition
- Calculating rev rec schedules from billing data
- Deferred revenue rollforward
- Contract modification impact analysis

### Financial Reporting
- Management reports from multiple data sources
- Board deck metrics automation
- Investor reporting packages

### Compliance and Audit
- SOX control testing data extraction
- Audit request file generation
- Transaction sampling for review

## The Bottom Line

Python isn't just for software engineers. It's a tool that lets finance professionals **stop doing repetitive work and start doing strategic work**.

Start small. Pick one task that takes you 2 hours a week. Write a script that does it in 30 seconds. Once you see the time savings, you'll find 10 more tasks to automate.

The best part: Python skills are transferable. Once you learn the fundamentals, you can apply them to any domain — revenue operations, FP&A, accounting, compliance, billing.

Your finance team shouldn't be spending 30% of their time copying and pasting data. Automate the work nobody wants to do, and free up time for work that actually matters.
