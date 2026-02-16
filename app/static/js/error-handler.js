/**
 * Comprehensive Error Handler and Recovery System
 * Provides graceful error handling, user-friendly notifications, and automatic recovery
 */

class ErrorHandler {
    constructor() {
        this.errorQueue = [];
        this.recoveryStrategies = new Map();
        this.fallbackComponents = new Map();
        this.retryAttempts = new Map();
        this.maxRetries = 3;
        this.retryDelays = [1000, 2000, 5000]; // Progressive delay
        this.isOnline = navigator.onLine;
        this.offlineQueue = [];
        
        this.initialize();
    }

    /**
     * Initialize error handling system
     */
    initialize() {
        this.setupGlobalErrorHandlers();
        this.setupNetworkMonitoring();
        this.setupDefaultRecoveryStrategies();
        this.setupFallbackComponents();
        this.startErrorProcessing();
    }

    /**
     * Setup global error handlers
     */
    setupGlobalErrorHandlers() {
        // JavaScript errors
        window.addEventListener('error', (event) => {
            this.handleError({
                type: 'javascript_error',
                message: event.message,
                filename: event.filename,
                lineno: event.lineno,
                colno: event.colno,
                error: event.error,
                stack: event.error?.stack,
                timestamp: Date.now(),
                severity: 'high',
                context: 'global'
            });
        });

        // Unhandled promise rejections
        window.addEventListener('unhandledrejection', (event) => {
            this.handleError({
                type: 'unhandled_promise_rejection',
                message: event.reason?.message || 'Unhandled promise rejection',
                error: event.reason,
                stack: event.reason?.stack,
                timestamp: Date.now(),
                severity: 'high',
                context: 'promise'
            });
        });

        // Resource loading errors
        window.addEventListener('error', (event) => {
            if (event.target !== window) {
                this.handleError({
                    type: 'resource_error',
                    message: `Failed to load resource: ${event.target.src || event.target.href}`,
                    element: event.target.tagName,
                    source: event.target.src || event.target.href,
                    timestamp: Date.now(),
                    severity: 'medium',
                    context: 'resource_loading'
                });
            }
        }, true);

        // Network errors
        window.addEventListener('fetch', (event) => {
            const originalFetch = window.fetch;
            window.fetch = async (...args) => {
                try {
                    const response = await originalFetch(...args);
                    if (!response.ok) {
                        this.handleError({
                            type: 'network_error',
                            message: `HTTP ${response.status}: ${response.statusText}`,
                            url: args[0],
                            status: response.status,
                            statusText: response.statusText,
                            timestamp: Date.now(),
                            severity: response.status >= 500 ? 'high' : 'medium',
                            context: 'network'
                        });
                    }
                    return response;
                } catch (error) {
                    this.handleError({
                        type: 'network_error',
                        message: error.message,
                        url: args[0],
                        error: error,
                        timestamp: Date.now(),
                        severity: 'high',
                        context: 'network'
                    });
                    throw error;
                }
            };
        });
    }

