"""
Demo API endpoints for interactive project demonstrations.
"""
import logging
from typing import Any

from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.models.demo import (
    DataExtractionParams,
    DemoError,
    DemoResponse,
    DemoType,
    PaymentEntry,
)
from app.services.demo import (
    collections_service,
    dashboard_service,
    payment_service,
    pipeline_service,
)
from app.services.websocket import (
    connection_manager,
    realtime_simulator,
    websocket_service,
)

logger = logging.getLogger(__name__)
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def demos_index(request: Request):
    """Demo portal homepage"""
    return templates.TemplateResponse("demos/index.html", {"request": request})


@router.get("/payment-processing", response_class=HTMLResponse)
async def payment_demo_page(request: Request):
    """Payment processing demo page"""
    return templates.TemplateResponse("demos/payment_processing.html", {"request": request})


@router.get("/data-pipeline", response_class=HTMLResponse)
async def pipeline_demo_page(request: Request):
    """Data pipeline demo page"""
    return templates.TemplateResponse("demos/data_pipeline.html", {"request": request})


@router.get("/sales-dashboard", response_class=HTMLResponse)
async def dashboard_demo_page(request: Request):
    """Sales dashboard demo page"""
    return templates.TemplateResponse("demos/sales_dashboard.html", {"request": request})


@router.get("/collections-dashboard", response_class=HTMLResponse)
async def collections_demo_page(request: Request):
    """Collections dashboard demo page"""
    return templates.TemplateResponse("demos/collections_dashboard.html", {"request": request})


@router.get("/automation-suite", response_class=HTMLResponse)
async def automation_demo_page(request: Request):
    """Automation suite demo page"""
    return templates.TemplateResponse("demos/automation_suite.html", {"request": request})


# API Endpoints for Payment Processing Demo
@router.post("/api/payment-processing/session")
async def create_payment_session():
    """Create a new payment processing demo session"""
    try:
        session = payment_service.create_session(DemoType.PAYMENT_PROCESSING)

        # Get sample data for the session
        open_invoices = payment_service.get_all_open_invoices()

        return DemoResponse(
            success=True,
            data={
                "session_id": session.session_id,
                "open_invoices": [inv.dict() for inv in open_invoices[:10]],  # Limit for demo
                "customers": list({(inv.customer_id, inv.customer_name) for inv in open_invoices})
            },
            message="Payment processing session created successfully",
            session_id=session.session_id
        )
    except Exception as e:
        logger.error(f"Error creating payment session: {str(e)}")
        return JSONResponse(
            status_code=500,
            content=DemoError(
                error_type="session_creation_error",
                message="Failed to create payment processing session",
                session_id=""
            ).dict()
        )


@router.post("/api/payment-processing/process")
async def process_payment(payment_data: dict[str, Any]):
    """Process a payment entry"""
    try:
        session_id = payment_data.get("session_id")
        if not session_id:
            raise ValueError("Session ID required")

        # Create PaymentEntry from request data
        payment = PaymentEntry(**payment_data["payment"])

        # Process the payment
        result = payment_service.process_payment(session_id, payment)

        return DemoResponse(
            success=True,
            data=result.dict(),
            message=f"Payment processed successfully - Status: {result.status}",
            session_id=session_id,
            execution_time_ms=150  # Simulated processing time
        )

    except Exception as e:
        logger.error(f"Error processing payment: {str(e)}")
        return JSONResponse(
            status_code=400,
            content=DemoError(
                error_type="payment_processing_error",
                message=f"Payment processing failed: {str(e)}",
                session_id=payment_data.get("session_id", "")
            ).dict()
        )


@router.get("/api/payment-processing/invoices/{customer_id}")
async def get_customer_invoices(customer_id: str):
    """Get open invoices for a specific customer"""
    try:
        invoices = payment_service.get_customer_invoices(customer_id)

        return DemoResponse(
            success=True,
            data={"invoices": [inv.dict() for inv in invoices]},
            message=f"Found {len(invoices)} open invoices for customer",
            session_id=""
        )

    except Exception as e:
        logger.error(f"Error fetching customer invoices: {str(e)}")
        return JSONResponse(
            status_code=500,
            content=DemoError(
                error_type="data_fetch_error",
                message="Failed to fetch customer invoices",
                session_id=""
            ).dict()
        )


# API Endpoints for Data Pipeline Demo
@router.post("/api/data-pipeline/session")
async def create_pipeline_session():
    """Create a new data pipeline demo session"""
    try:
        session = pipeline_service.create_session(DemoType.DATA_PIPELINE)

        return DemoResponse(
            success=True,
            data={
                "session_id": session.session_id,
                "available_sources": [
                    {"value": "netsuite_payments", "label": "NetSuite Payments"},
                    {"value": "netsuite_invoices", "label": "NetSuite Invoices"},
                    {"value": "netsuite_credit_memos", "label": "NetSuite Credit Memos"},
                    {"value": "netsuite_journal_entries", "label": "NetSuite Journal Entries"}
                ],
                "output_formats": [
                    {"value": "xml", "label": "XML"},
                    {"value": "json", "label": "JSON"}
                ]
            },
            message="Data pipeline session created successfully",
            session_id=session.session_id
        )

    except Exception as e:
        logger.error(f"Error creating pipeline session: {str(e)}")
        return JSONResponse(
            status_code=500,
            content=DemoError(
                error_type="session_creation_error",
                message="Failed to create data pipeline session",
                session_id=""
            ).dict()
        )


