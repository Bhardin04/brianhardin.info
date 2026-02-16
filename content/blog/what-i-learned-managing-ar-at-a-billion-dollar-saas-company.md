---
title: "What I Learned Managing AR at a Billion-Dollar SaaS Company"
slug: "what-i-learned-managing-ar-at-a-billion-dollar-saas-company"
excerpt: "At scale, accounts receivable stops being an accounting function and starts being a strategic operation. Here are the lessons that shaped how I think about AR."
tags: ["Revenue Operations", "Accounts Receivable", "SaaS", "Leadership"]
published: true
featured: true
created_at: "2025-08-25"
published_at: "2025-08-25"
author: "Brian Hardin"
meta_description: "Lessons learned managing accounts receivable at a billion-dollar SaaS company, from DSO management to team structure and technology decisions."
---

# What I Learned Managing AR at a Billion-Dollar SaaS Company

When I took over AR operations at a company approaching $1B in annual recurring revenue, I thought I understood the job. I'd managed billing teams before. I knew how to read an aging report. I understood the basics of collections.

I was wrong.

Managing AR at scale isn't about processing invoices and making collection calls. It's about **building systems that protect cash flow, enabling visibility that drives decisions, and creating processes that scale without breaking.**

Here are the lessons that reshaped how I think about accounts receivable—and why AR deserves a seat at the strategic table.

## Lesson 1: AR Is a Leading Indicator, Not a Lagging One

Most executives treat AR as a backward-looking metric. "How much do we have outstanding?" "What's our DSO this month?"

But AR is actually one of the **best leading indicators** of business health you have.

### What AR Tells You About Your Business

**1. Customer Health**

When a previously reliable customer starts paying late, that's often the first signal of trouble—long before they tell Customer Success they're thinking about churning.

We started tracking **payment pattern changes** as a customer health metric. If a customer who historically paid within 10 days starts paying at 45 days, that triggers a CSM check-in. We caught churn risk three months early multiple times using this signal.

**2. Product or Service Quality Issues**

A spike in disputed invoices isn't just a collections problem—it's feedback. If multiple customers are disputing the same line items, something is wrong upstream.

We once saw a 30% increase in invoice disputes over two weeks. Turns out, a billing system update had changed how usage was calculated, and customers noticed before we did. AR surfaced the problem; product fixed it.

**3. Sales Execution Issues**

When deals close with non-standard payment terms—Net 60, Net 90, quarterly payments instead of monthly—it often means sales gave away terms to close the deal.

We implemented a **payment terms approval workflow**. Any deal with terms longer than Net 30 required VP approval. Sales complained initially, but CFO loved it. Within six months, our weighted average payment terms dropped from 38 days to 31 days.

**4. Process Bottlenecks**

If invoices consistently go out late, that's not an AR problem—it's an order-to-cash problem. If payment reminders aren't being sent, that's an automation gap. If customers complain that invoices are confusing, that's a UX problem.

**AR doesn't create these problems, but AR *surfaces* them.** If you're paying attention, AR can help you fix issues across the entire revenue lifecycle.

## Lesson 2: DSO Is a Vanity Metric—Here's What to Track Instead

Every CFO watches Days Sales Outstanding (DSO). But DSO alone doesn't tell you much.

**DSO formula:**
```
DSO = (Accounts Receivable / Total Credit Sales) × Number of Days
```

The problem? DSO is heavily influenced by factors outside AR's control:
- Your payment terms (Net 30 vs. Net 60)
- Your customer mix (SMB vs. Enterprise)
- Seasonality and billing cycles

**A better approach: track DSO *and* these metrics:**

### 1. Collection Effectiveness Index (CEI)

CEI measures how much of the collectible AR you actually collected in a period.

**Formula:**
```
CEI = (Beginning AR + Credit Sales - Ending AR) / (Beginning AR + Credit Sales - Ending Current AR) × 100
```

**Target:** 95%+

A declining CEI means you're collecting less of what's owed—even if DSO stays flat.

### 2. AR Aging Distribution

Instead of total AR, look at the *distribution* of aging:

| Bucket | % of Total AR | Target |
|--------|---------------|--------|
| Current (0-30 days) | 75% | 70-80% |
| 31-60 days | 15% | 10-20% |
| 61-90 days | 7% | 5-8% |
| 90+ days | 3% | <5% |

