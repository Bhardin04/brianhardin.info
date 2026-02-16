/**
 * Real-time Performance Monitor
 * Monitors system performance, WebSocket connections, and user experience metrics
 */

class PerformanceMonitor {
    constructor() {
        this.metrics = new Map();
        this.alerts = [];
        this.thresholds = {
            fps: { warning: 45, critical: 30 },
            memory: { warning: 0.8, critical: 0.9 }, // Percentage of heap limit
            responseTime: { warning: 1000, critical: 2000 }, // milliseconds
            websocketLatency: { warning: 200, critical: 500 }, // milliseconds
            errorRate: { warning: 0.05, critical: 0.1 }, // 5% and 10%
            loadTime: { warning: 3000, critical: 5000 } // milliseconds
        };
        this.isMonitoring = false;
        this.monitoringInterval = null;
        this.performanceHistory = [];
        this.maxHistorySize = 100;

        this.initialize();
    }

    /**
     * Initialize performance monitoring
     */
    initialize() {
        this.startMonitoring();
        this.setupPerformanceObservers();
        this.trackInitialMetrics();
    }

    /**
     * Start monitoring
     */
    startMonitoring() {
        if (this.isMonitoring) return;

        this.isMonitoring = true;
        this.monitoringInterval = setInterval(() => {
            this.collectMetrics();
        }, 15000); // Collect metrics every 15 seconds instead of 5

        console.log('Performance monitoring started');
    }

    /**
     * Stop monitoring
     */
    stopMonitoring() {
        if (!this.isMonitoring) return;

        this.isMonitoring = false;
        if (this.monitoringInterval) {
            clearInterval(this.monitoringInterval);
            this.monitoringInterval = null;
        }

        console.log('Performance monitoring stopped');
    }

    /**
     * Collect current performance metrics
     */
    collectMetrics() {
        const timestamp = Date.now();
        const metrics = {
            timestamp: timestamp,
            memory: this.getMemoryMetrics(),
            timing: this.getTimingMetrics(),
            network: this.getNetworkMetrics(),
            rendering: this.getRenderingMetrics(),
            errors: this.getErrorMetrics(),
            websocket: this.getWebSocketMetrics()
        };

        this.metrics.set(timestamp, metrics);
        this.addToHistory(metrics);
        this.checkThresholds(metrics);

        // Track with analytics
        if (window.demoAnalytics) {
            window.demoAnalytics.trackPerformance('system_metrics', metrics);
        }

        return metrics;
    }

    /**
     * Get memory usage metrics
     */
    getMemoryMetrics() {
        if (!window.performance || !window.performance.memory) {
            return { available: false };
        }

        const memory = window.performance.memory;
        return {
            available: true,
            used: memory.usedJSHeapSize,
            total: memory.totalJSHeapSize,
            limit: memory.jsHeapSizeLimit,
            usagePercentage: (memory.usedJSHeapSize / memory.jsHeapSizeLimit) * 100,
            efficiency: (memory.usedJSHeapSize / memory.totalJSHeapSize) * 100
        };
    }

    /**
     * Get timing metrics
     */
    getTimingMetrics() {
        if (!window.performance || !window.performance.getEntriesByType) {
            return { available: false };
        }

        const navigation = window.performance.getEntriesByType('navigation')[0];
        if (!navigation) {
            return { available: false };
        }

        return {
            available: true,
            loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
            domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
            totalPageLoad: navigation.loadEventEnd - navigation.fetchStart,
            timeToFirstByte: navigation.responseStart - navigation.requestStart,
            domProcessing: navigation.domComplete - navigation.domLoading,
            resourceLoad: navigation.loadEventStart - navigation.domContentLoadedEventEnd
        };
    }

    /**
     * Get network performance metrics
     */
    getNetworkMetrics() {
        if (!window.performance || !window.performance.getEntriesByType) {
            return { available: false };
        }

        const resources = window.performance.getEntriesByType('resource');
        if (resources.length === 0) {
            return { available: false };
        }

        const recent = resources.slice(-10); // Last 10 resources
        const totalSize = recent.reduce((sum, r) => sum + (r.transferSize || 0), 0);
        const avgDuration = recent.reduce((sum, r) => sum + r.duration, 0) / recent.length;

        return {
            available: true,
            recentResourceCount: recent.length,
            totalResourceSize: totalSize,
            averageLoadTime: avgDuration,
            slowestResource: Math.max(...recent.map(r => r.duration)),
            resourceTypes: this.categorizeResources(recent)
        };
    }

