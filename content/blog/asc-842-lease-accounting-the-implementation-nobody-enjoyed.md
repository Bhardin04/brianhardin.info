---
title: "ASC 842 Lease Accounting: The Implementation Nobody Enjoyed"
slug: "asc-842-lease-accounting-the-implementation-nobody-enjoyed"
excerpt: "If you think lease accounting is boring, you've never had to implement it in an ERP system two weeks before an audit. Here's what the implementation actually looks like."
tags: ["ASC 842", "Lease Accounting", "Compliance", "ERP Implementation"]
published: true
featured: false
created_at: "2026-02-23"
published_at: "2026-02-23"
author: "Brian Hardin"
meta_description: "Lessons from implementing ASC 842 lease accounting in NetSuite, including data migration challenges and audit preparation."
---

If you think lease accounting is boring, you've never had to implement it in an ERP system two weeks before an audit.

It was late 2019, and our external auditors dropped this in a planning call: "You know ASC 842 went into effect this year, right? We'll need to review your lease accounting."

I looked at our controller. She looked at me. We both knew we had a problem.

ASC 842 is the accounting standard for leases. It went into effect January 1, 2019 for public companies and January 1, 2022 for private companies. **The standard requires companies to put most leases on the balance sheet**, which sounds simple until you try to actually do it.

We had three months until our year-end audit and zero systems in place to comply. Let me walk you through what that implementation looked like, because if you're in a similar position, you're about to have a very bad quarter.

## What ASC 842 Actually Requires

Before ASC 842, operating leases were off-balance-sheet. You'd disclose them in the footnotes, but they didn't impact your balance sheet. Finance leases (previously called capital leases) were on the balance sheet.

ASC 842 changed this. Now, **almost all leases must be on the balance sheet** as a right-of-use (ROU) asset and a lease liability.

The logic: if you've signed a 5-year office lease, you have an asset (the right to use that office for 5 years) and a liability (the obligation to pay rent). Those should be reflected in your financials.

### The Lease Classification

Leases are classified as either:
1. **Finance leases** (similar to the old capital leases)
2. **Operating leases** (everything else)

The classification affects how you recognize expense—finance leases have front-loaded expense (like a loan), operating leases have straight-line expense—but both go on the balance sheet.

The criteria for finance vs. operating are technical, but the short version: if the lease transfers ownership, is for most of the asset's useful life, or has a bargain purchase option, it's probably a finance lease. Otherwise, it's operating.

**For our implementation, we had 47 operating leases and 2 finance leases** (both vehicle leases). The operating leases were the bulk of the work.

## Our Starting Point (A Disaster)

Here's what we had when we started:

- **Lease documentation:** PDF files in a Dropbox folder labeled "Leases - Do Not Delete"
- **Payment tracking:** Expensed monthly in NetSuite based on invoices received
- **Lease data:** A spreadsheet the previous controller maintained, last updated 14 months prior
- **Amendments and renewals:** Some documented, some not

We had no centralized system, no consistent data structure, and no idea if we even had a complete list of leases.

**This is more common than you think.** Most companies don't manage leases well because, historically, they weren't balance sheet items. You just paid rent and moved on.

ASC 842 changed that overnight.

## Step 1: Inventory Your Leases

The first step was figuring out what we even had. We needed to identify every contract that might be a lease.

ASC 842 defines a lease as "a contract, or part of a contract, that conveys the right to control the use of identified property, plant, or equipment for a period of time in exchange for consideration."

That's broader than you think. It includes:
- Office leases
- Vehicle leases
- Equipment leases
- Data center space
- Warehouse space
- **Embedded leases in service contracts**

That last one is insidious. We had a managed services contract for our data center that included dedicated rack space. Under ASC 842, that's a lease embedded in a service contract.

### The Scavenger Hunt

We assigned someone from accounting to dig through:
- Accounts payable records for recurring payments to landlords or leasing companies
- Legal's contract management system
- Procurement's vendor list
- Real estate's records
- IT's vendor agreements

**We found 12 leases that weren't on the original spreadsheet.** Most were small (a copier, a storage unit), but one was a $180,000/year warehouse lease that someone in operations had signed without looping in finance.

