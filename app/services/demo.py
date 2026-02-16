"""
Demo services for interactive project demonstrations.
Provides business logic and data processing for demo scenarios.
"""

import random
from datetime import datetime, timedelta
from typing import Any
from uuid import uuid4

from app.models.demo import (
    AgingBucket,
    CollectorMetric,
    CustomerTarget,
    DashboardData,
    DataExtractionParams,
    DataRecord,
    DemoSession,
    DemoStatus,
    DemoType,
    Invoice,
    KPIMetric,
    PaymentEntry,
    PaymentMatch,
    PaymentProcessingResult,
    PipelineResult,
    RevenueRecord,
)


class DemoServiceBase:
    """Base service for all demo implementations"""

    MAX_SESSIONS = 100
    SESSION_TTL_SECONDS = 3600  # 1 hour

    def __init__(self) -> None:
        self.sessions: dict[str, DemoSession] = {}

    def _cleanup_expired_sessions(self) -> None:
        """Remove sessions older than SESSION_TTL_SECONDS"""
        now = datetime.now()
        expired = [
            sid
            for sid, session in self.sessions.items()
            if (now - session.created_at).total_seconds() > self.SESSION_TTL_SECONDS
        ]
        for sid in expired:
            del self.sessions[sid]

    def create_session(self, demo_type: DemoType) -> DemoSession:
        """Create a new demo session"""
        self._cleanup_expired_sessions()
        if len(self.sessions) >= self.MAX_SESSIONS:
            raise ValueError(
                "Maximum number of demo sessions reached. Please try again later."
            )
        session = DemoSession(demo_type=demo_type)
        self.sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> DemoSession | None:
        """Get existing demo session"""
        session = self.sessions.get(session_id)
        if session is None:
            return None
        if (
            datetime.now() - session.created_at
        ).total_seconds() > self.SESSION_TTL_SECONDS:
            del self.sessions[session_id]
            return None
        return session

    def update_session_status(
        self, session_id: str, status: DemoStatus, data: dict[str, Any] | None = None
    ) -> None:
        """Update session status and data"""
        if session := self.get_session(session_id):
            session.update_status(status, data or {})