    /**
     * Get rendering performance metrics
     */
    getRenderingMetrics() {
        if (!window.performance || !window.performance.getEntriesByType) {
            return { available: false };
        }

        // Get paint metrics
        const paintEntries = window.performance.getEntriesByType('paint');
        const paintMetrics = {};
        paintEntries.forEach(entry => {
            paintMetrics[entry.name.replace('-', '_')] = entry.startTime;
        });

        // Get layout shift metrics if available
        const layoutShifts = window.performance.getEntriesByType('layout-shift');
        const cumulativeLayoutShift = layoutShifts.reduce((sum, entry) => {
            if (!entry.hadRecentInput) {
                return sum + entry.value;
            }
            return sum;
        }, 0);

        return {
            available: true,
            paintMetrics: paintMetrics,
            layoutShifts: layoutShifts.length,
            cumulativeLayoutShift: cumulativeLayoutShift,
            renderingFrames: this.getCurrentFPS()
        };
    }

    /**
     * Get error metrics
     */
    getErrorMetrics() {
        const errorKey = 'performance_errors';
        const errors = this.metrics.get(errorKey) || { count: 0, recent: [] };

        return {
            totalErrors: errors.count,
            recentErrors: errors.recent.slice(-5), // Last 5 errors
            errorRate: this.calculateErrorRate()
        };
    }

    /**
     * Get WebSocket performance metrics
     */
    getWebSocketMetrics() {
        if (!window.demoWebSocket) {
            return { available: false };
        }

        const stats = window.demoWebSocket.getStats ? window.demoWebSocket.getStats() : {};
        return {
            available: true,
            connections: stats.totalConnections || 0,
            activeHeartbeats: stats.activeHeartbeats || 0,
            messageHandlers: stats.messageHandlers || 0,
            latency: this.getWebSocketLatency(),
            connectionStability: this.getConnectionStability()
        };
    }

    /**
     * Categorize resources by type
     */
    categorizeResources(resources) {
        const categories = {};
        resources.forEach(resource => {
            const type = resource.initiatorType || 'other';
            if (!categories[type]) {
                categories[type] = { count: 0, totalSize: 0, totalDuration: 0 };
            }
            categories[type].count++;
            categories[type].totalSize += resource.transferSize || 0;
            categories[type].totalDuration += resource.duration || 0;
        });
        return categories;
    }

    /**
     * Get current FPS estimate
     */
    getCurrentFPS() {
        // This is a simplified FPS calculation
        // In a real implementation, you'd track frame timestamps
        return this.lastFPS || 60;
    }

    /**
     * Calculate error rate
     */
    calculateErrorRate() {
        const recentMetrics = this.getRecentMetrics(10);
        if (recentMetrics.length === 0) return 0;

        const totalEvents = recentMetrics.reduce((sum, m) => sum + (m.eventCount || 0), 0);
        const totalErrors = recentMetrics.reduce((sum, m) => sum + (m.errors?.totalErrors || 0), 0);

        return totalEvents > 0 ? totalErrors / totalEvents : 0;
    }

    /**
     * Get WebSocket latency
     */
    getWebSocketLatency() {
        // This would be measured by ping/pong messages
        // For now, return a placeholder
        return this.lastWebSocketLatency || 0;
    }

    /**
     * Get connection stability score
     */
    getConnectionStability() {
        // Calculate based on reconnection attempts, message failures, etc.
        const recentMetrics = this.getRecentMetrics(5);
        if (recentMetrics.length === 0) return 1.0;

        // Simple stability calculation (1.0 = perfect, 0.0 = completely unstable)
        return 0.95; // Placeholder
    }

