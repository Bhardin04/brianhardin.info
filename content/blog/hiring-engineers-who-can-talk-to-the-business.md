---
title: "Hiring Engineers Who Can Talk to the Business"
slug: "hiring-engineers-who-can-talk-to-the-business"
excerpt: "The most valuable engineer on a revenue team isn't the one who writes the best code. It's the one who understands why the code matters to the business."
tags: ["Hiring", "Leadership", "Engineering Management", "Career"]
published: true
featured: false
created_at: "2025-12-29"
published_at: "2025-12-29"
author: "Brian Hardin"
meta_description: "How to hire engineers who bridge technical and business domains, with interview questions and evaluation frameworks."
---

# Hiring Engineers Who Can Talk to the Business

The best engineer I ever hired couldn't write code as fast as the other candidates. His take-home project was solid but not exceptional. His algorithms knowledge was fine, not brilliant.

But when I asked him, "Why does invoice accuracy matter to a SaaS company?" he didn't just say "customer satisfaction" or "data quality."

He said: **"Because every billing error either delays cash collection or creates a dispute that costs 10x more to resolve than it would have cost to prevent. At scale, that's millions in working capital and operational overhead."**

I hired him on the spot.

Three years later, he's the tech lead for our entire order-to-cash platform. Not because he's the strongest coder on the team — he's not. But because he **bridges the gap between engineering and the business** in a way that makes everyone around him more effective.

Here's how to find and hire engineers like him.

## Why Business-Aware Engineers Matter More Than You Think

Most engineering teams optimize for technical excellence. They hire people who can solve hard algorithm problems, design elegant systems, and ship clean code.

That's important. But on a **revenue engineering team**, technical excellence is table stakes. The real differentiator is whether your engineers understand **why they're building what they're building**.

### The Cost of Business-Blind Engineers

I've worked with brilliant engineers who had no idea how the business made money. They'd build features exactly as spec'd, even when the spec was wrong. They'd optimize for technical purity instead of business impact. They'd argue for rewrites when a quick patch would unblock $2M in revenue.

**Example 1: The Billing Calculation "Improvement"**

An engineer on my team spent three weeks refactoring our proration logic to make it "mathematically pure." The new logic was elegant. It was also incompatible with how we'd been billing customers for five years.

We discovered this during QA. Rolling back cost us two weeks. The real cost: we missed a deadline that delayed a major contract renewal.

If he'd understood that **billing consistency matters more than mathematical perfection**, he would have asked before making that change.

**Example 2: The "Just a Minor Bug"**

Another engineer deprioritized a bug that caused invoice emails to occasionally go to the wrong contact. "It only affects 2% of invoices," he said.

That 2% represented **$4M in monthly billing**. The wrong contacts weren't paying invoices because they didn't have authorization. Our DSO spiked 8 days in one month.

If he'd understood the **business impact of invoice delivery**, he would have treated that bug as P0.

### The Leverage of Business-Aware Engineers

Now contrast that with engineers who **get the business**:

- They ask clarifying questions during planning: "If we build this feature, how does it affect revenue recognition?"
- They flag risks proactively: "This architectural change will delay month-end close by 12 hours. Is that acceptable?"
- They propose solutions aligned with business outcomes: "Instead of rebuilding this entire module, we can patch three specific edge cases and unblock the sales team by Friday."

These engineers **make everyone around them better** because they translate between technical and business domains fluently.

That's the kind of engineer I want on my team. And they're rare.

## The Interview Framework

Most engineering interviews test coding ability, system design, and culture fit. That's necessary but insufficient.

Here's the framework I use to evaluate **business acumen** during technical interviews:

### 1. The Business Context Question (First 15 minutes)

Before I ask any technical questions, I explain what we do and why it matters.

**Example:**
"We run a B2B SaaS company. We have 3,000 customers paying us monthly. Our billing team processes $80M in invoices every month. Billing errors cost us an average of $1,200 per incident to resolve."

Then I ask: **"Based on what I just told you, what do you think are the top three technical challenges in this domain?"**

#### What I'm Listening For

**Strong Answer:**
- Mentions data accuracy / validation
- Talks about scale (processing thousands of transactions)
- Identifies risk areas (errors, failures, money movement)
- Asks clarifying questions ("What's your average deal size?" "How complex are your pricing models?")

**Weak Answer:**
- Focuses only on technical challenges (performance, databases, APIs)
- Doesn't connect technical problems to business outcomes
- Generic answers that could apply to any domain

**Red Flag:**
- Can't think of any challenges
- Dismisses the problem as "easy"
- Doesn't ask any follow-up questions

### 2. The "Why Does This Matter?" Follow-Up

