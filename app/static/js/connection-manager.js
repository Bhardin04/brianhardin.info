/**
 * Connection Manager
 * Handles offline/online states, connection recovery, and request queuing
 */

class ConnectionManager {
    constructor() {
        this.isOnline = navigator.onLine;
        this.connectionQuality = 'good';
        this.requestQueue = [];
        this.retryQueue = [];
        this.offlineData = new Map();
        this.connectionTests = [];
        this.lastPingTime = null;
        this.pingInterval = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.baseRetryDelay = 1000;
        
        this.initialize();
    }

    /**
     * Initialize connection manager
     */
    initialize() {
        this.setupNetworkListeners();
        this.startConnectionMonitoring();
        this.setupServiceWorker();
    }

    /**
     * Setup network event listeners
     */
    setupNetworkListeners() {
        window.addEventListener('online', () => {
            this.handleOnline();
        });

        window.addEventListener('offline', () => {
            this.handleOffline();
        });

        // Enhanced connection detection
        window.addEventListener('beforeunload', () => {
            this.saveOfflineData();
        });
    }

    /**
     * Handle online event
     */
    async handleOnline() {
        console.log('Connection restored');
        this.isOnline = true;
        this.reconnectAttempts = 0;
        
        // Verify actual connectivity
        const isReallyOnline = await this.verifyConnection();
        if (isReallyOnline) {
            this.showConnectionStatus('online');
            await this.processQueuedRequests();
            this.syncOfflineData();
        } else {
            // False positive, still offline
            this.isOnline = false;
        }
    }

    /**
     * Handle offline event
     */
    handleOffline() {
        console.log('Connection lost');
        this.isOnline = false;
        this.showConnectionStatus('offline');
        this.enableOfflineMode();
    }

    /**
     * Verify actual internet connectivity
     */
    async verifyConnection() {
        try {
            // Try multiple endpoints to ensure connectivity
            const testEndpoints = [
                '/api/health',
                '/api/ping',
                'https://httpbin.org/get',
                'https://jsonplaceholder.typicode.com/posts/1'
            ];

            const results = await Promise.allSettled(
                testEndpoints.map(endpoint => 
                    fetch(endpoint, { 
                        method: 'HEAD',
                        mode: 'no-cors',
                        cache: 'no-cache',
                        signal: AbortSignal.timeout(5000)
                    })
                )
            );

            // Consider online if at least one endpoint responds
            const successCount = results.filter(r => r.status === 'fulfilled').length;
            return successCount > 0;
        } catch (error) {
            return false;
        }
    }

    /**
     * Start connection quality monitoring
     */
    startConnectionMonitoring() {
        this.pingInterval = setInterval(() => {
            this.measureConnectionQuality();
        }, 30000); // Every 30 seconds
    }

    /**
     * Measure connection quality
     */
    async measureConnectionQuality() {
        if (!this.isOnline) return;

        const startTime = performance.now();
        
        try {
            const response = await fetch('/api/ping', {
                method: 'HEAD',
                cache: 'no-cache',
                signal: AbortSignal.timeout(10000)
            });
            
            const endTime = performance.now();
            const latency = endTime - startTime;
            
            this.updateConnectionQuality(latency, response.ok);
            this.lastPingTime = latency;
            
            // Track with performance monitor
            if (window.performanceMonitor) {
                window.performanceMonitor.trackPerformance('connection_latency', latency);
            }
            
        } catch (error) {
            this.updateConnectionQuality(null, false);
            
            // Might be offline
            if (this.isOnline) {
                const reallyOnline = await this.verifyConnection();
                if (!reallyOnline) {
                    this.handleOffline();
                }
            }
        }
    }

    /**
     * Update connection quality assessment
     */
    updateConnectionQuality(latency, success) {
        if (!success) {
            this.connectionQuality = 'poor';
        } else if (latency < 200) {
            this.connectionQuality = 'excellent';
        } else if (latency < 500) {
            this.connectionQuality = 'good';
        } else if (latency < 1000) {
            this.connectionQuality = 'fair';
        } else {
            this.connectionQuality = 'poor';
        }

        // Update UI indicator
        this.updateConnectionIndicator();
    }

    /**
     * Enhanced fetch with offline handling
     */
    async fetch(url, options = {}) {
        const requestId = this.generateRequestId();
        const request = {
            id: requestId,
            url: url,
            options: options,
            timestamp: Date.now(),
            attempts: 0
        };

        if (!this.isOnline) {
            return this.handleOfflineRequest(request);
        }

        try {
            const response = await this.makeRequest(request);
            return response;
        } catch (error) {
            return this.handleRequestError(request, error);
        }
    }

    /**
     * Make actual network request
     */
    async makeRequest(request) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

