"""
Demo models for interactive project demonstrations.
"""
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class DemoStatus(str, Enum):
    """Demo execution status"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"


class DemoType(str, Enum):
    """Types of interactive demos"""
    PAYMENT_PROCESSING = "payment_processing"
    DATA_PIPELINE = "data_pipeline"
    SALES_DASHBOARD = "sales_dashboard"
    COLLECTIONS_DASHBOARD = "collections_dashboard"
    AUTOMATION_SUITE = "automation_suite"


class DemoSession(BaseModel):
    """Demo session tracking"""
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    demo_type: DemoType
    status: DemoStatus = DemoStatus.IDLE
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    data: dict[str, Any] = Field(default_factory=dict)

    def update_status(self, status: DemoStatus, data: dict[str, Any] = None):
        """Update session status and data"""
        self.status = status
        self.updated_at = datetime.now()
        if data:
            self.data.update(data)


# Payment Processing Demo Models
class PaymentMethod(str, Enum):
    ACH = "ach"
    WIRE = "wire"
    CHECK = "check"


class PaymentEntry(BaseModel):
    """Payment entry form data"""
    customer_id: str
    amount: float = Field(gt=0, description="Payment amount must be positive")
    payment_method: PaymentMethod
    reference: str = Field(min_length=1, max_length=50)
    payment_date: datetime = Field(default_factory=datetime.now)
    memo: str | None = Field(None, max_length=200)


class Invoice(BaseModel):
    """Open invoice in AR ledger"""
    invoice_id: str
    invoice_number: str
    customer_id: str
    customer_name: str
    invoice_date: datetime
    due_date: datetime
    amount: float
    balance: float
    days_outstanding: int

    @property
    def aging_bucket(self) -> str:
        """Get aging bucket for this invoice"""
        if self.days_outstanding <= 30:
            return "current"
        elif self.days_outstanding <= 60:
            return "30_days"
        elif self.days_outstanding <= 90:
            return "60_days"
        else:
            return "90_plus"


class PaymentMatch(BaseModel):
    """Payment to invoice matching result"""
    payment_id: str
    invoice_id: str
    amount_applied: float
    confidence_score: float = Field(ge=0, le=1)
    match_type: str  # "exact", "partial", "manual"


class PaymentProcessingResult(BaseModel):
    """Result of payment processing"""
    payment_id: str
    status: str  # "matched", "partial", "exception"
    matches: list[PaymentMatch]
    remaining_amount: float = 0
    processing_notes: list[str] = Field(default_factory=list)


# Data Pipeline Demo Models
class DataSource(str, Enum):
    NETSUITE_PAYMENTS = "netsuite_payments"
    NETSUITE_INVOICES = "netsuite_invoices"
    NETSUITE_CREDIT_MEMOS = "netsuite_credit_memos"
    NETSUITE_JOURNAL_ENTRIES = "netsuite_journal_entries"


class OutputFormat(str, Enum):
    XML = "xml"
    JSON = "json"


class DataExtractionParams(BaseModel):
    """Parameters for data extraction"""
    source: DataSource
    start_date: datetime
    end_date: datetime
    customer_filter: str | None = None
    amount_min: float | None = None
    amount_max: float | None = None
    output_format: OutputFormat = OutputFormat.XML


class DataRecord(BaseModel):
    """Generic data record structure"""
    record_id: str
    source_id: str
    record_type: str
    data: dict[str, Any]
    extracted_at: datetime = Field(default_factory=datetime.now)
    processed_at: datetime | None = None
    status: str = "extracted"  # extracted, transformed, validated, posted


class TransformationRule(BaseModel):
    """Data transformation rule"""
    source_field: str
    target_field: str
    transformation: str  # "direct", "format_date", "currency_format", etc.
    validation_rule: str | None = None


class PipelineResult(BaseModel):
    """Data pipeline processing result"""
    batch_id: str
    total_records: int
    processed_records: int
    failed_records: int
    processing_time_ms: int
    errors: list[str] = Field(default_factory=list)
    success_rate: float


# Dashboard Demo Models
class KPIMetric(BaseModel):
    """Key Performance Indicator metric"""
    name: str
    value: float
    unit: str = ""
    change_percent: float | None = None
    trend: str = "neutral"  # "up", "down", "neutral"
    target: float | None = None


class RevenueRecord(BaseModel):
    """Customer revenue record"""
    customer_id: str
    customer_name: str
    current_month: float
    previous_month: float
    ytd_revenue: float
    growth_rate: float
    churn_risk: str = "low"  # "low", "medium", "high"


class DashboardData(BaseModel):
    """Dashboard visualization data"""
    kpis: list[KPIMetric]
    revenue_by_customer: list[RevenueRecord]
    chart_data: dict[str, Any]
    filters: dict[str, Any] = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=datetime.now)


# Collections Demo Models
class CollectorMetric(BaseModel):
    """Individual collector performance metrics"""
    collector_id: str
    collector_name: str
    collections_mtd: float
    target_mtd: float
    success_rate: float
    accounts_assigned: int
    calls_made: int
    emails_sent: int
    meetings_held: int
    performance_rank: int


class AgingBucket(BaseModel):
    """Aging analysis bucket"""
    bucket_name: str
    days_range: str
    amount: float
    count: int
    percentage: float


class CustomerTarget(BaseModel):
    """Customer in collections target list"""
    customer_id: str
    customer_name: str
    total_outstanding: float
    days_past_due: int
    risk_score: str
    priority_rank: int
    last_contact: datetime | None = None
    next_action: str
    assigned_collector: str
    payment_promise: dict[str, Any] | None = None


# Demo Response Models
class DemoResponse(BaseModel):
    """Generic demo API response"""
    success: bool
    data: Any = None
    message: str = ""
    session_id: str
    execution_time_ms: int = 0


class DemoError(BaseModel):
    """Demo error response"""
    error_type: str
    message: str
    details: dict[str, Any] | None = None
    session_id: str
