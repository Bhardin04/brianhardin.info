/**
 * Analytics Dashboard Component
 * Provides real-time visualization of analytics and performance data
 */

class AnalyticsDashboard {
    constructor() {
        this.isVisible = false;
        this.dashboard = null;
        this.charts = new Map();
        this.updateInterval = null;
        this.refreshRate = 5000; // 5 seconds

        this.initialize();
    }

    /**
     * Initialize dashboard
     */
    initialize() {
        this.createDashboard();
        this.setupEventListeners();
    }

    /**
     * Show analytics dashboard
     */
    show() {
        if (this.isVisible) return;

        this.createDashboard();
        this.isVisible = true;
        this.startUpdating();

        // Animate in
        requestAnimationFrame(() => {
            this.dashboard.style.opacity = '1';
        });
    }

    /**
     * Hide analytics dashboard
     */
    hide() {
        if (!this.isVisible || !this.dashboard) return;

        this.isVisible = false;
        this.stopUpdating();

        // Animate out
        this.dashboard.style.opacity = '0';

        setTimeout(() => {
            if (this.dashboard && this.dashboard.parentElement) {
                this.dashboard.parentElement.removeChild(this.dashboard);
            }
            this.dashboard = null;
        }, 300);
    }

    /**
     * Create dashboard UI
     */
    createDashboard() {
        if (this.dashboard) return;

        this.dashboard = document.createElement('div');
        this.dashboard.className = 'analytics-dashboard';
        this.dashboard.style.opacity = '0';
        this.dashboard.style.transition = 'opacity 0.3s ease';

        this.dashboard.innerHTML = `
            <div class="analytics-content">
                <div class="analytics-header">
                    <h2 class="text-xl font-bold text-gray-900 dark:text-white">Analytics Dashboard</h2>
                    <div class="analytics-controls">
                        <button id="export-analytics" class="btn-secondary">Export Data</button>
                        <button id="refresh-analytics" class="btn-secondary">Refresh</button>
                        <button id="close-analytics" class="btn-close">×</button>
                    </div>
                </div>

                <div class="analytics-grid">
                    ${this.createOverviewSection()}
                    ${this.createPerformanceSection()}
                    ${this.createEngagementSection()}
                    ${this.createErrorsSection()}
                    ${this.createHeatmapSection()}
                    ${this.createRealtimeSection()}
                </div>
            </div>
        `;

        document.body.appendChild(this.dashboard);
        this.attachEventListeners();
        this.updateDashboard();
    }

