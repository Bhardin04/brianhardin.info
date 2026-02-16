---
title: "Cross-Functional Leadership: Working with Sales, Finance, and Engineering"
slug: "cross-functional-leadership-working-with-sales-finance-and-engineering"
excerpt: "Revenue operations sits at the intersection of three departments that often don't speak the same language. That's your superpower — if you know how to use it."
tags: ["Leadership", "Cross-Functional", "Revenue Operations", "Communication"]
published: true
featured: false
created_at: "2026-01-19"
published_at: "2026-01-19"
author: "Brian Hardin"
meta_description: "How to lead effectively across sales, finance, and engineering teams, with frameworks for translation, trust-building, and conflict resolution."
---

Revenue operations sits at the intersection of three departments that often don't speak the same language. That's your superpower — if you know how to use it.

I've spent the last decade in this intersection, watching teams talk past each other in meetings, build solutions that miss the mark, and waste weeks on projects that could have been aligned in a single conversation. The problem isn't that people are bad at their jobs. **The problem is that sales, finance, and engineering operate with different metrics, different timelines, and different definitions of success.**

Your job as a RevOps leader isn't to be the smartest person in finance, the best engineer, or the top salesperson. Your job is to be fluent in all three languages and translate effectively between them.

Here's how I've learned to do that at scale.

## The Three Languages

Let me be specific about what I mean by "different languages."

**Sales speaks in:** Pipeline, close rates, quota attainment, ARR, deal velocity, competitive intel. Their timeline is this quarter — sometimes this month. Their currency is closed deals.

**Finance speaks in:** Revenue recognition, deferred revenue, collections, cash flow, bookings vs. billings, GAAP compliance. Their timeline is annual planning with quarterly checkpoints. Their currency is accurate forecasts.

**Engineering speaks in:** Architecture, scalability, technical debt, sprint capacity, bug severity, uptime. Their timeline is sprints and roadmap quarters. Their currency is shipped features that don't break.

When sales says "we need this feature to close a $2M deal," finance hears "unbudgeted project," and engineering hears "scope creep with no specs."

When finance says "we need better revenue forecasting," sales hears "more admin work," and engineering hears "build a crystal ball."

When engineering says "we need to refactor the billing engine," sales hears "nothing new for six months," and finance hears "risk to revenue recognition."

**Your job is to translate each of these statements into the language the other teams actually care about.**

## Translation in Action

Here's a real example from last year. Sales came to me asking for a feature to support multi-currency invoicing for a major European expansion. The deal was worth $5M ARR over three years.

Sales framed it as: "We need multi-currency ASAP or we lose the deal."

I translated for finance: "We have a $5M ARR opportunity that requires multi-currency invoicing. This would diversify our revenue geographically and reduce concentration risk in North America. We'd need to ensure proper FX handling for revenue recognition and cash application."

I translated for engineering: "We have a validated use case for multi-currency with a named customer and signed LOI. Scope is EUR and GBP initially, with potential expansion to 5-7 currencies in the next 18 months. We need to handle: invoice generation, payment processing, FX rate management, and reporting. What's the right architecture to scale this?"

**Notice what I did:**

- For finance, I connected it to strategic goals (diversification, risk reduction) and called out compliance considerations
- For engineering, I provided scope, scale, and clear requirements instead of "just make it work"
- For both, I validated the opportunity was real (LOI signed, not just "sales thinks maybe")

The result: Finance allocated budget, engineering scoped it at 2 sprints, and sales closed the deal. Everyone felt heard and understood.

## Building Trust Across Functions

Translation only works if people trust you. And trust is earned differently in each department.

### How Sales Learns to Trust You

Sales trusts you when you:

1. **Show up to their team meetings and actually listen.** I attend our Monday sales huddles. I don't talk much, but I hear what deals are stuck and why.

2. **Move fast when it matters.** When a rep has a billing question blocking a close, I don't schedule a meeting for next week. I Slack them back in under 10 minutes.

3. **Say no with alternatives.** "We can't build that custom invoicing portal, but we can configure our existing system to do X, Y, and Z, which solves 90% of the problem."

4. **Celebrate their wins.** When a rep closes a complex deal that required billing creativity, I call it out publicly. "Sarah closed a $1.2M multi-year deal with custom payment terms — great work navigating complexity."