The data we needed for each lease:
- Lease term (start date, end date)
- Payment schedule (monthly amount, escalations, variable payments)
- Renewal options
- Termination options
- Discount rate (more on this nightmare later)

We built a spreadsheet that became our source of truth:

| Lease ID | Description | Lessor | Start Date | End Date | Monthly Payment | Escalation | Discount Rate | Classification |
|----------|-------------|--------|------------|----------|-----------------|------------|---------------|----------------|
| L-001 | HQ Office | Landlord Corp | 2018-01-01 | 2028-12-31 | $45,000 | 3% annual | 5.2% | Operating |
| L-002 | SF Office | Bay Properties | 2019-03-01 | 2024-02-28 | $28,000 | 2.5% annual | 5.2% | Operating |
| L-003 | Company Vehicle | Ford Credit | 2019-06-01 | 2022-05-31 | $850 | None | 4.8% | Finance |

This took six weeks.

## Step 2: Calculate Initial Balances

ASC 842 requires you to calculate:
1. **Lease liability:** The present value of future lease payments
2. **ROU asset:** Generally equal to the lease liability, adjusted for prepayments, initial direct costs, and lease incentives

The formula for lease liability is:

```
Lease Liability = Σ (Payment_t / (1 + r)^t)

Where:
- Payment_t = lease payment in period t
- r = discount rate
- t = period number
```

This is a standard present value calculation, but there are wrinkles.

### The Discount Rate Problem

You're supposed to use the rate implicit in the lease. For most operating leases (like office space), **you have no idea what that rate is** because the lessor doesn't disclose it.

ASC 842 allows you to use your incremental borrowing rate (IBR)—the rate you'd pay to borrow money for a similar term. But determining your IBR requires:
- Knowing your credit profile
- Understanding market rates for similar term debt
- Adjusting for collateral (leases are secured by the leased asset)

We worked with our bank to get an IBR schedule based on lease term:

| Lease Term | IBR |
|------------|-----|
| 1-3 years | 4.5% |
| 3-5 years | 5.0% |
| 5-10 years | 5.2% |
| 10+ years | 5.5% |

**These rates are critical.** A 1% change in discount rate can swing your lease liability by 5-10% for long-term leases.

### The Calculation Spreadsheet

For each lease, we built a payment schedule and calculated the PV:

Example for our HQ lease:

| Period | Date | Payment | PV Factor (5.2%) | Present Value |
|--------|------|---------|------------------|---------------|
| 1 | 2020-01-31 | $45,000 | 0.9959 | $44,816 |
| 2 | 2020-02-29 | $45,000 | 0.9918 | $44,631 |
| 3 | 2020-03-31 | $45,000 | 0.9877 | $44,447 |
| ... | ... | ... | ... | ... |
| 108 | 2028-12-31 | $58,481 | 0.5934 | $34,702 |

**Total Lease Liability: $4,287,394**

We had to do this for 49 leases. The calculations themselves weren't hard—Excel can do PV functions—but the data entry and validation were brutal.

## Step 3: Choose and Configure a System

We evaluated three options for managing lease accounting:

### Option 1: Spreadsheets

**Pros:** Free, familiar, flexible
**Cons:** Not auditable, error-prone, doesn't scale, no integration with NetSuite

We ruled this out immediately. Our auditors wouldn't accept a spreadsheet-based process.

### Option 2: NetSuite Lease Accounting Module

**Pros:** Native integration with our ERP, built by our ERP vendor
**Cons:** $30,000/year, limited functionality for complex leases

This was the obvious choice, but when we demoed it, we found it couldn't handle:
- Leases with variable rent based on sales (we had 3 retail locations with revenue-sharing clauses)
- Embedded leases in service contracts
- Mid-lease modifications without creating a new lease

### Option 3: Third-Party Lease Accounting Software

We evaluated LeaseQuery, Visual Lease, and CoStar.

**We went with LeaseQuery** because:
- Better handling of complex lease structures
- Strong NetSuite integration (automated journal entry posting)
- Good audit trail and reporting
- $18,000/year for our lease volume

The implementation took 4 weeks from contract signature to go-live.

## Step 4: Data Migration (The Nightmare)

Loading our 49 leases into LeaseQuery sounds simple. It wasn't.

### The Data Quality Issues

Almost every lease had problems:

