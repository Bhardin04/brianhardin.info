---
title: "Connecting NetSuite to Everything: REST APIs and SuiteScript Patterns"
slug: "connecting-netsuite-to-everything-rest-apis-and-suitescript-patterns"
excerpt: "NetSuite is powerful. NetSuite's API documentation is... less powerful. Here's what actually works."
tags: ["NetSuite", "Integration", "API", "SuiteScript"]
published: true
featured: true
created_at: "2025-10-20"
published_at: "2025-10-20"
author: "Brian Hardin"
meta_description: "Practical patterns for integrating NetSuite with external systems using REST APIs, RESTlets, and SuiteScript 2.0."
---

I've integrated NetSuite with everything from Salesforce to homegrown Python scripts to Stripe to data warehouses. The documentation always promises it will be straightforward. It never is.

Here's what actually works.

## The NetSuite Integration Landscape

NetSuite gives you several ways to get data in and out:

1. **SuiteScript RESTlets** — Custom REST endpoints you write in JavaScript and deploy to NetSuite
2. **REST Web Services** — NetSuite's native REST API for standard records
3. **SOAP Web Services** — The old way (avoid if you can)
4. **SuiteTalk** — The overall umbrella term Oracle uses for their web services
5. **CSV Import** — Manual, but sometimes the fastest path

For programmatic integration, you'll use RESTlets and REST Web Services. Here's when to use each:

**Use REST Web Services when:**
- You're working with standard NetSuite records (customers, invoices, sales orders)
- You need simple CRUD operations
- You want NetSuite to handle the business logic

**Use RESTlets when:**
- You need custom business logic
- You're aggregating data from multiple record types
- Standard REST Web Services don't expose the fields you need
- You need complex filtering or calculations

In practice, I use both in the same integration.

## Token-Based Authentication (TBA): The Only Way

NetSuite's documentation mentions several auth methods. Use Token-Based Authentication. Everything else is deprecated or insecure.

**Setup steps in NetSuite:**

