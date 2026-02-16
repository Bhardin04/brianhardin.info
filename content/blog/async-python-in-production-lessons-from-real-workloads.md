---
title: "Async Python in Production: Lessons from Real Workloads"
slug: "async-python-in-production-lessons-from-real-workloads"
excerpt: "Async Python isn't just for web servers. Here's how we use it for batch processing, API integrations, and ETL pipelines in revenue operations."
tags: ["Python", "Asyncio", "Performance", "Production"]
published: true
featured: false
created_at: "2025-11-10"
published_at: "2025-11-10"
author: "Brian Hardin"
meta_description: "Practical lessons from using async Python in production for batch processing, API integrations, and ETL pipelines in business applications."
---

Most discussions about async Python focus on web frameworks and HTTP servers. But some of the biggest wins I've seen come from applying async patterns to batch processing, ETL pipelines, and business system integrations. The kind of workloads that run nightly, process thousands of records, and need to finish before the business day starts.

This isn't about theoretical performance gains. These are patterns we use in production to process revenue data, sync systems, and keep financial operations running smoothly.

## When Async Actually Matters

The first lesson: **async doesn't make your code faster—it makes waiting more efficient.**

If your bottleneck is CPU-bound computation, async won't help. You're still doing the same calculations on the same cores. But if you're waiting on external systems—APIs, databases, file I/O—async can dramatically reduce wall-clock time by eliminating sequential waiting.

Here's a real example. We need to fetch contract data from NetSuite, enrich it with usage data from our product API, and load it into our analytics database. Sequential processing takes about 2 hours for 10,000 contracts:

```python
# Sequential approach - 2 hours
for contract in contracts:
    netsuite_data = fetch_from_netsuite(contract.id)
    usage_data = fetch_from_product_api(contract.customer_id)
    enriched = merge_data(netsuite_data, usage_data)
    load_to_warehouse(enriched)
```

The async version completes in 15 minutes:

```python
# Async approach - 15 minutes
async def process_contract(contract, semaphore):
    async with semaphore:
        netsuite_data = await fetch_from_netsuite(contract.id)
        usage_data = await fetch_from_product_api(contract.customer_id)
        enriched = merge_data(netsuite_data, usage_data)
        await load_to_warehouse(enriched)

async def main():
    semaphore = asyncio.Semaphore(50)  # Control concurrency
    tasks = [process_contract(c, semaphore) for c in contracts]
    await asyncio.gather(*tasks, return_exceptions=True)
```

The key difference: instead of waiting for each API call to complete before starting the next one, we issue many requests concurrently and let the event loop handle the waiting.

## Patterns That Work in Business Applications

### Pattern 1: Controlled Parallelism with Semaphores

Don't just fire off unlimited concurrent requests. External APIs have rate limits, databases have connection pools, and your own infrastructure has capacity constraints.

```python
import asyncio
from typing import List, Any

class RateLimitedProcessor:
    def __init__(self, max_concurrent: int = 50, rate_limit: int = 100):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.rate_limit = rate_limit
        self.request_times: List[float] = []

    async def process_with_limits(self, coro):
        async with self.semaphore:
            # Enforce rate limiting
            await self._enforce_rate_limit()
            return await coro

    async def _enforce_rate_limit(self):
        now = asyncio.get_event_loop().time()
        # Remove timestamps older than 1 second
        self.request_times = [t for t in self.request_times if now - t < 1.0]

        if len(self.request_times) >= self.rate_limit:
            sleep_time = 1.0 - (now - self.request_times[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)

        self.request_times.append(now)
```

This pattern lets you respect API rate limits while still maximizing throughput. We use this for NetSuite integrations, where we can make 100 requests per second but want to leave headroom for other processes.

### Pattern 2: Batch Collection with Timeouts

When processing large datasets, you want progress updates and the ability to recover from partial failures. Don't wait for all tasks to complete—collect results as they finish and handle failures gracefully.

```python
async def process_with_progress(items: List[Any], processor_func):
    results = []
    errors = []

    tasks = [processor_func(item) for item in items]

    for coro in asyncio.as_completed(tasks):
        try:
            result = await asyncio.wait_for(coro, timeout=30.0)
            results.append(result)

            # Progress logging every 100 items
            if len(results) % 100 == 0:
                print(f"Processed {len(results)}/{len(items)}")

        except asyncio.TimeoutError:
            errors.append({"error": "timeout", "item": None})
        except Exception as e:
            errors.append({"error": str(e), "item": None})

    return results, errors
```

This approach gives you visibility into long-running jobs and prevents one slow API call from blocking the entire batch.

### Pattern 3: Async Database Operations

Database libraries like `asyncpg` for PostgreSQL offer significant performance improvements over synchronous drivers, especially for bulk inserts and parallel queries.

