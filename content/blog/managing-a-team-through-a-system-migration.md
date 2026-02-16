---
title: "Managing a Team Through a System Migration"
slug: "managing-a-team-through-a-system-migration"
excerpt: "System migrations fail more often because of people problems than technology problems. Here's how to lead your team through one without losing momentum or trust."
tags: ["Leadership", "Change Management", "System Migration", "Team Management"]
published: true
featured: false
created_at: "2025-12-22"
published_at: "2025-12-22"
author: "Brian Hardin"
meta_description: "How to lead a technical team through a system migration, including communication cadence, managing resistance, and protecting team morale."
---

# Managing a Team Through a System Migration

We were six months into a NetSuite migration when my best engineer quit.

Not because of the workload. Not because of the technology. She quit because she was exhausted from the **constant uncertainty, shifting priorities, and lack of visible progress**.

That was the moment I realized: **System migrations don't fail because of bad technology decisions. They fail because leaders don't manage the human side of massive change.**

We were halfway through migrating our entire order-to-cash system from a legacy ERP to NetSuite. The technical plan was solid. The budget was approved. The vendor was engaged.

But I hadn't prepared my team for the **emotional toll** of six months (that turned into twelve months) of building, testing, breaking, and rebuilding critical systems while the business depended on them not to fail.

Here's what I learned about leading a team through a system migration without losing people, momentum, or trust.

## The Emotional Arc of a Migration

Before you plan the technical work, understand the emotional journey your team will go through.

### Phase 1: Optimism (Weeks 1-4)

**What it feels like:** Excitement. New technology. A chance to fix all the old problems. Everyone is energized.

**What actually happens:** Kickoff meetings. Requirements gathering. Lots of talking, very little building.

**The danger:** People underestimate how hard this will be.

### Phase 2: Reality (Weeks 5-12)

**What it feels like:** Oh. This is harder than we thought. The old system is messier than we realized. The new system doesn't do what we expected out of the box.

**What actually happens:** The real work begins. Data migration issues surface. Integration assumptions break. The scope creeps.

**The danger:** This is where morale starts to crack. Teams start to question whether this was the right decision.

### Phase 3: The Grind (Months 4-8)

**What it feels like:** Will this ever end? We're fixing the same issues repeatedly. Every time we solve one problem, three more appear.

**What actually happens:** Testing cycles. Bug fixes. Edge case discovery. Workarounds for things that "should just work."

**The danger:** Burnout. People start looking for other jobs. Quality suffers because everyone is tired.

### Phase 4: The Final Push (Weeks before go-live)

**What it feels like:** Panic. Adrenaline. Sleep deprivation. "We're not ready, but we have to launch anyway."

**What actually happens:** Cutover planning. User training. Last-minute critical bugs. Weekend war rooms.

**The danger:** Pushing too hard here breaks people. Some of them won't recover even after launch.

### Phase 5: Post-Launch Hangover (Weeks after go-live)

**What it feels like:** Relief. Exhaustion. "Is it really over?"

**What actually happens:** Hypercare. Bug fixes. User support. Retrospectives.

**The danger:** Leaders move on to the next thing too quickly. The team needs time to recover and reflect.

I've led three major system migrations. The emotional arc is consistent every time. If you don't **actively manage** this journey, you'll lose your best people somewhere between Phase 3 and Phase 4.

## Communication Cadence: Over-Communicate Progress and Setbacks

The number one complaint I heard from my team during migrations: **"I don't know what's happening."**

Not because I wasn't talking to them. I was. But I was communicating **sporadically and reactively** instead of predictably and proactively.

Here's the communication cadence that worked:

### Daily Standups (15 minutes, every single day)

**Format:**
- What shipped yesterday
- What's shipping today
- What's blocked

**Why it matters:** In a migration, things change fast. A daily sync keeps everyone aligned and surfaces blockers before they cascade.

**The key:** Keep it short. No problem-solving in standup. Note blockers and solve them offline.

### Weekly All-Hands (30 minutes, every Friday)

**Format:**
- **Progress update:** What shipped this week
- **What's next:** Priorities for next week
- **Wins:** Celebrate something (even small progress)
- **Risks:** What might go wrong
- **Q&A:** Open floor for any questions

**Why it matters:** This is where you create **shared context**. Everyone sees the full picture, not just their slice.

**The key:** Be honest about setbacks. If you only share good news, people stop trusting you.

### Bi-Weekly Leadership Check-In (1 hour, every other Monday)

**Format:**
- Deep dive on a specific problem area
- Decision-making on scope changes
- Resource allocation discussions

**Attendees:** You, your tech leads, project manager, key stakeholders