After the candidate answers a technical question, I ask: **"Why does this matter to the business?"**

**Example:**
*Candidate explains how they'd design a reconciliation system.*

**Me:** "Why does reconciliation matter? Why not just trust that the numbers are right?"

#### What I'm Listening For

**Strong Answer:**
- Connects technical accuracy to financial outcomes
- Understands that errors compound at scale
- Recognizes trust and compliance implications

**Weak Answer:**
- "Because it's good practice"
- "Because we want clean data"
- Can't articulate the business impact

### 3. The Trade-Off Question

I present a realistic scenario with conflicting priorities:

**Example:**
"The sales team wants a new billing feature shipped by end of quarter so they can close a $5M deal. The feature will take six weeks to build properly, but you could ship a 'good enough' version in three weeks. The CEO is asking your opinion. What do you recommend?"

#### What I'm Listening For

**Strong Answer:**
- Asks clarifying questions: "What happens if we ship the quick version and it breaks?" "Can we negotiate terms with the customer to buy more time?" "What's the risk if this deal falls through?"
- Considers multiple options: ship quick version, negotiate timeline, offer manual workaround
- Frames recommendation in terms of **risk vs. reward**
- Acknowledges that this is ultimately a business decision, not just a technical one

**Weak Answer:**
- Absolutist: "Never ship bad code" or "Always do what sales wants"
- Doesn't ask questions
- Can't articulate the trade-offs

**Red Flag:**
- Blames sales for "always rushing us"
- Can't separate technical preference from business necessity

### 4. The Failure Post-Mortem Question

I describe a real failure scenario and ask them to diagnose it:

**Example:**
"Last month, our billing system double-charged 300 customers. We discovered it when customers started calling support. The bug was in a recent code change. How would you approach this situation?"

#### What I'm Listening For

**Strong Answer:**
- Mentions **customer impact first**: "Immediately stop charging additional customers, then reverse the incorrect charges"
- Talks about communication: "Alert finance, support, and leadership"
- Considers downstream effects: "Will refunds affect revenue recognition? Do we need to notify customers proactively?"
- Only then talks about technical remediation: "Root cause analysis, fix, add tests to prevent recurrence"

**Weak Answer:**
- Jumps straight to fixing the code
- Doesn't mention customer impact or communication
- Treats it as purely a technical problem

**Red Flag:**
- Blames QA or lack of testing
- Doesn't seem to understand the severity

### 5. The "Explain This to a Non-Technical Stakeholder" Question

I ask them to explain a technical concept to me as if I'm a finance executive who doesn't code.

**Example:**
"Explain to me why our API integration with Salesforce sometimes drops data, and what we should do about it."

#### What I'm Listening For

**Strong Answer:**
- Uses analogies: "Think of it like a phone call that drops mid-conversation. Some data doesn't make it through."
- Focuses on business impact: "This means sales data doesn't sync, so billing might use outdated pricing."
- Proposes solutions in business terms: "We can add a retry mechanism. This will cost us two weeks of dev time but will prevent 95% of data loss."
- Avoids jargon or explains it when necessary

**Weak Answer:**
- Uses heavy technical jargon without explanation
- Doesn't connect to business outcomes
- Can't simplify the explanation

**Red Flag:**
- Gets frustrated or condescending when asked to simplify
- Says "it's too technical to explain"

## Behavioral Interview Questions That Reveal Business Awareness

In addition to technical questions, I ask behavioral questions designed to surface whether someone has worked **cross-functionally** before:

### Question 1: "Tell me about a time you disagreed with a product or business decision."

**What I'm Listening For:**
- Did they engage with the decision or just complain about it?
- Did they try to understand the business rationale?
- Could they articulate both sides of the argument?

**Strong Answer:**
"Sales wanted us to build a feature that I thought was technically risky. I scheduled time with the VP of Sales to understand why it mattered. Turned out it was critical for a competitive deal worth $10M. I proposed an alternative approach that reduced technical risk while still meeting the business need. We shipped it and won the deal."

**Weak Answer:**
"Product asked us to build something dumb. We told them it was a bad idea but they made us do it anyway."

### Question 2: "Describe a project where you had to work closely with non-engineering teams."

**What I'm Listening For:**
- Have they worked cross-functionally before?
- How do they describe non-engineers? (Respectfully? Dismissively?)
- Can they speak to business outcomes, not just technical outputs?

**Strong Answer:**
"I worked with the finance team to automate our revenue recognition process. I spent the first two weeks just learning how rev rec works and why it's important. Then I collaborated with their team to design a solution that matched their workflow. We reduced close time by three days."

