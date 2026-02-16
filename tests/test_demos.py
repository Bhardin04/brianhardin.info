"""Tests for demo endpoints and demo services."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.middleware import limiter
from app.models.demo import DemoType, PaymentEntry, PaymentMethod
from app.services.demo import (
    CollectionsService,
    DashboardService,
    DataPipelineService,
    PaymentProcessingService,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def _reset_limiter():
    """Reset rate limiter state between tests."""
    limiter._limiter.storage.reset()
    yield


# ---- Demo Page Tests ----


class TestDemoPages:
    """Test that demo HTML pages render correctly."""

    def test_demos_index(self):
        response = client.get("/demos/")
        assert response.status_code == 200

    def test_payment_processing_page(self):
        response = client.get("/demos/payment-processing")
        assert response.status_code == 200

    def test_data_pipeline_page(self):
        response = client.get("/demos/data-pipeline")
        assert response.status_code == 200

    def test_sales_dashboard_page(self):
        response = client.get("/demos/sales-dashboard")
        assert response.status_code == 200

    def test_collections_dashboard_page(self):
        response = client.get("/demos/collections-dashboard")
        assert response.status_code == 200

    def test_automation_suite_page(self):
        response = client.get("/demos/automation-suite")
        assert response.status_code == 200


# ---- Payment Processing API Tests ----


class TestPaymentProcessingAPI:
    """Test payment processing demo API endpoints."""

    def test_create_payment_session(self):
        response = client.post("/demos/api/payment-processing/session")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "session_id" in data["data"]
        assert "open_invoices" in data["data"]
        assert "customers" in data["data"]

    def test_process_payment(self):
        # Create session first
        session_resp = client.post("/demos/api/payment-processing/session")
        session_id = session_resp.json()["data"]["session_id"]
        invoices = session_resp.json()["data"]["open_invoices"]

        # Process a payment
        customer_id = invoices[0]["customer_id"] if invoices else "CUST001"
        payment_data = {
            "session_id": session_id,
            "payment": {
                "customer_id": customer_id,
                "amount": 10000.00,
                "payment_method": "ach",
                "reference": "REF-12345",
            },
        }
        response = client.post(
            "/demos/api/payment-processing/process", json=payment_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["status"] in ("matched", "partial", "exception")

    def test_process_payment_missing_session(self):
        payment_data = {
            "payment": {
                "customer_id": "CUST001",
                "amount": 100.0,
                "payment_method": "ach",
                "reference": "REF-001",
            },
        }
        response = client.post(
            "/demos/api/payment-processing/process", json=payment_data
        )
        assert response.status_code == 400

    def test_get_customer_invoices(self):
        response = client.get("/demos/api/payment-processing/invoices/CUST001")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "invoices" in data["data"]


# ---- Data Pipeline API Tests ----


class TestDataPipelineAPI:
    """Test data pipeline demo API endpoints."""

    def test_create_pipeline_session(self):
        response = client.post("/demos/api/data-pipeline/session")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "session_id" in data["data"]
        assert "available_sources" in data["data"]

    def test_extract_pipeline_data(self):
        # Create session first
        session_resp = client.post("/demos/api/data-pipeline/session")
        session_id = session_resp.json()["data"]["session_id"]

        extraction_request = {
            "session_id": session_id,
            "params": {
                "source": "netsuite_payments",
                "start_date": "2024-01-01T00:00:00",
                "end_date": "2024-12-31T23:59:59",
            },
        }
        response = client.post(
            "/demos/api/data-pipeline/extract", json=extraction_request
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["total_records"] > 0
        assert data["data"]["success_rate"] > 0

    def test_extract_pipeline_data_missing_session(self):
        extraction_request = {
            "params": {
                "source": "netsuite_payments",
                "start_date": "2024-01-01T00:00:00",
                "end_date": "2024-12-31T23:59:59",
            },
        }
        response = client.post(
            "/demos/api/data-pipeline/extract", json=extraction_request
        )
        assert response.status_code == 400


# ---- Dashboard API Tests ----


class TestDashboardAPI:
    """Test dashboard demo API endpoints."""

    def test_create_dashboard_session(self):
        response = client.post("/demos/api/dashboard/session")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "session_id" in data["data"]

    def test_get_dashboard_data(self):
        # Create session
        session_resp = client.post("/demos/api/dashboard/session")
        session_id = session_resp.json()["data"]["session_id"]

        request_data = {
            "session_id": session_id,
            "period": "current_month",
        }
        response = client.post("/demos/api/dashboard/data", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "kpis" in data["data"]
        assert "revenue_by_customer" in data["data"]
        assert "chart_data" in data["data"]

    def test_get_dashboard_data_missing_session(self):
        response = client.post(
            "/demos/api/dashboard/data", json={"period": "current_month"}
        )
        assert response.status_code == 400


# ---- Collections API Tests ----


class TestCollectionsAPI:
    """Test collections demo API endpoints."""

    def test_create_collections_session(self):
        response = client.post("/demos/api/collections/session")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "session_id" in data["data"]

    def test_get_collections_data(self):
        # Create session
        session_resp = client.post("/demos/api/collections/session")
        session_id = session_resp.json()["data"]["session_id"]

        request_data = {"session_id": session_id}
        response = client.post("/demos/api/collections/data", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_collections_data_missing_session(self):
        response = client.post("/demos/api/collections/data", json={})
        assert response.status_code == 400


# ---- Demo Service Unit Tests ----


class TestPaymentProcessingService:
    """Test PaymentProcessingService business logic."""

    def setup_method(self):
        self.service = PaymentProcessingService()

    def test_create_session(self):
        session = self.service.create_session(DemoType.PAYMENT_PROCESSING)
        assert session.session_id
        assert session.demo_type == DemoType.PAYMENT_PROCESSING

    def test_get_all_open_invoices(self):
        invoices = self.service.get_all_open_invoices()
        assert len(invoices) > 0
        for inv in invoices:
            assert inv.balance > 0

    def test_get_customer_invoices(self):
        invoices = self.service.get_customer_invoices("CUST001")
        for inv in invoices:
            assert inv.customer_id == "CUST001"

    def test_process_payment_exact_match(self):
        session = self.service.create_session(DemoType.PAYMENT_PROCESSING)
        invoices = self.service.get_customer_invoices("CUST001")
        if invoices:
            payment = PaymentEntry(
                customer_id="CUST001",
                amount=invoices[0].balance,
                payment_method=PaymentMethod.ACH,
                reference="REF-TEST-001",
            )
            result = self.service.process_payment(session.session_id, payment)
            assert result.payment_id.startswith("PAY-")
            assert result.status in ("matched", "partial", "exception")

    def test_process_payment_invalid_session(self):
        payment = PaymentEntry(
            customer_id="CUST001",
            amount=100.0,
            payment_method=PaymentMethod.ACH,
            reference="REF-TEST",
        )
        with pytest.raises(ValueError, match="Invalid session"):
            self.service.process_payment("nonexistent", payment)

    def test_match_confidence_exact_amount(self):
        invoices = self.service.get_all_open_invoices()
        if invoices:
            inv = invoices[0]
            payment = PaymentEntry(
                customer_id=inv.customer_id,
                amount=inv.balance,
                payment_method=PaymentMethod.WIRE,
                reference="REF-EXACT",
            )
            confidence = self.service._calculate_match_confidence(payment, inv)
            assert confidence >= 0.9

    def test_session_expiration(self):
        """Test that expired sessions are cleaned up."""
        from datetime import datetime, timedelta

        session = self.service.create_session(DemoType.PAYMENT_PROCESSING)
        # Manually expire the session
        session.created_at = datetime.now() - timedelta(
            seconds=self.service.SESSION_TTL_SECONDS + 1
        )
        result = self.service.get_session(session.session_id)
        assert result is None

    def test_max_sessions_limit(self):
        """Test that session creation is limited."""
        self.service.MAX_SESSIONS = 3
        for _ in range(3):
            self.service.create_session(DemoType.PAYMENT_PROCESSING)
        with pytest.raises(ValueError, match="Maximum number"):
            self.service.create_session(DemoType.PAYMENT_PROCESSING)


class TestDataPipelineService:
    """Test DataPipelineService business logic."""

    def setup_method(self):
        self.service = DataPipelineService()

    def test_extract_data(self):
        from datetime import datetime

        from app.models.demo import DataExtractionParams, DataSource

        session = self.service.create_session(DemoType.DATA_PIPELINE)
        params = DataExtractionParams(
            source=DataSource.NETSUITE_PAYMENTS,
            start_date=datetime(2024, 1, 1),
            end_date=datetime(2024, 12, 31),
        )
        result = self.service.extract_data(session.session_id, params)
        assert result.batch_id.startswith("BATCH-")
        assert result.total_records > 0
        assert result.success_rate > 0
        assert result.processed_records + result.failed_records == result.total_records

    def test_extract_data_invalid_session(self):
        from datetime import datetime

        from app.models.demo import DataExtractionParams, DataSource

        params = DataExtractionParams(
            source=DataSource.NETSUITE_INVOICES,
            start_date=datetime(2024, 1, 1),
            end_date=datetime(2024, 12, 31),
        )
        with pytest.raises(ValueError, match="Invalid session"):
            self.service.extract_data("nonexistent", params)


class TestDashboardService:
    """Test DashboardService business logic."""

    def setup_method(self):
        self.service = DashboardService()

    def test_generate_dashboard_data(self):
        session = self.service.create_session(DemoType.SALES_DASHBOARD)
        data = self.service.generate_dashboard_data(session.session_id)
        assert len(data.kpis) == 5
        assert len(data.revenue_by_customer) == 10
        assert "revenue_trend" in data.chart_data

    def test_generate_dashboard_data_quarterly(self):
        session = self.service.create_session(DemoType.SALES_DASHBOARD)
        data = self.service.generate_dashboard_data(
            session.session_id, period="current_quarter"
        )
        assert len(data.kpis) == 5

    def test_generate_dashboard_invalid_session(self):
        with pytest.raises(ValueError, match="Invalid session"):
            self.service.generate_dashboard_data("nonexistent")


class TestCollectionsService:
    """Test CollectionsService business logic."""

    def setup_method(self):
        self.service = CollectionsService()

    def test_generate_collections_data(self):
        session = self.service.create_session(DemoType.COLLECTIONS_DASHBOARD)
        data = self.service.generate_collections_data(session.session_id)
        assert "dso_metrics" in data
        assert "collector_performance" in data
        assert "aging_analysis" in data
        assert "customer_targets" in data

    def test_dso_metrics(self):
        metrics = self.service._generate_dso_metrics()
        assert metrics["current_dso"] > 0
        assert metrics["target_dso"] > 0

    def test_aging_buckets(self):
        buckets = self.service._generate_aging_buckets()
        assert len(buckets) == 4
        total_pct = sum(b.percentage for b in buckets)
        assert abs(total_pct - 100.0) < 0.1

    def test_generate_collections_invalid_session(self):
        with pytest.raises(ValueError, match="Invalid session"):
            self.service.generate_collections_data("nonexistent")


# ---- WebSocket Tests ----


class TestWebSocket:
    """Test WebSocket connections."""

    def test_websocket_connect_and_ping(self):
        with client.websocket_connect(
            "/demos/ws/payment_processing/test-session"
        ) as websocket:
            # Should receive connection established message
            data = websocket.receive_json()
            assert data["type"] == "connection_established"
            assert data["session_id"] == "test-session"
            assert data["demo_type"] == "payment_processing"

            # Test ping/pong
            websocket.send_json({"type": "ping"})
            pong = websocket.receive_json()
            assert pong["type"] == "pong"

    def test_websocket_echo(self):
        with client.websocket_connect(
            "/demos/ws/sales_dashboard/test-session-2"
        ) as websocket:
            # Consume connection message
            websocket.receive_json()

            # Send unknown message type - should echo
            websocket.send_json({"type": "unknown", "data": "test"})
            echo = websocket.receive_json()
            assert echo["type"] == "echo"
            assert echo["original_message"]["data"] == "test"