class PaymentProcessingService(DemoServiceBase):
    """Service for payment processing demo"""

    def __init__(self) -> None:
        super().__init__()
        self.sample_invoices = self._generate_sample_invoices()
        self.processed_payments: list[dict[str, Any]] = []

    def _generate_sample_invoices(self) -> list[Invoice]:
        """Generate realistic sample invoices for demo"""
        customers = [
            ("CUST001", "Acme Corporation"),
            ("CUST002", "TechStart Inc"),
            ("CUST003", "Global Industries"),
            ("CUST004", "Retail Partners LLC"),
            ("CUST005", "Manufacturing Co"),
        ]

        invoices = []
        for i, (customer_id, customer_name) in enumerate(customers):
            # Create 2-4 invoices per customer
            for j in range(random.randint(2, 4)):
                invoice_date = datetime.now() - timedelta(days=random.randint(10, 120))
                due_date = invoice_date + timedelta(days=30)
                days_outstanding = (datetime.now() - due_date).days
                amount = random.uniform(5000, 50000)

                invoice = Invoice(
                    invoice_id=f"INV-{i + 1:03d}-{j + 1:03d}",
                    invoice_number=f"INV-2024-{(i * 4) + j + 1:04d}",
                    customer_id=customer_id,
                    customer_name=customer_name,
                    invoice_date=invoice_date,
                    due_date=due_date,
                    amount=round(amount, 2),
                    balance=round(amount, 2),
                    days_outstanding=max(0, days_outstanding),
                )
                invoices.append(invoice)

        return invoices

    def get_customer_invoices(self, customer_id: str) -> list[Invoice]:
        """Get open invoices for a customer"""
        return [
            inv
            for inv in self.sample_invoices
            if inv.customer_id == customer_id and inv.balance > 0
        ]

    def get_all_open_invoices(self) -> list[Invoice]:
        """Get all open invoices"""
        return [inv for inv in self.sample_invoices if inv.balance > 0]

    def process_payment(
        self, session_id: str, payment: PaymentEntry
    ) -> PaymentProcessingResult:
        """Process a payment and match to invoices"""
        session = self.get_session(session_id)
        if not session:
            raise ValueError("Invalid session")

        # Update session status
        self.update_session_status(session_id, DemoStatus.RUNNING)

        # Get customer invoices
        customer_invoices = self.get_customer_invoices(payment.customer_id)

        # Find matching invoices using automated logic
        matches = self._find_payment_matches(payment, customer_invoices)

        # Generate payment ID
        payment_id = f"PAY-{datetime.now().strftime('%Y%m%d')}-{len(self.processed_payments) + 1:04d}"

        # Calculate remaining amount
        total_applied = sum(match.amount_applied for match in matches)
        remaining_amount = max(0, payment.amount - total_applied)

        # Determine status
        if remaining_amount == 0:
            status = "matched"
        elif total_applied > 0:
            status = "partial"
        else:
            status = "exception"

        # Generate processing notes
        notes = self._generate_processing_notes(payment, matches, remaining_amount)

        result = PaymentProcessingResult(
            payment_id=payment_id,
            status=status,
            matches=matches,
            remaining_amount=remaining_amount,
            processing_notes=notes,
        )

        # Apply matches to invoices
        self._apply_payment_matches(matches)

        # Store processed payment
        self.processed_payments.append(
            {"payment": payment, "result": result, "processed_at": datetime.now()}
        )

        # Update session
        self.update_session_status(
            session_id,
            DemoStatus.COMPLETED,
            {
                "payment_result": result.model_dump(),
                "updated_invoices": [inv.model_dump() for inv in customer_invoices],
            },
        )

        return result

    def _find_payment_matches(
        self, payment: PaymentEntry, invoices: list[Invoice]
    ) -> list[PaymentMatch]:
        """Find the best matches for a payment"""
        matches = []
        remaining_amount = payment.amount

        # Sort invoices by aging (oldest first)
        sorted_invoices = sorted(
            invoices, key=lambda x: x.days_outstanding, reverse=True
        )

        for invoice in sorted_invoices:
            if remaining_amount <= 0:
                break

            if invoice.balance <= 0:
                continue

            # Calculate match confidence based on amount matching
            confidence = self._calculate_match_confidence(payment, invoice)

            if confidence < 0.5:  # Skip low confidence matches
                continue

            # Determine amount to apply
            amount_to_apply = min(remaining_amount, invoice.balance)

            # Determine match type
            if (
                amount_to_apply == invoice.balance
                and remaining_amount >= invoice.balance
            ):
                match_type = "exact"
            elif amount_to_apply < invoice.balance:
                match_type = "partial"
            else:
                match_type = "manual"

            match = PaymentMatch(
                payment_id=f"temp_{uuid4()}",
                invoice_id=invoice.invoice_id,
                amount_applied=amount_to_apply,
                confidence_score=confidence,
                match_type=match_type,
            )

            matches.append(match)
            remaining_amount -= amount_to_apply

        return matches

    def _calculate_match_confidence(
        self, payment: PaymentEntry, invoice: Invoice
    ) -> float:
        """Calculate confidence score for payment-invoice match"""
        # Base confidence
        confidence = 0.7

        # Exact amount match
        if abs(payment.amount - invoice.balance) < 0.01:
            confidence = 0.95
        # Close amount match (within 5%)
        elif abs(payment.amount - invoice.balance) / invoice.balance < 0.05:
            confidence = 0.85
        # Reference number contains invoice number
        elif invoice.invoice_number.replace("-", "").replace(
            "INV", ""
        ) in payment.reference.replace("-", ""):
            confidence = 0.9

        # Reduce confidence for very old invoices
        if invoice.days_outstanding > 90:
            confidence *= 0.9

        return round(confidence, 2)

    def _apply_payment_matches(self, matches: list[PaymentMatch]) -> None:
        """Apply payment matches to invoice balances"""
        for match in matches:
            for invoice in self.sample_invoices:
                if invoice.invoice_id == match.invoice_id:
                    invoice.balance = max(0, invoice.balance - match.amount_applied)
                    break

    def _generate_processing_notes(
        self, payment: PaymentEntry, matches: list[PaymentMatch], remaining: float
    ) -> list[str]:
        """Generate processing notes based on results"""
        notes = []

        if matches:
            notes.append(f"Successfully matched {len(matches)} invoice(s)")
            total_applied = sum(m.amount_applied for m in matches)
            notes.append(f"Applied ${total_applied:,.2f} to open invoices")

        if remaining > 0:
            notes.append(f"Remaining unapplied amount: ${remaining:,.2f}")
            notes.append("Manual review required for remaining balance")

        # Add method-specific notes
        if payment.payment_method.value == "ach":
            notes.append("ACH payment processed with standard clearing time")
        elif payment.payment_method.value == "wire":
            notes.append("Wire transfer - funds available immediately")
        elif payment.payment_method.value == "check":
            notes.append("Check payment - subject to clearing period")

        return notes