**HQ Office Lease:**
- Original lease was 10 years starting 2018
- Amendment in 2020 extended it to 2028
- Rent escalations changed from fixed 2% to CPI-based
- Tenant improvement allowance was $500K, half paid in 2018, half in 2019

**How do you model this?** You can't just enter "10-year lease starting 2018." You need to account for the modification in 2020, which under ASC 842 might require remeasuring the lease.

We spent three weeks with our auditors determining how to handle each modification. Some were treated as new leases, some as modifications to existing leases. Each required different accounting.

**SF Office Lease:**
- Rent was $25,000/month for the first year, then $28,000/month after
- We had a one-time $50,000 lease incentive (landlord paid for buildout)
- There was a 6-month rent-free period at signing

ASC 842 requires you to:
- Include all payments (even variable escalations) in the liability calculation
- Amortize lease incentives into the ROU asset
- Spread rent-free periods over the full lease term for expense purposes

The system configuration for this one lease took 6 hours.

### The Vehicle Leases

Our two vehicle leases should have been simple—36-month terms, fixed monthly payments, clear buyout options at the end.

But they were finance leases, which meant different accounting:
- Depreciate the ROU asset separately from the lease liability
- Split payments into principal and interest
- Show the vehicle as an asset on the balance sheet

LeaseQuery had a finance lease module, but we had to configure depreciation methods (straight-line vs. declining balance) and ensure the interest amortization matched our payment schedule.

### The Embedded Leases

Our data center contract was $300,000/year for managed services, which included:
- Dedicated rack space (4 racks)
- Power and cooling
- Network connectivity
- 24/7 monitoring

Under ASC 842, we needed to separate the lease component (rack space) from the service components (power, network, monitoring).

**How do you allocate $300,000 across these components?**

We worked with the vendor to get a breakout:
- Rack space: $120,000/year (40%)
- Services: $180,000/year (60%)

Only the $120,000 rack space component is a lease. The rest is expensed as purchased services.

We created a lease in LeaseQuery for $10,000/month (the rack component) and continued expensing the rest.

**Our auditors spent half a day reviewing this allocation.** They wanted to see how we determined it was reasonable. We provided market data on rack rental rates in the same region, which satisfied them.

## Step 5: Configure Journal Entries

Every month, LeaseQuery needs to post journal entries to NetSuite:

**For Operating Leases:**

```
DR: Lease Expense                     $45,000
  CR: Lease Liability                          $43,287
  CR: ROU Asset Amortization                    $1,713
```

(The split between liability reduction and asset amortization depends on the amortization schedule.)

**For Finance Leases:**

```
DR: Interest Expense                  $340
DR: Lease Liability (principal)      $510
  CR: Cash                                     $850

DR: Depreciation Expense             $710
  CR: Accumulated Depreciation                 $710
```

We configured LeaseQuery to automatically create these journal entries in NetSuite at month-end. This required:
- Mapping LeaseQuery accounts to NetSuite GL accounts
- Setting up subsidiaries and departments for multi-entity leases
- Configuring approval workflows (our controller had to approve before posting)

**The integration worked...mostly.** We found a bug where multi-currency leases (we had one office in Canada) weren't converting to USD correctly. LeaseQuery fixed it in a week, but it delayed our first month-end close.

## Step 6: Month-End Process

Our new month-end lease accounting checklist:

1. **Review lease activity** — any new leases signed, renewals exercised, or terminations?
2. **Update payment schedules** — if rent escalated or variable payments changed
3. **Run LeaseQuery calculation** — system recalculates liability and ROU asset balances
4. **Review journal entries** — Controller approves entries before posting
5. **Post to NetSuite** — LeaseQuery pushes journal entries automatically
6. **Reconcile** — Compare LeaseQuery balances to NetSuite GL balances

This added about 4 hours to our month-end close initially. We've optimized it down to about 90 minutes.

### The First Close

Our first month-end close with the new system was chaos.

We discovered:
- 3 leases had the wrong start date
- 1 lease was classified as operating when it should have been finance
- The discount rate on 2 leases was wrong
- LeaseQuery calculated a different liability than our spreadsheet for 7 leases