        try {
            const response = await originalFetch(request.url, {
                ...request.options,
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return response;
        } catch (error) {
            clearTimeout(timeoutId);
            throw error;
        }
    }

    /**
     * Handle offline request
     */
    async handleOfflineRequest(request) {
        // Check if we have cached data
        const cachedResponse = this.getCachedResponse(request.url);
        if (cachedResponse) {
            this.showNotification(
                'Using Cached Data',
                'Displaying previously loaded information',
                'info'
            );
            return cachedResponse;
        }

        // Queue request for later
        this.requestQueue.push(request);
        
        this.showNotification(
            'Request Queued',
            'This request will be processed when connection is restored',
            'warning'
        );

        // Return promise that resolves when connection is restored
        return new Promise((resolve, reject) => {
            request.resolve = resolve;
            request.reject = reject;
        });
    }

    /**
     * Handle request error
     */
    async handleRequestError(request, error) {
        request.attempts++;

        // If it's a network error and we have retries left
        if (this.isNetworkError(error) && request.attempts < 3) {
            const delay = this.baseRetryDelay * Math.pow(2, request.attempts - 1);
            
            this.showNotification(
                'Retrying Request',
                `Attempting to reconnect... (${request.attempts}/3)`,
                'info'
            );

            await this.delay(delay);
            
            try {
                return await this.makeRequest(request);
            } catch (retryError) {
                return this.handleRequestError(request, retryError);
            }
        }

        // All retries failed, queue for offline processing
        this.retryQueue.push(request);
        
        // Check if we have cached data as fallback
        const cachedResponse = this.getCachedResponse(request.url);
        if (cachedResponse) {
            this.showNotification(
                'Using Cached Data',
                'Network request failed, showing cached information',
                'warning'
            );
            return cachedResponse;
        }

        // No cache available, throw error
        throw error;
    }

    /**
     * Process queued requests when connection restored
     */
    async processQueuedRequests() {
        const queue = [...this.requestQueue, ...this.retryQueue];
        this.requestQueue = [];
        this.retryQueue = [];

        if (queue.length === 0) return;

        this.showNotification(
            'Processing Queued Requests',
            `Processing ${queue.length} queued request(s)`,
            'info'
        );

        const results = await Promise.allSettled(
            queue.map(async (request) => {
                try {
                    const response = await this.makeRequest(request);
                    if (request.resolve) {
                        request.resolve(response);
                    }
                    return { success: true, request };
                } catch (error) {
                    if (request.reject) {
                        request.reject(error);
                    }
                    return { success: false, request, error };
                }
            })
        );

        const successful = results.filter(r => r.value?.success).length;
        const failed = results.filter(r => !r.value?.success).length;

        if (successful > 0) {
            this.showNotification(
                'Requests Processed',
                `${successful} request(s) completed successfully`,
                'success'
            );
        }

        if (failed > 0) {
            this.showNotification(
                'Some Requests Failed',
                `${failed} request(s) still need attention`,
                'warning'
            );
        }
    }

    /**
     * Enable offline mode
     */
    enableOfflineMode() {
        // Cache current data
        this.cacheCurrentData();
        
        // Show offline indicator
        this.showOfflineIndicator();
        
        // Disable real-time features
        this.disableRealtimeFeatures();
        
        // Load offline data if available
        this.loadOfflineData();
    }

    /**
     * Cache current data for offline use
     */
    cacheCurrentData() {
        try {
            // Cache dashboard data
            if (window.dashboardData) {
                localStorage.setItem('offline_dashboard_data', JSON.stringify({
                    data: window.dashboardData,
                    timestamp: Date.now(),
                    expires: Date.now() + (24 * 60 * 60 * 1000) // 24 hours
                }));
            }

            // Cache user preferences
            if (window.userPreferences) {
                const preferences = window.userPreferences.preferences;
                localStorage.setItem('offline_preferences', JSON.stringify(preferences));
            }

            // Cache chart data
            if (window.charts) {
                const chartData = {};
                for (const [chartId, chart] of Object.entries(window.charts)) {
                    if (chart.data) {
                        chartData[chartId] = chart.data;
                    }
                }
                localStorage.setItem('offline_chart_data', JSON.stringify(chartData));
            }

        } catch (error) {
            console.error('Failed to cache data for offline use:', error);
        }
    }

    /**
     * Load offline data
     */
    loadOfflineData() {
        try {
            // Load cached dashboard data
            const cachedDashboard = localStorage.getItem('offline_dashboard_data');
            if (cachedDashboard) {
                const data = JSON.parse(cachedDashboard);
                if (data.expires > Date.now()) {
                    window.dashboardData = data.data;
                    this.showNotification(
                        'Offline Data Loaded',
                        'Displaying cached data from your last session',
                        'info'
                    );
                }
            }

        } catch (error) {
            console.error('Failed to load offline data:', error);
        }
    }

    /**
     * Setup service worker for advanced offline functionality
     */
    async setupServiceWorker() {
        if ('serviceWorker' in navigator) {
            try {
                const registration = await navigator.serviceWorker.register('/service-worker.js');
                console.log('Service Worker registered:', registration);
                
                // Listen for service worker messages
                navigator.serviceWorker.addEventListener('message', (event) => {
                    this.handleServiceWorkerMessage(event.data);
                });
                
            } catch (error) {
                console.log('Service Worker registration failed:', error);
            }
        }
    }

    /**
     * Handle service worker messages
     */
    handleServiceWorkerMessage(message) {
        switch (message.type) {
            case 'CACHE_UPDATED':
                this.showNotification(
                    'App Updated',
                    'New version available. Refresh to update.',
                    'info'
                );
                break;
            case 'OFFLINE_READY':
                this.showNotification(
                    'Offline Ready',
                    'App is ready to work offline',
                    'success'
                );
                break;
        }
    }

    /**
     * Utility methods
     */
    generateRequestId() {
        return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    isNetworkError(error) {
        return error instanceof TypeError || 
               error.message.includes('fetch') ||
               error.message.includes('network') ||
               error.name === 'AbortError';
    }

    getCachedResponse(url) {
        try {
            const cacheKey = `cache_${url.replace(/[^a-zA-Z0-9]/g, '_')}`;
            const cached = localStorage.getItem(cacheKey);
            if (cached) {
                const data = JSON.parse(cached);
                if (data.expires > Date.now()) {
                    return new Response(JSON.stringify(data.response), {
                        status: 200,
                        statusText: 'OK (Cached)',
                        headers: { 'Content-Type': 'application/json' }
                    });
                }
            }
        } catch (error) {
            console.error('Failed to get cached response:', error);
        }
        return null;
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * UI update methods
     */
    showConnectionStatus(status) {
        const indicator = this.getConnectionIndicator();
        
        switch (status) {
            case 'online':
                indicator.className = 'connection-indicator online';
                indicator.textContent = '🟢 Online';
                indicator.title = 'Connected to internet';
                break;
            case 'offline':
                indicator.className = 'connection-indicator offline';
                indicator.textContent = '🔴 Offline';
                indicator.title = 'No internet connection';
                break;
            case 'reconnecting':
                indicator.className = 'connection-indicator reconnecting';
                indicator.textContent = '🟡 Reconnecting...';
                indicator.title = 'Attempting to reconnect';
                break;
        }
    }

    updateConnectionIndicator() {
        const indicator = this.getConnectionIndicator();
        
        if (!this.isOnline) return;
        
        const qualityEmojis = {
            excellent: '🟢',
            good: '🟢',
            fair: '🟡',
            poor: '🟠'
        };
        
        const ping = this.lastPingTime ? ` (${Math.round(this.lastPingTime)}ms)` : '';
        indicator.textContent = `${qualityEmojis[this.connectionQuality]} ${this.connectionQuality.charAt(0).toUpperCase() + this.connectionQuality.slice(1)}${ping}`;
        indicator.className = `connection-indicator online ${this.connectionQuality}`;
    }

    getConnectionIndicator() {
        let indicator = document.getElementById('connection-indicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'connection-indicator';
            indicator.className = 'connection-indicator';
            
            // Add to page header or create floating indicator
            const header = document.querySelector('header') || document.querySelector('.demo-header');
            if (header) {
                header.appendChild(indicator);
            } else {
                document.body.appendChild(indicator);
            }
        }
        return indicator;
    }

    showOfflineIndicator() {
        const offlineBar = document.createElement('div');
        offlineBar.id = 'offline-bar';
        offlineBar.className = 'offline-indicator';
        offlineBar.innerHTML = `
            <div class="offline-content">
                <span class="offline-icon">📶</span>
                <span class="offline-text">You're offline. Some features may be limited.</span>
                <button class="retry-connection-btn" onclick="window.connectionManager.retryConnection()">
                    Retry Connection
                </button>
            </div>
        `;
        
        document.body.insertBefore(offlineBar, document.body.firstChild);
    }

    hideOfflineIndicator() {
        const offlineBar = document.getElementById('offline-bar');
        if (offlineBar) {
            offlineBar.remove();
        }
    }

    disableRealtimeFeatures() {
        // Disable WebSocket connections
        if (window.demoWebSocket) {
            window.demoWebSocket.disconnectAll();
        }
        
        // Disable real-time buttons
        const realtimeButtons = document.querySelectorAll('[id*="realtime"], [data-realtime]');
        realtimeButtons.forEach(btn => {
            btn.disabled = true;
            btn.title = 'Unavailable offline';
        });
    }

    enableRealtimeFeatures() {
        // Re-enable real-time buttons
        const realtimeButtons = document.querySelectorAll('[id*="realtime"], [data-realtime]');
        realtimeButtons.forEach(btn => {
            btn.disabled = false;
            btn.title = '';
        });
    }

    async retryConnection() {
        this.showConnectionStatus('reconnecting');
        
        const isOnline = await this.verifyConnection();
        if (isOnline) {
            this.handleOnline();
            this.hideOfflineIndicator();
            this.enableRealtimeFeatures();
        } else {
            this.showNotification(
                'Still Offline',
                'Connection could not be established. Will keep trying automatically.',
                'warning'
            );
            this.showConnectionStatus('offline');
        }
    }

    showNotification(title, message, type = 'info') {
        if (window.demoWebSocket?.showNotification) {
            window.demoWebSocket.showNotification(title, message, type);
        } else if (window.errorHandler?.showFallbackNotification) {
            window.errorHandler.showFallbackNotification(`${title}: ${message}`, type);
        }
    }

    /**
     * Sync offline data when connection restored
     */
    async syncOfflineData() {
        const offlineData = this.getOfflineDataToSync();
        if (offlineData.length === 0) return;

        this.showNotification(
            'Syncing Data',
            'Synchronizing offline changes...',
            'info'
        );

        try {
            const results = await Promise.allSettled(
                offlineData.map(data => this.syncDataItem(data))
            );

            const successful = results.filter(r => r.status === 'fulfilled').length;
            
            this.showNotification(
                'Sync Complete',
                `${successful}/${offlineData.length} items synchronized`,
                'success'
            );

        } catch (error) {
            this.showNotification(
                'Sync Failed',
                'Some offline data could not be synchronized',
                'error'
            );
        }
    }

    getOfflineDataToSync() {
        // Return any data that was modified while offline
        // This would be implementation-specific
        return [];
    }

    async syncDataItem(data) {
        // Sync individual data item
        // Implementation would depend on the data type
        return Promise.resolve();
    }

    saveOfflineData() {
        // Save any pending offline data before page unload
        try {
            const pendingData = {
                requestQueue: this.requestQueue,
                retryQueue: this.retryQueue,
                timestamp: Date.now()
            };
            
            localStorage.setItem('pending_offline_data', JSON.stringify(pendingData));
        } catch (error) {
            console.error('Failed to save offline data:', error);
        }
    }

    /**
     * Get connection statistics
     */
    getConnectionStats() {
        return {
            isOnline: this.isOnline,
            connectionQuality: this.connectionQuality,
            lastPingTime: this.lastPingTime,
            queuedRequests: this.requestQueue.length,
            retryQueue: this.retryQueue.length,
            reconnectAttempts: this.reconnectAttempts
        };
    }
}

// CSS for connection indicators
const connectionStyles = `
    .connection-indicator {
        position: fixed;
        top: 10px;
        right: 10px;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 1rem;
        font-size: 0.75rem;
        font-weight: 500;
        z-index: 9999;
        transition: all 0.3s ease;
    }

    .connection-indicator.online {
        background: rgba(16, 185, 129, 0.9);
    }

    .connection-indicator.offline {
        background: rgba(239, 68, 68, 0.9);
    }

    .connection-indicator.reconnecting {
        background: rgba(245, 158, 11, 0.9);
        animation: pulse 2s infinite;
    }

    .offline-indicator {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: #fbbf24;
        color: #92400e;
        z-index: 9998;
        animation: slideDown 0.3s ease-out;
    }

    .offline-content {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        padding: 0.75rem;
        font-size: 0.875rem;
        font-weight: 500;
    }

    .retry-connection-btn {
        background: #92400e;
        color: white;
        border: none;
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        cursor: pointer;
        font-size: 0.75rem;
    }

    .retry-connection-btn:hover {
        background: #78350f;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    @keyframes slideDown {
        from {
            transform: translateY(-100%);
        }
        to {
            transform: translateY(0);
        }
    }
`;

// Inject styles
if (!document.querySelector('#connection-manager-styles')) {
    const styleSheet = document.createElement('style');
    styleSheet.id = 'connection-manager-styles';
    styleSheet.textContent = connectionStyles;
    document.head.appendChild(styleSheet);
}

// Save original fetch before overriding
const originalFetch = window.fetch;

// Global connection manager instance
window.connectionManager = new ConnectionManager();

// Replace global fetch with connection-aware version
window.fetch = (url, options) => {
    return window.connectionManager.fetch(url, options);
};

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ConnectionManager;
}