    /**
     * Create overview section
     */
    createOverviewSection() {
        const summary = window.demoAnalytics?.getAnalyticsSummary() || {};
        const performanceStatus = window.performanceMonitor?.getStatus() || 'unknown';

        return `
            <div class="analytics-section overview-section">
                <h3 class="section-title">Session Overview</h3>
                <div class="overview-grid">
                    <div class="metric-card">
                        <div class="metric-value">${summary.eventCount || 0}</div>
                        <div class="metric-label">Events Tracked</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${Math.round((summary.sessionDuration || 0) / 60000)}m</div>
                        <div class="metric-label">Session Duration</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${summary.pageViews || 0}</div>
                        <div class="metric-label">Page Views</div>
                    </div>
                    <div class="metric-card status-${performanceStatus}">
                        <div class="metric-value">${performanceStatus.toUpperCase()}</div>
                        <div class="metric-label">Performance Status</div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Create performance section
     */
    createPerformanceSection() {
        return `
            <div class="analytics-section performance-section">
                <h3 class="section-title">Performance Metrics</h3>
                <div class="chart-container">
                    <canvas id="performance-chart" width="400" height="200"></canvas>
                </div>
                <div class="performance-details" id="performance-details">
                    Loading performance data...
                </div>
            </div>
        `;
    }

    /**
     * Create engagement section
     */
    createEngagementSection() {
        return `
            <div class="analytics-section engagement-section">
                <h3 class="section-title">User Engagement</h3>
                <div class="engagement-grid">
                    <div class="chart-container">
                        <canvas id="engagement-chart" width="300" height="150"></canvas>
                    </div>
                    <div class="engagement-stats" id="engagement-stats">
                        <div class="stat-item">
                            <span class="stat-label">Interactions:</span>
                            <span class="stat-value" id="interaction-count">-</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Features Used:</span>
                            <span class="stat-value" id="features-count">-</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Exports:</span>
                            <span class="stat-value" id="exports-count">-</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Current Demo:</span>
                            <span class="stat-value" id="current-demo">-</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Create errors section
     */
    createErrorsSection() {
        return `
            <div class="analytics-section errors-section">
                <h3 class="section-title">Errors & Alerts</h3>
                <div class="errors-list" id="errors-list">
                    Loading error data...
                </div>
            </div>
        `;
    }

    /**
     * Create heatmap section
     */
    createHeatmapSection() {
        return `
            <div class="analytics-section heatmap-section">
                <h3 class="section-title">Interaction Heatmap</h3>
                <div class="heatmap-container" id="heatmap-container">
                    <div class="heatmap-placeholder">
                        Interaction heatmap will appear here as you use the demo
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Create real-time section
     */
    createRealtimeSection() {
        return `
            <div class="analytics-section realtime-section">
                <h3 class="section-title">Real-time Activity</h3>
                <div class="activity-feed" id="activity-feed">
                    <div class="activity-item">
                        <span class="activity-time">${new Date().toLocaleTimeString()}</span>
                        <span class="activity-text">Analytics dashboard opened</span>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Attach event listeners
     */
    attachEventListeners() {
        // Close dashboard
        this.dashboard.querySelector('#close-analytics').addEventListener('click', () => {
            this.hide();
        });

        // Export data
        this.dashboard.querySelector('#export-analytics').addEventListener('click', () => {
            this.exportAnalyticsData();
        });

        // Refresh dashboard
        this.dashboard.querySelector('#refresh-analytics').addEventListener('click', () => {
            this.updateDashboard();
        });

        // Click outside to close
        this.dashboard.addEventListener('click', (e) => {
            if (e.target === this.dashboard) {
                this.hide();
            }
        });
    }

    /**
     * Setup global event listeners
     */
    setupEventListeners() {
        // Listen for new analytics events
        document.addEventListener('analytics:event', (e) => {
            this.addActivityItem(e.detail);
        });

        // Listen for performance alerts
        document.addEventListener('performance:alert', (e) => {
            this.addActivityItem({
                type: 'performance_alert',
                data: e.detail
            });
        });
    }

    /**
     * Start updating dashboard
     */
    startUpdating() {
        if (this.updateInterval) return;

        this.updateInterval = setInterval(() => {
            this.updateDashboard();
        }, this.refreshRate);
    }

    /**
     * Stop updating dashboard
     */
    stopUpdating() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }

    /**
     * Update dashboard with latest data
     */
    updateDashboard() {
        if (!this.isVisible || !this.dashboard) return;

        this.updateOverviewSection();
        this.updatePerformanceSection();
        this.updateEngagementSection();
        this.updateErrorsSection();
        this.updateHeatmapSection();
    }

    /**
     * Update overview section
     */
    updateOverviewSection() {
        const summary = window.demoAnalytics?.getAnalyticsSummary() || {};
        const performanceStatus = window.performanceMonitor?.getStatus() || 'unknown';

        // Update metric cards
        const metricCards = this.dashboard.querySelectorAll('.metric-card');
        if (metricCards.length >= 4) {
            metricCards[0].querySelector('.metric-value').textContent = summary.eventCount || 0;
            metricCards[1].querySelector('.metric-value').textContent = Math.round((summary.sessionDuration || 0) / 60000) + 'm';
            metricCards[2].querySelector('.metric-value').textContent = summary.pageViews || 0;
            metricCards[3].querySelector('.metric-value').textContent = performanceStatus.toUpperCase();
            metricCards[3].className = `metric-card status-${performanceStatus}`;
        }
    }

    /**
     * Update performance section
     */
    updatePerformanceSection() {
        const performanceSummary = window.performanceMonitor?.getPerformanceSummary();
        if (!performanceSummary) return;

        // Update performance chart
        this.updatePerformanceChart(performanceSummary);

        // Update performance details
        const detailsElement = this.dashboard.querySelector('#performance-details');
        if (detailsElement) {
            detailsElement.innerHTML = `
                <div class="performance-metric">
                    <span class="metric-name">Memory Usage:</span>
                    <span class="metric-value">${performanceSummary.averageMemoryUsage.toFixed(1)}%</span>
                </div>
                <div class="performance-metric">
                    <span class="metric-name">Average FPS:</span>
                    <span class="metric-value">${performanceSummary.averageFPS.toFixed(0)}</span>
                </div>
                <div class="performance-metric">
                    <span class="metric-name">Connection Stability:</span>
                    <span class="metric-value">${(performanceSummary.connectionStability * 100).toFixed(1)}%</span>
                </div>
                <div class="performance-metric">
                    <span class="metric-name">Active Alerts:</span>
                    <span class="metric-value">${performanceSummary.alertCount}</span>
                </div>
            `;
        }
    }

    /**
     * Update engagement section
     */
    updateEngagementSection() {
        const summary = window.demoAnalytics?.getAnalyticsSummary() || {};

        // Update engagement stats
        const interactionCount = this.dashboard.querySelector('#interaction-count');
        const featuresCount = this.dashboard.querySelector('#features-count');
        const exportsCount = this.dashboard.querySelector('#exports-count');
        const currentDemo = this.dashboard.querySelector('#current-demo');

        if (interactionCount) interactionCount.textContent = summary.currentDemo?.interactions || 0;
        if (featuresCount) featuresCount.textContent = summary.currentDemo?.features?.size || 0;
        if (exportsCount) exportsCount.textContent = summary.currentDemo?.exports || 0;
        if (currentDemo) currentDemo.textContent = summary.currentDemo?.type || 'None';

        // Update engagement chart
        this.updateEngagementChart(summary);
    }

    /**
     * Update errors section
     */
    updateErrorsSection() {
        const alerts = window.performanceMonitor?.alerts || [];
        const recentAlerts = alerts.slice(-5).reverse(); // Last 5 alerts, newest first

        const errorsList = this.dashboard.querySelector('#errors-list');
        if (!errorsList) return;

        if (recentAlerts.length === 0) {
            errorsList.innerHTML = '<div class="no-errors">No recent errors or alerts</div>';
            return;
        }

        errorsList.innerHTML = recentAlerts.map(alert => `
            <div class="error-item ${alert.severity}">
                <div class="error-header">
                    <span class="error-category">${alert.category}</span>
                    <span class="error-time">${new Date(alert.timestamp).toLocaleTimeString()}</span>
                </div>
                <div class="error-message">${alert.message}</div>
            </div>
        `).join('');
    }

    /**
     * Update heatmap section
     */
    updateHeatmapSection() {
        const heatmapData = window.demoAnalytics?.getHeatmapData() || {};
        const container = this.dashboard.querySelector('#heatmap-container');
        if (!container) return;

        if (Object.keys(heatmapData).length === 0) {
            container.innerHTML = '<div class="heatmap-placeholder">No interaction data yet. Start using the demo to see heatmap data.</div>';
            return;
        }

        // Create simplified heatmap visualization
        const maxClicks = Math.max(...Object.values(heatmapData));
        const heatmapHTML = Object.entries(heatmapData).map(([coords, clicks]) => {
            const [x, y] = coords.split(',').map(Number);
            const intensity = clicks / maxClicks;
            return `
                <div class="heatmap-point" style="
                    left: ${x * 50}px;
                    top: ${y * 50}px;
                    opacity: ${intensity};
                    background-color: hsl(${(1 - intensity) * 120}, 100%, 50%);
                " title="${clicks} interactions"></div>
            `;
        }).join('');

        container.innerHTML = `
            <div class="heatmap-visualization" style="position: relative; height: 200px; overflow: hidden;">
                ${heatmapHTML}
            </div>
        `;
    }

    /**
     * Update performance chart
     */
    updatePerformanceChart(data) {
        const canvas = this.dashboard.querySelector('#performance-chart');
        if (!canvas) return;

        // Simplified chart rendering (in a real implementation, use Chart.js)
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw memory usage bar
        const memoryPercentage = data.averageMemoryUsage / 100;
        ctx.fillStyle = memoryPercentage > 0.8 ? '#ef4444' : memoryPercentage > 0.6 ? '#f59e0b' : '#10b981';
        ctx.fillRect(10, 10, canvas.width * memoryPercentage - 20, 30);

        // Draw FPS indicator
        const fpsPercentage = Math.min(data.averageFPS / 60, 1);
        ctx.fillStyle = fpsPercentage < 0.5 ? '#ef4444' : fpsPercentage < 0.75 ? '#f59e0b' : '#10b981';
        ctx.fillRect(10, 50, canvas.width * fpsPercentage - 20, 30);

        // Labels
        ctx.fillStyle = '#374151';
        ctx.font = '12px sans-serif';
        ctx.fillText(`Memory: ${data.averageMemoryUsage.toFixed(1)}%`, 15, 30);
        ctx.fillText(`FPS: ${data.averageFPS.toFixed(0)}`, 15, 70);
    }

    /**
     * Update engagement chart
     */
    updateEngagementChart(data) {
        const canvas = this.dashboard.querySelector('#engagement-chart');
        if (!canvas || !data.currentDemo) return;

        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Simple pie chart for feature usage
        const features = Array.from(data.currentDemo.features || []);
        if (features.length === 0) return;

        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const radius = Math.min(centerX, centerY) - 10;

        const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];
        let currentAngle = 0;

        features.forEach((feature, index) => {
            const sliceAngle = (2 * Math.PI) / features.length;

            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
            ctx.closePath();
            ctx.fillStyle = colors[index % colors.length];
            ctx.fill();

            currentAngle += sliceAngle;
        });
    }

