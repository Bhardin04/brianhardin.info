---
title: "Building Internal Tools with FastAPI: A Practical Guide"
slug: "building-internal-tools-with-fastapi-a-practical-guide"
excerpt: "Your team doesn't need another SaaS subscription. They need a 200-line FastAPI app that does exactly what they need."
tags: ["Python", "FastAPI", "Internal Tools", "Tutorial"]
published: true
featured: false
created_at: "2025-10-13"
published_at: "2025-10-13"
author: "Brian Hardin"
meta_description: "How to build internal business tools with FastAPI, including project structure, authentication patterns, and deployment for non-engineering teams."
---

Last quarter, our collections team was spending 45 minutes every morning manually pulling payment status across three different systems to prioritize their outreach. They asked IT for a dashboard. IT quoted 12 weeks and $80k.

I built them a FastAPI tool in an afternoon. It's still running.

## When to Build vs Buy

Before you write a single line of code, answer these questions honestly:

**Build if:**
- The workflow is specific to your company's unique process
- You need to connect 2-3 internal systems that don't talk to each other
- The team needs it now, not in Q3 next year
- You can maintain it (or someone on your team can)
- The tool will save more time than it takes to build

**Buy if:**
- It's a solved problem (like project management or CRM)
- The workflow is standard across industries
- You need enterprise support and SLAs
- The vendor offers integrations you'll actually use

The collections tool was a perfect build candidate. The workflow was entirely specific to our contract structure, payment terms, and customer segments. No SaaS product understood our business logic.

## The Anatomy of a Good Internal Tool

Here's what that collections tool actually looks like:

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import os
from datetime import datetime, timedelta
import secrets

from services.netsuite import get_overdue_customers
from services.salesforce import get_customer_health_scores
from services.stripe import get_payment_status

app = FastAPI(title="Collections Priority Dashboard")
security = HTTPBasic()

# Simple auth - good enough for internal tools
def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(
        credentials.username, os.getenv("TOOL_USERNAME")
    )
    correct_password = secrets.compare_digest(
        credentials.password, os.getenv("TOOL_PASSWORD")
    )
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return credentials.username

class CollectionsPriority(BaseModel):
    customer_id: str
    customer_name: str
    amount_overdue: float
    days_overdue: int
    health_score: str
    last_payment_date: str
    priority_score: int
    recommended_action: str

@app.get("/")
async def root():
    return {"message": "Collections Priority Dashboard API"}

@app.get("/priority-list", response_model=list[CollectionsPriority])
async def get_priority_list(username: str = Depends(verify_credentials)):
    """
    Returns prioritized list of customers for collections outreach.
    Combines data from NetSuite (AR), Salesforce (health), and Stripe (payment patterns).
    """

    # Pull data from three systems
    overdue = get_overdue_customers()
    health_scores = get_customer_health_scores()
    payment_history = get_payment_status()

    results = []

    for customer in overdue:
        cust_id = customer['id']
        amount = customer['amount_overdue']
        days = customer['days_overdue']

        # Get supplemental data
        health = health_scores.get(cust_id, 'unknown')
        last_payment = payment_history.get(cust_id, {}).get('last_payment_date', 'N/A')

        # Priority scoring logic specific to our business
        priority = calculate_priority_score(amount, days, health)
        action = recommend_action(priority, health, days)

        results.append(CollectionsPriority(
            customer_id=cust_id,
            customer_name=customer['name'],
            amount_overdue=amount,
            days_overdue=days,
            health_score=health,
            last_payment_date=last_payment,
            priority_score=priority,
            recommended_action=action
        ))

    # Sort by priority score descending
    results.sort(key=lambda x: x.priority_score, reverse=True)

    return results

def calculate_priority_score(amount: float, days: int, health: str) -> int:
    """
    Custom scoring logic based on our collections strategy.
    Higher score = higher priority.
    """
    score = 0

    # Amount weighting
    if amount > 100000:
        score += 50
    elif amount > 50000:
        score += 30
    elif amount > 10000:
        score += 15

    # Days overdue weighting
    if days > 60:
        score += 40
    elif days > 30:
        score += 25
    elif days > 15:
        score += 10

    # Health score weighting
    health_weights = {
        'red': 30,
        'yellow': 15,
        'green': -10  # Deprioritize healthy customers
    }
    score += health_weights.get(health, 0)

    return score

def recommend_action(priority: int, health: str, days: int) -> str:
    """Business logic for recommended next action."""
    if priority > 80:
        return "Escalate to Director - immediate call required"
    elif priority > 60:
        return "Personal outreach from Account Manager"
    elif priority > 40:
        return "Email reminder with payment link"
    elif days > 45:
        return "Standard collections notice"
    else:
        return "Monitor - auto-reminder in 7 days"