    /**
     * Check performance thresholds and create alerts
     */
    checkThresholds(metrics) {
        const alerts = [];

        // Check memory usage
        if (metrics.memory.available && metrics.memory.usagePercentage > this.thresholds.memory.critical * 100) {
            alerts.push(this.createAlert('critical', 'memory', 'High memory usage detected', metrics.memory));
        } else if (metrics.memory.available && metrics.memory.usagePercentage > this.thresholds.memory.warning * 100) {
            alerts.push(this.createAlert('warning', 'memory', 'Memory usage is elevated', metrics.memory));
        }

        // Check rendering performance
        if (metrics.rendering.renderingFrames < this.thresholds.fps.critical) {
            alerts.push(this.createAlert('critical', 'rendering', 'Low FPS detected', { fps: metrics.rendering.renderingFrames }));
        } else if (metrics.rendering.renderingFrames < this.thresholds.fps.warning) {
            alerts.push(this.createAlert('warning', 'rendering', 'FPS below optimal', { fps: metrics.rendering.renderingFrames }));
        }

        // Check error rate
        const errorRate = this.calculateErrorRate();
        if (errorRate > this.thresholds.errorRate.critical) {
            alerts.push(this.createAlert('critical', 'errors', 'High error rate detected', { rate: errorRate }));
        } else if (errorRate > this.thresholds.errorRate.warning) {
            alerts.push(this.createAlert('warning', 'errors', 'Elevated error rate', { rate: errorRate }));
        }

        // Check WebSocket latency
        if (metrics.websocket.available && metrics.websocket.latency > this.thresholds.websocketLatency.critical) {
            alerts.push(this.createAlert('critical', 'websocket', 'High WebSocket latency', { latency: metrics.websocket.latency }));
        }

        // Add alerts and trigger notifications
        alerts.forEach(alert => {
            this.addAlert(alert);
            this.triggerAlert(alert);
        });
    }