    /**
     * Add activity item to real-time feed
     */
    addActivityItem(event) {
        if (!this.isVisible || !this.dashboard) return;

        const activityFeed = this.dashboard.querySelector('#activity-feed');
        if (!activityFeed) return;

        const activityItem = document.createElement('div');
        activityItem.className = 'activity-item';
        activityItem.innerHTML = `
            <span class="activity-time">${new Date().toLocaleTimeString()}</span>
            <span class="activity-text">${this.formatActivityText(event)}</span>
        `;

        activityFeed.insertBefore(activityItem, activityFeed.firstChild);

        // Keep only last 10 items
        const items = activityFeed.querySelectorAll('.activity-item');
        if (items.length > 10) {
            items[items.length - 1].remove();
        }
    }

    /**
     * Format activity text
     */
    formatActivityText(event) {
        switch (event.type) {
            case 'interaction':
                return `User ${event.data.action} on ${event.data.elementType || 'element'}`;
            case 'export':
                return `Chart exported as ${event.data.format.toUpperCase()}`;
            case 'feature_usage':
                return `Feature used: ${event.data.feature}`;
            case 'error':
                return `Error: ${event.data.message}`;
            case 'performance_alert':
                return `Performance alert: ${event.data.message}`;
            default:
                return `Event: ${event.type}`;
        }
    }