```

That's it. The entire API. Add 50 lines for the service integrations (NetSuite, Salesforce, Stripe clients), and you have a complete tool.

## Project Structure That Scales

Don't overthink structure for internal tools, but don't write spaghetti either:

```
collections-dashboard/
├── main.py                 # FastAPI app and routes
├── services/
│   ├── netsuite.py        # NetSuite API client
│   ├── salesforce.py      # Salesforce API client
│   └── stripe.py          # Stripe API client
├── models.py              # Pydantic models
├── config.py              # Configuration management
├── requirements.txt       # Dependencies
├── .env.example           # Environment variables template
└── README.md             # How to run this thing
```

Keep it simple. You're not building a SaaS product. You're solving one specific problem.

## Authentication Patterns for Internal Tools

For internal tools, you have three reasonable options:

**1. HTTP Basic Auth (what I used above)**
Good for: Quick tools, small teams, read-only dashboards
Bad for: Anything customer-facing, audit requirements

**2. SSO Integration (OAuth2 with your identity provider)**
Good for: Broader team access, audit trails, compliance requirements
Bad for: Quick builds, tools that run on schedules

**3. API Key per User**
Good for: Programmatic access, service accounts, automation
Bad for: Non-technical users, tools with UIs

For the collections dashboard, Basic Auth was fine. It's used by 8 people on the collections team. They access it via a simple HTML frontend that stores credentials in the browser. Not pretty, but it works.

When we built a similar tool for the accounting team that touches financial data, we integrated with Okta. Different tools, different requirements.

## Deployment: Keep It Simple

I deploy internal tools to a single EC2 instance running behind nginx. No Kubernetes. No microservices. No complexity.

**The stack:**
- Ubuntu 22.04 LTS
- Python 3.11 in a virtual environment
- Uvicorn running the FastAPI app
- Systemd to keep it running
- Nginx as reverse proxy for SSL termination
- Let's Encrypt for SSL certificates

**Total setup time:** 30 minutes, including SSL.

**Monthly cost:** $15 for a t3.small instance.

Here's the systemd service file:

```ini
# /etc/systemd/system/collections-dashboard.service
[Unit]
Description=Collections Dashboard API
After=network.target

[Service]
Type=notify
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/collections-dashboard
Environment="PATH=/home/ubuntu/collections-dashboard/venv/bin"
ExecStart=/home/ubuntu/collections-dashboard/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Run it with:
```bash
sudo systemctl enable collections-dashboard
sudo systemctl start collections-dashboard
```

It restarts on failure. It starts on boot. It runs forever.

## The Frontend (Or Lack Thereof)

FastAPI generates automatic OpenAPI documentation at `/docs`. For technical users, that's often good enough.

For the collections team, I built a 100-line HTML file with some JavaScript to call the API and render a sortable table. No build process. No React. No npm. Just a single HTML file they can bookmark.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Collections Priority Dashboard</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #4CAF50; color: white; cursor: pointer; }
        .high-priority { background-color: #ffebee; }
    </style>
</head>
<body>
    <h1>Collections Priority Dashboard</h1>
    <button onclick="loadData()">Refresh Data</button>
    <table id="priorityTable">
        <thead>
            <tr>
                <th onclick="sortTable(0)">Customer</th>
                <th onclick="sortTable(1)">Amount Overdue</th>
                <th onclick="sortTable(2)">Days Overdue</th>
                <th onclick="sortTable(3)">Health</th>
                <th onclick="sortTable(4)">Priority</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody id="tableBody"></tbody>
    </table>

    <script>
        async function loadData() {
            const response = await fetch('/priority-list', {
                headers: {
                    'Authorization': 'Basic ' + btoa('username:password')
                }
            });
            const data = await response.json();
            renderTable(data);
        }

        function renderTable(data) {
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';
            data.forEach(item => {
                const row = tbody.insertRow();
                if (item.priority_score > 80) row.classList.add('high-priority');
                row.innerHTML = `
                    <td>${item.customer_name}</td>
                    <td>$${item.amount_overdue.toLocaleString()}</td>
                    <td>${item.days_overdue}</td>
                    <td>${item.health_score}</td>
                    <td>${item.priority_score}</td>
                    <td>${item.recommended_action}</td>
                `;
            });
        }

        loadData(); // Load on page load
    </script>
</body>
</html>
```

Ship it.

## Maintenance and Evolution

The collections tool has been running for 18 months. I've touched it exactly three times:

1. Added a new field when we started tracking payment method
2. Updated the Stripe client when they changed their API
3. Fixed a bug where negative balances (credits) were showing as overdue

Total maintenance time: 4 hours over 18 months.

The ROI is absurd. The team saves 45 minutes per day. That's 195 hours per year, or about $10k in productivity. I spent 6 hours building it.

## When Internal Tools Grow Up

Sometimes an internal tool becomes critical infrastructure. When that happens, you'll know:

- More than 50 people depend on it daily
- Downtime creates immediate business impact
- Data accuracy becomes a compliance requirement
- You need audit trails and access controls

At that point, migrate it to proper infrastructure. Add monitoring. Write tests. Implement proper CI/CD. Bring in your platform team.

But start simple. Most internal tools never grow up, and that's fine.

Your team needs tools that solve their specific problems. FastAPI makes it easy to build exactly that—no framework bloat, no vendor lock-in, just Python and HTTP doing what they do best.

The collections dashboard still runs on that t3.small instance. Still saves 45 minutes a day. Still costs $15 a month.

Sometimes the right tool is the one you build yourself.
