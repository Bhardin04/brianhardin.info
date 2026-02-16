---
title: "Giving Technical Feedback That Actually Helps"
slug: "giving-technical-feedback-that-actually-helps"
excerpt: "'Looks good' isn't a code review. 'This is wrong' isn't feedback. Here's the space between that makes engineers better."
tags: ["Leadership", "Code Review", "Communication", "Engineering Management"]
published: true
featured: false
created_at: "2026-01-26"
published_at: "2026-01-26"
author: "Brian Hardin"
meta_description: "How to give technical feedback that improves code and develops engineers, with frameworks for code reviews, design reviews, and one-on-ones."
---

"Looks good" isn't a code review. "This is wrong" isn't feedback. Here's the space between that makes engineers better.

I review a lot of code. Not as much as I used to when I was an IC, but still enough to have opinions on what makes feedback useful versus what makes it noise.

**The problem with most technical feedback is that it's either too vague to be actionable or too harsh to be helpful.** You get rubber-stamp approvals that don't improve the code, or nitpicky comments that demoralize the engineer without addressing the real issues.

Good technical feedback sits in a very specific zone: specific enough to be actionable, kind enough to be heard, and structured in a way that develops the engineer's judgment over time.

Here's how I think about it.

## The Spectrum of Feedback Quality

Let me show you the range, from worst to best:

**Useless:** "Looks good 👍"

**Lazy:** "This won't scale."

**Nitpicky:** "Line 47: you should use `const` instead of `let` here."

**Better:** "I'm concerned about how this will perform when we hit 10K transactions per minute. Have you load-tested it?"

**Best:** "I'm concerned about performance at scale. Right now this makes a database call inside a loop (lines 52-58), which will cause N+1 queries when we have high transaction volume. Two options: (1) batch the queries using a single `WHERE IN` clause, or (2) cache the lookup table in Redis. Option 1 is simpler and probably enough for now. What do you think?"

**The difference is specificity, context, and collaboration.**

The last example tells the engineer:
- What the problem is (N+1 queries)
- Why it matters (performance at scale)
- Where it is (lines 52-58)
- What the options are (with trade-offs)
- That their judgment matters (what do you think?)

That's feedback that makes someone better.

## Separating Opinion from Requirement

One of the most important things I learned as a manager is to distinguish between **preferences** and **requirements**.

A preference is: "I would have used a switch statement here instead of if/else, but either works."

A requirement is: "This needs to handle the case where `userId` is null, or it will throw an error in production."

**If you don't label these clearly, engineers will treat every comment as a requirement, which leads to over-revision and wasted time.**

Here's how I label feedback:

- **[Required]** — This must be fixed before merge. It's a bug, a security issue, or violates a hard requirement.
- **[Suggestion]** — I think this would be better, but it's your call. Explain why, then defer to the author.
- **[Question]** — I don't understand this. Help me understand your reasoning.
- **[Nit]** — Tiny thing that doesn't matter much. Feel free to ignore.
- **[Blocking]** — This is a fundamental design issue that needs discussion before we proceed.

### Example Code Review with Labels

```python
# [Required] This will fail if `user` is None
def calculate_discount(user):
    if user.subscription_tier == "premium":  # What if user is None?
        return 0.20
    return 0.10

# [Suggestion] Consider extracting this into a constant
# This makes it easier to adjust the discount rates later without hunting through the code
PREMIUM_DISCOUNT = 0.20
STANDARD_DISCOUNT = 0.10

# [Question] Why are we using a raw SQL query here instead of the ORM?
# Is there a performance reason, or is this left over from an earlier version?

# [Nit] Extra blank line here (line 47)

# [Blocking] This approach won't work for multi-currency
# We need to discuss how to handle FX conversion before we proceed with this design
```

**Notice what this does:** It tells the engineer exactly what requires action, what's optional, and what needs conversation. That clarity is respectful of their time and judgment.

## Written vs. Verbal Feedback

Not all feedback should be written.

**Written feedback is great for:**
- Code review (needs to be documented and searchable)
- Architectural decisions (creates a paper trail)
- Async collaboration (different time zones, flexible schedules)
- Things that need precision (security, compliance, legal)