If the 90+ bucket is growing as a percentage, you have a collections problem—even if total AR is stable.

### 3. Past Due as a % of Total AR

This is simple but powerful:

```
Past Due % = (AR > 30 days) / Total AR
```

**Target:** <25%

We tracked this weekly. If it spiked above 30%, we triggered an immediate review to identify the root cause—usually a specific customer segment or a process breakdown.

### 4. Invoice Dispute Rate

```
Dispute Rate = (Disputed Invoices / Total Invoices) × 100
```

**Target:** <5%

A spike in disputes means something upstream (billing, product, sales) is broken.

### 5. Days Deduction Outstanding (DDO)

This is DSO's cousin—how long are deductions and disputes sitting unresolved?

```
DDO = (Unresolved Deductions / Average Daily Credit Sales) × Number of Days
```

**Target:** <15 days

At scale, unresolved deductions can represent millions in "ghost AR"—money you think you're owed but will never collect.

## Lesson 3: Team Structure Matters More Than Headcount

Early-stage companies treat AR as part of the accounting team. At scale, that doesn't work.

Here's the structure we landed on:

### AR Collections Team (4 FTEs at $100M ARR)
**Focus:** Customer outreach, payment follow-up, escalation management.

**Key skills:**
- Communication (written and verbal)
- Empathy and relationship management
- CRM proficiency (they live in NetSuite and Salesforce)

These are not accountants. They're **customer-facing operations people** who happen to work in finance.

### AR Operations Team (2 FTEs)
**Focus:** Process optimization, automation, data quality, reporting.

**Key skills:**
- ERP expertise (NetSuite, Salesforce integration)
- SQL and data analysis
- Process mapping and workflow design

This team builds the systems that let the collections team scale. They're the ones who built our payment tracking dashboard, automated reminders, and escalation workflows.

### Disputes & Deductions Team (1 FTE)
**Focus:** Resolving invoice disputes, handling deductions, reconciling short payments.

**Key skills:**
- Attention to detail
- Cross-functional coordination (they work with Sales, CS, Product)
- Problem-solving under ambiguity

Disputes can't be automated. They require investigation, collaboration, and judgment. Dedicating a person to this ensures disputes get resolved fast instead of sitting in a queue.

### AR Leadership (1 FTE—me)
**Focus:** Strategy, cross-functional alignment, reporting to leadership.

At scale, AR needs someone who can translate AR performance into business insights for the executive team.

**That's 8 people managing $100M in ARR and ~$15M in outstanding AR.** It sounds like a lot, but the ROI is clear: we reduced DSO by 12 days in the first year, which freed up $3.3M in working capital.

## Lesson 4: Technology Is Your Leverage Point

You cannot scale AR with spreadsheets and manual processes. At $100M ARR, you'll drown.

Here's our tech stack:

### 1. ERP (NetSuite)
The source of truth for invoices, payments, AR aging, and customer data. Everything flows through NetSuite.

### 2. Payment Processing (Stripe + Bill.com)
- **Stripe** for credit card payments (mostly SMB)
- **Bill.com** for ACH and check processing (mostly Enterprise)

Both integrate directly with NetSuite for automated cash application.

### 3. Collections Automation (Tesorio)
Sends automated reminders, tracks customer payment behavior, flags high-risk accounts. We tested several tools—Tesorio was the best fit for SaaS at our scale.

### 4. BI / Reporting (QlikSense)
Custom dashboards for AR aging, DSO trends, collections performance, and payment pattern analysis.

We built a **real-time AR dashboard** that the CFO checks daily:
- Current DSO
- AR aging distribution
- Top 10 overdue accounts
- Week-over-week payment velocity
- Collections team activity log

### 5. CRM Integration (Salesforce ↔ NetSuite)
AR needs visibility into customer relationships. When we're escalating collections, we need to know:
- Is this customer in renewal discussions?
- Is there an open support ticket?
- Who's the relationship owner?

We built a **two-way sync** so AR can see customer context in NetSuite, and Sales/CS can see payment history in Salesforce.

## Lesson 5: Policies Without Enforcement Are Just Suggestions

We spent months documenting AR policies—payment terms, collections escalation, service suspension criteria, write-off thresholds.

