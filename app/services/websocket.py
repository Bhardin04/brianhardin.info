"""
WebSocket service for real-time demo updates.
Provides live data streaming and interactive updates for demos.
"""

import asyncio
import json
import logging
from typing import Any
from uuid import uuid4

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    """WebSocket connection manager for demo sessions"""

    MAX_CONNECTIONS = 200
    MAX_CONNECTIONS_PER_SESSION = 5

    def __init__(self) -> None:
        # Active connections by session ID
        self.active_connections: dict[str, set[WebSocket]] = {}
        # Connection metadata
        self.connection_data: dict[WebSocket, dict[str, Any]] = {}

    async def connect(
        self, websocket: WebSocket, session_id: str, demo_type: str
    ) -> None:
        """Accept a new WebSocket connection"""
        if len(self.connection_data) >= self.MAX_CONNECTIONS:
            await websocket.close(code=1013, reason="Server at capacity")
            return

        session_conns = self.active_connections.get(session_id, set())
        if len(session_conns) >= self.MAX_CONNECTIONS_PER_SESSION:
            await websocket.close(code=1013, reason="Too many connections for session")
            return

        await websocket.accept()

        # Initialize session if not exists
        if session_id not in self.active_connections:
            self.active_connections[session_id] = set()

        # Add connection to session
        self.active_connections[session_id].add(websocket)

        # Store connection metadata
        self.connection_data[websocket] = {
            "session_id": session_id,
            "demo_type": demo_type,
            "connection_id": str(uuid4()),
            "connected_at": asyncio.get_event_loop().time(),
        }

        logger.info(f"WebSocket connected: session={session_id}, demo={demo_type}")

        # Send connection confirmation
        await self.send_to_connection(
            websocket,
            {
                "type": "connection_established",
                "session_id": session_id,
                "demo_type": demo_type,
                "timestamp": asyncio.get_event_loop().time(),
            },
        )

    def disconnect(self, websocket: WebSocket) -> None:
        """Remove a WebSocket connection"""
        if websocket in self.connection_data:
            data = self.connection_data[websocket]
            session_id = data["session_id"]

            # Remove from session
            if session_id in self.active_connections:
                self.active_connections[session_id].discard(websocket)

                # Clean up empty sessions
                if not self.active_connections[session_id]:
                    del self.active_connections[session_id]

            # Remove metadata
            del self.connection_data[websocket]

            logger.info(f"WebSocket disconnected: session={session_id}")

    async def send_to_connection(
        self, websocket: WebSocket, data: dict[str, Any]
    ) -> None:
        """Send data to a specific connection"""
        try:
            await websocket.send_text(json.dumps(data))
        except Exception as e:
            logger.error(f"Error sending WebSocket message: {e}")
            self.disconnect(websocket)

    async def send_to_session(self, session_id: str, data: dict[str, Any]) -> None:
        """Send data to all connections in a session"""
        if session_id in self.active_connections:
            connections = self.active_connections[session_id].copy()

            for websocket in connections:
                await self.send_to_connection(websocket, data)

    async def broadcast_to_demo_type(
        self, demo_type: str, data: dict[str, Any]
    ) -> None:
        """Broadcast data to all connections of a specific demo type"""
        for websocket, metadata in self.connection_data.items():
            if metadata["demo_type"] == demo_type:
                await self.send_to_connection(websocket, data)

    async def broadcast_to_all(self, data: dict[str, Any]) -> None:
        """Broadcast data to all active connections"""
        for websocket in self.connection_data.keys():
            await self.send_to_connection(websocket, data)

    def get_session_connections(self, session_id: str) -> int:
        """Get number of active connections for a session"""
        return len(self.active_connections.get(session_id, set()))

    def get_total_connections(self) -> int:
        """Get total number of active connections"""
        return len(self.connection_data)


