/**
 * Demo Analytics and Performance Tracker
 * Tracks user interactions, performance metrics, and engagement data
 */

class DemoAnalyticsTracker {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.userId = this.getUserId();
        this.startTime = Date.now();
        this.events = [];
        this.performanceMetrics = new Map();
        this.interactionHeatmap = new Map();
        this.pageViews = [];
        this.currentDemo = null;
        this.batchSize = 20; // Smaller batches
        this.sendInterval = 120000; // 2 minutes instead of 30 seconds
        this.maxRetries = 3;
        
        this.initializeTracking();
    }

    /**
     * Generate unique session ID
     */
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    /**
     * Get or create user ID
     */
    getUserId() {
        let userId = localStorage.getItem('demo_user_id');
        if (!userId) {
            userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('demo_user_id', userId);
        }
        return userId;
    }

    /**
     * Initialize tracking
     */
    initializeTracking() {
        this.trackPageView();
        this.setupEventListeners();
        this.startPerformanceMonitoring();
        this.startBatchSending();
        
        // Track initial page load performance
        this.trackPageLoadPerformance();
    }

    /**
     * Track page view
     */
    trackPageView() {
        const pageView = {
            type: 'page_view',
            url: window.location.href,
            path: window.location.pathname,
            referrer: document.referrer,
            timestamp: Date.now(),
            userAgent: navigator.userAgent,
            screenResolution: `${screen.width}x${screen.height}`,
            viewportSize: `${window.innerWidth}x${window.innerHeight}`,
            language: navigator.language,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
        };
        
        this.pageViews.push(pageView);
        this.trackEvent('page_view', pageView);
    }

    /**
     * Track demo initialization
     */
    trackDemoStart(demoType, sessionId, metadata = {}) {
        this.currentDemo = {
            type: demoType,
            sessionId: sessionId,
            startTime: Date.now(),
            interactions: 0,
            errors: 0,
            exports: 0,
            features: new Set()
        };

        this.trackEvent('demo_start', {
            demoType: demoType,
            demoSessionId: sessionId,
            metadata: metadata,
            timestamp: Date.now()
        });
    }

    /**
     * Track demo completion
     */
    trackDemoComplete(demoType, sessionId, completionData = {}) {
        const duration = Date.now() - (this.currentDemo?.startTime || 0);
        
        this.trackEvent('demo_complete', {
            demoType: demoType,
            demoSessionId: sessionId,
            duration: duration,
            interactions: this.currentDemo?.interactions || 0,
            errorsEncountered: this.currentDemo?.errors || 0,
            exportsPerformed: this.currentDemo?.exports || 0,
            featuresUsed: Array.from(this.currentDemo?.features || []),
            completionData: completionData,
            timestamp: Date.now()
        });
    }

    /**
     * Track user interaction
     */
    trackInteraction(element, action, data = {}) {
        if (this.currentDemo) {
            this.currentDemo.interactions++;
        }

        // Track interaction heatmap data
        if (element && element.getBoundingClientRect) {
            const rect = element.getBoundingClientRect();
            const heatmapKey = `${Math.floor(rect.left / 50)},${Math.floor(rect.top / 50)}`;
            const currentCount = this.interactionHeatmap.get(heatmapKey) || 0;
            this.interactionHeatmap.set(heatmapKey, currentCount + 1);
        }

        this.trackEvent('interaction', {
            elementType: element?.tagName?.toLowerCase(),
            elementId: element?.id,
            elementClass: element?.className,
            action: action,
            data: data,
            position: element ? {
                x: element.getBoundingClientRect().left,
                y: element.getBoundingClientRect().top
            } : null,
            timestamp: Date.now()
        });
    }

    /**
     * Track feature usage
     */
    trackFeatureUsage(feature, details = {}) {
        if (this.currentDemo) {
            this.currentDemo.features.add(feature);
        }

        this.trackEvent('feature_usage', {
            feature: feature,
            details: details,
            demoType: this.currentDemo?.type,
            timestamp: Date.now()
        });
    }

    /**
     * Track export action
     */
    trackExport(format, chartId, success = true, details = {}) {
        if (this.currentDemo) {
            this.currentDemo.exports++;
        }

        this.trackEvent('export', {
            format: format,
            chartId: chartId,
            success: success,
            details: details,
            demoType: this.currentDemo?.type,
            timestamp: Date.now()
        });

        // Track to user preferences as well
        if (window.userPreferences) {
            window.userPreferences.trackExport(format);
        }
    }

    /**
     * Track error occurrence
     */
    trackError(error, context = {}) {
        if (this.currentDemo) {
            this.currentDemo.errors++;
        }

        this.trackEvent('error', {
            message: error.message || error,
            stack: error.stack,
            context: context,
            demoType: this.currentDemo?.type,
            url: window.location.href,
            userAgent: navigator.userAgent,
            timestamp: Date.now()
        });
    }

    /**
     * Track performance metrics
     */
    trackPerformance(metric, value, context = {}) {
        const performanceData = {
            metric: metric,
            value: value,
            context: context,
            timestamp: Date.now(),
            demoType: this.currentDemo?.type
        };

        this.performanceMetrics.set(`${metric}_${Date.now()}`, performanceData);
        this.trackEvent('performance', performanceData);
    }

    /**
     * Track WebSocket connection metrics
     */
    trackWebSocketMetrics(event, data = {}) {
        this.trackEvent('websocket', {
            event: event,
            data: data,
            demoType: this.currentDemo?.type,
            timestamp: Date.now()
        });
    }

    /**
     * Track chart interaction
     */
    trackChartInteraction(chartId, interactionType, data = {}) {
        this.trackEvent('chart_interaction', {
            chartId: chartId,
            interactionType: interactionType, // 'drill_down', 'zoom', 'export', 'hover'
            data: data,
            demoType: this.currentDemo?.type,
            timestamp: Date.now()
        });
    }

    /**
     * Track search/filter usage
     */
    trackSearch(query, results, context = {}) {
        this.trackEvent('search', {
            query: query,
            resultCount: results,
            context: context,
            demoType: this.currentDemo?.type,
            timestamp: Date.now()
        });
    }

    /**
     * Track user preferences changes
     */
    trackPreferenceChange(preference, oldValue, newValue) {
        this.trackEvent('preference_change', {
            preference: preference,
            oldValue: oldValue,
            newValue: newValue,
            timestamp: Date.now()
        });
    }

    /**
     * Generic event tracking
     */
    trackEvent(eventType, data = {}) {
        const event = {
            sessionId: this.sessionId,
            userId: this.userId,
            eventType: eventType,
            data: data,
            timestamp: Date.now(),
            url: window.location.href,
            demoType: this.currentDemo?.type || null
        };

        this.events.push(event);
        
        // Console log for development
        if (this.isDevelopment()) {
            console.log('Analytics Event:', event);
        }
    }

    /**
     * Track page load performance
     */
    trackPageLoadPerformance() {
        window.addEventListener('load', () => {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                if (perfData) {
                    this.trackPerformance('page_load', {
                        loadTime: perfData.loadEventEnd - perfData.loadEventStart,
                        domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
                        totalTime: perfData.loadEventEnd - perfData.fetchStart,
                        dnsTime: perfData.domainLookupEnd - perfData.domainLookupStart,
                        connectTime: perfData.connectEnd - perfData.connectStart,
                        responseTime: perfData.responseEnd - perfData.responseStart
                    });
                }
            }, 1000);
        });
    }

    /**
     * Setup event listeners for automatic tracking
     */
    setupEventListeners() {
        // Track clicks - exclude navigation links to prevent blocking
        document.addEventListener('click', (e) => {
            if (e.target.tagName === 'BUTTON' || e.target.tagName === 'A' || 
                e.target.hasAttribute('data-track') || e.target.closest('[data-track]')) {
                
                // Skip tracking for navigation links that leave the demo pages
                if (e.target.tagName === 'A' && e.target.href) {
                    const href = e.target.href;
                    if (href.includes('/demos') || href.includes('/projects') || href.includes('/contact') || 
                        href.includes('/about') || href.includes('/resume') || href.includes('/blog')) {
                        console.log('Skipping analytics for navigation link to prevent blocking');
                        return;
                    }
                }
                
                // Track other interactions normally
                this.trackInteraction(e.target, 'click');
            }
        }, { passive: true });

        // Track form submissions
        document.addEventListener('submit', (e) => {
            this.trackInteraction(e.target, 'submit');
        });

        // Track input changes on key form elements
        document.addEventListener('change', (e) => {
            if (e.target.tagName === 'SELECT' || e.target.type === 'checkbox' || 
                e.target.type === 'radio' || e.target.hasAttribute('data-track-change')) {
                this.trackInteraction(e.target, 'change', {
                    value: e.target.value || e.target.checked
                });
            }
        });

        // Track window resize
        window.addEventListener('resize', () => {
            this.trackEvent('viewport_resize', {
                width: window.innerWidth,
                height: window.innerHeight
            });
        });

        // Track page visibility changes
        document.addEventListener('visibilitychange', () => {
            this.trackEvent('visibility_change', {
                hidden: document.hidden,
                visibilityState: document.visibilityState
            });
        });

        // Track scroll depth
        let maxScrollDepth = 0;
        window.addEventListener('scroll', () => {
            const scrollDepth = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
            if (scrollDepth > maxScrollDepth) {
                maxScrollDepth = scrollDepth;
                if (scrollDepth % 25 === 0) { // Track at 25%, 50%, 75%, 100%
                    this.trackEvent('scroll_depth', { depth: scrollDepth });
                }
            }
        });
    }

    /**
     * Start performance monitoring
     */
    startPerformanceMonitoring() {
        // Monitor memory usage (if available)
        setInterval(() => {
            if (performance.memory) {
                this.trackPerformance('memory_usage', {
                    used: performance.memory.usedJSHeapSize,
                    total: performance.memory.totalJSHeapSize,
                    limit: performance.memory.jsHeapSizeLimit
                });
            }
        }, 60000); // Every minute

        // Monitor FPS (rough approximation)
        this.monitorFPS();

        // Monitor resource performance
        this.monitorResourcePerformance();
    }

    /**
     * Monitor FPS
     */
    monitorFPS() {
        let lastTime = performance.now();
        let frameCount = 0;
        let measurementCount = 0;
        const maxMeasurements = 10; // Only measure for 10 seconds, then stop
        
        const measureFPS = (currentTime) => {
            frameCount++;
            
            if (currentTime - lastTime >= 5000) { // Every 5 seconds instead of 1
                const fps = Math.round((frameCount * 1000) / (currentTime - lastTime));
                this.trackPerformance('fps', fps);
                
                frameCount = 0;
                lastTime = currentTime;
                measurementCount++;
                
                // Stop aggressive FPS monitoring after initial measurements
                if (measurementCount >= maxMeasurements) {
                    return; // Stop the loop
                }
            }
            
            requestAnimationFrame(measureFPS);
        };
        
        requestAnimationFrame(measureFPS);
    }

    /**
     * Monitor resource performance
     */
    monitorResourcePerformance() {
        // Monitor resource loading times
        const observer = new PerformanceObserver((list) => {
            list.getEntries().forEach((entry) => {
                if (entry.entryType === 'resource') {
                    this.trackPerformance('resource_load', {
                        name: entry.name,
                        duration: entry.duration,
                        size: entry.transferSize,
                        type: entry.initiatorType
                    });
                }
            });
        });
        
        observer.observe({ entryTypes: ['resource'] });
    }

    /**
     * Start batch sending of analytics data
     */
    startBatchSending() {
        setInterval(() => {
            this.sendBatch();
        }, this.sendInterval);

        // Send on page unload
        window.addEventListener('beforeunload', () => {
            this.sendBatch(true);
        });
    }

    /**
     * Send batch of analytics data
     */
    async sendBatch(isUnloading = false) {
        if (this.events.length === 0) return;

        const batch = {
            sessionId: this.sessionId,
            userId: this.userId,
            events: this.events.splice(0, this.batchSize),
            performanceMetrics: Array.from(this.performanceMetrics.values()),
            heatmapData: Object.fromEntries(this.interactionHeatmap),
            sessionInfo: {
                startTime: this.startTime,
                duration: Date.now() - this.startTime,
                pageViews: this.pageViews.length,
                currentDemo: this.currentDemo
            },
            timestamp: Date.now()
        };

        try {
            // Use sendBeacon if available and unloading
            if (isUnloading && navigator.sendBeacon) {
                navigator.sendBeacon('/api/analytics', JSON.stringify(batch));
            } else {
                await this.sendAnalyticsData(batch);
            }
            
            // Clear sent data
            this.performanceMetrics.clear();
            
        } catch (error) {
            console.error('Failed to send analytics batch:', error);
            // Re-add events to queue for retry
            this.events.unshift(...batch.events);
        }
    }

    /**
     * Send analytics data to server
     */
    async sendAnalyticsData(data, retryCount = 0) {
        try {
            const response = await fetch('/api/analytics', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`Analytics request failed: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            if (retryCount < this.maxRetries) {
                console.warn(`Analytics send retry ${retryCount + 1}/${this.maxRetries}`);
                await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, retryCount)));
                return this.sendAnalyticsData(data, retryCount + 1);
            }
            throw error;
        }
    }

    /**
     * Get analytics summary
     */
    getAnalyticsSummary() {
        return {
            sessionId: this.sessionId,
            userId: this.userId,
            sessionDuration: Date.now() - this.startTime,
            eventCount: this.events.length,
            currentDemo: this.currentDemo,
            pageViews: this.pageViews.length,
            interactionPoints: this.interactionHeatmap.size,
            performanceMetrics: this.performanceMetrics.size
        };
    }

    /**
     * Export analytics data
     */
    exportAnalyticsData() {
        const exportData = {
            sessionInfo: {
                sessionId: this.sessionId,
                userId: this.userId,
                startTime: this.startTime,
                duration: Date.now() - this.startTime
            },
            events: this.events,
            performanceMetrics: Array.from(this.performanceMetrics.values()),
            heatmapData: Object.fromEntries(this.interactionHeatmap),
            pageViews: this.pageViews,
            currentDemo: this.currentDemo,
            exportedAt: new Date().toISOString()
        };

        const blob = new Blob([JSON.stringify(exportData, null, 2)], {
            type: 'application/json'
        });

        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `analytics_${this.sessionId}_${new Date().toISOString().split('T')[0]}.json`;
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        URL.revokeObjectURL(url);
    }

    /**
     * Check if in development mode
     */
    isDevelopment() {
        return window.location.hostname === 'localhost' || 
               window.location.hostname === '127.0.0.1' ||
               window.location.protocol === 'file:';
    }

    /**
     * Enable or disable tracking
     */
    setTrackingEnabled(enabled) {
        this.trackingEnabled = enabled;
        if (enabled) {
            this.trackEvent('tracking_enabled');
        } else {
            this.trackEvent('tracking_disabled');
        }
    }

    /**
     * Get heatmap data for visualization
     */
    getHeatmapData() {
        return Object.fromEntries(this.interactionHeatmap);
    }

    /**
     * Clear all analytics data
     */
    clearData() {
        this.events = [];
        this.performanceMetrics.clear();
        this.interactionHeatmap.clear();
        this.pageViews = [];
        this.trackEvent('data_cleared');
    }
}

// Global analytics instance
window.demoAnalytics = new DemoAnalyticsTracker();

// Auto-track common demo events
document.addEventListener('DOMContentLoaded', () => {
    // Track user preferences changes
    document.addEventListener('preferencesChanged', (e) => {
        window.demoAnalytics.trackEvent('preferences_changed', e.detail);
    });

    // Track chart events
    document.addEventListener('chart:drilldown', (e) => {
        window.demoAnalytics.trackChartInteraction(e.detail.chartId, 'drill_down', e.detail);
    });

    document.addEventListener('chart:drillup', (e) => {
        window.demoAnalytics.trackChartInteraction(e.detail.chartId, 'drill_up', e.detail);
    });

    document.addEventListener('chart:filter', (e) => {
        window.demoAnalytics.trackChartInteraction(e.detail.chartId, 'filter', e.detail);
    });

    // Track WebSocket events
    document.addEventListener('websocket:connected', (e) => {
        window.demoAnalytics.trackWebSocketMetrics('connected', e.detail);
    });

    document.addEventListener('websocket:disconnected', (e) => {
        window.demoAnalytics.trackWebSocketMetrics('disconnected', e.detail);
    });

    document.addEventListener('websocket:error', (e) => {
        window.demoAnalytics.trackWebSocketMetrics('error', e.detail);
    });
});

// Track JavaScript errors
window.addEventListener('error', (e) => {
    window.demoAnalytics.trackError(e.error || e, {
        filename: e.filename,
        lineno: e.lineno,
        colno: e.colno
    });
});

// Track unhandled promise rejections
window.addEventListener('unhandledrejection', (e) => {
    window.demoAnalytics.trackError(e.reason, {
        type: 'unhandled_promise_rejection'
    });
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DemoAnalyticsTracker;
}