"""Tests for demo endpoints and services."""

from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.demo import DemoType, PaymentEntry, PaymentMethod
from app.services.demo import (
    CollectionsService,
    DashboardService,
    DataPipelineService,
    PaymentProcessingService,
)

client = TestClient(app)


# ── Demo Page Tests ──────────────────────────────────────────────────


class TestDemoPages:
    """Test demo HTML page rendering."""

    def test_demos_index(self) -> None:
        response = client.get("/demos/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_payment_processing_page(self) -> None:
        response = client.get("/demos/payment-processing")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_data_pipeline_page(self) -> None:
        response = client.get("/demos/data-pipeline")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_sales_dashboard_page(self) -> None:
        response = client.get("/demos/sales-dashboard")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_collections_dashboard_page(self) -> None:
        response = client.get("/demos/collections-dashboard")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_automation_suite_page(self) -> None:
        response = client.get("/demos/automation-suite")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


# ── Payment Processing API Tests ─────────────────────────────────────


class TestPaymentProcessingAPI:
    """Test payment processing API endpoints."""

    def test_create_payment_session(self) -> None:
        response = client.post("/demos/api/payment-processing/session")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "session_id" in data["data"]
        assert "open_invoices" in data["data"]

    def test_get_customer_invoices(self) -> None:
        response = client.get("/demos/api/payment-processing/invoices/CUST001")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "invoices" in data["data"]

    def test_get_customer_invoices_unknown(self) -> None:
        response = client.get("/demos/api/payment-processing/invoices/UNKNOWN")
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["invoices"] == []

    def test_process_payment(self) -> None:
        # First create a session
        session_resp = client.post("/demos/api/payment-processing/session")
        session_id = session_resp.json()["data"]["session_id"]

        # Process a payment
        response = client.post(
            "/demos/api/payment-processing/process",
            json={
                "session_id": session_id,
                "payment": {
                    "customer_id": "CUST001",
                    "amount": 10000.00,
                    "payment_method": "ach",
                    "reference": "REF-12345",
                },
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


# ── Data Pipeline API Tests ──────────────────────────────────────────


class TestDataPipelineAPI:
    """Test data pipeline API endpoints."""

    def test_create_pipeline_session(self) -> None:
        response = client.post("/demos/api/data-pipeline/session")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "available_sources" in data["data"]

    def test_extract_pipeline_data(self) -> None:
        session_resp = client.post("/demos/api/data-pipeline/session")
        session_id = session_resp.json()["data"]["session_id"]

        response = client.post(
            "/demos/api/data-pipeline/extract",
            json={
                "session_id": session_id,
                "params": {
                    "source": "netsuite_payments",
                    "start_date": "2024-01-01T00:00:00",
                    "end_date": "2024-12-31T00:00:00",
                    "output_format": "json",
                },
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_extract_without_session(self) -> None:
        response = client.post(
            "/demos/api/data-pipeline/extract",
            json={
                "params": {
                    "source": "netsuite_payments",
                    "start_date": "2024-01-01T00:00:00",
                    "end_date": "2024-12-31T00:00:00",
                    "output_format": "json",
                },
            },
        )
        assert response.status_code == 400


# ── Dashboard API Tests ──────────────────────────────────────────────


class TestDashboardAPI:
    """Test dashboard API endpoints."""

    def test_create_dashboard_session(self) -> None:
        response = client.post("/demos/api/dashboard/session")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "available_periods" in data["data"]

    def test_get_dashboard_data(self) -> None:
        session_resp = client.post("/demos/api/dashboard/session")
        session_id = session_resp.json()["data"]["session_id"]

        response = client.post(
            "/demos/api/dashboard/data",
            json={"session_id": session_id, "period": "current_month"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_dashboard_without_session(self) -> None:
        response = client.post(
            "/demos/api/dashboard/data",
            json={"period": "current_month"},
        )
        assert response.status_code == 400


# ── Collections API Tests ────────────────────────────────────────────


class TestCollectionsAPI:
    """Test collections API endpoints."""

    def test_create_collections_session(self) -> None:
        response = client.post("/demos/api/collections/session")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_collections_data(self) -> None:
        session_resp = client.post("/demos/api/collections/session")
        session_id = session_resp.json()["data"]["session_id"]

        response = client.post(
            "/demos/api/collections/data",
            json={"session_id": session_id},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_collections_without_session(self) -> None:
        response = client.post(
            "/demos/api/collections/data",
            json={},
        )
        assert response.status_code == 400


# ── Payment Processing Service Tests ─────────────────────────────────


class TestPaymentProcessingService:
    """Test PaymentProcessingService business logic."""

    def setup_method(self) -> None:
        self.service = PaymentProcessingService()

    def test_create_session(self) -> None:
        session = self.service.create_session(DemoType.PAYMENT_PROCESSING)
        assert session.session_id
        assert session.demo_type == DemoType.PAYMENT_PROCESSING

    def test_get_session(self) -> None:
        session = self.service.create_session(DemoType.PAYMENT_PROCESSING)
        retrieved = self.service.get_session(session.session_id)
        assert retrieved is not None
        assert retrieved.session_id == session.session_id

    def test_get_nonexistent_session(self) -> None:
        assert self.service.get_session("nonexistent") is None

    def test_get_all_open_invoices(self) -> None:
        invoices = self.service.get_all_open_invoices()
        assert len(invoices) > 0
        for inv in invoices:
            assert inv.balance > 0

    def test_process_payment(self) -> None:
        session = self.service.create_session(DemoType.PAYMENT_PROCESSING)
        payment = PaymentEntry(
            customer_id="CUST001",
            amount=10000.00,
            payment_method=PaymentMethod.ACH,
            reference="REF-TEST-001",
        )
        result = self.service.process_payment(session.session_id, payment)
        assert result.payment_id
        assert result.status in ("matched", "partial", "exception")

    def test_session_expiration(self) -> None:
        session = self.service.create_session(DemoType.PAYMENT_PROCESSING)
        # Manually set created_at to past TTL
        session.created_at = datetime.now() - timedelta(
            seconds=self.service.SESSION_TTL_SECONDS + 1
        )
        assert self.service.get_session(session.session_id) is None

    def test_max_sessions_limit(self) -> None:
        for _ in range(self.service.MAX_SESSIONS):
            self.service.create_session(DemoType.PAYMENT_PROCESSING)
        with pytest.raises(ValueError, match="Maximum number"):
            self.service.create_session(DemoType.PAYMENT_PROCESSING)


# ── Data Pipeline Service Tests ──────────────────────────────────────


class TestDataPipelineService:
    """Test DataPipelineService business logic."""

    def setup_method(self) -> None:
        self.service = DataPipelineService()

    def test_create_session(self) -> None:
        session = self.service.create_session(DemoType.DATA_PIPELINE)
        assert session.session_id
        assert session.demo_type == DemoType.DATA_PIPELINE

    def test_extract_data(self) -> None:
        from app.models.demo import DataExtractionParams

        session = self.service.create_session(DemoType.DATA_PIPELINE)
        params = DataExtractionParams(
            source="netsuite_payments",
            start_date="2024-01-01T00:00:00",
            end_date="2024-12-31T00:00:00",
            output_format="json",
        )
        result = self.service.extract_data(session.session_id, params)
        assert result.batch_id
        assert result.total_records > 0
        assert result.success_rate > 0


# ── Dashboard Service Tests ──────────────────────────────────────────


class TestDashboardService:
    """Test DashboardService business logic."""

    def setup_method(self) -> None:
        self.service = DashboardService()

    def test_create_session(self) -> None:
        session = self.service.create_session(DemoType.SALES_DASHBOARD)
        assert session.session_id

    def test_generate_dashboard_data(self) -> None:
        session = self.service.create_session(DemoType.SALES_DASHBOARD)
        data = self.service.generate_dashboard_data(session.session_id)
        assert len(data.kpis) > 0
        assert len(data.revenue_by_customer) > 0
        assert data.chart_data

    def test_generate_dashboard_data_quarterly(self) -> None:
        session = self.service.create_session(DemoType.SALES_DASHBOARD)
        data = self.service.generate_dashboard_data(
            session.session_id, period="current_quarter"
        )
        assert data.filters["period"] == "current_quarter"


# ── Collections Service Tests ────────────────────────────────────────


class TestCollectionsService:
    """Test CollectionsService business logic."""

    def setup_method(self) -> None:
        self.service = CollectionsService()

    def test_create_session(self) -> None:
        session = self.service.create_session(DemoType.COLLECTIONS_DASHBOARD)
        assert session.session_id

    def test_generate_collections_data(self) -> None:
        session = self.service.create_session(DemoType.COLLECTIONS_DASHBOARD)
        data = self.service.generate_collections_data(session.session_id)
        assert "dso_metrics" in data
        assert "collector_performance" in data
        assert "aging_analysis" in data
        assert "customer_targets" in data

    def test_dso_metrics(self) -> None:
        session = self.service.create_session(DemoType.COLLECTIONS_DASHBOARD)
        data = self.service.generate_collections_data(session.session_id)
        dso = data["dso_metrics"]
        assert "current_dso" in dso
        assert "target_dso" in dso

    def test_aging_buckets(self) -> None:
        session = self.service.create_session(DemoType.COLLECTIONS_DASHBOARD)
        data = self.service.generate_collections_data(session.session_id)
        aging = data["aging_analysis"]
        assert len(aging) == 4  # Current, 30, 60, 90+ days


# ── WebSocket Tests ──────────────────────────────────────────────────


class TestWebSocket:
    """Test WebSocket connection handling."""

    def test_websocket_connect_and_ping(self) -> None:
        with client.websocket_connect(
            "/demos/ws/payment_processing/test-session"
        ) as ws:
            # Should receive connection established message
            data = ws.receive_json()
            assert data["type"] == "connection_established"

            # Send ping
            ws.send_json({"type": "ping"})
            pong = ws.receive_json()
            assert pong["type"] == "pong"

    def test_websocket_echo(self) -> None:
        with client.websocket_connect(
            "/demos/ws/payment_processing/test-session"
        ) as ws:
            # Consume connection message
            ws.receive_json()

            # Send unknown message type - should echo
            ws.send_json({"type": "unknown", "data": "test"})
            echo = ws.receive_json()
            assert echo["type"] == "echo"
            assert echo["original_message"]["data"] == "test"
