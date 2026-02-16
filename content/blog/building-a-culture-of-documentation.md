---
title: "Building a Culture of Documentation"
slug: "building-a-culture-of-documentation"
excerpt: "The best teams I've led had one thing in common: they wrote things down. Here's how to build a documentation culture that sticks."
tags: ["Leadership", "Documentation", "Process", "Team Management"]
published: true
featured: false
created_at: "2026-01-12"
published_at: "2026-01-12"
author: "Brian Hardin"
meta_description: "How to build a documentation culture in technical teams, with templates, review processes, and strategies for overcoming resistance."
---

# Building a Culture of Documentation

Six months into a new role, I inherited a system that processed $50M in monthly billing. It was complex, fragile, and completely undocumented.

When I asked the engineer who built it to explain how it worked, he said: **"It's all in my head."**

Two weeks later, he gave notice.

We spent the next three months reverse-engineering his system, breaking things in production, and scrambling to keep the business running. The cost: hundreds of engineering hours, multiple billing errors, and a near-miss on a major customer payment delay.

All because one person didn't write anything down.

That experience taught me: **Documentation isn't a nice-to-have. It's infrastructure.** Without it, your team's knowledge is trapped in people's heads, and every departure or transition becomes a crisis.

Here's how to build a culture where documentation actually happens — and sticks.

## Why Documentation Doesn't Happen

Before you can fix the documentation problem, you need to understand why it exists.

### The Real Reasons People Don't Document

**1. "I don't have time"**

This is the #1 excuse. It's also true — if you treat documentation as a separate task that happens after the "real work" is done.

**The fix:** Make documentation **part of the work**, not something you do after.

**2. "I'll document it later"**

Later never comes. By the time "later" arrives, you've moved on to the next project and forgotten the details.

**The fix:** Document as you build, not after you ship.

**3. "Nobody reads documentation anyway"**

If documentation sits in a wiki that nobody uses, this is true. People stop writing docs when they see their previous docs gathering dust.

**The fix:** Make documentation **discoverable and useful**, not a graveyard of outdated information.

**4. "I don't know what to document"**

People freeze because they don't know where to start or what level of detail is appropriate.

**The fix:** Provide **templates and examples** so people know what "good" looks like.

**5. "Documentation will be outdated as soon as we change the system"**

This is a self-fulfilling prophecy. If you assume docs will get stale, you won't maintain them, and they will get stale.

**The fix:** Build a **review and update process** so docs stay current.

**6. "Writing docs is boring / not rewarded"**

If your team gets recognized for shipping features but not for writing docs, they'll optimize for what's rewarded.

**The fix:** **Celebrate and reward** documentation work the same way you celebrate shipping code.

## The Documentation Culture Framework

Building a culture of documentation requires **systems, templates, accountability, and incentives**. You can't just ask people to "write more docs" and expect it to happen.

Here's the framework that worked for me.

## Step 1: Define What Needs to Be Documented

Not everything needs documentation. But some things absolutely do.

Here's the minimum set of documentation every technical team should maintain:

### 1. System Architecture Docs

**What it is:** High-level overview of how the system works, what the major components are, and how they interact.

**Who owns it:** The tech lead or architect.

**When to update it:** Every time a major architectural change is made.