@router.post("/api/data-pipeline/extract")
async def extract_pipeline_data(extraction_request: dict[str, Any]):
    """Extract data from NetSuite"""
    try:
        session_id = extraction_request.get("session_id")
        if not session_id:
            raise ValueError("Session ID required")

        # Create extraction parameters
        params = DataExtractionParams(**extraction_request["params"])

        # Extract data
        result = pipeline_service.extract_data(session_id, params)

        return DemoResponse(
            success=True,
            data=result.dict(),
            message=f"Extracted {result.processed_records} records successfully",
            session_id=session_id,
            execution_time_ms=result.processing_time_ms
        )

    except Exception as e:
        logger.error(f"Error extracting pipeline data: {str(e)}")
        return JSONResponse(
            status_code=400,
            content=DemoError(
                error_type="data_extraction_error",
                message=f"Data extraction failed: {str(e)}",
                session_id=extraction_request.get("session_id", "")
            ).dict()
        )


# API Endpoints for Dashboard Demo
@router.post("/api/dashboard/session")
async def create_dashboard_session():
    """Create a new dashboard demo session"""
    try:
        session = dashboard_service.create_session(DemoType.SALES_DASHBOARD)

        return DemoResponse(
            success=True,
            data={
                "session_id": session.session_id,
                "available_periods": [
                    {"value": "current_month", "label": "Current Month"},
                    {"value": "current_quarter", "label": "Current Quarter"},
                    {"value": "current_year", "label": "Current Year"}
                ]
            },
            message="Dashboard session created successfully",
            session_id=session.session_id
        )

    except Exception as e:
        logger.error(f"Error creating dashboard session: {str(e)}")
        return JSONResponse(
            status_code=500,
            content=DemoError(
                error_type="session_creation_error",
                message="Failed to create dashboard session",
                session_id=""
            ).dict()
        )


@router.post("/api/dashboard/data")
async def get_dashboard_data(request_data: dict[str, Any]):
    """Generate dashboard data"""
    try:
        session_id = request_data.get("session_id")
        period = request_data.get("period", "current_month")

        if not session_id:
            raise ValueError("Session ID required")

        # Generate dashboard data
        dashboard_data = dashboard_service.generate_dashboard_data(session_id, period)

        return DemoResponse(
            success=True,
            data=dashboard_data.dict(),
            message="Dashboard data generated successfully",
            session_id=session_id,
            execution_time_ms=250
        )

    except Exception as e:
        logger.error(f"Error generating dashboard data: {str(e)}")
        return JSONResponse(
            status_code=400,
            content=DemoError(
                error_type="dashboard_generation_error",
                message=f"Dashboard generation failed: {str(e)}",
                session_id=request_data.get("session_id", "")
            ).dict()
        )


# API Endpoints for Collections Demo
@router.post("/api/collections/session")
async def create_collections_session():
    """Create a new collections demo session"""
    try:
        session = collections_service.create_session(DemoType.COLLECTIONS_DASHBOARD)

        return DemoResponse(
            success=True,
            data={
                "session_id": session.session_id
            },
            message="Collections session created successfully",
            session_id=session.session_id
        )

    except Exception as e:
        logger.error(f"Error creating collections session: {str(e)}")
        return JSONResponse(
            status_code=500,
            content=DemoError(
                error_type="session_creation_error",
                message="Failed to create collections session",
                session_id=""
            ).dict()
        )


@router.post("/api/collections/data")
async def get_collections_data(request_data: dict[str, Any]):
    """Generate collections dashboard data"""
    try:
        session_id = request_data.get("session_id")

        if not session_id:
            raise ValueError("Session ID required")

        # Generate collections data
        collections_data = collections_service.generate_collections_data(session_id)

        return DemoResponse(
            success=True,
            data=collections_data,
            message="Collections data generated successfully",
            session_id=session_id,
            execution_time_ms=180
        )

    except Exception as e:
        logger.error(f"Error generating collections data: {str(e)}")
        return JSONResponse(
            status_code=400,
            content=DemoError(
                error_type="collections_generation_error",
                message=f"Collections data generation failed: {str(e)}",
                session_id=request_data.get("session_id", "")
            ).dict()
        )


# WebSocket Endpoints for Real-time Updates
@router.websocket("/ws/{demo_type}/{session_id}")
async def websocket_endpoint(websocket: WebSocket, demo_type: str, session_id: str):
    """WebSocket endpoint for real-time demo updates"""
    import asyncio
    import json

    await connection_manager.connect(websocket, session_id, demo_type)

    try:
        while True:
            # Listen for client messages
            data = await websocket.receive_text()
            message = json.loads(data)

            # Handle different message types
            message_type = message.get("type")

            if message_type == "start_simulation":
                if demo_type == "payment_processing":
                    await realtime_simulator.start_payment_processing_simulation(session_id)
                elif demo_type == "data_pipeline":
                    total_records = message.get("total_records", 100)
                    await realtime_simulator.start_pipeline_simulation(session_id, total_records)
                elif demo_type == "sales_dashboard":
                    await realtime_simulator.start_dashboard_simulation(session_id)

            elif message_type == "stop_simulation":
                realtime_simulator.stop_simulation(session_id)

            elif message_type == "ping":
                await connection_manager.send_to_connection(websocket, {
                    "type": "pong",
                    "timestamp": asyncio.get_event_loop().time()
                })

            # Echo other messages back for debugging
            else:
                await connection_manager.send_to_connection(websocket, {
                    "type": "echo",
                    "original_message": message
                })

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        realtime_simulator.stop_simulation(session_id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        connection_manager.disconnect(websocket)
        realtime_simulator.stop_simulation(session_id)