1. Enable TBA: Setup → Company → Enable Features → SuiteCloud → Manage Authentication (check "Token-Based Authentication")
2. Create an integration record: Setup → Integration → Manage Integrations → New
3. Save the Consumer Key and Consumer Secret (you'll never see the secret again)
4. Create an access token: Setup → Users/Roles → Access Tokens → New
5. Save the Token ID and Token Secret (again, last chance)

You now have four credentials:
- Account ID (your NetSuite account number)
- Consumer Key
- Consumer Secret
- Token ID
- Token Secret

Guard these like production database credentials. They are equivalent.

## Python Client for NetSuite REST API

Here's a working Python client for NetSuite's REST Web Services:

```python
# netsuite_client.py
import requests
import time
import hmac
import hashlib
import secrets
import base64
from urllib.parse import quote


class NetSuiteClient:
    """
    Client for NetSuite REST Web Services using Token-Based Authentication.
    """

    def __init__(self, account_id: str, consumer_key: str, consumer_secret: str,
                 token_id: str, token_secret: str):
        self.account_id = account_id.replace("_", "-").upper()
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.token_id = token_id
        self.token_secret = token_secret
        self.base_url = f"https://{account_id.replace('_', '-')}.suitetalk.api.netsuite.com"

    def _generate_oauth_header(self, method: str, url: str) -> str:
        """
        Generate OAuth 1.0 signature for NetSuite TBA.
        This is the part that takes hours to debug if you get it wrong.
        """
        timestamp = str(int(time.time()))
        nonce = secrets.token_hex(16)

        # OAuth parameters
        oauth_params = {
            "oauth_consumer_key": self.consumer_key,
            "oauth_token": self.token_id,
            "oauth_signature_method": "HMAC-SHA256",
            "oauth_timestamp": timestamp,
            "oauth_nonce": nonce,
            "oauth_version": "1.0"
        }

        # Create signature base string
        sorted_params = sorted(oauth_params.items())
        param_string = "&".join([f"{quote(k, safe='')}={quote(v, safe='')}"
                                for k, v in sorted_params])

        base_string = f"{method.upper()}&{quote(url, safe='')}&{quote(param_string, safe='')}"

        # Create signing key
        signing_key = f"{quote(self.consumer_secret, safe='')}&{quote(self.token_secret, safe='')}"

        # Generate signature
        signature = base64.b64encode(
            hmac.new(
                signing_key.encode('utf-8'),
                base_string.encode('utf-8'),
                hashlib.sha256
            ).digest()
        ).decode('utf-8')

        oauth_params["oauth_signature"] = signature

        # Build authorization header
        auth_header = "OAuth " + ", ".join([f'{k}="{quote(v, safe="")}"'
                                           for k, v in sorted(oauth_params.items())])

        return auth_header

    def get(self, endpoint: str, params: dict = None) -> dict:
        """GET request to NetSuite REST API."""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": self._generate_oauth_header("GET", url),
            "Content-Type": "application/json",
            "prefer": "transient"  # Prevents NetSuite from caching
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: dict) -> dict:
        """POST request to NetSuite REST API."""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": self._generate_oauth_header("POST", url),
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def get_customer(self, customer_id: str) -> dict:
        """Get customer record by internal ID."""
        return self.get(f"/services/rest/record/v1/customer/{customer_id}")

    def search_invoices(self, customer_id: str = None, status: str = None) -> list:
        """
        Search invoices with filters.
        NetSuite's query syntax is... unique.
        """
        query = []

        if customer_id:
            query.append(f"entity={customer_id}")
        if status:
            query.append(f"status={status}")

        q_string = " AND ".join(query) if query else ""

        endpoint = f"/services/rest/query/v1/suiteql"
        suiteql = f"SELECT id, tranid, entity, amount, status FROM transaction WHERE type='CustInvc'"

        if q_string:
            suiteql += f" AND {q_string}"

        response = self.post(endpoint, {"q": suiteql})
        return response.get("items", [])
```

**The OAuth signature generation is critical.** Get one character wrong in the base string construction and you'll get cryptic "Invalid Login" errors. This code works as of February 2026.

## RESTlet Pattern: Custom Endpoints

When REST Web Services aren't enough, write a RESTlet. RESTlets are custom JavaScript endpoints deployed to NetSuite.

**Use case:** I needed to get all open invoices for a customer with custom fields that REST Web Services doesn't expose, plus calculated aging buckets.

Here's the SuiteScript 2.0 RESTlet:

```javascript
/**
 * @NApiVersion 2.1
 * @NScriptType Restlet
 */
define(['N/search', 'N/record'], (search, record) => {

    /**
     * GET handler - returns open invoices with custom aging logic
     * @param {Object} context - Request parameters
     * @returns {Object} Response data
     */
    function get(context) {
        const customerId = context.customer_id;

        if (!customerId) {
            return {
                success: false,
                error: 'customer_id parameter required'
            };
        }

        try {
            const invoices = [];

            // Create saved search for open invoices
            const invoiceSearch = search.create({
                type: search.Type.INVOICE,
                filters: [
                    ['entity', 'is', customerId],
                    'AND',
                    ['status', 'anyof', 'CustInvc:A'], // Open status
                    'AND',
                    ['mainline', 'is', 'T'] // Header lines only
                ],
                columns: [
                    'tranid',
                    'trandate',
                    'duedate',
                    'amount',
                    'amountremaining',
                    'status',
                    'custbody_payment_terms_custom', // Custom field example
                    'memo'
                ]
            });

            invoiceSearch.run().each((result) => {
                const dueDate = new Date(result.getValue('duedate'));
                const today = new Date();
                const daysOverdue = Math.floor((today - dueDate) / (1000 * 60 * 60 * 24));

                // Custom aging bucket logic
                let agingBucket;
                if (daysOverdue < 0) {
                    agingBucket = 'current';
                } else if (daysOverdue <= 30) {
                    agingBucket = '1-30';
                } else if (daysOverdue <= 60) {
                    agingBucket = '31-60';
                } else if (daysOverdue <= 90) {
                    agingBucket = '61-90';
                } else {
                    agingBucket = '90+';
                }

                invoices.push({
                    id: result.id,
                    invoice_number: result.getValue('tranid'),
                    invoice_date: result.getValue('trandate'),
                    due_date: result.getValue('duedate'),
                    total_amount: parseFloat(result.getValue('amount')),
                    amount_remaining: parseFloat(result.getValue('amountremaining')),
                    status: result.getText('status'),
                    payment_terms: result.getValue('custbody_payment_terms_custom'),
                    days_overdue: daysOverdue,
                    aging_bucket: agingBucket,
                    memo: result.getValue('memo')
                });

                return true; // Continue iteration
            });

            return {
                success: true,
                customer_id: customerId,
                invoice_count: invoices.length,
                invoices: invoices
            };

        } catch (e) {
            return {
                success: false,
                error: e.message,
                stack: e.stack
            };
        }
    }

    /**
     * POST handler - create or update records
     * @param {Object} context - Request body
     * @returns {Object} Response data
     */
    function post(context) {
        // Example: Create a customer note
        try {
            const noteRecord = record.create({
                type: record.Type.NOTE
            });

            noteRecord.setValue('title', context.title);
            noteRecord.setValue('note', context.note);
            noteRecord.setValue('entity', context.customer_id);

            const noteId = noteRecord.save();

            return {
                success: true,
                note_id: noteId
            };

        } catch (e) {
            return {
                success: false,
                error: e.message
            };
        }
    }

    return {
        get: get,
        post: post
    };
});
```

**Deploy the RESTlet:**

1. Upload the JavaScript file to the File Cabinet (Documents → Files → SuiteScripts)
2. Create a Script record (Customization → Scripting → Scripts → New)
3. Select the file and set it as a RESTlet
4. Create a deployment (set audience, execution context)
5. Note the external URL

**Call it from Python:**

```python
def call_restlet(self, script_id: str, deploy_id: str, params: dict = None) -> dict:
    """
    Call a NetSuite RESTlet.
    Script and deployment IDs are from the NetSuite deployment record.
    """
    url = f"{self.base_url}/app/site/hosting/restlet.nl"
    url += f"?script={script_id}&deploy={deploy_id}"

    if params:
        for key, value in params.items():
            url += f"&{key}={value}"

    headers = {
        "Authorization": self._generate_oauth_header("GET", url),
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


# Usage
client = NetSuiteClient(account_id, consumer_key, consumer_secret, token_id, token_secret)
result = client.call_restlet(
    script_id="123",  # From deployment record
    deploy_id="1",
    params={"customer_id": "456"}
)

invoices = result['invoices']
```

## Rate Limits and Concurrency

NetSuite enforces governance limits. You'll hit them.

**Key limits:**
- 10 concurrent requests per integration
- Search results limited to 1000 rows per page
- SuiteScript execution time limited to 10,000 units (roughly 60 seconds)
- RESTlet concurrency: 10 concurrent requests

**Handle rate limits with exponential backoff:**

```python
import time
from requests.exceptions import HTTPError


def retry_with_backoff(func, max_retries=5):
    """Retry function with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return func()
        except HTTPError as e:
            if e.response.status_code == 429:  # Rate limited
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"Rate limited. Waiting {wait_time:.2f}s before retry {attempt + 1}/{max_retries}")
                time.sleep(wait_time)
            else:
                raise
    raise Exception(f"Failed after {max_retries} retries")


# Usage
result = retry_with_backoff(lambda: client.get_customer("12345"))
```

**For large data pulls, use pagination:**

```python
def get_all_customers(client: NetSuiteClient) -> list:
    """Get all customers with pagination."""
    customers = []
    offset = 0
    limit = 1000

    while True:
        suiteql = f"SELECT id, companyname, email FROM customer OFFSET {offset} LIMIT {limit}"
        response = client.post("/services/rest/query/v1/suiteql", {"q": suiteql})

        items = response.get("items", [])
        customers.extend(items)

        if len(items) < limit:
            break  # No more results

        offset += limit
        time.sleep(0.5)  # Be nice to NetSuite

    return customers
```

## Common Integration Architectures

**Pattern 1: Event-Driven Sync (NetSuite → External)**

Use a scheduled SuiteScript to detect changes and call your webhook:

```javascript
// Scheduled script that runs every 15 minutes
function execute(context) {
    // Find invoices modified in last 15 minutes
    const invoiceSearch = search.create({
        type: search.Type.INVOICE,
        filters: [
            ['lastmodifieddate', 'within', 'today'],
            'AND',
            ['lastmodifieddate', 'after', '15 minutes ago']
        ]
    });

    const changedInvoices = [];
    invoiceSearch.run().each((result) => {
        changedInvoices.push({
            id: result.id,
            invoice_number: result.getValue('tranid')
        });
        return true;
    });

    if (changedInvoices.length > 0) {
        // Call external webhook
        const response = https.post({
            url: 'https://your-api.com/webhooks/netsuite/invoice-updated',
            body: JSON.stringify(changedInvoices),
            headers: {'Content-Type': 'application/json'}
        });
    }
}
```

**Pattern 2: Batch Sync (Scheduled Python Job)**

Run a Python script on a schedule (cron, Airflow, etc.) to pull data from NetSuite and push to your data warehouse:

```python
# Runs nightly at 2 AM
def sync_invoices_to_warehouse():
    ns = NetSuiteClient(...)

    # Get yesterday's invoices
    suiteql = """
        SELECT id, tranid, entity, amount, trandate, status
        FROM transaction
        WHERE type = 'CustInvc'
        AND trandate = YESTERDAY
    """

    invoices = ns.post("/services/rest/query/v1/suiteql", {"q": suiteql})

    # Load into warehouse
    load_to_snowflake(invoices['items'])
```

**Pattern 3: Real-Time Lookup (RESTlet as Data Layer)**

Your application calls a RESTlet whenever it needs fresh NetSuite data:

```python
# In your FastAPI endpoint
@app.get("/customer/{customer_id}/invoices")
def get_customer_invoices(customer_id: str):
    ns = NetSuiteClient(...)
    result = ns.call_restlet(
        script_id="customscript_invoice_lookup",
        deploy_id="1",
        params={"customer_id": customer_id}
    )
    return result['invoices']
```

## What The Docs Don't Tell You

**1. Field internal IDs vs names:** NetSuite has internal IDs for everything. `custbody_custom_field` is not the same as "Custom Field" in the UI. Use SuiteAnswers or the Records Browser to find internal IDs.

**2. SuiteQL is not SQL:** It looks like SQL. It's not. No JOINs on custom records. Limited function support. Inconsistent WHERE clause behavior. Test everything.

**3. Sandbox behaves differently:** Your perfectly working production integration may fail in sandbox because sandbox has different data, different custom fields, or different governance limits.

**4. Error messages lie:** "Invalid login" usually means your OAuth signature is wrong. "Unexpected error" means you hit a governance limit. "Permission denied" might mean the record doesn't exist.

**5. Custom forms break APIs:** If a record uses a custom form that hides required fields, API operations may fail with cryptic errors. Always test with the standard form first.

## Final Advice

NetSuite integration is like plumbing. When it works, nobody notices. When it breaks, everyone notices.

Write defensive code. Log everything. Handle rate limits gracefully. Test in sandbox first (but don't trust it completely). Keep your auth tokens secure.

And when NetSuite's documentation fails you—which it will—remember: you're not the first person to hit this problem. SuiteAnswers, Stack Overflow, and the NetSuite Professionals group on LinkedIn are your friends.

The API is frustrating, but it's also incredibly powerful once you figure out the patterns. These patterns will save you hours of debugging.

You're welcome.