### How Finance Learns to Trust You

Finance trusts you when you:

1. **Speak their language fluently.** I know the difference between billings and revenue. I understand why they care about DSO. I read the monthly close deck.

2. **Bring problems before they become fires.** "We have a new contract structure that might affect rev rec timing — can we review it before we close the deal?"

3. **Document everything.** Finance lives and dies by audit trails. When I make a process change, I document the why, the what, and the controls.

4. **Respect their deadlines.** Month-end close is sacred. I don't deploy changes to billing systems on the 28th of the month.

### How Engineering Learns to Trust You

Engineering trusts you when you:

1. **Write clear requirements.** Not "make invoicing better." Instead: "Support split billing where Invoice A goes to Procurement (PO required) and Invoice B goes to AP (credit card). Need to maintain single contract record with two payment methods."

2. **Defend their time.** When sales asks for a one-off customization, I evaluate if it's worth interrupting the roadmap. Often it's not, and I tell sales that.

3. **Understand technical trade-offs.** I know the difference between a quick fix and a scalable solution. I know when it's worth incurring technical debt and when it's not.

4. **Give them context.** Engineers make better decisions when they understand the business impact. "This feature supports our expansion into EMEA, which is a $20M ARR opportunity over two years."

## Running Effective Cross-Functional Meetings

Most cross-functional meetings are a waste of time. People show up, give status updates, and leave without making decisions.

Here's how I run cross-functional meetings that actually work:

### Before the Meeting

**Define the decision to be made.** Not "discuss invoicing improvements." Instead: "Decide whether to build multi-entity invoicing in Q2 or Q3, and what scope to include."

**Send pre-reads 48 hours early.** Include: the problem statement, the options, the trade-offs, and your recommendation. If people can't be bothered to read it, they don't get to complain in the meeting.

**Invite only decision-makers and key stakeholders.** If someone doesn't need to be there to make or inform the decision, don't invite them. You can send notes afterward.

### During the Meeting

**Start with the decision.** "We're here to decide X. I'm recommending Y because of Z. What questions or concerns do you have?"

**Timebox discussion.** "We have 30 minutes. Let's spend 10 minutes on each option."

**Translate in real time.** When someone uses jargon the other departments don't understand, I paraphrase: "So what you're saying is we'd need to delay other projects by two weeks — is that right?"

**Drive to closure.** "It sounds like we're aligned on moving forward with Option B. Finance, can you confirm budget is available? Engineering, can you commit to Q2 delivery? Sales, does this timeline work for the customer pipeline?"

**Document decisions immediately.** I take notes in the meeting and send a summary within an hour: "Decisions made, action items, owners, deadlines."

### After the Meeting

**Follow up on action items.** I don't assume people will do what they said they'd do. I check in midway through the sprint: "Hey, just checking on that spec doc you were going to draft — need anything from me?"

**Close the loop.** When the project ships, I send an update to everyone involved: "Multi-currency invoicing is live. Thanks to [names] for making this happen. We've already closed $1.2M in new EMEA business using this feature."

## Navigating Conflicting Priorities

Here's the reality: Sales, finance, and engineering will always have conflicting priorities. Your job isn't to make everyone happy. Your job is to make the right trade-offs for the business.

### The Framework I Use

When priorities conflict, I evaluate based on:

1. **Revenue impact.** What's the dollar value and probability of success?
2. **Strategic alignment.** Does this support our annual goals or is it a one-off?
3. **Resource cost.** What does this require in terms of time, people, and budget?
4. **Risk.** What happens if we don't do this? What happens if we do it wrong?
5. **Scalability.** Does this solve the problem once, or set us up for future wins?

**Example:** Last quarter, sales wanted a feature to support usage-based billing for a $3M deal. Finance wanted a new collections dashboard to reduce DSO by 5 days (worth ~$800K in freed-up cash). Engineering wanted to refactor our payment processing architecture to reduce technical debt.

All three were important. All three couldn't happen simultaneously.

Here's how I evaluated it:

| Priority | Revenue Impact | Strategic | Resource Cost | Risk | Scalability |
|----------|---------------|-----------|---------------|------|-------------|
| Usage billing | $3M ARR | High (new model) | 3 sprints | High (rev rec complexity) | High (10+ prospects want this) |
| Collections dashboard | $800K cash | Medium | 1 sprint | Low | Medium (one-time benefit) |
| Refactor payments | $0 direct | Low | 4 sprints | Medium (tech debt compounds) | High (enables future features) |

