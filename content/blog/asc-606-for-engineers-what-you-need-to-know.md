---
title: "ASC 606 for Engineers: What You Need to Know"
slug: "asc-606-for-engineers-what-you-need-to-know"
excerpt: "Revenue recognition isn't just an accounting problem. If you build billing systems, ASC 606 shapes what you can and can't do — and most engineers have never heard of it."
tags: ["ASC 606", "Revenue Recognition", "SaaS Finance", "Compliance"]
published: true
featured: true
created_at: "2026-02-16"
published_at: "2026-02-16"
author: "Brian Hardin"
meta_description: "ASC 606 revenue recognition explained for engineers and technical leaders, including the five-step model and its impact on billing system design."
---

Revenue recognition isn't just an accounting problem. If you build billing systems, ASC 606 shapes what you can and can't do—and most engineers have never heard of it.

I learned about ASC 606 the hard way. We were six weeks from going public when our controller walked into an engineering planning meeting and said, "We need to change how the billing system works. We can't recognize revenue the way we're currently doing it."

The team looked at me like I'd grown a second head. We'd just spent four months rebuilding our invoicing pipeline. It worked. Customers were getting billed correctly. What could possibly be wrong?

Turns out, **billing correctly and recognizing revenue correctly are two different problems.** ASC 606 is the accounting standard that governs the second one, and if you're building B2B SaaS billing systems at any company that might go public or get acquired, you need to understand it.

Let me save you the six weeks of panic we went through.

## What ASC 606 Actually Is

ASC 606 (officially "Accounting Standards Codification Topic 606") is the FASB standard for revenue recognition. It replaced the old rules in 2018 and fundamentally changed how software companies account for revenue.

The old system had different rules for different industries. SaaS companies followed one set of guidelines, on-premise software followed another, consulting followed a third. ASC 606 created a single framework that applies to almost all revenue contracts.

**For public companies, ASC 606 compliance isn't optional.** Your auditors will review your revenue recognition process, and if you're doing it wrong, you'll fail your audit. I've seen this delay IPOs and derail M&A deals.

For pre-IPO companies, you might not be thinking about this yet. But when you start having those conversations with bankers and auditors, they'll ask how you're recognizing revenue. If the answer is "we recognize it when we bill it," you have a problem.

## The Five-Step Model (Simplified)

ASC 606 defines a five-step process for recognizing revenue. I'm going to explain this in engineering terms, not accounting-speak.

### Step 1: Identify the Contract

A contract exists when there's an agreement between your company and a customer that creates enforceable rights and obligations. Usually, this is your signed order form or MSA.

From a systems perspective: **your billing system needs to know which legal agreement governs each charge.** This means tracking contract IDs, effective dates, and amendment history.

We store this in our CRM (Salesforce), but our billing system (Stripe Billing) needs to reference it. The link between the two is critical for audit purposes.

### Step 2: Identify Performance Obligations

This is where it gets interesting. A performance obligation is a promise to deliver a distinct good or service.

Here's the nuance: **if you sell a bundle, you need to identify each distinct component.**

Example from my current company:

- Platform subscription: $10,000/month
- Implementation services: $50,000 one-time
- Premium support: $2,000/month

Under ASC 606, these are three separate performance obligations, even if they're on one invoice. Why? Because the customer could theoretically buy each one independently, and each one delivers value on its own.

### Step 3: Determine the Transaction Price

This is the total amount you expect to receive. Sounds simple, but there are wrinkles:

- Variable consideration (usage-based pricing)
- Discounts applied at the invoice level
- Credits or refund rights
- Non-cash consideration

**If your pricing model includes usage-based components, this step gets complicated.** You need to estimate the variable consideration using either the expected value method or the most likely amount method. Your accounting team will have opinions about which one to use.

### Step 4: Allocate the Transaction Price to Performance Obligations

You need to split the total contract value across each performance obligation based on standalone selling price (SSP).

Here's a simplified example:

| Performance Obligation | SSP | % of Total | Allocated Amount |
|------------------------|-----------|------------|------------------|
| Platform (12 months) | $120,000 | 70.6% | $84,700 |
| Implementation | $50,000 | 29.4% | $35,300 |
| **Total** | **$170,000** | **100%** | **$120,000** |

Wait—why doesn't the allocated amount equal the SSP?

Because the customer got a discount. They paid $120,000 for $170,000 worth of services. ASC 606 requires you to allocate that $50,000 discount proportionally across all performance obligations.

**From a systems perspective, this means your billing system can't just recognize revenue equal to the invoice amount.** You need logic that allocates revenue based on SSP, applies discounts proportionally, and tracks how much of each performance obligation has been delivered.

### Step 5: Recognize Revenue When Performance Obligations Are Satisfied

This is the step that impacts system design the most.