**We spent 16 hours reconciling the differences.** Most were rounding errors or differences in how we calculated PV (Excel's PV function vs. LeaseQuery's calculation engine). But one was a real error—we'd entered the wrong payment amount for a lease.

We had to restate that lease, which changed our ROU asset by $47,000.

## Step 7: Audit Preparation

When our auditors showed up, they wanted:

1. **A complete lease listing** — every lease, with term, payment, and classification
2. **Calculations for initial balances** — showing how we arrived at the Day 1 ROU asset and liability for each lease
3. **Reconciliation** — proving that LeaseQuery balances tied to NetSuite
4. **Roll-forward** — showing how balances changed from opening to closing
5. **Samples** — they picked 10 leases to audit in detail

For the sampled leases, they wanted:
- Signed lease agreements
- Payment history (proof we paid what we said we paid)
- Discount rate support (documentation of how we determined IBR)
- Journal entries for the year

**We spent 40 hours preparing this package.**

The audit itself took 12 hours over 3 days. They found:
- One lease where we'd used the wrong discount rate (immaterial)
- One embedded lease where they disagreed with our allocation (we adjusted)

Both required journal entries to correct, but the amounts were small (under $20,000 combined).

## What We Learned

### 1. Start Early

We had three months. It should have been six.

**If you're implementing ASC 842, start a full year before your compliance date.** You need time to:
- Inventory leases (this takes longer than you think)
- Evaluate systems
- Migrate data
- Run parallel processes to test
- Train your team

### 2. Lease Data Is Always Worse Than You Think

Every company I've talked to has the same story: "We thought we had 20 leases. We found 40."

**Document everything now.** Even if you're not implementing ASC 842 yet, start building a centralized lease repository. Future you will thank you.

### 3. Embedded Leases Are Everywhere

We found embedded leases in:
- Data center contracts
- Managed print services
- Warehouse logistics agreements
- Equipment service contracts

**If a contract gives you exclusive use of an identified asset, it might be a lease.** Review your vendor contracts with this lens.

### 4. Discount Rates Matter

We did a sensitivity analysis on our IBR. A 1% increase in discount rate would have reduced our total lease liability by $180,000.

**Work with your auditors to document your IBR methodology before you calculate balances.** Don't back into a rate that gives you the balance you want.

### 5. Software Is Worth It

We looked at the $18,000/year LeaseQuery cost and almost balked. But the alternative was:
- Building and maintaining complex Excel models
- Manually posting 50+ journal entries per month
- No audit trail
- High risk of errors

**The software paid for itself in the first year** in reduced accounting time and audit costs.

### 6. Modifications Are Hard

Mid-lease modifications (renewals, terminations, rent changes) require remeasurement under ASC 842. The rules are complex, and every modification requires judgment.

**Build a process for lease modifications that involves accounting from the start.** Don't let operations or real estate sign amendments without finance review.

## The Aftermath

It's been six years since we implemented ASC 842. Here's what's changed:

**Our balance sheet:**
- ROU Assets: $5.2M
- Lease Liabilities: $5.4M

**Our process:**
- Month-end lease accounting: 90 minutes
- New lease onboarding: 30 minutes
- Audit prep: 8 hours (down from 40)

**Our team:**
- One person owns lease accounting (used to be split across 3 people)
- We've trained operations and real estate to flag potential leases before signing

**What I'd do differently:**

1. **Involve legal earlier** — they had copies of leases we didn't know existed
2. **Document the IBR methodology before calculating anything** — we wasted time recalculating when auditors questioned our rates
3. **Implement the software 6 months earlier** — parallel running would have caught our data issues
4. **Create a lease approval process before implementation** — we were still finding new leases months after go-live

## Final Thoughts

ASC 842 is one of those regulations that feels like busywork until you realize it's actually fixing a real problem. **Companies were hiding billions in lease obligations off-balance-sheet.** The new standard makes financials more transparent.

But transparency comes at a cost. Implementation is painful, ongoing compliance requires process discipline, and the accounting is genuinely complex.

If you're staring down an ASC 842 implementation, my advice:
- Start now, not later
- Budget more time than you think you need
- Invest in proper software
- Work closely with your auditors

And remember: **every company that's gone through this has a horror story.** You're not alone. The implementation is miserable, but once it's done, it becomes routine.

Just don't wait until two weeks before your audit to start.
