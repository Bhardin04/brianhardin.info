---
title: "Building a Reconciliation Engine in Python"
slug: "building-a-reconciliation-engine-in-python"
excerpt: "Bank reconciliation, intercompany reconciliation, payment matching — they all follow the same pattern. Here's how to build a general-purpose engine."
tags: ["Python", "Finance", "Automation", "Architecture"]
published: true
featured: true
created_at: "2025-11-17"
published_at: "2025-11-17"
author: "Brian Hardin"
meta_description: "How to build a general-purpose reconciliation engine in Python for bank reconciliation, payment matching, and intercompany reconciliation."
---

Every finance team deals with reconciliation. Bank statements need to match GL transactions. Payments need to match invoices. Intercompany charges need to reconcile between entities. The specifics vary, but the pattern is always the same: match items from System A with items from System B, identify discrepancies, and report exceptions.

I've built reconciliation engines for bank accounts, payment processors, revenue recognition, and intercompany transactions. Each time, I start with the same core architecture. Here's what works.

## The Core Pattern

A reconciliation engine has three fundamental components:

1. **Data loaders** that standardize inputs from different sources
2. **Matching logic** that pairs items based on configurable rules
3. **Exception handlers** that classify and report unmatched items

The key insight: **reconciliation is a matching problem, not a calculation problem.** You're not computing balances—you're finding pairs.

```python
from dataclasses import dataclass
from typing import List, Optional, Callable
from decimal import Decimal
from datetime import datetime

@dataclass
class ReconItem:
    """Standardized item from any source system."""
    id: str
    source: str  # 'bank', 'gl', 'payment_processor', etc.
    date: datetime
    amount: Decimal
    reference: Optional[str]
    description: Optional[str]
    metadata: dict

@dataclass
class Match:
    """A successful match between items."""
    items: List[ReconItem]
    match_type: str  # 'exact', 'fuzzy', 'many_to_one', etc.
    confidence: float
    variance: Decimal

@dataclass
class Exception:
    """An unmatched item requiring investigation."""
    item: ReconItem
    reason: str
    suggestions: List[Match]  # Possible matches below confidence threshold
```

This structure works for any reconciliation scenario. The `ReconItem` normalizes data from any source, `Match` represents successful pairs, and `Exception` captures items that need review.

## Building the Matching Engine

The matching engine compares items from two datasets and finds pairs based on configurable rules. Start with exact matching, then layer on fuzzy matching for real-world messiness.

```python
from typing import List, Tuple, Set
from collections import defaultdict

class ReconciliationEngine:
    def __init__(self, tolerance: Decimal = Decimal('0.01')):
        self.tolerance = tolerance
        self.matchers = []

    def add_matcher(self, matcher: Callable, priority: int = 0):
        """Add a matching rule with priority (higher runs first)."""
        self.matchers.append((priority, matcher))
        self.matchers.sort(key=lambda x: x[0], reverse=True)

    def reconcile(
        self,
        source_a: List[ReconItem],
        source_b: List[ReconItem]
    ) -> Tuple[List[Match], List[Exception]]:
        """
        Main reconciliation algorithm.
        Returns matched pairs and exceptions.
        """
        matches = []
        unmatched_a = set(range(len(source_a)))
        unmatched_b = set(range(len(source_b)))

        # Try each matcher in priority order
        for priority, matcher in self.matchers:
            new_matches = matcher(
                [source_a[i] for i in unmatched_a],
                [source_b[i] for i in unmatched_b],
                self.tolerance
            )

            for match in new_matches:
                matches.append(match)
                # Remove matched items from unmatched sets
                for item in match.items:
                    if item.source == source_a[0].source:
                        idx = source_a.index(item)
                        unmatched_a.discard(idx)
                    else:
                        idx = source_b.index(item)
                        unmatched_b.discard(idx)

        # Create exceptions for unmatched items
        exceptions = []
        for idx in unmatched_a:
            exceptions.append(Exception(
                item=source_a[idx],
                reason="no_match_found",
                suggestions=self._find_suggestions(source_a[idx], source_b)
            ))

        for idx in unmatched_b:
            exceptions.append(Exception(
                item=source_b[idx],
                reason="no_match_found",
                suggestions=self._find_suggestions(source_b[idx], source_a)
            ))

        return matches, exceptions

    def _find_suggestions(
        self,
        item: ReconItem,
        candidates: List[ReconItem],
        max_suggestions: int = 3
    ) -> List[Match]:
        """Find possible matches that didn't meet confidence threshold."""
        # Implementation details for fuzzy matching suggestions
        pass
```

This architecture lets you add matching rules incrementally, from most specific to most general. Exact matches run first, then fuzzy matches, then complex multi-item matches.

## Matching Strategies

### Exact Matching

Start with the simplest case: items that match exactly on amount and date.

