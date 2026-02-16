---
title: "Running Effective One-on-Ones with Technical Staff"
slug: "running-effective-one-on-ones-with-technical-staff"
excerpt: "If your one-on-ones are status updates, you're wasting everyone's time. Here's how to make them the most valuable 30 minutes of your week."
tags: ["Leadership", "Management", "One-on-Ones", "Engineering Management"]
published: true
featured: false
created_at: "2026-02-09"
published_at: "2026-02-09"
author: "Brian Hardin"
meta_description: "How to run one-on-ones that develop engineers, surface problems early, and build trust with your team."
---

If your one-on-ones are status updates, you're wasting everyone's time.

I learned this the hard way when I took over a team of 12 engineers at my second company. I'd schedule 30-minute sessions, show up with a notebook, and ask "What are you working on?" We'd spend 25 minutes reviewing Jira tickets, and I'd leave thinking I was being a good manager.

Three months in, one of my best engineers quit. During the exit interview, she told me she'd been frustrated for months but never felt like our one-on-ones were the right place to bring it up. **I'd trained her to use our time together for status updates, not real conversations.**

That cost me a senior engineer and taught me what one-on-ones are actually for.

## What One-on-Ones Are For

Let me be direct: **one-on-ones are not status meetings**. You have Slack, standup, and sprint reviews for status updates. If someone needs 30 minutes to tell you what they're working on, your communication processes are broken.

One-on-ones serve three purposes:

1. **Career development** — helping your direct report grow in the direction they want to go
2. **Problem surfacing** — catching issues before they become crises
3. **Relationship building** — creating the trust required for the first two to work

Everything else is secondary.

## The Question Framework That Actually Works

I maintain a rotation of core questions that I cycle through based on what I'm seeing from each person. These aren't scripts—they're conversation starters that lead to real discussions.

### For Career Development

**"What do you want to be doing in two years that you're not doing now?"**

This is better than asking about a five-year plan because it's specific enough to be actionable but far enough out to be aspirational. When someone tells me they want to be leading architectural decisions, we can map out what skills they need and what opportunities would build those skills.

I keep notes on these answers. When someone tells me in February they want to get better at public speaking, and a conference CFP comes across my desk in May, I remember. **The best career development happens when managers create opportunities, not when they give advice.**

**"What's something you've learned recently that made you better at your job?"**

This question does two things. First, it tells me if someone is actually growing. If they can't answer this question, we have a problem. Second, it gives me insight into how they think about their own development.

The best engineers I've worked with can always answer this question, and their answers reveal whether they're learning from code reviews, from production incidents, from conference talks, or from reading. That tells me how to feed them more growth opportunities.

### For Problem Surfacing

**"What's the most frustrating part of your job right now?"**

Notice I didn't ask "Are you frustrated?" or "Is everything okay?" Those questions invite "fine" as an answer. **Asking what's most frustrating assumes something is frustrating and asks them to prioritize.**

The answers range from process issues ("our deploy pipeline takes 45 minutes") to technical debt ("the authentication system is held together with duct tape") to interpersonal problems ("I don't think my code reviews are being taken seriously").

Each category requires a different response, but all of them require me to actually do something. If someone tells me the deploy pipeline is slow and I nod sympathetically but don't fix it, they'll stop bringing up problems.

**"What's something I don't know about the project you're on?"**

This surfaces blind spots. Sometimes it's technical ("the API we depend on rate-limits us in ways that aren't documented"). Sometimes it's procedural ("the product manager keeps changing requirements in Slack instead of updating tickets"). Sometimes it's political ("the other team is blocking us because they disagree with our approach").

Whatever the answer, it's almost always something I needed to know.

## Giving Feedback That Lands

The hardest part of one-on-ones is giving difficult feedback. I've seen managers avoid this for months, letting small issues compound into performance problems.

**If you're waiting for the right moment to give critical feedback, the right moment was two weeks ago.** The second-best moment is now.

Here's my framework:

### Be Specific and Recent

Bad feedback: "You need to communicate better."

Good feedback: "In yesterday's architecture review, you dismissed Sarah's concerns about database scaling without explaining your reasoning. That made her feel like you weren't taking her input seriously."

**The more specific you are, the easier it is for someone to act on the feedback.** Vague feedback feels like an attack on character. Specific feedback feels like coaching.

### Separate Behavior from Impact

I use this structure: "When you [behavior], [impact]."

"When you merge PRs without waiting for approval, it makes the team feel like code review is optional, and we miss opportunities to catch bugs before production."