**Why it matters:** This is where you course-correct before small issues become big problems.

**The key:** Come with data. Don't litigate the same issues every meeting.

### Monthly Executive Update (30 minutes)

**Format:**
- High-level progress against milestones
- Budget status
- Risk assessment
- Go/no-go recommendation if launch is approaching

**Attendees:** You, CFO/CRO, exec sponsor

**Why it matters:** Keeps leadership informed and ensures you have top-cover when things go wrong.

**The key:** No surprises. If there's a major issue, your exec sponsor should already know about it before this meeting.

### Ad-Hoc "State of the Migration" Messages (Slack/Email, as needed)

When something **significant** happens — good or bad — send an update immediately. Don't wait for the next scheduled meeting.

Examples:
- "We just completed the data migration dry run. 47 validation errors. Team is triaging. Update tomorrow."
- "Integration with Salesforce is live in test environment. Zero errors in the first 24 hours. Huge win."
- "Go-live is delayed by two weeks. Here's why and what we're doing about it."

**Why it matters:** Uncertainty kills morale. Even bad news delivered quickly is better than silence.

## Managing Resistance: The People Who Don't Want This to Happen

Every migration has resisters. People who liked the old system, fear change, or just don't trust that the new system will be better.

Ignoring them doesn't make them go away. It makes them sabotage the project — sometimes intentionally, often unintentionally.

Here's how I've learned to manage resistance:

### 1. Identify the Resisters Early

In the first two weeks, you'll hear comments like:
- "The old system worked fine. Why are we changing it?"
- "This is going to break everything."
- "We tried this before and it didn't work."

These are your resisters. **Don't dismiss them.** Understand them.

### 2. Understand the Root Cause

Resistance usually comes from one of three places:

**Fear of Irrelevance**
"If we move to the new system, my expertise in the old system won't matter anymore."

**Legitimate Concern**
"I've seen migrations fail before. I don't trust that this will be different."

**Loss of Control**
"I had the old system set up exactly how I wanted. Now I have to relearn everything."

### 3. Engage Resisters as Contributors

The worst thing you can do: sideline resisters and build around them.

The better approach: **give them a role in the migration**.

One of my biggest resisters during a NetSuite migration was a senior analyst who had built the entire reporting infrastructure in the old system. She saw NetSuite as a threat to her work.

I made her the **lead for reporting migration**. Her job: ensure that every report we had in the old system either existed in NetSuite or had a documented alternative.

She went from sabotaging the project to becoming its fiercest advocate. Why? Because she had **ownership and influence** over the outcome.

### 4. Create Space for Dissent

I started holding monthly "open floor" sessions where anyone could voice concerns, complaints, or doubts about the migration.

No rebuttal. No defensiveness. Just listening.

Half the resistance melted away once people felt **heard**.

### 5. Know When to Override

Sometimes resistance is about ego, not substance. If someone is blocking progress for reasons that don't hold up under scrutiny, you have to override them.

But do it **publicly and with explanation**. Don't just move forward and hope they fall in line.

Example:
"I hear your concern that NetSuite's invoicing workflow is different from our current system. We've evaluated three alternatives and NetSuite is still the best fit for reasons X, Y, Z. We're moving forward. I need your support on this."

## Celebrating Small Wins: The Only Way to Sustain Momentum

Migrations are long. The finish line is months away. If you wait until go-live to celebrate, your team will burn out long before you get there.

**You need small, frequent wins to sustain energy.**

Here's what I celebrated during our last migration:

- **Week 4:** Data mapping completed for the first module
- **Week 8:** First successful integration test between NetSuite and Salesforce
- **Week 12:** First invoice processed in NetSuite test environment
- **Week 16:** 1,000 transactions migrated with zero errors
- **Week 20:** First user training session completed
- **Week 24:** First module deployed to production

Every single one of these milestones got:
- A Slack announcement with a shout-out to the people who made it happen
- A 10-minute discussion in the weekly all-hands
- Lunch or coffee for the team (small budget, big impact)

Did these wins matter in the grand scheme? Not really. The project wasn't done.

But they created **proof of progress**. They reminded the team that we were moving forward, not spinning in place.

## Handling Setbacks: When Things Go Wrong (And They Will)

Migrations don't go according to plan. Ever.

Data migrations fail. Integrations break. Go-live dates slip. Key people leave. Vendors miss deadlines.

How you handle setbacks determines whether your team trusts you.

### What Not to Do

**Don't hide bad news.** Your team already knows things are broken. Pretending otherwise destroys credibility.

**Don't blame people.** Migrations are complex. Most failures are system failures, not individual failures.

**Don't panic.** Your team takes emotional cues from you. If you panic, they panic.

### What to Do Instead

