/**
 * WebSocket Client for Real-time Demo Updates
 * Handles real-time communication with demo backends
 */

class DemoWebSocketClient {
    constructor() {
        this.connections = new Map();
        this.messageHandlers = new Map();
        this.reconnectAttempts = new Map();
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000; // Start with 1 second
        this.heartbeatInterval = 30000; // 30 seconds
        this.heartbeatTimers = new Map();
    }

    /**
     * Connect to WebSocket for a specific demo session
     */
    connect(demoType, sessionId, options = {}) {
        const connectionKey = `${demoType}-${sessionId}`;
        
        // Don't create duplicate connections
        if (this.connections.has(connectionKey)) {
            console.log(`WebSocket already connected for ${connectionKey}`);
            return this.connections.get(connectionKey);
        }

        // Determine WebSocket URL
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host;
        const wsUrl = `${protocol}//${host}/demos/ws/${demoType}/${sessionId}`;

        console.log(`Connecting to WebSocket: ${wsUrl}`);

        try {
            const ws = new WebSocket(wsUrl);
            this.connections.set(connectionKey, ws);
            this.reconnectAttempts.set(connectionKey, 0);

            // Setup event handlers
            this.setupWebSocketHandlers(ws, connectionKey, demoType, sessionId, options);

            return ws;
        } catch (error) {
            console.error(`Failed to create WebSocket connection: ${error}`);
            this.handleConnectionError(connectionKey, demoType, sessionId, options);
            return null;
        }
    }

    /**
     * Setup WebSocket event handlers
     */
    setupWebSocketHandlers(ws, connectionKey, demoType, sessionId, options) {
        ws.onopen = (event) => {
            console.log(`WebSocket connected: ${connectionKey}`);
            this.reconnectAttempts.set(connectionKey, 0);
            this.startHeartbeat(connectionKey);
            
            // Trigger connection event
            this.triggerEvent('connected', {
                connectionKey,
                demoType,
                sessionId,
                event
            });

            // Call user-defined onOpen handler
            if (options.onOpen) {
                options.onOpen(event);
            }
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                console.log(`WebSocket message received:`, data);
                
                this.handleMessage(connectionKey, data);
                
                // Call user-defined onMessage handler
                if (options.onMessage) {
                    options.onMessage(data);
                }
            } catch (error) {
                console.error('Error parsing WebSocket message:', error);
            }
        };

        ws.onclose = (event) => {
            console.log(`WebSocket closed: ${connectionKey}`, event);
            this.stopHeartbeat(connectionKey);
            this.connections.delete(connectionKey);
            
            // Trigger disconnection event
            this.triggerEvent('disconnected', {
                connectionKey,
                demoType,
                sessionId,
                event
            });

            // Attempt reconnection if not closed intentionally
            if (event.code !== 1000) {
                this.attemptReconnection(connectionKey, demoType, sessionId, options);
            }

            // Call user-defined onClose handler
            if (options.onClose) {
                options.onClose(event);
            }
        };