```python
def exact_matcher(
    items_a: List[ReconItem],
    items_b: List[ReconItem],
    tolerance: Decimal
) -> List[Match]:
    """Match items with identical amounts and dates."""
    matches = []

    # Index items_b by (date, amount) for O(1) lookup
    index = defaultdict(list)
    for item in items_b:
        key = (item.date.date(), item.amount)
        index[key].append(item)

    used_b = set()

    for item_a in items_a:
        key = (item_a.date.date(), item_a.amount)
        candidates = [b for b in index[key] if id(b) not in used_b]

        if candidates:
            match_b = candidates[0]  # Take first available match
            matches.append(Match(
                items=[item_a, match_b],
                match_type="exact",
                confidence=1.0,
                variance=Decimal('0')
            ))
            used_b.add(id(match_b))

    return matches
```

### Fuzzy Amount Matching

Real-world data is messy. Banks round differently, FX conversions introduce variance, timing differences cause small discrepancies.

```python
def fuzzy_amount_matcher(
    items_a: List[ReconItem],
    items_b: List[ReconItem],
    tolerance: Decimal
) -> List[Match]:
    """Match items with similar amounts within tolerance."""
    matches = []
    used_b = set()

    for item_a in items_a:
        best_match = None
        best_variance = None

        for item_b in items_b:
            if id(item_b) in used_b:
                continue

            # Check date proximity (within 3 days)
            date_diff = abs((item_a.date - item_b.date).days)
            if date_diff > 3:
                continue

            # Check amount variance
            variance = abs(item_a.amount - item_b.amount)
            if variance > tolerance:
                continue

            # Keep closest match
            if best_match is None or variance < best_variance:
                best_match = item_b
                best_variance = variance

        if best_match:
            confidence = float(1 - (best_variance / tolerance))
            matches.append(Match(
                items=[item_a, best_match],
                match_type="fuzzy_amount",
                confidence=confidence,
                variance=best_variance
            ))
            used_b.add(id(best_match))

    return matches
```

### Reference Number Matching

When amounts and dates don't align, reference numbers often do. Invoice numbers, transaction IDs, check numbers—these can bridge timing differences.

```python
import re

def reference_matcher(
    items_a: List[ReconItem],
    items_b: List[ReconItem],
    tolerance: Decimal
) -> List[Match]:
    """Match based on reference numbers in descriptions or reference fields."""
    matches = []

    def extract_references(text: str) -> Set[str]:
        """Extract potential reference numbers from text."""
        if not text:
            return set()
        # Match patterns like INV-12345, #123456, etc.
        patterns = [
            r'INV-?\d+',
            r'#\d+',
            r'\b\d{6,}\b',  # 6+ digit numbers
        ]
        refs = set()
        for pattern in patterns:
            refs.update(re.findall(pattern, text, re.IGNORECASE))
        return refs

    # Build reference index for items_b
    ref_index = defaultdict(list)
    for item in items_b:
        refs = extract_references(item.reference or '')
        refs.update(extract_references(item.description or ''))
        for ref in refs:
            ref_index[ref].append(item)

    used_b = set()

    for item_a in items_a:
        refs_a = extract_references(item_a.reference or '')
        refs_a.update(extract_references(item_a.description or ''))

        for ref in refs_a:
            candidates = [b for b in ref_index.get(ref, []) if id(b) not in used_b]
            for candidate in candidates:
                # Still check amount is reasonably close
                variance = abs(item_a.amount - candidate.amount)
                if variance <= tolerance * 10:  # More lenient for reference matches
                    matches.append(Match(
                        items=[item_a, candidate],
                        match_type="reference",
                        confidence=0.9,
                        variance=variance
                    ))
                    used_b.add(id(candidate))
                    break

    return matches
```

### Many-to-One Matching

Common scenario: one bank transaction represents multiple invoices paid together, or one invoice gets split across multiple payments.

```python
from itertools import combinations

def many_to_one_matcher(
    items_a: List[ReconItem],
    items_b: List[ReconItem],
    tolerance: Decimal,
    max_group_size: int = 5
) -> List[Match]:
    """
    Match groups of items that sum to a single item.
    Computationally expensive - use after simpler matchers.
    """
    matches = []
    used_a = set()
    used_b = set()

    # Try matching multiple items_a to single items_b
    for item_b in items_b:
        if id(item_b) in used_b:
            continue

        available_a = [a for a in items_a if id(a) not in used_a]

        # Try combinations up to max_group_size
        for size in range(2, min(max_group_size + 1, len(available_a) + 1)):
            for combo in combinations(available_a, size):
                total = sum(item.amount for item in combo)
                variance = abs(total - item_b.amount)

                if variance <= tolerance:
                    matches.append(Match(
                        items=list(combo) + [item_b],
                        match_type=f"many_to_one_{size}",
                        confidence=0.8,
                        variance=variance
                    ))
                    used_b.add(id(item_b))
                    for item in combo:
                        used_a.add(id(item))
                    break

            if id(item_b) in used_b:
                break

    return matches
```