```python
import asyncpg
from typing import List, Dict

async def bulk_upsert(records: List[Dict], table: str, pool: asyncpg.Pool):
    """
    Efficiently upsert thousands of records using COPY and temp tables.
    """
    async with pool.acquire() as conn:
        async with conn.transaction():
            # Create temporary table
            await conn.execute(f"""
                CREATE TEMP TABLE temp_{table} (LIKE {table} INCLUDING ALL)
                ON COMMIT DROP
            """)

            # Bulk load into temp table using COPY
            columns = list(records[0].keys())
            await conn.copy_records_to_table(
                f'temp_{table}',
                records=records,
                columns=columns
            )

            # Upsert from temp to main table
            await conn.execute(f"""
                INSERT INTO {table} ({','.join(columns)})
                SELECT {','.join(columns)} FROM temp_{table}
                ON CONFLICT (id) DO UPDATE SET
                {','.join(f'{col}=EXCLUDED.{col}' for col in columns if col != 'id')}
            """)
```

This pattern can load 50,000 records in under a minute, compared to 20+ minutes with sequential inserts.

## Error Handling in Production

Async error handling requires a different mindset. Exceptions can occur in any task at any time, and you need to handle them without bringing down the entire job.

```python
import logging
from typing import List, Callable, Any

logger = logging.getLogger(__name__)

async def resilient_gather(tasks: List, max_retries: int = 3):
    """
    Execute tasks with retry logic and comprehensive error tracking.
    """
    results = []

    for task in tasks:
        retries = 0
        while retries < max_retries:
            try:
                result = await task
                results.append({"success": True, "data": result})
                break

            except asyncio.TimeoutError:
                retries += 1
                logger.warning(f"Timeout on attempt {retries}/{max_retries}")
                if retries >= max_retries:
                    results.append({"success": False, "error": "max_retries_exceeded"})
                await asyncio.sleep(2 ** retries)  # Exponential backoff

            except Exception as e:
                logger.error(f"Task failed: {e}", exc_info=True)
                results.append({"success": False, "error": str(e)})
                break

    return results
```

The key is treating failures as data, not exceptions that crash the process. Log them, track them, report them—but keep processing.

## When Not to Use Async

Async adds complexity. Don't reach for it unless you have clear evidence that I/O waiting is your bottleneck.

**Don't use async when:**
- Your workload is CPU-bound (use multiprocessing instead)
- You're making a single API call or database query
- The codebase is primarily synchronous and mixing both would be messy
- You're processing small datasets (< 100 items)
- The sequential version completes in acceptable time

**Do use async when:**
- You're making many concurrent API calls
- You're processing thousands of records with I/O per record
- You need to coordinate multiple external systems
- Wall-clock time matters (batch windows, SLAs)
- You have genuine parallelizable I/O operations

## Monitoring Async Workloads

Production async code needs instrumentation. You can't just run it and hope.

```python
import time
from contextlib import asynccontextmanager

class AsyncMetrics:
    def __init__(self):
        self.task_count = 0
        self.success_count = 0
        self.error_count = 0
        self.total_time = 0.0

    @asynccontextmanager
    async def track_task(self):
        self.task_count += 1
        start = time.time()

        try:
            yield
            self.success_count += 1
        except Exception:
            self.error_count += 1
            raise
        finally:
            self.total_time += time.time() - start

    def report(self):
        return {
            "total_tasks": self.task_count,
            "successful": self.success_count,
            "failed": self.error_count,
            "avg_time": self.total_time / self.task_count if self.task_count > 0 else 0
        }
```

Track task counts, success/failure rates, and timing. When something goes wrong at 3am, you'll want data.

## Production Gotchas

**Event loop blocking**: One synchronous blocking call ruins everything. If you must call synchronous code, use `loop.run_in_executor()` to run it in a thread pool.

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=10)

async def call_sync_api(data):
    loop = asyncio.get_event_loop()
    # Run blocking code in thread pool
    return await loop.run_in_executor(executor, sync_api_call, data)
```

**Connection pooling**: Create your connection pools at startup, not in async functions. Pool creation itself is synchronous and expensive.

**Memory usage**: Loading 10,000 tasks into memory all at once can cause problems. Process in chunks if you're working with very large datasets.

```python
async def process_in_chunks(items: List, chunk_size: int = 1000):
    for i in range(0, len(items), chunk_size):
        chunk = items[i:i + chunk_size]
        tasks = [process_item(item) for item in chunk]
        await asyncio.gather(*tasks)
```

## The Bottom Line

Async Python has transformed how we handle business-critical data operations. Jobs that used to run for hours now complete in minutes. But it's not magic—it's a tool that works when you have the right problem.

Start with profiling. Measure where your time goes. If you're spending most of your time waiting on I/O, async can help. If you're doing heavy computation, look elsewhere.

And when you do use async, instrument it properly. You're building production systems, not demos. You need visibility into what's working, what's failing, and why.