Then we realized: **nobody was following them.**

Collections agents were making judgment calls inconsistently. Some customers got 90-day grace periods because they were "strategic accounts." Others got suspended at 60 days.

We learned: **A policy without accountability is useless.**

Here's what we implemented:

### 1. Mandatory Escalation Checkpoints
Every account that hits 60 days past due gets reviewed by the AR Manager. Every account at 90 days gets reviewed by the VP of Finance. No exceptions.

### 2. Service Suspension Authority
Only the VP of Finance can approve exceptions to the suspension policy. If an account executive wants to delay suspension, they need executive sign-off. This forces a real conversation about risk vs. relationship.

### 3. Weekly AR Review with Executive Sponsor
Every Monday, we review the top 20 overdue accounts with the CFO. Each one has a **status update and next action**. If an account has been sitting at 90+ days for three weeks with no progress, someone has to explain why.

**This level of rigor changes behavior.** When people know they'll be asked about inaction, they act.

## Lesson 6: AR Performance Is a Cross-Functional Effort

AR touches **every revenue function**:

| Function | AR Dependency |
|----------|---------------|
| **Sales** | Payment terms, billing contacts, contract accuracy |
| **Customer Success** | Relationship health, customer context for collections |
| **Finance** | Revenue recognition, cash forecasting, reporting |
| **Product** | Billing system reliability, usage data accuracy |
| **IT** | System integrations, automation, data quality |

If AR is treated as "Finance's problem," it will fail.

We started holding **monthly O2C (Order-to-Cash) review meetings** with representatives from Sales, CS, Finance, Product, and IT. We review:
- AR aging trends
- Collection escalation cases
- Billing system issues
- Process improvement ideas

This meeting became one of the most valuable forums in the company. Problems that used to take weeks to resolve now get fixed in days because the right people are in the room.

## Lesson 7: Celebrate the Wins

AR teams don't get celebrated the way Sales teams do. There's no gong when you collect a 90-day-overdue invoice.

But **recognition matters.**

We started tracking and celebrating:
- **Month-over-month DSO improvement**
- **Accounts brought current** (from 60+ days to paid)
- **Dispute resolution time**
- **Process improvements** that saved time or reduced errors

Every quarter, I present AR metrics to the executive team with **specific shout-outs** to team members who drove results.

This sounds small, but it transformed morale. The AR team went from feeling like the "bad guys chasing money" to feeling like **strategic operators protecting the business.**

## Lesson 8: You Can't Outsource Judgment

We explored outsourcing collections to a third party. On paper, it looked attractive—lower cost per FTE, 24/7 coverage, specialized expertise.

We ran a pilot with 100 accounts. It was a disaster.

The outsourced team followed the process perfectly, but they had **zero context**. They didn't know which customers were strategic. They didn't understand our product. They couldn't navigate internal systems to resolve disputes.

**Collections at scale requires judgment, and judgment requires context.**

We kept collections in-house and invested in training, technology, and process documentation instead. It cost more upfront, but the ROI in relationship preservation and collection effectiveness was undeniable.

## The Bottom Line

When I started managing AR at scale, I thought the job was about efficiency—process more invoices, make more calls, collect more cash.

But the real job is about **building systems that scale, creating visibility that drives decisions, and positioning AR as a strategic function that protects the business.**

At $1B ARR, AR isn't a cost center. It's **revenue protection infrastructure.**

Here's what I'd tell any leader stepping into AR at scale:

1. **Treat AR as a leading indicator.** Use it to surface problems across the business.
2. **Go beyond DSO.** Track CEI, aging distribution, and dispute rates.
3. **Invest in team structure.** You need specialists, not generalists.
4. **Leverage technology.** Automation is your only path to scale.
5. **Enforce policies consistently.** Otherwise, they're just suggestions.
6. **Make it cross-functional.** AR can't succeed in a silo.
7. **Celebrate wins.** Recognition drives performance.
8. **Keep judgment in-house.** Context matters too much to outsource.

The companies that figure this out collect cash faster, close their books cleaner, and scale without breaking.

The ones that don't end up fighting fires every month-end, wondering why DSO keeps creeping up and why finance is always underwater.

AR isn't glamorous. But at scale, it's one of the highest-leverage functions in the business.

Treat it that way.
