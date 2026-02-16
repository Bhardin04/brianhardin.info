# Blog Content Strategy — Brian Hardin

## Voice & Positioning

**Author Persona**: VP of Revenue, Billing & Collections at a ~$1B ARR SaaS company. Practitioner who codes Python, builds automations, manages NetSuite and QlikSense environments, navigates ASC 606/842 compliance, and leads teams through post-merger integrations.

**Tone**: Professional but approachable. First-person experience ("Here's what I've learned..."). Specific over vague. Opinionated where warranted. No fluff — respect the reader's time.

**Target Readers**: Engineering leaders, revenue operations professionals, SaaS finance leaders, technical managers, and software engineers who want to bridge business and technology.

---

## Content Categories (6)

| # | Category | Post Count | Focus |
|---|----------|-----------|-------|
| 1 | Revenue Operations | 9 | Billing systems, collections, AR optimization, order-to-cash |
| 2 | Technical How-Tos | 10 | Python, FastAPI, automation, data engineering |
| 3 | Leadership & Career | 9 | Engineering management, career growth, team building |
| 4 | SaaS Finance & Compliance | 8 | ASC 606/842, audit readiness, metrics, financial reporting |
| 5 | Integration & Change Management | 7 | Post-merger integration, system migrations, NetSuite |
| 6 | Productivity & Tools | 7 | QlikSense, developer tools, workflow optimization |

**Total: 50 posts**

---

## 50 Blog Post Topics

### Category 1: Revenue Operations (9 posts)

**1. Why Your Billing System Is Your Most Important Product**
- Type: Opinion / Strategy
- Hook: Your billing system touches every customer, every dollar, and every metric your board cares about. Treat it accordingly.
- Key Points: Billing as revenue infrastructure, common mistakes in treating billing as an afterthought, what "billing as product" looks like at scale

**2. The Order-to-Cash Pipeline Nobody Talks About**
- Type: Deep Dive
- Hook: Most SaaS companies obsess over the sales pipeline but ignore the pipeline that actually collects the money.
- Key Points: Mapping the O2C lifecycle, bottlenecks between contract signing and cash receipt, automation opportunities at each stage

**3. Building a Collections Strategy That Doesn't Destroy Customer Relationships**
- Type: Strategy / Playbook
- Hook: You need the money. They need the product. Here's how to handle the conversation when the invoice is 90 days past due.
- Key Points: Tiered escalation frameworks, automation for early-stage collections, when to involve humans, maintaining customer lifetime value

**4. What I Learned Managing AR at a Billion-Dollar SaaS Company**
- Type: Experience / Lessons Learned
- Hook: At scale, accounts receivable stops being an accounting function and starts being a strategic operation.
- Key Points: AR as a leading indicator, DSO management, team structure, technology stack decisions

**5. Revenue Leakage: Finding the Money You're Already Owed**
- Type: Tactical Guide
- Hook: Most SaaS companies are leaving 2-5% of recognized revenue on the table. Here's where to look.
- Key Points: Common leakage points (failed renewals, misconfigured billing rules, credit memo abuse), detection methods, prevention frameworks

**6. Automating Invoice Disputes: From 72 Hours to 15 Minutes**
- Type: Technical Case Study
- Hook: Our dispute resolution process was a manual nightmare. Here's how we automated 80% of it.
- Key Points: Dispute taxonomy, rule-based routing, self-service resolution portals, measuring resolution time

**7. The Real Cost of Manual Billing Processes**
- Type: Analysis
- Hook: That spreadsheet your team uses to calculate overages? It's costing you more than you think.
- Key Points: Hidden costs (labor, errors, audit risk, delayed recognition), building the business case for automation, ROI framework

**8. Subscription Billing Models: What Works and What Fails at Scale**
- Type: Strategy
- Hook: Usage-based, seat-based, hybrid — every billing model sounds great until you try to implement it in your ERP.
- Key Points: Model comparison from an implementation perspective, what each requires from your tech stack, migration strategies between models

**9. Building a Revenue Operations Team from Scratch**
- Type: Playbook
- Hook: Revenue operations isn't just sales ops with a new name. Here's how to build a team that actually drives cross-functional revenue outcomes.
- Key Points: Role definitions, hiring sequence, KPIs, reporting structure, common org design mistakes

### Category 2: Technical How-Tos (10 posts)

**10. Python for Finance Teams: Automating the Work Nobody Wants to Do**
- Type: Tutorial
- Hook: Your finance team spends 30% of their time on tasks a Python script could handle in seconds.
- Key Points: Common finance automation targets (reconciliation, report generation, data validation), starter patterns, libraries (pandas, openpyxl), real examples