**Verbal feedback is better for:**
- Complex issues that require back-and-forth (faster than 10 rounds of comments)
- Feedback that might be misinterpreted in text (tone matters)
- Coaching moments (discussing career growth, skill development)
- Sensitive topics (performance concerns, interpersonal issues)

### When to Switch from Written to Verbal

If you find yourself writing more than three paragraphs of feedback on a single issue, **stop typing and schedule a call.**

I see this all the time: someone writes a novel in a pull request comment, the engineer writes a novel back, and 20 comments later they're still not aligned.

**Just get on a call.** You'll resolve it in 10 minutes.

Here's what I write instead: "This raises some architectural questions that are easier to discuss live. Can we hop on a quick call to talk through the design? I'll summarize the decisions in the PR afterward."

Then after the call, I post a summary: "Talked through this with @engineer. Decision: We're going with Option B (batch queries) because it's simpler and meets our current scale needs. If we hit performance issues in the future, we can revisit caching."

**That's the best of both worlds: quick resolution, documented decision.**

## The Feedback Sandwich Is a Lie

You've probably heard the "feedback sandwich" advice: Start with something positive, deliver the criticism, end with something positive.

I hate this.

**Why it doesn't work:**

1. **It's transparent.** Engineers know you're doing it, which makes the positive feedback feel fake.
2. **It dilutes the message.** The real feedback gets lost in the fluff.
3. **It's condescending.** You're treating adults like children who can't handle direct feedback.

### What Works Instead

**Be direct, be specific, and be kind.**

Bad: "Great work on this feature! One small thing — the error handling is completely broken and will crash in production. But overall, nice job!"

Good: "The core logic here is solid. I'm concerned about the error handling in the payment processing flow (lines 120-135). If the API call fails, we're not catching the exception, which will crash the service. Can you add a try/catch block and log the error to our monitoring system?"

**The difference:** I didn't bury the feedback in compliments. I was direct about the problem, specific about where it is, and clear about what needs to change.

And I didn't insult their intelligence by pretending it was a "small thing" when it's actually a production-breaking bug.

## Psychological Safety and High Standards

Here's the paradox: **You need psychological safety and high standards at the same time.**

Psychological safety means people can make mistakes, ask questions, and take risks without fear of punishment.

High standards means you don't ship mediocre code, you don't tolerate sloppiness, and you don't accept "good enough."

Most teams get one or the other. Great teams get both.

### How to Build Both

**Psychological safety:**

- Normalize mistakes: "I missed this in my review too — good catch."
- Ask questions without judgment: "Help me understand why you chose this approach."
- Praise publicly: "Great debugging work by @engineer — this was a tricky issue."
- Take responsibility: "I should have caught this in the design review. That's on me."

**High standards:**

- Block bad code: "This doesn't meet our quality bar. Here's what needs to change."
- Require tests: "I don't see test coverage for the error cases. Can you add that?"
- Push back on shortcuts: "I know we're in a hurry, but skipping input validation will create security issues. We need to do this right."
- Celebrate excellence: "This is exactly how I want to see error handling done. Clean, thorough, well-tested."

**The key is to be hard on the work, not the person.**

Bad: "This code is a mess. Did you even test this?"

Good: "This approach has some issues we need to fix. The error handling isn't robust, and I don't see test coverage for edge cases. Let's walk through what needs to change."

## Code Review Frameworks

Here's the framework I use when reviewing code:

### 1. Correctness (Required)

- Does it work as intended?
- Does it handle edge cases?
- Does it handle errors gracefully?
- Are there security vulnerabilities?

### 2. Maintainability (Important)

- Is it readable?
- Is it well-structured?
- Are variable and function names clear?
- Is there adequate documentation?

### 3. Performance (Context-Dependent)

- Will it scale to our expected load?
- Are there obvious inefficiencies (N+1 queries, unnecessary loops)?
- Does it use resources (memory, CPU, DB connections) efficiently?

### 4. Style (Low Priority)

- Does it follow our style guide?
- Is the formatting consistent?
- Are there unnecessary comments or dead code?

**I focus 80% of my review time on correctness and maintainability.** Style issues I'll flag with a [Nit] tag and move on.

If the code is functionally correct and maintainable, I don't care if someone used a `for` loop instead of a list comprehension.

## The One-on-One Feedback Framework