**Weak Answer:**
"I had to work with marketing once to build a landing page. They kept changing the requirements. It was annoying."

### Question 3: "Tell me about a time you had to make a decision with incomplete information."

**What I'm Listening For:**
- How do they handle ambiguity?
- Do they seek out information or make assumptions?
- Do they consider business risk?

**Strong Answer:**
"We were deciding between two API vendors. We didn't have time for a full proof of concept. I ran a one-day spike on each, talked to their sales and support teams, and read user reviews. I recommended Vendor A because they had stronger SLAs and better support, even though Vendor B was cheaper. The business risk of downtime outweighed the cost savings."

**Weak Answer:**
"I just picked the one that looked better and hoped it would work out."

## Red Flags in Resumes and Interviews

Not all red flags are dealbreakers, but they're worth probing:

### Resume Red Flags

**1. No mention of business impact**
- All bullets are technical: "Built X using Y technology"
- None mention outcomes: "Reduced processing time by 40%, enabling $2M in cost savings"

**2. Only worked on internal tools or back-office systems**
- Limited exposure to customer-facing systems or revenue impact
- May not understand how technical decisions affect the business

**3. Short tenures at multiple companies (< 1 year each)**
- May not have stuck around long enough to see the consequences of their technical decisions

### Interview Red Flags

**1. Can't explain what their current company does**
- "We're a SaaS company" isn't enough
- They should know their company's business model, revenue, and market

**2. Dismissive of non-technical stakeholders**
- "Sales always asks for impossible things"
- "Finance doesn't understand how engineering works"

**3. Overconfidence without curiosity**
- Makes sweeping statements without asking questions
- Assumes they understand your business after five minutes

**4. Can't talk about trade-offs**
- Every technical decision is black and white
- Doesn't acknowledge that "it depends" is often the right answer

## How to Develop Business Acumen in Engineers You Already Have

Not everyone you hire will have strong business acumen. That's okay. **You can develop it.**

Here's how:

### 1. Embed Engineers in Business Meetings

Invite engineers to:
- Sales pipeline reviews
- Customer success check-ins
- Finance month-end close meetings
- Executive business reviews

They don't need to speak. They just need to **listen and observe**.

### 2. Share Business Context in Every Project Kickoff

Don't just explain **what** to build. Explain **why it matters**.

**Bad kickoff:** "We're building a new proration engine. Here are the requirements."

**Good kickoff:** "We're building a new proration engine because our current system can't handle mid-month plan changes accurately. This causes billing errors, which delay cash collection and create disputes. Last quarter, we had 47 billing disputes related to proration, costing us $56K in operational overhead and $230K in delayed payments. Fixing this will reduce disputes by ~80%."

### 3. Rotate Engineers Through Cross-Functional Projects

Assign engineers to projects that require them to work closely with sales, marketing, finance, or customer success.

**Example:**
- Pair an engineer with a finance analyst to build a revenue reporting dashboard
- Have an engineer shadow customer support for a day to see how users interact with the product
- Ask an engineer to present a technical roadmap to the sales team

### 4. Create a Business 101 Onboarding Module

We built a 2-hour onboarding session for all new engineers that covers:
- How the company makes money
- Revenue model and pricing structure
- Key metrics (ARR, MRR, DSO, churn, etc.)
- The customer journey from lead to payment
- How engineering work impacts revenue

### 5. Celebrate Business Outcomes, Not Just Technical Outputs

In team meetings and performance reviews, highlight **business impact**:

**Bad:** "Sarah shipped the new invoicing system."

**Good:** "Sarah shipped the new invoicing system, which reduced invoice generation time from 6 hours to 45 minutes. This means we can close our books faster and sales can send invoices the same day deals close."

## The Bottom Line

Technical excellence is necessary. But on a revenue engineering team, **business acumen is the multiplier**.

An engineer who understands the business will:
- Ask better questions during planning
- Make better trade-off decisions during execution
- Spot risks earlier
- Prioritize work more effectively
- Communicate more clearly with stakeholders

Here's how to hire for it:

1. **Ask business context questions** — not just technical ones
2. **Evaluate how they think about trade-offs** — every decision has business implications
3. **Test their ability to communicate with non-technical stakeholders** — this is a core skill, not a nice-to-have
4. **Look for cross-functional experience** — have they worked outside engineering?
5. **Watch for red flags** — dismissiveness, overconfidence, lack of curiosity

And if you're not finding candidates with strong business acumen, **develop it in the engineers you already have**. Embed them in business conversations, share context, and celebrate business outcomes.

The engineers who bridge the technical and business worlds are the ones who become indispensable.

Hire them. Develop them. Promote them.

Your revenue engine depends on it.