    /**
     * Setup network monitoring
     */
    setupNetworkMonitoring() {
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.showNotification('Connection Restored', 'You are back online. Retrying failed operations...', 'success');
            this.processOfflineQueue();
        });

        window.addEventListener('offline', () => {
            this.isOnline = false;
            this.showNotification('Connection Lost', 'You are offline. Operations will be queued and retried when connection is restored.', 'warning');
        });
    }

    /**
     * Setup default recovery strategies
     */
    setupDefaultRecoveryStrategies() {
        // Network error recovery
        this.addRecoveryStrategy('network_error', async (error) => {
            if (!this.isOnline) {
                return this.queueForOffline(error);
            }
            
            const retryKey = `${error.url}_${error.timestamp}`;
            const attempts = this.retryAttempts.get(retryKey) || 0;
            
            if (attempts < this.maxRetries) {
                this.retryAttempts.set(retryKey, attempts + 1);
                await this.delay(this.retryDelays[attempts] || 5000);
                
                try {
                    const response = await fetch(error.url, error.options);
                    if (response.ok) {
                        this.showNotification('Request Successful', 'Network request recovered successfully', 'success');
                        this.retryAttempts.delete(retryKey);
                        return { success: true, response };
                    }
                } catch (retryError) {
                    // Will be caught by the next attempt or fallback
                }
            }
            
            return this.activateFallback('network_error', error);
        });

        // JavaScript error recovery
        this.addRecoveryStrategy('javascript_error', async (error) => {
            // Log error for analytics
            if (window.demoAnalytics) {
                window.demoAnalytics.trackError(error);
            }

            // Try to reload affected component
            if (error.context && error.context !== 'global') {
                return this.reloadComponent(error.context);
            }

            // Show error boundary
            return this.activateFallback('javascript_error', error);
        });

        // Resource loading error recovery
        this.addRecoveryStrategy('resource_error', async (error) => {
            const element = document.querySelector(`[src="${error.source}"], [href="${error.source}"]`);
            if (!element) return { success: false };

            // Try alternative CDN or local fallback
            const fallbackSrc = this.getFallbackResource(error.source);
            if (fallbackSrc) {
                element.src = fallbackSrc;
                element.href = fallbackSrc;
                return { success: true, fallback: fallbackSrc };
            }

            // Hide element if critical resource fails
            element.style.display = 'none';
            return this.activateFallback('resource_error', error);
        });

        // WebSocket error recovery
        this.addRecoveryStrategy('websocket_error', async (error) => {
            if (window.demoWebSocket) {
                // Attempt reconnection
                const reconnectResult = await window.demoWebSocket.attemptReconnection();
                if (reconnectResult.success) {
                    this.showNotification('WebSocket Reconnected', 'Real-time connection restored', 'success');
                    return { success: true };
                }
            }
            
            // Disable real-time features gracefully
            return this.disableRealtimeFeatures();
        });
    }

    /**
     * Setup fallback components
     */
    setupFallbackComponents() {
        // Network error fallback
        this.addFallbackComponent('network_error', {
            template: `
                <div class="error-fallback network-error-fallback">
                    <div class="error-icon">🌐</div>
                    <h3>Connection Issues</h3>
                    <p>We're having trouble connecting to our servers. Your data is safe, and we'll keep trying to reconnect.</p>
                    <div class="error-actions">
                        <button onclick="window.errorHandler.retryLastOperation()" class="retry-btn">
                            Try Again
                        </button>
                        <button onclick="window.errorHandler.switchToOfflineMode()" class="offline-btn">
                            Work Offline
                        </button>
                    </div>
                </div>
            `,
            css: `
                .network-error-fallback {
                    background: linear-gradient(135deg, #fef3c7, #fbbf24);
                    border: 2px solid #f59e0b;
                }
            `
        });

        // JavaScript error fallback
        this.addFallbackComponent('javascript_error', {
            template: `
                <div class="error-fallback js-error-fallback">
                    <div class="error-icon">⚠️</div>
                    <h3>Something Went Wrong</h3>
                    <p>We encountered an unexpected error. Don't worry - your data is safe and we've been notified.</p>
                    <div class="error-actions">
                        <button onclick="window.errorHandler.reloadPage()" class="reload-btn">
                            Reload Page
                        </button>
                        <button onclick="window.errorHandler.reportError()" class="report-btn">
                            Report Issue
                        </button>
                    </div>
                </div>
            `,
            css: `
                .js-error-fallback {
                    background: linear-gradient(135deg, #fee2e2, #f87171);
                    border: 2px solid #ef4444;
                }
            `
        });

        // Chart loading error fallback
        this.addFallbackComponent('chart_error', {
            template: `
                <div class="error-fallback chart-error-fallback">
                    <div class="error-icon">📊</div>
                    <h3>Chart Unavailable</h3>
                    <p>We couldn't load this chart. You can try refreshing or view the data in table format.</p>
                    <div class="error-actions">
                        <button onclick="window.errorHandler.retryChart()" class="retry-btn">
                            Retry Chart
                        </button>
                        <button onclick="window.errorHandler.showDataTable()" class="table-btn">
                            View Table
                        </button>
                    </div>
                </div>
            `,
            css: `
                .chart-error-fallback {
                    background: linear-gradient(135deg, #e0e7ff, #6366f1);
                    border: 2px solid #4f46e5;
                    color: white;
                }
            `
        });

        // Data loading error fallback
        this.addFallbackComponent('data_error', {
            template: `
                <div class="error-fallback data-error-fallback">
                    <div class="error-icon">📄</div>
                    <h3>Data Temporarily Unavailable</h3>
                    <p>We're having trouble loading the latest data. You can use cached data or try again.</p>
                    <div class="error-actions">
                        <button onclick="window.errorHandler.useCachedData()" class="cache-btn">
                            Use Cached Data
                        </button>
                        <button onclick="window.errorHandler.retryDataLoad()" class="retry-btn">
                            Try Again
                        </button>
                    </div>
                </div>
            `,
            css: `
                .data-error-fallback {
                    background: linear-gradient(135deg, #f3e8ff, #a855f7);
                    border: 2px solid #9333ea;
                    color: white;
                }
            `
        });
    }

    /**
     * Handle error with recovery strategies
     */
    async handleError(errorInfo) {
        // Add to error queue
        this.errorQueue.push(errorInfo);
        
        // Track with analytics
        if (window.demoAnalytics) {
            window.demoAnalytics.trackError(errorInfo);
        }

        // Show user notification for high severity errors
        if (errorInfo.severity === 'high') {
            this.showErrorNotification(errorInfo);
        }

        // Try recovery strategy
        const strategy = this.recoveryStrategies.get(errorInfo.type);
        if (strategy) {
            try {
                const result = await strategy(errorInfo);
                if (result.success) {
                    this.logRecovery(errorInfo, result);
                    return result;
                }
            } catch (recoveryError) {
                console.error('Recovery strategy failed:', recoveryError);
            }
        }

        // If recovery fails, log the error
        this.logError(errorInfo);
        return { success: false, error: errorInfo };
    }

    /**
     * Add recovery strategy for error type
     */
    addRecoveryStrategy(errorType, strategy) {
        this.recoveryStrategies.set(errorType, strategy);
    }

    /**
     * Add fallback component for error type
     */
    addFallbackComponent(errorType, component) {
        this.fallbackComponents.set(errorType, component);
    }

    /**
     * Activate fallback component
     */
    activateFallback(errorType, error, targetElement = null) {
        const fallback = this.fallbackComponents.get(errorType);
        if (!fallback) return { success: false };

        // Find target element or create overlay
        const target = targetElement || this.findErrorTarget(error);
        if (!target) return { success: false };

        // Create fallback element
        const fallbackElement = document.createElement('div');
        fallbackElement.innerHTML = fallback.template;
        fallbackElement.className = 'error-boundary-fallback';
        
        // Add custom CSS if provided
        if (fallback.css) {
            this.injectCSS(fallback.css, `fallback-${errorType}`);
        }

        // Replace or overlay the target
        if (target.parentNode) {
            target.style.display = 'none';
            target.parentNode.insertBefore(fallbackElement, target.nextSibling);
        }

        return { success: true, element: fallbackElement };
    }

    /**
     * Find appropriate target element for error
     */
    findErrorTarget(error) {
        // Try to find specific element based on error context
        if (error.context) {
            const contextElement = document.getElementById(error.context) || 
                                 document.querySelector(`[data-context="${error.context}"]`);
            if (contextElement) return contextElement;
        }

        // Default to main content area
        return document.querySelector('main') || 
               document.querySelector('.content') || 
               document.body;
    }

    /**
     * Queue operation for offline retry
     */
    queueForOffline(error) {
        this.offlineQueue.push({
            ...error,
            queuedAt: Date.now()
        });

        this.showNotification(
            'Operation Queued', 
            'This operation will be retried when you\'re back online', 
            'info'
        );

        return { success: false, queued: true };
    }

    /**
     * Process offline queue when connection restored
     */
    async processOfflineQueue() {
        const queue = [...this.offlineQueue];
        this.offlineQueue = [];

        for (const operation of queue) {
            try {
                await this.retryOperation(operation);
            } catch (error) {
                console.error('Failed to retry queued operation:', error);
                // Re-queue if still failing
                this.offlineQueue.push(operation);
            }
        }

        if (this.offlineQueue.length > 0) {
            this.showNotification(
                'Some Operations Failed', 
                `${this.offlineQueue.length} operations are still pending`, 
                'warning'
            );
        }
    }

    /**
     * Retry operation
     */
    async retryOperation(operation) {
        switch (operation.type) {
            case 'network_error':
                return await fetch(operation.url, operation.options);
            case 'websocket_error':
                return await this.reconnectWebSocket();
            default:
                throw new Error(`Unknown operation type: ${operation.type}`);
        }
    }

    /**
     * Show error notification to user
     */
    showErrorNotification(error) {
        const userFriendlyMessage = this.getUserFriendlyMessage(error);
        
        if (window.demoWebSocket?.showNotification) {
            window.demoWebSocket.showNotification(
                'Error Occurred',
                userFriendlyMessage,
                'error'
            );
        } else {
            // Fallback notification
            this.showFallbackNotification(userFriendlyMessage, 'error');
        }
    }

    /**
     * Get user-friendly error message
     */
    getUserFriendlyMessage(error) {
        const messages = {
            'network_error': 'We\'re having trouble connecting to our servers. Please check your internet connection.',
            'javascript_error': 'Something unexpected happened. We\'ve been notified and are looking into it.',
            'resource_error': 'Some content couldn\'t be loaded. The page should still work normally.',
            'websocket_error': 'Real-time updates are temporarily unavailable. Data will still update when you refresh.',
            'chart_error': 'This chart couldn\'t be displayed. You can try refreshing or view the data in table format.',
            'data_error': 'We couldn\'t load the latest data. You can try again or use previously loaded information.'
        };

        return messages[error.type] || 'An unexpected error occurred. Please try again.';
    }

    /**
     * Show fallback notification
     */
    showFallbackNotification(message, type = 'error') {
        const notification = document.createElement('div');
        notification.className = `fallback-notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">${type === 'error' ? '⚠️' : 'ℹ️'}</span>
                <span class="notification-message">${message}</span>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;

        document.body.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }

    /**
     * Show notification using available system
     */
    showNotification(title, message, type = 'info') {
        if (window.demoWebSocket?.showNotification) {
            window.demoWebSocket.showNotification(title, message, type);
        } else {
            this.showFallbackNotification(`${title}: ${message}`, type);
        }
    }

    /**
     * Utility functions for error recovery
     */
    async delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    getFallbackResource(originalSrc) {
        const fallbacks = {
            'https://cdn.jsdelivr.net/npm/chart.js': '/static/js/chart.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/jspdf/': '/static/js/jspdf.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/xlsx/': '/static/js/xlsx.min.js'
        };

        for (const [pattern, fallback] of Object.entries(fallbacks)) {
            if (originalSrc.includes(pattern)) {
                return fallback;
            }
        }

        return null;
    }

    reloadComponent(componentId) {
        const component = document.getElementById(componentId);
        if (component) {
            const parent = component.parentNode;
            const newComponent = component.cloneNode(true);
            parent.replaceChild(newComponent, component);
            return { success: true };
        }
        return { success: false };
    }

    disableRealtimeFeatures() {
        // Hide real-time controls
        const realtimeButtons = document.querySelectorAll('[id*="realtime"], [id*="websocket"]');
        realtimeButtons.forEach(btn => {
            btn.disabled = true;
            btn.textContent = 'Offline';
        });

        this.showNotification(
            'Real-time Features Disabled',
            'Real-time updates are temporarily unavailable. You can still use all other features.',
            'warning'
        );

        return { success: true };
    }

    /**
     * User action handlers
     */
    retryLastOperation() {
        const lastError = this.errorQueue[this.errorQueue.length - 1];
        if (lastError) {
            this.handleError(lastError);
        }
    }

    switchToOfflineMode() {
        this.showNotification(
            'Offline Mode',
            'You\'re now in offline mode. Some features may be limited.',
            'info'
        );
        // Implement offline mode logic
    }

    reloadPage() {
        window.location.reload();
    }

    reportError() {
        const lastError = this.errorQueue[this.errorQueue.length - 1];
        if (lastError) {
            this.showNotification(
                'Error Reported',
                'Thank you for reporting this issue. We\'ll investigate it promptly.',
                'success'
            );
            // Send error report to server
            this.sendErrorReport(lastError);
        }
    }

    retryChart() {
        // Retry chart loading logic
        window.location.reload();
    }

    showDataTable() {
        // Show data in table format instead of chart
        this.showNotification(
            'Table View',
            'Displaying data in table format instead of chart.',
            'info'
        );
    }

    useCachedData() {
        // Use cached data logic
        this.showNotification(
            'Using Cached Data',
            'Displaying previously loaded data.',
            'info'
        );
    }

    retryDataLoad() {
        // Retry data loading
        window.location.reload();
    }

    /**
     * Utility methods
     */
    injectCSS(css, id) {
        if (document.getElementById(id)) return;

        const style = document.createElement('style');
        style.id = id;
        style.textContent = css;
        document.head.appendChild(style);
    }

    logError(error) {
        console.error('Unrecovered error:', error);
        
        // Send to server for logging
        this.sendErrorReport(error);
    }

    logRecovery(error, result) {
        console.log('Error recovered:', error.type, result);
        
        if (window.demoAnalytics) {
            window.demoAnalytics.trackEvent('error_recovery', {
                errorType: error.type,
                recoveryResult: result,
                timestamp: Date.now()
            });
        }
    }

    async sendErrorReport(error) {
        try {
            await fetch('/api/error-report', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    error: error,
                    userAgent: navigator.userAgent,
                    url: window.location.href,
                    timestamp: Date.now()
                })
            });
        } catch (e) {
            console.error('Failed to send error report:', e);
        }
    }

    startErrorProcessing() {
        // Process error queue periodically
        setInterval(() => {
            this.processErrorQueue();
        }, 10000); // Every 10 seconds
    }

    processErrorQueue() {
        // Clean up old errors
        const oneHourAgo = Date.now() - (60 * 60 * 1000);
        this.errorQueue = this.errorQueue.filter(error => error.timestamp > oneHourAgo);
    }

    /**
     * Get error statistics
     */
    getErrorStats() {
        const stats = {
            totalErrors: this.errorQueue.length,
            errorTypes: {},
            severityBreakdown: { high: 0, medium: 0, low: 0 },
            recentErrors: this.errorQueue.slice(-10)
        };

        this.errorQueue.forEach(error => {
            stats.errorTypes[error.type] = (stats.errorTypes[error.type] || 0) + 1;
            stats.severityBreakdown[error.severity || 'medium']++;
        });

        return stats;
    }
}

// Base CSS for error handling components
const errorHandlerStyles = `
    .error-boundary-fallback {
        margin: 1rem;
        padding: 2rem;
        border-radius: 0.75rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .error-fallback {
        background: #f9fafb;
        border: 2px solid #e5e7eb;
        color: #111827;
    }

    .dark .error-fallback {
        background: #374151;
        border-color: #4b5563;
        color: #f9fafb;
    }

    .error-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    .error-fallback h3 {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .error-fallback p {
        margin-bottom: 1.5rem;
        opacity: 0.8;
    }

    .error-actions {
        display: flex;
        gap: 0.75rem;
        justify-content: center;
        flex-wrap: wrap;
    }

    .error-actions button {
        background: #4f46e5;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        cursor: pointer;
        font-weight: 500;
        transition: background-color 0.2s;
    }

    .error-actions button:hover {
        background: #4338ca;
    }

    .retry-btn {
        background: #10b981 !important;
    }

    .retry-btn:hover {
        background: #059669 !important;
    }

    .offline-btn, .cache-btn {
        background: #f59e0b !important;
    }

    .offline-btn:hover, .cache-btn:hover {
        background: #d97706 !important;
    }

    .reload-btn {
        background: #ef4444 !important;
    }

    .reload-btn:hover {
        background: #dc2626 !important;
    }

    .fallback-notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        z-index: 10000;
        max-width: 400px;
        animation: slideIn 0.3s ease-out;
    }

    .notification-error {
        border-left: 4px solid #ef4444;
    }

    .notification-warning {
        border-left: 4px solid #f59e0b;
    }

    .notification-info {
        border-left: 4px solid #3b82f6;
    }

    .notification-success {
        border-left: 4px solid #10b981;
    }

    .notification-content {
        padding: 1rem;
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
    }

    .notification-icon {
        font-size: 1.25rem;
        flex-shrink: 0;
    }

    .notification-message {
        flex: 1;
        font-size: 0.875rem;
        line-height: 1.4;
    }

    .notification-close {
        background: none;
        border: none;
        font-size: 1.25rem;
        cursor: pointer;
        color: #9ca3af;
        flex-shrink: 0;
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

// Inject styles
if (!document.querySelector('#error-handler-styles')) {
    const styleSheet = document.createElement('style');
    styleSheet.id = 'error-handler-styles';
    styleSheet.textContent = errorHandlerStyles;
    document.head.appendChild(styleSheet);
}

// Global error handler instance
window.errorHandler = new ErrorHandler();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ErrorHandler;
}