**Example structure:**
- **System overview** (one-paragraph summary)
- **Architecture diagram** (visual representation)
- **Key components** (what they do, how they interact)
- **Data flow** (how data moves through the system)
- **External dependencies** (APIs, services, databases)
- **Known limitations** (what the system can't do)

### 2. Runbooks / Operational Docs

**What it is:** Step-by-step instructions for operating the system — deployments, monitoring, incident response, disaster recovery.

**Who owns it:** The team responsible for operating the system.

**When to update it:** After every incident or operational change.

**Example structure:**
- **How to deploy** (steps, commands, rollback process)
- **How to monitor** (dashboards, alerts, key metrics)
- **Common issues and fixes** (error messages and how to resolve them)
- **Incident response** (who to contact, escalation process)
- **Disaster recovery** (how to restore from failure)

### 3. Code-Level Documentation

**What it is:** Comments, README files, and inline explanations that help someone understand **why** the code does what it does.

**Who owns it:** The engineer who wrote the code.

**When to update it:** During code review, before merging.

**What to document:**
- **Non-obvious logic** (why this algorithm, why this approach)
- **Edge cases** (what happens when X fails)
- **Assumptions** (what must be true for this to work)
- **TODOs and known issues** (what still needs to be fixed)

### 4. Process Documentation

**What it is:** How the team operates — onboarding, code review process, deployment pipeline, how decisions are made.

**Who owns it:** The team lead or manager.

**When to update it:** When processes change.

**Example structure:**
- **Onboarding checklist** (what new team members need to do in their first week)
- **Code review guidelines** (what reviewers should look for)
- **Deployment process** (how code goes from dev to production)
- **Decision-making framework** (how we prioritize, how we decide what to build)

### 5. Decision Records (ADRs)

**What it is:** A record of **why** a significant decision was made — technology choice, architectural pattern, process change.

**Who owns it:** The person who made the decision.

**When to create it:** Before implementing the decision.

**Example structure:**
- **Context:** What problem are we solving?
- **Decision:** What did we decide to do?
- **Rationale:** Why did we choose this approach?
- **Alternatives considered:** What else did we evaluate?
- **Consequences:** What trade-offs are we accepting?

ADRs are one of the most valuable types of documentation because they preserve **context**. Six months later, when someone asks "Why did we build it this way?", the ADR has the answer.

## Step 2: Provide Templates

Templates eliminate the "I don't know what to document" problem. They give people a structure to fill in, which reduces the cognitive load of starting from scratch.

Here's a simple runbook template we use:

```markdown
# [System Name] Runbook

## Overview
[One-paragraph description of what this system does]

## Key Metrics
- [Metric 1]: [What it measures, where to find it, what's normal]
- [Metric 2]: [What it measures, where to find it, what's normal]

## Deployment
1. [Step 1]
2. [Step 2]
3. [How to verify deployment succeeded]
4. [How to rollback if something goes wrong]

## Common Issues

### Issue 1: [Error message or symptom]
**Cause:** [Why this happens]
**Fix:** [Step-by-step resolution]

### Issue 2: [Error message or symptom]
**Cause:** [Why this happens]
**Fix:** [Step-by-step resolution]

## Escalation
- **First responder:** [Name, Slack handle]
- **Escalate to:** [Name, Slack handle]
- **Emergency contact:** [Name, phone number]

## Related Documentation
- [Link to architecture doc]
- [Link to code repository]
```

Here's an ADR template:

```markdown
# ADR [Number]: [Title]

**Date:** [YYYY-MM-DD]
**Status:** [Proposed | Accepted | Deprecated | Superseded]
**Deciders:** [List of people involved in the decision]

## Context
[What problem are we solving? What constraints do we have?]

## Decision
[What did we decide to do?]

## Rationale
[Why is this the right choice?]

## Alternatives Considered
1. **[Alternative 1]:** [Why we didn't choose this]
2. **[Alternative 2]:** [Why we didn't choose this]

## Consequences
**Positive:**
- [What we gain from this decision]

**Negative:**
- [What trade-offs we're accepting]

**Neutral:**
- [Other impacts]

## Follow-Up Actions
- [ ] [Action 1]
- [ ] [Action 2]
```

We store these templates in the team wiki so they're easy to find and copy.

## Step 3: Make Documentation Part of the Workflow

The only way documentation happens consistently is if it's **embedded in the workflow**, not treated as an afterthought.

### Documentation as Part of Code Review

We added a checklist item to every pull request template:

```markdown
## Documentation Checklist
- [ ] README updated (if this changes how to use the code)
- [ ] Architecture doc updated (if this changes system design)
- [ ] Runbook updated (if this changes deployment or operations)
- [ ] ADR created (if this is a significant decision)
- [ ] Inline comments added (for non-obvious logic)
```

**The rule:** Code doesn't get merged unless the documentation checklist is complete.

This was controversial at first. Engineers complained it slowed them down.

But here's what happened: after two months, documentation coverage went from ~30% to ~85%. And the "slow down" was negligible — maybe 15 minutes per PR.

### Documentation as Part of Project Kickoff

We don't start building until we've documented the **decision** to build.

Every project begins with an ADR that answers:
- What problem are we solving?
- Why is this the right solution?
- What alternatives did we consider?
- What are we **not** doing?

This forces clarity before we write any code. It also creates a record of **intent** that helps future engineers understand why the system exists.

### Documentation as Part of Incident Response

After every incident, we update the runbook with:
- What went wrong
- How we diagnosed it
- How we fixed it
- How to prevent it from happening again

This turns incidents into learning opportunities and ensures we don't encounter the same problem twice.

## Step 4: Make Documentation Discoverable

If people can't find documentation, it doesn't exist.

Here's how we made docs easy to find:

### 1. Single Source of Truth

We use **Notion** as our documentation hub. Everything lives in Notion. No scattered Google Docs, no outdated wikis, no tribal knowledge in Slack threads.

**The rule:** If it's not in Notion, it doesn't exist.

### 2. Clear Information Architecture

We organized our Notion workspace like this:

```
📁 Engineering
  📁 Systems
    📄 Billing System
      - Architecture Doc
      - Runbook
      - ADRs
    📄 Payment Processing
      - Architecture Doc
      - Runbook
      - ADRs
  📁 Processes
    📄 Code Review Guidelines
    📄 Deployment Process
    📄 Onboarding Checklist
  📁 Templates
    📄 Runbook Template
    📄 ADR Template
    📄 Architecture Doc Template
```

**The structure is consistent.** Every system has the same documentation structure. You always know where to find what you need.

### 3. Searchable and Linked

We use **tags** and **backlinks** aggressively. If a runbook mentions a specific API, we link to the API's architecture doc. If an ADR references a previous decision, we link to the original ADR.

This creates a **web of knowledge** instead of isolated documents.

### 4. Inline Documentation Links in Code

We added links to relevant docs directly in the code:

```python
# Payment processing workflow
# See: https://notion.so/payment-processing-architecture
def process_payment(invoice_id):
    ...
```

Now, when someone is reading code and has questions, the doc is right there.

## Step 5: Build a Review and Update Process

Documentation rots. Systems change. Processes evolve. If you don't maintain docs, they become worse than useless — they become **misleading**.

Here's how we keep docs fresh:

### 1. Quarterly Documentation Review

Every quarter, we dedicate one sprint to **documentation debt**.

Each team reviews:
- Which docs are outdated?
- Which systems are undocumented?
- Which docs can be archived?

We treat this like any other sprint — backlog, assignments, retro.

### 2. Ownership and Accountability

Every doc has an **owner** listed at the top:

```markdown
**Owner:** Sarah Chen
**Last Updated:** 2026-01-10
**Next Review:** 2026-04-10
```

The owner is responsible for keeping the doc up to date. If something changes in their system, they update the doc.

### 3. Stale Doc Alerts

We use a Notion automation that flags docs that haven't been updated in 6 months. The owner gets a Slack reminder to review and update or mark as still accurate.

### 4. Sunsetting Outdated Docs

We don't delete outdated docs — we **archive** them. We move them to an "Archive" folder and add a banner:

```
⚠️ This document is archived and may be outdated.
Last updated: 2024-05-15
Replaced by: [Link to new doc]
```

This preserves history while preventing people from following stale guidance.

## Step 6: Incentivize and Celebrate Documentation

If you want people to write docs, you need to **reward** it the same way you reward shipping code.

### 1. Recognition in Team Meetings

Every week, we highlight one piece of documentation that was particularly valuable:

- "Shout-out to Alex for updating the billing runbook after last week's incident. It's already helped two people debug issues faster."
- "Sarah created an amazing ADR for our database migration decision. It's a great example of how to document complex trade-offs."

### 2. Documentation as Part of Performance Reviews

We added a "Documentation" section to our engineering career ladder:

| Level | Documentation Expectation |
|-------|---------------------------|
| **Junior Engineer** | Documents their own code clearly |
| **Mid-Level Engineer** | Maintains runbooks for systems they own |
| **Senior Engineer** | Creates ADRs for significant decisions |
| **Staff Engineer** | Sets documentation standards and mentors others |

Now, documentation **impacts career progression**. It's not just "nice to have" — it's required.

### 3. Documentation Bounties

We started offering **documentation bounties** for high-impact docs:

- $100 gift card for creating a runbook for a critical system
- $50 gift card for updating an outdated architecture doc
- Team lunch for completing a documentation sprint on time

This sounds gimmicky, but it works. People respond to incentives.

## Overcoming Resistance: The Pushback You'll Get

When you start enforcing documentation standards, you'll get resistance. Here's what I've heard and how I've responded:

### Pushback #1: "This slows us down"

**Response:**
"It slows us down **now**, but it speeds us up **later**. Every hour we spend documenting saves 10 hours of reverse-engineering or incident response down the road."

Then I'd show them the data: we reduced incident resolution time by 40% after improving our runbooks.

### Pushback #2: "I'm not a good writer"

**Response:**
"You don't need to be Shakespeare. You just need to be clear. Use our templates — they'll guide you. And if you're stuck, ask for help. I'll review any doc before you publish it."

### Pushback #3: "The code is self-documenting"

**Response:**
"Code tells you **what** the system does. Documentation tells you **why** it does it. Both are necessary."

I'd also point to situations where "self-documenting code" failed us — edge cases, business logic, integration quirks.

### Pushback #4: "Nobody will read it anyway"

**Response:**
"If docs aren't useful, that's a symptom of bad docs, not a reason to stop writing them. Let's make better docs."

Then I'd show them examples of docs that **were** useful — runbooks that resolved incidents, ADRs that answered stakeholder questions, architecture docs that helped new engineers onboard faster.

## Measuring Success: How to Know If It's Working

You can't manage what you don't measure. Here's how we track documentation culture:

### Metric 1: Documentation Coverage

**What it is:** % of systems with complete documentation (architecture doc, runbook, ADRs).

**Target:** 90%+

**How we track it:** Quarterly audit. We list all major systems and check if they have the required docs.

### Metric 2: Time to Onboard

**What it is:** How long it takes a new engineer to make their first meaningful contribution.

**Target:** <2 weeks

**How we track it:** Survey new hires after their first month.

**Why it matters:** Good documentation accelerates onboarding.

### Metric 3: Incident Resolution Time

**What it is:** Average time to resolve production incidents.

**Target:** 20% reduction year-over-year

**How we track it:** Incident tracking system.

**Why it matters:** Good runbooks reduce troubleshooting time.

### Metric 4: Documentation Freshness

**What it is:** % of docs updated in the last 6 months.

**Target:** 80%+

**How we track it:** Notion metadata (last updated timestamp).

**Why it matters:** Stale docs are worse than no docs.

### Metric 5: Documentation Usage

**What it is:** How often docs are accessed.

**Target:** Trending upward

**How we track it:** Notion analytics (page views).

**Why it matters:** If docs aren't being read, they're not useful.

## The Bottom Line

The best teams I've led had one thing in common: **they wrote things down.**

Not because they loved documentation. Because they understood that documentation is **infrastructure** — it enables teams to scale, onboard faster, recover from incidents quicker, and make better decisions.

Here's how to build a documentation culture that sticks:

1. **Understand why people don't document** — and address the root causes
2. **Define what needs to be documented** — architecture, runbooks, code, processes, decisions
3. **Provide templates** — eliminate the "I don't know what to write" problem
4. **Make documentation part of the workflow** — embed it in code review, project kickoff, and incident response
5. **Make documentation discoverable** — single source of truth, clear structure, searchable
6. **Build a review and update process** — docs rot without maintenance
7. **Incentivize and celebrate** — reward documentation work like you reward shipping code
8. **Measure success** — coverage, freshness, usage, onboarding time, incident resolution time

You'll get pushback. People will complain that it slows them down. They'll say nobody reads docs anyway.

Push through it. Enforce the standards. Lead by example. Celebrate the wins.

Within six months, you'll have a team that writes things down by default — not because they have to, but because they've seen the value.

And when someone leaves, their knowledge won't leave with them.

That's the real ROI of documentation culture.