class DemoWebSocketService:
    """Service for demo-specific WebSocket functionality"""

    def __init__(self, connection_manager: ConnectionManager) -> None:
        self.manager = connection_manager

    async def send_payment_processing_update(
        self, session_id: str, update_type: str, data: dict[str, Any]
    ) -> None:
        """Send payment processing real-time updates"""
        message = {
            "type": "payment_processing_update",
            "update_type": update_type,
            "data": data,
            "timestamp": asyncio.get_event_loop().time(),
        }
        await self.manager.send_to_session(session_id, message)

    async def send_pipeline_progress_update(
        self,
        session_id: str,
        step: str,
        progress: float,
        status: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Send data pipeline progress updates"""
        message = {
            "type": "pipeline_progress",
            "step": step,
            "progress": progress,
            "status": status,
            "details": details or {},
            "timestamp": asyncio.get_event_loop().time(),
        }
        await self.manager.send_to_session(session_id, message)

    async def send_dashboard_data_update(
        self, session_id: str, chart_type: str, data: dict[str, Any]
    ) -> None:
        """Send dashboard real-time data updates"""
        message = {
            "type": "dashboard_update",
            "chart_type": chart_type,
            "data": data,
            "timestamp": asyncio.get_event_loop().time(),
        }
        await self.manager.send_to_session(session_id, message)

    async def send_collections_metrics_update(
        self, session_id: str, metric_type: str, data: dict[str, Any]
    ) -> None:
        """Send collections dashboard metrics updates"""
        message = {
            "type": "collections_update",
            "metric_type": metric_type,
            "data": data,
            "timestamp": asyncio.get_event_loop().time(),
        }
        await self.manager.send_to_session(session_id, message)

    async def send_error_notification(
        self,
        session_id: str,
        error_type: str,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Send error notifications to session"""
        error_message = {
            "type": "error_notification",
            "error_type": error_type,
            "message": message,
            "details": details or {},
            "timestamp": asyncio.get_event_loop().time(),
        }
        await self.manager.send_to_session(session_id, error_message)

    async def send_system_notification(
        self, session_id: str, notification_type: str, title: str, message: str
    ) -> None:
        """Send system notifications to session"""
        notification = {
            "type": "system_notification",
            "notification_type": notification_type,
            "title": title,
            "message": message,
            "timestamp": asyncio.get_event_loop().time(),
        }
        await self.manager.send_to_session(session_id, notification)


class RealtimeDataSimulator:
    """Simulates real-time data updates for demos"""

    def __init__(self, websocket_service: DemoWebSocketService) -> None:
        self.websocket_service = websocket_service
        self.active_simulations: dict[str, asyncio.Task[None]] = {}

    async def start_payment_processing_simulation(self, session_id: str) -> None:
        """Start real-time payment processing simulation"""
        if session_id in self.active_simulations:
            return

        task = asyncio.create_task(self._simulate_payment_processing(session_id))
        self.active_simulations[session_id] = task

    async def start_pipeline_simulation(
        self, session_id: str, total_records: int
    ) -> None:
        """Start real-time data pipeline simulation"""
        if session_id in self.active_simulations:
            return

        task = asyncio.create_task(
            self._simulate_pipeline_processing(session_id, total_records)
        )
        self.active_simulations[session_id] = task

    async def start_dashboard_simulation(self, session_id: str) -> None:
        """Start real-time dashboard updates"""
        if session_id in self.active_simulations:
            return

        task = asyncio.create_task(self._simulate_dashboard_updates(session_id))
        self.active_simulations[session_id] = task

    def stop_simulation(self, session_id: str) -> None:
        """Stop simulation for a session"""
        if session_id in self.active_simulations:
            task = self.active_simulations[session_id]
            task.cancel()
            del self.active_simulations[session_id]

    async def _simulate_payment_processing(self, session_id: str) -> None:
        """Simulate payment processing steps with real-time updates"""
        try:
            steps = [
                ("validation", "Validating payment details", 2),
                ("matching", "Finding invoice matches", 3),
                ("scoring", "Calculating confidence scores", 2),
                ("applying", "Applying payment to invoices", 2),
                ("updating", "Updating AR ledger", 1),
                ("completed", "Payment processing complete", 0),
            ]

            for step, description, duration in steps:
                await self.websocket_service.send_payment_processing_update(
                    session_id,
                    "step_update",
                    {"step": step, "description": description, "status": "in_progress"},
                )

                if duration > 0:
                    await asyncio.sleep(duration)

                await self.websocket_service.send_payment_processing_update(
                    session_id,
                    "step_update",
                    {"step": step, "description": description, "status": "completed"},
                )

        except asyncio.CancelledError:
            logger.info(
                f"Payment processing simulation cancelled for session {session_id}"
            )
        except Exception as e:
            logger.error(f"Error in payment processing simulation: {e}")
            await self.websocket_service.send_error_notification(
                session_id, "simulation_error", "Payment processing simulation failed"
            )

    async def _simulate_pipeline_processing(
        self, session_id: str, total_records: int
    ) -> None:
        """Simulate data pipeline processing with progress updates"""
        try:
            stages = [
                ("extraction", "Extracting data from NetSuite", 30),
                ("transformation", "Applying transformation rules", 40),
                ("validation", "Validating data quality", 20),
                ("loading", "Loading to SAP system", 10),
            ]

            processed_records = 0

            for stage, description, percentage in stages:
                stage_records = int((percentage / 100) * total_records)

                for _i in range(stage_records):
                    processed_records += 1
                    progress = (processed_records / total_records) * 100

                    await self.websocket_service.send_pipeline_progress_update(
                        session_id,
                        stage,
                        progress,
                        "processing",
                        {
                            "processed_records": processed_records,
                            "total_records": total_records,
                            "current_stage": description,
                        },
                    )

                    # Simulate processing time
                    await asyncio.sleep(0.1)

            # Final completion update
            await self.websocket_service.send_pipeline_progress_update(
                session_id,
                "completed",
                100.0,
                "completed",
                {
                    "processed_records": total_records,
                    "total_records": total_records,
                    "message": "Data pipeline processing completed successfully",
                },
            )

        except asyncio.CancelledError:
            logger.info(f"Pipeline simulation cancelled for session {session_id}")
        except Exception as e:
            logger.error(f"Error in pipeline simulation: {e}")
            await self.websocket_service.send_error_notification(
                session_id, "simulation_error", "Pipeline processing simulation failed"
            )

    async def _simulate_dashboard_updates(self, session_id: str) -> None:
        """Simulate real-time dashboard data updates"""
        try:
            import random

            while True:
                # Simulate KPI updates every 10 seconds
                await asyncio.sleep(10)

                # Generate random KPI changes
                kpi_updates = {
                    "total_revenue": random.uniform(-5000, 15000),
                    "gross_margin": random.uniform(-0.5, 1.2),
                    "customer_count": random.randint(-2, 5),
                    "churn_rate": random.uniform(-0.3, 0.8),
                }

                await self.websocket_service.send_dashboard_data_update(
                    session_id, "kpi_update", kpi_updates
                )

                # Simulate new customer data every 15 seconds
                await asyncio.sleep(5)

                new_customer_data = {
                    "customer_id": f"CUST-{random.randint(100, 999)}",
                    "customer_name": f"New Customer {random.randint(1, 100)}",
                    "revenue": random.uniform(5000, 50000),
                    "growth_rate": random.uniform(-0.2, 0.4),
                }

                await self.websocket_service.send_dashboard_data_update(
                    session_id, "new_customer", new_customer_data
                )

        except asyncio.CancelledError:
            logger.info(f"Dashboard simulation cancelled for session {session_id}")
        except Exception as e:
            logger.error(f"Error in dashboard simulation: {e}")


# Global instances
connection_manager = ConnectionManager()
websocket_service = DemoWebSocketService(connection_manager)
realtime_simulator = RealtimeDataSimulator(websocket_service)