This is computationally expensive, so run it last and limit the group size. For 1,000 items, checking all 5-item combinations would be prohibitive. Use heuristics to narrow candidates first.

## Exception Classification and Reporting

Unmatched items aren't failures—they're the whole point. The reconciliation engine surfaces what needs human attention.

```python
from enum import Enum

class ExceptionType(Enum):
    UNMATCHED = "unmatched"
    DUPLICATE = "duplicate"
    VARIANCE_EXCEEDED = "variance_exceeded"
    DATE_MISMATCH = "date_mismatch"
    AMOUNT_MISMATCH = "amount_mismatch"

def classify_exception(exception: Exception, all_items: List[ReconItem]) -> ExceptionType:
    """Determine the type of exception for better reporting."""
    item = exception.item

    # Check for duplicates
    duplicates = [
        i for i in all_items
        if i.id != item.id
        and i.source == item.source
        and i.amount == item.amount
        and i.date.date() == item.date.date()
    ]
    if duplicates:
        return ExceptionType.DUPLICATE

    # Check suggestions for near-misses
    if exception.suggestions:
        best_suggestion = exception.suggestions[0]
        variance = best_suggestion.variance

        # Determine if it's a date or amount issue
        suggestion_item = [i for i in best_suggestion.items if i.id != item.id][0]
        date_diff = abs((item.date - suggestion_item.date).days)

        if date_diff > 2:
            return ExceptionType.DATE_MISMATCH
        elif variance > Decimal('0.01'):
            return ExceptionType.AMOUNT_MISMATCH

    return ExceptionType.UNMATCHED

def generate_exception_report(exceptions: List[Exception], all_items: List[ReconItem]) -> dict:
    """Create a structured exception report for finance team review."""
    classified = defaultdict(list)

    for exc in exceptions:
        exc_type = classify_exception(exc, all_items)
        classified[exc_type].append({
            'id': exc.item.id,
            'source': exc.item.source,
            'date': exc.item.date.isoformat(),
            'amount': float(exc.item.amount),
            'reference': exc.item.reference,
            'description': exc.item.description,
            'suggestions': [
                {
                    'match_type': s.match_type,
                    'confidence': s.confidence,
                    'variance': float(s.variance),
                    'items': [{'id': i.id, 'amount': float(i.amount)} for i in s.items]
                }
                for s in exc.suggestions[:3]  # Top 3 suggestions
            ]
        })

    return {
        'total_exceptions': len(exceptions),
        'by_type': {k.value: len(v) for k, v in classified.items()},
        'details': {k.value: v for k, v in classified.items()}
    }
```

## Putting It Together

Here's how you'd use this engine for a typical bank reconciliation:

```python
from decimal import Decimal

# Initialize engine
engine = ReconciliationEngine(tolerance=Decimal('0.01'))

# Add matchers in priority order
engine.add_matcher(exact_matcher, priority=100)
engine.add_matcher(reference_matcher, priority=80)
engine.add_matcher(fuzzy_amount_matcher, priority=60)
engine.add_matcher(many_to_one_matcher, priority=40)

# Load data (pseudo-code - actual implementation depends on your sources)
bank_transactions = load_bank_statement('2024-01.csv')
gl_entries = load_gl_entries('cash_account', '2024-01-01', '2024-01-31')

# Run reconciliation
matches, exceptions = engine.reconcile(bank_transactions, gl_entries)

# Generate reports
print(f"Matched: {len(matches)}")
print(f"Exceptions: {len(exceptions)}")

exception_report = generate_exception_report(exceptions, bank_transactions + gl_entries)
# Export to Excel, send to Slack, whatever your workflow requires
```

## Scaling Considerations

For small reconciliations (< 10,000 items per side), this approach works fine in memory. For larger datasets:

**Partition by date**: Reconcile month by month rather than all at once. Matches rarely cross month boundaries.

**Use databases**: Load items into PostgreSQL or similar, use SQL for initial filtering and exact matching, then pull smaller candidate sets into Python for fuzzy matching.

**Parallelize**: Each month or each account can be reconciled independently. Use multiprocessing or async to run them concurrently.

**Cache results**: Store matches and exceptions in a database so you can incrementally reconcile new items without reprocessing everything.

## The Bottom Line

Reconciliation engines follow the same pattern regardless of what you're reconciling. Standardize inputs, apply matching rules from specific to general, classify exceptions for review.

The hard part isn't the code—it's understanding your business logic well enough to encode the matching rules. Talk to your accounting team. Understand how they currently reconcile manually. Those heuristics become your matchers.

Build this once, configure it for different scenarios. Bank recon, payment matching, intercompany settlements—they all run through the same engine with different matchers and data loaders. That's the leverage.