        ws.onerror = (error) => {
            console.error(`WebSocket error: ${connectionKey}`, error);
            
            // Trigger error event
            this.triggerEvent('error', {
                connectionKey,
                demoType,
                sessionId,
                error
            });

            // Call user-defined onError handler
            if (options.onError) {
                options.onError(error);
            }
        };
    }

    /**
     * Handle incoming messages
     */
    handleMessage(connectionKey, data) {
        const messageType = data.type;
        
        // Handle built-in message types
        switch (messageType) {
            case 'connection_established':
                this.handleConnectionEstablished(connectionKey, data);
                break;
            case 'pong':
                this.handlePong(connectionKey, data);
                break;
            case 'payment_processing_update':
                this.handlePaymentProcessingUpdate(connectionKey, data);
                break;
            case 'pipeline_progress':
                this.handlePipelineProgress(connectionKey, data);
                break;
            case 'dashboard_update':
                this.handleDashboardUpdate(connectionKey, data);
                break;
            case 'collections_update':
                this.handleCollectionsUpdate(connectionKey, data);
                break;
            case 'error_notification':
                this.handleErrorNotification(connectionKey, data);
                break;
            case 'system_notification':
                this.handleSystemNotification(connectionKey, data);
                break;
        }

        // Call registered message handlers
        const handlers = this.messageHandlers.get(connectionKey) || [];
        handlers.forEach(handler => {
            try {
                handler(data);
            } catch (error) {
                console.error('Error in message handler:', error);
            }
        });

        // Trigger generic message event
        this.triggerEvent('message', {
            connectionKey,
            data
        });
    }

    /**
     * Handle connection established
     */
    handleConnectionEstablished(connectionKey, data) {
        console.log('Connection established:', data);
        this.showNotification('Connected', 'Real-time updates enabled', 'success');
    }

    /**
     * Handle heartbeat pong
     */
    handlePong(connectionKey, data) {
        console.log('Heartbeat pong received');
    }

    /**
     * Handle payment processing updates
     */
    handlePaymentProcessingUpdate(connectionKey, data) {
        const { update_type, data: updateData } = data;
        
        switch (update_type) {
            case 'step_update':
                this.updatePaymentProcessingStep(updateData);
                break;
            case 'invoice_match':
                this.updateInvoiceMatches(updateData);
                break;
            case 'balance_update':
                this.updateAccountBalances(updateData);
                break;
        }
    }

    /**
     * Handle pipeline progress updates
     */
    handlePipelineProgress(connectionKey, data) {
        const { step, progress, status, details } = data;
        
        // Update progress indicators
        this.updatePipelineProgress(step, progress, status, details);
        
        // Update step status in UI
        this.updatePipelineStepStatus(step, status);
        
        if (status === 'completed' && progress >= 100) {
            this.showNotification('Pipeline Complete', 'Data processing finished successfully', 'success');
        }
    }

    /**
     * Handle dashboard updates
     */
    handleDashboardUpdate(connectionKey, data) {
        const { chart_type, data: chartData } = data;
        
        switch (chart_type) {
            case 'kpi_update':
                this.updateDashboardKPIs(chartData);
                break;
            case 'new_customer':
                this.addNewCustomerData(chartData);
                break;
            case 'revenue_update':
                this.updateRevenueChart(chartData);
                break;
        }
    }

    /**
     * Handle collections updates
     */
    handleCollectionsUpdate(connectionKey, data) {
        const { metric_type, data: metricsData } = data;
        
        switch (metric_type) {
            case 'dso_update':
                this.updateDSOMetrics(metricsData);
                break;
            case 'collector_performance':
                this.updateCollectorPerformance(metricsData);
                break;
            case 'new_collection':
                this.addNewCollection(metricsData);
                break;
        }
    }

    /**
     * Handle error notifications
     */
    handleErrorNotification(connectionKey, data) {
        const { error_type, message, details } = data;
        
        console.error('Demo error notification:', data);
        this.showNotification('Error', message, 'error');
        
        // Trigger error event for specific handling
        this.triggerEvent('demo-error', {
            connectionKey,
            errorType: error_type,
            message,
            details
        });
    }

    /**
     * Handle system notifications
     */
    handleSystemNotification(connectionKey, data) {
        const { notification_type, title, message } = data;
        
        this.showNotification(title, message, notification_type);
    }

    /**
     * Send message to WebSocket
     */
    sendMessage(demoType, sessionId, message) {
        const connectionKey = `${demoType}-${sessionId}`;
        const ws = this.connections.get(connectionKey);
        
        if (!ws || ws.readyState !== WebSocket.OPEN) {
            console.error('WebSocket not connected or not ready');
            return false;
        }

        try {
            ws.send(JSON.stringify(message));
            return true;
        } catch (error) {
            console.error('Error sending WebSocket message:', error);
            return false;
        }
    }

    /**
     * Register message handler for specific connection
     */
    onMessage(demoType, sessionId, handler) {
        const connectionKey = `${demoType}-${sessionId}`;
        
        if (!this.messageHandlers.has(connectionKey)) {
            this.messageHandlers.set(connectionKey, []);
        }
        
        this.messageHandlers.get(connectionKey).push(handler);
    }

    /**
     * Start simulation
     */
    startSimulation(demoType, sessionId, options = {}) {
        return this.sendMessage(demoType, sessionId, {
            type: 'start_simulation',
            ...options
        });
    }

    /**
     * Stop simulation
     */
    stopSimulation(demoType, sessionId) {
        return this.sendMessage(demoType, sessionId, {
            type: 'stop_simulation'
        });
    }

    /**
     * Disconnect from WebSocket
     */
    disconnect(demoType, sessionId) {
        const connectionKey = `${demoType}-${sessionId}`;
        const ws = this.connections.get(connectionKey);
        
        if (ws) {
            this.stopHeartbeat(connectionKey);
            ws.close(1000, 'Client disconnect');
            this.connections.delete(connectionKey);
            this.messageHandlers.delete(connectionKey);
            this.reconnectAttempts.delete(connectionKey);
        }
    }

    /**
     * Disconnect all connections
     */
    disconnectAll() {
        for (const [connectionKey, ws] of this.connections) {
            this.stopHeartbeat(connectionKey);
            ws.close(1000, 'Client disconnect all');
        }
        
        this.connections.clear();
        this.messageHandlers.clear();
        this.reconnectAttempts.clear();
    }

    /**
     * Start heartbeat for connection
     */
    startHeartbeat(connectionKey) {
        this.stopHeartbeat(connectionKey); // Clear any existing heartbeat
        
        const timer = setInterval(() => {
            const ws = this.connections.get(connectionKey);
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({ type: 'ping' }));
            } else {
                this.stopHeartbeat(connectionKey);
            }
        }, this.heartbeatInterval);
        
        this.heartbeatTimers.set(connectionKey, timer);
    }

    /**
     * Stop heartbeat for connection
     */
    stopHeartbeat(connectionKey) {
        const timer = this.heartbeatTimers.get(connectionKey);
        if (timer) {
            clearInterval(timer);
            this.heartbeatTimers.delete(connectionKey);
        }
    }

    /**
     * Attempt reconnection
     */
    attemptReconnection(connectionKey, demoType, sessionId, options) {
        const attempts = this.reconnectAttempts.get(connectionKey) || 0;
        
        if (attempts >= this.maxReconnectAttempts) {
            console.log(`Max reconnection attempts reached for ${connectionKey}`);
            this.showNotification('Connection Lost', 'Unable to reconnect to real-time updates', 'error');
            return;
        }

        const delay = this.reconnectDelay * Math.pow(2, attempts); // Exponential backoff
        console.log(`Attempting reconnection ${attempts + 1}/${this.maxReconnectAttempts} for ${connectionKey} in ${delay}ms`);
        
        this.reconnectAttempts.set(connectionKey, attempts + 1);
        
        setTimeout(() => {
            this.connect(demoType, sessionId, options);
        }, delay);
    }

    /**
     * Handle connection error
     */
    handleConnectionError(connectionKey, demoType, sessionId, options) {
        console.error(`Connection error for ${connectionKey}`);
        this.attemptReconnection(connectionKey, demoType, sessionId, options);
    }

    /**
     * Show notification to user
     */
    showNotification(title, message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <strong>${title}</strong>
                <p>${message}</p>
            </div>
            <button class="notification-close">&times;</button>
        `;

        // Add to notifications container or create one
        let container = document.querySelector('.notifications-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'notifications-container';
            document.body.appendChild(container);
        }

        container.appendChild(notification);

        // Handle close button
        notification.querySelector('.notification-close').onclick = () => {
            notification.remove();
        };

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }

    /**
     * Trigger custom events
     */
    triggerEvent(eventName, data) {
        const event = new CustomEvent(`websocket:${eventName}`, {
            detail: data
        });
        document.dispatchEvent(event);
    }

    /**
     * Update UI methods (to be implemented by specific demos)
     */
    updatePaymentProcessingStep(data) {
        // Implementation depends on payment processing UI structure
        console.log('Payment processing step update:', data);
    }

    updatePipelineProgress(step, progress, status, details) {
        // Update progress bars and step indicators
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');
        
        if (progressBar) {
            progressBar.style.width = `${progress}%`;
        }
        
        if (progressText) {
            progressText.textContent = `${progress.toFixed(1)}%`;
        }
    }

    updatePipelineStepStatus(step, status) {
        // Update step status in pipeline UI
        console.log(`Pipeline step ${step} status: ${status}`);
    }

    updateDashboardKPIs(data) {
        // Update KPI values in dashboard
        console.log('Dashboard KPI update:', data);
    }

    addNewCustomerData(data) {
        // Add new customer to revenue table
        console.log('New customer data:', data);
    }

    updateDSOMetrics(data) {
        // Update DSO metrics in collections dashboard
        console.log('DSO metrics update:', data);
    }

    /**
     * Get connection status
     */
    getConnectionStatus(demoType, sessionId) {
        const connectionKey = `${demoType}-${sessionId}`;
        const ws = this.connections.get(connectionKey);
        
        if (!ws) {
            return 'disconnected';
        }
        
        switch (ws.readyState) {
            case WebSocket.CONNECTING: return 'connecting';
            case WebSocket.OPEN: return 'connected';
            case WebSocket.CLOSING: return 'closing';
            case WebSocket.CLOSED: return 'closed';
            default: return 'unknown';
        }
    }

    /**
     * Get connection statistics
     */
    getStats() {
        return {
            totalConnections: this.connections.size,
            activeHeartbeats: this.heartbeatTimers.size,
            messageHandlers: Array.from(this.messageHandlers.values()).reduce((sum, handlers) => sum + handlers.length, 0)
        };
    }
}

// CSS for notifications
const notificationStyles = `
    .notifications-container {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        max-width: 400px;
    }

    .notification {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 0.5rem;
        padding: 1rem;
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        animation: slideIn 0.3s ease-out;
    }

    .notification-success {
        border-left: 4px solid #10b981;
    }

    .notification-error {
        border-left: 4px solid #ef4444;
    }

    .notification-info {
        border-left: 4px solid #3b82f6;
    }

    .notification-content strong {
        display: block;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }

    .notification-content p {
        margin: 0;
        font-size: 0.875rem;
        color: #6b7280;
    }

    .notification-close {
        background: none;
        border: none;
        font-size: 1.25rem;
        cursor: pointer;
        color: #9ca3af;
        margin-left: 1rem;
    }

    .notification-close:hover {
        color: #374151;
    }

    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;

// Inject notification styles
if (!document.querySelector('#websocket-notification-styles')) {
    const styleSheet = document.createElement('style');
    styleSheet.id = 'websocket-notification-styles';
    styleSheet.textContent = notificationStyles;
    document.head.appendChild(styleSheet);
}

// Global instance
window.demoWebSocket = new DemoWebSocketClient();

// Auto-cleanup on page unload
window.addEventListener('beforeunload', () => {
    window.demoWebSocket.disconnectAll();
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DemoWebSocketClient;
}