**11. Building Internal Tools with FastAPI: A Practical Guide**
- Type: Tutorial
- Hook: Your team doesn't need another SaaS subscription. They need a 200-line FastAPI app that does exactly what they need.
- Key Points: When to build vs buy, FastAPI project structure for internal tools, authentication patterns, deployment considerations

**12. Connecting NetSuite to Everything: REST APIs and SuiteScript Patterns**
- Type: Technical Deep Dive
- Hook: NetSuite is powerful. NetSuite's API documentation is... less powerful. Here's what actually works.
- Key Points: RESTlet patterns, SuiteScript 2.0 essentials, token-based auth, handling rate limits, common integration architectures

**13. Data Pipeline Architecture for Revenue Reporting**
- Type: Architecture Guide
- Hook: If your revenue reports take three days to produce, you don't have a reporting problem — you have a data architecture problem.
- Key Points: Source system extraction, transformation logic for revenue data, staging patterns, incremental loading, data quality checks

**14. Writing Python Scripts That Finance People Can Actually Use**
- Type: Best Practices
- Hook: The best automation script in the world is worthless if nobody on your team can run it.
- Key Points: CLI design, configuration files vs hardcoded values, logging for non-developers, error messages humans can understand, packaging and distribution

**15. Async Python in Production: Lessons from Real Workloads**
- Type: Experience / Technical
- Hook: Async Python isn't just for web servers. Here's how we use it for batch processing, API integrations, and ETL pipelines.
- Key Points: When async matters (and when it doesn't), asyncio patterns for business applications, error handling, monitoring, production gotchas

**16. Building a Reconciliation Engine in Python**
- Type: Tutorial / Architecture
- Hook: Bank reconciliation, intercompany reconciliation, payment matching — they all follow the same pattern. Here's how to build a general-purpose engine.
- Key Points: Matching algorithms, fuzzy matching for amounts and dates, exception handling, reporting, scaling considerations

**17. SQL Patterns Every Revenue Analyst Should Know**
- Type: Reference / Tutorial
- Hook: You don't need to be a database engineer to write SQL that answers real business questions about revenue.
- Key Points: Window functions for MRR calculation, cohort analysis queries, revenue waterfall patterns, performance optimization for large datasets

**18. Deploying Python Applications with Docker: Beyond the Basics**
- Type: Technical Guide
- Hook: Getting a Dockerfile to work is step one. Getting it to work reliably in production is the real challenge.
- Key Points: Multi-stage builds, secrets management, health checks, logging strategies, CI/CD integration, common mistakes

**19. API Design for Internal Business Systems**
- Type: Architecture / Best Practices
- Hook: Internal APIs deserve the same design rigor as external ones. Your future self is the most important API consumer.
- Key Points: REST conventions for business domains, versioning for internal systems, error handling that helps debugging, documentation that stays current

### Category 3: Leadership & Career (9 posts)

**20. The Technical Leader's Dilemma: When to Code and When to Delegate**
- Type: Leadership / Opinion
- Hook: The hardest transition in a technical career isn't learning to lead. It's learning to let go of the keyboard.
- Key Points: Signs you're coding when you should be leading, maintaining technical credibility without being the bottleneck, the "architect" escape hatch

**21. Managing a Team Through a System Migration**
- Type: Leadership / Playbook
- Hook: System migrations fail more often because of people problems than technology problems. Here's how to lead your team through one.
- Key Points: Communication cadence, managing resistance, celebrating small wins, handling the inevitable setbacks, protecting team morale

**22. Hiring Engineers Who Can Talk to the Business**
- Type: Hiring / Leadership
- Hook: The most valuable engineer on a revenue team isn't the one who writes the best code. It's the one who understands why the code matters.
- Key Points: Interview questions that reveal business acumen, evaluating communication skills, red flags, building a team that bridges technical and business

**23. What I Wish I Knew Before Becoming a VP**
- Type: Career / Reflection
- Hook: Nobody prepares you for the loneliness of senior leadership. Here's what the job actually looks like.
- Key Points: The shift from execution to strategy, managing up, political navigation, maintaining authenticity, the imposter syndrome that never fully goes away

**24. Building a Culture of Documentation**
- Type: Leadership / Process
- Hook: The best teams I've led had one thing in common: they wrote things down.
- Key Points: Why documentation culture matters, practical implementation (templates, review processes), overcoming resistance, measuring adoption

**25. Cross-Functional Leadership: Working with Sales, Finance, and Engineering**
- Type: Leadership / Strategy
- Hook: Revenue operations sits at the intersection of three departments that often don't speak the same language. That's your superpower.
- Key Points: Translation skills, building trust across functions, running effective cross-functional meetings, navigating conflicting priorities

**26. Giving Technical Feedback That Actually Helps**
- Type: Leadership / Communication
- Hook: "Looks good" isn't a code review. "This is wrong" isn't feedback. Here's the space between.
- Key Points: Specificity in feedback, separating opinion from requirement, written vs verbal feedback, creating psychological safety for honest discussion

**27. The Underrated Skill of Saying No**
- Type: Career / Opinion
- Hook: Every "yes" to the wrong thing is a "no" to the right thing. Learning to decline is a career accelerator.
- Key Points: Frameworks for evaluating requests, how to say no without burning bridges, opportunity cost thinking, protecting your team's focus

**28. Running Effective One-on-Ones with Technical Staff**
- Type: Leadership / Tactical
- Hook: If your one-on-ones are status updates, you're wasting everyone's time. Here's how to make them count.
- Key Points: Question frameworks, career development conversations, giving hard feedback privately, frequency and format, common pitfalls

### Category 4: SaaS Finance & Compliance (8 posts)

**29. ASC 606 for Engineers: What You Need to Know**
- Type: Educational
- Hook: Revenue recognition isn't just an accounting problem. If you build billing systems, ASC 606 shapes what you can and can't do.
- Key Points: Five-step model simplified, performance obligations in SaaS, what engineers need to understand about contract modifications, system implications

**30. ASC 842 Lease Accounting: The Implementation Nobody Enjoyed**
- Type: Experience / Guide
- Hook: If you think lease accounting is boring, you've never had to implement it in an ERP system two weeks before an audit.
- Key Points: Key requirements, system configuration challenges, data migration nightmares, lessons from a real implementation

**31. Preparing Revenue Systems for External Audits**
- Type: Strategic Guide
- Hook: External auditors will find every shortcut your revenue team ever took. Here's how to fix them before the auditors arrive.
- Key Points: SOX compliance requirements for revenue systems, documentation standards, system controls, audit trail requirements, remediation prioritization

**32. SaaS Metrics That Actually Matter: A Practitioner's Guide**
- Type: Analysis / Opinion
- Hook: ARR. NRR. LTV/CAC. Gross Margin. Everyone tracks them. Few calculate them correctly.
- Key Points: Metric definitions that withstand scrutiny, common calculation errors, building metrics infrastructure, what investors actually look at

**33. Month-End Close in 5 Days: How We Cut Our Close Time in Half**
- Type: Case Study
- Hook: Our month-end close used to take 12 business days. Here's the playbook we used to get it under 5.
- Key Points: Process mapping, automation targets, parallel workstream design, dependency reduction, technology changes, culture changes

**34. Building Financial Controls That Don't Slow You Down**
- Type: Strategy / Tactical
- Hook: Controls exist to prevent errors and fraud. They shouldn't also prevent your team from getting work done.
- Key Points: Risk-based control design, automation as a control, segregation of duties in lean teams, monitoring vs prevention

**35. The CFO's Dashboard: What Finance Leaders Actually Need to See**
- Type: Product / Strategy
- Hook: I've built reporting dashboards for three different CFOs. Here's what they all wanted and what none of them asked for.
- Key Points: Real-time vs batch metrics, drill-down requirements, exception-based alerting, the metrics CFOs care about during board prep

**36. Revenue Forecasting When Your Data Is Messy**
- Type: Practical Guide
- Hook: Every forecasting model assumes clean data. Here's how to build useful forecasts when your data is anything but.
- Key Points: Data quality assessment frameworks, statistical methods that tolerate noise, ensemble approaches, communicating uncertainty

### Category 5: Integration & Change Management (7 posts)

**37. Post-Merger Integration: Combining Two Revenue Tech Stacks**
- Type: Experience / Playbook
- Hook: Merging two companies is hard. Merging their billing systems, ERPs, and revenue processes is where the real work begins.
- Key Points: Assessment framework, prioritization (what to merge first), parallel running strategies, data migration, organizational integration

**38. NetSuite Implementation: What They Don't Tell You in the Sales Demo**
- Type: Experience / Honest Guide
- Hook: NetSuite is a great platform. The implementation process will test your patience, your budget, and your relationships with vendors.
- Key Points: Realistic timelines, hidden costs, customization decisions, data migration pitfalls, change management essentials

**39. Migrating Billing Systems Without Losing Your Mind (or Your Data)**
- Type: Tactical Guide
- Hook: Billing system migrations have a failure rate that would terrify most project sponsors. Here's how to be on the right side of that statistic.
- Key Points: Parallel running strategy, reconciliation checkpoints, rollback planning, customer communication, testing strategy

**40. Change Management for Technical Teams**
- Type: Leadership / Change
- Hook: Engineers don't resist change because they're stubborn. They resist change because they've seen too many bad changes.
- Key Points: Building credibility before proposing change, involving engineers in solution design, pilot programs, measuring adoption, handling holdouts

**41. The Hidden Complexity of Multi-Entity Financial Systems**
- Type: Technical / Architecture
- Hook: One company, one chart of accounts, one currency — that's the easy version. Here's what happens when you add subsidiaries.
- Key Points: Intercompany transactions, elimination entries, multi-currency challenges, consolidation automation, reporting across entities

**42. Data Migration Playbook: Moving Financial Data Between Systems**
- Type: Playbook
- Hook: Financial data migration is unforgiving. Every dollar has to balance. Here's the methodology that's saved me more than once.
- Key Points: Data profiling, mapping strategies, validation frameworks, reconciliation automation, cutover planning, rollback procedures

**43. Building vs Buying Integration Solutions: A Decision Framework**
- Type: Strategy / Analysis
- Hook: "Just use Zapier" works until it doesn't. "Just build a custom integration" works until it breaks at 3 AM. Here's how to choose.
- Key Points: Evaluation criteria (volume, complexity, criticality, maintenance), total cost of ownership analysis, hybrid approaches, when to re-evaluate

### Category 6: Productivity & Tools (7 posts)

**44. QlikSense for Revenue Analytics: Getting Started the Right Way**
- Type: Tutorial / Guide
- Hook: QlikSense is powerful for revenue analytics — if you set it up correctly from the start. Most implementations don't.
- Key Points: Data model design for financial data, associative model advantages, set analysis for revenue calculations, dashboard design principles

**45. The Developer Workflow That Saves Me 10 Hours a Week**
- Type: Productivity / Personal
- Hook: After years of tweaking my setup, here's the workflow, tools, and habits that make the biggest difference in my daily output.
- Key Points: Terminal setup, automation scripts, keyboard shortcuts, time management patterns, meeting management, focus time protection

**46. Version Control for Configuration: Managing NetSuite Customizations**
- Type: Technical / Best Practices
- Hook: Your NetSuite customizations aren't in version control? That's a risk you're not being paid to take.
- Key Points: SuiteCloud Development Framework, Git workflows for ERP customizations, deployment pipelines, environment management, rollback strategies

**47. Building Dashboards That People Actually Use**
- Type: Product / Design
- Hook: The average business dashboard has 47 metrics and 3 users. Here's how to build dashboards that drive decisions.
- Key Points: User research for dashboards, progressive disclosure, alert-driven design, mobile considerations, refresh cadence, governance

**48. Automating Report Distribution: From Manual Email to Self-Service**
- Type: Tutorial / Automation
- Hook: If someone on your team manually emails a report every Monday morning, this post is for you.
- Key Points: Report scheduling architecture, conditional distribution logic, self-service portals, format considerations, audit trails

**49. My Essential Python Libraries for Business Automation**
- Type: Reference / Tools
- Hook: These are the Python libraries I reach for every time I need to automate a business process. Battle-tested, production-proven.
- Key Points: pandas (data manipulation), openpyxl (Excel), paramiko (SFTP), requests (APIs), schedule (job scheduling), Pydantic (validation), real-world usage examples for each

**50. Technical Debt in Business Systems: When to Pay It Down**
- Type: Strategy / Opinion
- Hook: That billing workaround from the merger? The hardcoded tax rule? The spreadsheet that feeds the ERP? Technical debt in business systems is invisible until it isn't.
- Key Points: Identifying business system technical debt, risk assessment frameworks, prioritization methods, building the business case for remediation, incremental vs big-bang approaches

---

## Execution Plan

| Batch | Posts | Description |
|-------|-------|-------------|
| 1 | — | Content strategy and 50 topics (this document) |
| 2 | 1-10 | Revenue Ops (1-9) + first Technical post (10) |
| 3 | 11-20 | Technical How-Tos (11-19) + first Leadership post (20) |
| 4 | 21-30 | Leadership & Career (21-28) + first SaaS Finance posts (29-30) |
| 5 | 31-40 | SaaS Finance (31-36) + Integration & Change (37-40) |
| 6 | 41-50 | Integration & Change (41-43) + Productivity & Tools (44-50) |

Each batch creates a seed script that inserts 10 posts into the database.

## Date Strategy

Posts will be backdated across a 6-month span (August 2025 - February 2026) to create a natural publishing cadence of ~2 posts/week. Featured posts will be distributed across categories.