Code reviews are one type of feedback. One-on-ones are another.

**In one-on-ones, I focus on three types of feedback:**

### 1. Performance Feedback (What You're Doing)

This is about the work: quality, speed, impact.

Good: "Your last three PRs have been really clean. I especially liked how you structured the error handling in the payment refactor — that's exactly the level of rigor I want to see."

Bad: "You're doing great!"

### 2. Growth Feedback (How You're Developing)

This is about skills and career trajectory.

Good: "I've noticed you're getting more comfortable leading design reviews. The API spec you presented last week was thorough and well-thought-out. The next level is bringing the team to consensus faster — right now the discussions run long because you're trying to address every concern in real-time. Try pre-socializing the design with key stakeholders before the meeting so you can move to decision faster."

Bad: "You should work on your communication skills."

### 3. Behavioral Feedback (How You're Working with Others)

This is about collaboration, communication, and team dynamics.

Good: "I want to flag something I've noticed. In the last two sprint plannings, you've pushed back pretty hard on estimates from other engineers. I think you're trying to hold the team to a high standard, which I appreciate, but it's coming across as dismissive. Try asking questions instead of challenging: 'What are the risks you're accounting for in that estimate?' instead of 'That's way too long.'"

Bad: "You need to be a better team player."

**Notice the pattern: Specificity, examples, and actionable next steps.**

## When Feedback Isn't Landing

Sometimes you give good feedback and the engineer doesn't act on it. What do you do?

**First, check yourself:**

- Was the feedback clear and specific?
- Did I give them the context they needed?
- Did I make it seem optional when it was actually required?

**If the feedback was clear, follow up:**

"Hey, I noticed the error handling issue I flagged in the last PR is still present in this one. Was there a reason you didn't address it, or did my comment get lost?"

Sometimes it's an oversight. Sometimes they didn't understand the feedback. Sometimes they disagreed and didn't say so.

**If it happens repeatedly, have a direct conversation:**

"I want to talk about code review feedback. I've flagged the same issue in the last three PRs, and it's still not being addressed. What's going on?"

Then listen. Maybe they don't understand the issue. Maybe they think it's not important. Maybe they're overwhelmed and cutting corners.

**The conversation sounds like this:**

"I need you to address code review feedback before merging. If you disagree with the feedback, let's discuss it — I'm open to being wrong. But I can't approve PRs that have unresolved [Required] comments."

That's clear, direct, and fair.

## What Great Feedback Looks Like Over Time

You know your feedback is working when:

- **Engineers start self-reviewing before submitting.** They catch the issues you would have flagged because they've internalized your feedback.
- **Code quality improves without more review time.** You're not writing as many comments because the code is getting better.
- **Engineers ask for your feedback on design, not just code.** They want your input early, not just at the end.
- **They give each other the same kind of feedback you give.** The culture spreads.

I've seen this happen on teams I've led. Early on, I was writing 15-20 comments per PR. Six months later, I was writing 3-5. Not because I lowered my standards, but because the engineers got better.

**That's the goal: Make yourself less necessary over time.**

## The Mistakes I Still Make

I'm not perfect at this.

**Mistakes I've made:**

- **Being too harsh in written feedback.** Text doesn't convey tone, and I've hurt feelings when I thought I was just being direct.
- **Rubber-stamping when I'm busy.** Approving a PR with "LGTM" because I didn't have time to review it properly. That's unfair to the engineer and the codebase.
- **Focusing too much on style.** Getting into debates about tabs vs. spaces when the real issue is architectural.
- **Not following up.** Giving feedback and assuming it's addressed, then finding out three months later it wasn't.

**What I'm working on:**

- Defaulting to calls for complex feedback instead of long written comments
- Blocking time on my calendar for code reviews so I'm not rushing through them
- Being more explicit about what's [Required] vs. [Suggestion]
- Checking in on feedback I've given to make sure it's landing

## The Bottom Line

**Good technical feedback is specific, kind, and actionable.**

It tells the engineer:
- What the problem is
- Why it matters
- Where it is
- What good looks like
- Whether it's required or optional

It respects their time, their intelligence, and their judgment.

And over time, it makes them better engineers — which is the whole point.

If you're giving feedback that doesn't meet that bar, you're wasting everyone's time. Including your own.