This separates what they did from what it caused. It's not about judging them as a person—it's about helping them understand consequences they might not have seen.

### Make It a Two-Way Conversation

After delivering feedback, I ask: "Does that land? Do you see it differently?"

Sometimes they have context I don't have. Sometimes they disagree with my assessment. Either way, making space for their perspective turns feedback into dialogue instead of lecture.

I had an engineer who was consistently late to sprint planning. When I brought it up, he explained that he had to drop his kids off at school and couldn't make our 9am meeting. We moved sprint planning to 10am. **If I'd just told him to be on time, I would have missed the real problem.**

## Frequency and Format

I run one-on-ones weekly with my direct reports and biweekly with skip-levels.

**Weekly is not negotiable for direct reports.** I've tried biweekly, and problems that should take one week to resolve take three because we don't catch them early enough. The cost of 30 minutes per week is vastly cheaper than the cost of letting issues fester.

For format, I default to walking one-on-ones when possible. There's something about walking side-by-side that makes hard conversations easier. When someone doesn't have to make eye contact, they're more willing to bring up uncomfortable topics.

When remote, I keep cameras on but don't require it. Some people think better when they're not performing for a camera.

### The Document

I maintain a shared Google Doc for each direct report with three sections:

1. **Topics for next time** — either of us can add items throughout the week
2. **Notes from this meeting** — I write these during the meeting
3. **Long-term themes** — career goals, skill development, ongoing challenges

This serves two purposes. First, it ensures we don't forget topics between meetings. Second, it creates a record we can look back on. When someone tells me in January they want to lead a project, and I'm planning Q3 work in May, I can go back and remember what they wanted.

**The document is shared and editable by both of us.** I'm not taking secret notes. Everything I write, they can see and comment on.

## Common Pitfalls

### Canceling When Things Get Busy

The busier things get, the more tempting it is to cancel one-on-ones to "focus on real work." This is exactly backwards. **When things are busy is when you most need to know how your team is doing.**

I have a rule: I'll reschedule a one-on-one, but I won't cancel it. If I need to move it from Tuesday to Thursday because of an executive meeting, fine. But it happens that week.

### Letting Them Become Status Updates

This happens gradually. You start by asking about their project. They tell you about their progress. You nod and take notes. Before you know it, 30 minutes are gone and you've had a standup meeting, not a one-on-one.

I prevent this by asking explicitly: **"Anything from work you want to cover, or should we talk about bigger-picture stuff?"** This signals that status is optional and development/problems are primary.

### Talking Too Much

Early in my management career, I'd spend 20 minutes of a 30-minute one-on-one talking. Explaining my perspective, sharing my experience, giving advice they didn't ask for.

**Your job in a one-on-one is to listen, not to perform.** If you're talking more than 30% of the time, you're doing it wrong.

I now aim for an 80/20 split—they talk 80%, I talk 20%. My talking should be questions, feedback, and commitments to action, not monologues.

### Not Following Through

If someone brings up a problem and you say you'll fix it, you have to fix it. Or you have to explain why you can't fix it. The fastest way to make one-on-ones useless is to let issues raised in them disappear into the void.

I keep a "commitments" section in my own notebook. After each one-on-one, I review what I said I'd do and make sure it makes it onto my task list. **If I committed to investigating why deploys are slow, that needs to get done before the next one-on-one.**

## What Success Looks Like

You know your one-on-ones are working when:

- People bring up problems before they become crises
- You're rarely surprised by what's happening on projects
- Engineers come to meetings with topics already in the shared doc
- Difficult conversations happen regularly, not just during performance reviews
- People tell you things they're not telling anyone else

That last one is critical. If your one-on-ones are working, you'll know about problems before your boss does, before your skip-levels do, before they become public. **You become the early warning system for your team.**

## The Long Game

I've been doing one-on-ones for 15 years now. The engineers who've stayed in touch, who still ask for advice, who list me as a reference—they're the ones where we had great one-on-ones.

Not because I'm particularly wise. Not because I gave amazing career advice. But because I consistently showed up, asked good questions, and actually followed through on what they told me.

**The best thing you can do as a manager is make one-on-ones the most valuable 30 minutes of your direct report's week.** Not sprint planning. Not the all-hands. Not the strategy meeting.

Their one-on-one with you.

When you get that right, everything else gets easier. You retain your best people because they feel seen and supported. You catch problems early because people trust you with bad news. You build engineers who know what they're working toward because you've helped them see the path.

And you never have to learn about someone's frustrations in an exit interview again.