    /**
     * Export analytics data
     */
    exportAnalyticsData() {
        const analyticsData = window.demoAnalytics?.exportAnalyticsData();
        const performanceData = window.performanceMonitor?.exportPerformanceData();

        // Combine both exports
        const combinedData = {
            analytics: analyticsData,
            performance: performanceData,
            exportedAt: new Date().toISOString(),
            exportType: 'combined_dashboard_export'
        };

        const blob = new Blob([JSON.stringify(combinedData, null, 2)], {
            type: 'application/json'
        });

        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `analytics_dashboard_${new Date().toISOString().split('T')[0]}.json`;

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        URL.revokeObjectURL(url);
    }
}

// CSS styles for analytics dashboard
const dashboardStyles = `
    .analytics-dashboard {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        padding: 2rem;
    }

    .analytics-content {
        background: white;
        border-radius: 0.75rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        width: 100%;
        max-width: 1200px;
        max-height: 90vh;
        overflow-y: auto;
        padding: 1.5rem;
    }

    .dark .analytics-content {
        background: #1f2937;
        color: white;
    }

    .analytics-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e5e7eb;
    }

    .dark .analytics-header {
        border-bottom-color: #374151;
    }

    .analytics-controls {
        display: flex;
        gap: 0.5rem;
    }

    .btn-secondary {
        background: #6b7280;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        cursor: pointer;
        font-size: 0.875rem;
        transition: background-color 0.2s;
    }

    .btn-secondary:hover {
        background: #4b5563;
    }

    .btn-close {
        background: #ef4444;
        color: white;
        border: none;
        padding: 0.5rem 0.75rem;
        border-radius: 0.375rem;
        cursor: pointer;
        font-size: 1.25rem;
        line-height: 1;
    }

    .btn-close:hover {
        background: #dc2626;
    }

    .analytics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        gap: 1.5rem;
    }

    .analytics-section {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1.5rem;
    }

    .dark .analytics-section {
        background: #374151;
        border-color: #4b5563;
    }

    .section-title {
        font-size: 1.125rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #111827;
    }

    .dark .section-title {
        color: #f9fafb;
    }

    .overview-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
    }

    .metric-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 0.375rem;
        padding: 1rem;
        text-align: center;
    }

    .dark .metric-card {
        background: #1f2937;
        border-color: #374151;
    }

    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #111827;
    }

    .dark .metric-value {
        color: #f9fafb;
    }

    .metric-label {
        font-size: 0.875rem;
        color: #6b7280;
        margin-top: 0.25rem;
    }

    .dark .metric-label {
        color: #9ca3af;
    }

    .status-good .metric-value {
        color: #10b981;
    }

    .status-warning .metric-value {
        color: #f59e0b;
    }

    .status-critical .metric-value {
        color: #ef4444;
    }

    .chart-container {
        margin-bottom: 1rem;
    }

    .engagement-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }

    .engagement-stats {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .stat-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem;
        background: white;
        border-radius: 0.25rem;
        border: 1px solid #e5e7eb;
    }

    .dark .stat-item {
        background: #1f2937;
        border-color: #374151;
    }

    .stat-label {
        font-weight: 500;
        color: #6b7280;
    }

    .dark .stat-label {
        color: #9ca3af;
    }

    .stat-value {
        font-weight: 600;
        color: #111827;
    }

    .dark .stat-value {
        color: #f9fafb;
    }

    .errors-list {
        max-height: 200px;
        overflow-y: auto;
    }

    .error-item {
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        border-radius: 0.375rem;
        border-left: 4px solid;
    }

    .error-item.warning {
        background: #fef3c7;
        border-color: #f59e0b;
    }

    .error-item.critical {
        background: #fee2e2;
        border-color: #ef4444;
    }

    .dark .error-item.warning {
        background: #451a03;
        color: #fbbf24;
    }

    .dark .error-item.critical {
        background: #450a0a;
        color: #f87171;
    }

    .error-header {
        display: flex;
        justify-content: space-between;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }

    .error-message {
        font-size: 0.875rem;
        opacity: 0.9;
    }

    .activity-feed {
        max-height: 200px;
        overflow-y: auto;
    }

    .activity-item {
        display: flex;
        gap: 0.75rem;
        padding: 0.5rem;
        border-bottom: 1px solid #e5e7eb;
        font-size: 0.875rem;
    }

    .dark .activity-item {
        border-bottom-color: #374151;
    }

    .activity-time {
        color: #6b7280;
        font-weight: 500;
        min-width: 80px;
    }

    .dark .activity-time {
        color: #9ca3af;
    }

    .activity-text {
        color: #111827;
    }

    .dark .activity-text {
        color: #f9fafb;
    }

    .heatmap-placeholder {
        text-align: center;
        color: #6b7280;
        padding: 2rem;
        font-style: italic;
    }

    .dark .heatmap-placeholder {
        color: #9ca3af;
    }

    .heatmap-point {
        position: absolute;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        pointer-events: none;
    }

    .performance-metric {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem;
        margin-bottom: 0.25rem;
        background: white;
        border-radius: 0.25rem;
        border: 1px solid #e5e7eb;
    }

    .dark .performance-metric {
        background: #1f2937;
        border-color: #374151;
    }

    .metric-name {
        font-weight: 500;
        color: #6b7280;
    }

    .dark .metric-name {
        color: #9ca3af;
    }

    .no-errors {
        text-align: center;
        color: #10b981;
        padding: 2rem;
        font-weight: 500;
    }
`;

// Inject styles
if (!document.querySelector('#analytics-dashboard-styles')) {
    const styleSheet = document.createElement('style');
    styleSheet.id = 'analytics-dashboard-styles';
    styleSheet.textContent = dashboardStyles;
    document.head.appendChild(styleSheet);
}

// Global instance
window.analyticsDashboard = new AnalyticsDashboard();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AnalyticsDashboard;
}