    /**
     * Create performance alert
     */
    createAlert(severity, category, message, data) {
        return {
            id: `alert_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            severity: severity,
            category: category,
            message: message,
            data: data,
            timestamp: Date.now(),
            resolved: false
        };
    }

    /**
     * Add alert to alerts list
     */
    addAlert(alert) {
        this.alerts.push(alert);

        // Keep only recent alerts (last 50)
        if (this.alerts.length > 50) {
            this.alerts = this.alerts.slice(-50);
        }

        // Track with analytics
        if (window.demoAnalytics) {
            window.demoAnalytics.trackEvent('performance_alert', alert);
        }
    }

    /**
     * Trigger alert notification
     */
    triggerAlert(alert) {
        // Only show critical alerts to avoid spam
        if (alert.severity === 'critical' && window.demoWebSocket?.showNotification) {
            window.demoWebSocket.showNotification(
                'Performance Alert',
                alert.message,
                'error'
            );
        }

        console.warn(`Performance Alert [${alert.severity.toUpperCase()}]:`, alert.message, alert.data);
    }

    /**
     * Setup performance observers
     */
    setupPerformanceObservers() {
        // Observer for layout shifts
        if ('PerformanceObserver' in window) {
            try {
                const layoutShiftObserver = new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        if (entry.hadRecentInput) continue;

                        if (window.demoAnalytics) {
                            window.demoAnalytics.trackPerformance('layout_shift', {
                                value: entry.value,
                                sources: entry.sources?.map(source => ({
                                    node: source.node?.tagName,
                                    currentRect: source.currentRect,
                                    previousRect: source.previousRect
                                }))
                            });
                        }
                    }
                });

                layoutShiftObserver.observe({ entryTypes: ['layout-shift'] });
            } catch (error) {
                console.warn('Layout shift observer not supported:', error);
            }

            // Observer for largest contentful paint
            try {
                const lcpObserver = new PerformanceObserver((list) => {
                    const entries = list.getEntries();
                    const lastEntry = entries[entries.length - 1];

                    if (window.demoAnalytics) {
                        window.demoAnalytics.trackPerformance('largest_contentful_paint', {
                            startTime: lastEntry.startTime,
                            size: lastEntry.size,
                            element: lastEntry.element?.tagName
                        });
                    }
                });

                lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
            } catch (error) {
                console.warn('LCP observer not supported:', error);
            }
        }
    }

    /**
     * Track initial metrics
     */
    trackInitialMetrics() {
        // Track initial page load performance
        window.addEventListener('load', () => {
            setTimeout(() => {
                const metrics = this.collectMetrics();
                console.log('Initial performance metrics:', metrics);
            }, 1000);
        });
    }

    /**
     * Add metrics to history
     */
    addToHistory(metrics) {
        this.performanceHistory.push(metrics);

        if (this.performanceHistory.length > this.maxHistorySize) {
            this.performanceHistory.shift();
        }
    }

    /**
     * Get recent metrics
     */
    getRecentMetrics(count = 10) {
        return this.performanceHistory.slice(-count);
    }

    /**
     * Get performance summary
     */
    getPerformanceSummary() {
        const recent = this.getRecentMetrics(10);
        if (recent.length === 0) return null;

        const summary = {
            timestamp: Date.now(),
            averageMemoryUsage: this.calculateAverage(recent, 'memory.usagePercentage'),
            averageFPS: this.calculateAverage(recent, 'rendering.renderingFrames'),
            totalErrors: recent.reduce((sum, m) => sum + (m.errors?.totalErrors || 0), 0),
            alertCount: this.alerts.filter(a => !a.resolved).length,
            connectionStability: this.calculateAverage(recent, 'websocket.connectionStability'),
            recommendations: this.generateRecommendations(recent)
        };

        return summary;
    }

    /**
     * Calculate average of a nested property
     */
    calculateAverage(metrics, property) {
        const values = metrics
            .map(m => this.getNestedProperty(m, property))
            .filter(v => v !== null && v !== undefined);

        return values.length > 0 ? values.reduce((sum, v) => sum + v, 0) / values.length : 0;
    }

    /**
     * Get nested property value
     */
    getNestedProperty(obj, path) {
        return path.split('.').reduce((current, key) => current?.[key], obj);
    }

    /**
     * Generate performance recommendations
     */
    generateRecommendations(metrics) {
        const recommendations = [];
        const latest = metrics[metrics.length - 1];

        if (latest.memory.available && latest.memory.usagePercentage > 70) {
            recommendations.push({
                type: 'memory',
                message: 'Consider reducing memory usage by clearing unused data or optimizing data structures',
                priority: 'medium'
            });
        }

        if (latest.rendering.renderingFrames < 50) {
            recommendations.push({
                type: 'rendering',
                message: 'Performance issues detected. Consider reducing visual complexity or disabling animations',
                priority: 'high'
            });
        }

        if (latest.network.available && latest.network.averageLoadTime > 1000) {
            recommendations.push({
                type: 'network',
                message: 'Slow network performance detected. Consider optimizing resource loading',
                priority: 'medium'
            });
        }

        return recommendations;
    }

    /**
     * Export performance data
     */
    exportPerformanceData() {
        const exportData = {
            summary: this.getPerformanceSummary(),
            history: this.performanceHistory,
            alerts: this.alerts,
            thresholds: this.thresholds,
            exportedAt: new Date().toISOString()
        };

        const blob = new Blob([JSON.stringify(exportData, null, 2)], {
            type: 'application/json'
        });

        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `performance_data_${new Date().toISOString().split('T')[0]}.json`;

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        URL.revokeObjectURL(url);
    }

    /**
     * Track custom performance metrics
     */
    trackPerformance(metric, value, context = {}) {
        try {
            const performanceData = {
                metric: metric,
                value: value,
                context: context,
                timestamp: Date.now()
            };

            // Store the metric for internal tracking
            const key = `custom_${metric}`;
            if (!this.metrics.has(key)) {
                this.metrics.set(key, []);
            }

            const metricHistory = this.metrics.get(key);
            metricHistory.push(performanceData);

            // Keep only recent entries
            if (metricHistory.length > 100) {
                metricHistory.shift();
            }

            // Track with analytics if available
            if (window.demoAnalytics) {
                window.demoAnalytics.trackPerformance(metric, value, context);
            }

            return performanceData;
        } catch (error) {
            console.warn('Error tracking performance metric:', error);
            return null;
        }
    }

    /**
     * Get current performance status
     */
    getStatus() {
        const recent = this.getRecentMetrics(1)[0];
        if (!recent) return 'unknown';

        const criticalAlerts = this.alerts.filter(a => !a.resolved && a.severity === 'critical');
        const warningAlerts = this.alerts.filter(a => !a.resolved && a.severity === 'warning');

        if (criticalAlerts.length > 0) return 'critical';
        if (warningAlerts.length > 0) return 'warning';
        return 'good';
    }
}

// Global performance monitor instance
window.performanceMonitor = new PerformanceMonitor();

// Auto-cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.performanceMonitor) {
        window.performanceMonitor.stopMonitoring();
    }
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PerformanceMonitor;
}
