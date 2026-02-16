---
title: "Writing Python Scripts That Finance People Can Actually Use"
slug: "writing-python-scripts-that-finance-people-can-actually-use"
excerpt: "The best automation script in the world is worthless if nobody on your team can run it. Here's how to bridge the gap."
tags: ["Python", "Automation", "Finance", "Best Practices"]
published: true
featured: false
created_at: "2025-11-03"
published_at: "2025-11-03"
author: "Brian Hardin"
meta_description: "How to write Python scripts that non-technical finance team members can actually run, with practical patterns for CLI design, configuration, and error handling."
---

I wrote a beautiful Python script that automated three hours of daily work for our accounting team. Elegant code. Comprehensive error handling. Well-tested.

Nobody used it.

The problem wasn't the code. It was the interface. Running it required:
1. Opening Terminal (terrifying for Excel users)
2. Activating a virtual environment (what's a virtual environment?)
3. Running `python reconcile_payments.py --start-date 2024-01-01 --end-date 2024-01-31 --output ./reports/` (what's a flag?)
4. Checking logs to confirm it worked (where are logs?)

I rewrote the interface. Same logic, different wrapper. Now they double-click an icon, pick dates from dropdowns, and click "Run." They use it every day.

The automation didn't change. The user experience did.

## Principle 1: Configuration Over Code

Finance users should never edit code to change behavior. Never.

**Bad:**
```python
# reconcile_payments.py

# Configuration
START_DATE = "2024-01-01"  # Change this!
END_DATE = "2024-01-31"    # Change this!
OUTPUT_DIR = "./reports"   # Change this!
```

**Good:**
```python
# reconcile_payments.py
import json
from pathlib import Path


def load_config():
    """Load configuration from JSON file."""
    config_path = Path.home() / ".payment_reconciliation" / "config.json"

    if not config_path.exists():
        # Create default config on first run
        config_path.parent.mkdir(parents=True, exist_ok=True)
        default_config = {
            "output_directory": str(Path.home() / "Documents" / "Payment Reports"),
            "netsuite_account_id": "",
            "email_recipients": ["accounting@company.com"],
            "auto_send_email": false
        }
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)

        print(f"Created default config at {config_path}")
        print("Please edit this file with your settings.")
        return None

    with open(config_path) as f:
        return json.load(f)


config = load_config()
if config is None:
    exit(1)
```

Users edit a simple JSON file, not Python code. They can't break the script with a syntax error. You can add helpful comments in the JSON:

```json
{
  "_comment": "Payment Reconciliation Configuration",
  "_comment_output": "Where to save reports (must be an existing folder)",
  "output_directory": "C:/Users/jsmith/Documents/Payment Reports",

  "_comment_netsuite": "Your NetSuite account ID (ask IT if you don't know)",
  "netsuite_account_id": "1234567",

  "_comment_email": "Who should receive the report when it completes",
  "email_recipients": [
    "accounting@company.com",
    "controller@company.com"
  ],

  "auto_send_email": true
}
```

JSON doesn't support comments officially, but keys starting with `_comment` work fine and make configs self-documenting.

## Principle 2: CLI Design for Humans

If your script has a command-line interface, make it intuitive.

**Bad:**
```python
import sys

start = sys.argv[1]
end = sys.argv[2]
output = sys.argv[3]
```

**Good:**
```python
import argparse
from datetime import datetime, timedelta


def parse_args():
    parser = argparse.ArgumentParser(
        description="Reconcile payments between Stripe and NetSuite",
        epilog="Example: python reconcile_payments.py --month 2024-01"
    )

    parser.add_argument(
        '--month',
        type=str,
        help='Month to reconcile (YYYY-MM format). Defaults to last month.',
        default=(datetime.now().replace(day=1) - timedelta(days=1)).strftime('%Y-%m')
    )

    parser.add_argument(
        '--output',
        type=str,
        help='Output directory. Defaults to config file setting.',
        default=None
    )

    parser.add_argument(
        '--send-email',
        action='store_true',
        help='Send email report when complete.'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run without making any changes (test mode).'
    )

    return parser.parse_args()


args = parse_args()
```

**Key improvements:**

- Help text for every argument (`--help` shows usage)
- Sensible defaults (last month if not specified)
- Clear format expectations (YYYY-MM)
- Flags don't require values (`--send-email`, not `--send-email true`)
- Dry run mode for testing

**Running it:**
```bash
# Use defaults (last month)
python reconcile_payments.py

# Specific month
python reconcile_payments.py --month 2024-01

# Test without making changes
python reconcile_payments.py --month 2024-01 --dry-run

# See all options
python reconcile_payments.py --help
```

Much better than memorizing positional arguments.

## Principle 3: Error Messages a Human Can Understand

**Bad error message:**
```
Traceback (most recent call last):
  File "reconcile.py", line 47, in <module>
    ns_data = ns.get_invoices(start_date, end_date)
  File "netsuite_client.py", line 123, in get_invoices
    response = requests.post(url, headers=headers)
  File "requests/models.py", line 234, in post
    raise ConnectionError("Max retries exceeded")
ConnectionError: Max retries exceeded with url: https://...
```

That's what the user sees. They don't know what to do with it.

**Good error message:**
```
❌ ERROR: Cannot connect to NetSuite

The script couldn't reach NetSuite's servers. This usually means:

1. Your internet connection is down
2. NetSuite is having issues (check status.netsuite.com)
3. Your NetSuite credentials expired

What to do:
- Check your internet connection
- Try again in a few minutes
- If it keeps failing, contact IT with this error code: NS_CONNECTION_001

Technical details (for IT):
ConnectionError: Max retries exceeded with url: https://1234567.suitetalk.api.netsuite.com/...
```

**Implementation:**

```python
import logging
from typing import Optional


class UserFriendlyException(Exception):
    """Exception with user-friendly message and technical details."""

    def __init__(self, user_message: str, technical_details: str, error_code: str):
        self.user_message = user_message
        self.technical_details = technical_details
        self.error_code = error_code
        super().__init__(user_message)

    def display(self):
        """Display formatted error message."""
        print("\n" + "="*60)
        print("❌ ERROR: " + self.user_message)
        print("="*60)
        print(f"\nError code: {self.error_code}")
        print(f"\nTechnical details (for IT):")
        print(f"{self.technical_details}")
        print("="*60 + "\n")


def get_netsuite_data(start_date, end_date):
    """Get data from NetSuite with friendly error handling."""

    try:
        ns = NetSuiteClient.from_config()
        return ns.get_invoices(start_date, end_date)

    except ConnectionError as e:
        raise UserFriendlyException(
            user_message=(
                "Cannot connect to NetSuite\n\n"
                "The script couldn't reach NetSuite's servers. This usually means:\n"
                "1. Your internet connection is down\n"
                "2. NetSuite is having issues (check status.netsuite.com)\n"
                "3. Your VPN isn't connected\n\n"
                "What to do:\n"
                "- Check your internet connection\n"
                "- Connect to VPN if required\n"
                "- Try again in a few minutes\n"
                "- If it keeps failing, contact IT"
            ),
            technical_details=str(e),
            error_code="NS_CONNECTION_001"
        )

    except AuthenticationError as e:
        raise UserFriendlyException(
            user_message=(
                "NetSuite login failed\n\n"
                "Your NetSuite credentials aren't working. This usually means:\n"
                "1. Your password changed recently\n"
                "2. Your API token expired\n"
                "3. Your account was locked\n\n"
                "What to do:\n"
                "- Contact IT to reset your NetSuite API credentials\n"
                "- Provide them with this error code"
            ),
            technical_details=str(e),
            error_code="NS_AUTH_002"
        )

    except Exception as e:
        # Unexpected errors still show details
        raise UserFriendlyException(
            user_message="An unexpected error occurred",
            technical_details=f"{type(e).__name__}: {str(e)}",
            error_code="UNKNOWN_999"
        )


# In main script
if __name__ == "__main__":
    try:
        data = get_netsuite_data(start_date, end_date)
        # ... process data ...
        print("✅ Reconciliation complete!")

    except UserFriendlyException as e:
        e.display()
        exit(1)
```

Users get actionable guidance. IT gets technical details when they forward the error.

## Principle 4: Progress Indication and Feedback

Finance scripts often process thousands of records. Give feedback.

**Bad:**
```python
# Script runs silently for 5 minutes
# User assumes it's broken and kills it
for customer in customers:
    process_customer(customer)
```

**Good:**
```python
from tqdm import tqdm
import time


print("Processing 1,247 customers...")
print("This usually takes 3-5 minutes.\n")

for customer in tqdm(customers, desc="Reconciling payments", unit="customer"):
    process_customer(customer)
    time.sleep(0.1)  # Rate limiting

print("\n✅ Processing complete!")
```

Users see:
```
Processing 1,247 customers...
This usually takes 3-5 minutes.

Reconciling payments: 42%|████████▌          | 523/1247 [01:34<02:09,  5.58customer/s]
```

They know it's working. They know how long it will take. They don't panic.

**For multi-step processes:**

```python
def run_reconciliation():
    """Run full reconciliation with step-by-step feedback."""

    steps = [
        ("Connecting to NetSuite", connect_netsuite),
        ("Connecting to Stripe", connect_stripe),
        ("Downloading NetSuite invoices", download_invoices),
        ("Downloading Stripe charges", download_charges),
        ("Matching payments", match_payments),
        ("Generating report", generate_report),
        ("Sending email", send_email)
    ]

    total_steps = len(steps)

    for i, (step_name, step_func) in enumerate(steps, 1):
        print(f"\n[{i}/{total_steps}] {step_name}...", end=" ", flush=True)

        try:
            result = step_func()
            print("✅")

        except Exception as e:
            print("❌")
            raise UserFriendlyException(
                user_message=f"Failed at step: {step_name}",
                technical_details=str(e),
                error_code=f"STEP_{i:02d}"
            )

    print("\n🎉 All steps completed successfully!")
```

Output:
```
[1/7] Connecting to NetSuite... ✅
[2/7] Connecting to Stripe... ✅
[3/7] Downloading NetSuite invoices... ✅
[4/7] Downloading Stripe charges... ✅
[5/7] Matching payments... ✅
[6/7] Generating report... ✅
[7/7] Sending email... ✅

🎉 All steps completed successfully!
```

Clear. Informative. Reassuring.

## Principle 5: Logging for Debugging (Not for Users)

Users shouldn't read logs. But you need logs for debugging.

**Separate user output from debug logs:**

```python
import logging
from pathlib import Path
from datetime import datetime


def setup_logging(verbose=False):
    """
    Set up dual logging:
    - File: Detailed debug logs
    - Console: Only important messages (unless verbose=True)
    """

    log_dir = Path.home() / ".payment_reconciliation" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"reconciliation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    # Root logger - captures everything
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # File handler - detailed logs
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler - only important stuff (unless verbose)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if verbose else logging.WARNING)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return log_file


# In script
log_file = setup_logging(verbose=args.verbose)
logger = logging.getLogger(__name__)

logger.debug("Starting reconciliation with parameters: %s", args)  # File only
logger.info("Processing customer %s", customer_id)  # File only
logger.warning("Customer %s has no payment method", customer_id)  # Console + file
logger.error("Failed to process customer %s: %s", customer_id, error)  # Console + file

print(f"\n📋 Detailed logs saved to: {log_file}")
print("Share this file with IT if you need help debugging.\n")
```

Users see clean output. Debug logs go to a file. When something breaks, they can share the log file with IT.

## Principle 6: Graceful Degradation

Scripts should handle partial failures gracefully.

**Bad:**
```python
# Script crashes on first error
for customer in customers:
    process_customer(customer)  # If one fails, all fails
```

**Good:**
```python
results = {
    'success': [],
    'failed': [],
    'skipped': []
}

for customer in tqdm(customers, desc="Processing"):
    try:
        process_customer(customer)
        results['success'].append(customer.id)

    except PaymentMethodMissing:
        results['skipped'].append({
            'id': customer.id,
            'reason': 'No payment method on file'
        })
        logger.warning(f"Skipped {customer.id}: no payment method")

    except Exception as e:
        results['failed'].append({
            'id': customer.id,
            'reason': str(e)
        })
        logger.error(f"Failed to process {customer.id}: {e}")

# Summary report
print("\n" + "="*60)
print("RECONCILIATION SUMMARY")
print("="*60)
print(f"✅ Successful: {len(results['success'])} customers")
print(f"⚠️  Skipped:    {len(results['skipped'])} customers (no payment method)")
print(f"❌ Failed:     {len(results['failed'])} customers")

if results['failed']:
    print("\nFailed customers:")
    for failure in results['failed'][:10]:  # Show first 10
        print(f"  - {failure['id']}: {failure['reason']}")
    if len(results['failed']) > 10:
        print(f"  ... and {len(results['failed']) - 10} more (see log file)")

print("="*60 + "\n")

# Export failures to CSV for review
if results['failed']:
    failures_file = Path(config['output_directory']) / f"failures_{datetime.now().strftime('%Y%m%d')}.csv"
    pd.DataFrame(results['failed']).to_csv(failures_file, index=False)
    print(f"Failed customer details saved to: {failures_file}\n")
```

Users get a complete picture. Partial success is still useful. Failed items are logged for follow-up.

## Principle 7: Packaging for Distribution

Making your script easy to run:

**Option 1: Virtual environment + batch file (Windows)**

```batch
REM run_reconciliation.bat
@echo off
echo Starting Payment Reconciliation...
echo.

REM Activate virtual environment
call "%~dp0venv\Scripts\activate.bat"

REM Run script
python "%~dp0reconcile_payments.py" %*

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Script failed. Press any key to close...
    pause > nul
)
```

Users double-click `run_reconciliation.bat`. It handles the virtual environment and runs the script.

**Option 2: Standalone executable (PyInstaller)**

```bash
# Build standalone executable
pip install pyinstaller

pyinstaller --onefile \
            --name "Payment Reconciliation" \
            --add-data "config.json:." \
            --icon=icon.ico \
            reconcile_payments.py
```

Produces a single `.exe` file. No Python installation required. Users double-click it.

**Option 3: Simple GUI wrapper (tkinter)**

```python
# gui_wrapper.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import threading
from reconcile_payments import run_reconciliation


class ReconciliationGUI:
    def __init__(self, root):
        self.root = root
        root.title("Payment Reconciliation")
        root.geometry("500x400")

        # Month selection
        ttk.Label(root, text="Select Month:").grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.month_var = tk.StringVar(value=self.get_last_month())
        month_entry = ttk.Entry(root, textvariable=self.month_var, width=20)
        month_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        ttk.Label(root, text="(YYYY-MM format)").grid(row=0, column=2, padx=10, pady=10, sticky="w")

        # Output directory
        ttk.Label(root, text="Save Report To:").grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.output_var = tk.StringVar(value=str(Path.home() / "Documents"))
        output_entry = ttk.Entry(root, textvariable=self.output_var, width=40)
        output_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        browse_btn = ttk.Button(root, text="Browse...", command=self.browse_output)
        browse_btn.grid(row=1, column=2, padx=10, pady=10)

        # Options
        self.email_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(root, text="Send email when complete", variable=self.email_var).grid(
            row=2, column=1, padx=10, pady=5, sticky="w"
        )

        self.dry_run_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(root, text="Test mode (don't make changes)", variable=self.dry_run_var).grid(
            row=3, column=1, padx=10, pady=5, sticky="w"
        )

        # Run button
        self.run_btn = ttk.Button(root, text="Run Reconciliation", command=self.run_script)
        self.run_btn.grid(row=4, column=1, padx=10, pady=20)

        # Progress display
        self.progress_text = tk.Text(root, height=10, width=60, state='disabled')
        self.progress_text.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=6, column=0, columnspan=3, sticky="ew")

    def get_last_month(self):
        last_month = datetime.now().replace(day=1) - timedelta(days=1)
        return last_month.strftime("%Y-%m")

    def browse_output(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_var.set(directory)

    def log_message(self, message):
        """Add message to progress text widget."""
        self.progress_text.config(state='normal')
        self.progress_text.insert(tk.END, message + "\n")
        self.progress_text.see(tk.END)
        self.progress_text.config(state='disabled')

    def run_script(self):
        """Run reconciliation in background thread."""

        self.run_btn.config(state='disabled')
        self.status_var.set("Running...")
        self.progress_text.config(state='normal')
        self.progress_text.delete(1.0, tk.END)
        self.progress_text.config(state='disabled')

        # Run in background thread so GUI doesn't freeze
        thread = threading.Thread(target=self._run_reconciliation_thread)
        thread.daemon = True
        thread.start()

    def _run_reconciliation_thread(self):
        """Background thread for running reconciliation."""
        try:
            self.log_message(f"Starting reconciliation for {self.month_var.get()}...")

            # Call actual reconciliation function
            result = run_reconciliation(
                month=self.month_var.get(),
                output_dir=self.output_var.get(),
                send_email=self.email_var.get(),
                dry_run=self.dry_run_var.get(),
                log_callback=self.log_message  # Pass callback for progress updates
            )

            self.log_message("\n✅ Reconciliation complete!")
            self.log_message(f"Report saved to: {result['report_path']}")

            self.status_var.set("Complete")
            messagebox.showinfo("Success", "Reconciliation completed successfully!")

        except Exception as e:
            self.log_message(f"\n❌ Error: {str(e)}")
            self.status_var.set("Failed")
            messagebox.showerror("Error", f"Reconciliation failed:\n\n{str(e)}")

        finally:
            self.run_btn.config(state='normal')


if __name__ == "__main__":
    root = tk.Tk()
    app = ReconciliationGUI(root)
    root.mainloop()
```

Users get a simple GUI. No command line. No configuration files to edit. Just click and run.

## Principle 8: Documentation That Doesn't Require a Degree

**Bad README:**
```markdown
# Payment Reconciliation

## Installation
```bash
git clone https://github.com/company/reconciliation
cd reconciliation
pip install -r requirements.txt
```

## Usage
```bash
python reconcile_payments.py --month YYYY-MM --output DIR
```
```

**Good README:**
```markdown
# Payment Reconciliation Tool

Automatically matches Stripe payments to NetSuite invoices and generates a reconciliation report.

## For Accounting Team (Non-Technical Users)

### How to Run the Tool

1. **Double-click** `Run Reconciliation.bat` on your desktop
2. **Select the month** you want to reconcile (e.g., 2024-01)
3. **Choose where to save** the report
4. **Click "Run Reconciliation"**
5. Wait 3-5 minutes for it to complete
6. Find your report in the folder you selected

### Troubleshooting

**"Cannot connect to NetSuite"**
- Check your internet connection
- Make sure you're connected to VPN
- Contact IT if it still doesn't work

**"NetSuite login failed"**
- Your API credentials may have expired
- Contact IT to renew your access

**"No data found for this month"**
- Make sure the month format is YYYY-MM (e.g., 2024-01)
- Check that you have data in NetSuite for that month

### Getting Help

- For technical issues: Email it@company.com
- For report questions: Email accounting-manager@company.com
- Include the log file from `C:\Users\[YourName]\.payment_reconciliation\logs\`

---

## For IT / Developers

### Installation
[Technical setup instructions here]

### Configuration
[Technical configuration details here]

### Architecture
[Technical architecture documentation here]
```

Separate user docs from technical docs. Most users never need the technical section.

## The Real Test

A script is usable when a non-technical person can:

1. **Run it successfully** without asking for help
2. **Understand what it's doing** from the progress messages
3. **Recover from common errors** using the error messages
4. **Get the output they need** in a format they can use

If they're calling you every time they run it, the script isn't done yet.

## Results

After applying these principles to our payment reconciliation tool:

- **Adoption rate:** 0% → 100% of accounting team
- **Support requests:** 3-4 per week → 1 per month
- **Time saved:** 3 hours per day across the team
- **Errors:** Frequent manual mistakes → zero in 12 months

The accounting team now asks me to automate other processes. They trust that the tools will work and won't require a CS degree to operate.

Write Python for humans, not just for Python.