**1. Acknowledge the setback quickly**

"We just discovered that our customer payment history didn't migrate correctly. We have 10,000 records with missing data. This is a problem."

**2. Explain the impact**

"This affects our ability to track AR aging accurately. It also means we can't go live on the original date."

**3. Share the plan to fix it**

"We're running a reconciliation script tonight to identify the gaps. The team will spend the next three days manually verifying the top 500 accounts. We'll re-run the migration on Friday."

**4. Adjust expectations**

"This pushes go-live by two weeks. I've already communicated this to the exec team. Our new target is April 15."

**5. Protect the team**

"I know this feels like a setback. It is. But it's also **normal** in a migration of this scale. We caught it before go-live. That's the system working."

### The Post-Setback Debrief

After every major setback, I run a quick retrospective:

- **What went wrong?**
- **Why didn't we catch this earlier?**
- **What can we change to prevent this next time?**

The goal isn't blame. It's **learning**.

One of our biggest setbacks was discovering that our product catalog data was inconsistent between systems. We didn't catch it until the integration testing phase.

The debrief revealed: we hadn't included product data validation in our data migration checklist.

We added it. Caught three more issues before go-live.

## Protecting Team Morale: The Long Game

Migrations are marathons. Most people treat them like sprints.

Your job as a leader is to **pace the team** so they don't burn out before the finish line.

### 1. Enforce Boundaries

No weekend work unless it's truly critical. No expectation of 24/7 availability. No "just one more thing" on Friday afternoon.

**I learned this the hard way.** During my first migration, I let the team work every weekend for two months straight. By month three, half the team was mentally checked out.

Now I enforce:
- No weekend work without explicit approval
- No expectation to respond to Slack after 7 PM
- Mandatory time off after go-live

### 2. Rotate the Hard Work

Some parts of a migration are brutal — data reconciliation, overnight cutover work, hypercare support.

Don't let the same people carry all the hard work. **Rotate it.**

During our last migration, we rotated hypercare shifts so everyone took a turn, but no one was on hypercare for more than a week.

### 3. Acknowledge the Toll

Migrations are exhausting. Don't pretend they're not.

I started saying this explicitly in team meetings:

"I know this is hard. I know you're tired. I know it feels like this will never end. It will end. And when it does, we'll take a break before we start the next big thing."

That simple acknowledgment mattered more than I expected.

### 4. Plan the Recovery Period

After go-live, your team needs time to recover. Not just a long weekend. Real recovery.

We implemented a **two-week "innovation sprint"** immediately after go-live. The team could work on anything they wanted — bug fixes, tech debt, exploratory projects. No pressure, no deadlines.

Half the team used it to actually take time off. The other half used it to clean up things they'd been wanting to fix for months.

Everyone came back recharged.

## When to Pull the Plug

Sometimes migrations should be stopped.

I've never had to do this, but I've been close. Here are the signals that a migration is headed for disaster:

- **The team has lost confidence in the plan.** If the people doing the work don't believe it will succeed, it won't.
- **The scope has doubled but the timeline hasn't changed.** You're now building twice the system in the same amount of time. The math doesn't work.
- **Key people are leaving because of the migration.** One departure is normal. Three is a pattern.
- **The business has changed in a way that makes this migration obsolete.** Don't finish building something the company no longer needs.
- **The vendor has repeatedly failed to deliver.** If the foundation is broken, the rest of the project is too.

If you see these signals, you have two choices:
1. **Pause and reset.** Re-scope, re-plan, re-resource.
2. **Cancel and pivot.** Admit the sunk cost and choose a different path.

Both are better than marching the team off a cliff.

## The Bottom Line

System migrations are hard. Not because of the technology — although that's hard too.

They're hard because you're asking people to build something complex and critical while the business depends on them not to fail. That's **emotionally exhausting**.

Your job as a leader isn't to shield the team from the difficulty. It's to **help them navigate it** without breaking.

Here's what that looks like:

1. **Understand the emotional arc.** Migrations follow a predictable pattern. Plan for it.
2. **Over-communicate.** Uncertainty kills morale. Transparency builds trust.
3. **Engage resisters.** Give them a role instead of sidelining them.
4. **Celebrate small wins.** Frequent progress beats one big finish line.
5. **Handle setbacks with honesty.** Acknowledge problems, explain impact, share the plan.
6. **Protect team morale.** Enforce boundaries, rotate hard work, acknowledge the toll.
7. **Know when to pull the plug.** Not every migration should be finished.

The migrations I'm proudest of aren't the ones that went perfectly. They're the ones where the team came out the other side **still intact, still trusting each other, and still willing to do hard things together**.

That's the real measure of success.