Revenue is recognized either:
- **At a point in time** (when control transfers, like shipping a product)
- **Over time** (as the service is delivered, like SaaS)

For SaaS subscriptions, you almost always recognize revenue over time. If I sell an annual contract for $120,000 on January 1, I recognize $10,000 per month for 12 months—not $120,000 on January 1.

**The critical system requirement: you need to track the period over which each performance obligation is satisfied, and recognize revenue proportionally across that period.**

## What This Means for System Design

When we rebuilt our billing system to be ASC 606 compliant, here are the changes we had to make:

### Revenue Schedules

We added a revenue schedule table that tracks when to recognize revenue for each line item on every invoice.

Schema (simplified):

```sql
CREATE TABLE revenue_schedules (
  id UUID PRIMARY KEY,
  invoice_line_item_id UUID NOT NULL,
  performance_obligation_id UUID NOT NULL,
  recognition_period_start DATE NOT NULL,
  recognition_period_end DATE NOT NULL,
  allocated_amount DECIMAL(10,2) NOT NULL,
  recognized_to_date DECIMAL(10,2) DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);
```

Every time we invoice a customer, we create revenue schedule records that define when to recognize that revenue. Our month-end close process queries this table to determine how much revenue to recognize in the current period.

### Performance Obligation Tracking

We needed a table to define all possible performance obligations across our product catalog:

```sql
CREATE TABLE performance_obligations (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  recognition_type VARCHAR(20) NOT NULL, -- 'over_time' or 'point_in_time'
  standalone_selling_price DECIMAL(10,2),
  gl_account VARCHAR(50) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

Each SKU in our product catalog maps to one or more performance obligations. When we add a new product, we define its performance obligations and SSP before we can sell it.

### Deferred Revenue Calculation

The formula for deferred revenue is:

```
Deferred Revenue = Total Allocated Amount - Revenue Recognized to Date
```

Every month, we run a process that:
1. Queries all revenue schedules where `recognition_period_start <= today <= recognition_period_end`
2. Calculates how much revenue to recognize based on time elapsed
3. Updates `recognized_to_date`
4. Posts journal entries to our ERP (NetSuite)

**This process must be auditable.** We maintain logs of every revenue recognition event, including the calculation logic, input values, and output.

## Contract Modifications Are Evil

Here's where ASC 606 becomes a nightmare: contract modifications.

A contract modification happens when you change the terms of an existing contract—like adding users, changing pricing, or extending the term.

Under ASC 606, you need to determine whether the modification is:
1. **A separate contract** (if you're adding distinct goods/services at their SSP)
2. **A termination and new contract** (if the remaining goods/services are distinct)
3. **Part of the existing contract** (if the remaining goods/services are not distinct)

Each of these requires different accounting treatment.

Example: Customer signs a 12-month contract for $120,000 on January 1. On July 1, they want to add another product for $60,000 for the remaining 6 months.

Is this a separate contract? Depends on whether the new product is priced at its SSP. If they're getting a discount because they're an existing customer, it might not be. Your accounting team will need to analyze this.

**From a systems perspective, contract modifications require you to:**
- Recalculate revenue schedules mid-period
- Track the modification reason and accounting treatment
- Handle pro-rata adjustments
- Maintain an audit trail

We built a contract modification workflow that requires finance approval before the billing system processes the change. This ensures the accounting treatment is correct before we create invoices.

## Usage-Based Pricing Is Complicated

If your pricing includes usage-based components (per API call, per seat, per GB), ASC 606 makes this challenging.

The standard requires you to estimate variable consideration and include it in the transaction price—but only to the extent it's probable that recognizing that revenue won't result in a significant reversal later.

Translation: **You need to estimate how much usage revenue you'll collect, but only recognize the amount you're confident about.**

We handle this with a two-step process:

1. **Minimum commitment:** If the contract guarantees $10,000/month minimum, we recognize that evenly over the term.
2. **Overage:** If the customer uses more, we recognize that revenue as it's incurred (since it's no longer variable—it happened).

The challenge is when customers prepay for usage credits. We had a customer prepay $500,000 for API credits. Under ASC 606, we recognize that revenue as the credits are consumed, not when we receive the cash.

**System requirement:** Track prepaid credit balances, consumption by period, and revenue recognized to date. We built a credits ledger that logs every consumption event and ties it to revenue recognition.

## Professional Services and SaaS Bundles

Many SaaS companies sell implementation services alongside subscriptions. This is where SSP allocation gets messy.

Say you sell:
- $120,000 annual subscription (SSP: $120,000)
- $50,000 implementation (SSP: $75,000)

Total contract value: $170,000
Total SSP: $195,000

The discount is $25,000, which needs to be allocated proportionally:

| Component | SSP | % | Allocated Price | Discount |
|-----------|----------|-------|-----------------|----------|
| Subscription | $120,000 | 61.5% | $104,600 | $15,400 |
| Implementation | $75,000 | 38.5% | $65,400 | $9,600 |

You recognize the subscription revenue over 12 months: $8,717/month.

You recognize the implementation revenue when the work is complete. **But here's the catch:** if the implementation takes 3 months, do you recognize it evenly over 3 months or all at once when the customer goes live?

ASC 606 says it depends on whether the customer receives and consumes the benefits as you perform the work. For most implementations, the answer is "over time," which means you need to track percent-complete.

**System requirement:** We built a project tracking module that lets project managers update percent-complete, which triggers revenue recognition. This required integrating our billing system with our PSA tool (FinancialForce).

## Multi-Element Arrangements Are Worse

If you sell SaaS, professional services, and third-party software in one contract, you have a multi-element arrangement (MEA).

Example:
- Your SaaS platform: $100,000/year
- Implementation services: $50,000
- Snowflake data warehouse (resold): $20,000/year

Each of these is a separate performance obligation. The SaaS and Snowflake are recognized over time. Implementation is recognized when complete (or over the implementation period).

**The Snowflake component is interesting:** If you're reselling Snowflake, are you acting as a principal or an agent?

- **Principal:** You control the service before transferring it to the customer. You recognize the full $20,000 as revenue and the cost to Snowflake as COGS.
- **Agent:** You're arranging for Snowflake to provide the service. You recognize only your margin as revenue.

This distinction changes your revenue by $20,000/year. Your auditors will scrutinize this.

## What Happens If You Get It Wrong

I worked with a company that was recognizing all revenue at the time of invoicing. When they started their S-1 process, their auditors flagged it.

They had to restate three years of financials. **This delayed their IPO by six months** and required them to rebuild their entire revenue recognition system.

The cost:
- $2M in audit fees
- $1.5M in engineering and consulting
- 6 months of executive time
- Damaged credibility with investors

Getting ASC 606 wrong isn't just an accounting problem. It's a business problem.

## How to Build for ASC 606 From the Start

If you're building a billing system and you want to avoid the nightmare we went through, here's what to build:

### 1. Separate Billing from Revenue Recognition

**Your billing system should create invoices. A separate system should handle revenue recognition.**

We use:
- **Stripe Billing** for subscription management and invoicing
- **NetSuite Revenue Management** for revenue recognition
- **Custom middleware** to translate Stripe events into revenue schedules

This separation ensures billing logic doesn't get polluted with accounting rules, and accounting logic doesn't interfere with getting customers invoiced.

### 2. Track Performance Obligations at the SKU Level

Every product you sell should map to one or more performance obligations. Define these before you start selling.

We have a product catalog that looks like:

| SKU | Name | Performance Obligations | SSP |
|-----|------|-------------------------|-----|
| PLAT-ENT | Enterprise Platform | Platform Access | $120,000/yr |
| IMPL-STD | Standard Implementation | Implementation Services | $50,000 |
| SUPP-PREM | Premium Support | Support Services | $24,000/yr |

When a sales rep adds SKU "PLAT-ENT" to a quote, the system knows it's creating a platform access performance obligation with SSP of $120,000/year.

### 3. Build Revenue Schedules Automatically

When an invoice is created, automatically generate revenue schedules based on:
- Performance obligations on the invoice
- SSP allocation
- Recognition period (contract start/end dates)
- Recognition method (over time vs. point in time)

**This should happen programmatically, not manually.** If your finance team is creating revenue schedules in spreadsheets, you're going to have problems at scale.

### 4. Make Everything Auditable

Every revenue recognition event should be logged with:
- Timestamp
- User/system that triggered it
- Input data
- Calculation logic
- Output (revenue amount, GL account, period)

We send all revenue recognition events to a data warehouse where auditors can query them. This has saved us countless hours during audits.

### 5. Work with Your Accounting Team Early

**Don't build a billing system in isolation.** Your controller needs to review the design before you write code.

We now have monthly meetings between engineering and accounting where we review upcoming features and discuss revenue recognition implications. This has prevented so many problems.

## The Real Impact

ASC 606 feels like bureaucratic overhead until you're trying to go public or get acquired.

I've been through two IPOs and three M&A transactions. In every one, revenue recognition was a top-3 diligence item. Buyers and investors want to know:

1. How do you recognize revenue?
2. Is it ASC 606 compliant?
3. Can you prove it?

If the answers are "we recognize when we bill," "probably not," and "no," you're going to have a bad time.

**Building for ASC 606 compliance from the start is an investment in your company's future.** It's the difference between a smooth IPO process and a six-month fire drill.

And for engineers, it's a reminder that the systems we build don't exist in a vacuum. They exist in a world of regulations, audits, and accounting standards. **Understanding ASC 606 won't make you a better programmer, but it will make you a better system designer.**

Which, at the end of the day, is what we're here to do.