class DataPipelineService(DemoServiceBase):
    """Service for data pipeline demo"""

    def extract_data(
        self, session_id: str, params: DataExtractionParams
    ) -> PipelineResult:
        """Extract data from NetSuite based on parameters"""
        session = self.get_session(session_id)
        if not session:
            raise ValueError("Invalid session")

        self.update_session_status(session_id, DemoStatus.RUNNING)

        # Simulate data extraction
        records = self._generate_sample_records(params)

        # Process records
        processed_count = len(records)
        failed_count = random.randint(
            0, max(1, len(records) // 20)
        )  # 0-5% failure rate
        success_rate = (
            (processed_count - failed_count) / processed_count
            if processed_count > 0
            else 0
        )

        result = PipelineResult(
            batch_id=f"BATCH-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            total_records=len(records),
            processed_records=processed_count - failed_count,
            failed_records=failed_count,
            processing_time_ms=random.randint(1500, 5000),
            errors=self._generate_sample_errors(failed_count),
            success_rate=round(success_rate, 3),
        )

        self.update_session_status(
            session_id,
            DemoStatus.COMPLETED,
            {
                "extraction_result": result.model_dump(),
                "sample_records": [
                    r.model_dump() for r in records[:5]
                ],  # Show first 5 records
            },
        )

        return result

    def _generate_sample_records(
        self, params: DataExtractionParams
    ) -> list[DataRecord]:
        """Generate sample data records based on extraction parameters"""
        records = []
        record_count = random.randint(50, 500)  # Simulate variable data volume

        for i in range(record_count):
            # Generate realistic data based on source type
            data = self._generate_record_data(params.source.value, i)

            record = DataRecord(
                record_id=f"REC-{i + 1:06d}",
                source_id=f"{params.source.value.upper()}-{i + 1}",
                record_type=params.source.value,
                data=data,
            )
            records.append(record)

        return records

    def _generate_record_data(self, source_type: str, index: int) -> dict[str, Any]:
        """Generate realistic record data based on source type"""
        base_date = datetime.now() - timedelta(days=random.randint(1, 30))

        if source_type == "netsuite_payments":
            return {
                "payment_id": f"PAY-{index + 1:06d}",
                "customer_id": f"CUST-{random.randint(1, 100):03d}",
                "amount": round(random.uniform(1000, 50000), 2),
                "payment_date": base_date.isoformat(),
                "payment_method": random.choice(["ACH", "Wire", "Check"]),
                "reference": f"REF-{random.randint(100000, 999999)}",
            }
        elif source_type == "netsuite_invoices":
            return {
                "invoice_id": f"INV-{index + 1:06d}",
                "customer_id": f"CUST-{random.randint(1, 100):03d}",
                "amount": round(random.uniform(5000, 100000), 2),
                "invoice_date": base_date.isoformat(),
                "due_date": (base_date + timedelta(days=30)).isoformat(),
                "status": random.choice(["Open", "Paid", "Overdue"]),
            }
        else:
            return {
                "id": f"ID-{index + 1:06d}",
                "date": base_date.isoformat(),
                "amount": round(random.uniform(1000, 10000), 2),
                "status": "Active",
            }

    def _generate_sample_errors(self, count: int) -> list[str]:
        """Generate sample error messages"""
        error_types = [
            "Invalid date format in field 'transaction_date'",
            "Missing required field 'customer_id'",
            "Amount exceeds maximum allowed value",
            "Duplicate record detected",
            "Customer ID not found in target system",
            "Currency code validation failed",
        ]

        return random.sample(error_types, min(count, len(error_types)))


class DashboardService(DemoServiceBase):
    """Service for dashboard demo"""

    def generate_dashboard_data(
        self, session_id: str, period: str = "current_month"
    ) -> DashboardData:
        """Generate comprehensive dashboard data"""
        session = self.get_session(session_id)
        if not session:
            raise ValueError("Invalid session")

        self.update_session_status(session_id, DemoStatus.RUNNING)

        # Generate KPIs
        kpis = self._generate_kpis(period)

        # Generate revenue data
        revenue_records = self._generate_revenue_records()

        # Generate chart data
        chart_data = self._generate_chart_data(period)

        dashboard_data = DashboardData(
            kpis=kpis,
            revenue_by_customer=revenue_records,
            chart_data=chart_data,
            filters={"period": period, "currency": "USD"},
        )

        self.update_session_status(
            session_id,
            DemoStatus.COMPLETED,
            {"dashboard_data": dashboard_data.model_dump()},
        )

        return dashboard_data

    def _generate_kpis(self, period: str) -> list[KPIMetric]:
        """Generate realistic KPI metrics"""
        base_revenue = 2500000 if period == "current_month" else 8500000

        return [
            KPIMetric(
                name="Total Revenue",
                value=base_revenue,
                unit="$",
                change_percent=15.2,
                trend="up",
                target=base_revenue * 0.9,
            ),
            KPIMetric(
                name="Gross Margin",
                value=40.5,
                unit="%",
                change_percent=2.1,
                trend="up",
                target=38.0,
            ),
            KPIMetric(
                name="Customer Count",
                value=125,
                unit="",
                change_percent=-3.2,
                trend="down",
                target=130,
            ),
            KPIMetric(
                name="Average Deal Size",
                value=20000,
                unit="$",
                change_percent=8.7,
                trend="up",
                target=18000,
            ),
            KPIMetric(
                name="Churn Rate",
                value=5.2,
                unit="%",
                change_percent=-12.5,
                trend="down",
                target=7.0,
            ),
        ]

    def _generate_revenue_records(self) -> list[RevenueRecord]:
        """Generate customer revenue records"""
        customers = [
            "Enterprise Corp",
            "TechStart Inc",
            "Global Industries",
            "Retail Partners",
            "Manufacturing Co",
            "Finance Solutions",
            "Healthcare Systems",
            "Education Group",
            "Transport LLC",
            "Energy Services",
        ]

        records = []
        for i, customer in enumerate(customers):
            current_revenue = random.uniform(50000, 300000)
            previous_revenue = current_revenue * random.uniform(0.8, 1.2)
            ytd_revenue = current_revenue * random.uniform(8, 12)
            growth_rate = (current_revenue - previous_revenue) / previous_revenue

            record = RevenueRecord(
                customer_id=f"CUST-{i + 1:03d}",
                customer_name=customer,
                current_month=round(current_revenue, 2),
                previous_month=round(previous_revenue, 2),
                ytd_revenue=round(ytd_revenue, 2),
                growth_rate=round(growth_rate, 3),
                churn_risk=random.choice(["low", "medium", "high"]),
            )
            records.append(record)

        return records

    def _generate_chart_data(self, period: str) -> dict[str, Any]:
        """Generate chart data for visualizations"""
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

        return {
            "revenue_trend": {
                "labels": months,
                "data": [random.randint(180000, 220000) for _ in months],
            },
            "margin_trend": {
                "labels": months,
                "data": [round(random.uniform(38, 42), 1) for _ in months],
            },
            "customer_distribution": {
                "labels": ["Enterprise", "Mid-Market", "SMB"],
                "data": [45, 35, 20],
            },
        }


class CollectionsService(DemoServiceBase):
    """Service for collections demo"""

    def generate_collections_data(self, session_id: str) -> dict[str, Any]:
        """Generate comprehensive collections dashboard data"""
        session = self.get_session(session_id)
        if not session:
            raise ValueError("Invalid session")

        self.update_session_status(session_id, DemoStatus.RUNNING)

        data = {
            "dso_metrics": self._generate_dso_metrics(),
            "collector_performance": self._generate_collector_metrics(),
            "aging_analysis": self._generate_aging_buckets(),
            "customer_targets": self._generate_customer_targets(),
        }

        self.update_session_status(
            session_id, DemoStatus.COMPLETED, {"collections_data": data}
        )

        return data

    def _generate_dso_metrics(self) -> dict[str, Any]:
        """Generate DSO (Days Sales Outstanding) metrics"""
        return {
            "current_dso": 42.5,
            "target_dso": 35.0,
            "previous_month_dso": 45.2,
            "industry_benchmark": 38.0,
            "trend": "improving",
        }

    def _generate_collector_metrics(self) -> list[CollectorMetric]:
        """Generate collector performance metrics"""
        collectors = [
            "Sarah Johnson",
            "Mike Chen",
            "Lisa Rodriguez",
            "David Thompson",
            "Anna Williams",
        ]

        metrics = []
        for i, name in enumerate(collectors):
            metric = CollectorMetric(
                collector_id=f"COL-{i + 1:03d}",
                collector_name=name,
                collections_mtd=random.uniform(80000, 150000),
                target_mtd=100000,
                success_rate=random.uniform(0.6, 0.8),
                accounts_assigned=random.randint(35, 60),
                calls_made=random.randint(80, 120),
                emails_sent=random.randint(150, 200),
                meetings_held=random.randint(8, 15),
                performance_rank=i + 1,
            )
            metrics.append(metric)

        return sorted(metrics, key=lambda x: x.collections_mtd, reverse=True)

    def _generate_aging_buckets(self) -> list[AgingBucket]:
        """Generate AR aging analysis"""
        return [
            AgingBucket(
                bucket_name="Current",
                days_range="0-30 days",
                amount=850000.00,
                count=125,
                percentage=56.7,
            ),
            AgingBucket(
                bucket_name="30 Days",
                days_range="31-60 days",
                amount=320000.00,
                count=48,
                percentage=21.3,
            ),
            AgingBucket(
                bucket_name="60 Days",
                days_range="61-90 days",
                amount=180000.00,
                count=28,
                percentage=12.0,
            ),
            AgingBucket(
                bucket_name="90+ Days",
                days_range="90+ days",
                amount=150000.00,
                count=22,
                percentage=10.0,
            ),
        ]

    def _generate_customer_targets(self) -> list[CustomerTarget]:
        """Generate priority customer target list"""
        customers = [
            "ABC Manufacturing",
            "XYZ Retail Corp",
            "Global Tech Solutions",
            "Premier Services Inc",
            "Advanced Systems LLC",
        ]

        targets = []
        for i, customer in enumerate(customers):
            target = CustomerTarget(
                customer_id=f"CUST-{i + 1:03d}",
                customer_name=customer,
                total_outstanding=random.uniform(25000, 100000),
                days_past_due=random.randint(35, 120),
                risk_score=random.choice(["high", "medium", "low"]),
                priority_rank=i + 1,
                last_contact=datetime.now() - timedelta(days=random.randint(1, 14)),
                next_action=random.choice(
                    [
                        "phone_call",
                        "email_follow_up",
                        "meeting_scheduled",
                        "payment_plan",
                    ]
                ),
                assigned_collector=f"COL-{random.randint(1, 5):03d}",
                payment_promise={
                    "amount": random.uniform(5000, 25000),
                    "promise_date": (
                        datetime.now() + timedelta(days=random.randint(1, 30))
                    ).isoformat(),
                    "status": random.choice(["pending", "confirmed", "broken"]),
                }
                if random.random() > 0.3
                else None,
            )
            targets.append(target)

        return targets


# Global service instances
payment_service = PaymentProcessingService()
pipeline_service = DataPipelineService()
dashboard_service = DashboardService()
collections_service = CollectionsService()