**Decision:** We did usage-based billing first, collections dashboard second, and deferred the refactor to Q3 with a commitment to prioritize it then.

Sales got their feature. Finance got their dashboard (just delayed by 6 weeks). Engineering got a concrete commitment on the refactor with a date.

**The key is being explicit about the trade-offs and getting buy-in from all parties before you make the call.**

## When You're the Bad Guy

Sometimes you have to say no to people you like and respect. That's part of the job.

Last year, our VP of Sales wanted to pilot a new pricing model with zero contractual commitment — essentially a free trial for enterprise customers. He believed it would accelerate deal velocity.

Finance said absolutely not. No revenue recognition, no cash flow, too much risk.

Engineering said it would require significant changes to our provisioning and billing systems.

I said no.

Not because the idea was bad — it wasn't. But because:

1. We didn't have the systems to support it without significant engineering investment
2. Finance wouldn't recognize any revenue from it, which hurt our quarterly targets
3. We had no data suggesting this would actually increase close rates

The VP of Sales was frustrated. He thought I was blocking innovation.

**Here's what I did:** I didn't just say no. I said, "Here's what we'd need to make this work: A 60-day pilot with 3 named customers, clear success metrics (close rate and time-to-close), and a plan for how we'd roll it back if it doesn't work. If you can define that, I'll get finance and engineering on board."

He came back two weeks later with a tighter proposal. We ran the pilot with 3 customers, tracked the data, and learned that it didn't actually improve close rates — it just delayed decisions.

**By requiring rigor, I saved us from wasting months on a low-probability bet.**

The VP of Sales wasn't thrilled in the moment, but he respected the process. And when we killed the pilot based on data, there was no argument.

## The Skills That Matter Most

If you want to lead effectively across sales, finance, and engineering, here are the skills that matter:

### 1. Active Listening

Most people listen to respond. You need to listen to understand. When a salesperson says "we need this feature," dig deeper: "What customer problem does this solve? How many deals does this affect? What happens if we don't build it?"

### 2. Pattern Recognition

After you've sat in enough cross-functional meetings, you start to see patterns. "This is the third time engineering has pushed back on a finance request because the requirements were vague." Fix the pattern, not just the instance.

### 3. Emotional Intelligence

You need to read the room. When someone is frustrated, acknowledge it: "I know this is frustrating — you've been asking for this for six months. Here's why it hasn't happened, and here's what I'm doing to change that."

### 4. Decisiveness

Cross-functional teams get stuck in analysis paralysis. Someone needs to call the question: "We've debated this for two meetings. Here's what we're doing."

### 5. Follow-Through

Nothing destroys trust faster than commitments you don't keep. If you say you'll get back to someone by Friday, do it. If you commit to a delivery date, hit it or communicate early that you won't.

## What Good Looks Like

You know you're doing cross-functional leadership well when:

- **Sales stops going around you.** They come to you first when they have a billing question or need a deal structure reviewed.
- **Finance treats you as a partner, not a ticket-taker.** They involve you in planning, not just execution.
- **Engineering respects your roadmap input.** They ask your opinion on prioritization and trade-offs.
- **Meetings get shorter.** Because people trust the process and come prepared.
- **Decisions stick.** You're not re-litigating the same issues every quarter.

I'm not perfect at this. I still occasionally say yes when I should say no. I still sometimes under-communicate and assume people have context they don't have. I still get pulled into conflicts that I could have prevented with earlier intervention.

But I'm better at it than I was five years ago. And the teams I work with are more aligned, more productive, and less frustrated than any teams I worked with early in my career.

## The Bottom Line

**Cross-functional leadership is not about being liked by everyone.** It's about being trusted by the right people to make the right trade-offs for the business.

You will disappoint people. You will make calls that someone disagrees with. You will say no to projects that people are passionate about.

That's the job.

But if you translate effectively, build trust across functions, run meetings that drive decisions, and navigate conflicts with clear frameworks, you'll build something rare: a revenue operations function that sales, finance, and engineering all see as a strategic partner, not an obstacle.

And that's when you unlock real leverage.
